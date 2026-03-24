#!/usr/bin/env python3
"""Cross-file belief consistency checker — detects belief superposition.

Belief superposition (L-1648): contradictory claims about the same PHIL/B-ID
coexist in different files, with neither referencing the other. The system
can cite whichever frame serves the current argument (Orwell's doublethink).

This tool scans lessons for assertions about PHIL claims, then checks whether
those assertions are consistent with the claim's ground truth in PHILOSOPHY.md.
Flags unresolved contradictions.

Usage:
  python3 tools/belief_consistency.py              # full report
  python3 tools/belief_consistency.py --json       # machine-readable
  python3 tools/belief_consistency.py --phil PHIL-16  # single claim

Closes the tool gap identified in L-1648.
"""

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PHIL_PATH = REPO / "beliefs" / "PHILOSOPHY.md"
LESSONS_DIR = REPO / "memory" / "lessons"

# Keywords indicating positive vs negative status assertions
POS_WORDS = {"confirmed", "grounded", "achieved", "beneficiary", "demonstrated", "measured"}
NEG_WORDS = {"0 external", "aspirational", "not grounded", "zero external", "no evidence",
             "not yet", "remains untested", "0 beneficiar"}


def _read(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


def parse_phil_claims(text: str) -> dict:
    """Extract PHIL-N claims with their ground truth blocks."""
    claims = {}
    lines = text.split("\n")
    i = 0
    while i < len(lines):
        m = re.search(r"\[PHIL-(\d+[a-z]?)\]", lines[i])
        if m:
            phil_id = f"PHIL-{m.group(1)}"
            ground_truth = ""
            status = ""
            block_lines = [lines[i]]
            j = i + 1
            while j < len(lines):
                if re.match(r"^##\s", lines[j]):
                    break
                if re.search(r"\[PHIL-\d+[a-z]?\]", lines[j]) and j != i:
                    break
                block_lines.append(lines[j])
                if "*Ground truth" in lines[j] or "*ground truth" in lines[j]:
                    gt_lines = [lines[j]]
                    k = j + 1
                    while k < len(lines) and lines[k].strip() and not re.match(r"^(##|\[PHIL)", lines[k]):
                        gt_lines.append(lines[k])
                        k += 1
                    ground_truth = "\n".join(gt_lines)
                    st = re.search(
                        r"\*\*(grounded|aspirational|partial|theorized|"
                        r"partially grounded|reframed)\*\*",
                        ground_truth, re.IGNORECASE
                    )
                    if st:
                        status = st.group(1).lower()
                j += 1
            block = "\n".join(block_lines)
            claims[phil_id] = {
                "text": block,
                "ground_truth": ground_truth,
                "status": status,
                "dropped": "DROPPED" in block or "SUPERSEDED" in block,
            }
        i += 1
    return claims


def build_lesson_index() -> dict:
    """Single-pass scan of all lessons. Returns {lesson_id: {text, session, phil_refs, all_L_refs}}."""
    index = {}
    if not LESSONS_DIR.exists():
        return index
    phil_pat = re.compile(r"PHIL-\d+[a-z]?")
    l_pat = re.compile(r"L-\d+")
    for f in LESSONS_DIR.iterdir():
        if not f.name.endswith(".md"):
            continue
        lid = re.match(r"(L-\d+)", f.stem)
        if not lid:
            continue
        lesson_id = lid.group(1)
        text = _read(f)
        phil_refs = set(phil_pat.findall(text))
        if not phil_refs:
            continue
        sm = re.search(r"(?:\*\*)?Session(?:\*\*)?:\s*S(\d+)", text)
        session = int(sm.group(1)) if sm else 0
        # Extract lines mentioning each PHIL ref
        lines_by_phil = defaultdict(list)
        for line in text.split("\n"):
            for pid in phil_pat.findall(line):
                lines_by_phil[pid].append(line.strip())
        all_l_refs = set(l_pat.findall(text))
        index[lesson_id] = {
            "text_head": text[:1500],
            "session": session,
            "phil_refs": phil_refs,
            "lines_by_phil": dict(lines_by_phil),
            "all_l_refs": all_l_refs,
        }
    return index


def classify_assertion(assertion: str, ground_truth: str, status: str) -> str:
    """Classify whether an assertion potentially contradicts the ground truth."""
    a_low = assertion.lower()
    gt_low = ground_truth.lower()
    a_pos = any(w in a_low for w in POS_WORDS)
    a_neg = any(w in a_low for w in NEG_WORDS)
    gt_pos = any(w in gt_low for w in POS_WORDS)
    gt_neg = any(w in gt_low for w in NEG_WORDS)
    if a_pos and gt_neg:
        return "potential_conflict"
    if a_neg and gt_pos:
        return "potential_conflict"
    if status == "aspirational" and "grounded" in a_low:
        return "status_conflict"
    if status == "grounded" and "aspirational" in a_low:
        return "status_conflict"
    return "consistent"


def check_conflicts(claims: dict, lesson_index: dict) -> list:
    """Check lesson assertions against ground truth."""
    conflicts = []
    for phil_id, claim in claims.items():
        if claim["dropped"]:
            continue
        gt = claim["ground_truth"]
        status = claim["status"]
        if not gt:
            continue
        gt_session = 0
        sm = re.search(r"S(\d+)", gt)
        if sm:
            gt_session = int(sm.group(1))

        for lid, ldata in lesson_index.items():
            if phil_id not in ldata["phil_refs"]:
                continue
            for assertion in ldata["lines_by_phil"].get(phil_id, []):
                cls = classify_assertion(assertion, gt, status)
                if cls in ("potential_conflict", "status_conflict"):
                    conflicts.append({
                        "phil_id": phil_id,
                        "lesson_id": lid,
                        "lesson_session": ldata["session"],
                        "gt_session": gt_session,
                        "type": cls,
                        "assertion": assertion[:200],
                        "gt_status": status,
                        "temporal": "pre-gt" if ldata["session"] < gt_session else "post-gt",
                    })
    return conflicts


def check_isolation(claims: dict, lesson_index: dict) -> list:
    """Detect belief superposition: lessons about the same claim that don't
    reference each other and make potentially conflicting assertions."""
    isolations = []
    for phil_id, claim in claims.items():
        if claim["dropped"]:
            continue
        # Gather lessons referencing this claim
        relevant = []
        for lid, ldata in lesson_index.items():
            if phil_id in ldata["phil_refs"]:
                lines = ldata["lines_by_phil"].get(phil_id, [])
                joined = " ".join(lines).lower()
                is_pos = any(w in joined for w in POS_WORDS)
                is_neg = any(w in joined for w in NEG_WORDS)
                if is_pos or is_neg:
                    relevant.append({
                        "id": lid,
                        "session": ldata["session"],
                        "l_refs": ldata["all_l_refs"],
                        "assertions": lines[:3],
                        "pos": is_pos,
                        "neg": is_neg,
                    })
        if len(relevant) < 2:
            continue
        # Find isolated contradictory pairs
        for i, l1 in enumerate(relevant):
            for l2 in relevant[i + 1:]:
                # Neither references the other
                if l2["id"] in l1["l_refs"] or l1["id"] in l2["l_refs"]:
                    continue
                # One positive, one negative
                if (l1["pos"] and l2["neg"]) or (l1["neg"] and l2["pos"]):
                    gap = abs(l1["session"] - l2["session"])
                    isolations.append({
                        "phil_id": phil_id,
                        "lesson_a": l1["id"],
                        "session_a": l1["session"],
                        "lesson_b": l2["id"],
                        "session_b": l2["session"],
                        "assertions_a": l1["assertions"][:2],
                        "assertions_b": l2["assertions"][:2],
                        "severity": "high" if gap > 20 else "medium",
                    })
    return isolations


def main():
    args = sys.argv[1:]
    json_mode = "--json" in args
    single_phil = None
    if "--phil" in args:
        idx = args.index("--phil")
        if idx + 1 < len(args):
            single_phil = args[idx + 1]

    phil_text = _read(PHIL_PATH)
    claims = parse_phil_claims(phil_text)
    if single_phil:
        claims = {k: v for k, v in claims.items() if k == single_phil}

    # Single-pass lesson scan
    lesson_index = build_lesson_index()

    # Run checks
    conflicts = check_conflicts(claims, lesson_index)
    isolations = check_isolation(claims, lesson_index)

    # Count lessons per claim
    lessons_per_claim = {}
    for phil_id in claims:
        if claims[phil_id]["dropped"]:
            continue
        count = sum(1 for l in lesson_index.values() if phil_id in l["phil_refs"])
        lessons_per_claim[phil_id] = count

    total_claims = len([c for c in claims.values() if not c["dropped"]])

    if json_mode:
        result = {
            "total_claims": total_claims,
            "lessons_indexed": len(lesson_index),
            "conflicts": conflicts,
            "isolations": isolations,
            "lessons_per_claim": lessons_per_claim,
        }
        print(json.dumps(result, indent=2))
        return

    print(f"=== BELIEF CONSISTENCY CHECK (L-1648 superposition detector) ===")
    print(f"Claims scanned: {total_claims} active PHIL claims")
    print(f"Lessons indexed: {len(lesson_index)} (with PHIL references)")
    print()

    top = sorted(lessons_per_claim.items(), key=lambda x: -x[1])[:10]
    print("--- Most-referenced claims ---")
    for pid, count in top:
        status = claims[pid]["status"] or "unknown"
        print(f"  {pid} ({status}): {count} lessons")
    print()

    if conflicts:
        print(f"--- Ground-truth conflicts ({len(conflicts)}) ---")
        for c in sorted(conflicts, key=lambda x: x["phil_id"]):
            arrow = "<" if c["temporal"] == "pre-gt" else ">"
            print(f"  [{c['type']}] {c['phil_id']} × {c['lesson_id']} "
                  f"(S{c['lesson_session']} {arrow} GT S{c['gt_session']})")
            print(f"    says: {c['assertion'][:120]}")
            print()
    else:
        print("--- Ground-truth conflicts: none ---")
        print()

    if isolations:
        high = [i for i in isolations if i["severity"] == "high"]
        med = [i for i in isolations if i["severity"] == "medium"]
        print(f"--- Belief superposition ({len(isolations)} isolated pairs) ---")
        if high:
            print(f"  HIGH ({len(high)}):")
            for iso in high[:10]:
                print(f"    {iso['phil_id']}: {iso['lesson_a']} (S{iso['session_a']}) "
                      f"↔ {iso['lesson_b']} (S{iso['session_b']})")
                if iso["assertions_a"]:
                    print(f"      A: {iso['assertions_a'][0][:100]}")
                if iso["assertions_b"]:
                    print(f"      B: {iso['assertions_b'][0][:100]}")
            if len(high) > 10:
                print(f"    ... and {len(high) - 10} more")
        if med:
            summaries = [f"{i['phil_id']}: {i['lesson_a']}↔{i['lesson_b']}" for i in med[:5]]
            print(f"  MEDIUM ({len(med)}): {', '.join(summaries)}")
        print()
    else:
        print("--- Belief superposition: none detected ---")
        print()

    n_issues = len(conflicts) + len(isolations)
    if n_issues == 0:
        print(f"RESULT: CLEAN — no cross-file contradictions detected")
    else:
        print(f"RESULT: {n_issues} issues — {len(conflicts)} conflicts, "
              f"{len(isolations)} superpositions")
        print(f"  Rx: annotate pre-GT lessons with rejection notes (L-1648)")

    sys.exit(1 if n_issues > 0 else 0)


if __name__ == "__main__":
    main()
