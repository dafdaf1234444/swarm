#!/usr/bin/env python3
"""
evolve.py — Automated evolution pipeline for the swarm.

Usage:
    python3 tools/evolve.py init <child-name> <task-description>
    python3 tools/evolve.py harvest <child-name>
    python3 tools/evolve.py integrate <child-name> [--dry-run]
    python3 tools/evolve.py cycle <child-name> <task-description>

Commands:
    init      — Spawn child swarm with task, output sub-agent prompt
    harvest   — Evaluate child + generate merge-back report
    integrate — Auto-integrate novel rules/questions into parent
    cycle     — Full pipeline summary (init → agent → harvest → integrate)

This closes the evolution loop: spawn → run → evaluate → learn.
The "self-developing system" pattern the human described.
"""

import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CHILDREN_DIR = REPO_ROOT / "experiments" / "children"


def get_next_principle_id() -> int:
    """Find the next available P-NNN id."""
    principles = REPO_ROOT / "memory" / "PRINCIPLES.md"
    if not principles.exists():
        return 1
    text = principles.read_text()
    ids = [int(m.group(1)) for m in re.finditer(r"\*\*P-(\d+)\*\*", text)]
    return max(ids) + 1 if ids else 1


def get_next_lesson_id() -> int:
    """Find the next available L-NNN id."""
    lessons_dir = REPO_ROOT / "memory" / "lessons"
    if not lessons_dir.exists():
        return 1
    ids = []
    for f in lessons_dir.glob("L-*.md"):
        m = re.match(r"L-(\d+)", f.stem)
        if m:
            ids.append(int(m.group(1)))
    return max(ids) + 1 if ids else 1


def get_next_frontier_id() -> int:
    """Find the next available F-NN id."""
    frontier = REPO_ROOT / "tasks" / "FRONTIER.md"
    if not frontier.exists():
        return 1
    text = frontier.read_text()
    ids = [int(m.group(1)) for m in re.finditer(r"F(\d+)", text)]
    return max(ids) + 1 if ids else 1


def init_child(child_name: str, task_description: str):
    """Spawn child swarm with task, output sub-agent prompt."""
    # Use agent_swarm.py to create
    agent_swarm = REPO_ROOT / "tools" / "agent_swarm.py"
    r = subprocess.run(
        ["python3", str(agent_swarm), "create", child_name, task_description],
        capture_output=True, text=True
    )
    if r.returncode != 0:
        print(f"Failed to create child: {r.stderr}")
        sys.exit(1)
    print(r.stdout)

    # Generate prompt
    r = subprocess.run(
        ["python3", str(agent_swarm), "prompt", child_name],
        capture_output=True, text=True
    )
    print("\n" + "=" * 60)
    print("SUB-AGENT PROMPT (copy into Task tool):")
    print("=" * 60)
    print(r.stdout)
    print("=" * 60)

    child_dir = CHILDREN_DIR / child_name
    print(f"\nChild ready at: {child_dir}")
    print(f"Next steps:")
    print(f"  1. Launch sub-agent with the prompt above")
    print(f"  2. After completion: python3 tools/evolve.py harvest {child_name}")
    print(f"  3. Review: python3 tools/evolve.py integrate {child_name} --dry-run")
    print(f"  4. Apply: python3 tools/evolve.py integrate {child_name}")


def harvest_child(child_name: str) -> dict:
    """Evaluate child + generate merge-back report."""
    child_dir = CHILDREN_DIR / child_name
    if not child_dir.exists():
        print(f"Child '{child_name}' does not exist at {child_dir}")
        sys.exit(1)

    # Evaluate viability
    swarm_test = REPO_ROOT / "tools" / "swarm_test.py"
    r = subprocess.run(
        ["python3", str(swarm_test), "evaluate", str(child_dir)],
        capture_output=True, text=True
    )
    print("=== VIABILITY ===")
    print(r.stdout)

    # Merge-back report
    merge_back = REPO_ROOT / "tools" / "merge_back.py"
    r = subprocess.run(
        ["python3", str(merge_back), str(child_dir)],
        capture_output=True, text=True
    )
    print("\n=== MERGE-BACK ===")
    print(r.stdout)

    # Parse results for return
    report_path = REPO_ROOT / "experiments" / "merge-reports" / f"{child_name}.md"
    report = report_path.read_text() if report_path.exists() else ""

    novel_count = 0
    m = re.search(r"Novel rules: (\d+)/", report)
    if m:
        novel_count = int(m.group(1))

    viability = "unknown"
    vm = re.search(r"Viability: (\d+/4)", r.stdout)
    if vm:
        viability = vm.group(1)

    return {
        "child_name": child_name,
        "viability": viability,
        "novel_rules": novel_count,
        "report": report,
    }


