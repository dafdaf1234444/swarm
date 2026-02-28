#!/usr/bin/env python3
"""Shared I/O utilities for swarm tools.

Eliminates duplication of _read(), _git(), _session_number(), _token_count()
across 10+ tool files (L-476). Import from here instead of redefining.
"""

import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def read_text(path: Path) -> str:
    """Read file as UTF-8 with replace errors. Returns '' on any failure."""
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


def git_cmd(*args: str, timeout: int = 10) -> str:
    """Run git command in repo root, return stdout. Returns '' on failure."""
    try:
        return subprocess.run(
            ["git", "-C", str(REPO_ROOT)] + list(args),
            capture_output=True, text=True, timeout=timeout,
        ).stdout.rstrip("\n")
    except Exception:
        return ""


def git_cmd_strict(*args: str, timeout: int = 10) -> str:
    """Run git command in repo root, raise RuntimeError on failure."""
    r = subprocess.run(
        ["git", "-C", str(REPO_ROOT)] + list(args),
        capture_output=True, text=True, timeout=timeout,
    )
    if r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {r.stderr.strip()}")
    return r.stdout.rstrip("\n")


def session_number() -> int:
    """Best-effort current session number from SESSION-LOG + git log."""
    numbers = re.findall(
        r"^S(\d+)", read_text(REPO_ROOT / "memory" / "SESSION-LOG.md"), re.MULTILINE
    )
    log_max = max(int(n) for n in numbers) if numbers else 0
    try:
        git_out = subprocess.run(
            ["git", "log", "--oneline", "-50"],
            capture_output=True, text=True, cwd=REPO_ROOT, timeout=5,
        ).stdout
        git_max = max(
            (int(m) for m in re.findall(r"\[S(\d+)\]", git_out)), default=0
        )
    except Exception:
        git_max = 0
    return max(log_max, git_max)


def token_count(path: Path) -> int:
    """Estimate token count (chars / 4). Returns 0 on failure."""
    try:
        return len(read_text(path)) // 4
    except Exception:
        return 0


def line_count(path: Path) -> int:
    """Count lines in file. Returns 0 on failure."""
    try:
        return len(read_text(path).splitlines())
    except Exception:
        return 0
