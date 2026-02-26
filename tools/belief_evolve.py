#!/usr/bin/env python3
"""
belief_evolve.py — Recursive belief evolution: test which core ideologies produce useful swarms.

Usage:
    python3 tools/belief_evolve.py variants              # list defined belief variants
    python3 tools/belief_evolve.py spawn <variant>       # spawn a child with that variant
    python3 tools/belief_evolve.py spawn-all             # spawn all variants
    python3 tools/belief_evolve.py combine <v1> <v2>     # spawn grandchild combining 2 variants
    python3 tools/belief_evolve.py evaluate <child>      # measure outcomes
    python3 tools/belief_evolve.py evaluate-all          # evaluate all belief-* children
    python3 tools/belief_evolve.py compare               # compare all variant children
    python3 tools/belief_evolve.py lineage               # show parent→child→grandchild tree
    python3 tools/belief_evolve.py synthesize            # extract lessons about beliefs

The core idea: spawn sub-swarms with different core belief sets as genesis points,
let them evolve independently, then compare which beliefs produce useful swarms.
This is A/B testing for epistemology. Recursive: grandchildren combine winning traits.
"""

import json
import os
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
VARIANTS_DIR = REPO_ROOT / "experiments" / "belief-variants"
CHILDREN_DIR = REPO_ROOT / "experiments" / "children"
RESULTS_FILE = VARIANTS_DIR / "evolution-results.json"
LINEAGE_FILE = VARIANTS_DIR / "lineage.json"

# --- BELIEF VARIANTS ---
# Each variant modifies one dimension of the core belief system.
# The control is standard genesis.sh (no modifications).

VARIANTS = {
    "control": {
        "description": "Standard genesis.sh, no modifications",
        "hypothesis": "Baseline: standard beliefs produce standard outcomes",
        "modifications": {},
    },
    "no-falsification": {
        "description": "Remove falsification requirement from beliefs",
        "hypothesis": "Without falsification, beliefs accumulate faster but accuracy decreases",
        "modifications": {
            "DEPS.md": {
                "remove_lines_containing": ["Falsified if"],
            },
            "CLAUDE.md": {
                "replace": {
                    "Every belief needs `observed`/`theorized` evidence type and a falsification condition.":
                    "Every belief needs `observed`/`theorized` evidence type.",
                },
            },
        },
    },
    "no-lesson-limit": {
        "description": "Remove 20-line lesson limit",
        "hypothesis": "Without the limit, lessons are more detailed but context window fills faster",
        "modifications": {
            "CLAUDE.md": {
                "replace": {
                    "**Learn then lesson**: Write to `memory/lessons/` (max 20 lines, use template).":
                    "**Learn then lesson**: Write to `memory/lessons/` (use template).",
                },
            },
            "CORE.md": {
                "replace": {
                    "Lessons are max 20 lines.": "Write thorough lessons.",
                },
            },
        },
    },
    "no-modes": {
        "description": "Remove session modes — flat structure",
        "hypothesis": "Without modes, sessions are more flexible but less structured",
        "modifications": {
            "CLAUDE.md": {
                "remove_sections": ["Session modes"],
            },
        },
    },
    "aggressive-challenge": {
        "description": "Emphasize challenging existing beliefs over building new ones",
        "hypothesis": "More challenges lead to fewer but stronger beliefs",
        "modifications": {
            "CORE.md": {
                "replace": {
                    "**Challenge the setup.** Write challenges to tasks/FRONTIER.md.":
                    "**Challenge everything aggressively.** Every session MUST disprove at least one belief or demonstrate why it can't be disproven. Write challenges to tasks/FRONTIER.md.",
                },
            },
        },
    },
    "minimal": {
        "description": "Absolute minimum: just CLAUDE.md + DEPS.md, no protocols",
        "hypothesis": "Minimal structure lets the swarm self-organize, but may lose knowledge",
        "modifications": {
            "remove_files": [
                "memory/DISTILL.md", "memory/VERIFY.md",
                "beliefs/CONFLICTS.md", "memory/PRINCIPLES.md",
            ],
            "CLAUDE.md": {
                "replace": {
                    "## Protocols (read as needed)\n- `memory/DISTILL.md` — distillation\n- `memory/VERIFY.md` — 3-S Rule (Specific, Stale, Stakes-high)\n- `beliefs/CONFLICTS.md` — conflict resolution":
                    "## Note\nNo protocols defined. Self-organize as needed.",
                },
            },
        },
    },
}