def integrate_child(child_name: str, dry_run: bool = False):
    """Auto-integrate novel rules/questions into parent."""
    child_dir = CHILDREN_DIR / child_name
    if not child_dir.exists():
        print(f"Child '{child_name}' does not exist")
        sys.exit(1)

    # Load merge-back report
    report_path = REPO_ROOT / "experiments" / "merge-reports" / f"{child_name}.md"
    if not report_path.exists():
        print(f"No merge-back report. Run 'harvest' first.")
        sys.exit(1)

    report = report_path.read_text()

    # Extract novel rules from child lessons
    child_lessons_dir = child_dir / "memory" / "lessons"
    parent_principles = REPO_ROOT / "memory" / "PRINCIPLES.md"
    parent_principles_text = parent_principles.read_text() if parent_principles.exists() else ""

    parent_rules_lower = set()
    for m in re.finditer(r"\*\*P-\d+\*\*:\s*(.+?)(?:\(L-|\Z)", parent_principles_text):
        parent_rules_lower.add(m.group(1).strip().lower())

    novel_rules = []
    if child_lessons_dir.exists():
        for f in sorted(child_lessons_dir.glob("L-*.md")):
            if f.name == "TEMPLATE.md":
                continue
            text = f.read_text()
            rule_m = re.search(
                r"## Rule extracted.*?\n(.+?)(?:\n\n|\n##|\Z)",
                text, re.DOTALL
            )
            if rule_m:
                rule = rule_m.group(1).strip()
                # Check novelty (same logic as merge_back.py)
                rule_lower = rule.lower()
                is_novel = True
                for pr in parent_rules_lower:
                    child_words = set(rule_lower.split())
                    parent_words = set(pr.split())
                    if len(child_words & parent_words) > 0.6 * len(child_words):
                        is_novel = False
                        break
                if is_novel:
                    novel_rules.append(rule)

    # Extract novel frontier questions
    child_frontier = child_dir / "tasks" / "FRONTIER.md"
    parent_frontier = REPO_ROOT / "tasks" / "FRONTIER.md"
    parent_frontier_text = parent_frontier.read_text() if parent_frontier.exists() else ""

    novel_questions = []
    if child_frontier.exists():
        child_text = child_frontier.read_text()
        child_qs = re.findall(r"^\- \*\*F\d+\*\*:\s*(.+)$", child_text, re.MULTILINE)
        for q in child_qs:
            # Skip if parent already has a similar question
            q_lower = q.lower()
            q_words = set(q_lower.split())
            is_novel = True
            for line in parent_frontier_text.lower().splitlines():
                if not line.strip().startswith("-"):
                    continue
                p_words = set(line.split())
                if len(q_words & p_words) > 0.5 * len(q_words):
                    is_novel = False
                    break
            if is_novel:
                novel_questions.append(q)

    # Report what we'd integrate
    print(f"=== INTEGRATION PLAN for {child_name} ===\n")

    if novel_rules:
        next_p = get_next_principle_id()
        next_l = get_next_lesson_id()
        print(f"Novel rules to add to PRINCIPLES.md ({len(novel_rules)}):")
        for i, rule in enumerate(novel_rules):
            pid = next_p + i
            print(f"  P-{pid:03d}: {rule} (from {child_name})")
    else:
        print("No novel rules to integrate.")

    if novel_questions:
        next_f = get_next_frontier_id()
        print(f"\nNovel frontier questions to add ({len(novel_questions)}):")
        for i, q in enumerate(novel_questions):
            fid = next_f + i
            print(f"  F{fid}: {q}")
    else:
        print("\nNo novel frontier questions.")

    if dry_run:
        print("\n[DRY RUN — no changes made]")
        return

    if not novel_rules and not novel_questions:
        print("\nNothing to integrate. Child confirmed existing knowledge.")
        return

    # Actually integrate
    changes_made = []

    # Add novel rules to PRINCIPLES.md
    if novel_rules:
        next_p = get_next_principle_id()
        additions = []
        for i, rule in enumerate(novel_rules):
            pid = next_p + i
            additions.append(
                f"- **P-{pid:03d}**: {rule} (from child:{child_name})"
            )

        # Append to the end of the last section in PRINCIPLES.md
        new_section = (
            f"\n## From child:{child_name}\n" +
            "\n".join(additions) + "\n"
        )
        with open(parent_principles, "a") as f:
            f.write(new_section)
        changes_made.append(f"Added {len(novel_rules)} rule(s) to PRINCIPLES.md")
        print(f"\nAdded {len(novel_rules)} rule(s) to PRINCIPLES.md")

    # Add novel questions to FRONTIER.md
    if novel_questions:
        next_f = get_next_frontier_id()
        additions = []
        for i, q in enumerate(novel_questions):
            fid = next_f + i
            additions.append(f"- **F{fid}**: {q} (from child:{child_name})")

        # Insert before ## Resolved section
        if "## Resolved" in parent_frontier_text:
            insert_point = parent_frontier_text.index("## Resolved")
            new_text = (
                parent_frontier_text[:insert_point] +
                "\n".join(additions) + "\n\n" +
                parent_frontier_text[insert_point:]
            )
        else:
            new_text = parent_frontier_text + "\n" + "\n".join(additions) + "\n"

        parent_frontier.write_text(new_text)
        changes_made.append(f"Added {len(novel_questions)} question(s) to FRONTIER.md")
        print(f"Added {len(novel_questions)} question(s) to FRONTIER.md")

    # Write integration log
    log_dir = REPO_ROOT / "experiments" / "integration-log"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_entry = {
        "child": child_name,
        "date": datetime.now().isoformat(),
        "novel_rules": len(novel_rules),
        "novel_questions": len(novel_questions),
        "changes": changes_made,
    }
    log_path = log_dir / f"{child_name}.json"
    log_path.write_text(json.dumps(log_entry, indent=2))
    print(f"\nIntegration logged to: {log_path}")


