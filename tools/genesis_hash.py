#!/usr/bin/env python3
"""
genesis_hash.py — Compute and optionally write the genesis bundle hash.

The genesis bundle hash guards against replay attacks (FM-11, L-720).
Uses the SAME file set as tools/check.sh genesis_check():
  - workspace/genesis.sh
  - beliefs/CORE.md
  - memory/PRINCIPLES.md (or beliefs/PRINCIPLES.md if present)

Usage:
    python3 tools/genesis_hash.py           # print current hash
    python3 tools/genesis_hash.py --write   # compute and write workspace/genesis-bundle-SXXX.hash
    python3 tools/genesis_hash.py --check   # exit 0 if matches latest hash file, else exit 1
"""

import argparse
import hashlib
import re
import sys
from pathlib import Path

try:
    from swarm_io import session_number
except ImportError:
    def session_number() -> int:
        return 0

ROOT = Path(__file__).resolve().parent.parent
GENESIS_FILES_ORDER = [
    ROOT / "workspace" / "genesis.sh",
    ROOT / "beliefs" / "CORE.md",
]
PRINCIPLES_CANDIDATES = [ROOT / "beliefs" / "PRINCIPLES.md", ROOT / "memory" / "PRINCIPLES.md"]
CANONICAL_HASH_RE = re.compile(r"genesis-bundle-S\d+[A-Za-z0-9-]*\.hash$")


def compute_hash() -> str:
    files = []
    for f in GENESIS_FILES_ORDER:
        if f.exists():
            files.append(f)
    for candidate in PRINCIPLES_CANDIDATES:
        if candidate.exists():
            files.append(candidate)
            break
    h = hashlib.sha256()
    for f in files:
        h.update(f.read_bytes())
    return h.hexdigest()


def latest_hash_file():
    files = sorted((ROOT / "workspace").glob("genesis-bundle-*.hash"), key=lambda f: f.stat().st_mtime)
    if not files:
        return None
    canonical = [f for f in files if CANONICAL_HASH_RE.fullmatch(f.name)]
    pool = canonical or files
    return pool[-1]


def default_session_label() -> str:
    sess = session_number()
    return f"S{sess}" if sess > 0 else "S0"


def main():
    default_session = default_session_label()
    parser = argparse.ArgumentParser(description="Genesis bundle hash tool")
    parser.add_argument("--write", action="store_true", help="Write hash to workspace/genesis-bundle-SXXX.hash")
    parser.add_argument("--session", default=default_session, help=f"Session label for hash filename (default: {default_session})")
    parser.add_argument("--check", action="store_true", help="Exit 0 if hash matches, 1 if mismatch")
    args = parser.parse_args()

    current = compute_hash()

    if args.check:
        hf = latest_hash_file()
        if hf is None:
            print("genesis_hash: no hash file found — SKIP")
            sys.exit(0)
        stored = hf.read_text().strip()
        if current == stored:
            print(f"genesis_hash: PASS ({current[:12]}...)")
            sys.exit(0)
        else:
            print(f"genesis_hash: FAIL (current {current[:12]}... != stored {stored[:12]}...)")
            sys.exit(1)

    if args.write:
        out = ROOT / "workspace" / f"genesis-bundle-{args.session}.hash"
        out.write_text(current + "\n")
        print(f"Written: {out.relative_to(ROOT)} ({current[:12]}...)")
    else:
        print(current)


if __name__ == "__main__":
    main()
