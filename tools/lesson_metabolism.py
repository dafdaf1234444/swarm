#!/usr/bin/env python3
"""Lesson Metabolism — find tensioned lesson pairs and propose syntheses.

Unlike compaction (shortens) or recombination (finds missing edges), metabolism
identifies lessons that are in TENSION (contradictory or complementary claims)
and proposes a synthesis that supersedes both. Chemical reaction, not editing.

Usage:
    python3 tools/lesson_metabolism.py                 # Find top metabolizable pairs
    python3 tools/lesson_metabolism.py --top 20        # Top 20 pairs
    python3 tools/lesson_metabolism.py --json          # Machine-readable
"""
import argparse, json, os, re, sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LESSONS_DIR = ROOT / "memory" / "lessons"
CHALLENGES_PATH = ROOT / "beliefs" / "CHALLENGES.md"
CONFLICTS_PATH = ROOT / "beliefs" / "CONFLICTS.md"


def parse_lesson(path):
    """Parse a lesson file into structured fields."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return None
    lines = text.strip().splitlines()
    if not lines:
        return None

    lesson = {"path": str(path), "id": path.stem, "text": text, "lines": lines}

    # Extract header fields — handle both "Key: value" and "Key: val | Key2: val2" formats
    for line in lines[:12]:
        if line.startswith("Supports:"):
            lesson["supports"] = [x.strip() for x in line[9:].split(",") if x.strip()]
        elif line.startswith("Contradicts:"):
            lesson["contradicts"] = [x.strip() for x in line[12:].split(",") if x.strip()]
        elif line.startswith("Cites:"):
            lesson["cites"] = [x.strip() for x in line[6:].split(",") if x.strip()]
        # Parse pipe-separated metadata (Session: S473 | Domain: meta | Sharpe: 9 | Level: L5)
        parts = line.split("|")
        for p in parts:
            p = p.strip()
            if p.startswith("Domain:"):
                lesson["domain"] = p[7:].strip().split(",")[0].strip()
            elif p.startswith("Confidence:"):
                lesson["confidence"] = p[11:].strip()
            elif p.startswith("Level:"):
                lesson["level"] = p[6:].strip()
            elif p.startswith("Sharpe:"):
                try:
                    lesson["sharpe"] = int(p[7:].strip())
                except ValueError:
                    pass

    # Extract claim/finding (## Claim or ## Finding)
    claim_start = None
    for i, line in enumerate(lines):
        if line.startswith("## Claim") or line.startswith("## Finding"):
            claim_start = i + 1
        elif claim_start and line.startswith("## "):
            break
        elif claim_start:
            lesson.setdefault("claim", "")
            lesson["claim"] += line + " "

    if "claim" in lesson:
        lesson["claim"] = lesson["claim"].strip()

    # Extract L-NNN references
    lesson["refs"] = set(re.findall(r'L-\d+', text))
    lesson["refs"].discard(lesson["id"])

    return lesson


def find_tension_pairs(lessons):
    """Find pairs of lessons in tension (explicit contradictions, shared refs with different conclusions)."""
    pairs = []

    # 1. Explicit contradictions (Contradicts: field)
    for lid, lesson in lessons.items():
        for contra in lesson.get("contradicts", []):
            if contra in lessons and contra > lid:  # avoid duplicates
                pairs.append({
                    "l1": lid, "l2": contra,
                    "type": "explicit_contradiction",
                    "score": 10.0,
                    "reason": f"{lid} explicitly contradicts {contra}",
                })

    # 2. Same domain, different conclusions on shared topic
    # Group by domain
    by_domain = defaultdict(list)
    for lid, lesson in lessons.items():
        d = lesson.get("domain", "unknown")
        by_domain[d].append(lid)

    for domain, lids in by_domain.items():
        if len(lids) < 2:
            continue
        for i in range(len(lids)):
            for j in range(i + 1, len(lids)):
                l1, l2 = lids[i], lids[j]
                lesson1, lesson2 = lessons[l1], lessons[l2]

                # Shared references = discussing same topic
                shared_refs = lesson1["refs"] & lesson2["refs"]
                if len(shared_refs) < 2:
                    continue

                # Check for tension signals in claims
                claim1 = lesson1.get("claim", "").lower()
                claim2 = lesson2.get("claim", "").lower()

                tension_words = ["falsified", "incorrect", "wrong", "not ", "however",
                                 "contradicts", "overturns", "revises", "but ", "actually",
                                 "corrects", "unlike", "versus", "opposite"]

                tension_score = sum(1 for w in tension_words
                                    if w in claim1 or w in claim2)

                if tension_score == 0 and len(shared_refs) < 4:
                    continue

                score = len(shared_refs) * 1.5 + tension_score * 2.0

                # Bonus for level difference (L3 + L2 = synthesis opportunity)
                lev1 = lesson1.get("level", "")
                lev2 = lesson2.get("level", "")
                if lev1 != lev2 and lev1 and lev2:
                    score += 1.0

                pairs.append({
                    "l1": l1, "l2": l2,
                    "type": "shared_topic_tension",
                    "score": round(score, 1),
                    "shared_refs": len(shared_refs),
                    "tension_words": tension_score,
                    "reason": f"Same domain ({domain}), {len(shared_refs)} shared refs, "
                              f"{tension_score} tension signals",
                })

    # 3. Cross-domain pairs that cite each other with tension
    for lid, lesson in lessons.items():
        for ref in lesson.get("contradicts", []):
            if ref in lessons:
                other = lessons[ref]
                if lesson.get("domain") != other.get("domain"):
                    pairs.append({
                        "l1": lid, "l2": ref,
                        "type": "cross_domain_tension",
                        "score": 8.0,
                        "reason": f"Cross-domain contradiction: {lesson.get('domain')} vs {other.get('domain')}",
                    })

    # Deduplicate (normalize pair ordering)
    seen = set()
    unique_pairs = []
    for p in pairs:
        key = tuple(sorted([p["l1"], p["l2"]]))
        if key not in seen:
            seen.add(key)
            unique_pairs.append(p)

    unique_pairs.sort(key=lambda x: -x["score"])
    return unique_pairs


def propose_synthesis(pair, lessons):
    """Generate a synthesis proposal for a tensioned pair."""
    l1, l2 = lessons.get(pair["l1"]), lessons.get(pair["l2"])
    if not l1 or not l2:
        return None

    claim1 = l1.get("claim", "(no claim)")[:120]
    claim2 = l2.get("claim", "(no claim)")[:120]

    return {
        "pair": (pair["l1"], pair["l2"]),
        "type": pair["type"],
        "score": pair["score"],
        "l1_claim": claim1,
        "l2_claim": claim2,
        "l1_domain": l1.get("domain", "?"),
        "l2_domain": l2.get("domain", "?"),
        "l1_level": l1.get("level", "?"),
        "l2_level": l2.get("level", "?"),
        "synthesis_prompt": f"Synthesize {pair['l1']} and {pair['l2']}: "
                           f"what higher-order principle resolves both? "
                           f"Archive both parents if synthesis succeeds.",
    }


def main():
    ap = argparse.ArgumentParser(description="Lesson metabolism — find tensioned pairs for synthesis")
    ap.add_argument("--top", type=int, default=15, help="Show top N pairs")
    ap.add_argument("--json", action="store_true", help="JSON output")
    ap.add_argument("--min-score", type=float, default=3.0, help="Min tension score")
    args = ap.parse_args()

    # Parse all lessons
    lessons = {}
    for f in sorted(LESSONS_DIR.glob("L-*.md")):
        parsed = parse_lesson(f)
        if parsed:
            # Normalize ID
            m = re.match(r'L-0*(\d+)', parsed["id"])
            if m:
                parsed["id"] = f"L-{m.group(1)}"
            lessons[parsed["id"]] = parsed

    # Find tensions
    pairs = find_tension_pairs(lessons)
    pairs = [p for p in pairs if p["score"] >= args.min_score]

    # Propose syntheses
    syntheses = []
    for p in pairs[:args.top]:
        s = propose_synthesis(p, lessons)
        if s:
            syntheses.append(s)

    if args.json:
        print(json.dumps({
            "total_lessons": len(lessons),
            "tension_pairs": len(pairs),
            "top_syntheses": syntheses,
        }, indent=2))
        return

    print(f"=== LESSON METABOLISM — {len(lessons)} lessons scanned ===")
    print(f"  Tension pairs found: {len(pairs)} (score >= {args.min_score})")
    print()

    if not syntheses:
        print("  No metabolizable pairs found above threshold.")
        return

    print(f"--- TOP {len(syntheses)} SYNTHESIS CANDIDATES ---")
    for i, s in enumerate(syntheses, 1):
        l1, l2 = s["pair"]
        print(f"\n  #{i}  {l1} × {l2}  score={s['score']:.1f}  type={s['type']}")
        print(f"    {l1} [{s['l1_domain']}/{s['l1_level']}]: {s['l1_claim'][:100]}")
        print(f"    {l2} [{s['l2_domain']}/{s['l2_level']}]: {s['l2_claim'][:100]}")
        print(f"    → {s['synthesis_prompt'][:120]}")

    print(f"\n--- PRESCRIPTION ---")
    print(f"  {len(pairs)} pairs have metabolic potential")
    print(f"  Explicit contradictions: {sum(1 for p in pairs if p['type'] == 'explicit_contradiction')}")
    print(f"  Shared-topic tensions: {sum(1 for p in pairs if p['type'] == 'shared_topic_tension')}")
    print(f"  Cross-domain tensions: {sum(1 for p in pairs if p['type'] == 'cross_domain_tension')}")
    print(f"  Target: synthesize top 3 per session → net lesson reduction")


if __name__ == "__main__":
    main()