# --- EVALUATION METRICS ---
# These measure swarm outcome quality.

def evaluate_child(child_path: Path) -> dict:
    """Measure outcomes of a child swarm."""
    metrics = {
        "lessons_count": 0,
        "lessons_avg_length": 0.0,
        "beliefs_count": 0,
        "observed_count": 0,
        "theorized_count": 0,
        "frontier_open": 0,
        "frontier_resolved": 0,
        "principles_count": 0,
        "total_files": 0,
        "total_lines": 0,
        "has_tools": False,
        "has_workspace": False,
        "validator_passes": False,
        "commit_count": 0,
    }

    # Lessons
    lessons_dir = child_path / "memory" / "lessons"
    if lessons_dir.exists():
        lesson_files = list(lessons_dir.glob("L-*.md"))
        metrics["lessons_count"] = len(lesson_files)
        if lesson_files:
            lengths = [len(f.read_text().splitlines()) for f in lesson_files]
            metrics["lessons_avg_length"] = sum(lengths) / len(lengths)

    # Beliefs
    deps = child_path / "beliefs" / "DEPS.md"
    if deps.exists():
        text = deps.read_text()
        metrics["beliefs_count"] = len(re.findall(r"^### B\d+:", text, re.MULTILINE))
        metrics["observed_count"] = len(re.findall(r"\*\*Evidence\*\*:\s*observed", text))
        metrics["theorized_count"] = len(re.findall(r"\*\*Evidence\*\*:\s*theorized", text))

    # Frontier
    frontier = child_path / "tasks" / "FRONTIER.md"
    if frontier.exists():
        text = frontier.read_text()
        metrics["frontier_open"] = len(re.findall(r"^- \*\*F\d+\*\*:", text, re.MULTILINE))
        metrics["frontier_resolved"] = len(re.findall(r"^\| F\d+", text, re.MULTILINE))

    # Principles
    principles = child_path / "memory" / "PRINCIPLES.md"
    if principles.exists():
        metrics["principles_count"] = len(re.findall(r"P-\d+", principles.read_text()))

    # Files and lines
    for f in child_path.rglob("*"):
        if f.is_file() and ".git" not in str(f):
            metrics["total_files"] += 1
            try:
                metrics["total_lines"] += len(f.read_text().splitlines())
            except Exception:
                pass

    metrics["has_tools"] = (child_path / "tools").is_dir()
    metrics["has_workspace"] = (child_path / "workspace").is_dir()

    # Validator
    validator = child_path / "tools" / "validate_beliefs.py"
    if validator.exists():
        r = subprocess.run(
            ["python3", str(validator)],
            cwd=str(child_path), capture_output=True, text=True, timeout=30
        )
        metrics["validator_passes"] = "PASS" in r.stdout

    # Commits
    r = subprocess.run(
        ["git", "-C", str(child_path), "log", "--oneline"],
        capture_output=True, text=True
    )
    if r.returncode == 0:
        metrics["commit_count"] = len(r.stdout.strip().splitlines())

    return metrics


def compute_fitness(metrics: dict) -> float:
    """Compute fitness score from metrics. Higher = better."""
    score = 0.0

    # Knowledge production (lessons + beliefs)
    score += metrics["lessons_count"] * 3
    score += metrics["beliefs_count"] * 5
    score += metrics["observed_count"] * 10  # observed beliefs are gold
    score += metrics["principles_count"] * 2

    # Frontier health (generating AND resolving questions)
    score += metrics["frontier_resolved"] * 4
    score += min(metrics["frontier_open"], 10) * 1  # cap open questions credit

    # Quality bonuses
    if metrics["validator_passes"]:
        score += 20
    if metrics["has_tools"]:
        score += 5
    if metrics["has_workspace"]:
        score += 5

    # Penalties
    if metrics["lessons_avg_length"] > 30:
        score -= 10  # bloated lessons
    if metrics["theorized_count"] > metrics["observed_count"] * 3:
        score -= 15  # too speculative

    return max(0, score)


# --- COMMANDS ---

def cmd_variants():
    """List all defined belief variants."""
    print("=== BELIEF VARIANTS ===\n")
    for name, v in VARIANTS.items():
        print(f"  {name}")
        print(f"    {v['description']}")
        print(f"    Hypothesis: {v['hypothesis']}")
        print()


