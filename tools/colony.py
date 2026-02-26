#!/usr/bin/env python3
"""
colony.py — Spawn and evaluate multiple child swarms as a colony.

Usage:
    python3 tools/colony.py run <experiment-name>
    python3 tools/colony.py status <experiment-name>
    python3 tools/colony.py compare <experiment-name>

A colony experiment spawns N child swarms with variations, runs
sessions on each, then compares outcomes to identify which
architectural choices produce the most viable offspring.

This is genetic-algorithm-like: the "genome" is the genesis template,
"fitness" is swarm_test viability score, and "selection" is parent
integration of winning strategies.

Experiment configs are stored in experiments/colonies/<name>.json
"""

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
COLONIES_DIR = REPO_ROOT / "experiments" / "colonies"


def create_experiment(name: str, config: dict) -> Path:
    """Create a colony experiment config."""
    COLONIES_DIR.mkdir(parents=True, exist_ok=True)
    config_path = COLONIES_DIR / f"{name}.json"
    config_path.write_text(json.dumps(config, indent=2))
    return config_path


def run_experiment(name: str):
    """Run a colony experiment: spawn children, run sessions, evaluate."""
    config_path = COLONIES_DIR / f"{name}.json"
    if not config_path.exists():
        print(f"No experiment config at {config_path}")
        print("Creating default experiment...")
        config = {
            "name": name,
            "children": [
                {"name": f"{name}-baseline", "topic": "baseline"},
                {"name": f"{name}-minimal", "topic": "minimal-structure-test"},
            ],
            "sessions_per_child": 1,
            "status": "created",
        }
        create_experiment(name, config)
        print(f"Config created at {config_path}")
        print("Edit the config, then run again.")
        return

    config = json.loads(config_path.read_text())

    if config.get("status") == "completed":
        print(f"Experiment '{name}' already completed. Use 'compare' to see results.")
        return

    # Spawn children
    print(f"=== Colony Experiment: {name} ===")
    print(f"Children: {len(config['children'])}")
    print()

    swarm_test = REPO_ROOT / "tools" / "swarm_test.py"
    results = []

    for child_config in config["children"]:
        child_name = child_config["name"]
        child_topic = child_config.get("topic", "general")

        print(f"--- Spawning: {child_name} (topic: {child_topic}) ---")

        # Spawn
        r = subprocess.run(
            ["python3", str(swarm_test), "spawn", child_name, child_topic],
            capture_output=True, text=True
        )
        if r.returncode != 0:
            print(f"  Spawn failed: {r.stderr}")
            results.append({"name": child_name, "status": "spawn_failed"})
            continue

        print(f"  Spawned successfully")

        # Evaluate (pre-session)
        child_dir = REPO_ROOT / "experiments" / "children" / child_name
        r = subprocess.run(
            ["python3", str(swarm_test), "evaluate", str(child_dir)],
            capture_output=True, text=True
        )
        print(f"  Pre-session evaluation:\n{r.stdout}")

        results.append({
            "name": child_name,
            "topic": child_topic,
            "status": "spawned",
            "path": str(child_dir),
        })

    # Save results
    config["status"] = "spawned"
    config["results"] = results
    config_path.write_text(json.dumps(config, indent=2))

    print(f"\n{len(results)} children spawned.")
    print(f"Next: Run sessions on each child, then use 'compare' to evaluate.")


def compare_experiment(name: str):
    """Compare children in a colony experiment."""
    config_path = COLONIES_DIR / f"{name}.json"
    if not config_path.exists():
        print(f"No experiment at {config_path}")
        sys.exit(1)

    config = json.loads(config_path.read_text())

    print(f"=== Colony Comparison: {name} ===\n")

    swarm_test = REPO_ROOT / "tools" / "swarm_test.py"
    merge_back = REPO_ROOT / "tools" / "merge_back.py"

    evaluations = []
    for child_config in config.get("results", config.get("children", [])):
        child_name = child_config.get("name", "unknown")
        child_dir = REPO_ROOT / "experiments" / "children" / child_name

        if not child_dir.exists():
            print(f"  {child_name}: NOT FOUND")
            continue

        # Evaluate
        r = subprocess.run(
            ["python3", str(swarm_test), "evaluate", str(child_dir)],
            capture_output=True, text=True
        )

        # Extract viability score from output
        viability_m = None
        for line in r.stdout.splitlines():
            if "Viability:" in line:
                viability_m = line.strip()
                break

        evaluations.append({
            "name": child_name,
            "viability": viability_m or "unknown",
            "output": r.stdout,
        })

    # Print comparison table
    print(f"{'Child':<30} {'Viability':<30}")
    print("-" * 60)
    for e in evaluations:
        print(f"{e['name']:<30} {e['viability']:<30}")

    # Find winner
    if evaluations:
        # Sort by viability score (extract number)
        def extract_score(e):
            import re
            m = re.search(r"(\d+)/4", e["viability"])
            return int(m.group(1)) if m else 0

        evaluations.sort(key=extract_score, reverse=True)
        winner = evaluations[0]
        print(f"\nMost viable: {winner['name']} ({winner['viability']})")

        # Generate merge-back report for winner
        winner_dir = REPO_ROOT / "experiments" / "children" / winner["name"]
        r = subprocess.run(
            ["python3", str(merge_back), str(winner_dir)],
            capture_output=True, text=True
        )
        if r.stdout:
            print(f"\n--- Merge-back report for {winner['name']} ---")
            print(r.stdout)


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]
    name = sys.argv[2]

    if cmd == "run":
        run_experiment(name)
    elif cmd == "status":
        config_path = COLONIES_DIR / f"{name}.json"
        if config_path.exists():
            print(json.dumps(json.loads(config_path.read_text()), indent=2))
        else:
            print(f"No experiment at {config_path}")
    elif cmd == "compare":
        compare_experiment(name)
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
