#!/usr/bin/env python3

import importlib
import json
import hashlib
import os
import platform
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

def _load_symbol(module_names: tuple[str, ...], symbol: str):
    for name in module_names:
        try: return getattr(importlib.import_module(name), symbol)
        except (ModuleNotFoundError, AttributeError): continue
    return None

_paper_drift = _load_symbol(("tools.paper_drift", "paper_drift"), "check_paper_accuracy")
if _paper_drift is None:
    def run_paper_drift_check(repo_root: Path, session: int) -> list[tuple[str, str]]:
        return [
            ("NOTICE", "paper_drift module missing — skipping PAPER drift check (restore tools/paper_drift.py)")
        ]
else:
    run_paper_drift_check = _paper_drift

_parse_active_principle_ids = _load_symbol(("tools.swarm_parse", "swarm_parse"), "active_principle_ids")
if _parse_active_principle_ids is None:
    def parse_active_principle_ids(text: str) -> tuple[set[int], set[int]]:
        all_ids = {int(m.group(1)) for m in re.finditer(r"\bP-(\d+)\b", text)}
        superseded = {int(m.group(1)) for m in re.finditer(r"\bP-(\d+)→", text)}
        superseded |= {
            int(m.group(1))
            for m in re.finditer(r"\(P-(\d+)\s+(?:merged|superseded|absorbed)\)", text, re.IGNORECASE)
        }
        for m in re.finditer(r"P-(\d+)\+P-(\d+)\s+merged", text, re.IGNORECASE):
            superseded.add(int(m.group(1)))
            superseded.add(int(m.group(2)))
        return all_ids, superseded
else:
    parse_active_principle_ids = _parse_active_principle_ids

REPO_ROOT = Path(__file__).resolve().parent.parent
PYTHON_EXE = sys.executable or "python3"
PRINCIPLE_ID_RE = re.compile(r"\bP-(\d+)\b")
UTILITY_CITATION_MAX_BYTES = 256 * 1024
UTILITY_CITATION_SKIP_PREFIXES = (
    ".git/",
    "workspace/notes/",
    "experiments/colonies/",
)
FILE_REF_ALIAS_MAP = {
    "SWARM.md": "SWARM.md", "CLAUDE.md": "CLAUDE.md", "AGENTS.md": "AGENTS.md",
    "GEMINI.md": "GEMINI.md", "README.md": "README.md",
    "CORE.md": "beliefs/CORE.md", "PHILOSOPHY.md": "beliefs/PHILOSOPHY.md",
    "DEPS.md": "beliefs/DEPS.md", "INVARIANTS.md": "beliefs/INVARIANTS.md",
    "CONFLICTS.md": "beliefs/CONFLICTS.md", "CHALLENGES.md": "beliefs/CHALLENGES.md",
    "INDEX.md": "memory/INDEX.md", "PRINCIPLES.md": "memory/PRINCIPLES.md",
    "SESSION-LOG.md": "memory/SESSION-LOG.md", "OPERATIONS.md": "memory/OPERATIONS.md",
    "HUMAN.md": "memory/HUMAN.md",
    "FRONTIER.md": "tasks/FRONTIER.md", "NEXT.md": "tasks/NEXT.md",
    "HUMAN-QUEUE.md": "tasks/HUMAN-QUEUE.md", "RESOLUTION-CLAIMS.md": "tasks/RESOLUTION-CLAIMS.md",
    "PAPER.md": "docs/PAPER.md",
}
LANE_ACTIVE_STATUSES = {"CLAIMED", "ACTIVE", "BLOCKED", "READY"}
LANE_PLACEHOLDERS = {"", "-", "n/a", "na", "none", "pending", "tbd", "unknown"}
LANE_STALE_NOTICE_SESSIONS = 1
LANE_STALE_DUE_SESSIONS = 3
LANE_ANTIWINDUP_ROWS = 10
LANE_REPORT_KEYS = ("capabilities", "intent", "progress", "available", "blocked", "next_step", "human_open_item")
DOMAIN_SYNC_ALLOWED_VALUES = {"queued", "syncing", "synced", "stale", "n/a", "na"}
LANE_AVAILABLE_ALLOWED_VALUES = {"yes", "no", "partial"}
LANE_AVAILABLE_LEGACY_MAP = {"ready": "yes", "now": "yes", "true": "yes", "false": "no"}
HIGH_RISK_LANE_PATTERNS = (
    (re.compile(r"\b(?:git[-_\s]*)?reset[-_\s]*(?:--)?hard\b", re.IGNORECASE), "reset-hard"),
    (re.compile(r"\b(?:git[-_\s]*)?clean[-_\s]*(?:-fd|-fdx|fd|fdx)\b", re.IGNORECASE), "clean-fd"),
    (re.compile(r"\b(?:push[-_\s]*--force|force[-_\s]*push)\b", re.IGNORECASE), "force-push"),
    (re.compile(r"\brm[-_\s]*-?rf\b", re.IGNORECASE), "rm-rf"),
    (re.compile(r"\b(?:branch[-_\s]*delete|delete[-_\s]*branch)\b", re.IGNORECASE), "delete-branch"),
    (re.compile(r"\bdrop[-_\s]*table\b", re.IGNORECASE), "drop-table"),
    (re.compile(r"\bkill[-_\s]*switch[-_\s]*activate\b", re.IGNORECASE), "kill-switch-activate"),
    (re.compile(r"\bshutdown\b", re.IGNORECASE), "shutdown"),
    (re.compile(r"\b(?:irreversible|destructive|wipe[-_\s]*repo|purge)\b", re.IGNORECASE), "irreversible"),
    # External-facing actions (L-366: high-risk tier — visible to others, hard to reverse)
    (re.compile(r"\b(?:create[-_\s]*pr|open[-_\s]*pr|gh[-_\s]*pr[-_\s]*create)\b", re.IGNORECASE), "create-pr"),
    (re.compile(r"\b(?:send[-_\s]*email|send[-_\s]*mail|smtp|mailto)\b", re.IGNORECASE), "send-email"),
    (re.compile(r"\b(?:post[-_\s]*to[-_\s]*external|external[-_\s]*api[-_\s]*write|publish[-_\s]*external)\b", re.IGNORECASE), "external-publish"),
)
IGNORED_UNTRACKED_RUNTIME_FILES = {"tools/check.ps1", "tools/maintenance.ps1"}
LANE_GLOBAL_FOCUS_VALUES = {"global", "system", "all", "coordination", "cross-cutting", "crosscutting"}
CHECK_FOCUS_HISTORIAN_REQUIRED = {"objective", "historian"}
HISTORIAN_SELF_ANCHOR_TOKENS = ("next", "swarm-lanes", "session-log")
HISTORIAN_SURROUNDINGS_ANCHOR_TOKENS = ("frontier", "artifact", "domain", "experiment", "bulletin")
F119_STALE_EVIDENCE_SESSIONS = {"python-alias-missing": 12, "inter-swarm-tooling-missing": 16}
F119_TRANSITION_OUTCOME_PATTERNS = (r"Beliefs:? PASS", r"NOTICE-only", r"no DUE", r"no URGENT", r"verification pass")
F119_RECENT_REASON_ACTIVITY_WINDOW = 6
BRIDGE_FILES = ["SWARM.md", "CLAUDE.md", "AGENTS.md", "GEMINI.md",
                ".cursorrules", ".windsurfrules", ".github/copilot-instructions.md"]
KILL_SWITCH_PATH = REPO_ROOT / "tasks" / "KILL-SWITCH.md"
DOMAIN_FRONTIER_ID_PATTERN = r"F(?:-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*|\d+(?:-[A-Za-z0-9]+)?)"
DOMAIN_FRONTIER_ID_RE = re.compile(rf"\b({DOMAIN_FRONTIER_ID_PATTERN})\b", re.IGNORECASE)
DOMAIN_ACTIVE_BULLET_RE = re.compile(rf"^\s*-\s*(?:~~)?\*\*({DOMAIN_FRONTIER_ID_PATTERN})\*\*", re.IGNORECASE)
STRUCTURE_REQUIRED_PATHS = (
    "docs/SWARM-STRUCTURE.md",
    "references/README.md",
    "recordings/README.md",
)
STRUCTURE_ALLOWED_FILENAMES = {"README.md", ".gitkeep"}
STRUCTURE_ALLOWED_EXTENSIONS = {
    "references": {".md", ".json", ".txt", ".csv", ".tsv", ".bib", ".yml", ".yaml"},
    "recordings": {".md", ".json", ".txt", ".csv", ".tsv", ".log", ".yml", ".yaml"},
}

def _truncated(items, n=3, sep=", ", fmt=None):
    show = items[:n]
    parts = [fmt(x) for x in show] if fmt else [str(x) for x in show]
    return sep.join(parts) + ("..." if len(items) > n else "")

def _command_exists(cmd: str) -> bool:
    return bool(shutil.which(cmd))

def _command_runs(cmd: str, args: list[str], timeout: int = 5) -> bool:
    if not _command_exists(cmd): return False
    try: return subprocess.run([cmd] + args, capture_output=True, text=True, timeout=timeout).returncode == 0
    except Exception: return False

def _python_command_runs(cmd: str) -> bool:
    return _command_runs(cmd, ["-c", "import sys"], timeout=8)

def _py_launcher_runs() -> bool:
    return _command_runs("py", ["-3", "-c", "import sys"], timeout=8)

def _select_python_command() -> str:
    for c in ("python3", "python"):
        if _python_command_runs(c): return c
    if _py_launcher_runs(): return "py -3"
    name = Path(PYTHON_EXE).name
    return name if _python_command_runs(name) else PYTHON_EXE

PYTHON_CMD = _select_python_command()

def _git(*args: str) -> str:
    try: return subprocess.run(["git", "-C", str(REPO_ROOT)] + list(args),
                               capture_output=True, text=True, timeout=10).stdout.rstrip("\n")
    except Exception: return ""

def _decode_git_path(path: str) -> str:
    p = path.strip()
    if p.startswith('"') and p.endswith('"') and len(p) >= 2:
        inner = p[1:-1]
        try:
            unescaped = bytes(inner, "latin1").decode("unicode_escape")
            p = unescaped.encode("latin1", "ignore").decode("utf-8", "replace")
        except Exception:
            p = inner
    p = p.replace("\\", "/").replace("\uf03a", ":")
    if re.match(r"^[A-Za-z]:[^/]", p):
        p = p[:2] + "/" + p[2:]
    return p

def _status_path(line: str) -> str:
    path = line[3:].strip() if len(line) >= 3 else line.strip()
    if " -> " in path:
        path = path.split(" -> ", 1)[1].strip()
    return _decode_git_path(path)

def _tracked_changed_paths() -> list[str]:
    status = _git("-c", "core.quotepath=false", "status", "--porcelain")
    if not status:
        return []
    return [_status_path(line) for line in status.splitlines()
            if line.rstrip() and line[:2] != "??"]

def _line_count(path: Path) -> int:
    try: return len(_read(path).splitlines())
    except Exception: return 0

def _token_count(path: Path) -> int:
    try: return len(_read(path)) // 4
    except Exception: return 0

def _read(path: Path) -> str:
    try: return path.read_text(encoding="utf-8", errors="replace")
    except Exception: return ""

def _exists(path: str) -> bool:
    return (REPO_ROOT / path).exists()

def _is_wsl_mnt_repo() -> bool:
    if not sys.platform.startswith("linux"): return False
    info = (platform.release() + " " + platform.platform()).lower()
    if "microsoft" not in info: return False
    return str(REPO_ROOT).replace("\\", "/").startswith("/mnt/")

def _session_number() -> int:
    numbers = re.findall(r"^S(\d+)", _read(REPO_ROOT / "memory" / "SESSION-LOG.md"), re.MULTILINE)
    log_max = max(int(n) for n in numbers) if numbers else 0
    try:
        git_out = subprocess.run(["git", "log", "--oneline", "-50"], capture_output=True, text=True, cwd=REPO_ROOT, timeout=5).stdout
        git_max = max((int(m) for m in re.findall(r"\[S(\d+)\]", git_out)), default=0)
    except Exception:
        git_max = 0
    return max(log_max, git_max)

_active_principle_ids = parse_active_principle_ids

def _normalize_hq_question(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-zA-Z0-9\s]", " ", (text or "").lower())).strip()

def _resolve_repo_file_ref(ref: str) -> str | None:
    return ref if "/" in ref else FILE_REF_ALIAS_MAP.get(ref)

def _is_lane_placeholder(value: str) -> bool:
    return (value or "").strip().lower() in LANE_PLACEHOLDERS

def _parse_lane_tags(value: str) -> dict[str, str]:
    return {k.strip().lower(): v.strip()
            for k, v in re.findall(r"([A-Za-z][A-Za-z0-9_-]*)\s*=\s*([^\s,;|]+)", value or "")}

def _lane_domain_focus(row: dict[str, str], tags: dict[str, str]) -> str | None:
    for raw in (tags.get("focus", ""), row.get("scope_key", "")):
        match = re.search(r"domains/([a-z0-9][a-z0-9-]*)", (raw or "").strip().lower())
        if match:
            return match.group(1)
    return None

def _parse_check_focus_modes(raw: str) -> set[str]:
    return {tok for tok in re.split(r"[+,/;|]+", (raw or "").strip().lower()) if tok}

def _historian_anchor_coverage(raw: str) -> tuple[bool, bool]:
    low = (raw or "").strip().lower()
    has_self = any(token in low for token in HISTORIAN_SELF_ANCHOR_TOKENS)
    has_surroundings = any(token in low for token in HISTORIAN_SURROUNDINGS_ANCHOR_TOKENS)
    return has_self, has_surroundings

def _lane_has_any_tag(tags: dict[str, str], keys: tuple[str, ...]) -> bool:
    return any(key in tags for key in keys)

