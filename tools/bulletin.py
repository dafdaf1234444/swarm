#!/usr/bin/env python3
"""
bulletin.py — Inter-swarm communication via bulletins.

Usage:
    python3 tools/bulletin.py write <swarm-name> <type> <message>
    python3 tools/bulletin.py read [swarm-name]
    python3 tools/bulletin.py scan
    python3 tools/bulletin.py sync <child-name>

Types: discovery, question, warning, principle
Sync copies parent bulletins into a child's workspace for cross-swarm reading.
"""

import re
import shutil
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BULLETINS_DIR = REPO_ROOT / "experiments" / "inter-swarm" / "bulletins"
CHILDREN_DIR = REPO_ROOT / "experiments" / "children"


def write_bulletin(swarm_name: str, bulletin_type: str, message: str):
    """Append a bulletin to a swarm's bulletin file."""
    valid_types = {"discovery", "question", "warning", "principle"}
    if bulletin_type not in valid_types:
        print(f"Invalid type: {bulletin_type}. Use: {valid_types}")
        sys.exit(1)

    BULLETINS_DIR.mkdir(parents=True, exist_ok=True)
    bulletin_file = BULLETINS_DIR / f"{swarm_name}.md"

    entry = (
        f"\n---\n"
        f"# Bulletin from: {swarm_name}\n"
        f"Date: {date.today()}\n"
        f"Type: {bulletin_type}\n\n"
        f"## Content\n"
        f"{message}\n"
    )

    with open(bulletin_file, "a") as f:
        f.write(entry)

    print(f"Bulletin written to {bulletin_file}")


def read_bulletins(swarm_name: str = None):
    """Read bulletins, optionally filtered by swarm name."""
    if not BULLETINS_DIR.exists():
        print("No bulletins directory found.")
        return

    files = (
        [BULLETINS_DIR / f"{swarm_name}.md"]
        if swarm_name
        else sorted(BULLETINS_DIR.glob("*.md"))
    )

    for f in files:
        if not f.exists():
            if swarm_name:
                print(f"No bulletins from {swarm_name}")
            continue
        print(f.read_text())


def scan_bulletins():
    """Scan all bulletins and produce a summary."""
    if not BULLETINS_DIR.exists():
        print("No bulletins directory found.")
        return

    files = sorted(BULLETINS_DIR.glob("*.md"))
    if not files:
        print("No bulletins found.")
        return

    stats = {
        "total": 0,
        "discovery": 0,
        "question": 0,
        "warning": 0,
        "principle": 0,
        "swarms": set(),
    }

    for f in files:
        text = f.read_text()
        swarm_name = f.stem
        stats["swarms"].add(swarm_name)

        for m in re.finditer(r"Type:\s*(\w+)", text):
            btype = m.group(1).lower()
            stats["total"] += 1
            if btype in stats:
                stats[btype] += 1

    print("=== BULLETIN SCAN ===")
    print(f"Swarms reporting: {len(stats['swarms'])} ({', '.join(sorted(stats['swarms']))})")
    print(f"Total bulletins: {stats['total']}")
    print(f"  Discoveries: {stats['discovery']}")
    print(f"  Questions: {stats['question']}")
    print(f"  Warnings: {stats['warning']}")
    print(f"  Principles: {stats['principle']}")


def sync_to_child(child_name: str):
    """Copy parent bulletins into a child swarm for cross-swarm reading."""
    child_dir = CHILDREN_DIR / child_name
    if not child_dir.exists():
        print(f"Child '{child_name}' not found at {child_dir}")
        sys.exit(1)

    if not BULLETINS_DIR.exists():
        print("No bulletins to sync.")
        return

    # Create bulletins dir in child workspace
    child_bulletins = child_dir / "workspace" / "bulletins"
    child_bulletins.mkdir(parents=True, exist_ok=True)

    # Copy all bulletins EXCEPT the child's own
    copied = 0
    for f in sorted(BULLETINS_DIR.glob("*.md")):
        if f.stem == child_name:
            continue  # Don't copy own bulletins
        shutil.copy2(f, child_bulletins / f.name)
        copied += 1

    print(f"Synced {copied} bulletin file(s) to {child_bulletins}")
    print(f"Child '{child_name}' can now read sibling discoveries.")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "write":
        if len(sys.argv) < 5:
            print("Usage: bulletin.py write <swarm-name> <type> <message>")
            sys.exit(1)
        write_bulletin(sys.argv[2], sys.argv[3], " ".join(sys.argv[4:]))

    elif cmd == "read":
        swarm_name = sys.argv[2] if len(sys.argv) > 2 else None
        read_bulletins(swarm_name)

    elif cmd == "scan":
        scan_bulletins()

    elif cmd == "sync":
        if len(sys.argv) < 3:
            print("Usage: bulletin.py sync <child-name>")
            sys.exit(1)
        sync_to_child(sys.argv[2])

    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
