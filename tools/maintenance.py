#!/usr/bin/env python3

import importlib
import json
import hashlib
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
    for module_name in module_names:
        try:
            mod = importlib.import_module(module_name)
            return getattr(mod, symbol)
        except (ModuleNotFoundError, AttributeError):
            continue
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


def _command_exists(cmd: str) -> bool:
    return bool(shutil.which(cmd))


def _command_runs(cmd: str, args: list[str], timeout: int = 5) -> bool:
    if not _command_exists(cmd):
        return False
    try:
        r = subprocess.run([cmd] + args, capture_output=True, text=True, timeout=timeout)
    except Exception:
        return False
    return r.returncode == 0


def _python_command_runs(cmd: str) -> bool:
    return _command_runs(cmd, ["-c", "import sys"], timeout=8)


def _select_python_command() -> str:
    for candidate in ("python3", "python", "py"):
        if _python_command_runs(candidate):
            return candidate
    exe_name = Path(PYTHON_EXE).name
    if _python_command_runs(exe_name):
        return exe_name
    return PYTHON_EXE


PYTHON_CMD = _select_python_command()


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


def _token_count(path: Path) -> int:
    try:
        return len(_read(path)) // 4
    except Exception:
        return 0


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


def _exists(path: str) -> bool:
    return (REPO_ROOT / path).exists()


def _is_wsl_mnt_repo() -> bool:
    if not sys.platform.startswith("linux"):
        return False
    rel = platform.release().lower()
    plat = platform.platform().lower()
    if "microsoft" not in rel and "microsoft" not in plat:
        return False
    repo_posix = str(REPO_ROOT).replace("\\", "/")
    return repo_posix.startswith("/mnt/")


def _session_number() -> int:
    log = _read(REPO_ROOT / "memory" / "SESSION-LOG.md")
    numbers = re.findall(r"^S(\d+)", log, re.MULTILINE)
    return max(int(n) for n in numbers) if numbers else 0


def _active_principle_ids(text: str) -> tuple[set[int], set[int]]:
    return parse_active_principle_ids(text)


def _normalize_hq_question(text: str) -> str:
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", (text or "").lower())
    return re.sub(r"\s+", " ", text).strip()


def _iter_utility_citation_files() -> list[Path]:
    tracked = _git("ls-files", "*.md", "*.py", "*.json")
    if tracked:
        files: list[Path] = []
        for rel in tracked.splitlines():
            rel = rel.strip().replace("\\", "/")
            if not rel or any(rel.startswith(prefix) for prefix in UTILITY_CITATION_SKIP_PREFIXES):
                continue
            path = REPO_ROOT / rel
            if not path.exists() or not path.is_file():
                continue
            try:
                if path.stat().st_size > UTILITY_CITATION_MAX_BYTES:
                    continue
            except Exception:
                continue
            files.append(path)
        return files

    files: list[Path] = []
    for ext in ("*.md", "*.py", "*.json"):
        for path in REPO_ROOT.rglob(ext):
            rel = path.relative_to(REPO_ROOT).as_posix()
            if any(rel.startswith(prefix) for prefix in UTILITY_CITATION_SKIP_PREFIXES):
                continue
            try:
                if path.stat().st_size > UTILITY_CITATION_MAX_BYTES:
                    continue
            except Exception:
                continue
            files.append(path)
    return files




def check_unpushed() -> list[tuple[str, str]]:
    results = []
    ahead = _git("rev-list", "--count", "@{upstream}..HEAD")
    if ahead and ahead.isdigit() and int(ahead) > 0:
        n = int(ahead)
        level = "URGENT" if n >= 10 else "DUE" if n >= 5 else "NOTICE"
        results.append((level, f"{n} unpushed commits — git push"))
    return results


