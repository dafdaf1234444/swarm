#!/usr/bin/env python3
"""Principle Tournament — selection pressure on principles via explanatory competition.

Unlike principles_dedup.py (similarity-based merging), this tool measures which
principles are load-bearing by testing citation overlap: if two principles explain
the same set of lessons, the one with less exclusive coverage is an archival candidate.

Creates selection pressure on principles (r-mode → K-mode transition).

Usage:
    python3 tools/principle_tournament.py              # Full tournament
    python3 tools/principle_tournament.py --top 20     # Top 20 archival candidates
    python3 tools/principle_tournament.py --json       # Machine-readable
    python3 tools/principle_tournament.py --bracket    # Show head-to-head matchups
"""
import argparse, json, os, re, sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRINCIPLES_PATH = ROOT / "memory" / "PRINCIPLES.md"
LESSONS_DIR = ROOT / "memory" / "lessons"


def parse_principle_ids(text):
    """Extract all P-NNN IDs and their brief names from PRINCIPLES.md."""
    principles = {}
    for m in re.finditer(r'(P-\d+)\s+([^|]+?)(?:\s*\||\s*$)', text):
        pid = m.group(1)
        name = m.group(2).strip()
        # Truncate long names
        if len(name) > 80:
            name = name[:77] + "..."
        principles[pid] = name
    return principles


def parse_principle_sections(text):
    """Map P-NNN to its section in PRINCIPLES.md."""
    sections = {}
    current_section = ""
    for line in text.splitlines():
        if line.startswith("## "):
            current_section = line[3:].strip()
        for m in re.finditer(r'P-\d+', line):
            if m.group() not in sections:
                sections[m.group()] = current_section
    return sections


def scan_lesson_citations():
    """For each lesson, find which P-NNN it cites. Return {lesson_id: set(P-NNN)}."""
    lesson_principles = {}
    if not LESSONS_DIR.exists():
        return lesson_principles
    for f in LESSONS_DIR.glob("L-*.md"):
        lid = f.stem  # e.g. L-0042 or L-42
        # Normalize to L-NNN
        m = re.match(r'L-0*(\d+)', lid)
        if m:
            lid = f"L-{m.group(1)}"
        try:
            content = f.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        # Find all P-NNN references
        pids = set(re.findall(r'P-\d+', content))
        if pids:
            lesson_principles[lid] = pids
    return lesson_principles


def build_citation_index(lesson_principles):
    """Invert: {P-NNN: set(lesson_ids that cite it)}."""
    index = defaultdict(set)
    for lid, pids in lesson_principles.items():
        for pid in pids:
            index[pid].add(lid)
    return dict(index)


def find_competitions(citation_index, min_overlap=2):
    """Find principle pairs that compete: they explain overlapping lessons.

    Returns sorted list of (p1, p2, overlap_count, p1_exclusive, p2_exclusive, overlap_ratio).
    """
    pids = sorted(citation_index.keys())
    competitions = []
    for i in range(len(pids)):
        for j in range(i + 1, len(pids)):
            p1, p2 = pids[i], pids[j]
            s1, s2 = citation_index[p1], citation_index[p2]
            overlap = s1 & s2
            if len(overlap) < min_overlap:
                continue
            exclusive1 = s1 - s2
            exclusive2 = s2 - s1
            # Overlap ratio: what fraction of the smaller set is shared
            smaller = min(len(s1), len(s2))
            ratio = len(overlap) / smaller if smaller > 0 else 0
            competitions.append({
                "p1": p1, "p2": p2,
                "overlap": len(overlap),
                "p1_total": len(s1), "p2_total": len(s2),
                "p1_exclusive": len(exclusive1),
                "p2_exclusive": len(exclusive2),
                "overlap_ratio": round(ratio, 3),
                "overlap_lessons": sorted(overlap),
            })
    # Sort by overlap ratio descending (highest competition first)
    competitions.sort(key=lambda x: (-x["overlap_ratio"], -x["overlap"]))
    return competitions


