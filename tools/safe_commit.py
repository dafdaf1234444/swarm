#!/usr/bin/env python3
"""safe_commit.py — Concurrent-safe git commit using isolated index.

Builds a tree from HEAD + specified files using GIT_INDEX_FILE=/tmp/...,
then creates commit via plumbing (commit-tree + update-ref). Immune to
concurrent sessions corrupting .git/index.

Usage:
    python3 tools/safe_commit.py -m "[S529] what: why" file1 file2 ...
    python3 tools/safe_commit.py -m "msg" --deleted old_file -- new_file1
"""

import argparse, fcntl, os, shutil, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT, **kw)
    if r.returncode != 0:
        print(f"FAIL: {' '.join(cmd)}\n{r.stderr}", file=sys.stderr)
        sys.exit(1)
    return r.stdout.strip()


def index_env(index_path: str) -> dict[str, str]:
    return {**os.environ, "GIT_INDEX_FILE": index_path}


def run_validation(index_path: str) -> None:
    """Run the standard quick validation suite against an isolated index."""
    check_sh = ROOT / "tools" / "check.sh"
    check_ps1 = ROOT / "tools" / "check.ps1"
    if shutil.which("bash") and check_sh.exists():
        run(
            ["bash", "tools/check.sh", "--quick", "--index-file", index_path],
            env=index_env(index_path),
        )
        return
    if shutil.which("pwsh") and check_ps1.exists():
        run(
            ["pwsh", "-NoProfile", "-File", "tools/check.ps1", "--quick", "--index-file", index_path],
            env=index_env(index_path),
        )
        return
    print("FAIL: no check.sh/check.ps1 runtime available; use --no-verify to bypass.", file=sys.stderr)
    sys.exit(1)


def rebuild_main_index() -> None:
    """Best-effort index sync without exposing a zero-byte main index window."""
    git_dir = ROOT / ".git"
    lock_path = git_dir / "index.lock"
    if lock_path.exists():
        print("NOTICE: skipped main-index refresh because .git/index.lock exists.", file=sys.stderr)
        return

    fd, temp_path = tempfile.mkstemp(prefix="index.safe-commit-", dir=git_dir)
    os.close(fd)
    temp_index = Path(temp_path)
    try:
        run(["git", "read-tree", "HEAD"], env=index_env(str(temp_index)))
        os.replace(temp_index, git_dir / "index")
    finally:
        temp_index.unlink(missing_ok=True)


def main():
    ap = argparse.ArgumentParser(description="Concurrent-safe commit")
    ap.add_argument("-m", "--message", required=True, help="Commit message")
    ap.add_argument("--no-verify", action="store_true",
                    help="Skip tools/check.sh --quick on the isolated index")
    ap.add_argument("files", nargs="+", help="Files to add (use --deleted for removals)")
    ap.add_argument("--deleted", nargs="*", default=[], help="Files to remove from tree")
    ap.add_argument("--parent", default=None, help="Parent ref (default: HEAD)")
    args = ap.parse_args()

    fd, idx = tempfile.mkstemp(prefix="swarm-safe-commit-")
    os.close(fd)
    env = index_env(idx)

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

            if not args.no_verify:
                run_validation(idx)
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

            # Rebuild the shared index only via atomic replacement.
            rebuild_main_index()

        print(f"{commit[:8]} {args.message.splitlines()[0]}")

    finally:
        Path(idx).unlink(missing_ok=True)


if __name__ == "__main__":
    main()
