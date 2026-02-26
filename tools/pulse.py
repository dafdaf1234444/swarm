#!/usr/bin/env python3
"""
pulse.py — Colony pulse: quick session orientation.

Usage:
    python3 tools/pulse.py          # print to stdout
    python3 tools/pulse.py --save   # also write to memory/PULSE.md

Generates a snapshot of system state for fast session start:
- Recent commits and their modes
- Most recently modified files
- Active claims on frontier questions
- Frontier questions sorted by signal strength
- Active children and their status
"""

import io
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DECAY_FILE = REPO_ROOT / "experiments" / "frontier-decay.json"
CLAIMS_FILE = REPO_ROOT / "experiments" / "frontier-claims.json"
CHILDREN_DIR = REPO_ROOT / "experiments" / "children"
PULSE_PATH = REPO_ROOT / "memory" / "PULSE.md"


def _git(*args: str) -> str:
    try:
        r = subprocess.run(
            ["git", "-C", str(REPO_ROOT)] + list(args),
            capture_output=True, text=True, timeout=10
        )
        return r.stdout.strip()
    except Exception:
        return ""


def generate_pulse(out=None):
    """Generate the colony pulse. Prints to out (default sys.stdout)."""
    if out is None:
        out = sys.stdout

    def p(s=""):
        print(s, file=out)

    p("=== COLONY PULSE ===")
    p(f"Date: {date.today()}")
    p()

    # --- Recent commits ---
    p("## Recent Activity (last 10 commits)")
    log = _git("log", "--oneline", "-10", "--format=%h %s (%ar)")
    if log:
        for line in log.splitlines():
            p(f"  {line}")
    p()

    # --- Most recently modified files ---
    p("## Hot Files (modified in last 5 commits)")
    recent_shas = _git("log", "-5", "--format=%H").splitlines()
    file_counts = {}
    for sha in recent_shas:
        files = _git("diff-tree", "--no-commit-id", "--name-only", "-r", sha)
        for f in files.splitlines():
            f = f.strip()
            if f:
                file_counts[f] = file_counts.get(f, 0) + 1
    for f, count in sorted(file_counts.items(), key=lambda x: -x[1])[:10]:
        p(f"  {f} ({count}x)")
    p()

    # --- Active claims ---
    p("## Active Claims")
    if CLAIMS_FILE.exists():
        claims = json.loads(CLAIMS_FILE.read_text())
        active = {k: v for k, v in claims.items() if v.get("status") == "claimed"}
        if active:
            for fid, info in sorted(active.items()):
                p(f"  {fid}: claimed by {info.get('session', '?')} at {info.get('timestamp', '?')}")
        else:
            p("  No active claims.")
    else:
        p("  No claims file.")
    p()

    # --- Frontier questions by strength ---
    p("## Frontier Questions (by signal strength)")
    frontier_path = REPO_ROOT / "tasks" / "FRONTIER.md"
    if frontier_path.exists():
        text = frontier_path.read_text()
        resolved_pos = text.find("## Resolved")
        open_text = text[:resolved_pos] if resolved_pos > 0 else text

        decay = {}
        if DECAY_FILE.exists():
            decay = json.loads(DECAY_FILE.read_text())

        today = date.today().isoformat()
        questions = []
        for m in re.finditer(r"^- \*\*F(\d+)\*\*:\s*(.+)$", open_text, re.MULTILINE):
            fid = f"F{m.group(1)}"
            q_text = m.group(2).strip()
            last_active = decay.get(fid, {}).get("last_active", today)
            days = (date.fromisoformat(today) - date.fromisoformat(last_active)).days
            strength = 0.9 ** days
            questions.append((strength, fid, q_text))

        questions.sort(reverse=True)
        for strength, fid, q_text in questions[:8]:
            p(f"  [{strength:.2f}] {fid}: {q_text[:65]}")

        resolved_count = len(re.findall(r"^\| F\d+", text, re.MULTILINE))
        p(f"\n  Open: {len(questions)} | Resolved: {resolved_count}")
    p()

    # --- Active children ---
    p("## Children")
    if CHILDREN_DIR.exists():
        children = sorted([d for d in CHILDREN_DIR.iterdir() if d.is_dir()])
        if children:
            for child_dir in children:
                name = child_dir.name
                lessons = len(list((child_dir / "memory" / "lessons").glob("L-*.md"))) if (child_dir / "memory" / "lessons").exists() else 0
                log_path = REPO_ROOT / "experiments" / "integration-log" / f"{name}.json"
                status = "integrated" if log_path.exists() else ("active" if lessons > 0 else "spawned")
                p(f"  {name:<25} [{status}] lessons: {lessons}")
        else:
            p("  No children spawned.")
    else:
        p("  No children directory.")
    p()

    # --- System health ---
    p("## System Health")
    r = subprocess.run(
        ["python3", str(REPO_ROOT / "tools" / "validate_beliefs.py")],
        capture_output=True, text=True
    )
    swarmability_m = re.search(r"SWARMABILITY: (\d+/100)", r.stdout)
    entropy_m = re.search(r"Entropy items: (\d+)", r.stdout)
    p(f"  Swarmability: {swarmability_m.group(1) if swarmability_m else '?'}")
    p(f"  Entropy: {entropy_m.group(1) if entropy_m else '?'}")

    lessons_count = len(list((REPO_ROOT / "memory" / "lessons").glob("L-*.md")))
    principles_count = len(re.findall(
        r"P-\d+",
        (REPO_ROOT / "memory" / "PRINCIPLES.md").read_text()
    )) if (REPO_ROOT / "memory" / "PRINCIPLES.md").exists() else 0
    total_commits = len(_git("log", "--oneline").splitlines())

    p(f"  Commits: {total_commits} | Lessons: {lessons_count} | Principles: {principles_count}")


if __name__ == "__main__":
    save = "--save" in sys.argv

    if save:
        buf = io.StringIO()
        generate_pulse(buf)
        output = buf.getvalue()
        sys.stdout.write(output)
        PULSE_PATH.write_text(output)
        print(f"\nSaved to {PULSE_PATH}")
    else:
        generate_pulse()
