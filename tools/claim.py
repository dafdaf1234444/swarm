#!/usr/bin/env python3
"""tools/claim.py — Soft-claim protocol for concurrent session coordination

Prevents C-EDIT DUE-convergence collisions (L-557, F-CON2). Sessions declare
intent before editing shared files; check/release prevents duplicate work.
Lesson-slot pre-claiming (CE-4 fix, F-CON2): sessions atomically reserve the
next available L-NNN slot before writing a new lesson.

Usage:
  python3 tools/claim.py claim <file> [--session <id>]   # Claim a file
  python3 tools/claim.py check <file>                     # Check if claimed (exit 0=free, 1=claimed)
  python3 tools/claim.py release <file> [--session <id>] # Release claim
  python3 tools/claim.py list                             # List active claims
  python3 tools/claim.py gc                               # Garbage collect expired claims
  python3 tools/claim.py next-lesson [--session <id>]    # Claim next L-NNN slot; prints path
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

CLAIMS_DIR = Path("workspace/claims")
CLAIM_TTL_SECONDS = 120  # 2 minutes — sessions that crash leave auto-expiring claims (L-589: 300s→120s, commit cycle ~60s at N≥5)


def get_session_id():
    """Get current session ID from env or generate a stable one from PID."""
    return os.environ.get("SWARM_SESSION_ID", f"pid-{os.getpid()}")


def claim_path(file: str) -> Path:
    """Map a file path to its claim file in workspace/claims/."""
    safe = file.replace("/", "__").replace("\\", "__")
    return CLAIMS_DIR / f"{safe}.claim.json"


def read_claim(path: Path) -> dict | None:
    """Read a claim file; return None if missing or expired."""
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text())
        age = (datetime.now(timezone.utc) - datetime.fromisoformat(data["timestamp"])).total_seconds()
        if age > CLAIM_TTL_SECONDS:
            path.unlink(missing_ok=True)
            return None
        return data
    except (json.JSONDecodeError, KeyError, ValueError):
        return None


def cmd_claim(file: str, session: str) -> int:
    CLAIMS_DIR.mkdir(parents=True, exist_ok=True)
    path = claim_path(file)
    existing = read_claim(path)
    if existing and existing.get("session") != session:
        age = (datetime.now(timezone.utc) - datetime.fromisoformat(existing["timestamp"])).total_seconds()
        print(f"CLAIMED: {file} — held by {existing['session']} ({int(age)}s ago). Wait or choose different work.")
        return 1
    data = {"file": file, "session": session, "timestamp": datetime.now(timezone.utc).isoformat()}
    path.write_text(json.dumps(data, indent=2))
    print(f"CLAIMED: {file} by {session}")
    return 0


def cmd_check(file: str) -> int:
    path = claim_path(file)
    existing = read_claim(path)
    if existing:
        age = (datetime.now(timezone.utc) - datetime.fromisoformat(existing["timestamp"])).total_seconds()
        print(f"CLAIMED by {existing['session']} ({int(age)}s ago) — {file}")
        return 1
    print(f"FREE: {file}")
    return 0


def cmd_release(file: str, session: str) -> int:
    path = claim_path(file)
    existing = read_claim(path)
    if not existing:
        print(f"NOT CLAIMED: {file}")
        return 0
    if existing.get("session") != session:
        print(f"WARN: {file} is claimed by {existing['session']}, not {session} — not releasing")
        return 1
    path.unlink(missing_ok=True)
    print(f"RELEASED: {file} by {session}")
    return 0


def cmd_list() -> int:
    if not CLAIMS_DIR.exists():
        print("No claims directory.")
        return 0
    claims = []
    for p in CLAIMS_DIR.glob("*.claim.json"):
        data = read_claim(p)
        if data:
            age = (datetime.now(timezone.utc) - datetime.fromisoformat(data["timestamp"])).total_seconds()
            claims.append((data["file"], data["session"], int(age)))
    if not claims:
        print("No active claims.")
        return 0
    for file, session, age in sorted(claims, key=lambda x: x[2]):
        print(f"  {session:20s} {age:4d}s  {file}")
    return 0


def cmd_gc() -> int:
    if not CLAIMS_DIR.exists():
        return 0
    removed = 0
    for p in CLAIMS_DIR.glob("*.claim.json"):
        if read_claim(p) is None:
            p.unlink(missing_ok=True)
            removed += 1
    print(f"GC: removed {removed} expired claims")
    return 0


def cmd_next_lesson(session: str) -> int:
    """Atomically claim the next available L-NNN lesson slot (CE-4 fix, F-CON2).

    Scans existing lessons + active claims to find the highest slot in use, then
    claims max+1. Prints the claimed path so callers can use it directly.

    Returns 0 on success, 1 if claim failed (race with another session).
    """
    import re
    LESSONS_DIR = Path("memory/lessons")
    CLAIMS_DIR.mkdir(parents=True, exist_ok=True)

    # Find max existing lesson number
    max_existing = 0
    if LESSONS_DIR.exists():
        for p in LESSONS_DIR.glob("L-*.md"):
            m = re.match(r"L-(\d+)\.md$", p.name)
            if m:
                max_existing = max(max_existing, int(m.group(1)))

    # Find max claimed lesson slot (active claims only)
    max_claimed = max_existing
    for p in CLAIMS_DIR.glob("*.claim.json"):
        data = read_claim(p)
        if data and data.get("slot_type") == "lesson":
            m = re.match(r"L-(\d+)\.md$", Path(data["file"]).name)
            if m:
                max_claimed = max(max_claimed, int(m.group(1)))

    # Claim the next slot
    next_num = max_claimed + 1
    slot_path = f"memory/lessons/L-{next_num}.md"
    claim_file = claim_path(slot_path)

    existing = read_claim(claim_file)
    if existing and existing.get("session") != session:
        age = (datetime.now(timezone.utc) - datetime.fromisoformat(existing["timestamp"])).total_seconds()
        print(f"SLOT_CONFLICT: L-{next_num} already claimed by {existing['session']} ({int(age)}s ago)", file=sys.stderr)
        # Try next slot
        next_num += 1
        slot_path = f"memory/lessons/L-{next_num}.md"
        claim_file = claim_path(slot_path)

    data = {
        "file": slot_path,
        "session": session,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "slot_type": "lesson",
    }
    claim_file.write_text(json.dumps(data, indent=2))
    print(slot_path)
    return 0


def main():
    parser = argparse.ArgumentParser(description="Soft-claim protocol for concurrent session coordination (L-557, F-CON2)")
    parser.add_argument("command", choices=["claim", "check", "release", "list", "gc", "next-lesson"])
    parser.add_argument("file", nargs="?", help="File to claim/check/release")
    parser.add_argument("--session", default=None, help="Session ID (defaults to SWARM_SESSION_ID env or PID)")
    args = parser.parse_args()

    session = args.session or get_session_id()

    if args.command in ("claim", "check", "release") and not args.file:
        parser.error(f"'{args.command}' requires a file argument")

    if args.command == "claim":
        return cmd_claim(args.file, session)
    elif args.command == "check":
        return cmd_check(args.file)
    elif args.command == "release":
        return cmd_release(args.file, session)
    elif args.command == "list":
        return cmd_list()
    elif args.command == "gc":
        return cmd_gc()
    elif args.command == "next-lesson":
        return cmd_next_lesson(session)


if __name__ == "__main__":
    sys.exit(main())
