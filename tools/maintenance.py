#!/usr/bin/env python3
"""maintenance.py — Surface what needs doing now. Run at session start.
Priority: URGENT > DUE > PERIODIC > NOTICE. Use --quick to skip remote checks."""

import json
import platform
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PYTHON_EXE = sys.executable or "python3"
PYTHON_CMD = "python3" if shutil.which("python3") else "python"
if not shutil.which(PYTHON_CMD):
    PYTHON_CMD = Path(PYTHON_EXE).name


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
        return len(_read(path).splitlines())
    except Exception:
        return 0


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


def _exists(path: str) -> bool:
    return (REPO_ROOT / path).exists()


def _session_number() -> int:
    """Extract current session number from SESSION-LOG.md."""
    log = _read(REPO_ROOT / "memory" / "SESSION-LOG.md")
    numbers = re.findall(r"^S(\d+)", log, re.MULTILINE)
    return max(int(n) for n in numbers) if numbers else 0


def _active_principle_ids(text: str) -> tuple[set[int], set[int]]:
    """Parse PRINCIPLES.md text, return (all_ids, superseded_ids)."""
    all_ids = {int(m.group(1)) for m in re.finditer(r"\bP-(\d+)\b", text)}
    sup = {int(m.group(1)) for m in re.finditer(r"\bP-(\d+)→", text)}
    sup |= {int(m.group(1)) for m in re.finditer(
        r"\(P-(\d+)\s+(?:merged|superseded|absorbed)\)", text, re.IGNORECASE)}
    for m in re.finditer(r"P-(\d+)\+P-(\d+)\s+merged", text, re.IGNORECASE):
        sup.add(int(m.group(1))); sup.add(int(m.group(2)))
    return all_ids, sup


def _normalize_hq_question(text: str) -> str:
    """Normalize HUMAN-QUEUE headings for duplicate/re-ask detection."""
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", (text or "").lower())
    return re.sub(r"\s+", " ", text).strip()


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
    """Check human queue quality: open count, re-asks, and metadata completeness."""
    results = []
    hq_text = _read(REPO_ROOT / "tasks" / "HUMAN-QUEUE.md")
    if not hq_text:
        return results

    answered_pos = hq_text.find("## Answered")
    heading_matches = list(re.finditer(r"^###\s+.*$", hq_text, re.MULTILINE))

    open_items: list[str] = []
    missing_metadata: list[str] = []
    open_by_norm: dict[str, list[str]] = {}
    answered_by_norm: dict[str, list[str]] = {}

    for i, m in enumerate(heading_matches):
        line = m.group(0).strip()
        heading = line[4:].strip()  # strip leading "### "
        plain = heading.replace("~~", "").strip()
        id_match = re.search(r"\b(HQ-\d+)\b", plain)
        if not id_match:
            continue

        hq_id = id_match.group(1)
        body_start = m.end()
        body_end = heading_matches[i + 1].start() if i + 1 < len(heading_matches) else len(hq_text)
        body = hq_text[body_start:body_end]

        in_answered = answered_pos >= 0 and m.start() >= answered_pos
        is_struck = heading.startswith("~~")

        # Extract question text from heading: "HQ-N: question"
        question = plain.split(":", 1)[1].strip() if ":" in plain else plain
        question = re.sub(r"\s+(?:RESOLVED|ANSWERED|CLOSED)\b.*$", "", question, flags=re.IGNORECASE).strip()
        q_norm = _normalize_hq_question(question)

        if q_norm:
            if in_answered or is_struck:
                answered_by_norm.setdefault(q_norm, []).append(hq_id)
            else:
                open_by_norm.setdefault(q_norm, []).append(hq_id)

        if not in_answered and not is_struck:
            open_items.append(hq_id)
            # Each open question should carry ask-time metadata for traceability.
            if not re.search(r"\*\*(Asked|Date)\*\*:", body, re.IGNORECASE):
                missing_metadata.append(hq_id)

    if open_items:
        results.append(("NOTICE", f"{len(open_items)} unanswered item(s) in HUMAN-QUEUE.md"))

    duplicate_open = [ids for ids in open_by_norm.values() if len(ids) > 1]
    if duplicate_open:
        sample = "; ".join("/".join(ids[:3]) for ids in duplicate_open[:3])
        results.append(("DUE", f"Possible duplicate open HUMAN-QUEUE items: {sample}"))

    reasked = []
    for norm, open_ids in open_by_norm.items():
        if norm in answered_by_norm:
            reasked.append(f"{'/'.join(open_ids[:2])} (answered: {'/'.join(answered_by_norm[norm][:2])})")
    if reasked:
        results.append(("DUE", f"Open HUMAN-QUEUE item(s) match already answered question(s): {'; '.join(reasked[:3])}"))

    if missing_metadata:
        results.append(("NOTICE", f"{len(missing_metadata)} open HUMAN-QUEUE item(s) missing ask metadata (**Asked**/**Date**): {', '.join(missing_metadata[:5])}"))

    return results