def check_uncommitted() -> list[tuple[str, str]]:
    results = []
    status = _git("-c", "core.quotepath=false", "status", "--porcelain")
    if status:
        lines = [l for l in status.splitlines() if l.strip()]
        # Count any tracked delta (M/A/D/R/C/U) instead of only modified entries.
        tracked = [l for l in lines if not l.startswith("??")]

        def _decode_git_path(path: str) -> str:
            p = path.strip()
            if p.startswith('"') and p.endswith('"') and len(p) >= 2:
                inner = p[1:-1]
                try:
                    # Git quoted paths may contain octal-escaped UTF-8 bytes.
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

        # On WSL /mnt repos, status often over-reports CRLF-only edits compared to
        # Windows-native runs. Filter modification entries to substantive diffs.
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
                results.append(("NOTICE", f"WSL portability: suppressed {suppressed} CRLF-only tracked delta(s)"))

        untracked = [l for l in lines if l.startswith("??")]
        def _is_ephemeral_parent_child_artifact(path: str) -> bool:
            # Temp integration artifacts can appear with either normalized
            # separators or collapsed Windows path fragments.
            p = path.replace("\\", "/")
            return bool(re.search(r"AppData/?Local/?Temp/?tmp[^/]*parent-child/?$", p, re.IGNORECASE))

        # Ignore generated wiki swarm notes and temp integration artifacts.
        untracked_paths = [_status_path(l) for l in untracked]
        untracked_actionable = [
            p for p in untracked_paths
            if not (
                (p.startswith("workspace/notes/wiki-swarm-") and p.endswith(".md"))
                or re.fullmatch(r"memory/lessons/L-\d+\.md", p)
                or _is_ephemeral_parent_child_artifact(p)
            )
        ]
        if tracked:
            tracked_paths = [_status_path(l) for l in tracked]
            sample = ", ".join(tracked_paths[:3])
            suffix = "..." if len(tracked) > 3 else ""
            results.append(("NOTICE", f"{len(tracked)} tracked file(s) uncommitted: {sample}{suffix}"))
        if untracked_actionable:
            sample = ", ".join(untracked_actionable[:3])
            suffix = "..." if len(untracked_actionable) > 3 else ""
            results.append(("NOTICE", f"{len(untracked_actionable)} untracked file(s): {sample}{suffix}"))
    return results


def check_open_challenges() -> list[tuple[str, str]]:
    results = []

    challenges_text = _read(REPO_ROOT / "beliefs" / "CHALLENGES.md")
    open_challenges = re.findall(r"\|\s*OPEN\s*\|", challenges_text, re.IGNORECASE)
    if open_challenges:
        results.append(("DUE", f"{len(open_challenges)} open challenge(s) in CHALLENGES.md"))

    phil_text = _read(REPO_ROOT / "beliefs" / "PHILOSOPHY.md")
    phil_section = phil_text[phil_text.find("## Challenges"):] if "## Challenges" in phil_text else ""
    open_phil = re.findall(r"\|\s*open\s*\|", phil_section, re.IGNORECASE)
    if open_phil:
        results.append(("DUE", f"{len(open_phil)} open PHIL challenge(s)"))

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


def check_child_bulletins() -> list[tuple[str, str]]:
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
        results.append(("NOTICE", f"{len(stale)} stale bulletin(s): {', '.join(stale[:5])}"))
    if external:
        results.append(("NOTICE", f"{len(external)} external bulletin file(s) ignored: {', '.join(external[:5])}"))

    return results


def check_help_requests() -> list[tuple[str, str]]:
    results = []
    bulletin_dir = REPO_ROOT / "experiments" / "inter-swarm" / "bulletins"
    if not bulletin_dir.exists():
        return results

    req_re = re.compile(r"Type:\s*help-request.*?Request-ID:\s*(\S+)", re.DOTALL)
    resp_re = re.compile(r"Type:\s*help-response.*?Request-ID:\s*(\S+)", re.DOTALL)
    open_ids: set[str] = set()
    responses: set[str] = set()

    for f in bulletin_dir.glob("*.md"):
        text = _read(f)
        open_ids |= {m.group(1).strip() for m in req_re.finditer(text)}
        responses |= {m.group(1).strip() for m in resp_re.finditer(text)}

    open_ids = sorted(open_ids - responses)
    if open_ids:
        sample = ", ".join(open_ids[:3])
        results.append((
            "DUE",
            f"{len(open_ids)} open help request(s): {sample}; respond with `{PYTHON_CMD} tools/bulletin.py offer-help ...`",
        ))

    return results


def check_compaction() -> list[tuple[str, str]]:
    results = []

    index_lines = _line_count(REPO_ROOT / "memory" / "INDEX.md")
    if index_lines > 60:
        results.append(("DUE", f"INDEX.md is {index_lines} lines (>60)"))

    mandatory = sum(_line_count(REPO_ROOT / p) for p in [
        Path("CLAUDE.md"),
        Path("beliefs") / "CORE.md",
        Path("memory") / "INDEX.md",
    ])
    if mandatory > 200:
        results.append(("DUE", f"Mandatory load is {mandatory} lines (>200)"))

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


