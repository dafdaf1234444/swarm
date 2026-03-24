#!/usr/bin/env python3
"""safe_commit.py — Concurrent-safe git commit using isolated index.

Builds a tree from HEAD + specified files using GIT_INDEX_FILE=/tmp/...,
then creates commit via plumbing (commit-tree + update-ref). Immune to
concurrent sessions corrupting .git/index.

Usage:
    python3 tools/safe_commit.py -m "[S529] what: why" file1 file2 ...
    python3 tools/safe_commit.py -m "msg" --deleted old_file -- new_file1
"""

import argparse, fcntl, os, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT, **kw)
    if r.returncode != 0:
        print(f"FAIL: {' '.join(cmd)}\n{r.stderr}", file=sys.stderr)
        sys.exit(1)
    return r.stdout.strip()


def main():
    ap = argparse.ArgumentParser(description="Concurrent-safe commit")
    ap.add_argument("-m", "--message", required=True, help="Commit message")
    ap.add_argument("files", nargs="+", help="Files to add (use --deleted for removals)")
    ap.add_argument("--deleted", nargs="*", default=[], help="Files to remove from tree")
    ap.add_argument("--parent", default=None, help="Parent ref (default: HEAD)")
    args = ap.parse_args()

    idx = tempfile.mktemp(prefix="swarm-safe-commit-")
    env = {**os.environ, "GIT_INDEX_FILE": idx}

    try:
        # Serialize entire commit with flock to prevent stale-parent race (L-1541)
        lock_path = "/tmp/swarm-git.lock"
        with open(lock_path, "w") as lock_fh:
            fcntl.flock(lock_fh, fcntl.LOCK_EX)

            # Read HEAD inside lock to avoid stale-parent race
            parent = args.parent or run(["git", "rev-parse", "HEAD"])

            # Re-build tree from fresh parent
            run(["git", "read-tree", parent], env=env)
            for f in args.files:
                if not Path(ROOT / f).exists():
                    continue
                run(["git", "update-index", "--add", f], env=env)
            for f in args.deleted:
                run(["git", "update-index", "--force-remove", f], env=env)
            tree = run(["git", "write-tree"], env=env)

            # Verify tree integrity
            claude_ck = subprocess.run(
                ["git", "ls-tree", tree, "--", "CLAUDE.md"],
                capture_output=True, text=True, cwd=ROOT
            )
            if "CLAUDE.md" not in claude_ck.stdout:
                print("ABORT: tree missing CLAUDE.md — index corruption", file=sys.stderr)
                sys.exit(1)

            # Create commit
            r = subprocess.run(
                ["git", "commit-tree", tree, "-p", parent],
                input=args.message, capture_output=True, text=True, cwd=ROOT
            )
            if r.returncode != 0:
                print(f"commit-tree failed: {r.stderr}", file=sys.stderr)
                sys.exit(1)
            commit = r.stdout.strip()

            # Update ref with expected parent (atomic)
            upd = subprocess.run(
                ["git", "update-ref", "refs/heads/master", commit, parent],
                capture_output=True, text=True, cwd=ROOT
            )
            if upd.returncode != 0:
                print(f"update-ref race: parent changed during commit. Retry.", file=sys.stderr)
                sys.exit(1)

            # Rebuild main index from new HEAD
            idx_lock = ROOT / ".git" / "index.lock"
            idx_lock.unlink(missing_ok=True)
            main_idx = ROOT / ".git" / "index"
            main_idx.unlink(missing_ok=True)
            subprocess.run(["git", "read-tree", "HEAD"], cwd=ROOT,
                            capture_output=True)

        print(f"{commit[:8]} {args.message.splitlines()[0]}")

    finally:
        Path(idx).unlink(missing_ok=True)


if __name__ == "__main__":
    main()
