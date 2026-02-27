import re
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


def _git(*args: str) -> str:
    try:
        r = subprocess.run(
            ["git", "-C", str(REPO_ROOT)] + list(args),
            capture_output=True,
            text=True,
            timeout=10,
        )
        return r.stdout.strip()
    except Exception:
        return ""


def _line_count(path: Path) -> int:
    try:
        return len(_read_text(path).splitlines())
    except Exception:
        return 9999


def _sc(pts, cond, msg):
    return (pts, pts if cond else 0, f"  {msg}: +{pts if cond else 0}")


def print_swarmability(beliefs: list[dict], has_errors: bool, existence_ok: bool):
    print("\n=== SWARMABILITY SCORE ===\n")
    frontier_path = REPO_ROOT / "tasks" / "FRONTIER.md"
    frontier_text = _read_text(frontier_path) if frontier_path.exists() else ""
    open_qs = re.findall(r"^\- \*\*F\d+\*\*:(.+)", frontier_text, re.MULTILINE)
    theorized_pct = sum(1 for b in beliefs if b["evidence"] == "theorized") / max(len(beliefs), 1)
    has_tested = any(b["last_tested"] and b["last_tested"].lower() != "never" for b in beliefs)

    dep_log = _git("log", "--oneline", "-5", "--", "beliefs/DEPS.md")
    belief_modified = False
    for sha in (l.split()[0] for l in dep_log.splitlines() if l.strip()):
        stat = _git("show", "--stat", sha, "--", "beliefs/DEPS.md")
        if "insertions" in stat and "deletions" in stat:
            belief_modified = True
            break
    ev_log = _git("log", "-20", "-p", "--", "beliefs/DEPS.md")
    ev_changed = bool(re.search(r"^[-+].*\*\*Evidence\*\*:", ev_log, re.MULTILINE)) if ev_log else False

    mandatory = sum(_line_count(REPO_ROOT / p) for p in ["CLAUDE.md", "beliefs/CORE.md", "memory/INDEX.md"])
    lessons_dir = REPO_ROOT / "memory" / "lessons"
    over_20 = sum(1 for f in lessons_dir.glob("L-*.md") if _line_count(f) > 20) if lessons_dir.exists() else 0

    ext_kw = ["RFC", "websocket", "library", "API", "code", "test", "external", "build", "tool", "implement", "research"]
    has_external = any(any(k.lower() in q.lower() for k in ext_kw) for q in open_qs)
    git_log = _git("log", "--oneline", "-3", "--name-only")
    recent = {l.strip() for l in git_log.splitlines() if "/" in l or "." in l} if git_log else set()
    non_meta = any(
        f.startswith(("workspace/", "experiments/", "tools/"))
        or (not f.startswith(("beliefs/", "memory/", "tasks/", "CLAUDE")) and "." in f)
        for f in recent
    )

    categories = [
        ("Onboarding Clarity", [
            _sc(5, (REPO_ROOT / "CLAUDE.md").exists() and _line_count(REPO_ROOT / "CLAUDE.md") < 300, "CLAUDE.md exists and <300 lines"),
            _sc(5, bool(_git("log", "--oneline", "-3", "--", "memory/INDEX.md")), "INDEX.md updated within last 3 commits"),
            _sc(5, bool(open_qs), f"FRONTIER.md has {len(open_qs)} open question(s)"),
            _sc(5, existence_ok, "No broken B-ID references"),
        ]),
        ("Belief Health", [
            _sc(10, not has_errors, "Validator PASS (0 errors)"),
            _sc(5, theorized_pct < 0.6, f"Theorized {theorized_pct:.0%} < 60%"),
            _sc(5, has_tested, "At least 1 belief has a Last tested date"),
        ]),
        ("Adaptation Rate", [
            _sc(10, belief_modified, "Belief modified in last 5 DEPS.md commits"),
            _sc(10, ev_changed, "Evidence type changed in history"),
        ]),
        ("Context Efficiency", [
            _sc(10, mandatory < 450, f"Mandatory files {mandatory} lines (<450)"),
            _sc(10, over_20 == 0, "No lessons over 20 lines"),
        ]),
        ("Forward Momentum", [
            _sc(5, len(open_qs) >= 3, f"{len(open_qs)} open frontier questions (>=3)"),
            _sc(5, has_external, "At least 1 external-facing frontier question"),
            _sc(10, non_meta, "Recent commits touch non-meta files"),
        ]),
    ]

    total = 0
    for i, (name, checks) in enumerate(categories, 1):
        earned = sum(c[1] for c in checks)
        max_pts = sum(c[0] for c in checks)
        print(f"{i}. {name}: {earned}/{max_pts}")
        for _, _, note in checks:
            print(note)
        total += earned
    print(f"\nSWARMABILITY: {total}/100")


def detect_entropy(beliefs: list[dict]) -> list[str]:
    findings = []
    for b in beliefs:
        if b["evidence"] == "theorized" and (not b["last_tested"] or b["last_tested"].lower() == "never"):
            findings.append(f"  {b['id']}: theorized and never tested")

    deps_path = REPO_ROOT / "beliefs" / "DEPS.md"
    superseded = set(re.findall(r"~~(B\d+)~~", _read_text(deps_path))) if deps_path.exists() else set()
    lessons_dir = REPO_ROOT / "memory" / "lessons"
    if lessons_dir.exists() and superseded:
        for f in sorted(lessons_dir.glob("L-*.md")):
            text = _read_text(f) if f.exists() else ""
            m = re.search(r"## Affected beliefs:\s*(.+)", text)
            if m:
                stale = [bid for bid in re.findall(r"B\d+", m.group(1)) if bid in superseded]
                if stale:
                    findings.append(f"  {f.name}: references superseded {', '.join(stale)}")

    refs = "".join(_read_text(p) for p in [REPO_ROOT / "CLAUDE.md", REPO_ROOT / "memory" / "INDEX.md"] if p.exists())
    skip = {"INDEX.md", "PRINCIPLES.md", "SESSION-LOG.md", "PULSE.md", "HEALTH.md"}
    memory_dir = REPO_ROOT / "memory"
    if memory_dir.exists():
        for f in sorted(memory_dir.glob("*.md")):
            if f.name not in skip and f.name not in refs:
                findings.append(f"  {f.relative_to(REPO_ROOT)}: not referenced by CLAUDE.md or INDEX.md")
    return findings


def print_entropy(beliefs: list[dict]):
    findings = detect_entropy(beliefs)
    print("\n=== ENTROPY DETECTOR ===\n")
    if findings:
        for f in findings:
            print(f)
        print(f"\nEntropy items: {len(findings)}")
    else:
        print("  No entropy detected.")
        print("\nEntropy items: 0")