def cmd_spawn(variant_name: str):
    """Spawn a child swarm with the specified variant."""
    if variant_name not in VARIANTS:
        print(f"Unknown variant: {variant_name}")
        print(f"Available: {', '.join(VARIANTS.keys())}")
        sys.exit(1)

    variant = VARIANTS[variant_name]
    child_name = f"belief-{variant_name}"
    child_dir = CHILDREN_DIR / child_name

    if child_dir.exists():
        print(f"Child already exists: {child_dir}")
        print("Delete it first or pick a different name.")
        sys.exit(1)

    # Run genesis
    genesis = REPO_ROOT / "workspace" / "genesis.sh"
    r = subprocess.run(
        ["bash", str(genesis), str(child_dir), child_name],
        capture_output=True, text=True
    )
    if r.returncode != 0:
        print(f"Genesis failed: {r.stderr}")
        sys.exit(1)

    # Apply variant modifications
    mods = variant["modifications"]

    # Handle file removals
    for f in mods.get("remove_files", []):
        fp = child_dir / f
        if fp.exists():
            fp.unlink()
            print(f"  Removed: {f}")

    # Handle per-file modifications
    for filename, changes in mods.items():
        if filename in ("remove_files",):
            continue
        if not isinstance(changes, dict):
            continue

        # Find the file
        candidates = list(child_dir.rglob(filename))
        if not candidates:
            print(f"  Warning: {filename} not found in child")
            continue

        for filepath in candidates:
            text = filepath.read_text()

            # Replace strings
            for old, new in changes.get("replace", {}).items():
                text = text.replace(old, new)

            # Remove lines containing specific strings
            for pattern in changes.get("remove_lines_containing", []):
                lines = text.splitlines()
                text = "\n".join(l for l in lines if pattern not in l) + "\n"

            # Remove sections
            for section in changes.get("remove_sections", []):
                # Remove ## Section ... until next ##
                text = re.sub(
                    rf"^## {re.escape(section)}.*?(?=^## |\Z)",
                    "", text, flags=re.MULTILINE | re.DOTALL
                )

            filepath.write_text(text)
            print(f"  Modified: {filepath.relative_to(child_dir)}")

    # Init git
    subprocess.run(["git", "init"], cwd=str(child_dir), capture_output=True)
    subprocess.run(["git", "add", "-A"], cwd=str(child_dir), capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", f"[S] genesis: {variant_name} variant"],
        cwd=str(child_dir), capture_output=True
    )

    # Record variant info
    VARIANTS_DIR.mkdir(parents=True, exist_ok=True)
    info = {
        "variant": variant_name,
        "description": variant["description"],
        "hypothesis": variant["hypothesis"],
        "spawned": date.today().isoformat(),
        "child_dir": str(child_dir),
    }
    info_file = VARIANTS_DIR / f"{variant_name}.json"
    info_file.write_text(json.dumps(info, indent=2))

    print(f"\nChild '{child_name}' spawned with variant '{variant_name}'")
    print(f"Directory: {child_dir}")
    print(f"\nTo run a session on this child, use the Task tool:")
    print(f'  Task(prompt="Run a session on this swarm at {child_dir}...")')


def cmd_spawn_all():
    """Spawn all variants."""
    for name in VARIANTS:
        child_dir = CHILDREN_DIR / f"belief-{name}"
        if child_dir.exists():
            print(f"Skipping {name} (already exists)")
            continue
        print(f"\n--- Spawning variant: {name} ---")
        cmd_spawn(name)


def _load_lineage():
    """Load lineage tracking data."""
    if LINEAGE_FILE.exists():
        return json.loads(LINEAGE_FILE.read_text())
    return {}


def _save_lineage(data):
    """Save lineage tracking data."""
    VARIANTS_DIR.mkdir(parents=True, exist_ok=True)
    LINEAGE_FILE.write_text(json.dumps(data, indent=2))


