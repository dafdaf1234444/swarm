#!/usr/bin/env python3
"""
frontier_claim.py — Task claiming for frontier questions.

Usage:
    python3 tools/frontier_claim.py claim <F-id> <session-id>
    python3 tools/frontier_claim.py release <F-id>
    python3 tools/frontier_claim.py resolve <F-id>
    python3 tools/frontier_claim.py status

Prevents two sessions from unknowingly working on the same question.
Protocol: claim → commit → push. Push failure = someone else got it.
"""

import json
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CLAIMS_FILE = REPO_ROOT / "experiments" / "frontier-claims.json"


def _load() -> dict:
    if CLAIMS_FILE.exists():
        return json.loads(CLAIMS_FILE.read_text())
    return {}


def _save(data: dict):
    CLAIMS_FILE.parent.mkdir(parents=True, exist_ok=True)
    CLAIMS_FILE.write_text(json.dumps(data, indent=2, sort_keys=True))


def claim(fid: str, session: str):
    """Claim a frontier question. Fails if already claimed."""
    data = _load()
    existing = data.get(fid, {})
    if existing.get("status") == "claimed":
        print(f"CONFLICT: {fid} already claimed by {existing['session']} at {existing['timestamp']}")
        print("Pick another question or wait for release.")
        sys.exit(1)
    data[fid] = {
        "status": "claimed",
        "session": session,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
    }
    _save(data)
    print(f"{fid} claimed by {session}")
    print("Now: git add + commit + push. Push failure = someone else got it.")


def release(fid: str):
    """Release a claim (abandoned work)."""
    data = _load()
    if fid not in data or data[fid].get("status") != "claimed":
        print(f"{fid} is not currently claimed.")
        return
    data[fid]["status"] = "released"
    data[fid]["released_at"] = datetime.now().isoformat(timespec="seconds")
    _save(data)
    print(f"{fid} released.")


def resolve(fid: str):
    """Mark a claimed question as resolved."""
    data = _load()
    if fid in data:
        data[fid]["status"] = "resolved"
        data[fid]["resolved_at"] = datetime.now().isoformat(timespec="seconds")
    else:
        data[fid] = {
            "status": "resolved",
            "resolved_at": datetime.now().isoformat(timespec="seconds"),
        }
    _save(data)
    print(f"{fid} marked resolved.")


def status():
    """Show all claims."""
    data = _load()
    if not data:
        print("No claims.")
        return
    print(f"{'ID':<8} {'Status':<10} {'Session':<12} {'Since'}")
    print("-" * 50)
    for fid in sorted(data.keys(), key=lambda x: int(x[1:])):
        info = data[fid]
        ts = info.get("timestamp", info.get("resolved_at", "?"))
        print(f"{fid:<8} {info['status']:<10} {info.get('session', '-'):<12} {ts}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "claim":
        if len(sys.argv) < 4:
            print("Usage: frontier_claim.py claim <F-id> <session-id>")
            sys.exit(1)
        claim(sys.argv[2], sys.argv[3])
    elif cmd == "release":
        if len(sys.argv) < 3:
            print("Usage: frontier_claim.py release <F-id>")
            sys.exit(1)
        release(sys.argv[2])
    elif cmd == "resolve":
        if len(sys.argv) < 3:
            print("Usage: frontier_claim.py resolve <F-id>")
            sys.exit(1)
        resolve(sys.argv[2])
    elif cmd == "status":
        status()
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
