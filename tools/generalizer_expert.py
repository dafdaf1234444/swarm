#!/usr/bin/env python3
"""
generalizer_expert.py — Swarm Generalization Analyst

Surfaces cross-domain generalization candidates and atlas gaps.

Usage:
  python3 tools/generalizer_expert.py          # human-readable report
  python3 tools/generalizer_expert.py --json   # machine-readable JSON
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).parent.parent


def build_prefix_map() -> tuple[dict[str, str], dict[str, list[str]]]:
    """Map F-<PREFIX> to domain directory names by scanning domain frontiers."""
    prefixes: dict[str, str] = {}
    collisions: dict[str, set[str]] = {}
    domains_dir = ROOT / "domains"
    if not domains_dir.exists():
        return prefixes, {}

    for domain_dir in sorted(domains_dir.iterdir()):
        if not domain_dir.is_dir():
            continue
        frontier = domain_dir / "tasks" / "FRONTIER.md"
        if not frontier.exists():
            continue
        text = frontier.read_text(encoding="utf-8", errors="replace")
        for match in re.findall(r"\*\*F-([A-Z]{2,6})\d+\*\*", text):
            prefix = match
            if prefix not in prefixes:
                prefixes[prefix] = domain_dir.name
            elif prefixes[prefix] != domain_dir.name:
                collisions.setdefault(prefix, set()).update(
                    [prefixes[prefix], domain_dir.name]
                )

    return prefixes, {k: sorted(v) for k, v in collisions.items()}


def extract_domains(text: str, prefix_map: dict[str, str]) -> list[str]:
    domains = set()
    for prefix, domain in prefix_map.items():
        if re.search(rf"\bF-{re.escape(prefix)}\d+\b", text):
            domains.add(domain)
    return sorted(domains)


def extract_prefixes(text: str) -> set[str]:
    return set(re.findall(r"\bF-([A-Z]{2,6})\d+\b", text))


def analyze_lessons(prefix_map: dict[str, str]) -> dict:
    lessons_dir = ROOT / "memory" / "lessons"
    if not lessons_dir.exists():
        return {}

    total = 0
    cross_count = 0
    lesson_rows: list[dict] = []
    domain_counts: Counter = Counter()
    domain_pair_counts: Counter = Counter()
    unknown_prefixes: Counter = Counter()

    for path in sorted(lessons_dir.glob("L-*.md")):
        if path.stem == "TEMPLATE":
            continue
        total += 1
        text = path.read_text(encoding="utf-8", errors="replace")
        domains = extract_domains(text, prefix_map)
        domain_count = len(domains)
        if domain_count >= 2:
            cross_count += 1
        if domains:
            for d in domains:
                domain_counts[d] += 1
        if domain_count >= 2:
            for a, b in combinations(domains, 2):
                domain_pair_counts[(a, b)] += 1

        for prefix in extract_prefixes(text):
            if prefix not in prefix_map:
                unknown_prefixes[prefix] += 1

        lesson_rows.append(
            {
                "lesson": path.stem,
                "domains": domains,
                "domain_count": domain_count,
            }
        )

    def _lesson_key(row: dict) -> tuple[int, int]:
        try:
            num = int(row["lesson"].split("-")[1])
        except Exception:
            num = 0
        return (-row["domain_count"], num)

    top_lessons = sorted(lesson_rows, key=_lesson_key)[:10]
    domain_pairs = [
        {"pair": list(pair), "count": count}
        for pair, count in domain_pair_counts.most_common(10)
    ]
    domains_with_zero = sorted(
        {d for d in prefix_map.values()} - set(domain_counts.keys())
    )

    return {
        "total_lessons": total,
        "cross_domain_lessons": cross_count,
        "cross_domain_rate": round(cross_count / total, 3) if total else 0.0,
        "top_cross_domain_lessons": top_lessons,
        "domain_reference_counts": dict(sorted(domain_counts.items())),
        "domain_pair_counts": domain_pairs,
        "domains_with_zero_lessons": domains_with_zero,
        "unknown_prefix_counts": dict(sorted(unknown_prefixes.items())),
    }


def parse_isomorphism_gaps() -> dict:
    atlas = ROOT / "domains" / "ISOMORPHISM-ATLAS.md"
    if not atlas.exists():
        return {}
    text = atlas.read_text(encoding="utf-8", errors="replace")
    counts: Counter = Counter()
    for match in re.finditer(r"\*\*Gaps\*\*:\s*(.*)", text):
        blob = match.group(1).strip()
        if not blob:
            continue
        for raw in re.split(r",\s*", blob):
            cleaned = re.sub(r"\([^)]*\)", "", raw).strip()
            cleaned = re.split(r"\s+[-–—]\s+", cleaned)[0].strip()
            cleaned = cleaned.strip(".?;")
            if not cleaned:
                continue
            counts[cleaned.lower()] += 1
    return {
        "gap_counts": dict(sorted(counts.items(), key=lambda x: (-x[1], x[0]))),
        "top_gaps": [{"gap": k, "count": v} for k, v in counts.most_common(10)],
        "total_gap_refs": sum(counts.values()),
    }


def build_recommendations(lessons: dict, gaps: dict, collisions: dict[str, list[str]]) -> list[str]:
    recs: list[str] = []
    total = lessons.get("total_lessons", 0)
    cross_rate = lessons.get("cross_domain_rate", 0.0)

    if total:
        if cross_rate < 0.15:
            recs.append(
                f"WARN: only {cross_rate:.0%} of lessons cite multiple domains — generalization low"
            )
        elif cross_rate < 0.3:
            recs.append(
                f"INFO: cross-domain lesson rate {cross_rate:.0%} — room to generalize more"
            )

    top_lessons = lessons.get("top_cross_domain_lessons", [])
    if top_lessons:
        recs.append(
            f"Review top {min(5, len(top_lessons))} cross-domain lessons for isomorphism or principle promotion"
        )

    gap_list = gaps.get("top_gaps", [])
    if gap_list:
        top = ", ".join(g["gap"] for g in gap_list[:5])
        recs.append(f"Atlas gaps to verify next: {top}")

    zero_domains = lessons.get("domains_with_zero_lessons", [])
    if zero_domains:
        recs.append(
            f"Domains with zero lesson references: {', '.join(zero_domains[:5])}"
            + (" (and more)" if len(zero_domains) > 5 else "")
        )

    if collisions:
        recs.append(
            f"Resolve prefix collisions in domain frontiers: {', '.join(collisions)}"
        )

    if not recs:
        recs.append("OK: generalization coverage healthy — no urgent gaps detected")

    return recs


def run() -> dict:
    prefix_map, collisions = build_prefix_map()
    lessons = analyze_lessons(prefix_map) if prefix_map else {}
    gaps = parse_isomorphism_gaps()
    recs = build_recommendations(lessons, gaps, collisions)
    return {
        "prefix_map": prefix_map,
        "prefix_collisions": collisions,
        "lesson_generalization": lessons,
        "isomorphism_gaps": gaps,
        "recommendations": recs,
    }


def _fmt(report: dict) -> None:
    lessons = report.get("lesson_generalization", {})
    gaps = report.get("isomorphism_gaps", {})
    collisions = report.get("prefix_collisions", {})
    recs = report.get("recommendations", [])

    print("=== SWARM GENERALIZER REPORT ===\n")

    prefix_map = report.get("prefix_map", {})
    print(f"[PREFIXES] {len(prefix_map)} domain prefixes detected")
    if collisions:
        print(f"  Collisions: {', '.join(collisions.keys())}")

    if lessons:
        total = lessons.get("total_lessons", 0)
        cross = lessons.get("cross_domain_lessons", 0)
        rate = lessons.get("cross_domain_rate", 0.0)
        print(f"\n[LESSONS] {cross}/{total} cross-domain ({rate:.0%})")
        top = lessons.get("top_cross_domain_lessons", [])[:5]
        if top:
            print("  Top cross-domain lessons:")
            for row in top:
                domains = ", ".join(row["domains"]) if row["domains"] else "none"
                print(f"  - {row['lesson']}: {row['domain_count']} domains ({domains})")
        pairs = lessons.get("domain_pair_counts", [])[:5]
        if pairs:
            print("  Top domain pairs:")
            for pair in pairs:
                print(f"  - {pair['pair'][0]} ↔ {pair['pair'][1]} ({pair['count']})")
        unknown = lessons.get("unknown_prefix_counts", {})
        if unknown:
            unk = ", ".join(f"{k}({v})" for k, v in list(unknown.items())[:5])
            print(f"  Unknown prefixes: {unk}")

    if gaps:
        top_gaps = gaps.get("top_gaps", [])
        if top_gaps:
            print("\n[ATLAS GAPS] Top gap mentions:")
            for g in top_gaps[:5]:
                print(f"  - {g['gap']} ({g['count']})")

    print("\n[RECOMMENDATIONS]")
    for r in recs:
        print(f"  {r}")
    print()


def main() -> None:
    report = run()
    if "--json" in sys.argv:
        print(json.dumps(report, indent=2))
    else:
        _fmt(report)


if __name__ == "__main__":
    main()