def check_frontier_decay() -> list[tuple[str, str]]:
    results = []
    frontier_path = REPO_ROOT / "tasks" / "FRONTIER.md"
    decay_file = REPO_ROOT / "experiments" / "frontier-decay.json"
    if not frontier_path.exists():
        return results

    text = _read(frontier_path)
    open_text = text.split("## Archive", 1)[0]
    decay: dict[str, dict[str, str]] = {}
    if decay_file.exists():
        try:
            decay = json.loads(_read(decay_file))
        except Exception:
            decay = {}

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


def check_periodics() -> list[tuple[str, str]]:
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
    dirty = bool(_git("status", "--porcelain"))

    for item in data.get("items", []):
        item_id = item.get("id", "<unknown>")
        description = item.get("description", item_id)
        cadence = item.get("cadence_sessions", 10)
        last = item.get("last_reviewed_session", 0)
        if last > session:
            # In a dirty tree, state files are commonly updated before session-log
            # entries are finalized; suppress transient ahead-marker noise.
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
    results = []

    has_git = _command_exists("git")
    has_bash = _command_exists("bash")
    has_python_alias = _python_command_runs("python3") or _python_command_runs("python")

    if not has_git:
        results.append(("URGENT", "git not found in PATH — swarm memory/commit workflow cannot run"))
    if not has_python_alias:
        results.append(("DUE", f"No python alias in PATH — use explicit interpreter: {PYTHON_EXE}"))
    if not has_bash and (_exists("workspace/genesis.sh") or _exists("tools/check.sh")):
        results.append(("DUE", "bash not found — `workspace/genesis.sh` and `tools/check.sh` won't run on this host"))

    # Cross-runtime warning: WSL over /mnt/* often reports different git/index state
    # than Windows-native runs due line-ending/index semantics.
    if _is_wsl_mnt_repo():
        results.append(("NOTICE", "WSL on /mnt/* repo: status/proxy-K may diverge from Windows runtime"))

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

    # Setup hygiene: bridge files should explicitly point back to SWARM.md protocol.
    swarm_ref_re = re.compile(r"\bswarm\.md\b", re.IGNORECASE)
    bridge_without_swarm_ref = []
    for path in bridges:
        if path == "SWARM.md" or path in missing_bridges:
            continue
        if not swarm_ref_re.search(_read(REPO_ROOT / path)):
            bridge_without_swarm_ref.append(path)
    if bridge_without_swarm_ref:
        sample = ", ".join(bridge_without_swarm_ref[:3])
        results.append(("DUE", f"{len(bridge_without_swarm_ref)} bridge file(s) missing SWARM.md protocol reference: {sample}"))

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
        tracked_lessons = []
        if tracked_raw:
            tracked_lessons = [
                l.strip() for l in tracked_raw.splitlines()
                if re.search(r"memory/lessons/L-\d+\.md$", l.strip())
            ]
        if not tracked_lessons:
            tracked_dir_raw = _git("ls-files", "--", "memory/lessons")
            tracked_lessons = [
                l for l in tracked_dir_raw.splitlines()
                if re.fullmatch(r"memory/lessons/L-\d+\.md", l.strip())
            ]
        tracked = len(tracked_lessons) if tracked_lessons else actual
        tracked_set = {p.replace("\\", "/") for p in tracked_lessons}
        untracked_names = []
        for p in lesson_paths:
            rel = p.relative_to(REPO_ROOT).as_posix()
            if rel not in tracked_set:
                untracked_names.append(p.name)
        # Cross-runtime path normalization can diverge (e.g., /mnt vs Windows path
        # semantics). If every lesson appears "untracked" but basenames match git
        # tracked basenames, treat this as a path-normalization artifact.
        if untracked_names and len(untracked_names) == actual and tracked_lessons:
            tracked_basenames = {Path(p).name for p in tracked_lessons}
            lesson_basenames = {p.name for p in lesson_paths}
            if tracked_basenames == lesson_basenames:
                untracked_names = []
        untracked_names.sort()
        untracked = len(untracked_names)
        count_match = re.search(r"\*\*(\d+) lessons\*\*", index_text)
        claimed = None
        if count_match:
            claimed = int(count_match.group(1))
            count_includes_untracked = untracked > 0 and claimed == actual
            if tracked != claimed and not count_includes_untracked:
                results.append(("NOTICE", f"INDEX lessons {claimed} != tracked {tracked}"))
        if untracked:
            sample = ", ".join(untracked_names[:3])
            includes = claimed == actual if claimed is not None else False
            if includes:
                results.append(("NOTICE", f"{untracked} untracked lesson draft(s): {sample} (INDEX includes drafts; tracked count excludes them)"))
            else:
                results.append(("NOTICE", f"{untracked} untracked lesson draft(s): {sample} (not counted in tracked lesson total)"))

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
    actual_frontier = len(re.findall(r"^- \*\*F\d+\*\*:", frontier_text, re.MULTILINE))
    if idx_f_match:
        claimed_f = int(idx_f_match.group(1))
        if claimed_f != actual_frontier:
            results.append(("NOTICE", f"INDEX frontier count {claimed_f} != active {actual_frontier}"))

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
    """Check session-header consistency across key swarm state files."""
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
    m = re.search(r"Last updated:\s*\d{4}-\d{2}-\d{2}\s+S(\d+)\b", frontier_text)
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
    # Ahead markers are expected while a session is in progress on a dirty tree.
    if ahead and not dirty:
        results.append(("NOTICE", f"State header ahead of SESSION-LOG S{session}: {', '.join(ahead)}"))

    return results


