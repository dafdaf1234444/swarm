#!/usr/bin/env python3
"""Validate structural integrity of the swarm belief graph and compute swarmability score."""

import hashlib
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def parse_beliefs(path: str) -> list[dict]:
    """Parse beliefs from DEPS.md. Supports both table and heading-based formats."""
    text = Path(path).read_text()
    beliefs = []

    heading_pattern = re.compile(
        r"^###\s+(?P<id>B\d+):\s*(?P<statement>.+?)$", re.MULTILINE
    )
    matches = list(heading_pattern.finditer(text))

    if matches:
        for i, m in enumerate(matches):
            block_start = m.end()
            block_end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            block = text[block_start:block_end]

            evidence_m = re.search(r"\*\*Evidence\*\*:\s*(\S+)", block, re.IGNORECASE)
            falsified_m = re.search(
                r"\*\*Falsified if\*\*:\s*(.+?)$", block, re.MULTILINE | re.IGNORECASE
            )
            depends_m = re.search(
                r"\*\*Depends on\*\*:\s*(.+?)$", block, re.MULTILINE | re.IGNORECASE
            )
            tested_m = re.search(
                r"\*\*Last tested\*\*:\s*(.+?)$", block, re.MULTILINE | re.IGNORECASE
            )
            depended_m = re.search(
                r"\*\*Depended on by\*\*:\s*(.+?)$", block, re.MULTILINE | re.IGNORECASE
            )

            dep_ids = []
            if depends_m:
                dep_text = depends_m.group(1).strip()
                if dep_text.lower() not in ("none", "n/a", "-", ""):
                    dep_ids = re.findall(r"B\d+", dep_text)

            rev_dep_ids = []
            if depended_m:
                rev_text = depended_m.group(1).strip()
                if rev_text.lower() not in ("none", "n/a", "-", ""):
                    rev_dep_ids = re.findall(r"B\d+", rev_text)

            beliefs.append({
                "id": m.group("id"),
                "statement": m.group("statement").strip(),
                "evidence": evidence_m.group(1).strip().lower() if evidence_m else "",
                "falsification": falsified_m.group(1).strip() if falsified_m else "",
                "depends_on": dep_ids,
                "depended_on_by": rev_dep_ids,
                "last_tested": tested_m.group(1).strip() if tested_m else "",
            })
        return beliefs

    return beliefs


def check_format(beliefs: list[dict]) -> list[str]:
    issues = []
    for b in beliefs:
        bid = b["id"]
        if b["evidence"] not in ("observed", "theorized"):
            issues.append(f"FAIL FORMAT: {bid} missing or invalid evidence type "
                          f"(got '{b['evidence']}', need 'observed' or 'theorized')")
        if not b["falsification"] or b["falsification"].lower() in ("", "none", "n/a"):
            issues.append(f"WARN FORMAT: {bid} missing falsification condition (optional for observed beliefs — F102)")
        if not b["last_tested"]:
            issues.append(f"FAIL FORMAT: {bid} missing 'Last tested' field")
    return issues


def check_existence(beliefs: list[dict]) -> list[str]:
    known_ids = {b["id"] for b in beliefs}
    issues = []
    for b in beliefs:
        for dep in b["depends_on"]:
            if dep not in known_ids:
                issues.append(
                    f"FAIL EXISTENCE: {b['id']} depends on {dep}, which is not defined"
                )
    return issues


def check_cycles(beliefs: list[dict]) -> list[str]:
    adj: dict[str, list[str]] = {b["id"]: b["depends_on"] for b in beliefs}
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {bid: WHITE for bid in adj}
    issues = []

    def dfs(node: str, path: list[str]) -> None:
        color[node] = GRAY
        for dep in adj.get(node, []):
            if dep not in color:
                continue
            if color[dep] == GRAY:
                cycle_start = path.index(dep)
                cycle = " -> ".join(path[cycle_start:] + [dep])
                issues.append(f"FAIL CYCLE: circular dependency: {cycle}")
            elif color[dep] == WHITE:
                dfs(dep, path + [dep])
        color[node] = BLACK

    for bid in adj:
        if color[bid] == WHITE:
            dfs(bid, [bid])
    return issues


def check_dep_consistency(beliefs: list[dict]) -> list[str]:
    """Cross-check Depends on vs Depended on by fields."""
    issues = []
    known = {b["id"] for b in beliefs}
    forward: dict[str, set[str]] = {b["id"]: set(b["depends_on"]) for b in beliefs}
    reverse: dict[str, set[str]] = {b["id"]: set(b.get("depended_on_by", [])) for b in beliefs}

    for bid, deps in forward.items():
        for dep in deps:
            if dep in known and bid not in reverse.get(dep, set()) and reverse.get(dep) is not None:
                issues.append(f"WARN DEP_SYNC: {dep} should list {bid} in 'Depended on by'")
    for bid, rev_deps in reverse.items():
        for rdep in rev_deps:
            if rdep in known and bid not in forward.get(rdep, set()):
                issues.append(f"WARN DEP_SYNC: {rdep} should list {bid} in 'Depends on'")
    return issues