def score_principles(citation_index, competitions):
    """Score each principle. Lower score = more archival-worthy.

    Score = exclusive_coverage + 0.5 * shared_coverage - redundancy_penalty
    Redundancy penalty: how often this principle loses head-to-head (less exclusive coverage).
    """
    scores = {}
    losses = defaultdict(int)
    wins = defaultdict(int)

    for comp in competitions:
        p1, p2 = comp["p1"], comp["p2"]
        # Winner has more exclusive coverage
        if comp["p1_exclusive"] > comp["p2_exclusive"]:
            wins[p1] += 1
            losses[p2] += 1
        elif comp["p2_exclusive"] > comp["p1_exclusive"]:
            wins[p2] += 1
            losses[p1] += 1
        else:
            # Tie — the one with more total citations wins
            if comp["p1_total"] >= comp["p2_total"]:
                wins[p1] += 1
                losses[p2] += 1
            else:
                wins[p2] += 1
                losses[p1] += 1

    for pid, lessons in citation_index.items():
        total = len(lessons)
        # Count exclusive lessons (not shared with ANY other principle)
        exclusive = set(lessons)
        for other_pid, other_lessons in citation_index.items():
            if other_pid != pid:
                exclusive -= other_lessons

        w = wins.get(pid, 0)
        l = losses.get(pid, 0)
        win_rate = w / (w + l) if (w + l) > 0 else 0.5

        scores[pid] = {
            "total_citations": total,
            "exclusive_citations": len(exclusive),
            "wins": w,
            "losses": l,
            "win_rate": round(win_rate, 3),
            # Composite: exclusive coverage is king, then win rate, then total
            "tournament_score": round(len(exclusive) + win_rate * 2 + total * 0.1, 2),
        }

    return scores


def identify_archival_candidates(scores, citation_index, defined_pids):
    """Principles with 0 exclusive citations and losing record are archival candidates.
    Only considers defined principles (not ghost references from merged/removed P-NNN).
    """
    candidates = []
    for pid, s in scores.items():
        if pid not in defined_pids:
            continue  # Skip ghost references
        if s["exclusive_citations"] == 0 and s["win_rate"] < 0.5:
            candidates.append({
                "id": pid,
                "reason": "zero exclusive coverage + losing record",
                **s,
            })
        elif s["total_citations"] == 0:
            candidates.append({
                "id": pid,
                "reason": "uncited (zero citations in lesson corpus)",
                **s,
            })
        elif s["exclusive_citations"] == 0 and s["total_citations"] <= 2:
            candidates.append({
                "id": pid,
                "reason": "low-citation + zero exclusive coverage",
                **s,
            })
    candidates.sort(key=lambda x: x["tournament_score"])
    return candidates