def check_child_bulletins() -> list[tuple[str, str]]:
    """Check for unprocessed child bulletins, filtering already-integrated children."""
    results = []
    bulletin_dir = REPO_ROOT / "experiments" / "inter-swarm" / "bulletins"
    integration_dir = REPO_ROOT / "experiments" / "integration-log"
    children_dir = REPO_ROOT / "experiments" / "children"
    if not bulletin_dir.exists():
        return results

    integrated = set()
    if integration_dir.exists():
        for f in integration_dir.glob("*.json"):
            integrated.add(f.stem)

    known_children = set()
    if children_dir.exists():
        known_children = {d.name for d in children_dir.iterdir() if d.is_dir()}

    unprocessed = []
    stale = []
    external = []
    for f in bulletin_dir.glob("*.md"):
        name = f.stem
        # Child-bulletin check is scoped to known children only.
        # External/swarm-to-swarm coordination files are handled separately
        # by check_help_requests and direct bulletin scanning.
        if name not in known_children and name not in integrated:
            external.append(name)
            continue

        content = _read(f)
        if name in integrated:
            stale.append(name)
        elif "<!-- PROCESSED" in content:
            continue  # bulletin manually marked as processed
        else:
            unprocessed.append(name)

    if unprocessed:
        results.append(("DUE", f"{len(unprocessed)} unprocessed bulletin(s): {', '.join(unprocessed[:5])}"))
    if stale:
        results.append(("NOTICE", f"{len(stale)} stale bulletin(s) from integrated children (can delete): {', '.join(stale[:5])}"))
    if external:
        results.append(("NOTICE", f"{len(external)} external bulletin file(s) ignored by child-harvest check: {', '.join(external[:5])}"))

    return results