def check_orphans(beliefs: list[dict]) -> list[str]:
    depended_on: set[str] = set()
    for b in beliefs:
        depended_on.update(b["depends_on"])
    issues = []
    for b in beliefs:
        if b["id"] not in depended_on and not b["falsification"]:
            issues.append(
                f"WARN ORPHAN: {b['id']} has no dependents and no falsification condition"
            )
    return issues


# --- Swarmability Scoring ---

def _git(*args: str) -> str:
    """Run a git command in the repo root. Returns stdout or empty on failure."""
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
        return 9999


def _sc(pts, cond, msg):
    """Score check: returns (max_pts, earned, note)."""
    return (pts, pts if cond else 0, f"  {msg}: +{pts if cond else 0}")


def print_swarmability(beliefs: list[dict], has_errors: bool, existence_ok: bool):
    print("\n=== SWARMABILITY SCORE ===\n")

    # Pre-compute shared state
    frontier_path = REPO_ROOT / "tasks" / "FRONTIER.md"
    frontier_text = frontier_path.read_text() if frontier_path.exists() else ""
    open_qs = re.findall(r"^\- \*\*F\d+\*\*:(.+)", frontier_text, re.MULTILINE)
    theorized_pct = sum(1 for b in beliefs if b["evidence"] == "theorized") / max(len(beliefs), 1)
    has_tested = any(b["last_tested"] and b["last_tested"].lower() != "never" for b in beliefs)

    # Adaptation: belief modifications in recent commits
    dep_log = _git("log", "--oneline", "-5", "--", "beliefs/DEPS.md")
    belief_modified = False
    for sha in (l.split()[0] for l in dep_log.splitlines() if l.strip()):
        stat = _git("show", "--stat", sha, "--", "beliefs/DEPS.md")
        if "insertions" in stat and "deletions" in stat:
            belief_modified = True
            break
    ev_log = _git("log", "-20", "-p", "--", "beliefs/DEPS.md")
    ev_changed = bool(re.search(r"^[-+].*\*\*Evidence\*\*:", ev_log, re.MULTILINE)) if ev_log else False

    # Context efficiency
    mandatory_lines = sum(_line_count(REPO_ROOT / p) for p in ["CLAUDE.md", "beliefs/CORE.md", "memory/INDEX.md"])
    lessons_dir = REPO_ROOT / "memory" / "lessons"
    over_20 = sum(1 for f in lessons_dir.glob("L-*.md") if _line_count(f) > 20) if lessons_dir.exists() else 0

    # Forward momentum
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
            _sc(10, mandatory_lines < 450, f"Mandatory files {mandatory_lines} lines (<450)"),
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


# --- Entropy Detection ---

def detect_entropy(beliefs: list[dict]) -> list[str]:
    """Detect entropy accumulation: stale beliefs, orphaned files, drifted lessons."""
    findings = []

    # 1. Stale beliefs: theorized AND never tested
    for b in beliefs:
        if b["evidence"] == "theorized" and (
            not b["last_tested"] or b["last_tested"].lower() == "never"
        ):
            findings.append(f"  {b['id']}: theorized and never tested")

    # 2. Lessons referencing superseded beliefs
    deps_path = REPO_ROOT / "beliefs" / "DEPS.md"
    superseded: set[str] = set()
    if deps_path.exists():
        superseded = set(re.findall(r"~~(B\d+)~~", deps_path.read_text()))

    lessons_dir = REPO_ROOT / "memory" / "lessons"
    if lessons_dir.exists() and superseded:
        for f in sorted(lessons_dir.glob("L-*.md")):
            try:
                text = f.read_text()
            except Exception:
                continue
            affected_m = re.search(r"## Affected beliefs:\s*(.+)", text)
            if affected_m:
                affected_ids = re.findall(r"B\d+", affected_m.group(1))
                stale = [bid for bid in affected_ids if bid in superseded]
                if stale:
                    findings.append(
                        f"  {f.name}: references superseded {', '.join(stale)}"
                    )

    # 3. Protocol files in memory/ not referenced by CLAUDE.md or INDEX.md
    structural_refs = ""
    for ref_file in [REPO_ROOT / "CLAUDE.md", REPO_ROOT / "memory" / "INDEX.md"]:
        try:
            structural_refs += ref_file.read_text()
        except Exception:
            pass

    memory_dir = REPO_ROOT / "memory"
    skip = {"INDEX.md", "PRINCIPLES.md", "SESSION-LOG.md", "PULSE.md", "HEALTH.md"}
    if memory_dir.exists():
        for f in sorted(memory_dir.glob("*.md")):
            if f.name in skip:
                continue
            if f.name not in structural_refs:
                findings.append(f"  {f.relative_to(REPO_ROOT)}: not referenced by CLAUDE.md or INDEX.md")

    return findings


