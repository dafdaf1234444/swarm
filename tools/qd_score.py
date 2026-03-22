#!/usr/bin/env python3
"""qd_score.py — Quality-Diversity score for swarm knowledge.

Inspired by MAP-Elites (CarperAI/OpenELM). In MAP-Elites, the QD score
is the sum of fitness across all niches in a discretized behavior space.
High QD = high quality AND high diversity. Either dimension alone is
insufficient.

For the swarm:
- Niches = domains (the behavior space)
- Fitness per niche = best Sharpe score among lessons in that domain
- QD score = sum of niche fitnesses
- Coverage = fraction of niches with at least one lesson
- Niche competition: identifies which lessons are the "elite" per niche
  (highest Sharpe) and which are dominated (lower Sharpe in same niche)

This provides the missing selection pressure signal (L-1301, L-895):
the swarm produces knowledge but never discards dominated knowledge.

Usage:
    python3 tools/qd_score.py [--verbose] [--threshold N]
"""

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path


def parse_lesson(path: Path) -> dict:
    """Extract domain, Sharpe, and title from a lesson file."""
    try:
        content = path.read_text(errors="ignore")
    except OSError:
        return {}

    result = {"path": str(path.name), "domain": None, "sharpe": 0, "title": ""}

    # Extract title from first line
    lines = content.split("\n")
    if lines and lines[0].startswith("# L-"):
        title_match = re.match(r"# (L-\d+): (.+)", lines[0])
        if title_match:
            result["title"] = title_match.group(2)

    # Extract domain
    domain_match = re.search(r"Domain:\s*(\S+)", content)
    if domain_match:
        result["domain"] = domain_match.group(1).lower().rstrip("|")

    # Extract Sharpe
    sharpe_match = re.search(r"Sharpe:\s*(\d+)", content)
    if sharpe_match:
        result["sharpe"] = int(sharpe_match.group(1))

    return result


def compute_qd_score(lessons_dir: str = "memory/lessons",
                     domains_dir: str = "domains") -> dict:
    """Compute MAP-Elites-style QD score for swarm knowledge."""
    lessons_path = Path(lessons_dir)
    domains_path = Path(domains_dir)

    # Parse all lessons
    lessons = []
    for f in sorted(lessons_path.glob("L-*.md")):
        parsed = parse_lesson(f)
        if parsed and parsed.get("domain"):
            lessons.append(parsed)

    # Discover all niches (domains)
    all_domains = set()
    if domains_path.exists():
        for d in domains_path.iterdir():
            if d.is_dir() and not d.name.startswith("."):
                all_domains.add(d.name)

    # Also include domains from lessons
    for l in lessons:
        if l["domain"]:
            all_domains.add(l["domain"])

    # Build niche map
    niche_map = defaultdict(list)
    for l in lessons:
        if l["domain"]:
            niche_map[l["domain"]].append(l)

    # Compute per-niche stats
    niche_stats = {}
    total_qd = 0.0
    for domain in sorted(all_domains):
        domain_lessons = niche_map.get(domain, [])
        if domain_lessons:
            sharpes = [l["sharpe"] for l in domain_lessons]
            best = max(sharpes)
            elite = [l for l in domain_lessons if l["sharpe"] == best][0]
            dominated = [l for l in domain_lessons if l["sharpe"] < best and l["sharpe"] > 0]
            niche_stats[domain] = {
                "count": len(domain_lessons),
                "best_sharpe": best,
                "elite": elite["path"],
                "elite_title": elite["title"][:60],
                "dominated_count": len(dominated),
                "mean_sharpe": sum(sharpes) / len(sharpes) if sharpes else 0,
            }
            total_qd += best
        else:
            niche_stats[domain] = {
                "count": 0,
                "best_sharpe": 0,
                "elite": None,
                "elite_title": None,
                "dominated_count": 0,
                "mean_sharpe": 0,
            }

    filled = sum(1 for s in niche_stats.values() if s["count"] > 0)
    total_niches = len(all_domains)
    total_dominated = sum(s["dominated_count"] for s in niche_stats.values())

    return {
        "qd_score": total_qd,
        "coverage": filled / total_niches if total_niches > 0 else 0,
        "niches_filled": filled,
        "total_niches": total_niches,
        "total_lessons_with_domain": len(lessons),
        "total_dominated": total_dominated,
        "mean_niche_fitness": total_qd / filled if filled > 0 else 0,
        "niche_stats": niche_stats,
    }


def main():
    parser = argparse.ArgumentParser(description="QD score for swarm knowledge")
    parser.add_argument("--verbose", "-v", action="store_true")
    parser.add_argument("--threshold", type=int, default=3,
                        help="Sharpe threshold below which lessons are 'weak'")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = compute_qd_score()

    if args.json:
        # Exclude niche_stats for brevity
        summary = {k: v for k, v in result.items() if k != "niche_stats"}
        print(json.dumps(summary, indent=2))
        return

    print(f"=== Quality-Diversity Score (MAP-Elites analog) ===")
    print(f"  QD Score: {result['qd_score']:.1f} (sum of best Sharpe per niche)")
    print(f"  Coverage: {result['coverage']:.1%} ({result['niches_filled']}/{result['total_niches']} niches)")
    print(f"  Mean niche fitness: {result['mean_niche_fitness']:.1f}")
    print(f"  Total lessons with domain: {result['total_lessons_with_domain']}")
    print(f"  Dominated lessons: {result['total_dominated']} (lower Sharpe than elite in same niche)")
    print()

    if args.verbose:
        # Show top niches
        ranked = sorted(result["niche_stats"].items(),
                       key=lambda x: x[1]["best_sharpe"], reverse=True)
        print("Top niches by fitness:")
        for domain, stats in ranked[:15]:
            if stats["count"] > 0:
                print(f"  {domain:30s} best={stats['best_sharpe']:2d} "
                      f"n={stats['count']:3d} dominated={stats['dominated_count']:3d} "
                      f"elite={stats['elite']}")

        print()
        # Show empty niches
        empty = [d for d, s in result["niche_stats"].items() if s["count"] == 0]
        if empty:
            print(f"Empty niches ({len(empty)}): {', '.join(sorted(empty)[:10])}")


if __name__ == "__main__":
    main()