def check_help_requests() -> list[tuple[str, str]]:
    """Check for unresolved help-request bulletins across swarms."""
    results = []
    bulletin_dir = REPO_ROOT / "experiments" / "inter-swarm" / "bulletins"
    if not bulletin_dir.exists():
        return results

    req_re = re.compile(
        r"# Bulletin from:\s*(.+?)\nDate:\s*(\S+)\nType:\s*help-request\n\n## Content\n"
        r"Request-ID:\s*(\S+)\nNeed:\s*(.+?)(?:\n---|\Z)",
        re.DOTALL,
    )
    resp_re = re.compile(
        r"# Bulletin from:\s*(.+?)\nDate:\s*(\S+)\nType:\s*help-response\n\n## Content\n"
        r"Request-ID:\s*(\S+)\nResponse:\s*(.+?)(?:\n---|\Z)",
        re.DOTALL,
    )

    requests: dict[str, str] = {}
    responses: set[str] = set()

    for f in sorted(bulletin_dir.glob("*.md")):
        text = _read(f)
        for m in req_re.finditer(text):
            requester, _, request_id, _ = m.groups()
            requests[request_id.strip()] = requester.strip()
        for m in resp_re.finditer(text):
            _, _, request_id, _ = m.groups()
            responses.add(request_id.strip())

    open_ids = [rid for rid in sorted(requests) if rid not in responses]
    if open_ids:
        sample = ", ".join(f"{rid}({requests[rid]})" for rid in open_ids[:3])
        results.append((
            "DUE",
            f"{len(open_ids)} open help request(s) across swarms — respond via: {PYTHON_CMD} tools/bulletin.py offer-help <your-name> <request-id> <response> ({sample})",
        ))

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
    """Check for decayed frontier questions. Auto-refreshes decay from SESSION-LOG.md."""
    results = []
    frontier_path = REPO_ROOT / "tasks" / "FRONTIER.md"
    decay_file = REPO_ROOT / "experiments" / "frontier-decay.json"
    if not frontier_path.exists():
        return results
    text = frontier_path.read_text()
    open_text = text[:text.find("## Archive")] if "## Archive" in text else text
    decay = {}
    if decay_file.exists():
        try: decay = json.loads(decay_file.read_text())
        except Exception: pass
    # Auto-refresh from SESSION-LOG and FRONTIER session mentions
    for line in _read(REPO_ROOT / "memory" / "SESSION-LOG.md").splitlines():
        dm = re.search(r"\d{4}-\d{2}-\d{2}", line)
        if not dm: continue
        for fm in re.finditer(r"\bF(\d+)\b", line):
            fid = f"F{fm.group(1)}"
            if dm.group() > decay.get(fid, {}).get("last_active", "1970-01-01"):
                decay[fid] = {"last_active": dm.group()}
    for m in re.finditer(r"^- \*\*F(\d+)\*\*:.*S(\d+)", open_text, re.MULTILINE):
        decay.setdefault(f"F{m.group(1)}", {"last_active": date.today().isoformat()})
    try: decay_file.parent.mkdir(parents=True, exist_ok=True); decay_file.write_text(json.dumps(decay, indent=2))
    except Exception: pass
    today = date.today()
    weak, archive = [], []
    for m in re.finditer(r"^- \*\*F(\d+)\*\*:", open_text, re.MULTILINE):
        fid = f"F{m.group(1)}"
        days = (today - date.fromisoformat(decay.get(fid, {}).get("last_active", today.isoformat()))).days
        strength = 0.9 ** days
        if strength < 0.1: archive.append(fid)
        elif strength < 0.3: weak.append(fid)
    if archive:
        results.append(("DUE", f"{len(archive)} frontier(s) below archive threshold: {', '.join(archive)}"))
    if weak:
        results.append(("NOTICE", f"{len(weak)} frontier(s) weakening: {', '.join(weak)}"))
    return results


def check_periodics() -> list[tuple[str, str]]:
    """Check self-scheduled periodic items from periodics.json."""
    results = []
    periodics_path = REPO_ROOT / "tools" / "periodics.json"
    if not periodics_path.exists():
        return results

    try:
        data = json.loads(periodics_path.read_text())
    except Exception:
        return results

    session = _session_number()
    if session <= 0:
        return results

    for item in data.get("items", []):
        cadence = item.get("cadence_sessions", 10)
        last = item.get("last_reviewed_session", 0)
        gap = session - last
        if gap >= cadence:
            overdue = gap - cadence
            urgency = "DUE" if overdue > cadence else "PERIODIC"
            results.append((urgency, f"{item['description']} (every ~{cadence} sessions, last: S{last})"))

    return results


def check_validator() -> list[tuple[str, str]]:
    """Quick check if validator passes."""
    results = []
    try:
        r = subprocess.run(
            [PYTHON_EXE, str(REPO_ROOT / "tools" / "validate_beliefs.py"), "--quick"],
            capture_output=True, text=True, timeout=30
        )
        if "RESULT: FAIL" in r.stdout:
            results.append(("URGENT", "validate_beliefs.py FAIL — fix before other work"))
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


