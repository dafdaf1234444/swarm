#!/usr/bin/env python3
"""
orient.py — Single-command session orientation for swarm nodes.

Synthesizes maintenance status, NEXT.md priorities, FRONTIER.md open questions,
and INDEX.md state counts into a decision-ready snapshot.

Replaces the manual pattern of: read NEXT.md + INDEX.md + FRONTIER.md + run maintenance.py.

Usage:
    python3 tools/orient.py           # full orientation
    python3 tools/orient.py --brief   # compact one-screen summary
"""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def run_maintenance():
    """Run maintenance --quick and return stdout."""
    result = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "maintenance.py"), "--quick"],
        capture_output=True, text=True, cwd=ROOT
    )
    return result.stdout + result.stderr


def read_file(relpath):
    try:
        return (ROOT / relpath).read_text(encoding="utf-8")
    except Exception:
        return ""


def extract_state_line(index_text):
    """Extract session + counts from INDEX.md header."""
    session = "S?"
    m = re.search(r"Sessions:\s*(\d+)", index_text[:300])
    if m:
        session = f"S{m.group(1)}"
    counts = "?"
    m2 = re.search(r"(\d+)\s+lessons", index_text[:500])
    m3 = re.search(r"(\d+)\s+principles", index_text[:500])
    m4 = re.search(r"(\d+)\s+beliefs", index_text[:500])
    m5 = re.search(r"(\d+)\s+frontier", index_text[:500])
    parts = []
    if m2: parts.append(f"{m2.group(1)}L")
    if m3: parts.append(f"{m3.group(1)}P")
    if m4: parts.append(f"{m4.group(1)}B")
    if m5: parts.append(f"{m5.group(1)}F")
    counts = " ".join(parts) if parts else "?"
    return session, counts


def extract_next_priorities(next_text):
    """Extract numbered items from 'For next session' section."""
    m = re.search(r"## For next session\n(.*?)(?:\n##|\Z)", next_text, re.DOTALL)
    if not m:
        return []
    items = re.findall(r"^\d+\.\s+\*\*(.+?)\*\*", m.group(1), re.MULTILINE)
    if not items:
        items = re.findall(r"^\d+\.\s+(.+)$", m.group(1), re.MULTILINE)
    return [i[:100] for i in items[:6]]


def extract_key_state(next_text):
    """Extract key state lines (compact URGENT, counts, etc.)."""
    m = re.search(r"## Key state\n(.*?)(?:\n##|\Z)", next_text, re.DOTALL)
    if not m:
        return []
    lines = [l.strip("- ").strip() for l in m.group(1).splitlines()
             if l.strip().startswith("-")]
    return [l[:100] for l in lines[:4]]


def extract_critical_frontiers(frontier_text):
    """Extract Critical and Important frontier titles."""
    items = []
    for section in ("## Critical", "## Important"):
        m = re.search(rf"{re.escape(section)}\n(.*?)(?:\n##|\Z)", frontier_text, re.DOTALL)
        if not m:
            continue
        bullets = re.findall(r"^- \*\*(F\d+)\*\*:(.+)", m.group(1), re.MULTILINE)
        for fid, desc in bullets:
            first = desc.strip().split(".")[0][:80]
            items.append(f"{fid}: {first}")
    return items


def classify_maint(maint_out):
    """Return urgency level string from maintenance output."""
    if "URGENT" in maint_out:
        return "URGENT"
    if "[DUE]" in maint_out:
        return "DUE items present"
    if "[PERIODIC]" in maint_out:
        return "periodics due"
    return "NOTICE-only"


def extract_session_log_tail(log_text, n=10):
    """Return last N non-header session log lines (behavioral pattern signal)."""
    lines = [l for l in log_text.splitlines()
             if l.strip() and not l.startswith("#") and "|" in l]
    return lines[-n:]


def main():
    brief = "--brief" in sys.argv

    maint_out = run_maintenance()
    index_text = read_file("memory/INDEX.md")
    next_text = read_file("tasks/NEXT.md")
    frontier_text = read_file("tasks/FRONTIER.md")
    log_text = read_file("memory/SESSION-LOG.md") if not brief else ""

    session, counts = extract_state_line(index_text)
    maint_level = classify_maint(maint_out)

    # Header
    print(f"=== ORIENT {session} | {counts} ===")
    print(f"Maintenance: {maint_level}")
    print()

    # Maintenance details (skip if NOTICE-only in brief mode)
    if not brief or maint_level != "NOTICE-only":
        signal_lines = [l for l in maint_out.splitlines()
                        if l.strip() and "===" not in l and "maintenance" not in l.lower()[:10]]
        if signal_lines:
            print("--- Maintenance ---")
            for line in signal_lines[:10]:
                print(f"  {line}")
            print()

    # Key state
    key_state = extract_key_state(next_text)
    if key_state:
        print("--- Key state ---")
        for s in key_state:
            print(f"  {s}")
        print()

    # Priorities
    priorities = extract_next_priorities(next_text)
    if priorities:
        print("--- Priorities ---")
        for i, p in enumerate(priorities, 1):
            print(f"  {i}. {p}")
        print()

    # Frontiers
    frontiers = extract_critical_frontiers(frontier_text)
    if frontiers:
        print("--- Open frontiers (critical/important) ---")
        for f in frontiers:
            print(f"  • {f}")
        print()

    # Session log tail (full mode only — last 10 entries = behavioral signal)
    if not brief and log_text:
        tail = extract_session_log_tail(log_text)
        if tail:
            print("--- Recent sessions (behavioral pattern) ---")
            for entry in tail:
                print(f"  {entry[:120]}")
            print()

    # Suggested action
    print("--- Suggested next action ---")
    if "URGENT" in maint_out:
        # Find what's urgent
        urgent_lines = [l.strip() for l in maint_out.splitlines() if "URGENT" in l]
        for l in urgent_lines[:2]:
            print(f"  URGENT: {l}")
    elif "[DUE]" in maint_out:
        # Find the actual DUE item lines (marked with !)
        due_lines = [l.strip() for l in maint_out.splitlines() if l.strip().startswith("!")]
        for l in due_lines[:2]:
            print(f"  DUE: {l.lstrip('! ')}")
    elif "[PERIODIC]" in maint_out:
        periodic_lines = [l.strip() for l in maint_out.splitlines() if l.strip().startswith("~")]
        for l in periodic_lines[:2]:
            print(f"  PERIODIC: {l.lstrip('~ ')}")
    elif priorities:
        print(f"  {priorities[0]}")
    else:
        print("  State clean — pick a frontier or run a periodic")


if __name__ == "__main__":
    main()