def cascade_check(beliefs: list[dict], changed_id: str) -> list[str]:
    """F110-A2: Flag downstream beliefs needing re-review after a change."""
    issues = []
    by_id = {b["id"]: b for b in beliefs}

    if changed_id not in by_id:
        issues.append(f"FAIL CASCADE: Unknown belief ID '{changed_id}'")
        return issues

    # Build forward graph from depends_on entries
    forward: dict[str, list[str]] = {}
    for b in beliefs:
        for dep in b.get("depends_on", []):
            forward.setdefault(dep, []).append(b["id"])

    # BFS from changed_id
    visited: set[str] = set()
    queue = [changed_id]
    downstream: list[str] = []
    while queue:
        node = queue.pop(0)
        for child in forward.get(node, []):
            if child not in visited:
                visited.add(child)
                downstream.append(child)
                queue.append(child)

    if not downstream:
        issues.append(f"INFO CASCADE: {changed_id} has no downstream beliefs — no cascade needed")
        return issues

    changed = by_id[changed_id]
    changed_date = changed.get("last_tested", "")[:10]

    for did in downstream:
        dep = by_id[did]
        dep_date = dep.get("last_tested", "")[:10]
        stmt_preview = dep["statement"][:55].rstrip()
        if not dep_date or (changed_date and dep_date < changed_date):
            issues.append(
                f"WARN STALE: {did} ('{stmt_preview}') depends on changed {changed_id} — "
                f"last reviewed {dep_date or 'never'} vs {changed_id} updated {changed_date}. Review."
            )
        else:
            issues.append(
                f"INFO CASCADE: {did} last reviewed {dep_date} ≥ {changed_id} date {changed_date} — OK"
            )

    return issues


def check_identity() -> list[str]:
    """Check that CORE.md hasn't drifted from its stored constitutional hash (F110-B3)."""
    index_md = REPO_ROOT / "memory" / "INDEX.md"
    core_md = REPO_ROOT / "beliefs" / "CORE.md"

    if not index_md.exists() or not core_md.exists():
        return []

    index_text = index_md.read_text()
    m = re.search(r"<!--\s*core_md_hash:\s*([a-f0-9]{64})\s*-->", index_text)
    if not m:
        return []  # Hash not yet stored — not an error; run renew_identity.py to add it

    stored_hash = m.group(1)
    current_hash = hashlib.sha256(core_md.read_bytes()).hexdigest()

    if stored_hash != current_hash:
        return [
            f"FAIL IDENTITY: CORE.md has changed without renewal — "
            f"run tools/renew_identity.py after intentional changes "
            f"(stored={stored_hash[:12]}..., current={current_hash[:12]}...)"
        ]
    return []


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


# --- Main ---

def main() -> int:
    quick = "--quick" in sys.argv
    raw_args = [a for a in sys.argv[1:] if a != "--quick"]

    # Extract --changed=B-ID or --changed B-ID flag (F110-A2 cascade check)
    changed_id = None
    args = []
    skip_next = False
    for i, a in enumerate(raw_args):
        if skip_next:
            skip_next = False
            continue
        if a.startswith("--changed="):
            changed_id = a.split("=", 1)[1]
        elif a == "--changed" and i + 1 < len(raw_args):
            changed_id = raw_args[i + 1]
            skip_next = True
        else:
            args.append(a)

    path = args[0] if args else "beliefs/DEPS.md"
    if not Path(path).exists():
        print(f"ERROR: {path} not found")
        return 1

    beliefs = parse_beliefs(path)
    if not beliefs:
        print(f"ERROR: No beliefs found in {path}")
        return 1

    all_issues: list[str] = []
    existence_issues = check_existence(beliefs)
    all_issues.extend(existence_issues)
    all_issues.extend(check_cycles(beliefs))
    all_issues.extend(check_orphans(beliefs))
    all_issues.extend(check_dep_consistency(beliefs))
    all_issues.extend(check_format(beliefs))
    all_issues.extend(check_identity())

    n_observed = sum(1 for b in beliefs if b["evidence"] == "observed")
    n_theorized = sum(1 for b in beliefs if b["evidence"] == "theorized")

    for issue in all_issues:
        print(issue)

    fails = [i for i in all_issues if i.startswith("FAIL")]
    warns = [i for i in all_issues if i.startswith("WARN")]

    print()
    print(f"Summary: {len(beliefs)} beliefs, {n_observed} observed, "
          f"{n_theorized} theorized, {len(fails)} errors, {len(warns)} warnings")

    if fails:
        print("RESULT: FAIL")
        exit_code = 1
    else:
        print("RESULT: PASS")
        exit_code = 0

    if not quick:
        # Swarmability score is informational — does not affect exit code
        print_swarmability(beliefs, bool(fails), not existence_issues)

        # Entropy detection — tracks decay, not just growth
        print_entropy(beliefs)

    # Cascade check: --changed=B-ID flag (F110-A2)
    if changed_id:
        print(f"\n=== CASCADE CHECK ({changed_id} changed) ===")
        for issue in cascade_check(beliefs, changed_id):
            print(issue)

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
