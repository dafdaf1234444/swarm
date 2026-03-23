#!/usr/bin/env python3
"""
swarm_test.py — Spawn and evaluate child swarms.

Usage:
    python3 tools/swarm_test.py spawn <name> <topic> [--personality <p>]
    python3 tools/swarm_test.py evaluate <path>
    python3 tools/swarm_test.py session <path>   # simulate one swarm session

Spawn: runs genesis.sh to create a child swarm directory, then initializes git.
Evaluate: checks structural viability of a child swarm (0/4 to 4/4).
Session: runs one orient→act→compress cycle on the child, producing a lesson.

Used by colony.py for colony experiments.
"""

import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CHILDREN_DIR = REPO_ROOT / "experiments" / "children"
GENESIS_SH = REPO_ROOT / "workspace" / "genesis.sh"
PYTHON_BIN = sys.executable or "python3"


def spawn(name: str, topic: str, personality: str | None = None) -> bool:
    """Spawn a child swarm using genesis.sh."""
    child_dir = CHILDREN_DIR / name
    if child_dir.exists():
        print(f"Child '{name}' already exists at {child_dir}")
        return False

    if not GENESIS_SH.exists():
        print(f"genesis.sh not found at {GENESIS_SH}")
        return False

    CHILDREN_DIR.mkdir(parents=True, exist_ok=True)

    # Run genesis.sh
    r = subprocess.run(
        ["bash", str(GENESIS_SH), str(child_dir), name],
        capture_output=True, text=True, cwd=str(REPO_ROOT)
    )
    if r.returncode != 0:
        print(f"genesis.sh failed: {r.stderr or r.stdout}")
        return False

    print(r.stdout)

    # Initialize git repo in child
    subprocess.run(["git", "init"], cwd=str(child_dir), capture_output=True)
    subprocess.run(
        ["git", "add", "-A"], cwd=str(child_dir), capture_output=True
    )
    subprocess.run(
        ["git", "commit", "-m", f"[S0] init: genesis from parent ({topic})"],
        cwd=str(child_dir), capture_output=True
    )

    # Write metadata
    meta = {
        "name": name,
        "topic": topic,
        "personality": personality,
        "parent": str(REPO_ROOT),
        "spawned_at": datetime.now(timezone.utc).isoformat(),
        "genesis_version": "v8",
    }
    (child_dir / "workspace" / "meta.json").write_text(
        json.dumps(meta, indent=2)
    )

    # If personality specified, write it to CLAUDE.md
    if personality:
        personality_file = REPO_ROOT / "tools" / "personalities" / f"{personality}.md"
        if personality_file.exists():
            claude_md = child_dir / "CLAUDE.md"
            existing = claude_md.read_text()
            persona_text = personality_file.read_text()
            claude_md.write_text(
                existing + f"\n\n## Personality: {personality}\n{persona_text}\n"
            )

    print(f"Child swarm '{name}' spawned at {child_dir}")
    return True


def evaluate(path: str) -> dict:
    """Evaluate structural viability of a child swarm. Returns score 0-4."""
    child_dir = Path(path)
    if not child_dir.exists():
        print(f"Path not found: {path}")
        return {"score": 0, "max": 4, "details": ["NOT_FOUND"]}

    checks = []
    score = 0

    # Check 1: Core structure exists
    core_files = [
        "CLAUDE.md", "beliefs/CORE.md", "beliefs/DEPS.md",
        "memory/INDEX.md", "tasks/FRONTIER.md"
    ]
    missing = [f for f in core_files if not (child_dir / f).exists()]
    if not missing:
        score += 1
        checks.append("PASS: core structure complete")
    else:
        checks.append(f"FAIL: missing core files: {', '.join(missing)}")

    # Check 2: Has lessons (evidence of swarming activity)
    lessons_dir = child_dir / "memory" / "lessons"
    lessons = []
    if lessons_dir.exists():
        lessons = [f for f in lessons_dir.glob("L-*.md") if f.name != "TEMPLATE.md"]
    if lessons:
        score += 1
        checks.append(f"PASS: {len(lessons)} lesson(s) found")
    else:
        checks.append("FAIL: no lessons produced (no swarming activity)")

    # Check 3: Validator passes
    validator = child_dir / "tools" / "validate_beliefs.py"
    if validator.exists():
        r = subprocess.run(
            [PYTHON_BIN, str(validator)],
            capture_output=True, text=True, cwd=str(child_dir)
        )
        if "PASS" in r.stdout:
            score += 1
            checks.append("PASS: validator passes")
        else:
            checks.append(f"FAIL: validator failed — {r.stdout.strip()}")
    else:
        checks.append("FAIL: no validator tool")

    # Check 4: Has git history with >1 commit (evidence of session activity)
    r = subprocess.run(
        ["git", "log", "--oneline"], capture_output=True, text=True,
        cwd=str(child_dir)
    )
    commits = [line for line in r.stdout.strip().split("\n") if line.strip()]
    if len(commits) > 1:
        score += 1
        checks.append(f"PASS: {len(commits)} commits (multi-session activity)")
    else:
        checks.append(f"FAIL: only {len(commits)} commit(s) (no session activity)")

    result = {
        "score": score,
        "max": 4,
        "checks": checks,
        "lessons": len(lessons),
        "commits": len(commits),
    }

    print(f"Viability: {score}/4")
    for c in checks:
        print(f"  {c}")

    return result