def _lane_high_risk_signal(row: dict[str, str], tags: dict[str, str]) -> str | None:
    haystack = " ".join(
        part for part in (
            row.get("scope_key", ""),
            row.get("notes", ""),
            tags.get("intent", ""),
            tags.get("next_step", ""),
            tags.get("action", ""),
            tags.get("plan", ""),
            tags.get("objective", ""),
        )
        if part
    )
    for pattern, label in HIGH_RISK_LANE_PATTERNS:
        if pattern.search(haystack):
            return label
    return None

def _is_dispatch_lane_row(row: dict[str, str], tags: dict[str, str]) -> bool:
    lane = (row.get("lane", "") or "").strip().lower()
    if any(key in tags for key in ("dispatch", "slot", "wip_cap")):
        return True
    return bool(re.search(r"(?:^|[-_/])(msw\d*|domex|slot)(?:$|[-_/])", lane))

def _is_coordinator_lane_row(row: dict[str, str], tags: dict[str, str]) -> bool:
    lane = (row.get("lane", "") or "").strip().lower()
    scope = (row.get("scope_key", "") or "").strip().lower()
    has_coord_hint = (
        bool(re.search(r"(?:^|[-_/])(coord|coordinator)(?:$|[-_/])", lane))
        or "coordinator" in scope
        or "tasks/swarm-lanes.md" in scope
    )
    return has_coord_hint

_LANE_KEYS = ("date", "lane", "session", "agent", "branch", "pr", "model", "platform", "scope_key", "etc", "status", "notes")