def cmd_combine(variant_names: list):
    """Spawn a grandchild combining 2+ variants."""
    # Validate all variant names
    for name in variant_names:
        if name not in VARIANTS:
            print(f"Unknown variant: {name}")
            print(f"Available: {', '.join(VARIANTS.keys())}")
            sys.exit(1)

    # Create combined name (shortened for directory friendliness)
    short_names = {
        "no-falsification": "nofalsif",
        "no-lesson-limit": "nolimit",
        "no-modes": "nomodes",
        "aggressive-challenge": "aggressive",
        "control": "control",
        "minimal": "minimal",
    }
    combined_name = "-".join(short_names.get(n, n) for n in sorted(variant_names))
    child_name = f"belief-{combined_name}"
    child_dir = CHILDREN_DIR / child_name

    if child_dir.exists():
        print(f"Combined child already exists: {child_dir}")
        sys.exit(1)

    # Run genesis
    genesis = REPO_ROOT / "workspace" / "genesis.sh"
    r = subprocess.run(
        ["bash", str(genesis), str(child_dir)],
        capture_output=True, text=True
    )
    if r.returncode != 0:
        print(f"Genesis failed: {r.stderr}")
        sys.exit(1)

    # Apply all variant modifications in sequence
    for variant_name in variant_names:
        variant = VARIANTS[variant_name]
        mods = variant["modifications"]

        for f in mods.get("remove_files", []):
            fp = child_dir / f
            if fp.exists():
                fp.unlink()
                print(f"  [{variant_name}] Removed: {f}")

        for filename, changes in mods.items():
            if filename in ("remove_files",) or not isinstance(changes, dict):
                continue
            candidates = list(child_dir.rglob(filename))
            for filepath in candidates:
                text = filepath.read_text()
                for old, new in changes.get("replace", {}).items():
                    text = text.replace(old, new)
                for pattern in changes.get("remove_lines_containing", []):
                    lines = text.splitlines()
                    text = "\n".join(l for l in lines if pattern not in l) + "\n"
                for section in changes.get("remove_sections", []):
                    text = re.sub(
                        rf"^## {re.escape(section)}.*?(?=^## |\Z)",
                        "", text, flags=re.MULTILINE | re.DOTALL
                    )
                filepath.write_text(text)
                print(f"  [{variant_name}] Modified: {filepath.relative_to(child_dir)}")

    # Init git
    subprocess.run(["git", "init"], cwd=str(child_dir), capture_output=True)
    subprocess.run(["git", "add", "-A"], cwd=str(child_dir), capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", f"[S] genesis: {combined_name} combined variant (grandchild)"],
        cwd=str(child_dir), capture_output=True
    )

    # Track lineage
    lineage = _load_lineage()
    lineage[child_name] = {
        "parents": [f"belief-{n}" for n in variant_names],
        "generation": 2,
        "variants_combined": variant_names,
        "spawned": date.today().isoformat(),
    }
    # Ensure single-variant entries exist
    for name in variant_names:
        single = f"belief-{name}"
        if single not in lineage:
            lineage[single] = {
                "parents": ["genesis"],
                "generation": 1,
                "variants_combined": [name],
                "spawned": date.today().isoformat(),
            }
    _save_lineage(lineage)

    print(f"\nGrandchild '{child_name}' spawned combining: {', '.join(variant_names)}")
    print(f"Directory: {child_dir}")


def cmd_evaluate_all():
    """Evaluate all belief-* children."""
    if not CHILDREN_DIR.exists():
        print("No children directory found.")
        sys.exit(1)

    children = sorted([
        d for d in CHILDREN_DIR.iterdir()
        if d.is_dir() and d.name.startswith("belief-") and (d / ".git").exists()
    ])

    if not children:
        print("No belief-variant children found.")
        sys.exit(1)

    print(f"Evaluating {len(children)} children...\n")
    for child in children:
        cmd_evaluate(child.name)
        print()


