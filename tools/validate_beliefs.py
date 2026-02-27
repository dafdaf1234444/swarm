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

    # Fallback: parse markdown table (legacy format)
    row_pattern = re.compile(r"^\|\s*(B\d+)\s*\|(.+)$", re.MULTILINE)
    for m in row_pattern.finditer(text):
        cols = [c.strip() for c in m.group(2).split("|")]
        beliefs.append({
            "id": m.group(1),
            "statement": cols[0] if cols else "",
            "evidence": "",
            "falsification": "",
            "depends_on": [],
            "last_tested": "",
        })
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
    """Cross-check 'Depends on' vs 'Depended on by' fields for consistency."""
    issues = []
    known = {b["id"] for b in beliefs}
    # Build forward map: who depends on whom
    forward: dict[str, set[str]] = {b["id"]: set(b["depends_on"]) for b in beliefs}
    # Build reverse map from "Depended on by" fields
    reverse: dict[str, set[str]] = {b["id"]: set(b.get("depended_on_by", [])) for b in beliefs}

    for bid, deps in forward.items():
        for dep in deps:
            if dep not in known:
                continue
            # If B2 depends on B1, then B1 should list B2 in "Depended on by"
            if bid not in reverse.get(dep, set()):
                # Only warn if the target has a depended_on_by field at all
                if reverse.get(dep) is not None:
                    issues.append(
                        f"WARN DEP_SYNC: {dep} should list {bid} in 'Depended on by' "
                        f"(since {bid} depends on {dep})"
                    )
    for bid, rev_deps in reverse.items():
        for rdep in rev_deps:
            if rdep not in known:
                continue
            # If B1 says "Depended on by B2", then B2 should depend on B1
            if bid not in forward.get(rdep, set()):
                issues.append(
                    f"WARN DEP_SYNC: {rdep} should list {bid} in 'Depends on' "
                    f"(since {bid} lists {rdep} in 'Depended on by')"
                )
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


def _char_count(path: Path) -> int:
    try:
        return len(path.read_text())
    except Exception:
        return 999999


def score_onboarding(existence_ok: bool) -> tuple[int, list[str]]:
    pts, notes = 0, []
    claude_md = REPO_ROOT / "CLAUDE.md"
    index_md = REPO_ROOT / "memory" / "INDEX.md"
    frontier_md = REPO_ROOT / "tasks" / "FRONTIER.md"

    # CLAUDE.md exists and under ~300 lines (~4000 tokens)
    if claude_md.exists() and _line_count(claude_md) < 300:
        pts += 5
        notes.append("  CLAUDE.md exists and <300 lines: +5")
    else:
        notes.append("  CLAUDE.md missing or >=300 lines: +0")

    # INDEX.md exists and updated recently (within last 3 sessions by commit count)
    if index_md.exists():
        log = _git("log", "--oneline", "-3", "--", "memory/INDEX.md")
        if log:
            pts += 5
            notes.append("  INDEX.md updated within last 3 commits: +5")
        else:
            notes.append("  INDEX.md not updated recently: +0")
    else:
        notes.append("  INDEX.md missing: +0")

    # FRONTIER.md has at least 1 non-resolved open question with context
    if frontier_md.exists():
        text = frontier_md.read_text()
        open_qs = re.findall(r"^\- \*\*F\d+\*\*:.+", text, re.MULTILINE)
        if open_qs:
            pts += 5
            notes.append(f"  FRONTIER.md has {len(open_qs)} open question(s): +5")
        else:
            notes.append("  FRONTIER.md has no open questions: +0")
    else:
        notes.append("  FRONTIER.md missing: +0")

    # No broken B-ID references
    if existence_ok:
        pts += 5
        notes.append("  No broken B-ID references: +5")
    else:
        notes.append("  Broken B-ID references found: +0")

    return pts, notes


def score_belief_health(beliefs: list[dict], has_errors: bool) -> tuple[int, list[str]]:
    pts, notes = 0, []
    n_theorized = sum(1 for b in beliefs if b["evidence"] == "theorized")
    total = len(beliefs) or 1

    # Validator passes with 0 errors
    if not has_errors:
        pts += 10
        notes.append("  Validator PASS (0 errors): +10")
    else:
        notes.append("  Validator FAIL: +0")

    # Less than 60% theorized
    pct = n_theorized / total
    if pct < 0.6:
        pts += 5
        notes.append(f"  Theorized {pct:.0%} < 60%: +5")
    else:
        notes.append(f"  Theorized {pct:.0%} >= 60%: +0")

    # At least 1 belief tested within last 3 sessions (approximate: last 3 commits touching DEPS.md)
    tested_recently = any(
        b["last_tested"] and b["last_tested"].lower() != "never"
        for b in beliefs
    )
    if tested_recently:
        pts += 5
        notes.append("  At least 1 belief has a Last tested date: +5")
    else:
        notes.append("  No beliefs have been tested: +0")

    return pts, notes


def score_adaptation() -> tuple[int, list[str]]:
    pts, notes = 0, []

    # At least 1 belief modified (not just created) in last 5 DEPS.md commits
    log = _git("log", "--oneline", "-5", "--", "beliefs/DEPS.md")
    commits = [line.split()[0] for line in log.splitlines() if line.strip()] if log else []
    belief_modified = False
    for sha in commits:
        diff = _git("show", "--stat", sha, "--", "beliefs/DEPS.md")
        # If a commit changes DEPS.md and it's not the initial creation, count it
        if "insertions" in diff and "deletions" in diff:
            belief_modified = True
            break
    if belief_modified:
        pts += 10
        notes.append("  Belief modified in last 5 DEPS.md commits: +10")
    else:
        notes.append("  No belief modifications in last 5 DEPS.md commits: +0")

    # At least 1 belief has had evidence type changed in repo history
    full_log = _git("log", "-p", "--", "beliefs/DEPS.md")
    evidence_changed = bool(re.search(
        r"^[-+].*\*\*Evidence\*\*:", full_log, re.MULTILINE
    )) if full_log else False
    if evidence_changed:
        pts += 10
        notes.append("  Evidence type changed in history: +10")
    else:
        notes.append("  No evidence type changes in history: +0")

    return pts, notes


