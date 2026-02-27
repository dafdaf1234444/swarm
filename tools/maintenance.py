#!/usr/bin/env python3
"""
maintenance.py — What needs doing right now.

Usage:
    python3 tools/maintenance.py          # show all due maintenance
    python3 tools/maintenance.py --quick  # skip slow checks (git remote)

The swarm runs this at session start. It reads state and surfaces conditions —
not a checklist. The swarm decides what matters most.

Categories:
  URGENT   — do this before other work
  DUE      — threshold crossed, handle this session
  PERIODIC — cadence-based, check if it's time
  NOTICE   — informational, act if relevant
"""

import json
import os
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def _git(*args: str) -> str:
    try:
        r = subprocess.run(
            ["git", "-C", str(REPO_ROOT)] + list(args),
            capture_output=True, text=True, timeout=10
        )
        return r.stdout.strip()
    except Exception:
        return ""


def _line_count(path: Path) -> int:
    try:
        return len(path.read_text().splitlines())
    except Exception:
        return 0


def _read(path: Path) -> str:
    try:
        return path.read_text()
    except Exception:
        return ""


def _session_number() -> int:
    """Extract current session number from SESSION-LOG.md."""
    log = _read(REPO_ROOT / "memory" / "SESSION-LOG.md")
    numbers = re.findall(r"^S(\d+)", log, re.MULTILINE)
    return max(int(n) for n in numbers) if numbers else 0


# --- Check functions ---
# Each returns a list of (priority, message) tuples.
# Priority: URGENT > DUE > PERIODIC > NOTICE


def check_unpushed() -> list[tuple[str, str]]:
    """Check for unpushed commits."""
    results = []
    ahead = _git("rev-list", "--count", "@{upstream}..HEAD")
    if ahead and ahead.isdigit() and int(ahead) > 0:
        n = int(ahead)
        level = "URGENT" if n >= 10 else "DUE" if n >= 5 else "NOTICE"
        results.append((level, f"{n} unpushed commits — git push"))
    return results


def check_uncommitted() -> list[tuple[str, str]]:
    """Check for uncommitted changes."""
    results = []
    status = _git("status", "--porcelain")
    if status:
        lines = [l for l in status.splitlines() if l.strip()]
        modified = [l for l in lines if l.startswith(" M") or l.startswith("M ")]
        untracked = [l for l in lines if l.startswith("??")]
        if modified:
            results.append(("NOTICE", f"{len(modified)} modified file(s) uncommitted"))
        if untracked:
            results.append(("NOTICE", f"{len(untracked)} untracked file(s)"))
    return results


def check_open_challenges() -> list[tuple[str, str]]:
    """Check for open challenges in CHALLENGES.md and PHILOSOPHY.md."""
    results = []

    # CHALLENGES.md (B-ID and P-NNN challenges)
    challenges_text = _read(REPO_ROOT / "beliefs" / "CHALLENGES.md")
    open_challenges = re.findall(r"\|\s*OPEN\s*\|", challenges_text, re.IGNORECASE)
    if open_challenges:
        results.append(("DUE", f"{len(open_challenges)} open challenge(s) in CHALLENGES.md — can you resolve any?"))

    # PHILOSOPHY.md challenges
    phil_text = _read(REPO_ROOT / "beliefs" / "PHILOSOPHY.md")
    phil_section = phil_text[phil_text.find("## Challenges"):] if "## Challenges" in phil_text else ""
    open_phil = re.findall(r"\|\s*open\s*\|", phil_section, re.IGNORECASE)
    if open_phil:
        results.append(("DUE", f"{len(open_phil)} open PHIL challenge(s) in PHILOSOPHY.md"))

    return results


def check_human_queue() -> list[tuple[str, str]]:
    """Check for unanswered human queue items."""
    results = []
    hq_text = _read(REPO_ROOT / "tasks" / "HUMAN-QUEUE.md")
    if not hq_text:
        return results

    # Find items NOT in the Answered section and NOT struck through
    answered_pos = hq_text.find("## Answered")
    open_section = hq_text[:answered_pos] if answered_pos > 0 else hq_text
    open_items = re.findall(r"^### (?!~~)HQ-\d+", open_section, re.MULTILINE)
    if open_items:
        results.append(("NOTICE", f"{len(open_items)} unanswered item(s) in HUMAN-QUEUE.md"))

    return results


