#!/usr/bin/env python3
"""
session_tracker.py — Track session metrics for the swarm.

Usage:
    python3 tools/session_tracker.py record <session-number>
    python3 tools/session_tracker.py report
    python3 tools/session_tracker.py lambda

Records per-session metrics by analyzing git history.
Provides λ_swarm calculation (Langton's lambda for the swarm).
"""

import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TRACKER_FILE = REPO_ROOT / "experiments" / "session-metrics.json"


def _git(*args: str) -> str:
    try:
        r = subprocess.run(
            ["git", "-C", str(REPO_ROOT)] + list(args),
            capture_output=True, text=True, timeout=10
        )
        return r.stdout.strip()
    except Exception:
        return ""


def record_session(session_num: int):
    """Record metrics for a session by analyzing recent commits."""
    # Load existing data
    data = {}
    if TRACKER_FILE.exists():
        data = json.loads(TRACKER_FILE.read_text())

    sessions = data.get("sessions", {})

    # Get all commits (approximate session boundary by looking at commit timestamps)
    log = _git("log", "--oneline", "--format=%H %s")
    all_commits = log.splitlines() if log else []

    # Analyze recent commits for this session
    recent = _git("log", "--oneline", "-10", "--format=%H")
    recent_shas = recent.splitlines() if recent else []

    files_touched = set()
    commit_count = 0
    structural_change = False

    for sha in recent_shas:
        commit_count += 1
        # Get files changed in this commit
        diff_stat = _git("show", "--stat", "--name-only", sha)
        for line in diff_stat.splitlines():
            line = line.strip()
            if "/" in line or "." in line:
                files_touched.add(line)
                # Structural changes: CLAUDE.md, DEPS.md, validator, genesis
                if line in (
                    "CLAUDE.md", "beliefs/DEPS.md",
                    "tools/validate_beliefs.py", "workspace/genesis.sh"
                ):
                    structural_change = True

    # Count current state
    lessons_count = len(list(
        (REPO_ROOT / "memory" / "lessons").glob("L-*.md")
    ))
    principles_count = len(re.findall(
        r"\*\*P-\d+\*\*",
        (REPO_ROOT / "memory" / "PRINCIPLES.md").read_text()
    )) if (REPO_ROOT / "memory" / "PRINCIPLES.md").exists() else 0

    session_data = {
        "commits": commit_count,
        "files_touched": len(files_touched),
        "structural_change": structural_change,
        "lessons_total": lessons_count,
        "principles_total": principles_count,
    }

    sessions[str(session_num)] = session_data

    data["sessions"] = sessions
    data["latest_session"] = session_num
    TRACKER_FILE.parent.mkdir(parents=True, exist_ok=True)
    TRACKER_FILE.write_text(json.dumps(data, indent=2))

    print(f"Session {session_num} recorded:")
    print(f"  Commits: {commit_count}")
    print(f"  Files touched: {len(files_touched)}")
    print(f"  Structural change: {structural_change}")
    print(f"  Lessons total: {lessons_count}")
    print(f"  Principles total: {principles_count}")


def report():
    """Print a report of all tracked sessions."""
    if not TRACKER_FILE.exists():
        print("No session data. Run 'record' first.")
        return

    data = json.loads(TRACKER_FILE.read_text())
    sessions = data.get("sessions", {})

    print("=== SESSION METRICS ===\n")
    print(f"{'Session':<10} {'Commits':<10} {'Files':<10} {'Structural':<12} {'Lessons':<10} {'Principles':<12}")
    print("-" * 64)

    for sid in sorted(sessions.keys(), key=int):
        s = sessions[sid]
        struct = "Yes" if s.get("structural_change") else "No"
        print(
            f"{sid:<10} {s.get('commits', '?'):<10} "
            f"{s.get('files_touched', '?'):<10} {struct:<12} "
            f"{s.get('lessons_total', '?'):<10} {s.get('principles_total', '?'):<12}"
        )


def calculate_lambda():
    """Calculate Langton's lambda for the swarm."""
    if not TRACKER_FILE.exists():
        # Estimate from git history
        log = _git("log", "--oneline")
        total_commits = len(log.splitlines()) if log else 0

        # Count commits that touch structural files
        structural_files = [
            "CLAUDE.md", "beliefs/DEPS.md",
            "tools/validate_beliefs.py", "workspace/genesis.sh",
            "memory/OPERATIONS.md"
        ]
        structural_commits = 0
        for f in structural_files:
            flog = _git("log", "--oneline", "--", f)
            structural_commits += len(flog.splitlines()) if flog else 0

        # Rough dedup (some commits touch multiple structural files)
        structural_commits = min(structural_commits, total_commits)

        if total_commits == 0:
            print("No commits found.")
            return

        lambda_val = structural_commits / total_commits
        print(f"=== LANGTON'S λ (estimated from git) ===")
        print(f"Total commits: {total_commits}")
        print(f"Structural commits: {structural_commits}")
        print(f"λ_swarm ≈ {lambda_val:.2f}")
        print()

        if lambda_val < 0.2:
            print("Assessment: TOO LOW (Class I/II — frozen)")
            print("The system is not adapting enough. Consider challenging beliefs.")
        elif lambda_val < 0.4:
            print("Assessment: GOOD (Class IV — edge of chaos)")
            print("Healthy balance of structure and adaptation.")
        elif lambda_val < 0.7:
            print("Assessment: SLIGHTLY HIGH (trending toward Class III)")
            print("Consider more routine work, less structural change.")
        else:
            print("Assessment: TOO HIGH (Class III — chaotic)")
            print("Too much structural change. Stabilize before adding more.")
        return

    data = json.loads(TRACKER_FILE.read_text())
    sessions = data.get("sessions", {})

    total = len(sessions)
    structural = sum(
        1 for s in sessions.values() if s.get("structural_change")
    )

    if total == 0:
        print("No sessions recorded.")
        return

    lambda_val = structural / total
    print(f"=== LANGTON'S λ ===")
    print(f"Sessions: {total}")
    print(f"Structural changes: {structural}")
    print(f"λ_swarm = {lambda_val:.2f}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "record":
        session_num = int(sys.argv[2]) if len(sys.argv) > 2 else 35
        record_session(session_num)
    elif cmd == "report":
        report()
    elif cmd == "lambda":
        calculate_lambda()
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
