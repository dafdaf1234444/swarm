#!/usr/bin/env python3
"""
orient.py — Single-command session orientation for swarm nodes.

Synthesizes maintenance status, NEXT.md priorities, FRONTIER.md open questions,
and INDEX.md state counts into a decision-ready snapshot.

Replaces the manual pattern of: read NEXT.md + INDEX.md + FRONTIER.md + run maintenance.py.

Usage:
    python3 tools/orient.py                         # full orientation
    python3 tools/orient.py --brief                 # compact one-screen summary
    python3 tools/orient.py --classify "build X"   # route a task to domain+personality
"""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORE_SWARM_TOOLS = (
    "tools/orient.py",
    "tools/maintenance.py",
    "tools/sync_state.py",
    "tools/validate_beliefs.py",
    "tools/check.sh",
    "tools/check.ps1",
    "tools/maintenance.sh",
    "tools/maintenance.ps1",
    "tools/compact.py",
    "tools/proxy_k.py",
    "tools/frontier_decay.py",
    "tools/swarm_pr.py",
    "tools/bulletin.py",
    "tools/merge_back.py",
    "tools/propagate_challenges.py",
    "tools/spawn_coordinator.py",
    "tools/colony.py",
    "tools/swarm_test.py",
    "tools/swarm_parse.py",
    "tools/change_quality.py",
    "tools/session_tracker.py",
    "tools/context_router.py",
    "tools/substrate_detect.py",
    "tools/kill_switch.py",
    "tools/task_recognizer.py",
)


def run_maintenance():
    """Run maintenance --quick and return stdout."""
    result = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "maintenance.py"), "--quick"],
        capture_output=True, text=True, cwd=ROOT
    )
    return result.stdout + result.stderr


def read_file(relpath):
    try:
        return (ROOT / relpath).read_text(encoding="utf-8")
    except Exception:
        return ""


def extract_state_line(index_text):
    """Extract session + counts from INDEX.md header."""
    session = "S?"
    m = re.search(r"Sessions:\s*(\d+)", index_text[:300])
    if m:
        session = f"S{m.group(1)}"
    counts = "?"
    m2 = re.search(r"(\d+)\s+lessons", index_text[:500])
    m3 = re.search(r"(\d+)\s+principles", index_text[:500])
    m4 = re.search(r"(\d+)\s+beliefs", index_text[:500])
    m5 = re.search(r"(\d+)\s+frontier", index_text[:500])
    parts = []
    if m2: parts.append(f"{m2.group(1)}L")
    if m3: parts.append(f"{m3.group(1)}P")
    if m4: parts.append(f"{m4.group(1)}B")
    if m5: parts.append(f"{m5.group(1)}F")
    counts = " ".join(parts) if parts else "?"
    return session, counts


def extract_next_priorities(next_text):
    """Extract numbered items from 'For next session' section."""
    m = re.search(r"## For next session\n(.*?)(?:\n##|\Z)", next_text, re.DOTALL)
    if not m:
        return []
    items = re.findall(r"^\d+\.\s+\*\*(.+?)\*\*", m.group(1), re.MULTILINE)
    if not items:
        items = re.findall(r"^\d+\.\s+(.+)$", m.group(1), re.MULTILINE)
    return [i[:100] for i in items[:6]]


def extract_key_state(next_text):
    """Extract key state lines (compact URGENT, counts, etc.)."""
    m = re.search(r"## Key state\n(.*?)(?:\n##|\Z)", next_text, re.DOTALL)
    if not m:
        return []
    lines = [l.strip("- ").strip() for l in m.group(1).splitlines()
             if l.strip().startswith("-")]
    return [l[:100] for l in lines[:4]]


def extract_critical_frontiers(frontier_text):
    """Extract Critical and Important frontier titles."""
    items = []
    for section in ("## Critical", "## Important"):
        m = re.search(rf"{re.escape(section)}\n(.*?)(?:\n##|\Z)", frontier_text, re.DOTALL)
        if not m:
            continue
        bullets = re.findall(r"^- \*\*(F\d+)\*\*:(.+)", m.group(1), re.MULTILINE)
        for fid, desc in bullets:
            first = desc.strip().split(".")[0][:80]
            items.append(f"{fid}: {first}")
    return items


def classify_maint(maint_out):
    """Return urgency level string from maintenance output."""
    if "URGENT" in maint_out:
        return "URGENT"
    if "[DUE]" in maint_out:
        return "DUE items present"
    if "[PERIODIC]" in maint_out:
        return "periodics due"
    return "NOTICE-only"