def show_cycle(child_name: str, task: str):
    """Show the full evolution cycle for reference."""
    print(f"=== EVOLUTION CYCLE: {child_name} ===\n")
    print(f"Task: {task}\n")
    print("Steps:")
    print(f"  1. INIT:      python3 tools/evolve.py init {child_name} \"{task}\"")
    print(f"  2. RUN:       Use Task tool with the generated prompt")
    print(f"  3. HARVEST:   python3 tools/evolve.py harvest {child_name}")
    print(f"  4. REVIEW:    python3 tools/evolve.py integrate {child_name} --dry-run")
    print(f"  5. INTEGRATE: python3 tools/evolve.py integrate {child_name}")
    print()
    print("Or for parallel evolution:")
    print(f"  - Spawn multiple children with different tasks")
    print(f"  - Launch sub-agents in parallel")
    print(f"  - Harvest all → compare viability → integrate best")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "init":
        if len(sys.argv) < 4:
            print("Usage: evolve.py init <child-name> <task-description>")
            sys.exit(1)
        init_child(sys.argv[2], " ".join(sys.argv[3:]))

    elif cmd == "harvest":
        if len(sys.argv) < 3:
            print("Usage: evolve.py harvest <child-name>")
            sys.exit(1)
        harvest_child(sys.argv[2])

    elif cmd == "integrate":
        if len(sys.argv) < 3:
            print("Usage: evolve.py integrate <child-name> [--dry-run]")
            sys.exit(1)
        dry_run = "--dry-run" in sys.argv
        integrate_child(sys.argv[2], dry_run)

    elif cmd == "cycle":
        if len(sys.argv) < 4:
            print("Usage: evolve.py cycle <child-name> <task-description>")
            sys.exit(1)
        show_cycle(sys.argv[2], " ".join(sys.argv[3:]))

    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