def check_child_bulletins() -> list[tuple[str, str]]:
    """Check for unprocessed child bulletins."""
    results = []
    bulletin_dir = REPO_ROOT / "experiments" / "inter-swarm" / "bulletins"
    if bulletin_dir.exists():
        bulletins = list(bulletin_dir.glob("*.md"))
        if bulletins:
            results.append(("DUE", f"{len(bulletins)} child bulletin(s) — propagate_challenges.py / harvest"))

    return results


def check_compaction() -> list[tuple[str, str]]:
    """Check compaction thresholds from OPERATIONS.md."""
    results = []

    # INDEX.md > 60 lines
    index_lines = _line_count(REPO_ROOT / "memory" / "INDEX.md")
    if index_lines > 60:
        results.append(("DUE", f"INDEX.md is {index_lines} lines (threshold: 60) — compaction needed"))

    # Mandatory load > 200 lines
    mandatory = sum(_line_count(REPO_ROOT / p) for p in [
        Path("CLAUDE.md"),
        Path("beliefs") / "CORE.md",
        Path("memory") / "INDEX.md",
    ])
    if mandatory > 200:
        results.append(("DUE", f"Mandatory load is {mandatory} lines (threshold: 200) — compaction needed"))

    return results


def check_lessons() -> list[tuple[str, str]]:
    """Check lesson health: count and length."""
    results = []
    lessons_dir = REPO_ROOT / "memory" / "lessons"
    if not lessons_dir.exists():
        return results

    lessons = list(lessons_dir.glob("L-*.md"))

    # Lessons over 20 lines
    over_20 = []
    for f in lessons:
        if _line_count(f) > 20:
            over_20.append(f.name)
    if over_20:
        results.append(("DUE", f"{len(over_20)} lesson(s) over 20 lines: {', '.join(over_20[:5])}"))

    return results


def check_frontier_decay() -> list[tuple[str, str]]:
    """Check for decayed frontier questions."""
    results = []
    decay_file = REPO_ROOT / "experiments" / "frontier-decay.json"
    frontier_path = REPO_ROOT / "tasks" / "FRONTIER.md"

    if not frontier_path.exists():
        return results

    text = frontier_path.read_text()
    archive_pos = text.find("## Archive")
    open_text = text[:archive_pos] if archive_pos > 0 else text

    decay = {}
    if decay_file.exists():
        try:
            decay = json.loads(decay_file.read_text())
        except Exception:
            pass

    today = date.today().isoformat()
    weak = []
    archive_candidates = []

    for m in re.finditer(r"^- \*\*F(\d+)\*\*:", open_text, re.MULTILINE):
        fid = f"F{m.group(1)}"
        last_active = decay.get(fid, {}).get("last_active", today)
        days = (date.fromisoformat(today) - date.fromisoformat(last_active)).days
        strength = 0.9 ** days
        if strength < 0.1:
            archive_candidates.append(fid)
        elif strength < 0.3:
            weak.append(fid)

    if archive_candidates:
        results.append(("DUE", f"{len(archive_candidates)} frontier question(s) below archive threshold: {', '.join(archive_candidates)}"))
    if weak:
        results.append(("NOTICE", f"{len(weak)} frontier question(s) weakening: {', '.join(weak)}"))

    return results


def check_health_due() -> list[tuple[str, str]]:
    """Check if periodic health check is due (every ~5 sessions)."""
    results = []
    session = _session_number()
    if session > 0 and session % 5 == 0:
        results.append(("PERIODIC", f"Session {session} — health check due (every ~5 sessions). See memory/HEALTH.md"))
    return results


def check_tool_consolidation() -> list[tuple[str, str]]:
    """Check if tool consolidation is due (every ~25 sessions)."""
    results = []
    session = _session_number()
    if session > 0 and session % 25 == 0:
        results.append(("PERIODIC", f"Session {session} — tool consolidation due (every ~25 sessions). Audit tools/ for duplicates and dead code."))
    return results