def main():
    ap = argparse.ArgumentParser(description="Principle tournament — selection pressure via competition")
    ap.add_argument("--top", type=int, default=15, help="Show top N archival candidates")
    ap.add_argument("--bracket", action="store_true", help="Show head-to-head matchups")
    ap.add_argument("--min-overlap", type=int, default=2, help="Min lesson overlap for competition")
    ap.add_argument("--json", action="store_true", help="JSON output")
    args = ap.parse_args()

    # Parse principles
    ptext = PRINCIPLES_PATH.read_text(encoding="utf-8")
    all_principles = parse_principle_ids(ptext)
    sections = parse_principle_sections(ptext)

    # Scan lesson citations
    lesson_principles = scan_lesson_citations()
    citation_index = build_citation_index(lesson_principles)

    # Find competitions
    competitions = find_competitions(citation_index, min_overlap=args.min_overlap)

    # Score
    scores = score_principles(citation_index, competitions)

    # Archival candidates
    defined_pids = set(all_principles.keys())
    candidates = identify_archival_candidates(scores, citation_index, defined_pids)

    # Uncited principles (not in any lesson)
    cited_pids = set(citation_index.keys())
    uncited = sorted(set(all_principles.keys()) - cited_pids)

    # Stats — only count defined principles
    defined_pids = set(all_principles.keys())
    cited_and_defined = defined_pids & cited_pids
    ghost_citations = cited_pids - defined_pids  # in lessons but not in PRINCIPLES.md

    total_p = len(all_principles)
    cited_p = len(cited_and_defined)
    uncited_p = len(uncited)
    compete_p = len({c["p1"] for c in competitions} | {c["p2"] for c in competitions})
    ghost_p = len(ghost_citations)

    if args.json:
        print(json.dumps({
            "total_principles": total_p,
            "cited": cited_p,
            "uncited": uncited_p,
            "ghost_citations": ghost_p,
            "competing": compete_p,
            "competitions": len(competitions),
            "archival_candidates": candidates[:args.top],
            "uncited_list": uncited[:30],
            "top_competitions": competitions[:20] if args.bracket else competitions[:5],
        }, indent=2))
        return

    print(f"=== PRINCIPLE TOURNAMENT — {total_p}P ===")
    print(f"  Cited in lessons: {cited_p}/{total_p} ({cited_p*100//total_p}%)")
    print(f"  Uncited: {uncited_p}/{total_p} ({uncited_p*100//total_p}%)")
    if ghost_p:
        print(f"  Ghost refs (merged/removed P-NNN in lessons): {ghost_p}")
    print(f"  In competition: {compete_p} ({compete_p*100//total_p}%)")
    print(f"  Total matchups: {len(competitions)} (min overlap={args.min_overlap})")
    print()

    # Archival candidates
    print(f"--- ARCHIVAL CANDIDATES (top {args.top}) ---")
    if not candidates and not uncited:
        print("  None found.")
    else:
        shown = 0
        for c in candidates[:args.top]:
            pid = c["id"]
            name = all_principles.get(pid, "?")[:60]
            sec = sections.get(pid, "?")
            print(f"  {pid:8s} [{sec[:20]:20s}] score={c['tournament_score']:5.1f}  "
                  f"W/L={c['wins']}/{c['losses']}  cite={c['total_citations']}  "
                  f"excl={c['exclusive_citations']}  — {c['reason']}")
            print(f"           {name}")
            shown += 1
        # Add uncited as candidates too
        for pid in uncited[:args.top - shown]:
            name = all_principles.get(pid, "?")[:60]
            sec = sections.get(pid, "?")
            print(f"  {pid:8s} [{sec[:20]:20s}] score= 0.0  "
                  f"W/L=0/0  cite=0  excl=0  — uncited")
            print(f"           {name}")
            shown += 1
            if shown >= args.top:
                break

    if args.bracket and competitions:
        print(f"\n--- HEAD-TO-HEAD MATCHUPS (top 20) ---")
        for i, c in enumerate(competitions[:20], 1):
            p1n = all_principles.get(c["p1"], "?")[:40]
            p2n = all_principles.get(c["p2"], "?")[:40]
            winner = c["p1"] if c["p1_exclusive"] >= c["p2_exclusive"] else c["p2"]
            print(f"\n  #{i}  overlap={c['overlap']} ({c['overlap_ratio']:.0%} of smaller)")
            print(f"    {c['p1']:8s} ({c['p1_total']}cit, {c['p1_exclusive']}excl) {p1n}")
            print(f"    {c['p2']:8s} ({c['p2_total']}cit, {c['p2_exclusive']}excl) {p2n}")
            print(f"    → Winner: {winner}")

    # Summary prescription
    print(f"\n--- PRESCRIPTION ---")
    print(f"  {uncited_p} uncited principles: review for archival (40% target → ≤{total_p*60//100}P)")
    if candidates:
        print(f"  {len(candidates)} competition losers: merge into winners or archive")
    carrying = total_p - uncited_p - len(candidates)
    print(f"  {carrying} load-bearing principles with exclusive explanatory coverage")


if __name__ == "__main__":
    main()