def score_context_efficiency() -> tuple[int, list[str]]:
    pts, notes = 0, []
    claude_md = REPO_ROOT / "CLAUDE.md"
    index_md = REPO_ROOT / "memory" / "INDEX.md"
    core_md = REPO_ROOT / "beliefs" / "CORE.md"

    combined_chars = sum(_char_count(f) for f in [claude_md, index_md, core_md])
    approx_tokens = combined_chars // 4
    combined_lines = sum(_line_count(f) for f in [claude_md, index_md, core_md])

    if combined_lines < 450:
        pts += 10
        notes.append(f"  Mandatory files {combined_lines} lines (<450): +10")
    else:
        notes.append(f"  Mandatory files {combined_lines} lines (>=450): +0")

    # No lesson over 20 lines
    lessons_dir = REPO_ROOT / "memory" / "lessons"
    over_20 = 0
    if lessons_dir.exists():
        for f in lessons_dir.glob("L-*.md"):
            if _line_count(f) > 20:
                over_20 += 1
    if over_20 == 0:
        pts += 10
        notes.append("  No lessons over 20 lines: +10")
    else:
        notes.append(f"  {over_20} lesson(s) over 20 lines: +0")

    return pts, notes


def score_forward_momentum() -> tuple[int, list[str]]:
    pts, notes = 0, []
    frontier_md = REPO_ROOT / "tasks" / "FRONTIER.md"

    # 3+ open questions
    open_qs = []
    if frontier_md.exists():
        text = frontier_md.read_text()
        open_qs = re.findall(r"^\- \*\*F\d+\*\*:(.+)", text, re.MULTILINE)
    if len(open_qs) >= 3:
        pts += 5
        notes.append(f"  {len(open_qs)} open frontier questions (>=3): +5")
    else:
        notes.append(f"  {len(open_qs)} open frontier questions (<3): +0")

    # At least 1 open question about something external
    external_keywords = ["RFC", "websocket", "library", "API", "code", "test",
                         "external", "build", "tool", "implement", "research"]
    has_external = any(
        any(kw.lower() in q.lower() for kw in external_keywords)
        for q in open_qs
    )
    if has_external:
        pts += 5
        notes.append("  At least 1 external-facing frontier question: +5")
    else:
        notes.append("  No external-facing frontier questions: +0")

    # Last 3 commits not all meta files
    log = _git("log", "--oneline", "-3", "--name-only")
    if log:
        recent_files = set()
        for line in log.splitlines():
            if "/" in line or "." in line:
                recent_files.add(line.strip())
        non_meta = any(
            f.startswith(("workspace/", "experiments/", "tools/"))
            or (not f.startswith(("beliefs/", "memory/", "tasks/", "CLAUDE"))
                and "." in f)
            for f in recent_files
        )
        if non_meta:
            pts += 10
            notes.append("  Recent commits touch non-meta files: +10")
        else:
            notes.append("  Last 3 commits are all meta: +0")
    else:
        notes.append("  Git history unavailable: +0")

    return pts, notes


def print_swarmability(beliefs: list[dict], has_errors: bool, existence_ok: bool):
    print("\n=== SWARMABILITY SCORE ===\n")

    total = 0

    s1, n1 = score_onboarding(existence_ok)
    print(f"1. Onboarding Clarity: {s1}/20")
    for n in n1:
        print(n)
    total += s1

    s2, n2 = score_belief_health(beliefs, has_errors)
    print(f"2. Belief Health: {s2}/20")
    for n in n2:
        print(n)
    total += s2

    s3, n3 = score_adaptation()
    print(f"3. Adaptation Rate: {s3}/20")
    for n in n3:
        print(n)
    total += s3

    s4, n4 = score_context_efficiency()
    print(f"4. Context Efficiency: {s4}/20")
    for n in n4:
        print(n)
    total += s4

    s5, n5 = score_forward_momentum()
    print(f"5. Forward Momentum: {s5}/20")
    for n in n5:
        print(n)
    total += s5

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

    # 3. Protocol files in memory/ not referenced by any .md outside themselves
    ref_corpus = ""
    for md_file in REPO_ROOT.rglob("*.md"):
        # Skip lessons (they're outputs, not structure) and the file itself
        rel = md_file.relative_to(REPO_ROOT)
        if str(rel).startswith("memory/lessons/"):
            continue
        try:
            ref_corpus += md_file.read_text() + "\n"
        except Exception:
            pass

    memory_dir = REPO_ROOT / "memory"
    skip = {"INDEX.md", "PRINCIPLES.md"}  # meta-files, always relevant
    if memory_dir.exists():
        for f in sorted(memory_dir.glob("*.md")):
            if f.name in skip:
                continue
            # Check if filename appears in the corpus (excluding self-references)
            self_text = ""
            try:
                self_text = f.read_text()
            except Exception:
                pass
            # Remove self-content from corpus for this check
            corpus_without_self = ref_corpus.replace(self_text, "")
            if f.name not in corpus_without_self:
                findings.append(
                    f"  {f.relative_to(REPO_ROOT)}: not referenced by any structural file"
                )

    return findings


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
    args = [a for a in sys.argv[1:] if a != "--quick"]
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

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