def cmd_lineage():
    """Show parent→child→grandchild tree."""
    lineage = _load_lineage()

    # Also scan for any children not yet in lineage
    if CHILDREN_DIR.exists():
        for d in sorted(CHILDREN_DIR.iterdir()):
            if d.is_dir() and d.name.startswith("belief-") and d.name not in lineage:
                # Infer generation from name
                variant_name = d.name.replace("belief-", "")
                if variant_name in VARIANTS:
                    lineage[d.name] = {
                        "parents": ["genesis"],
                        "generation": 1,
                        "variants_combined": [variant_name],
                    }
                else:
                    lineage[d.name] = {
                        "parents": ["unknown"],
                        "generation": 2,
                        "variants_combined": [],
                    }

    # Load fitness data for display
    results = {}
    if RESULTS_FILE.exists():
        results = json.loads(RESULTS_FILE.read_text())

    # Print tree
    print("=== BELIEF EVOLUTION LINEAGE ===\n")
    print("genesis (standard beliefs)")

    gen1 = {k: v for k, v in lineage.items() if v.get("generation") == 1}
    gen2 = {k: v for k, v in lineage.items() if v.get("generation", 0) >= 2}

    for name, info in sorted(gen1.items()):
        fitness = results.get(name, {}).get("fitness", "?")
        print(f"  ├── {name} (fitness={fitness})")

        # Find grandchildren of this variant
        for gname, ginfo in sorted(gen2.items()):
            if name in ginfo.get("parents", []):
                gfitness = results.get(gname, {}).get("fitness", "?")
                print(f"  │   └── {gname} (fitness={gfitness})")

    # Show orphan grandchildren (parents not in gen1)
    shown = set()
    for gname, ginfo in sorted(gen2.items()):
        parents = ginfo.get("parents", [])
        if not any(p in gen1 for p in parents):
            gfitness = results.get(gname, {}).get("fitness", "?")
            print(f"  └── {gname} (fitness={gfitness}) [parents: {', '.join(parents)}]")


def cmd_evaluate(child_name: str):
    """Evaluate a child swarm's outcomes."""
    child_dir = CHILDREN_DIR / child_name
    if not child_dir.exists():
        print(f"Child not found: {child_dir}")
        sys.exit(1)

    metrics = evaluate_child(child_dir)
    fitness = compute_fitness(metrics)

    print(f"=== EVALUATION: {child_name} ===\n")
    print(f"  Lessons:          {metrics['lessons_count']} (avg {metrics['lessons_avg_length']:.1f} lines)")
    print(f"  Beliefs:          {metrics['beliefs_count']} ({metrics['observed_count']} observed, {metrics['theorized_count']} theorized)")
    print(f"  Principles:       {metrics['principles_count']}")
    print(f"  Frontier:         {metrics['frontier_open']} open, {metrics['frontier_resolved']} resolved")
    print(f"  Files/Lines:      {metrics['total_files']} / {metrics['total_lines']}")
    print(f"  Commits:          {metrics['commit_count']}")
    print(f"  Validator:        {'PASS' if metrics['validator_passes'] else 'FAIL'}")
    print(f"\n  FITNESS SCORE:    {fitness:.1f}")

    # Save results
    VARIANTS_DIR.mkdir(parents=True, exist_ok=True)
    results = {}
    if RESULTS_FILE.exists():
        results = json.loads(RESULTS_FILE.read_text())
    results[child_name] = {
        "metrics": metrics,
        "fitness": fitness,
        "evaluated": date.today().isoformat(),
    }
    RESULTS_FILE.write_text(json.dumps(results, indent=2))

    return metrics, fitness


