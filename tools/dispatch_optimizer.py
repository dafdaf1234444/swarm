#!/usr/bin/env python3
"""
Dispatch Optimizer — Expert Economy Tool (F-ECO4)
Scores and ranks domain experiments by expected yield (Sharpe × ISO × maturity).
Addresses structural unemployment of expert capacity (63 unrun experiments, 2% throughput).

Usage:
    python3 tools/dispatch_optimizer.py                 # Top-10 recommendations
    python3 tools/dispatch_optimizer.py --all           # Full ranked list
    python3 tools/dispatch_optimizer.py --domain X      # Score single domain
    python3 tools/dispatch_optimizer.py --json          # JSON output
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path


DOMAINS_DIR = Path("domains")
EXPERIMENTS_DIR = Path("experiments")


def score_domain(domain: str) -> dict | None:
    """Compute expected yield score for a domain's open frontiers."""
    frontier_path = DOMAINS_DIR / domain / "tasks" / "FRONTIER.md"
    domain_md_path = DOMAINS_DIR / domain / "DOMAIN.md"
    index_path = DOMAINS_DIR / domain / "INDEX.md"

    if not frontier_path.exists():
        return None

    content = frontier_path.read_text()

    # Active frontier count (lines with - **F or - **F-prefix)
    active_count = len(re.findall(r"^- \*\*F", content, re.MULTILINE))
    if active_count == 0:
        return None  # Skip domains with no open work

    # Resolved count (rows in Resolved table)
    resolved_count = 0
    resolved_match = re.search(r"## Resolved.*", content, re.DOTALL)
    if resolved_match:
        resolved_count = len(re.findall(r"^\| F", resolved_match.group(), re.MULTILINE))

    # Unique ISO references in DOMAIN.md (cross-domain linkage)
    iso_count = 0
    if domain_md_path.exists():
        dm = domain_md_path.read_text()
        iso_count = len(set(re.findall(r"ISO-\d+", dm)))

    # Experiment count (JSON artifacts produced)
    exp_dir = EXPERIMENTS_DIR / domain
    exp_count = 0
    if exp_dir.exists():
        exp_count = len(list(exp_dir.glob("*.json")))

    # Has domain INDEX (team has oriented and knows state)
    has_index = index_path.exists()

    # --- Yield score formula ---
    # iso_count * 3.0  : cross-domain leverage (highest multiplier)
    # resolved * 2.0   : domain maturity (team knows how to extract lessons here)
    # active * 1.5     : open work (demand signal)
    # novelty +2.0     : uncharted territory bonus (exp_count == 0)
    # has_index +1.0   : orientation artifact present
    novelty_bonus = 2.0 if exp_count == 0 else 0.0
    score = (
        iso_count * 3.0
        + resolved_count * 2.0
        + active_count * 1.5
        + novelty_bonus
        + (1.0 if has_index else 0.0)
    )

    # Extract first open frontier description (dispatch target)
    first_frontier = ""
    match = re.search(r"^- (\*\*F[^*\n]+\*\*.*?)(?=^- \*\*F|\Z)", content, re.MULTILINE | re.DOTALL)
    if match:
        first_frontier = match.group(1).strip()[:120].replace("\n", " ")

    return {
        "domain": domain,
        "score": round(score, 1),
        "active": active_count,
        "resolved": resolved_count,
        "iso": iso_count,
        "experiments": exp_count,
        "has_index": has_index,
        "novelty_bonus": novelty_bonus > 0,
        "top_frontier": first_frontier,
    }


def run(args: argparse.Namespace) -> None:
    if not DOMAINS_DIR.exists():
        print("ERROR: domains/ directory not found. Run from repo root.", file=sys.stderr)
        sys.exit(1)

    results = []
    target_domains = [args.domain] if args.domain else sorted(os.listdir(DOMAINS_DIR))

    for domain in target_domains:
        r = score_domain(domain)
        if r:
            results.append(r)

    results.sort(key=lambda x: x["score"], reverse=True)

    if not args.all and not args.domain:
        results = results[:10]

    if args.json:
        print(json.dumps(results, indent=2))
        return

    # Human-readable output
    print("\n=== DISPATCH OPTIMIZER (F-ECO4) ===")
    print(f"Expert economy: rank open frontiers by expected yield\n")
    print(f"{'Score':>6}  {'Domain':<28}  {'Active':>6}  {'Resolved':>8}  {'ISO':>4}  {'Exps':>5}  {'Nov':>3}")
    print("-" * 75)

    for r in results:
        nov = "★" if r["novelty_bonus"] else " "
        print(
            f"{r['score']:6.1f}  {r['domain']:<28}  {r['active']:6d}  "
            f"{r['resolved']:8d}  {r['iso']:4d}  {r['experiments']:5d}  {nov:>3}"
        )
        if r["top_frontier"]:
            print(f"         → {r['top_frontier'][:72]}")

    print("\n--- Scoring formula ---")
    print("  score = iso*3 + resolved*2 + active*1.5 + novelty_bonus(2) + has_index(1)")
    print("  ★ = no experiments yet (novelty territory)")
    print(f"\n  Showing {'all' if args.all else 'top 10'} of {len(results)} domains with open work.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Dispatch Optimizer — rank domain experiments by expected yield")
    parser.add_argument("--all", action="store_true", help="Show all domains, not just top 10")
    parser.add_argument("--domain", metavar="NAME", help="Score a single domain")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()