def extract_session_log_tail(log_text, n=10):
    """Return last N non-header session log lines (behavioral pattern signal)."""
    lines = [l for l in log_text.splitlines()
             if l.strip() and not l.startswith("#") and "|" in l]
    return lines[-n:]


def get_recent_commits(n=6):
    """Get recent commit summaries for collision-avoidance (L-251)."""
    result = subprocess.run(
        ["git", "log", "--oneline", f"-{n}"],
        capture_output=True, text=True, cwd=ROOT
    )
    if result.returncode != 0:
        return []
    commits = []
    for line in result.stdout.strip().splitlines():
        parts = line.split(" ", 1)
        if len(parts) == 2:
            commits.append(parts[1])
    return commits


def check_stale_experiments():
    """Scan domain frontier files for active (unrun) experiments. L-246."""
    domain_dir = ROOT / "domains"
    if not domain_dir.exists():
        return []
    stale = []
    for frontier_file in sorted(domain_dir.glob("*/tasks/FRONTIER.md")):
        domain = frontier_file.parent.parent.name
        text = frontier_file.read_text(encoding="utf-8")
        active_m = re.search(r"## Active\n(.*?)(?:\n## |\Z)", text, re.DOTALL)
        if not active_m:
            continue
        active_block = active_m.group(1)
        seen = set()
        for line in active_block.splitlines():
            # Canonical frontier entry forms:
            # - **F-XXX1**: ...
            # - F-XXX1: ...
            # | F-XXX1 | ... |
            bullet_bold = re.match(r"^\s*[-*]\s+(~~)?\*\*(F-[A-Z]+\d+)\*\*(?:~~)?", line)
            bullet_plain = re.match(r"^\s*[-*]\s+(~~)?(F-[A-Z]+\d+)(?:~~)?\b", line)
            table_row = re.match(r"^\s*\|\s*(~~)?(F-[A-Z]+\d+)(?:~~)?\s*\|", line)
            m = bullet_bold or bullet_plain or table_row
            if not m:
                continue
            is_struck = bool(m.group(1))
            eid = m.group(2)
            if is_struck or eid in seen:
                continue
            # Treat frontiers with session-tagged evidence/artifacts as already run.
            # This avoids false "unrun" flags for active items carrying S### updates.
            has_run_evidence = (
                re.search(r"\bS\d+\b", line) is not None
                or "experiments/" in line
                or re.search(r"\.json\b", line) is not None
            )
            if has_run_evidence:
                seen.add(eid)
                continue
            stale.append(f"{domain}/{eid}")
            seen.add(eid)
    return stale


def check_underused_core_tools(log_text, window_sessions=20):
    """Find core swarm tools not referenced in recent session-log entries."""
    rows = []
    for raw in log_text.splitlines():
        m = re.match(r"^S(\d+)\b", raw)
        if m:
            rows.append((int(m.group(1)), raw.lower().replace("\\", "/")))
    if not rows:
        return [], None, None

    latest_session = max(sid for sid, _ in rows)
    start_session = max(1, latest_session - window_sessions + 1)
    haystack = "\n".join(text for sid, text in rows if sid >= start_session)

    underused = []
    for tool in CORE_SWARM_TOOLS:
        normalized = tool.lower().replace("\\", "/")
        filename = Path(normalized).name
        pattern = rf"(?<![A-Za-z0-9_])(?:{re.escape(normalized)}|{re.escape(filename)})(?![A-Za-z0-9_])"
        if not re.search(pattern, haystack):
            underused.append(tool)
    return underused, latest_session, start_session


def _get_classify_task() -> str | None:
    """Extract --classify value from sys.argv, or None."""
    argv = sys.argv[1:]
    for i, arg in enumerate(argv):
        if arg == "--classify" and i + 1 < len(argv):
            return argv[i + 1]
        if arg.startswith("--classify="):
            return arg[len("--classify="):]
    return None


def _run_classify(task: str) -> None:
    """Route a task description to domain + personality via task_recognizer."""
    sys.path.insert(0, str(ROOT / "tools"))
    try:
        from task_recognizer import recognize  # type: ignore
    except ImportError:
        print("ERROR: tools/task_recognizer.py not found — cannot classify")
        return
    result = recognize(task)
    print(f"=== CLASSIFY: {task!r} ===")
    flag = "YES" if result["recognized"] else "NO"
    print(f"Recognized: {flag} | Confidence: {result['confidence']:.2f} | Personality: {result['personality']}")
    if result["routes"]:
        top = result["routes"][0]
        print(f"Primary domain: {top['domain']} (score {top['score']:.2f})")
        frontiers = top.get("open_frontiers", [])
        if frontiers:
            print(f"Open frontiers: {', '.join(frontiers[:3])}")
        if len(result["routes"]) > 1:
            alts = [f"{r['domain']}({r['score']:.2f})" for r in result["routes"][1:3]]
            print(f"Alternatives: {', '.join(alts)}")
    if result.get("new_domain_suggestion"):
        print(f"New domain suggestion: {result['new_domain_suggestion']}")