def check_validator() -> list[tuple[str, str]]:
    """Quick check if validator passes."""
    results = []
    try:
        r = subprocess.run(
            ["python3", str(REPO_ROOT / "tools" / "validate_beliefs.py"), "--quick"],
            capture_output=True, text=True, timeout=30
        )
        if "RESULT: FAIL" in r.stdout:
            results.append(("URGENT", "validate_beliefs.py FAIL — fix before other work"))
        # Extract swarmability if present
        m = re.search(r"SWARMABILITY: (\d+)/100", r.stdout)
        if m:
            score = int(m.group(1))
            if score < 80:
                results.append(("DUE", f"Swarmability {score}/100 — below 80, investigate"))
    except Exception as e:
        results.append(("URGENT", f"validate_beliefs.py failed to run: {e}"))
    return results


def check_version_drift() -> list[tuple[str, str]]:
    """Check if .swarm_meta.json versions match current files."""
    results = []
    meta_path = REPO_ROOT / ".swarm_meta.json"
    if not meta_path.exists():
        return results

    try:
        meta = json.loads(meta_path.read_text())
    except Exception:
        return results

    claude_md = _read(REPO_ROOT / "CLAUDE.md")
    core_md = _read(REPO_ROOT / "beliefs" / "CORE.md")

    claude_ver = re.search(r"claude_md_version:\s*([\d.]+)", claude_md)
    core_ver = re.search(r"core_md_version:\s*([\d.]+)", core_md)

    if claude_ver and meta.get("claude_md_version"):
        if str(claude_ver.group(1)) != str(meta["claude_md_version"]):
            results.append(("URGENT", f"CLAUDE.md version {claude_ver.group(1)} != meta {meta['claude_md_version']} — re-read CLAUDE.md"))

    if core_ver and meta.get("core_md_version"):
        if str(core_ver.group(1)) != str(meta["core_md_version"]):
            results.append(("URGENT", f"CORE.md version {core_ver.group(1)} != meta {meta['core_md_version']} — re-read CORE.md"))

    return results


def check_resolution_claims() -> list[tuple[str, str]]:
    """Check for stale resolution claims."""
    results = []
    claims_path = REPO_ROOT / "tasks" / "RESOLUTION-CLAIMS.md"
    if not claims_path.exists():
        return results

    text = claims_path.read_text()
    claimed = re.findall(r"CLAIMED", text)
    resolved = re.findall(r"RESOLVED", text)
    stale = len(claimed) - len(resolved)
    if stale > 0:
        results.append(("NOTICE", f"{stale} frontier question(s) CLAIMED but not RESOLVED"))

    return results


# --- Main ---

PRIORITY_ORDER = {"URGENT": 0, "DUE": 1, "PERIODIC": 2, "NOTICE": 3}
PRIORITY_SYMBOLS = {"URGENT": "!!!", "DUE": " ! ", "PERIODIC": " ~ ", "NOTICE": " . "}


def main():
    quick = "--quick" in sys.argv

    all_checks = [
        check_validator,
        check_version_drift,
        check_open_challenges,
        check_compaction,
        check_lessons,
        check_child_bulletins,
        check_frontier_decay,
        check_health_due,
        check_tool_consolidation,
        check_human_queue,
        check_uncommitted,
        check_resolution_claims,
    ]

    if not quick:
        all_checks.append(check_unpushed)

    items: list[tuple[str, str]] = []
    for check_fn in all_checks:
        try:
            items.extend(check_fn())
        except Exception as e:
            items.append(("NOTICE", f"{check_fn.__name__} error: {e}"))

    # Sort by priority
    items.sort(key=lambda x: PRIORITY_ORDER.get(x[0], 99))

    print("=== MAINTENANCE ===")
    print()

    if not items:
        print("  Nothing due. All clear.")
    else:
        current_priority = None
        for priority, msg in items:
            if priority != current_priority:
                current_priority = priority
                print(f"  [{priority}]")
            symbol = PRIORITY_SYMBOLS.get(priority, "   ")
            print(f"  {symbol} {msg}")
        print()
        counts = {}
        for p, _ in items:
            counts[p] = counts.get(p, 0) + 1
        summary = " | ".join(f"{p}: {c}" for p, c in sorted(counts.items(), key=lambda x: PRIORITY_ORDER.get(x[0], 99)))
        print(f"  {summary}")

    print()


if __name__ == "__main__":
    main()