def check_runtime_portability() -> list[tuple[str, str]]:
    """Check host runtime capabilities required for cross-environment swarming."""
    results = []

    has_git = bool(shutil.which("git"))
    has_bash = bool(shutil.which("bash"))
    has_python_alias = bool(shutil.which("python3") or shutil.which("python"))

    if not has_git:
        results.append(("URGENT", "git not found in PATH — swarm memory/commit workflow cannot run"))
    if not has_python_alias:
        results.append(("DUE", f"No python alias in PATH — use explicit interpreter: {PYTHON_EXE}"))
    if not has_bash and (_exists("workspace/genesis.sh") or _exists("tools/check.sh")):
        results.append(("DUE", "bash not found — `workspace/genesis.sh` and `tools/check.sh` won't run on this host"))

    bridges = [
        "SWARM.md",
        "CLAUDE.md",
        "AGENTS.md",
        "GEMINI.md",
        ".cursorrules",
        ".windsurfrules",
        ".github/copilot-instructions.md",
    ]
    missing_bridges = [p for p in bridges if not _exists(p)]
    if missing_bridges:
        level = "URGENT" if "SWARM.md" in missing_bridges else "DUE"
        sample = ", ".join(missing_bridges[:3])
        results.append((level, f"{len(missing_bridges)} missing bridge file(s): {sample}"))

    return results


def check_cross_references() -> list[tuple[str, str]]:
    """Check that top-level directories in INDEX.md structure section exist (F112)."""
    results = []
    index_text = _read(REPO_ROOT / "memory" / "INDEX.md")

    # Extract directory prefixes from structure block (lines starting with word/)
    struct_match = re.search(r"```\n(.*?)```", index_text, re.DOTALL)
    if not struct_match:
        return results

    broken = []
    for line in struct_match.group(1).splitlines():
        m = re.match(r"^(\w[\w-]*/)", line.strip())
        if not m:
            continue
        dir_path = m.group(1).rstrip("/")
        full = REPO_ROOT / dir_path
        if not full.exists():
            broken.append(dir_path)

    if broken:
        results.append(("DUE", f"{len(broken)} broken directory(s) in INDEX.md structure: {', '.join(broken[:3])}"))

    # Check lesson count matches actual files
    lessons_dir = REPO_ROOT / "memory" / "lessons"
    if lessons_dir.exists():
        actual = len(list(lessons_dir.glob("L-*.md")))
        count_match = re.search(r"\*\*(\d+) lessons\*\*", index_text)
        if count_match:
            claimed = int(count_match.group(1))
            if actual != claimed:
                results.append(("NOTICE", f"INDEX.md claims {claimed} lessons but {actual} exist"))

    # Check principles count — ID-count is ground truth (S73b resolution: headers drift)
    principles_text = _read(REPO_ROOT / "memory" / "PRINCIPLES.md")
    all_pids, superseded_pids = _active_principle_ids(principles_text)
    actual_active_p = len(all_pids - superseded_pids)

    p_header_match = re.search(r"(\d+)\s+(?:live\s+)?principles", principles_text)
    idx_p_match = re.search(r"\*\*(\d+) principles\*\*", index_text)
    if p_header_match and int(p_header_match.group(1)) != actual_active_p:
        results.append(("NOTICE", f"PRINCIPLES.md header says {p_header_match.group(1)} but ID-count finds {actual_active_p} active"))
    if idx_p_match and int(idx_p_match.group(1)) != actual_active_p:
        results.append(("NOTICE", f"INDEX.md claims {idx_p_match.group(1)} principles but ID-count finds {actual_active_p} active"))

    # Check frontier question count
    frontier_text = _read(REPO_ROOT / "tasks" / "FRONTIER.md")
    idx_f_match = re.search(r"\*\*(\d+) frontier questions\*\*", index_text)
    actual_frontier = len(re.findall(r"^- \*\*F\d+\*\*:", frontier_text, re.MULTILINE))
    if idx_f_match:
        claimed_f = int(idx_f_match.group(1))
        if claimed_f != actual_frontier:
            results.append(("NOTICE", f"INDEX.md claims {claimed_f} frontier questions but {actual_frontier} active"))

    return results