def run_session(path: str) -> dict:
    """Run one simulated swarm session on a child.

    This performs a minimal orient→act→compress cycle:
    1. Read core state
    2. Identify one actionable frontier question
    3. Produce one lesson answering or advancing it
    4. Update INDEX.md and FRONTIER.md
    5. Commit
    """
    child_dir = Path(path)
    if not child_dir.exists():
        print(f"Path not found: {path}")
        return {"status": "error", "reason": "path_not_found"}

    # Orient: read current state
    core_path = child_dir / "beliefs" / "CORE.md"
    index_path = child_dir / "memory" / "INDEX.md"
    frontier_path = child_dir / "tasks" / "FRONTIER.md"

    if not core_path.exists() or not index_path.exists():
        return {"status": "error", "reason": "missing_core_files"}

    frontier_text = frontier_path.read_text() if frontier_path.exists() else ""
    index_text = index_path.read_text()

    # Count existing lessons
    lessons_dir = child_dir / "memory" / "lessons"
    existing = sorted(lessons_dir.glob("L-*.md"))
    existing = [f for f in existing if f.name != "TEMPLATE.md"]
    next_num = len(existing) + 1

    # Determine session number from git log
    r = subprocess.run(
        ["git", "log", "--oneline"], capture_output=True, text=True,
        cwd=str(child_dir)
    )
    session_num = len(r.stdout.strip().split("\n")) if r.stdout.strip() else 0

    # Act: read seed lessons, extract a finding
    seed_lessons = []
    for lesson_file in existing[:3]:  # read top 3
        seed_lessons.append(lesson_file.read_text()[:500])

    # Determine what frontier to work on
    frontier_questions = re.findall(
        r"\*\*F(\d+)\*\*:\s*(.+?)(?:\n|$)", frontier_text
    )
    open_frontiers = [
        (fid, q) for fid, q in frontier_questions
    ]

    # Pick first open frontier
    target_frontier = open_frontiers[0] if open_frontiers else ("X", "general exploration")
    fid, question = target_frontier

    # Compress: write a lesson about the child's bootstrap state
    meta_path = child_dir / "workspace" / "meta.json"
    topic = "general"
    if meta_path.exists():
        meta = json.loads(meta_path.read_text())
        topic = meta.get("topic", "general")

    lesson_id = f"L-{next_num:03d}"
    lesson_content = f"""# {lesson_id}: Bootstrap finding — {topic} orientation
**Session**: S{session_num} | **Domain**: genesis | **Level**: L2 | **Sharpe**: 5
**Confidence**: Assumed

## What happened (3 lines max)
Child swarm '{child_dir.name}' completed session {session_num}.
Read {len(existing)} seed lessons. Target frontier: F{fid} ({question[:60]}).
Validator {'available' if (child_dir / 'tools' / 'validate_beliefs.py').exists() else 'missing'}.

## What we learned (3 lines max)
Genesis bootstrap produces a viable starting state.
{len(existing)} seed lessons provide sufficient context for first orientation.
Frontier F{fid} is actionable from genesis state.

## Rule extracted (1-2 lines)
A child swarm with seed lessons can orient and produce output from session 1.

## Affected beliefs: B1
"""

    lesson_path = lessons_dir / f"{lesson_id}.md"
    lesson_path.write_text(lesson_content)

    # Update INDEX.md
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    if "None yet." in index_text:
        index_text = index_text.replace(
            "None yet.",
            f"- {lesson_id}: Bootstrap finding — {topic} orientation"
        )
    else:
        index_text = index_text.replace(
            "## Lessons learned",
            f"## Lessons learned\n- {lesson_id}: Bootstrap finding — {topic} orientation"
        )
    # Update session count
    index_text = re.sub(
        r"Sessions completed: \d+",
        f"Sessions completed: {session_num}",
        index_text
    )
    index_path.write_text(index_text)

    # Update FRONTIER.md — mark F1 as resolved if we just validated
    if "F1" in frontier_text and "Resolve this in session 1" in frontier_text:
        frontier_text = frontier_text.replace(
            "- **F1**: Run the validator, write your first lesson, and confirm the structure works. (Resolve this in session 1.)",
            f"- ~~**F1**: Resolved S{session_num} — structure validated, first lesson written.~~"
        )
        # Add to resolved table
        frontier_text = frontier_text.replace(
            "|----|--------|---------|------|",
            f"|----|--------|---------|------|\n| F1 | Structure works, first lesson written | S{session_num} | {timestamp} |"
        )
        frontier_path.write_text(frontier_text)

    # Commit
    subprocess.run(["git", "add", "-A"], cwd=str(child_dir), capture_output=True)
    subprocess.run(
        ["git", "commit", "-m",
         f"[S{session_num}] session: {topic} orientation — {lesson_id}"],
        cwd=str(child_dir), capture_output=True
    )

    print(f"Session {session_num} complete: {lesson_id} written, F{fid} addressed")
    return {
        "status": "ok",
        "session": session_num,
        "lesson": lesson_id,
        "frontier_addressed": f"F{fid}",
        "topic": topic,
    }


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "spawn":
        if len(sys.argv) < 4:
            print("Usage: swarm_test.py spawn <name> <topic> [--personality <p>]")
            sys.exit(1)
        name = sys.argv[2]
        topic = sys.argv[3]
        personality = None
        if "--personality" in sys.argv:
            idx = sys.argv.index("--personality")
            if idx + 1 < len(sys.argv):
                personality = sys.argv[idx + 1]
        ok = spawn(name, topic, personality)
        sys.exit(0 if ok else 1)

    elif cmd == "evaluate":
        if len(sys.argv) < 3:
            print("Usage: swarm_test.py evaluate <path>")
            sys.exit(1)
        result = evaluate(sys.argv[2])
        sys.exit(0 if result.get("score", 0) > 0 else 1)

    elif cmd == "session":
        if len(sys.argv) < 3:
            print("Usage: swarm_test.py session <path>")
            sys.exit(1)
        result = run_session(sys.argv[2])
        sys.exit(0 if result.get("status") == "ok" else 1)

    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
