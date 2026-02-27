#!/usr/bin/env python3
"""close_lane.py — F-META: reduce friction in lane closure.

Appends a MERGED/ABANDONED row to tasks/SWARM-LANES.md for a given lane ID
and optionally updates the target FRONTIER.md with a status note.

Usage:
  python3 tools/close_lane.py --lane L-S186-DOMEX-BRN --status MERGED \\
      --note "BRN3 baseline complete, Sharpe compaction confirmed (L-268)"
"""

import argparse
import sys
import re
from datetime import date, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
LANES_FILE = REPO_ROOT / "tasks" / "SWARM-LANES.md"

VALID_STATUSES = {"MERGED", "ABANDONED", "SUPERSEDED"}


def find_latest_lane_row(lane_id: str) -> dict | None:
    """Return the most recent row for this lane from SWARM-LANES.md."""
    rows = []
    with open(LANES_FILE) as f:
        for line in f:
            if not line.startswith("|"):
                continue
            cols = [c.strip() for c in line.split("|")]
            if len(cols) < 13:
                continue
            if cols[2] == lane_id:
                rows.append(cols)
    return rows[-1] if rows else None


def append_closure_row(
    lane_id: str,
    status: str,
    note: str,
    session: str,
    author: str,
    model: str,
) -> None:
    today = date.today().isoformat()
    row = latest = find_latest_lane_row(lane_id)
    if row is None:
        print(f"WARNING: lane {lane_id} not found in SWARM-LANES.md — appending stub closure", file=sys.stderr)
        branch = "local"
        scope_key = ""
        setup = ""
        tags = f"intent=closure, progress=closed"
    else:
        # Carry forward branch/scope from latest row
        branch = row[5] if len(row) > 5 else "local"
        scope_key = row[8] if len(row) > 8 else ""
        existing_etc = row[10] if len(row) > 10 else ""
        # Strip old next_step, add closed status
        existing_etc_clean = re.sub(r"next_step=[^\s,|]+", "", existing_etc).strip().strip(",")
        tags = f"{existing_etc_clean}, progress=closed, next_step=none".lstrip(", ")

    line = (
        f"| {today} | {lane_id} | {session} | {author} | {branch} | - | {model} | close_lane.py | "
        f"{scope_key} | {tags} | {status} | {note} |\n"
    )
    with open(LANES_FILE, "a") as f:
        f.write(line)
    print(f"Appended {status} closure for {lane_id} to {LANES_FILE.relative_to(REPO_ROOT)}")


def main():
    parser = argparse.ArgumentParser(description="Close a swarm lane with minimal friction.")
    parser.add_argument("--lane", required=True, help="Lane ID, e.g. L-S186-DOMEX-BRN")
    parser.add_argument("--status", default="MERGED", choices=sorted(VALID_STATUSES),
                        help="Closure status (default: MERGED)")
    parser.add_argument("--note", default="", help="Closure note / summary")
    parser.add_argument("--session", default="S186", help="Current session tag, e.g. S186")
    parser.add_argument("--author", default="claude-code", help="Author identifier")
    parser.add_argument("--model", default="claude-sonnet-4-6", help="Model used")
    args = parser.parse_args()

    if not args.note:
        args.note = f"Lane closed via close_lane.py (no note provided)"

    append_closure_row(
        lane_id=args.lane,
        status=args.status,
        note=args.note,
        session=args.session,
        author=args.author,
        model=args.model,
    )


if __name__ == "__main__":
    main()