def check_handoff_staleness() -> list[tuple[str, str]]:
    """Check for stale handoff items in NEXT.md (>3 sessions old)."""
    results = []
    next_text = _read(REPO_ROOT / "tasks" / "NEXT.md")
    session = _session_number()
    if not next_text or session <= 0:
        return results
    stale = []
    for m in re.finditer(r"\(added S(\d+)\)", next_text):
        age = session - int(m.group(1))
        if age > 3:
            line_start = next_text.rfind("\n", 0, m.start()) + 1
            line_end = next_text.find("\n", m.end())
            line = next_text[line_start:line_end if line_end > 0 else len(next_text)].strip()
            item_match = re.search(r"\*\*(.+?)\*\*", line)
            stale.append(f"{item_match.group(1) if item_match else line[:50]} (age: {age})")
    if stale:
        results.append(("DUE", f"{len(stale)} stale handoff(s) in NEXT.md: {'; '.join(stale[:3])}"))
    return results


def check_utility() -> list[tuple[str, str]]:
    """Surface zero-citation active principles (F116/F114)."""
    results = []
    principles_text = _read(REPO_ROOT / "memory" / "PRINCIPLES.md")
    if not principles_text:
        return results
    all_ids, superseded = _active_principle_ids(principles_text)
    active_ids = all_ids - superseded
    cited: set[int] = set()
    principles_path = REPO_ROOT / "memory" / "PRINCIPLES.md"
    for ext in ("*.md", "*.py", "*.json"):
        for f in REPO_ROOT.rglob(ext):
            if f == principles_path or ".git" in f.parts:
                continue
            for m in re.finditer(r"\bP-(\d+)\b", _read(f)):
                cited.add(int(m.group(1)))
    uncited = sorted(active_ids - cited)
    if uncited:
        sample = ", ".join(f"P-{x}" for x in uncited[:5])
        results.append(("NOTICE", f"{len(uncited)} active principle(s) with 0 citations — compression candidates: {sample}{'...' if len(uncited) > 5 else ''}"))
    return results


def check_proxy_k_drift() -> list[tuple[str, str]]:
    """Check if proxy K has drifted >6% above last compression floor (P-163, F105)."""
    results = []
    log_path = REPO_ROOT / "experiments" / "proxy-k-log.json"
    if not log_path.exists():
        return results

    try:
        entries = json.loads(log_path.read_text())
    except Exception:
        return results

    if len(entries) < 2:
        return results

    # Find compression floor: most recent entry where total decreased from previous
    floor_idx = 0
    for i in range(1, len(entries)):
        if entries[i]["total"] < entries[i - 1]["total"]:
            floor_idx = i

    floor_entry = entries[floor_idx]
    floor = floor_entry["total"]
    latest_entry = entries[-1]
    latest = latest_entry["total"]
    if floor <= 0:
        return results

    drift = (latest - floor) / floor
    if drift > 0.06:
        # Identify which tiers grew most since floor
        floor_tiers = floor_entry.get("tiers", {})
        latest_tiers = latest_entry.get("tiers", {})
        tier_deltas = []
        for tier in sorted(latest_tiers):
            delta = latest_tiers.get(tier, 0) - floor_tiers.get(tier, 0)
            if delta > 0:
                tier_deltas.append(f"{tier}+{delta}")
        targets = ", ".join(tier_deltas[:3]) if tier_deltas else "unknown"
        level = "URGENT" if drift > 0.10 else "DUE"
        results.append((level, f"Proxy K drift {drift:.1%} ({latest} vs floor {floor}) — run: {PYTHON_CMD} tools/compact.py (P-163, F105)"))

    return results


def check_file_graph() -> list[tuple[str, str]]:
    """Check that file references in structural files point to existing files (F112, P-136)."""
    results = []
    # Structural files whose references form the swarm's internal topology
    structural = [
        REPO_ROOT / "SWARM.md",
        REPO_ROOT / "CLAUDE.md",
        REPO_ROOT / "beliefs" / "CORE.md",
        REPO_ROOT / "memory" / "INDEX.md",
    ]
    # Extract backtick-quoted file paths (e.g., `beliefs/DEPS.md`, `memory/DISTILL.md`)
    broken = []
    for sf in structural:
        text = _read(sf)
        if not text:
            continue
        refs = re.findall(r"`([a-zA-Z][\w\-/]+\.(?:md|py|json|sh))`", text)
        for ref in refs:
            # Skip if it's a code pattern, not a file reference
            if ref.startswith("L-") or ref.startswith("P-") or ref.startswith("B-"):
                continue
            full = REPO_ROOT / ref
            if not full.exists():
                broken.append(f"{sf.name}→{ref}")
    if broken:
        results.append(("DUE", f"{len(broken)} broken file reference(s): {', '.join(broken[:5])}"))
    return results


