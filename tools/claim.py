#!/usr/bin/env python3
"""tools/claim.py — Soft-claim protocol for concurrent session coordination

Prevents C-EDIT DUE-convergence collisions (L-557, F-CON2). Sessions declare
intent before editing shared files; check/release prevents duplicate work.

Usage:
  python3 tools/claim.py claim <file> [--session <id>]   # Claim a file
  python3 tools/claim.py check <file>                     # Check if claimed (exit 0=free, 1=claimed)
  python3 tools/claim.py release <file> [--session <id>] # Release claim
  python3 tools/claim.py list                             # List active claims
  python3 tools/claim.py gc                               # Garbage collect expired claims
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

CLAIMS_DIR = Path("workspace/claims")
CLAIM_TTL_SECONDS = 300  # 5 minutes — sessions that crash leave auto-expiring claims


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


def main():
    parser = argparse.ArgumentParser(description="Soft-claim protocol for concurrent session coordination (L-557, F-CON2)")
    parser.add_argument("command", choices=["claim", "check", "release", "list", "gc"])
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


if __name__ == "__main__":
    sys.exit(main())