def main():
    brief = "--brief" in sys.argv

    classify_task = _get_classify_task()
    if classify_task:
        _run_classify(classify_task)
        return

    maint_out = run_maintenance()
    index_text = read_file("memory/INDEX.md")
    next_text = read_file("tasks/NEXT.md")
    frontier_text = read_file("tasks/FRONTIER.md")
    log_text = read_file("memory/SESSION-LOG.md")

    session, counts = extract_state_line(index_text)
    maint_level = classify_maint(maint_out)

    # Header
    print(f"=== ORIENT {session} | {counts} ===")
    print(f"Maintenance: {maint_level}")
    print()

    # Maintenance details (skip if NOTICE-only in brief mode)
    if not brief or maint_level != "NOTICE-only":
        signal_lines = [l for l in maint_out.splitlines()
                        if l.strip() and "===" not in l and "maintenance" not in l.lower()[:10]]
        if signal_lines:
            print("--- Maintenance ---")
            for line in signal_lines[:10]:
                print(f"  {line}")
            print()

    # Key state
    key_state = extract_key_state(next_text)
    if key_state:
        print("--- Key state ---")
        for s in key_state:
            print(f"  {s}")
        print()

    # Priorities
    priorities = extract_next_priorities(next_text)
    if priorities:
        print("--- Priorities ---")
        for i, p in enumerate(priorities, 1):
            print(f"  {i}. {p}")
        print()

    # Frontiers
    frontiers = extract_critical_frontiers(frontier_text)
    if frontiers:
        print("--- Open frontiers (critical/important) ---")
        for f in frontiers:
            print(f"  • {f}")
        print()

    # Stale domain experiments (L-246: design debt)
    stale_experiments = check_stale_experiments()
    if stale_experiments:
        print(f"--- Unrun domain experiments ({len(stale_experiments)}) ---")
        for e in stale_experiments[:6]:
            print(f"  ○ {e}")
        print()

    # Underused core tools (session-log execution signal)
    underused_tools, latest_sid, start_sid = check_underused_core_tools(log_text)
    if underused_tools:
        window = "recent sessions"
        if latest_sid is not None and start_sid is not None:
            window = f"S{start_sid}..S{latest_sid}"
        print(f"--- Underused core tools ({len(underused_tools)} in {window}) ---")
        for tool in underused_tools[:6]:
            print(f"  ○ {tool}")
        print()

    # Recent commits — collision-avoidance for concurrent nodes (L-251)
    recent_commits = get_recent_commits()
    if recent_commits:
        print("--- Recent commits (avoid repeating) ---")
        for c in recent_commits:
            print(f"  ✓ {c[:100]}")
        print()

    # Session log tail (full mode only — last 10 entries = behavioral signal)
    if not brief and log_text:
        tail = extract_session_log_tail(log_text)
        if tail:
            print("--- Recent sessions (behavioral pattern) ---")
            for entry in tail:
                print(f"  {entry[:120]}")
            print()

    # Suggested action
    print("--- Suggested next action ---")
    if "URGENT" in maint_out:
        # Find what's urgent
        urgent_lines = [l.strip() for l in maint_out.splitlines() if "URGENT" in l]
        for l in urgent_lines[:2]:
            print(f"  URGENT: {l}")
    elif "[DUE]" in maint_out:
        # Find the actual DUE item lines (marked with !)
        due_lines = [l.strip() for l in maint_out.splitlines() if l.strip().startswith("!")]
        for l in due_lines[:2]:
            print(f"  DUE: {l.lstrip('! ')}")
    elif "[PERIODIC]" in maint_out:
        periodic_lines = [l.strip() for l in maint_out.splitlines() if l.strip().startswith("~")]
        for l in periodic_lines[:2]:
            print(f"  PERIODIC: {l.lstrip('~ ')}")
    elif priorities:
        print(f"  {priorities[0]}")
    else:
        print("  State clean — pick a frontier or run a periodic")


if __name__ == "__main__":
    main()