def build_inventory() -> dict:
    """Build a compact capability inventory for fast orientation."""
    bridges = [
        "SWARM.md",
        "CLAUDE.md",
        "AGENTS.md",
        "GEMINI.md",
        ".cursorrules",
        ".windsurfrules",
        ".github/copilot-instructions.md",
    ]
    core_state = [
        "beliefs/CORE.md",
        "memory/INDEX.md",
        "tasks/FRONTIER.md",
        "tasks/NEXT.md",
        "memory/PRINCIPLES.md",
    ]
    capability_sets: dict[str, list[str]] = {
        "orientation": ["tools/maintenance.py", "tools/pulse.py", "tools/context_router.py"],
        "validation": ["tools/validate_beliefs.py", "tools/check.sh"],
        "evolution": ["tools/evolve.py", "tools/swarm_test.py", "tools/agent_swarm.py", "tools/colony.py", "tools/spawn_coordinator.py"],
        "inter_swarm": ["tools/bulletin.py", "tools/merge_back.py", "tools/propagate_challenges.py"],
        "compaction": ["tools/compact.py", "tools/proxy_k.py", "tools/frontier_decay.py"],
        "analysis": ["tools/nk_analyze.py", "tools/nk_analyze_go.py", "tools/wiki_swarm.py"],
    }
    commands = {
        "python3": bool(shutil.which("python3")),
        "python": bool(shutil.which("python")),
        "git": bool(shutil.which("git")),
        "bash": bool(shutil.which("bash")),
    }

    return {
        "host": {
            "platform": platform.platform(),
            "python_executable": PYTHON_EXE,
            "python_command_hint": PYTHON_CMD,
            "commands": commands,
        },
        "bridges": [{"path": p, "exists": _exists(p)} for p in bridges],
        "core_state": [{"path": p, "exists": _exists(p)} for p in core_state],
        "capabilities": {
            name: {
                "present": sum(1 for p in files if _exists(p)),
                "total": len(files),
                "files": files,
            }
            for name, files in capability_sets.items()
        },
    }


def print_inventory(inv: dict):
    print("=== SWARM INVENTORY ===")
    host = inv["host"]
    print(f"Host: {host['platform']}")
    print(f"Python: {host['python_executable']}")
    print(f"Command hint: {host['python_command_hint']}")
    print()

    print("Commands:")
    for name, ok in host["commands"].items():
        print(f"  {'OK ' if ok else 'NO '} {name}")
    print()

    print("Bridge files:")
    for item in inv["bridges"]:
        print(f"  {'OK ' if item['exists'] else 'NO '} {item['path']}")
    print()

    print("Core state:")
    for item in inv["core_state"]:
        print(f"  {'OK ' if item['exists'] else 'NO '} {item['path']}")
    print()

    print("Capabilities:")
    for name, info in inv["capabilities"].items():
        print(f"  {name:<12} {info['present']}/{info['total']}")
    print()




# --- Main ---

PRIORITY_ORDER = {"URGENT": 0, "DUE": 1, "PERIODIC": 2, "NOTICE": 3}
PRIORITY_SYMBOLS = {"URGENT": "!!!", "DUE": " ! ", "PERIODIC": " ~ ", "NOTICE": " . "}


def main():
    if "--inventory" in sys.argv:
        inv = build_inventory()
        if "--json" in sys.argv:
            print(json.dumps(inv, indent=2))
        else:
            print_inventory(inv)
        return

    quick = "--quick" in sys.argv

    all_checks = [
        check_validator,
        check_runtime_portability,
        check_version_drift,
        check_open_challenges,
        check_compaction,
        check_lessons,
        check_child_bulletins,
        check_help_requests,
        check_frontier_decay,
        check_periodics,
        check_human_queue,
        check_uncommitted,
        check_handoff_staleness,
        check_cross_references,
        check_file_graph,
        check_utility,
        check_proxy_k_drift,
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
