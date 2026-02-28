#!/usr/bin/env python3
"""
f_con3_constitution_monitor.py — F-CON3 immune-response detection for constitutional mutation (A1).

Design: hash constitutional files at session start (--save), rehash at session end (--check).
If any monitored file changed between save and check, emit a WARNING and optionally call bulletin.py.

Usage:
    python3 tools/f_con3_constitution_monitor.py --save [--session SESSION]
    python3 tools/f_con3_constitution_monitor.py --check [--session SESSION] [--bulletin]
    python3 tools/f_con3_constitution_monitor.py --list

Exit codes:
    0 = no changes detected
    1 = changes detected (A1 constitutional mutation alert)
    2 = no checkpoint exists (--check without prior --save)

Monitored files (constitutional):
    CLAUDE.md            — swarm bridge + protocol
    beliefs/CORE.md      — operating principles, belief update protocol
    beliefs/PHILOSOPHY.md — primary goals, PHIL-N axioms

Checkpoint: experiments/conflict/f-con3-checkpoint.json (session-ephemeral, not committed)
Artifact:   experiments/conflict/f-con3-check-s<SESSION>.json

Related: F110-A1, F-CON3, tools/validate_beliefs.py (A2 semantic drift coverage)
"""

import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

MONITORED_FILES = [
    "CLAUDE.md",
    "beliefs/CORE.md",
    "beliefs/PHILOSOPHY.md",
]

CHECKPOINT_PATH = REPO_ROOT / "experiments" / "conflict" / "f-con3-checkpoint.json"
ARTIFACT_DIR = REPO_ROOT / "experiments" / "conflict"


def _sha256(path: Path) -> str:
    """Return hex SHA-256 of file contents, or 'MISSING' if file does not exist."""
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except FileNotFoundError:
        return "MISSING"
    except Exception as e:
        return f"ERROR:{e}"


def _hash_all() -> dict[str, str]:
    """Hash all monitored files and return {rel_path: hex_digest}."""
    result = {}
    for rel in MONITORED_FILES:
        abs_path = REPO_ROOT / rel
        result[rel] = _sha256(abs_path)
    return result


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _git_rev() -> str:
    """Return short HEAD commit hash, or 'unknown'."""
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=str(REPO_ROOT),
            stderr=subprocess.DEVNULL,
        )
        return out.decode().strip()
    except Exception:
        return "unknown"


def cmd_save(session: str) -> int:
    """Save current constitutional hashes as checkpoint."""
    hashes = _hash_all()
    ts = _now_iso()
    rev = _git_rev()

    checkpoint = {
        "session": session,
        "saved_at": ts,
        "git_rev": rev,
        "hashes": hashes,
    }

    CHECKPOINT_PATH.parent.mkdir(parents=True, exist_ok=True)
    CHECKPOINT_PATH.write_text(json.dumps(checkpoint, indent=2), encoding="utf-8")

    print(f"[F-CON3] Checkpoint saved at {ts} (session={session}, rev={rev})")
    for rel, digest in hashes.items():
        print(f"  {digest[:16]}...  {rel}")
    print(f"Checkpoint: {CHECKPOINT_PATH}")
    return 0


