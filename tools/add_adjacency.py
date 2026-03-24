#!/usr/bin/env python3
"""add_adjacency.py — Complete the domain adjacency network.

Idempotent: only adds Adjacent: to domains that don't have it.
Usage: python3 tools/add_adjacency.py --apply
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOMAINS_DIR = ROOT / "domains"

ADJACENCY = {
    "catastrophic-risks": "conflict, control-theory, governance, health",
    "city-plan": "graph-theory, operations-research, meta, nk-complexity",
    "claude-code": "ai, expert-swarm, meta",
    "concept-inventor": "dream, meta, epistemology, psychology",
    "control-theory": "stochastic-processes, fluid-dynamics, thermodynamics, filtering",
    "cryptocurrency": "distributed-systems, finance, game-theory, security",
    "cryptography": "distributed-systems, protocol-engineering, security, information-science",
    "distributed-systems": "control-theory, protocol-engineering, nk-complexity, cryptography",
    "dream": "concept-inventor, brain, psychology, meta",
    "economy": "finance, game-theory, strategy, governance",
    "evaluation": "meta, epistemology, quality, expert-swarm",
    "farming": "evolution, strategy, quality, plant-biology",
    "filtering": "information-science, statistics, control-theory, stochastic-processes",
    "fluid-dynamics": "control-theory, physics, stochastic-processes, thermodynamics",
    "fractals": "graph-theory, mathematics, physics, nk-complexity",
    "gaming": "game-theory, psychology, strategy, dream",
    "graph-theory": "nk-complexity, distributed-systems, mathematics, fractals",
    "guesstimates": "statistics, forecasting, operations-research, mathematics",
    "health": "evolution, control-theory, catastrophic-risks, brain",
    "helper-swarm": "expert-swarm, operations-research, strategy, meta",
    "history": "epistemology, governance, human-systems, linguistics",
    "human-systems": "governance, psychology, conflict, history",
    "linguistics": "brain, information-science, statistics, history",
    "physics": "thermodynamics, fluid-dynamics, mathematics, string-theory",
    "plant-biology": "farming, evolution, brain, health",
    "protocol-engineering": "distributed-systems, cryptography, governance, security",
    "psychology": "brain, empathy, human-systems, gaming",
    "quality": "evaluation, meta, information-science, farming",
    "random-matrix-theory": "mathematics, statistics, nk-complexity, physics",
    "security": "cryptography, distributed-systems, conflict, protocol-engineering",
    "social-media": "human-systems, game-theory, forecasting, linguistics",
    "statistics": "information-science, forecasting, mathematics, random-matrix-theory",
    "stochastic-processes": "epistemology, statistics, control-theory, mathematics",
    "strategy": "game-theory, operations-research, meta, economy",
    "string-theory": "mathematics, physics, information-science, thermodynamics",
    "thermodynamics": "physics, information-science, fluid-dynamics, control-theory",
}

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    added = 0
    for domain, adj_value in sorted(ADJACENCY.items()):
        f = DOMAINS_DIR / domain / "DOMAIN.md"
        if not f.exists():
            continue
        content = f.read_text(encoding="utf-8")
        if any(line.startswith("Adjacent:") for line in content.split("\n")[:10]):
            continue
        if args.apply:
            lines = content.split("\n")
            lines.insert(1, f"Adjacent: {adj_value}")
            f.write_text("\n".join(lines), encoding="utf-8")
            print(f"  ADDED: {domain}")
        else:
            print(f"  WOULD ADD: {domain}")
        added += 1
    print(f"\n{'Applied' if args.apply else 'Would apply'}: {added}")