def cmd_compare():
    """Compare all belief variant children."""
    if not RESULTS_FILE.exists():
        print("No results. Run 'evaluate' on each child first.")

        # Auto-evaluate all belief-* children
        children = sorted([
            d for d in CHILDREN_DIR.iterdir()
            if d.is_dir() and d.name.startswith("belief-")
        ]) if CHILDREN_DIR.exists() else []

        if not children:
            print("No belief-variant children found.")
            sys.exit(1)

        print(f"Auto-evaluating {len(children)} children...\n")
        for child in children:
            cmd_evaluate(child.name)
        print()

    results = json.loads(RESULTS_FILE.read_text())

    lineage = _load_lineage()

    print("=== BELIEF VARIANT COMPARISON ===\n")
    print(f"{'Variant':<30} {'Gen':>4} {'Fitness':>8} {'Lessons':>8} {'Beliefs':>8} {'Observed':>9} {'Frontier':>9} {'Valid':>6}")
    print("-" * 95)

    sorted_results = sorted(results.items(), key=lambda x: -x[1]["fitness"])
    for name, data in sorted_results:
        m = data["metrics"]
        valid = "PASS" if m["validator_passes"] else "FAIL"
        frontier = f"{m['frontier_resolved']}/{m['frontier_open']+m['frontier_resolved']}"
        gen = lineage.get(name, {}).get("generation", 1)
        print(
            f"{name:<30} {gen:>4} {data['fitness']:>8.1f} {m['lessons_count']:>8} "
            f"{m['beliefs_count']:>8} {m['observed_count']:>9} "
            f"{frontier:>9} {valid:>6}"
        )

    if len(sorted_results) >= 2:
        best = sorted_results[0]
        worst = sorted_results[-1]
        print(f"\nBest:  {best[0]} (fitness={best[1]['fitness']:.1f})")
        print(f"Worst: {worst[0]} (fitness={worst[1]['fitness']:.1f})")

        # Identify which belief differences matter
        print("\n## Analysis")
        for name, data in sorted_results:
            variant_name = name.replace("belief-", "")
            if variant_name in VARIANTS:
                v = VARIANTS[variant_name]
                status = "CONFIRMED" if data["fitness"] > sorted_results[len(sorted_results)//2][1]["fitness"] else "REFUTED"
                print(f"  {variant_name}: {v['hypothesis']}")
                print(f"    → {status} (fitness={data['fitness']:.1f})")


def cmd_synthesize():
    """Extract lessons about which beliefs matter."""
    if not RESULTS_FILE.exists():
        print("No results. Run 'compare' first.")
        sys.exit(1)

    results = json.loads(RESULTS_FILE.read_text())
    sorted_results = sorted(results.items(), key=lambda x: -x[1]["fitness"])

    print("=== BELIEF EVOLUTION SYNTHESIS ===\n")

    if len(sorted_results) < 2:
        print("Need at least 2 variants to synthesize. Spawn and run more.")
        return

    best_name, best_data = sorted_results[0]
    worst_name, worst_data = sorted_results[-1]
    avg_fitness = sum(d["fitness"] for _, d in sorted_results) / len(sorted_results)

    print(f"Variants tested:  {len(sorted_results)}")
    print(f"Average fitness:  {avg_fitness:.1f}")
    print(f"Best variant:     {best_name} ({best_data['fitness']:.1f})")
    print(f"Worst variant:    {worst_name} ({worst_data['fitness']:.1f})")
    print()

    # Identify which modifications helped/hurt
    print("## Belief Impact Analysis\n")
    control_fitness = results.get("belief-control", {}).get("fitness", avg_fitness)

    for name, data in sorted_results:
        variant_name = name.replace("belief-", "")
        if variant_name in VARIANTS:
            delta = data["fitness"] - control_fitness
            direction = "+" if delta >= 0 else ""
            v = VARIANTS[variant_name]
            print(f"  {variant_name}: {direction}{delta:.1f} vs control")
            print(f"    Hypothesis: {v['hypothesis']}")
            bm, bk = best_data["metrics"], data["metrics"]
            print(f"    Lessons: {data['metrics']['lessons_count']}, Observed: {data['metrics']['observed_count']}")
            print()

    print("## Recommendations")
    print()

    # Check which dimensions matter most
    dims = []
    for name, data in sorted_results:
        variant_name = name.replace("belief-", "")
        if variant_name != "control" and variant_name in VARIANTS:
            delta = data["fitness"] - control_fitness
            dims.append((abs(delta), variant_name, delta))

    dims.sort(reverse=True)
    if dims:
        print("  Belief dimensions ranked by impact (|delta| from control):")
        for abs_delta, name, delta in dims:
            impact = "HELPS" if delta > 0 else "HURTS" if delta < 0 else "NEUTRAL"
            print(f"    {abs_delta:>5.1f}  {name:<25} → {impact}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "variants":
        cmd_variants()
    elif cmd == "spawn":
        if len(sys.argv) < 3:
            print("Usage: belief_evolve.py spawn <variant>")
            sys.exit(1)
        cmd_spawn(sys.argv[2])
    elif cmd == "spawn-all":
        cmd_spawn_all()
    elif cmd == "combine":
        if len(sys.argv) < 4:
            print("Usage: belief_evolve.py combine <variant1> <variant2> [variant3...]")
            sys.exit(1)
        cmd_combine(sys.argv[2:])
    elif cmd == "evaluate":
        if len(sys.argv) < 3:
            print("Usage: belief_evolve.py evaluate <child-name>")
            sys.exit(1)
        cmd_evaluate(sys.argv[2])
    elif cmd == "evaluate-all":
        cmd_evaluate_all()
    elif cmd == "compare":
        cmd_compare()
    elif cmd == "lineage":
        cmd_lineage()
    elif cmd == "synthesize":
        cmd_synthesize()
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