def cmd_check(session: str, emit_bulletin: bool) -> int:
    """Compare current hashes to saved checkpoint. Returns 0=clean, 1=changed, 2=no-checkpoint."""
    if not CHECKPOINT_PATH.exists():
        print("[F-CON3] WARNING: No checkpoint found. Run --save at session start first.")
        return 2

    checkpoint = json.loads(CHECKPOINT_PATH.read_text(encoding="utf-8"))
    saved_hashes = checkpoint.get("hashes", {})
    saved_session = checkpoint.get("session", "unknown")
    saved_at = checkpoint.get("saved_at", "unknown")
    saved_rev = checkpoint.get("git_rev", "unknown")

    current_hashes = _hash_all()
    current_rev = _git_rev()
    ts = _now_iso()

    changes = []
    for rel in MONITORED_FILES:
        old = saved_hashes.get(rel, "MISSING")
        new = current_hashes.get(rel, "MISSING")
        if old != new:
            changes.append({
                "file": rel,
                "old_hash": old,
                "new_hash": new,
            })

    status = "CHANGE" if changes else "NO_CHANGE"

    # Build artifact
    artifact = {
        "session": session,
        "checked_at": ts,
        "checkpoint_session": saved_session,
        "checkpoint_at": saved_at,
        "git_rev_at_save": saved_rev,
        "git_rev_at_check": current_rev,
        "monitored_files": MONITORED_FILES,
        "hashes_at_save": saved_hashes,
        "hashes_at_check": current_hashes,
        "changes_detected": len(changes),
        "changes": changes,
        "hash_check_result": status,
        "detection_latency_model": "per-session (--save at start, --check at end)",
        "false_positive_risk": "low — hash comparison is exact; only structural changes trigger",
        "coverage": "A1 (constitutional mutation) — complements validate_beliefs.py (A2 semantic drift)",
        "verdict": "MUTATION_DETECTED" if changes else "CONSTITUTION_STABLE",
    }

    artifact_path = ARTIFACT_DIR / f"f-con3-check-{session.lower()}.json"
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    artifact_path.write_text(json.dumps(artifact, indent=2), encoding="utf-8")

    if changes:
        print(f"[F-CON3] WARNING: Constitutional mutation detected! {len(changes)} file(s) changed.")
        for ch in changes:
            print(f"  CHANGED: {ch['file']}")
            print(f"    was: {ch['old_hash'][:16]}...")
            print(f"    now: {ch['new_hash'][:16]}...")
        print()
        print("ALERT: A1 conflict detected — a concurrent session modified constitutional files.")
        print("Action: review git log for changes to the above files since session start.")
        print(f"Artifact: {artifact_path}")

        if emit_bulletin:
            files_str = ", ".join(ch["file"] for ch in changes)
            msg = (
                f"A1 constitutional mutation detected in session {session}. "
                f"Changed files: {files_str}. "
                f"Checkpoint from {saved_at} (rev {saved_rev}), "
                f"current rev {current_rev}. "
                f"Artifact: experiments/conflict/f-con3-check-{session.lower()}.json"
            )
            try:
                subprocess.run(
                    [
                        sys.executable,
                        str(REPO_ROOT / "tools" / "bulletin.py"),
                        "write",
                        session,
                        "warning",
                        msg,
                    ],
                    cwd=str(REPO_ROOT),
                    check=True,
                )
                print("[F-CON3] Bulletin emitted (type=warning).")
            except Exception as e:
                print(f"[F-CON3] Bulletin emission failed: {e}")

        return 1
    else:
        print(f"[F-CON3] Constitution stable. No changes detected since {saved_at}.")
        print(f"  Checkpoint session: {saved_session} (rev {saved_rev})")
        print(f"  Current rev: {current_rev}")
        print(f"Artifact: {artifact_path}")
        return 0


def cmd_list() -> int:
    """Show monitored files and their current hashes."""
    current_hashes = _hash_all()
    rev = _git_rev()
    ts = _now_iso()
    print(f"[F-CON3] Constitutional files monitor — {ts} (rev={rev})")
    print()
    print(f"{'File':<35} {'SHA-256 (first 32 chars)'}")
    print("-" * 75)
    for rel, digest in current_hashes.items():
        print(f"{rel:<35} {digest[:32]}...")

    if CHECKPOINT_PATH.exists():
        checkpoint = json.loads(CHECKPOINT_PATH.read_text(encoding="utf-8"))
        print()
        print(f"Checkpoint: {checkpoint.get('saved_at', '?')} session={checkpoint.get('session', '?')}")
        saved_hashes = checkpoint.get("hashes", {})
        changed = [r for r in MONITORED_FILES if saved_hashes.get(r) != current_hashes.get(r)]
        if changed:
            print(f"  CHANGED since checkpoint: {', '.join(changed)}")
        else:
            print("  No changes since checkpoint.")
    else:
        print()
        print("No checkpoint found. Run --save to establish baseline.")

    return 0


def main() -> int:
    args = sys.argv[1:]

    if not args or "--help" in args or "-h" in args:
        print(__doc__)
        return 0

    # Parse flags
    session = "S191"
    for i, a in enumerate(args):
        if a.startswith("--session="):
            session = a.split("=", 1)[1]
        elif a == "--session" and i + 1 < len(args):
            session = args[i + 1]

    emit_bulletin = "--bulletin" in args

    if "--save" in args:
        return cmd_save(session)
    elif "--check" in args:
        return cmd_check(session, emit_bulletin)
    elif "--list" in args:
        return cmd_list()
    else:
        print(f"Unknown arguments: {args}")
        print("Use --save, --check, or --list")
        return 1


if __name__ == "__main__":
    sys.exit(main())