def _parse_swarm_lane_rows(text: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line.startswith("|") or re.match(r"^\|\s*(Date\s*\||[-: ]+\|)", line, re.IGNORECASE):
            continue
        parts = [part.strip() for part in line.strip("|").split("|")]
        if len(parts) < 12:
            continue
        row = dict(zip(_LANE_KEYS, parts))
        row["status"] = row["status"].upper()
        rows.append(row)
    return rows

def _normalize_frontier_id(frontier_id: str) -> str:
    return (frontier_id or "").strip().upper()

def _sorted_frontier_ids(frontier_ids: set[str]) -> list[str]:
    def _id_key(frontier_id: str) -> tuple[int, str]:
        num = re.search(r"\d+", frontier_id or "")
        return (int(num.group(0)) if num else 10 ** 9, frontier_id)

    return sorted(frontier_ids, key=_id_key)

def _extract_markdown_section(text: str, heading_pattern: str) -> str | None:
    heading = re.search(rf"^##\s*{heading_pattern}\b.*$", text, re.IGNORECASE | re.MULTILINE)
    if not heading:
        return None
    start = heading.end()
    tail = text[start:]
    next_heading = re.search(r"^##\s+\S", tail, re.MULTILINE)
    return tail[:next_heading.start()] if next_heading else tail

def _extract_domain_frontier_active_ids(frontier_text: str) -> tuple[set[str], bool]:
    section = _extract_markdown_section(frontier_text, "Active")
    if section is None:
        return set(), False

    active_ids: set[str] = set()
    for line in section.splitlines():
        if "~~" in line and "**F" in line.upper():
            continue
        match = DOMAIN_ACTIVE_BULLET_RE.match(line)
        if match:
            active_ids.add(_normalize_frontier_id(match.group(1)))
    return active_ids, True

def _parse_domain_frontier_active_count(frontier_text: str) -> int | None:
    match = re.search(r"\bActive:\s*(\d+)\b", frontier_text)
    return int(match.group(1)) if match else None

def _parse_domain_index_active_count(index_text: str) -> int | None:
    for line in index_text.splitlines():
        if not re.search(r"active frontiers?", line, re.IGNORECASE):
            continue
        match = re.search(r"\b(\d+)\s+active\b", line, re.IGNORECASE)
        if match:
            return int(match.group(1))
        match = re.search(r":\s*(\d+)\b", line)
        if match:
            return int(match.group(1))
    return None

def _parse_domain_index_active_line_ids(index_text: str) -> set[str] | None:
    for line in index_text.splitlines():
        if not re.search(r"active frontiers?", line, re.IGNORECASE):
            continue
        paren = re.search(r"\(([^)]*)\)", line)
        if not paren:
            continue
        body = paren.group(1)
        if "–" in body or "..." in body or re.search(r"\bto\b", body, re.IGNORECASE):
            continue
        ids = {_normalize_frontier_id(m.group(1)) for m in DOMAIN_FRONTIER_ID_RE.finditer(body)}
        if ids:
            return ids
    return None

def _parse_domain_index_open_ids(index_text: str) -> tuple[bool, set[str]]:
    section = _extract_markdown_section(index_text, r"What(?:['’]s| is)\s+open")
    if section is None:
        return False, set()
    ids: set[str] = set()
    for line in section.splitlines():
        if "~~" in line and "**F" in line.upper():
            continue
        match = DOMAIN_ACTIVE_BULLET_RE.match(line)
        if match:
            ids.add(_normalize_frontier_id(match.group(1)))
    return True, ids

def _format_frontier_id_diff(expected: set[str], actual: set[str]) -> str:
    missing = _sorted_frontier_ids(expected - actual)
    extra = _sorted_frontier_ids(actual - expected)
    parts: list[str] = []
    if missing:
        parts.append(f"missing {_truncated(missing, 4)}")
    if extra:
        parts.append(f"extra {_truncated(extra, 4)}")
    return "; ".join(parts) if parts else "matched"

def _reason_action_evidence_sessions(
    text: str,
    reason_patterns: tuple[str, ...],
    action_patterns: tuple[str, ...],
) -> list[int]:
    sessions: list[int] = []
    current_session: int | None = None
    current_lines: list[str] = []
    entries: list[tuple[int, str]] = []

    def flush_entry() -> None:
        nonlocal current_session, current_lines
        if current_session is not None and current_lines:
            entries.append((current_session, "\n".join(current_lines)))
        current_session = None
        current_lines = []

    for raw in (text or "").splitlines():
        line = raw.strip()
        if not line:
            flush_entry()
            continue
        m = re.search(r"\bS(\d+)\b", line)
        if m:
            flush_entry()
            current_session = int(m.group(1))
            current_lines = [line]
            continue
        if current_session is not None:
            current_lines.append(line)

    flush_entry()

    for session, entry_text in entries:
        if (any(re.search(p, entry_text, re.IGNORECASE) for p in reason_patterns)
                and any(re.search(p, entry_text, re.IGNORECASE) for p in action_patterns)):
            sessions.append(session)
    return sessions

def _iter_utility_citation_files() -> list[Path]:
    def _accept(rel: str, path: Path) -> bool:
        if any(rel.startswith(prefix) for prefix in UTILITY_CITATION_SKIP_PREFIXES):
            return False
        try:
            return path.exists() and path.is_file() and path.stat().st_size <= UTILITY_CITATION_MAX_BYTES
        except Exception:
            return False

    tracked = _git("ls-files", "*.md", "*.py", "*.json")
    if tracked:
        files: list[Path] = []
        for rel in tracked.splitlines():
            rel = rel.strip().replace("\\", "/")
            if rel and _accept(rel, REPO_ROOT / rel):
                files.append(REPO_ROOT / rel)
        return files

    files: list[Path] = []
    for ext in ("*.md", "*.py", "*.json"):
        for path in REPO_ROOT.rglob(ext):
            if _accept(path.relative_to(REPO_ROOT).as_posix(), path):
                files.append(path)
    return files

def check_unpushed() -> list[tuple[str, str]]:
    ahead = _git("rev-list", "--count", "@{upstream}..HEAD")
    if not (ahead and ahead.isdigit() and int(ahead) > 0):
        return []
    n = int(ahead)
    items = [(("URGENT" if n >= 10 else "DUE" if n >= 5 else "NOTICE"), f"{n} unpushed commits — git push")]
    if n >= 20:
        items.append(("URGENT", "Commit saturation (>=20 unpushed) — run: python3 tools/agent_swarm.py create <child> \"reduce commit backlog\" --personality commit-swarmer"))
    return items

def _parse_kill_switch() -> dict[str, str]:
    if not KILL_SWITCH_PATH.exists():
        return {}
    text = _read(KILL_SWITCH_PATH)
    fields: dict[str, str] = {}
    for line in text.splitlines():
        m = re.match(r"^\s*([A-Za-z][A-Za-z0-9_-]*)\s*:\s*(.*?)\s*$", line)
        if not m:
            continue
        fields[m.group(1).strip().lower()] = m.group(2).strip()
    return fields

def check_kill_switch() -> list[tuple[str, str]]:
    results: list[tuple[str, str]] = []
    if (os.environ.get("SWARM_STOP", "") or "").strip().lower() in {"1", "true", "yes", "on"}:
        return [("URGENT", "SWARM_STOP env var is active — halt swarm activity")]
    fields = _parse_kill_switch()
    if not fields:
        if KILL_SWITCH_PATH.exists():
            results.append(("DUE", "Kill switch file exists but no parseable key/value fields were found"))
        return results
    missing_required = [k for k in ("status", "mode", "reason", "requested_by", "since") if not (fields.get(k, "") or "").strip()]
    if missing_required:
        return [("DUE", f"Kill switch missing required field(s): {', '.join(missing_required)}")]
    status = (fields.get("status", "") or "").strip().lower()
    if status in {"inactive", "off", "false", "0"}:
        return results
    if status not in {"active", "on", "true", "1"}:
        return [("DUE", f"Kill switch status is invalid: {fields.get('status', '')}")]
    mode = (fields.get("mode", "halt") or "halt").strip()
    if mode.lower() not in {"halt", "shutdown-request"}:
        return [("DUE", f"Kill switch mode is invalid: {mode}")]
    reason = (fields.get("reason", "unspecified") or "unspecified").strip()
    requested_by = (fields.get("requested_by", "unknown") or "unknown").strip()
    since = (fields.get("since", "") or "").strip()
    ctx = f"mode={mode}, requested_by={requested_by}, reason={reason}" + (f", since={since}" if since else "")
    results.append(("URGENT", f"Kill switch ACTIVE — {ctx}"))
    if mode.lower() == "shutdown-request":
        results.append(("NOTICE", "Shutdown request is declarative only; execute shutdown manually with explicit human confirmation"))
    return results

def check_uncommitted() -> list[tuple[str, str]]:
    results = []
    status = _git("-c", "core.quotepath=false", "status", "--porcelain")
    if status:
        lines = [l for l in status.splitlines() if l.strip()]
        tracked = [l for l in lines if not l.startswith("??")]
        wsl_suppressed_crlf = 0
        wsl_suppressed_claude = 0

        if tracked and _is_wsl_mnt_repo():
            def _numstat_paths(*args: str) -> set[str]:
                paths: set[str] = set()
                raw = _git("diff", *args, "--numstat", "--ignore-cr-at-eol")
                for row in raw.splitlines():
                    parts = row.split("\t")
                    if len(parts) < 3:
                        continue
                    path = parts[-1].strip()
                    if not path:
                        continue
                    paths.add(path.replace("\\", "/"))
                return paths

            substantive = _numstat_paths() | _numstat_paths("--cached")

            filtered = []
            suppressed = 0
            for line in tracked:
                status_code = line[:2]
                path = _status_path(line)
                structural = any(ch in status_code for ch in "ADRCU")
                if structural or path in substantive:
                    filtered.append(line)
                else:
                    suppressed += 1
            if suppressed > 0:
                tracked = filtered
                wsl_suppressed_crlf = suppressed

            wsl_hidden = []
            filtered = []
            for line in tracked:
                status_code = line[:2]
                path = _status_path(line)
                is_delete = "D" in status_code and not any(ch in status_code for ch in "ARCU")
                if is_delete and path.startswith(".claude/"):
                    wsl_hidden.append(path)
                    continue
                filtered.append(line)
            if wsl_hidden:
                tracked = filtered
                wsl_suppressed_claude = len(wsl_hidden)

        untracked = [l for l in lines if l.startswith("??")]
        def _is_ephemeral_parent_child_artifact(path: str) -> bool:
            p = path.replace("\\", "/")
            return bool(re.search(r"AppData/?Local/?Temp/?tmp[^/]*parent-child/?$", p, re.IGNORECASE))

        untracked_paths = [_status_path(l) for l in untracked]
        untracked_actionable = [
            p for p in untracked_paths
            if not (
                (p.startswith("workspace/notes/wiki-swarm-") and p.endswith(".md"))
                or re.fullmatch(r"memory/lessons/L-\d+\.md", p)
                or _is_ephemeral_parent_child_artifact(p)
                or p in IGNORED_UNTRACKED_RUNTIME_FILES
            )
        ]
        if tracked:
            tracked_paths = [_status_path(l) for l in tracked]
            portability_suffix = ""
            if _is_wsl_mnt_repo():
                filter_parts = []
                if wsl_suppressed_crlf:
                    filter_parts.append(f"{wsl_suppressed_crlf} CRLF-only")
                if wsl_suppressed_claude:
                    filter_parts.append(f"{wsl_suppressed_claude} .claude")
                if filter_parts:
                    portability_suffix = f" (WSL filtered: {', '.join(filter_parts)})"
            results.append(("NOTICE", f"{len(tracked)} tracked file(s) uncommitted: {_truncated(tracked_paths)}{portability_suffix}"))
        if untracked_actionable:
            results.append(("NOTICE", f"{len(untracked_actionable)} untracked file(s): {_truncated(untracked_actionable)} (stage if intentional, or ignore via .gitignore)"))
    return results

def check_open_challenges() -> list[tuple[str, str]]:
    results = []
    n = len(re.findall(r"\|\s*OPEN\s*\|", _read(REPO_ROOT / "beliefs" / "CHALLENGES.md"), re.IGNORECASE))
    if n: results.append(("DUE", f"{n} open challenge(s) in CHALLENGES.md"))
    pt = _read(REPO_ROOT / "beliefs" / "PHILOSOPHY.md")
    ps = pt[pt.find("## Challenges"):] if "## Challenges" in pt else ""
    n = len(re.findall(r"\|\s*open\s*\|", ps, re.IGNORECASE))
    if n: results.append(("DUE", f"{n} open PHIL challenge(s)"))
    return results

def check_human_queue() -> list[tuple[str, str]]:
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
        heading = line[4:].strip()
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
            if not re.search(r"\*\*(Asked|Date)\*\*:", body, re.IGNORECASE):
                missing_metadata.append(hq_id)

    if open_items:
        results.append(("NOTICE", f"{len(open_items)} open HUMAN-QUEUE item(s)"))

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
        results.append(("NOTICE", f"{len(missing_metadata)} HUMAN-QUEUE item(s) missing ask metadata: {', '.join(missing_metadata[:5])}"))

    return results

def check_swarm_lanes() -> list[tuple[str, str]]:
    results = []
    lanes_text = _read(REPO_ROOT / "tasks" / "SWARM-LANES.md")
    if not lanes_text:
        return results

    rows = _parse_swarm_lane_rows(lanes_text)
    if not rows:
        return results

    latest_by_lane: dict[str, dict[str, str]] = {}
    for row in rows:
        lane = row.get("lane", "").strip()
        if not lane:
            continue
        latest_by_lane[lane] = row

    active = [
        row for row in latest_by_lane.values()
        if row.get("status", "").upper() in LANE_ACTIVE_STATUSES
    ]
    if not active:
        return results

    current_session = _session_number()
    stale_notice: list[str] = []
    stale_due: list[str] = []
    if current_session > 0:
        for row in active:
            lane = row.get("lane", "").strip() or "<unknown>"
            session_raw = row.get("session", "")
            m = re.search(r"S(\d+)", session_raw)
            if not m:
                continue
            lane_session = int(m.group(1))
            age = current_session - lane_session
            if age > LANE_STALE_DUE_SESSIONS:
                stale_due.append(f"{lane}(S{lane_session},+{age})")
            elif age > LANE_STALE_NOTICE_SESSIONS:
                stale_notice.append(f"{lane}(S{lane_session},+{age})")
    if stale_due:
        results.append(("DUE", f"{len(stale_due)} active lane(s) stale >{LANE_STALE_DUE_SESSIONS} sessions: {_truncated(stale_due, 5)}"))
    if stale_notice:
        results.append(("NOTICE", f"{len(stale_notice)} active lane(s) stale >{LANE_STALE_NOTICE_SESSIONS} sessions: {_truncated(stale_notice, 5)}"))

    # Anti-windup: active lanes that have been re-queued >= LANE_ANTIWINDUP_ROWS times
    row_counts: dict[str, int] = {}
    for row in rows:
        lane = row.get("lane", "").strip()
        if lane:
            row_counts[lane] = row_counts.get(lane, 0) + 1
    antiwindup: list[str] = []
    for row in active:
        lane = row.get("lane", "").strip() or "<unknown>"
        count = row_counts.get(lane, 0)
        if count >= LANE_ANTIWINDUP_ROWS:
            antiwindup.append(f"{lane}({count}rows)")
    if antiwindup:
        results.append(("NOTICE", f"{len(antiwindup)} active lane(s) with >={LANE_ANTIWINDUP_ROWS} total rows (anti-windup, consider ABANDONED): {_truncated(antiwindup, 5)}"))

    # Check only the LATEST active row per lane (rows appended in order; last = most recent)
    latest_active: dict[str, dict] = {}
    for row in active:
        latest_active[row.get("lane", "")] = row
    missing_meta: list[str] = []
    for row in sorted(latest_active.values(), key=lambda item: item.get("lane", "")):
        missing = []
        for key, label in (("branch", "branch"), ("model", "model"), ("platform", "platform"), ("scope_key", "scope")):
            if _is_lane_placeholder(row.get(key, "")):
                missing.append(label)
        if missing:
            missing_meta.append(f"{row.get('lane')}({','.join(missing)})")
    if missing_meta:
        results.append(("NOTICE", f"{len(missing_meta)} active lane(s) missing metadata: {_truncated(missing_meta, 5)}"))

    missing_coordination_tags: list[str] = []
    missing_domain_memory_tags: list[str] = []
    invalid_domain_sync_tags: list[str] = []
    invalid_available_tags: list[str] = []
    legacy_available_tags: list[str] = []
    high_risk_missing_human: list[str] = []
    setup_values: set[str] = set()
    has_global_focus = False
    for row in active:
        lane = row.get("lane", "").strip() or "<unknown>"
        tags = _parse_lane_tags(row.get("etc", ""))
        domain_focus = _lane_domain_focus(row, tags)
        if domain_focus:
            domain_missing = []
            domain_sync = tags.get("domain_sync", "").strip().lower()
            memory_target = tags.get("memory_target", "").strip().lower()
            if _is_lane_placeholder(domain_sync):
                domain_missing.append("domain_sync")
            elif domain_sync not in DOMAIN_SYNC_ALLOWED_VALUES:
                invalid_domain_sync_tags.append(f"{lane}(domain_sync={domain_sync})")
            if _is_lane_placeholder(memory_target):
                domain_missing.append("memory_target")
            if domain_missing:
                missing_domain_memory_tags.append(f"{lane}({','.join(domain_missing)})")
        missing = []
        for key in ("setup", "focus"):
            if _is_lane_placeholder(tags.get(key, "")):
                missing.append(key)
        if not any(k in tags for k in ("available", "capacity", "availability", "ready")):
            missing.append("available")
        if not any(k in tags for k in ("blocked", "blocker")):
            missing.append("blocked")
        if not any(k in tags for k in ("next_step", "next", "action", "plan")):
            missing.append("next_step")
        if not any(k in tags for k in ("human_open_item", "human_open")):
            missing.append("human_open_item")
        if missing:
            missing_coordination_tags.append(f"{lane}({','.join(missing)})")
            continue

        human_open_value = (tags.get("human_open_item", "") or tags.get("human_open", "")).strip().lower()
        high_risk_signal = _lane_high_risk_signal(row, tags)
        if high_risk_signal and _is_lane_placeholder(human_open_value):
            high_risk_missing_human.append(f"{lane}({high_risk_signal})")

        available_raw = (tags.get("available", "") or "").strip().lower()
        if available_raw:
            if available_raw in LANE_AVAILABLE_LEGACY_MAP:
                canonical = LANE_AVAILABLE_LEGACY_MAP[available_raw]
                legacy_available_tags.append(f"{lane}(available={available_raw}->{canonical})")
            elif available_raw not in LANE_AVAILABLE_ALLOWED_VALUES:
                invalid_available_tags.append(f"{lane}(available={available_raw})")

        setup_value = tags.get("setup", "").strip().lower()
        focus_value = tags.get("focus", "").strip().lower()
        setup_values.add(setup_value)
        if focus_value in LANE_GLOBAL_FOCUS_VALUES:
            has_global_focus = True

    if missing_coordination_tags:
        results.append(("DUE", f"{len(missing_coordination_tags)} active lane(s) missing coordination contract tags (setup/focus/available/blocked/next_step/human_open_item): {_truncated(missing_coordination_tags, 5)}"))
    if missing_domain_memory_tags:
        results.append(("DUE", f"{len(missing_domain_memory_tags)} active domain-focused lane(s) missing domain-memory coordination tags (domain_sync/memory_target): {_truncated(missing_domain_memory_tags, 5)}"))
    if invalid_domain_sync_tags:
        results.append(("NOTICE", f"{len(invalid_domain_sync_tags)} active domain-focused lane(s) with invalid domain_sync value (allowed: {','.join(sorted(DOMAIN_SYNC_ALLOWED_VALUES))}): {_truncated(invalid_domain_sync_tags, 5)}"))
    if invalid_available_tags:
        results.append(("DUE", f"{len(invalid_available_tags)} active lane(s) with invalid available value (allowed: {','.join(sorted(LANE_AVAILABLE_ALLOWED_VALUES))}): {_truncated(invalid_available_tags, 5)}"))
    if legacy_available_tags:
        results.append(("NOTICE", f"{len(legacy_available_tags)} active lane(s) using legacy available value (normalize to {','.join(sorted(LANE_AVAILABLE_ALLOWED_VALUES))}): {_truncated(legacy_available_tags, 5)}"))
    if high_risk_missing_human:
        results.append(("DUE", f"{len(high_risk_missing_human)} active lane(s) declare high-risk intent without `human_open_item=HQ-N` (MC-SAFE): {_truncated(high_risk_missing_human, 5)}"))

    missing_evidence_tags: list[str] = []
    for row in active:
        lane = row.get("lane", "").strip() or "<unknown>"
        tags = _parse_lane_tags(row.get("etc", ""))
        missing_ev = [k for k in ("expect", "artifact") if not tags.get(k, "").strip()]
        if missing_ev:
            missing_evidence_tags.append(f"{lane}({','.join(missing_ev)})")
    if missing_evidence_tags:
        results.append(("NOTICE", f"{len(missing_evidence_tags)} active lane(s) missing evidence fields (expect/artifact — use open_lane.py, F-META1 S331): {_truncated(missing_evidence_tags, 5)}"))

    if len(setup_values) > 1 and not has_global_focus:
        results.append(("NOTICE", "Multi-setup active lanes have no global coordination focus (`focus=global|system|coordination`) in Etc"))

    # Branch values that are non-collidable trunk names (all sessions share them)
    _TRUNK_BRANCHES = {"master", "main"}

    def _detect_collisions(key_field: str, label: str) -> None:
        mapping: dict[str, set[str]] = {}
        for row in active:
            lane = row.get("lane", "")
            val = row.get(key_field, "").strip().lower()
            if not _is_lane_placeholder(val) and val not in _TRUNK_BRANCHES:
                mapping.setdefault(val, set()).add(lane)
        conflicts = sorted((k, sorted(v)) for k, v in mapping.items() if len(v) > 1)
        if conflicts:
            sample = "; ".join(f"{k}:{'/'.join(v[:3])}" for k, v in conflicts[:3])
            results.append(("DUE", f"Active lane {label} collision(s): {sample}"))

    _detect_collisions("branch", "branch")
    _detect_collisions("scope_key", "scope")

    return results

def check_swarm_coordinator() -> list[tuple[str, str]]:
    results: list[tuple[str, str]] = []
    lanes_text = _read(REPO_ROOT / "tasks" / "SWARM-LANES.md")
    if not lanes_text:
        return results

    rows = _parse_swarm_lane_rows(lanes_text)
    if not rows:
        return results

    latest_by_lane: dict[str, dict[str, str]] = {}
    for row in rows:
        lane = row.get("lane", "").strip()
        if lane:
            latest_by_lane[lane] = row

    active = [
        row for row in latest_by_lane.values()
        if row.get("status", "").upper() in LANE_ACTIVE_STATUSES
    ]
    if len(active) < 2:
        return results

    dispatch_rows: list[tuple[dict[str, str], dict[str, str]]] = []
    coordinator_rows: list[tuple[dict[str, str], dict[str, str]]] = []
    for row in active:
        tags = _parse_lane_tags(row.get("etc", ""))
        if _is_dispatch_lane_row(row, tags):
            dispatch_rows.append((row, tags))
        if _is_coordinator_lane_row(row, tags):
            coordinator_rows.append((row, tags))

    # Single dispatch lane can run without a dedicated coordinator row; fan-out swarms cannot.
    if len(dispatch_rows) < 2:
        return results

    if not coordinator_rows:
        dispatch_lanes = [row.get("lane", "").strip() or "<unknown>" for row, _ in dispatch_rows]
        results.append(("DUE", f"{len(dispatch_rows)} active dispatch lane(s) have no active coordinator lane: {_truncated(dispatch_lanes, 5)}"))
        return results

    missing_contract: list[str] = []
    for row, tags in coordinator_rows:
        lane = row.get("lane", "").strip() or "<unknown>"
        missing: list[str] = []
        if tags.get("focus", "").strip().lower() not in LANE_GLOBAL_FOCUS_VALUES: missing.append("focus")
        if not _lane_has_any_tag(tags, ("intent", "objective", "goal")): missing.append("intent")
        if not _lane_has_any_tag(tags, ("progress", "status_note", "evidence", "artifact")): missing.append("progress")
        if not _lane_has_any_tag(tags, ("available", "capacity", "availability", "ready")): missing.append("available")
        if not _lane_has_any_tag(tags, ("blocked", "blocker")): missing.append("blocked")
        if not _lane_has_any_tag(tags, ("next_step", "next", "action", "plan")): missing.append("next_step")
        if not _lane_has_any_tag(tags, ("human_open_item", "human_open")): missing.append("human_open_item")
        if not _lane_has_any_tag(tags, ("check_focus",)): missing.append("check_focus")
        if missing: missing_contract.append(f"{lane}({','.join(missing)})")

    if missing_contract:
        results.append(("DUE", f"{len(missing_contract)} coordinator lane(s) missing coordinator contract fields (focus,intent,progress,available,blocked,next_step,human_open_item,check_focus): {_truncated(missing_contract, 5)}"))

    return results

def check_lane_reporting_quality() -> list[tuple[str, str]]:
    results: list[tuple[str, str]] = []
    lanes_text = _read(REPO_ROOT / "tasks" / "SWARM-LANES.md")
    if not lanes_text:
        return results

    rows = _parse_swarm_lane_rows(lanes_text)
    if not rows:
        return results

    latest_by_lane: dict[str, dict[str, str]] = {}
    for row in rows:
        lane = row.get("lane", "").strip()
        if lane:
            latest_by_lane[lane] = row

    active = [
        row for row in latest_by_lane.values()
        if row.get("status", "").upper() in LANE_ACTIVE_STATUSES
    ]
    if not active:
        return results

    missing_contract: list[str] = []
    missing_historian_contract: list[str] = []
    explicit_counts = {key: 0 for key in LANE_REPORT_KEYS}
    dispatchable = 0

    for row in sorted(active, key=lambda item: item.get("lane", "")):
        lane = row.get("lane", "").strip() or "<unknown>"
        tags = _parse_lane_tags(row.get("etc", ""))

        fields = {
            "capabilities": (
                not _is_lane_placeholder(row.get("model", ""))
                and not _is_lane_placeholder(row.get("platform", ""))
                and not _is_lane_placeholder(tags.get("setup", ""))
            ),
            "intent": any(k in tags for k in ("intent", "objective", "goal", "frontier", "dispatch", "task")),
            "progress": any(k in tags for k in ("progress", "status_note", "evidence", "artifact")),
            "available": any(k in tags for k in ("available", "capacity", "availability", "ready")),
            "blocked": "blocked" in tags or "blocker" in tags,
            "next_step": any(k in tags for k in ("next_step", "next", "action", "plan")),
            "human_open_item": "human_open_item" in tags or "human_open" in tags,
        }

        missing = [key for key in LANE_REPORT_KEYS if not fields[key]]
        if missing:
            missing_contract.append(f"{lane}({','.join(missing)})")
        else:
            dispatchable += 1
        for key, present in fields.items():
            if present:
                explicit_counts[key] += 1

        check_modes = _parse_check_focus_modes(tags.get("check_focus", ""))
        if check_modes & CHECK_FOCUS_HISTORIAN_REQUIRED:
            if "objective" in check_modes and _is_lane_placeholder(tags.get("objective_check", "")):
                missing_historian_contract.append(f"{lane}(objective_check)")
            historian_raw = tags.get("historian_check", "")
            if _is_lane_placeholder(historian_raw):
                missing_historian_contract.append(f"{lane}(historian_check)")
            else:
                has_self, has_surroundings = _historian_anchor_coverage(historian_raw)
                anchor_missing: list[str] = []
                if not has_self:
                    anchor_missing.append("self_anchor")
                if not has_surroundings:
                    anchor_missing.append("surroundings_anchor")
                if anchor_missing:
                    missing_historian_contract.append(f"{lane}({','.join(anchor_missing)})")

    lane_count = len(active)
    dispatchable_rate = dispatchable / lane_count if lane_count else 0.0
    if missing_contract:
        severity = "DUE" if dispatchable_rate < 0.5 else "NOTICE"
        results.append((severity, f"{len(missing_contract)} active lane(s) missing explicit reporting contract fields ({dispatchable}/{lane_count} dispatchable): {_truncated(missing_contract, 5)}"))
        weakest = sorted(explicit_counts.items(), key=lambda item: (item[1], item[0]))[:3]
        if weakest:
            results.append(("NOTICE", f"Lane explicit-reporting weakest keys: {', '.join(f'{k}={c}/{lane_count}' for k, c in weakest)}"))

    if missing_historian_contract:
        results.append(("DUE", f"{len(missing_historian_contract)} active lane(s) with historian/objective check focus missing historian grounding (self+surroundings anchors): {_truncated(missing_historian_contract, 5)}"))

    return results

def check_github_swarm_intake() -> list[tuple[str, str]]:
    results: list[tuple[str, str]] = []
    mission_path = REPO_ROOT / ".github" / "ISSUE_TEMPLATE" / "swarm-mission.yml"
    blocker_path = REPO_ROOT / ".github" / "ISSUE_TEMPLATE" / "swarm-blocker.yml"
    workflow_path = REPO_ROOT / ".github" / "workflows" / "swarm-pr-intake.yml"

    missing_paths = [
        str(path.relative_to(REPO_ROOT)).replace("\\", "/")
        for path in (mission_path, blocker_path, workflow_path)
        if not path.exists()
    ]
    if missing_paths:
        results.append(("DUE", f"GitHub swarm intake file(s) missing: {_truncated(missing_paths)}"))
        return results

    def _check_template(path: Path, label: str, required_ids: set[str]) -> None:
        text = _read(path)
        ids = re.findall(r"^\s*id:\s*([A-Za-z0-9_-]+)\s*$", text, re.MULTILINE)
        if not ids:
            results.append(("NOTICE", f"{label} has no parsed input ids"))
            return

        counts: dict[str, int] = {}
        for item in ids:
            counts[item] = counts.get(item, 0) + 1
        duplicate_ids = sorted(k for k, v in counts.items() if v > 1)
        if duplicate_ids:
            results.append(("DUE", f"{label} duplicate id(s): {_truncated(duplicate_ids)}"))

        missing_ids = sorted(required_ids - set(ids))
        if missing_ids:
            results.append(("DUE", f"{label} missing core-alignment id(s): {_truncated(missing_ids)}"))

    _check_template(
        mission_path,
        "swarm-mission template",
        {
            "objective",
            "expectation",
            "diff_signal",
            "scope",
            "acceptance",
            "state_sync",
            "available",
            "blocked",
            "human_open_item",
        },
    )
    _check_template(
        blocker_path,
        "swarm-blocker template",
        {
            "blocker",
            "unblocking_ask",
            "state_sync",
            "available",
            "blocked",
            "human_open_item",
        },
    )

    workflow_text = _read(workflow_path)
    for snippet in ("tools/swarm_pr.py plan", "<!-- swarm-pr-plan -->", "Swarm Intake Plan"):
        if snippet not in workflow_text:
            results.append(("NOTICE", f"swarm-pr-intake workflow missing marker: {snippet}"))

    return results

def check_child_bulletins() -> list[tuple[str, str]]:
    results = []
    bulletin_dir = REPO_ROOT / "experiments" / "inter-swarm" / "bulletins"
    integration_dir = REPO_ROOT / "experiments" / "integration-log"
    children_dir = REPO_ROOT / "experiments" / "children"
    if not bulletin_dir.exists(): return results
    integrated = {f.stem for f in integration_dir.glob("*.json")} if integration_dir.exists() else set()
    known_children = {d.name for d in children_dir.iterdir() if d.is_dir()} if children_dir.exists() else set()
    unprocessed, stale, external = [], [], []
    for f in bulletin_dir.glob("*.md"):
        name = f.stem
        if name not in known_children and name not in integrated: external.append(name); continue
        if name in integrated: stale.append(name)
        elif "<!-- PROCESSED" not in _read(f): unprocessed.append(name)
    if unprocessed: results.append(("DUE", f"{len(unprocessed)} unprocessed bulletin(s): {', '.join(unprocessed[:5])}"))
    if stale: results.append(("NOTICE", f"{len(stale)} stale bulletin(s): {', '.join(stale[:5])}"))
    if external: results.append(("NOTICE", f"{len(external)} external bulletin file(s) ignored: {', '.join(external[:5])}"))
    return results

def check_help_requests() -> list[tuple[str, str]]:
    bulletin_dir = REPO_ROOT / "experiments" / "inter-swarm" / "bulletins"
    if not bulletin_dir.exists(): return []
    req_re = re.compile(r"Type:\s*help-request.*?Request-ID:\s*(\S+)", re.DOTALL)
    resp_re = re.compile(r"Type:\s*help-response.*?Request-ID:\s*(\S+)", re.DOTALL)
    open_ids: set[str] = set()
    responses: set[str] = set()
    for f in bulletin_dir.glob("*.md"):
        text = _read(f)
        open_ids |= {m.group(1).strip() for m in req_re.finditer(text)}
        responses |= {m.group(1).strip() for m in resp_re.finditer(text)}
    remaining = sorted(open_ids - responses)
    if remaining:
        return [("DUE", f"{len(remaining)} open help request(s): {_truncated(remaining)}; respond with `{PYTHON_CMD} tools/bulletin.py offer-help ...`")]
    return []

def check_compaction() -> list[tuple[str, str]]:
    results = []
    idx = _line_count(REPO_ROOT / "memory" / "INDEX.md")
    if idx > 60: results.append(("DUE", f"INDEX.md is {idx} lines (>60)"))
    mandatory = sum(_line_count(REPO_ROOT / p) for p in [Path("CLAUDE.md"), Path("beliefs") / "CORE.md", Path("memory") / "INDEX.md"])
    if mandatory > 200: results.append(("DUE", f"Mandatory load is {mandatory} lines (>200)"))
    return results

def check_lessons() -> list[tuple[str, str]]:
    results = []
    lessons_dir = REPO_ROOT / "memory" / "lessons"
    if not lessons_dir.exists():
        return results

    lessons = list(lessons_dir.glob("L-*.md"))

    over_20 = []
    for f in lessons:
        if _line_count(f) > 20:
            over_20.append(f.name)
    if over_20:
        results.append(("DUE", f"{len(over_20)} lesson(s) over 20 lines: {', '.join(over_20[:5])}"))

    return results

T4_TOOL_TOKEN_WARN = 5_000    # warn above this (chars//4); L-469 finding

def check_t4_tool_size() -> list[tuple[str, str]]:
    """Flag T4-tools files over token ceiling (anti-cascade L-469)."""
    results = []
    tools_dir = REPO_ROOT / "tools"
    if not tools_dir.exists():
        return results
    oversized = []
    for f in sorted(tools_dir.glob("*.py")):
        try:
            tokens = len(f.read_text(encoding="utf-8", errors="replace")) // 4
            if tokens > T4_TOOL_TOKEN_WARN:
                oversized.append((f.name, tokens))
        except Exception:
            continue
    if oversized:
        names = ", ".join(f"{n}({t}t)" for n, t in sorted(oversized, key=lambda x: -x[1])[:4])
        results.append(("NOTICE", f"T4 anti-cascade: {len(oversized)} tool(s) exceed {T4_TOOL_TOKEN_WARN}t ceiling: {names}"))
    return results

def check_frontier_decay() -> list[tuple[str, str]]:
    results = []
    frontier_path = REPO_ROOT / "tasks" / "FRONTIER.md"
    decay_file = REPO_ROOT / "experiments" / "frontier-decay.json"
    if not frontier_path.exists():
        return results

    text = _read(frontier_path)
    open_text = text.split("## Archive", 1)[0]
    try: decay = json.loads(_read(decay_file)) if decay_file.exists() else {}
    except Exception: decay = {}

    open_ids = {f"F{m.group(1)}" for m in re.finditer(r"^- \*\*F(\d+)\*\*:", open_text, re.MULTILINE)}
    for fid in open_ids:
        decay.setdefault(fid, {"last_active": date.today().isoformat()})
    try:
        decay_file.parent.mkdir(parents=True, exist_ok=True)
        decay_file.write_text(json.dumps(decay, indent=2))
    except Exception:
        pass

    today = date.today()
    weak, archive = [], []
    for fid in sorted(open_ids):
        meta = decay.get(fid, {})
        last = meta.get("last_active", today.isoformat())
        try:
            strength = 0.9 ** ((today - date.fromisoformat(last)).days)
        except Exception:
            strength = 1.0
        if strength < 0.1:
            archive.append(fid)
        elif strength < 0.3:
            weak.append(fid)

    if archive:
        results.append(("DUE", f"{len(archive)} frontier(s) below archive threshold: {', '.join(archive)}"))
    if weak:
        results.append(("NOTICE", f"{len(weak)} frontier(s) weakening: {', '.join(weak)}"))
    return results

def check_anxiety_zones() -> list[tuple[str, str]]:
    results = []
    current = _session_number()
    ANXIETY_THRESHOLD = 15
    frontier_path = REPO_ROOT / "tasks" / "FRONTIER.md"
    if not frontier_path.exists():
        return results
    open_text = _read(frontier_path).split("## Archive", 1)[0]
    anxiety_zones = []
    for match in re.finditer(r"^- \*\*(F[^*]+)\*\*:(.*?)(?=^- \*\*F|\Z)", open_text, re.MULTILINE | re.DOTALL):
        s_nums = [int(m) for m in re.findall(r"\bS(\d+)\b", match.group(2))]
        if not s_nums: continue
        last_active = max(s_nums)
        age = current - last_active
        if age > ANXIETY_THRESHOLD:
            anxiety_zones.append((match.group(1).strip(), last_active, age))
    if anxiety_zones:
        anxiety_zones.sort(key=lambda x: x[2], reverse=True)
        ids = ", ".join(f"{fid}(S{s},+{age})" for fid, s, age in anxiety_zones[:5])
        tail = f"... +{len(anxiety_zones)-5} more" if len(anxiety_zones) > 5 else ""
        results.append(("NOTICE", f"{len(anxiety_zones)} anxiety-zone frontier(s) open >{ANXIETY_THRESHOLD} sessions without update (F-COMM1: auto-trigger multi-expert synthesis): {ids}{tail}"))
    return results


def check_dispatch_log() -> list[tuple[str, str]]:
    results = []
    dispatch_log = REPO_ROOT / "workspace" / "DISPATCH-LOG.md"
    if not dispatch_log.exists():
        return [("NOTICE", "workspace/DISPATCH-LOG.md missing — create with: python3 tools/dispatch_tracker.py init (F-EXP1: dispatch tracking not instrumented)")]
    current = _session_number()
    STALE_THRESHOLD = 3
    stale = []
    for match in re.finditer(r"^\|\s*(S\d+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|", _read(dispatch_log), re.MULTILINE):
        session_str, frontier, status, _ = (match.group(i).strip() for i in range(1, 5))
        if status.lower() != "in-progress": continue
        s_num_match = re.match(r"S(\d+)", session_str)
        if not s_num_match: continue
        age = current - int(s_num_match.group(1))
        if age > STALE_THRESHOLD:
            stale.append((session_str, frontier.strip(), age))
    if stale:
        results.append(("NOTICE", f"{len(stale)} dispatch entry(ies) stale in-progress >{STALE_THRESHOLD} sessions — may be abandoned (F-EXP1 tracking): {', '.join(f'{s}:{f}(+{a})' for s, f, a in stale[:5])}"))
    return results


def check_domain_expert_coverage() -> list[tuple[str, str]]:
    """Every domain with ≥1 active frontier must have ≥1 non-ABANDONED DOMEX lane (L-349, P-185)."""
    results = []
    domains_dir = REPO_ROOT / "domains"
    lanes_path = REPO_ROOT / "tasks" / "SWARM-LANES.md"
    if not domains_dir.exists() or not lanes_path.exists():
        return results

    lanes_text = _read(lanes_path)
    uncovered = []
    for frontier_path in sorted(domains_dir.glob("*/tasks/FRONTIER.md")):
        domain = frontier_path.parts[-3]
        text = _read(frontier_path)
        active_section = text.split("## Resolved", 1)[0].split("## Archive", 1)[0]
        has_active = bool(re.search(r"^\s*[-*]\s*\*\*F", active_section, re.MULTILINE))
        if not has_active:
            continue
        # Check for non-ABANDONED DOMEX lane mentioning this domain
        domex_rows = [r for r in lanes_text.splitlines()
                      if "DOMEX" in r and domain.lower() in r.lower()
                      and "ABANDONED" not in r and "MERGED" not in r]
        if not domex_rows:
            uncovered.append(domain)

    if uncovered:
        results.append(("NOTICE", f"Domain expert coverage gap ({len(uncovered)} domains with active frontiers but no DOMEX lane): {', '.join(uncovered)}"))
    return results


def check_historian_integrity() -> list[tuple[str, str]]:
    """Auto-run historian grounding checks: lane coverage + domain frontier session anchors."""
    results = []

    # --- Part 1: lane grounding score via f_his1 analysis ---
    try:
        import importlib.util as _ilu
        import sys as _sys
        _mod_name = "f_his1_historian_grounding"
        if _mod_name not in _sys.modules:
            _spec = _ilu.spec_from_file_location(_mod_name, REPO_ROOT / "tools" / "f_his1_historian_grounding.py")
            _his1 = _ilu.module_from_spec(_spec)
            _sys.modules[_mod_name] = _his1
            _spec.loader.exec_module(_his1)
        else:
            _his1 = _sys.modules[_mod_name]
        lanes_text = _read(REPO_ROOT / "tasks" / "SWARM-LANES.md")
        rows = _his1.parse_rows(lanes_text)
        analysis = _his1.analyze(rows)
        score = analysis["mean_grounding_score"]
        active = analysis["active_lane_count"]
        if active >= 3 and score < 0.40:
            results.append(("DUE", f"historian grounding low: mean_score={score:.2f} across {active} active lanes (target ≥0.5) — run python3 tools/f_his1_historian_grounding.py"))
        elif active >= 3 and score < 0.60:
            results.append(("NOTICE", f"historian grounding below target: mean_score={score:.2f} across {active} lanes"))
    except Exception as e:
        results.append(("NOTICE", f"check_historian_integrity lane-check error: {e}"))

    # --- Part 2: domain frontier session-anchor coverage (block-level scan) ---
    SESSION_ANCHOR = re.compile(r"\bS\d{2,}\b")
    domains_dir = REPO_ROOT / "domains"
    if not domains_dir.exists():
        return results
    unanchored: list[str] = []
    total_active = 0
    for fp in sorted(domains_dir.glob("*/tasks/FRONTIER.md")):
        domain = fp.parts[-3]
        text = _read(fp)
        active_section = text.split("## Resolved", 1)[0].split("## Archive", 1)[0]
        lines = active_section.splitlines()
        i = 0
        while i < len(lines):
            m = re.match(r"\s*[-*]\s*\*\*(\S+)\*\*", lines[i])
            if m:
                total_active += 1
                # Collect full block until next frontier item or section header
                block = [lines[i]]
                j = i + 1
                while j < len(lines):
                    nxt = lines[j]
                    if re.match(r"\s*[-*]\s*\*\*\S", nxt) or re.match(r"^##", nxt):
                        break
                    block.append(nxt)
                    j += 1
                if not SESSION_ANCHOR.search("\n".join(block)):
                    unanchored.append(f"{domain}:{m.group(1)}")
                i = j
            else:
                i += 1
    if total_active > 0:
        rate = len(unanchored) / total_active
        sample = ", ".join(unanchored[:8])
        if rate > 0.70:
            results.append(("DUE", f"domain frontier historian gap: {len(unanchored)}/{total_active} active frontiers lack session anchor (SNN): {sample}"))
        elif rate > 0.40:
            results.append(("NOTICE", f"domain frontier historian partial: {len(unanchored)}/{total_active} unanchored: {sample}"))

    return results


def check_periodics() -> list[tuple[str, str]]:
    results = []
    periodics_path = REPO_ROOT / "tools" / "periodics.json"
    if not periodics_path.exists():
        return results

    try: data = json.loads(periodics_path.read_text())
    except Exception: return results
    session = _session_number()
    if session <= 0: return results
    dirty = bool(_git("status", "--porcelain"))

    for item in data.get("items", []):
        item_id = item.get("id", "<unknown>")
        description = item.get("description", item_id)
        cadence = item.get("cadence_sessions", 10)
        last = item.get("last_reviewed_session", 0)
        if last > session:
            if not dirty:
                results.append(("NOTICE", f"periodics marker {item_id} S{last} > session log S{session}"))
            continue
        gap = session - last
        if gap >= cadence:
            overdue = gap - cadence
            urgency = "DUE" if overdue > cadence else "PERIODIC"
            results.append((urgency, f"[{item_id}] {description} (every ~{cadence} sessions, last: S{last})"))

    return results

def check_validator() -> list[tuple[str, str]]:
    try:
        r = subprocess.run([PYTHON_EXE, str(REPO_ROOT / "tools" / "validate_beliefs.py"), "--quick"],
                           capture_output=True, text=True, timeout=30)
        return [("URGENT", "validate_beliefs.py FAIL — fix before other work")] if "RESULT: FAIL" in r.stdout else []
    except Exception as e:
        return [("URGENT", f"validate_beliefs.py failed to run: {e}")]

def check_version_drift() -> list[tuple[str, str]]:
    results = []
    meta_path = REPO_ROOT / ".swarm_meta.json"
    if not meta_path.exists(): return results
    try: meta = json.loads(meta_path.read_text())
    except Exception: return results
    for label, fpath, key in [("CLAUDE.md", "CLAUDE.md", "claude_md_version"), ("CORE.md", "beliefs/CORE.md", "core_md_version")]:
        ver = re.search(rf"{key}:\s*([\d.]+)", _read(REPO_ROOT / fpath))
        if ver and meta.get(key) and str(ver.group(1)) != str(meta[key]):
            results.append(("URGENT", f"{label} version {ver.group(1)} != meta {meta[key]} — re-read {label}"))
    return results

def check_runtime_portability() -> list[tuple[str, str]]:
    results = []

    has_git = _command_exists("git")
    has_bash = _command_exists("bash")
    has_pwsh = _command_exists("pwsh") or _command_exists("powershell")
    has_python_alias = _python_command_runs("python3") or _python_command_runs("python") or _py_launcher_runs()
    has_check_wrapper_sh = _exists("tools/check.sh")
    has_maintenance_wrapper_sh = _exists("tools/maintenance.sh")
    has_check_wrapper_ps = _exists("tools/check.ps1")
    has_maintenance_wrapper_ps = _exists("tools/maintenance.ps1")
    has_bash_wrapper_pair = has_check_wrapper_sh and has_maintenance_wrapper_sh
    has_ps_wrapper_pair = has_check_wrapper_ps and has_maintenance_wrapper_ps
    has_bash_wrappers = has_bash and has_bash_wrapper_pair
    has_pwsh_wrappers = has_pwsh and has_ps_wrapper_pair

    if not has_git:
        results.append(("URGENT", "git not found in PATH — swarm memory/commit workflow cannot run"))
    if not has_python_alias:
        if has_bash_wrappers and has_pwsh_wrappers:
            results.append(("NOTICE", "No python alias in active shell; use wrappers (`bash tools/check.sh --quick` or `pwsh -NoProfile -File tools/check.ps1 --quick`)"))
        elif has_bash_wrappers:
            results.append(("NOTICE", "No python alias in active shell; use bash wrappers (`bash tools/check.sh --quick`, `bash tools/maintenance.sh --inventory`)"))
        else:
            results.append(("DUE", f"No python alias in PATH — use explicit interpreter: {PYTHON_EXE}"))
    if not has_bash and (_exists("workspace/genesis.sh") or _exists("tools/check.sh")):
        if has_python_alias and has_pwsh_wrappers:
            results.append(("NOTICE", "bash not found — use PowerShell wrappers (`pwsh -NoProfile -File tools/check.ps1 --quick`, `pwsh -NoProfile -File tools/maintenance.ps1 --inventory`)"))
        elif has_python_alias:
            results.append(("NOTICE", f"bash not found — use direct python entrypoints (`{PYTHON_CMD} tools/maintenance.py --quick`, `{PYTHON_CMD} tools/maintenance.py --inventory`)"))
        else:
            results.append(("DUE", "bash not found and no python alias — portable startup path is broken"))
    if has_bash and not has_maintenance_wrapper_sh:
        results.append(("DUE", "tools/maintenance.sh missing — portable maintenance/inventory path is broken"))
    if has_pwsh and not has_maintenance_wrapper_ps:
        level = "DUE" if not has_bash else "NOTICE"
        results.append((level, "tools/maintenance.ps1 missing — PowerShell maintenance/inventory path is degraded"))

    if _is_wsl_mnt_repo() and not _git("status", "--porcelain"):
        results.append(("NOTICE", "WSL on /mnt/* repo: status/proxy-K may diverge from Windows runtime"))

    if _is_wsl_mnt_repo():  # WSL corruption: .claude/commands/swarm.md may lose permissions or be deleted
        swarm_cmd = REPO_ROOT / ".claude" / "commands" / "swarm.md"
        if not swarm_cmd.exists():
            results.append(("DUE", ".claude/commands/swarm.md DELETED — WSL deletion bug (L-279). Fix: rm -f .claude/commands/swarm.md && git checkout HEAD -- .claude/commands/swarm.md"))
        else:
            try:
                content = swarm_cmd.read_text(encoding="utf-8")
                if "# /swarm" not in content:
                    results.append(("DUE", ".claude/commands/swarm.md exists but has unexpected content — may be corrupted (WSL). Restore: python3 -c \"import os; os.remove('.claude/commands/swarm.md')\" then git show HEAD:.claude/commands/swarm.md > /tmp/s.md && python3 -c \"open('.claude/commands/swarm.md','w').write(open('/tmp/s.md').read())\""))
            except (PermissionError, OSError):
                results.append(("DUE", ".claude/commands/swarm.md inaccessible — WSL permission corruption. Fix: python3 -c \"import os; os.remove('.claude/commands/swarm.md')\" then restore from git show HEAD:.claude/commands/swarm.md"))

    bridges = BRIDGE_FILES
    missing_bridges = [p for p in bridges if not _exists(p)]
    if missing_bridges:
        level = "URGENT" if "SWARM.md" in missing_bridges else "DUE"
        sample = ", ".join(missing_bridges[:3])
        results.append((level, f"{len(missing_bridges)} missing bridge file(s): {sample}"))

    swarm_ref_re = re.compile(r"\bswarm\.md\b", re.IGNORECASE)
    swarm_signal_re = re.compile(r"\bswarm signaling\b", re.IGNORECASE)
    no_ref, no_signal = [], []
    for path in bridges:
        if path == "SWARM.md" or path in missing_bridges:
            continue
        content = _read(REPO_ROOT / path)
        if not swarm_ref_re.search(content):
            no_ref.append(path)
        if not swarm_signal_re.search(content):
            no_signal.append(path)
    if no_ref:
        results.append(("DUE", f"{len(no_ref)} bridge file(s) missing SWARM.md protocol reference: {', '.join(no_ref[:3])}"))
    if "SWARM.md" not in missing_bridges and not swarm_signal_re.search(_read(REPO_ROOT / "SWARM.md")):
        results.append(("DUE", "SWARM.md missing explicit swarm signaling rule"))
    if no_signal:
        results.append(("DUE", f"{len(no_signal)} bridge file(s) missing swarm signaling guidance: {', '.join(no_signal[:3])}"))

    # F-GOV2: required protocol sections in bridge files (L-351)
    min_swarmed_re = re.compile(r"Minimum Swarmed Cycle", re.IGNORECASE)
    no_min_swarmed = []
    for path in bridges:
        if path == "SWARM.md" or path in missing_bridges:
            continue
        content = _read(REPO_ROOT / path)
        if not min_swarmed_re.search(content):
            no_min_swarmed.append(path)
    if no_min_swarmed:
        results.append(("DUE", f"{len(no_min_swarmed)} bridge file(s) missing 'Minimum Swarmed Cycle' section (F-GOV2, L-351): {', '.join(no_min_swarmed[:3])}"))

    return results

def check_commit_hooks() -> list[tuple[str, str]]:
    results = []
    git_dir = REPO_ROOT / ".git"
    if not git_dir.exists(): return results
    hooks_dir = git_dir / "hooks"
    if not hooks_dir.exists(): return [("NOTICE", ".git/hooks missing — commit quality hooks unavailable")]
    expected = [("pre-commit", "tools/pre-commit.hook"), ("commit-msg", "tools/commit-msg.hook")]
    missing_tpl = [tpl for _, tpl in expected if not _exists(tpl)]
    if missing_tpl: return [("DUE", f"Hook template(s) missing: {', '.join(missing_tpl[:3])}")]
    missing_inst, drifted = [], []
    for hook_name, tpl_rel in expected:
        tpl_text = _read(REPO_ROOT / tpl_rel).replace("\r\n", "\n").strip()
        inst_path = hooks_dir / hook_name
        if not inst_path.exists(): missing_inst.append(hook_name); continue
        if tpl_text != _read(inst_path).replace("\r\n", "\n").strip(): drifted.append(hook_name)
    if missing_inst: results.append(("DUE", f"Missing hook(s): {', '.join(missing_inst)} — run: bash tools/install-hooks.sh"))
    if drifted: results.append(("NOTICE", f"Hook drift detected ({', '.join(drifted)}) — run: bash tools/install-hooks.sh"))
    return results

def check_cross_references() -> list[tuple[str, str]]:
    results = []
    index_text = _read(REPO_ROOT / "memory" / "INDEX.md")

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

    lessons_dir = REPO_ROOT / "memory" / "lessons"
    if lessons_dir.exists():
        lesson_paths = list(lessons_dir.glob("L-*.md"))
        actual = len(lesson_paths)
        tracked_raw = _git("ls-files", "--", "memory/lessons")
        tracked_lessons = [l.strip() for l in (tracked_raw or "").splitlines()
                           if re.fullmatch(r"memory/lessons/L-\d+\.md", l.strip())]
        tracked = len(tracked_lessons) if tracked_lessons else actual
        tracked_set = {p.replace("\\", "/") for p in tracked_lessons}
        untracked_names = sorted(p.name for p in lesson_paths if p.relative_to(REPO_ROOT).as_posix() not in tracked_set)
        if untracked_names and len(untracked_names) == actual and tracked_lessons:
            if {Path(p).name for p in tracked_lessons} == {p.name for p in lesson_paths}:
                untracked_names = []
        untracked = len(untracked_names)
        count_match = re.search(r"\*\*(\d+) lessons\*\*", index_text)
        claimed = int(count_match.group(1)) if count_match else None
        if claimed is not None:
            if tracked != claimed and not (untracked > 0 and claimed == actual):
                results.append(("NOTICE", f"INDEX lessons {claimed} != tracked {tracked}"))
        if untracked:
            includes = claimed == actual if claimed is not None else False
            note = "(INDEX includes drafts; tracked count excludes them)" if includes else "(not counted in tracked lesson total)"
            results.append(("NOTICE", f"{untracked} untracked lesson draft(s): {_truncated(untracked_names)} {note}"))

    principles_text = _read(REPO_ROOT / "memory" / "PRINCIPLES.md")
    all_pids, superseded_pids = _active_principle_ids(principles_text)
    actual_active_p = len(all_pids - superseded_pids)

    p_header_match = re.search(r"(\d+)\s+(?:live\s+)?principles", principles_text)
    idx_p_match = re.search(r"\*\*(\d+) principles\*\*", index_text)
    if p_header_match and int(p_header_match.group(1)) != actual_active_p:
        results.append(("NOTICE", f"PRINCIPLES header {p_header_match.group(1)} != ID-count {actual_active_p}"))
    if idx_p_match and int(idx_p_match.group(1)) != actual_active_p:
        results.append(("NOTICE", f"INDEX principles {idx_p_match.group(1)} != ID-count {actual_active_p}"))

    frontier_text = _read(REPO_ROOT / "tasks" / "FRONTIER.md")
    idx_f_match = re.search(r"\*\*(\d+) frontier questions\*\*", index_text)
    try:
        from swarm_parse import active_frontier_ids as _afi
        actual_frontier = len(_afi(frontier_text))
    except Exception:
        # fallback: count both numeric (F110) and named (F-COMM1) frontier entries
        numeric = re.findall(r"^- \*\*F\d+\*\*:", frontier_text, re.MULTILINE)
        named = re.findall(r"^- \*\*F-[A-Z][A-Z0-9]*\d*\*\*:", frontier_text, re.MULTILINE)
        actual_frontier = len(numeric) + len(named)
    if idx_f_match:
        claimed_f = int(idx_f_match.group(1))
        if claimed_f != actual_frontier:
            results.append(("NOTICE", f"INDEX frontier count {claimed_f} != active {actual_frontier}"))

    return results

def check_domain_frontier_consistency() -> list[tuple[str, str]]:
    results: list[tuple[str, str]] = []
    domains_dir = REPO_ROOT / "domains"
    if not domains_dir.exists():
        return results

    frontier_header_mismatch: list[str] = []
    index_count_mismatch: list[str] = []
    index_active_line_mismatch: list[str] = []
    index_open_section_mismatch: list[str] = []

    for frontier_path in sorted(domains_dir.glob("*/tasks/FRONTIER.md")):
        domain = frontier_path.parent.parent.name
        frontier_text = _read(frontier_path)
        if not frontier_text:
            continue

        frontier_ids, has_active_section = _extract_domain_frontier_active_ids(frontier_text)
        frontier_count = len(frontier_ids)
        frontier_header_count = _parse_domain_frontier_active_count(frontier_text)
        if has_active_section and frontier_header_count is not None and frontier_header_count != frontier_count:
            frontier_header_mismatch.append(f"{domain}(header={frontier_header_count}, parsed={frontier_count})")

        index_path = frontier_path.parent.parent / "INDEX.md"
        if not index_path.exists():
            continue
        index_text = _read(index_path)
        if not index_text:
            continue

        index_count = _parse_domain_index_active_count(index_text)
        if index_count is not None and index_count != frontier_count:
            index_count_mismatch.append(f"{domain}(index={index_count}, frontier={frontier_count})")

        active_line_ids = _parse_domain_index_active_line_ids(index_text)
        if active_line_ids is not None and active_line_ids != frontier_ids:
            index_active_line_mismatch.append(f"{domain}({_format_frontier_id_diff(frontier_ids, active_line_ids)})")

        has_open_section, open_ids = _parse_domain_index_open_ids(index_text)
        if has_open_section and open_ids != frontier_ids:
            index_open_section_mismatch.append(f"{domain}({_format_frontier_id_diff(frontier_ids, open_ids)})")

    if frontier_header_mismatch:
        results.append(("NOTICE", f"Domain FRONTIER Active header mismatch: {_truncated(frontier_header_mismatch, 5)}"))
    if index_count_mismatch:
        results.append(("NOTICE", f"Domain INDEX active-count mismatch vs FRONTIER: {_truncated(index_count_mismatch, 5)}"))
    if index_active_line_mismatch:
        results.append(("NOTICE", f"Domain INDEX active frontier list mismatch: {_truncated(index_active_line_mismatch, 4)}"))
    if index_open_section_mismatch:
        results.append(("NOTICE", f"Domain INDEX 'What's open' mismatch: {_truncated(index_open_section_mismatch, 4)}"))

    return results

def check_readme_snapshot_drift() -> list[tuple[str, str]]:
    results = []
    readme_text = _read(REPO_ROOT / "README.md")
    if not readme_text:
        return results

    session = _session_number()
    index_text = _read(REPO_ROOT / "memory" / "INDEX.md")
    index_session_match = re.search(
        r"^Updated:\s*\d{4}-\d{2}-\d{2}\s*\|\s*Sessions:\s*(\d+)\b",
        index_text,
        re.MULTILINE,
    )
    index_session = int(index_session_match.group(1)) if index_session_match else 0
    reference_session = index_session or session

    snap_match = re.search(
        r"^##\s+Current State Snapshot\s*\([^)]+,\s*S(\d+)\)",
        readme_text,
        re.MULTILINE,
    )
    if not snap_match:
        results.append(("NOTICE", "README missing session-stamped 'Current State Snapshot' header"))
        return results

    snap_session = int(snap_match.group(1))
    if reference_session > 0 and snap_session != reference_session:
        delta = reference_session - snap_session
        level = "DUE" if abs(delta) > 3 else "NOTICE"
        direction = "behind" if delta > 0 else "ahead"
        target_label = f"INDEX S{reference_session}" if index_session else f"SESSION-LOG S{reference_session}"
        results.append((level, f"README snapshot session S{snap_session} is {abs(delta)} session(s) {direction} of {target_label}"))

    scale_match = re.search(
        r"-\s*Swarm scale:\s*(\d+)\s*lessons,\s*(\d+)\s*principles,\s*(\d+)\s*beliefs,\s*(\d+)\s*active frontier questions\.",
        readme_text,
    )
    if not scale_match:
        results.append(("NOTICE", "README 'Swarm scale' line missing or unparsable"))
        return results

    l_match = re.search(r"\*\*(\d+) lessons\*\*", index_text)
    p_match = re.search(r"\*\*(\d+) principles\*\*", index_text)
    b_match = re.search(r"\*\*(\d+) beliefs\*\*", index_text)
    f_match = re.search(r"\*\*(\d+) frontier questions\*\*", index_text)
    if not (l_match and p_match and b_match and f_match):
        return results

    readme_scale = tuple(int(scale_match.group(i)) for i in range(1, 5))
    index_scale = (
        int(l_match.group(1)),
        int(p_match.group(1)),
        int(b_match.group(1)),
        int(f_match.group(1)),
    )
    if readme_scale != index_scale:
        results.append((
            "NOTICE",
            "README swarm scale drift vs INDEX "
            f"(README L/P/B/F={readme_scale[0]}/{readme_scale[1]}/{readme_scale[2]}/{readme_scale[3]}, "
            f"INDEX={index_scale[0]}/{index_scale[1]}/{index_scale[2]}/{index_scale[3]})",
        ))

    if "tools/orient.py" not in readme_text:
        results.append(("NOTICE", "README onboarding missing orient.py fast-path reference"))

    return results

def check_structure_layout() -> list[tuple[str, str]]:
    results: list[tuple[str, str]] = []

    missing_required = [path for path in STRUCTURE_REQUIRED_PATHS if not _exists(path)]
    if missing_required:
        results.append(("DUE", f"Structure policy files missing: {_truncated(missing_required, 5)}"))

    for folder, allowed_exts in STRUCTURE_ALLOWED_EXTENSIONS.items():
        folder_path = REPO_ROOT / folder
        if not folder_path.exists():
            results.append(("DUE", f"Missing required structure folder: {folder}/"))
            continue

        disallowed: list[str] = []
        for path in folder_path.rglob("*"):
            if not path.is_file():
                continue
            rel = path.relative_to(REPO_ROOT).as_posix()
            if path.name in STRUCTURE_ALLOWED_FILENAMES:
                continue
            ext = path.suffix.lower()
            if ext not in allowed_exts:
                disallowed.append(rel)
        if disallowed:
            results.append((
                "DUE",
                f"{folder}/ has disallowed file types: {_truncated(disallowed, 5)} "
                f"(allowed: {', '.join(sorted(allowed_exts))})",
            ))

    return results

def check_frontier_registry() -> list[tuple[str, str]]:
    results = []

    active_text = _read(REPO_ROOT / "tasks" / "FRONTIER.md")
    archived_text = _read(REPO_ROOT / "tasks" / "FRONTIER-ARCHIVE.md")

    active_ids = [int(m.group(1)) for m in re.finditer(r"^- \*\*F(\d+)\*\*:", active_text, re.MULTILINE)]
    archived_ids = [int(m.group(1)) for m in re.finditer(r"\|\s*F(\d+)\s*\|", archived_text)]

    def _duplicate_counts(ids: list[int]) -> list[tuple[int, int]]:
        counts: dict[int, int] = {}
        for fid in ids:
            counts[fid] = counts.get(fid, 0) + 1
        return sorted((fid, count) for fid, count in counts.items() if count > 1)

    active_dupes = _duplicate_counts(active_ids)
    archived_dupes = _duplicate_counts(archived_ids)
    if active_dupes:
        results.append(("DUE", f"FRONTIER duplicate ID(s): {_truncated(active_dupes, 5, fmt=lambda x: f'F{x[0]} x{x[1]}')}"))
    if archived_dupes:
        results.append(("DUE", f"FRONTIER-ARCHIVE duplicate ID(s): {_truncated(archived_dupes, 5, fmt=lambda x: f'F{x[0]} x{x[1]}')}"))

    overlap = sorted(set(active_ids) & set(archived_ids))
    if overlap:
        results.append(("DUE", f"Frontier ID(s) both open and archived: {_truncated(overlap, 8, fmt=lambda x: f'F{x}')}"))

    return results

def check_handoff_staleness() -> list[tuple[str, str]]:
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

def check_state_header_sync() -> list[tuple[str, str]]:
    results = []
    session = _session_number()
    if session <= 0:
        return results

    values: dict[str, int] = {}
    parse_fail = []

    next_text = _read(REPO_ROOT / "tasks" / "NEXT.md")
    m = re.search(r"^Updated:\s*\d{4}-\d{2}-\d{2}\s+S(\d+)\b", next_text, re.MULTILINE)
    if m:
        values["NEXT"] = int(m.group(1))
    else:
        parse_fail.append("NEXT")

    index_text = _read(REPO_ROOT / "memory" / "INDEX.md")
    m = re.search(r"^Updated:\s*\d{4}-\d{2}-\d{2}\s*\|\s*Sessions:\s*(\d+)\b", index_text, re.MULTILINE)
    if m:
        values["INDEX"] = int(m.group(1))
    else:
        parse_fail.append("INDEX")

    frontier_text = _read(REPO_ROOT / "tasks" / "FRONTIER.md")
    m = re.search(
        r"last\s+updated\s*:\s*\d{4}-\d{2}-\d{2}\s*(?:\|\s*)?S(\d+)\b",
        frontier_text,
        re.IGNORECASE,
    )
    if m:
        values["FRONTIER"] = int(m.group(1))
    else:
        parse_fail.append("FRONTIER")

    if parse_fail:
        results.append(("NOTICE", f"State header parse failed: {', '.join(parse_fail)}"))

    dirty = bool(_git("status", "--porcelain"))
    behind = [f"{name}:S{val}" for name, val in values.items() if val < session]
    ahead = [f"{name}:S{val}" for name, val in values.items() if val > session]

    if behind:
        results.append(("NOTICE", f"State header drift vs SESSION-LOG S{session}: {', '.join(behind)}"))
    if ahead and not dirty:
        results.append(("NOTICE", f"State header ahead of SESSION-LOG S{session}: {', '.join(ahead)}"))

    return results

def check_mission_constraints() -> list[tuple[str, str]]:
    results = []

    frontier_text = _read(REPO_ROOT / "tasks" / "FRONTIER.md")
    if not re.search(r"^- \*\*F119\*\*:", frontier_text, re.MULTILINE):
        results.append(("DUE", "F119 missing from tasks/FRONTIER.md (mission-constraint swarming)"))

    next_text = _read(REPO_ROOT / "tasks" / "NEXT.md")
    if "F119" not in next_text:
        results.append(("NOTICE", "F119 not tracked in tasks/NEXT.md priorities"))

    invariants_text = _read(REPO_ROOT / "beliefs" / "INVARIANTS.md")
    invariant_ids = re.findall(r"^##\s+(I\d+)\b", invariants_text, re.MULTILINE)
    id_counts: dict[str, int] = {}
    for inv_id in invariant_ids:
        id_counts[inv_id] = id_counts.get(inv_id, 0) + 1
    duplicate_ids = sorted(inv_id for inv_id, count in id_counts.items() if count > 1)
    if duplicate_ids:
        results.append(("DUE", f"INVARIANTS duplicate ID(s): {_truncated(duplicate_ids, 5)}"))

    mission_rows = {
        "I9": ("mission safety (do no harm)", "MC-SAFE"),
        "I10": ("mission portability (work everywhere)", "MC-PORT"),
        "I11": ("mission learning quality (improve knowledge)", "MC-LEARN"),
        "I12": ("mission continuity (stay connected)", "MC-CONN"),
    }
    missing_invariants = [
        f"{inv_id} ({label})"
        for inv_id, (label, tag) in mission_rows.items()
        if not re.search(rf"^##\s+{re.escape(inv_id)}\b.*\[{re.escape(tag)}\]", invariants_text, re.MULTILINE)
    ]
    if missing_invariants:
        results.append(("DUE", f"F119 mission invariants missing: {_truncated(missing_invariants)}"))

    check_sh = _read(REPO_ROOT / "tools" / "check.sh")
    portability_markers = ["choose_python()", "python3", "python", "py -3"]
    missing_portability_markers = [m for m in portability_markers if m not in check_sh]
    if missing_portability_markers:
        sample = ", ".join(missing_portability_markers)
        results.append(("NOTICE", f"F119 portability fallback drift in tools/check.sh: missing {sample}"))

    has_python_alias = _python_command_runs("python3") or _python_command_runs("python") or _py_launcher_runs()
    has_bash = _command_exists("bash")
    has_pwsh = _command_exists("pwsh") or _command_exists("powershell")
    has_check_wrapper = _exists("tools/check.sh")
    has_maintenance_wrapper = _exists("tools/maintenance.sh")
    has_check_wrapper_ps = _exists("tools/check.ps1")
    has_maintenance_wrapper_ps = _exists("tools/maintenance.ps1")
    inter_swarm_tools = all(_exists(p) for p in ("tools/bulletin.py", "tools/merge_back.py", "tools/propagate_challenges.py"))
    fallback_ready = ((has_bash and has_check_wrapper and has_maintenance_wrapper)
                      or (has_pwsh and has_check_wrapper_ps and has_maintenance_wrapper_ps))

    degraded_reasons: list[str] = []
    if not has_python_alias:
        degraded_reasons.append("python-alias-missing")
    if not inter_swarm_tools:
        degraded_reasons.append("inter-swarm-tooling-missing")

    if degraded_reasons:
        session = _session_number()
        continuity_text = (
            next_text
            + "\n"
            + "\n".join(_read(REPO_ROOT / "memory" / "SESSION-LOG.md").splitlines()[-80:])
        )
        if not has_python_alias and not fallback_ready:
            results.append(("DUE",
                "F119 degraded runtime continuity broken: no python alias and no wrapper path "
                "(`tools/check.sh` + `tools/maintenance.sh` or `tools/check.ps1` + `tools/maintenance.ps1`)"))

        _OC = F119_TRANSITION_OUTCOME_PATTERNS
        reason_specs = {
            "python-alias-missing": (
                "runtime portability",
                (r"runtime portability", r"python unavailable", r"no runnable python", r"python launcher", r"python alias"),
                (r"bash tools/(?:check|maintenance)\.", r"(?:pwsh|powershell).*tools/(?:check|maintenance)\.",
                 r"tools/(?:check|maintenance)\.ps1", r"python3 tools/maintenance\.py", r"py -3"),
                _OC,
            ),
            "inter-swarm-tooling-missing": (
                "offline/inter-swarm continuity",
                (r"inter-swarm", r"offline", r"disconnected", r"bulletin"),
                (r"tools/bulletin\.py (?:help-queue|request-help|offer-help|sync)", r"tasks/PR-QUEUE\.json", r"tasks/SWARM-LANES\.md"),
                _OC,
            ),
        }

        for reason in degraded_reasons:
            spec = reason_specs.get(reason)
            if not spec:
                continue
            label, reason_patterns, action_patterns, outcome_patterns = spec

            action_sessions = set(
                _reason_action_evidence_sessions(continuity_text, reason_patterns, action_patterns)
            )
            outcome_sessions = set(
                _reason_action_evidence_sessions(continuity_text, reason_patterns, outcome_patterns)
            )
            reason_sessions = set(
                _reason_action_evidence_sessions(continuity_text, reason_patterns, (r".+",))
            )

            if not action_sessions:
                results.append(("NOTICE", f"F119 {label} degraded mode lacks reason+action transition evidence in NEXT/SESSION-LOG"))
                continue
            if not outcome_sessions:
                results.append(("NOTICE", f"F119 {label} degraded mode lacks reason+outcome evidence in NEXT/SESSION-LOG"))
                continue

            joined_sessions = sorted(action_sessions & outcome_sessions)
            if not joined_sessions:
                results.append(("NOTICE", f"F119 {label} transition evidence is split across sessions (action/outcome not co-located)"))
                continue

            latest = max(joined_sessions)
            stale_limit = F119_STALE_EVIDENCE_SESSIONS.get(reason, max(F119_STALE_EVIDENCE_SESSIONS.values()))
            if session > 0 and (session - latest) > stale_limit:
                if not any((session - s) <= F119_RECENT_REASON_ACTIVITY_WINDOW for s in reason_sessions):
                    continue
                recent_reason = max(reason_sessions) if reason_sessions else latest
                results.append(("NOTICE",
                    f"F119 {label} degraded transition evidence stale "
                    f"(latest S{latest}, current S{session}, threshold >{stale_limit} sessions, recent reason S{recent_reason})"))

        if "inter-swarm-tooling-missing" in degraded_reasons:
            continuity_artifacts = ["tasks/PR-QUEUE.json", "tasks/SWARM-LANES.md"]
            missing_artifacts = [path for path in continuity_artifacts if not _exists(path)]
            if missing_artifacts:
                results.append(("DUE", f"F119 offline continuity artifacts missing: {_truncated(missing_artifacts)}"))

    maintenance_text = _read(REPO_ROOT / "tools" / "maintenance.py")
    required_checks = [
        "check_validator",
        "check_runtime_portability",
        "check_cross_references",
        "check_readme_snapshot_drift",
        "check_structure_layout",
        "check_state_header_sync",
        "check_session_log_integrity",
        "check_child_bulletins",
        "check_help_requests",
        "check_swarm_lanes",
        "check_swarm_coordinator",
        "check_lane_reporting_quality",
    ]
    missing_defs = [
        name for name in required_checks
        if not re.search(rf"^def\s+{re.escape(name)}\s*\(", maintenance_text, re.MULTILINE)
    ]
    if missing_defs:
        results.append(("DUE", f"F119 guard definition(s) missing in maintenance.py: {_truncated(missing_defs)}"))

    list_match = re.search(r"all_checks\s*=\s*\[(.*?)\]", maintenance_text, re.DOTALL)
    if list_match:
        list_block = list_match.group(1)
        missing_wired = [name for name in required_checks if name not in list_block]
        if missing_wired:
            results.append(("DUE", f"F119 guard(s) not wired in all_checks: {_truncated(missing_wired)}"))
    else:
        results.append(("NOTICE", "F119 guard wiring parse failed for all_checks list"))

    tracked_paths = _tracked_changed_paths()
    if tracked_paths:
        knowledge_state_paths = {
            "tasks/NEXT.md",
            "memory/SESSION-LOG.md",
            "memory/INDEX.md",
            "tasks/FRONTIER.md",
            "memory/PRINCIPLES.md",
            "beliefs/CHALLENGES.md",
            "memory/HEALTH.md",
        }
        has_lesson_delta = any(re.fullmatch(r"memory/lessons/L-\d+\.md", p) for p in tracked_paths)
        has_knowledge_delta = has_lesson_delta or any(p in knowledge_state_paths for p in tracked_paths)
        if len(tracked_paths) >= 5 and not has_knowledge_delta:
            results.append(("DUE", "F119 learning-quality gap: tracked deltas without knowledge-state update (NEXT/SESSION-LOG/INDEX/FRONTIER/PRINCIPLES/lessons)"))

        commands = {
            "python3": _python_command_runs("python3"),
            "python": _python_command_runs("python"),
            "py -3": _py_launcher_runs(),
            "git": _command_runs("git", ["--version"]),
            "bash": _command_runs("bash", ["--version"]),
        }
        inter_swarm_cap = {
            "inter_swarm": {
                "present": sum(1 for p in ("tools/bulletin.py", "tools/merge_back.py", "tools/propagate_challenges.py") if _exists(p)),
                "total": 3,
            }
        }
        connectivity = _inter_swarm_connectivity(inter_swarm_cap, commands)
        if not connectivity.get("ready"):
            has_continuity_delta = any(p in {"tasks/NEXT.md", "memory/SESSION-LOG.md"} for p in tracked_paths)
            if not has_continuity_delta:
                missing = connectivity.get("missing", [])
                detail = f" ({_truncated(missing)})" if isinstance(missing, list) and missing else ""
                results.append(("NOTICE",
                    f"F119 continuity risk: degraded inter-swarm connectivity{detail} with no local handoff/log delta (tasks/NEXT.md or memory/SESSION-LOG.md)"))

    return results

def check_session_log_integrity() -> list[tuple[str, str]]:
    results = []
    text = _read(REPO_ROOT / "memory" / "SESSION-LOG.md")
    if not text:
        return results

    control_hits: list[tuple[int, int]] = []
    for line_no, raw in enumerate(text.splitlines(), start=1):
        for ch in raw:
            code = ord(ch)
            if code < 32 and ch not in ("\t",):
                control_hits.append((line_no, code))
    if control_hits:
        results.append(("NOTICE", f"SESSION-LOG contains control character(s): {_truncated(control_hits, 5, fmt=lambda x: f'L{x[0]}:0x{x[1]:02x}')}"))

    rows = []
    for raw in text.splitlines():
        m = re.match(r"^S(\d+)\b", raw)
        if not m:
            continue
        sid = int(m.group(1))
        normalized = re.sub(r"\s+", " ", raw.strip())
        rows.append((sid, normalized))

    if not rows:
        return results

    dup_counts: dict[str, int] = {}
    for _, row in rows:
        dup_counts[row] = dup_counts.get(row, 0) + 1
    dup_rows = [(row, n) for row, n in dup_counts.items() if n > 1]
    if dup_rows:
        results.append(("NOTICE", f"SESSION-LOG exact duplicate row(s): {_truncated(dup_rows, fmt=lambda x: f'{x[0][:40]}... x{x[1]}')}"))

    recent_window = 40
    recent_rows = rows[-recent_window:]
    historical_ids = {sid for sid, _ in rows[:-recent_window]} if len(rows) > recent_window else set()

    non_monotonic = []
    for i in range(1, len(recent_rows)):
        prev_sid = recent_rows[i - 1][0]
        sid = recent_rows[i][0]
        one_step_backfill = sid < prev_sid and (prev_sid - sid) == 1
        benign_backfill = sid in historical_ids or one_step_backfill
        if sid < prev_sid and not benign_backfill:
            non_monotonic.append((prev_sid, sid))
    if non_monotonic:
        results.append(("NOTICE", f"SESSION-LOG recent non-monotonic order: {_truncated(non_monotonic, 5, fmt=lambda x: f'S{x[0]}->S{x[1]}')}"))

    return results

def check_paper_accuracy() -> list[tuple[str, str]]:
    return run_paper_drift_check(REPO_ROOT, _session_number())

def check_utility() -> list[tuple[str, str]]:
    results = []
    principles_text = _read(REPO_ROOT / "memory" / "PRINCIPLES.md")
    if not principles_text:
        return results
    all_ids, superseded = _active_principle_ids(principles_text)
    active_ids = all_ids - superseded
    cited: set[int] = set()
    principles_path = REPO_ROOT / "memory" / "PRINCIPLES.md"
    for f in _iter_utility_citation_files():
        if f == principles_path:
            continue
        for m in PRINCIPLE_ID_RE.finditer(_read(f)):
            cited.add(int(m.group(1)))
    uncited = sorted(active_ids - cited)
    if uncited:
        results.append(("NOTICE", f"{len(uncited)} active principle(s) with 0 citations: {_truncated(uncited, 5, fmt=lambda x: f'P-{x}')}"))
    return results

def check_proxy_k_drift() -> list[tuple[str, str]]:
    results = []
    log_path = REPO_ROOT / "experiments" / "proxy-k-log.json"
    if not log_path.exists():
        return results

    try:
        entries = json.loads(_read(log_path))
    except Exception:
        return results

    if len(entries) < 2:
        return results

    tiers = {
        "T0-mandatory": ["SWARM.md", "CLAUDE.md", "beliefs/CORE.md", "memory/INDEX.md"],
        "T1-identity": ["beliefs/PHILOSOPHY.md", "beliefs/DEPS.md", "beliefs/INVARIANTS.md"],
        "T2-protocols": ["memory/DISTILL.md", "memory/VERIFY.md", "memory/OPERATIONS.md", "beliefs/CONFLICTS.md"],
        "T3-knowledge": ["memory/PRINCIPLES.md", "tasks/FRONTIER.md"],
        "T4-tools": ["tools/validate_beliefs.py", "tools/maintenance.py", "tools/paper_drift.py", "tools/swarm_parse.py"],
    }
    schema_payload = json.dumps(tiers, sort_keys=True, separators=(",", ":")).encode("utf-8")
    current_schema = hashlib.sha256(schema_payload).hexdigest()
    schema_entries = [e for e in entries if e.get("tier_schema") == current_schema]
    clean_schema_entries = [e for e in schema_entries if not e.get("dirty_tree")]
    baseline = clean_schema_entries if len(clean_schema_entries) >= 2 else schema_entries
    if len(baseline) < 2:
        n = len(schema_entries)
        results.append(("NOTICE",
            f"Proxy K schema baseline unavailable ({n} matching snapshot{'s' if n != 1 else ''}); run clean snapshots: {PYTHON_CMD} tools/proxy_k.py --save"))
        return results

    floor_idx = 0
    for i in range(1, len(baseline)):
        if baseline[i]["total"] < baseline[i - 1]["total"]:
            floor_idx = i

    floor_entry = baseline[floor_idx]
    floor = floor_entry["total"]
    if floor <= 0:
        return results

    # If the historical-minimum floor is stale (>= 8 sessions ago) and a more
    # recent clean baseline exists, use that as the floor to acknowledge
    # intentional tool growth without triggering false URGENT compaction. (L-273)
    _cur_s = _session_number()
    _floor_s = int(floor_entry.get("session", 0) or 0)
    if len(clean_schema_entries) >= 2 and _floor_s > 0 and _cur_s > 0 and (_cur_s - _floor_s) >= 8:
        _newer = [e for e in clean_schema_entries if int(e.get("session", 0) or 0) > _floor_s]
        if _newer:
            _latest_clean = max(_newer, key=lambda e: int(e.get("session", 0) or 0))
            if _latest_clean["total"] > floor:
                floor_entry = _latest_clean
                floor = _latest_clean["total"]

    live_tiers: dict[str, int] = {}
    live_total = 0
    for tier, files in tiers.items():
        tier_total = sum(_token_count(REPO_ROOT / f) for f in files)
        live_tiers[tier] = tier_total
        live_total += tier_total

    latest_entry = entries[-1]
    latest_logged = latest_entry["total"]
    latest_session = int(latest_entry.get("session", 0) or 0)
    latest_marked_dirty = bool(latest_entry.get("dirty_tree", False))
    floor_session = int(floor_entry.get("session", 0) or 0)
    current_session = _session_number()
    logged_drift = (latest_logged - floor) / floor
    live_drift = (live_total - floor) / floor
    dirty = bool(_git("status", "--porcelain"))
    stale_clean_baseline = (
        dirty
        and floor_session > 0
        and current_session > 0
        and (current_session - floor_session) >= 8
    )

    likely_dirty_logged = latest_marked_dirty
    if not likely_dirty_logged and dirty and latest_session > 0 and current_session > 0:
        recent = latest_session >= max(0, current_session - 2)
        proximity = abs(latest_logged - live_total) / max(1, live_total)
        if recent and proximity <= 0.02:
            likely_dirty_logged = True
    same_dirty_snapshot = (
        likely_dirty_logged
        and dirty
        and current_session > 0
        and latest_session >= max(0, current_session - 2)
        and abs(live_total - latest_logged) / max(1, latest_logged) <= 0.01
    )

    def _tier_targets() -> str:
        floor_tiers = floor_entry.get("tiers", {})
        tier_deltas = []
        for tier in sorted(live_tiers):
            delta = live_tiers.get(tier, 0) - floor_tiers.get(tier, 0)
            if delta > 0:
                tier_deltas.append(f"{tier}+{delta}")
        return f" [{', '.join(tier_deltas[:3])}]" if tier_deltas else ""

    if logged_drift > 0.06:
        if dirty and live_drift <= 0.06:
            results.append(("NOTICE",
                f"Proxy K logged drift {logged_drift:.1%} ({latest_logged} vs {floor}) but live drift is {live_drift:.1%} on dirty tree; re-save clean snapshot: {PYTHON_CMD} tools/proxy_k.py --save"))
        elif likely_dirty_logged:
            if logged_drift > 0.10:
                # Dirty-tree floor approximation is sufficient at high drift — escalate (L-245)
                level = "URGENT" if logged_drift > 0.20 else "DUE"
                results.append((level,
                    f"Proxy K drift {logged_drift:.1%} ({latest_logged} vs {floor}) on dirty tree — compaction overdue{_tier_targets()}; run: {PYTHON_CMD} tools/compact.py"))
            elif not same_dirty_snapshot:
                qualifier = "current dirty" if (current_session > 0 and latest_session >= current_session) else f"likely dirty S{latest_session}"
                results.append(("NOTICE",
                    f"Proxy K logged drift {logged_drift:.1%} ({latest_logged} vs {floor}) from {qualifier}; save clean snapshot when stable: {PYTHON_CMD} tools/proxy_k.py --save"))
        elif stale_clean_baseline:
            results.append(("NOTICE",
                f"Proxy K baseline S{floor_session} is stale on dirty tree (current S{current_session}); re-save clean snapshot: {PYTHON_CMD} tools/proxy_k.py --save"))
        else:
            level = "URGENT" if logged_drift > 0.10 else "DUE"
            results.append((level, f"Proxy K drift {logged_drift:.1%} ({latest_logged} vs {floor}); run: {PYTHON_CMD} tools/compact.py"))
    elif live_drift > 0.06 and dirty:
        results.append(("NOTICE",
            f"Proxy K live drift {live_drift:.1%} ({live_total} vs {floor}) on dirty tree{_tier_targets()}; save when stable: {PYTHON_CMD} tools/proxy_k.py --save"))
    elif live_drift > 0.06:
        level = "URGENT" if live_drift > 0.10 else "DUE"
        results.append((level, f"Proxy K drift {live_drift:.1%} ({live_total} vs {floor}){_tier_targets()}; run: {PYTHON_CMD} tools/compact.py"))

    return results

def check_file_graph() -> list[tuple[str, str]]:
    results = []
    structural = [REPO_ROOT / p for p in (
        "SWARM.md", "CLAUDE.md", "README.md", "beliefs/CORE.md",
        "memory/INDEX.md", "memory/OPERATIONS.md", "tasks/NEXT.md")]
    broken = []
    seen = set()
    for sf in structural:
        text = _read(sf)
        if not text:
            continue
        refs = re.findall(r"`([a-zA-Z][\w\-/]+\.(?:md|py|json|sh))`", text)
        for ref in refs:
            if ref.startswith("L-") or ref.startswith("P-") or ref.startswith("B-"):
                continue
            resolved = _resolve_repo_file_ref(ref)
            if not resolved:
                continue
            full = REPO_ROOT / resolved
            if not full.exists():
                label = f"{sf.name}→{ref}"
                if resolved != ref:
                    label += f" ({resolved})"
                if label not in seen:
                    seen.add(label)
                    broken.append(label)
    if broken:
        results.append(("DUE", f"{len(broken)} broken file reference(s): {', '.join(broken[:5])}"))
    return results

def _inter_swarm_connectivity(capabilities: dict, commands: dict[str, bool]) -> dict:
    protocol_paths = ["experiments/inter-swarm/PROTOCOL.md", "memory/OPERATIONS.md"]
    protocol_state = [{"path": p, "exists": _exists(p)} for p in protocol_paths]
    missing_protocols = [s["path"] for s in protocol_state if not s["exists"]]
    inter_swarm = capabilities.get("inter_swarm", {}) if isinstance(capabilities, dict) else {}
    present = inter_swarm.get("present", 0) if isinstance(inter_swarm, dict) else 0
    total = inter_swarm.get("total", 0) if isinstance(inter_swarm, dict) else 0
    if not isinstance(present, int): present = 0
    if not isinstance(total, int): total = 0
    tooling_ready = total > 0 and present >= total
    python_ready = any(bool(commands.get(n)) for n in ("python3", "python", "py -3"))
    missing: list[str] = []
    if not tooling_ready: missing.append(f"inter_swarm_tools:{present}/{total}")
    if not python_ready: missing.append("python-command")
    missing.extend(missing_protocols)
    return {"ready": tooling_ready and python_ready and not missing_protocols,
            "tooling": {"present": present, "total": total}, "python_command_ready": python_ready,
            "protocols": protocol_state, "missing": missing}

def build_inventory() -> dict:
    def _tools(*names: str) -> list[str]:
        return [f"tools/{name}" for name in names]

    bridges = BRIDGE_FILES
    core_state = ["beliefs/CORE.md", "memory/INDEX.md", "tasks/FRONTIER.md", "tasks/NEXT.md", "memory/PRINCIPLES.md"]
    capability_sets: dict[str, list[str]] = {
        "orientation": _tools("maintenance.py", "orient.py", "sync_state.py", "pulse.py",
                              "context_router.py", "substrate_detect.py", "alignment_check.py"),
        "validation": _tools("validate_beliefs.py", "check.sh", "check.ps1", "maintenance.sh",
                             "maintenance.ps1", "install-hooks.sh", "repair.py", "pre-commit.hook", "commit-msg.hook"),
        "evolution": _tools("evolve.py", "swarm_test.py", "agent_swarm.py", "colony.py", "swarm_colony.py", "spawn_coordinator.py"),
        "collaboration": _tools("swarm_pr.py"),
        "inter_swarm": _tools("bulletin.py", "merge_back.py", "propagate_challenges.py",
                              "close_lane.py", "harvest_expert.py"),
        "compaction": _tools("compact.py", "proxy_k.py", "frontier_decay.py"),
        "analysis": _tools("nk_analyze.py", "nk_analyze_go.py", "wiki_swarm.py",
                           "dream.py", "change_quality.py", "task_recognizer.py",
                           "generalizer_expert.py", "contamination_investigator.py"),
        "benchmarks": _tools("f92_benchmark.py", "f92_real_coop_benchmark.py", "spawn_quality.py", "p155_live_trace.py"),
        "support": _tools("swarm_parse.py", "novelty.py", "validate_beliefs_extras.py"),
    }
    commands = {
        "python3": _python_command_runs("python3"),
        "python": _python_command_runs("python"),
        "git": _command_runs("git", ["--version"]),
        "bash": _command_runs("bash", ["--version"]),
    }
    if platform.system().lower().startswith("windows") or _command_exists("pwsh"):
        commands["pwsh"] = _command_runs("pwsh", ["-NoProfile", "-Command", "$PSVersionTable.PSVersion.Major"], timeout=8)
    elif _command_exists("powershell"):
        commands["powershell"] = _command_runs("powershell", ["-NoProfile", "-Command", "$PSVersionTable.PSVersion.Major"], timeout=8)
    if platform.system().lower().startswith("windows") or _command_exists("py"):
        commands["py -3"] = _py_launcher_runs()
    capabilities = {
        name: {
            "present": sum(1 for p in files if _exists(p)),
            "total": len(files),
            "files": files,
        }
        for name, files in capability_sets.items()
    }
    inter_swarm_connectivity = _inter_swarm_connectivity(capabilities, commands)

    return {
        "host": {
            "platform": platform.platform(),
            "python_executable": PYTHON_EXE,
            "python_command_hint": PYTHON_CMD,
            "commands": commands,
        },
        "bridges": [{"path": p, "exists": _exists(p)} for p in bridges],
        "core_state": [{"path": p, "exists": _exists(p)} for p in core_state],
        "capabilities": capabilities,
        "inter_swarm_connectivity": inter_swarm_connectivity,
    }

def print_inventory(inv: dict):
    _ok = lambda v: "OK " if v else "NO "
    host = inv["host"]
    print(f"=== SWARM INVENTORY ===\nHost: {host['platform']}\nPython: {host['python_executable']}  hint: {host['python_command_hint']}\n")
    print("Commands:")
    for name, ok in host["commands"].items():
        print(f"  {_ok(ok)}{name}")
    for section, key in (("Bridge files", "bridges"), ("Core state", "core_state")):
        print(f"\n{section}:")
        for item in inv[key]:
            print(f"  {_ok(item['exists'])}{item['path']}")
    print("\nCapabilities:")
    for name, info in inv["capabilities"].items():
        print(f"  {name:<12} {info['present']}/{info['total']}")
    inter_swarm = inv.get("inter_swarm_connectivity", {})
    if isinstance(inter_swarm, dict) and inter_swarm:
        tooling = inter_swarm.get("tooling", {}) if isinstance(inter_swarm.get("tooling"), dict) else {}
        status = "READY" if inter_swarm.get("ready") else "NOT READY"
        print(f"\nInter-swarm: {status} (tooling {tooling.get('present', '?')}/{tooling.get('total', '?')}, python {_ok(inter_swarm.get('python_command_ready'))})")
        missing = inter_swarm.get("missing", [])
        if isinstance(missing, list) and missing:
            print(f"  Missing: {', '.join(str(item) for item in missing)}")
    print()

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
        check_kill_switch,
        check_validator,
        check_mission_constraints,
        check_runtime_portability,
        check_commit_hooks,
        check_version_drift,
        check_open_challenges,
        check_compaction,
        check_lessons,
        check_child_bulletins,
        check_help_requests,
        check_frontier_decay,
        check_periodics,
        check_human_queue,
        check_swarm_lanes,
        check_swarm_coordinator,
        check_lane_reporting_quality,
        check_github_swarm_intake,
        check_uncommitted,
        check_handoff_staleness,
        check_session_log_integrity,
        check_state_header_sync,
        check_cross_references,
        check_anxiety_zones,
        check_dispatch_log,
        check_domain_expert_coverage,
        check_historian_integrity,
        check_domain_frontier_consistency,
        check_readme_snapshot_drift,
        check_structure_layout,
        check_frontier_registry,
        check_file_graph,
        check_paper_accuracy,
        check_utility,
        check_proxy_k_drift,
        check_t4_tool_size,
    ]

    if quick:
        all_checks = [c for c in all_checks if c is not check_utility]

    if not quick:
        all_checks.append(check_unpushed)

    items: list[tuple[str, str]] = []
    for check_fn in all_checks:
        try:
            items.extend(check_fn())
        except Exception as e:
            items.append(("NOTICE", f"{check_fn.__name__} error: {e}"))

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