def check_session_log_integrity() -> list[tuple[str, str]]:
    """Surface append-only log drift with low-noise integrity signals."""
    results = []
    text = _read(REPO_ROOT / "memory" / "SESSION-LOG.md")
    if not text:
        return results

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

    # Multiple entries for the same session are expected; only flag exact repeated rows.
    dup_counts: dict[str, int] = {}
    for _, row in rows:
        dup_counts[row] = dup_counts.get(row, 0) + 1
    dup_rows = [(row, n) for row, n in dup_counts.items() if n > 1]
    if dup_rows:
        sample = ", ".join(f"{row[:40]}... x{n}" for row, n in dup_rows[:3])
        suffix = "..." if len(dup_rows) > 3 else ""
        results.append(("NOTICE", f"SESSION-LOG exact duplicate row(s): {sample}{suffix}"))

    # Append-only logs should be non-decreasing in recent entries. Historical
    # legacy ordering can be noisy and is not actionable during normal runs.
    # Also allow benign backfills where an older already-seen session ID is
    # appended after a newer one during concurrent reconciliation.
    recent_window = 40
    recent_rows = rows[-recent_window:]
    non_monotonic = []
    seen_ids = {recent_rows[0][0]} if recent_rows else set()
    for i in range(1, len(recent_rows)):
        prev_sid = recent_rows[i - 1][0]
        sid = recent_rows[i][0]
        if sid < prev_sid and sid not in seen_ids:
            non_monotonic.append((prev_sid, sid))
        seen_ids.add(sid)
    if non_monotonic:
        sample = ", ".join(f"S{a}->S{b}" for a, b in non_monotonic[:5])
        suffix = "..." if len(non_monotonic) > 5 else ""
        results.append(("NOTICE", f"SESSION-LOG recent non-monotonic order: {sample}{suffix}"))

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
        sample = ", ".join(f"P-{x}" for x in uncited[:5])
        results.append(("NOTICE", f"{len(uncited)} active principle(s) with 0 citations: {sample}{'...' if len(uncited) > 5 else ''}"))
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
        results.append((
            "NOTICE",
            f"Proxy K schema baseline unavailable ({n} matching snapshot{'s' if n != 1 else ''}); run clean snapshots: {PYTHON_CMD} tools/proxy_k.py --save",
        ))
        return results

    floor_idx = 0
    for i in range(1, len(baseline)):
        if baseline[i]["total"] < baseline[i - 1]["total"]:
            floor_idx = i

    floor_entry = baseline[floor_idx]
    floor = floor_entry["total"]
    if floor <= 0:
        return results

    live_tiers: dict[str, int] = {}
    live_total = 0
    for tier, files in tiers.items():
        tier_total = sum(_token_count(REPO_ROOT / f) for f in files)
        live_tiers[tier] = tier_total
        live_total += tier_total

    # Floor should come from stable history, but severity should reflect the
    # newest recorded snapshot (dirty or clean) to avoid stale DUE/URGENT spam
    # while the tree is actively in flux.
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

    def _tier_targets() -> str:
        floor_tiers = floor_entry.get("tiers", {})
        tier_deltas = []
        for tier in sorted(live_tiers):
            delta = live_tiers.get(tier, 0) - floor_tiers.get(tier, 0)
            if delta > 0:
                tier_deltas.append(f"{tier}+{delta}")
        return f" [{', '.join(tier_deltas[:3])}]" if tier_deltas else ""

    if logged_drift > 0.06:
        # If working tree is dirty and live drift is already within threshold,
        # treat stale logged spikes as volatile and ask for a stable re-save.
        if dirty and live_drift <= 0.06:
            results.append((
                "NOTICE",
                f"Proxy K logged drift {logged_drift:.1%} ({latest_logged} vs {floor}) but live drift is {live_drift:.1%} on dirty tree; re-save clean snapshot: {PYTHON_CMD} tools/proxy_k.py --save",
            ))
        elif stale_clean_baseline:
            results.append((
                "NOTICE",
                f"Proxy K baseline S{floor_session} is stale on dirty tree (current S{current_session}); re-save clean snapshot: {PYTHON_CMD} tools/proxy_k.py --save",
            ))
        elif likely_dirty_logged:
            results.append((
                "NOTICE",
                f"Proxy K logged drift {logged_drift:.1%} ({latest_logged} vs {floor}) from likely dirty S{latest_session}; re-save: {PYTHON_CMD} tools/proxy_k.py --save",
            ))
        else:
            level = "URGENT" if logged_drift > 0.10 else "DUE"
            results.append((
                level,
                f"Proxy K drift {logged_drift:.1%} ({latest_logged} vs {floor}); run: {PYTHON_CMD} tools/compact.py",
            ))
    elif live_drift > 0.06 and dirty:
        results.append((
            "NOTICE",
            f"Proxy K live drift {live_drift:.1%} ({live_total} vs {floor}) on dirty tree{_tier_targets()}; save when stable: {PYTHON_CMD} tools/proxy_k.py --save",
        ))
    elif live_drift > 0.06:
        level = "URGENT" if live_drift > 0.10 else "DUE"
        results.append((
            level,
            f"Proxy K drift {live_drift:.1%} ({live_total} vs {floor}){_tier_targets()}; run: {PYTHON_CMD} tools/compact.py",
        ))

    return results


