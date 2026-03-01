#!/usr/bin/env python3
"""close_lane.py — F-META: reduce friction in lane closure.

Appends a MERGED/ABANDONED row to tasks/SWARM-LANES.md for a given lane ID
and optionally updates the target FRONTIER.md with a status note.

By default, prior rows for the lane are removed (merge-on-close) to reduce
SWARM-LANES bloat (L-340). Use --no-merge to preserve all prior rows.

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


def count_prior_rows(lane_id: str) -> int:
    """Count existing rows for this lane in SWARM-LANES.md."""
    count = 0
    with open(LANES_FILE) as f:
        for line in f:
            if not line.startswith("|"):
                continue
            cols = [c.strip() for c in line.split("|")]
            if len(cols) >= 3 and cols[2] == lane_id:
                count += 1
    return count


def remove_prior_rows(lane_id: str) -> int:
    """Remove all existing rows for lane_id from SWARM-LANES.md. Returns count removed."""
    with open(LANES_FILE) as f:
        lines = f.readlines()
    kept = []
    removed = 0
    for line in lines:
        if line.startswith("|"):
            cols = [c.strip() for c in line.split("|")]
            if len(cols) >= 3 and cols[2] == lane_id:
                removed += 1
                continue
        kept.append(line)
    with open(LANES_FILE, "w") as f:
        f.writelines(kept)
    return removed


def append_closure_row(
    lane_id: str,
    status: str,
    note: str,
    session: str,
    author: str,
    model: str,
    merge: bool = True,
) -> None:
    today = date.today().isoformat()
    row = latest = find_latest_lane_row(lane_id)
    if row is None:
        print(f"WARNING: lane {lane_id} not found in SWARM-LANES.md — appending stub closure", file=sys.stderr)
        branch = "local"
        scope_key = ""
        tags = f"intent=closure, progress=closed"
    else:
        # Carry forward branch/scope from latest row
        branch = row[5] if len(row) > 5 else "local"
        scope_key = row[8] if len(row) > 8 else ""
        existing_etc = row[10] if len(row) > 10 else ""
        # Strip old next_step, add closed status
        existing_etc_clean = re.sub(r"next_step=[^\s,|]+", "", existing_etc).strip().strip(",")
        tags = f"{existing_etc_clean}, progress=closed, next_step=none".lstrip(", ")

    if merge:
        removed = remove_prior_rows(lane_id)
        if removed:
            print(f"Removed {removed} prior row(s) for {lane_id} (merge-on-close)")

    line = (
        f"| {today} | {lane_id} | {session} | {author} | {branch} | - | {model} | close_lane.py | "
        f"{scope_key} | {tags} | {status} | {note} |\n"
    )
    with open(LANES_FILE, "a") as f:
        f.write(line)
    display = LANES_FILE.relative_to(REPO_ROOT) if LANES_FILE.is_relative_to(REPO_ROOT) else LANES_FILE
    print(f"Appended {status} closure for {lane_id} to {display}")


def main():
    parser = argparse.ArgumentParser(description="Close a swarm lane with minimal friction.")
    parser.add_argument("--lane", required=True, help="Lane ID, e.g. L-S186-DOMEX-BRN")
    parser.add_argument("--status", default="MERGED", choices=sorted(VALID_STATUSES),
                        help="Closure status (default: MERGED)")
    parser.add_argument("--note", default="", help="Closure note / summary")
    # Dynamic session detection via swarm_io (fixes hardcoded S186 bug — L-488)
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from swarm_io import session_number
        _default_session = f"S{session_number()}"
    except Exception:
        _default_session = "S000"
    parser.add_argument("--session", default=_default_session, help="Current session tag (auto-detected)")
    parser.add_argument("--author", default="claude-code", help="Author identifier")
    parser.add_argument("--model", default="claude-sonnet-4-6", help="Model used")
    parser.add_argument("--no-merge", action="store_true",
                        help="Disable merge-on-close: keep all prior rows (append-only mode)")
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
        merge=not args.no_merge,
    )


if __name__ == "__main__":
    main()
