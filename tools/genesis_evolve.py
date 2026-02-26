#!/usr/bin/env python3
"""
genesis_evolve.py — Propose genesis template improvements from child swarm data.

Usage:
    python3 tools/genesis_evolve.py analyze
    python3 tools/genesis_evolve.py report

Reads integration logs and child evaluation data to identify patterns
that could improve the genesis template. This is the "selection" step
in the genetic algorithm: what worked in children should inform the
template that produces the next generation.

F38: Colony-level selection to improve the genesis template.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CHILDREN_DIR = REPO_ROOT / "experiments" / "children"
INTEGRATION_LOG_DIR = REPO_ROOT / "experiments" / "integration-log"
MERGE_REPORTS_DIR = REPO_ROOT / "experiments" / "merge-reports"


def analyze_children() -> dict:
    """Analyze all children to find patterns for genesis improvement."""
    swarm_test = REPO_ROOT / "tools" / "swarm_test.py"
    results = {
        "children_analyzed": 0,
        "total_novel_rules": 0,
        "total_novel_questions": 0,
        "viability_scores": [],
        "common_patterns": [],
        "genesis_proposals": [],
    }

    if not CHILDREN_DIR.exists():
        return results

    children = [d for d in CHILDREN_DIR.iterdir() if d.is_dir()]
    results["children_analyzed"] = len(children)

    for child_dir in sorted(children):
        # Evaluate
        r = subprocess.run(
            ["python3", str(swarm_test), "evaluate", str(child_dir)],
            capture_output=True, text=True
        )
        vm = re.search(r"Viability: (\d+)/4", r.stdout)
        score = int(vm.group(1)) if vm else 0
        results["viability_scores"].append({
            "name": child_dir.name,
            "score": score,
        })

    # Read integration logs
    if INTEGRATION_LOG_DIR.exists():
        for f in INTEGRATION_LOG_DIR.glob("*.json"):
            data = json.loads(f.read_text())
            results["total_novel_rules"] += data.get("novel_rules", 0)
            results["total_novel_questions"] += data.get("novel_questions", 0)

    # Analyze patterns across children
    avg_viability = (
        sum(v["score"] for v in results["viability_scores"])
        / len(results["viability_scores"])
        if results["viability_scores"] else 0
    )

    # Generate proposals based on data
    if avg_viability < 3.0:
        results["genesis_proposals"].append({
            "type": "structure",
            "proposal": "Children average < 3/4 viability. Consider adding a NEXT.md template to genesis to improve first-session onboarding.",
            "evidence": f"avg viability = {avg_viability:.1f}/4",
        })

    # Check if children commonly fail to resolve frontier questions
    low_resolve = [
        v for v in results["viability_scores"]
        if v["score"] < 4
    ]
    if len(low_resolve) > len(results["viability_scores"]) * 0.5:
        results["genesis_proposals"].append({
            "type": "frontier",
            "proposal": "Most children don't resolve F1 in first session. Consider making F1 auto-resolvable or replacing with a more tractable first question.",
            "evidence": f"{len(low_resolve)}/{len(results['viability_scores'])} children below 4/4",
        })

    # Check if novel rules are being produced
    if results["total_novel_rules"] > 0:
        results["genesis_proposals"].append({
            "type": "knowledge",
            "proposal": f"Children producing novel rules ({results['total_novel_rules']} total). Evolution pipeline is working — continue spawning domain-specific children.",
            "evidence": f"{results['total_novel_rules']} novel rules from {results['children_analyzed']} children",
        })

    # Check principles template in genesis
    genesis = REPO_ROOT / "workspace" / "genesis.sh"
    if genesis.exists():
        genesis_text = genesis.read_text()
        if "PRINCIPLES.md" not in genesis_text:
            results["genesis_proposals"].append({
                "type": "missing_file",
                "proposal": "Genesis doesn't create PRINCIPLES.md. Children can't track building blocks without it.",
                "evidence": "PRINCIPLES.md absent from genesis template",
            })

    return results


def print_report(results: dict):
    """Print the genesis evolution report."""
    print("=== GENESIS EVOLUTION REPORT ===\n")
    print(f"Children analyzed: {results['children_analyzed']}")
    print(f"Novel rules produced: {results['total_novel_rules']}")
    print(f"Novel questions produced: {results['total_novel_questions']}")

    if results["viability_scores"]:
        print(f"\n--- Viability Scores ---")
        for v in sorted(results["viability_scores"], key=lambda x: x["score"], reverse=True):
            bar = "#" * v["score"] + "." * (4 - v["score"])
            print(f"  {v['name']:<25} [{bar}] {v['score']}/4")

        avg = sum(v["score"] for v in results["viability_scores"]) / len(results["viability_scores"])
        print(f"\n  Average: {avg:.1f}/4")

    if results["genesis_proposals"]:
        print(f"\n--- Proposals for Genesis v5 ---")
        for i, p in enumerate(results["genesis_proposals"], 1):
            print(f"\n  {i}. [{p['type'].upper()}] {p['proposal']}")
            print(f"     Evidence: {p['evidence']}")
    else:
        print("\n  No proposals — genesis template is performing well.")

    # Current genesis version
    genesis = REPO_ROOT / "workspace" / "genesis.sh"
    if genesis.exists():
        first_line = genesis.read_text().splitlines()[1] if genesis.read_text() else ""
        print(f"\n  Current: {first_line.strip()}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd in ("analyze", "report"):
        results = analyze_children()
        print_report(results)
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
