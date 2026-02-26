#!/usr/bin/env python3
"""claim.py — Frontier task claiming to prevent duplicate work.
Usage: python3 tools/claim.py {claim <id> <session> | release <id> | status | resolve <id> "summary"}
"""
import json, sys
from datetime import datetime, timezone
from pathlib import Path

CLAIMS = Path(__file__).resolve().parent.parent / "tasks" / "claims.json"
now = lambda: datetime.now(timezone.utc).isoformat()

def load():
    return json.loads(CLAIMS.read_text()) if CLAIMS.exists() else {}

def save(data):
    CLAIMS.write_text(json.dumps(data, indent=2) + "\n")

def claim(fid, session):
    c = load()
    if fid in c and c[fid]["status"] == "claimed":
        print(f"REFUSED: {fid} already claimed by {c[fid]['claimed_by']} at {c[fid]['timestamp']}")
        sys.exit(1)
    c[fid] = {"claimed_by": session, "timestamp": now(), "status": "claimed"}
    save(c)
    print(f"CLAIMED: {fid} by {session}")

def release(fid):
    c = load()
    if fid not in c or c[fid]["status"] != "claimed":
        print(f"Nothing to release: {fid} is not currently claimed"); return
    c[fid]["status"] = "released"
    save(c)
    print(f"RELEASED: {fid}")

def status():
    c = load()
    if not c: print("No claims recorded."); return
    active   = {k: v for k, v in c.items() if v["status"] == "claimed"}
    resolved = {k: v for k, v in c.items() if v["status"] == "resolved"}
    released = {k: v for k, v in c.items() if v["status"] == "released"}
    if active:
        print("ACTIVE CLAIMS:")
        for fid, v in sorted(active.items()):
            print(f"  {fid}: {v['claimed_by']} (since {v['timestamp']})")
    if resolved:
        print("RESOLVED:")
        for fid, v in sorted(resolved.items()):
            print(f"  {fid}: {v.get('resolution', '-')}")
    if released:
        print(f"RELEASED: {', '.join(sorted(released.keys()))}")

def resolve(fid, summary):
    c = load()
    c[fid] = {**c.get(fid, {}), "status": "resolved", "resolution": summary, "resolved_at": now()}
    save(c)
    print(f"RESOLVED: {fid} -- {summary}")

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:                                      print(__doc__.strip()); sys.exit(1)
    elif args[0] == "claim"   and len(args) == 3:     claim(args[1], args[2])
    elif args[0] == "release" and len(args) == 2:     release(args[1])
    elif args[0] == "status":                         status()
    elif args[0] == "resolve" and len(args) == 3:     resolve(args[1], args[2])
    else:                                             print(__doc__.strip()); sys.exit(1)