def check_file_graph() -> list[tuple[str, str]]:
    results = []
    structural = [
        REPO_ROOT / "SWARM.md",
        REPO_ROOT / "CLAUDE.md",
        REPO_ROOT / "beliefs" / "CORE.md",
        REPO_ROOT / "memory" / "INDEX.md",
    ]
    broken = []
    for sf in structural:
        text = _read(sf)
        if not text:
            continue
        refs = re.findall(r"`([a-zA-Z][\w\-/]+\.(?:md|py|json|sh))`", text)
        for ref in refs:
            if ref.startswith("L-") or ref.startswith("P-") or ref.startswith("B-"):
                continue
            full = REPO_ROOT / ref
            if not full.exists():
                broken.append(f"{sf.name}→{ref}")
    if broken:
        results.append(("DUE", f"{len(broken)} broken file reference(s): {', '.join(broken[:5])}"))
    return results


def build_inventory() -> dict:
    def _tools(*names: str) -> list[str]:
        return [f"tools/{name}" for name in names]

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
        "orientation": _tools("maintenance.py", "pulse.py", "context_router.py"),
        "validation": _tools("validate_beliefs.py", "check.sh"),
        "evolution": _tools("evolve.py", "swarm_test.py", "agent_swarm.py", "colony.py", "spawn_coordinator.py"),
        "inter_swarm": _tools("bulletin.py", "merge_back.py", "propagate_challenges.py"),
        "compaction": _tools("compact.py", "proxy_k.py", "frontier_decay.py"),
        "analysis": _tools("nk_analyze.py", "nk_analyze_go.py", "wiki_swarm.py"),
    }
    commands = {
        "python3": _python_command_runs("python3"),
        "python": _python_command_runs("python"),
        "git": _command_runs("git", ["--version"]),
        "bash": _command_runs("bash", ["--version"]),
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
        check_session_log_integrity,
        check_state_header_sync,
        check_cross_references,
        check_file_graph,
        check_paper_accuracy,
        check_utility,
        check_proxy_k_drift,
    ]

    # Keep --quick focused on startup-critical integrity signals.
    # check_utility() scans the full repo for citations and is the dominant
    # cost on large/WSL working trees.
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

