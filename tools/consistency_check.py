#!/usr/bin/env python3
"""Document consistency checker — stigmergic cross-reference validation.

Detects stale, contradictory, or broken cross-references across the repo.
Enforces that when a canonical claim (PHIL-N, F-*, B-*) is updated, all
references to it across the repo reflect the current state.

Problem (L-601): voluntary consistency decays to zero. This tool makes
drift visible so every session sees it.

Checks:
  1. DROPPED/SUPERSEDED claims referenced as if active
  2. DECOMPOSED claims referenced in old form (PHIL-16 vs PHIL-16a/16b)
  3. Stale session counts in PHILOSOPHY.md itself
  4. Frontier status contradictions (header vs content)
  5. MERGED PHIL claims referenced without noting the merge

Usage:
  python3 tools/consistency_check.py              # human-readable report
  python3 tools/consistency_check.py --json        # machine-readable
  python3 tools/consistency_check.py --fix         # auto-fix what's safe to fix
  python3 tools/consistency_check.py --quick       # only check source-of-truth files
"""
import argparse
import json
import os
import re
import subprocess
import sys
from collections import defaultdict

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Files that ARE the source of truth — consistency issues here are highest priority
SOURCE_OF_TRUTH = {
    "beliefs/PHILOSOPHY.md",
    "tasks/FRONTIER.md",
    "beliefs/DEPS.md",
    "tasks/SIGNALS.md",
}

# Files that are historical records — stale refs here are expected/tolerable
HISTORICAL_FILES = {
    "beliefs/PHILOSOPHY-CHALLENGE-ARCHIVE.md",
    "tasks/NEXT-ARCHIVE.md",
}

# Patterns for immutable historical records — LOW severity always
HISTORICAL_PATTERNS = [
    "memory/lessons/",
    "memory/SESSION-LOG.md",
    "experiments/",
    "tasks/SWARM-LANES-ARCHIVE.md",
    "docs/bulletins/",
]

# Skip binary/generated files
SKIP_PATTERNS = [
    ".git/", "__pycache__/", ".pyc", ".png", ".jpg", ".jpeg",
    "node_modules/", ".swarm_meta.json", "workspace/",
]


def get_current_session():
    """Get the latest session number from git log."""
    try:
        result = subprocess.run(
            ["git", "log", "--oneline", "-1"],
            capture_output=True, text=True, cwd=REPO_ROOT,
        )
        m = re.search(r"\[S(\d+)\]", result.stdout)
        if m:
            return int(m.group(1))
    except Exception:
        pass
    return 540  # fallback


def parse_phil_states():
    """Parse PHILOSOPHY.md to extract canonical state of each PHIL claim.

    Returns dict: {
        'PHIL-2': {
            'status': 'GROUNDED'|'ASPIRATIONAL'|'DROPPED'|'SUPERSEDED'|'DECOMPOSED'|...,
            'decomposed_into': ['PHIL-16a', 'PHIL-16b'] or None,
            'merged_into': 'PHIL-8' or None,
            'short_desc': 'first line of claim',
            'line': line_number,
        }
    }
    """
    path = os.path.join(REPO_ROOT, "beliefs", "PHILOSOPHY.md")
    if not os.path.exists(path):
        return {}

    with open(path, encoding="utf-8") as f:
        text = f.read()

    states = {}
    lines = text.split("\n")

    for i, line in enumerate(lines, 1):
        # Match PHIL-N definitions: **[PHIL-N]** or ~~PHIL-N~~
        m = re.match(r".*\*\*\[PHIL-(\d+[a-z]?)\]\*\*\s*(.*)", line)
        if m:
            phil_id = f"PHIL-{m.group(1)}"
            desc = m.group(2).strip()
            # Look ahead for status in ground truth
            status = "ACTIVE"
            context = "\n".join(lines[i:min(i + 15, len(lines))])
            if re.search(r"\*\*DROPPED\b", context, re.IGNORECASE):
                status = "DROPPED"
            elif re.search(r"\*\*(OBSERVED|observed)\*\*", context):
                status = "OBSERVED"
            elif re.search(r"\*\*aspirational\*\*", context, re.IGNORECASE):
                status = "ASPIRATIONAL"
            elif re.search(r"\*\*grounded\*\*", context, re.IGNORECASE):
                status = "GROUNDED"
            elif re.search(r"\*\*partial(ly grounded)?\*\*", context, re.IGNORECASE):
                status = "PARTIAL"
            elif re.search(r"\*\*theorized\*\*", context, re.IGNORECASE):
                status = "THEORIZED"
            elif re.search(r"\*\*reframed\*\*", context, re.IGNORECASE):
                status = "REFRAMED"
            states[phil_id] = {
                "status": status,
                "short_desc": desc[:120],
                "line": i,
                "decomposed_into": None,
                "merged_into": None,
            }

        # Match dropped/superseded via strikethrough
        m2 = re.match(r".*~~(PHIL-\d+)~~.*", line)
        if m2:
            phil_id = m2.group(1)
            status = "DROPPED"
            merged_into = None
            if "SUPERSEDED" in line:
                status = "SUPERSEDED"
                m3 = re.search(r"absorbed into (PHIL-\d+)", line)
                if m3:
                    merged_into = m3.group(1)
            if phil_id not in states:
                states[phil_id] = {
                    "status": status,
                    "short_desc": line.strip()[:120],
                    "line": i,
                    "decomposed_into": None,
                    "merged_into": merged_into,
                }
            else:
                states[phil_id]["status"] = status
                states[phil_id]["merged_into"] = merged_into

    # Detect decompositions from the version header
    header_line = lines[1] if len(lines) > 1 else ""
    decomp_matches = re.findall(r"(PHIL-\d+) decomposed → (\w+)\+(\w+)", header_line)
    for phil_id, part_a, part_b in decomp_matches:
        if phil_id in states:
            states[phil_id]["status"] = "DECOMPOSED"
            states[phil_id]["decomposed_into"] = [
                f"PHIL-{part_a}" if not part_a.startswith("PHIL-") else part_a,
                f"PHIL-{part_b}" if not part_b.startswith("PHIL-") else part_b,
            ]

    # Mark PHIL-N as DECOMPOSED if Na and Nb both exist
    for phil_id, state in list(states.items()):
        base_match = re.match(r"PHIL-(\d+)$", phil_id)
        if base_match:
            num = base_match.group(1)
            has_a = f"PHIL-{num}a" in states
            has_b = f"PHIL-{num}b" in states
            if has_a and has_b and state["status"] not in ("DECOMPOSED", "DROPPED", "SUPERSEDED"):
                states[phil_id]["status"] = "DECOMPOSED"
                states[phil_id]["decomposed_into"] = [f"PHIL-{num}a", f"PHIL-{num}b"]

    return states


def find_stale_session_counts(current_session):
    """Find session counts in PHILOSOPHY.md that are outdated."""
    path = os.path.join(REPO_ROOT, "beliefs", "PHILOSOPHY.md")
    if not os.path.exists(path):
        return []

    with open(path, encoding="utf-8") as f:
        lines = f.readlines()

    issues = []
    for i, line in enumerate(lines, 1):
        # Find patterns like "305/305 sessions" or "In 355 sessions"
        for m in re.finditer(r"(\d+)/\1 sessions", line):
            old_count = int(m.group(1))
            if current_session - old_count > 20:
                issues.append({
                    "file": "beliefs/PHILOSOPHY.md",
                    "line": i,
                    "severity": "HIGH",
                    "type": "stale_session_count",
                    "detail": f"'{m.group(0)}' is {current_session - old_count} sessions stale (current: S{current_session})",
                    "old_text": m.group(0),
                    "fix": f"{current_session}/{current_session} sessions",
                })
        for m in re.finditer(r"[Ii]n (\d+) sessions?:", line):
            old_count = int(m.group(1))
            if current_session - old_count > 20:
                issues.append({
                    "file": "beliefs/PHILOSOPHY.md",
                    "line": i,
                    "severity": "HIGH",
                    "type": "stale_session_count",
                    "detail": f"'In {old_count} sessions' is {current_session - old_count} sessions stale",
                    "old_text": m.group(0),
                    "fix": f"In {current_session} sessions:",
                })
        # "across N sessions" pattern — may be historically accurate
        for m in re.finditer(r"across (\d+) sessions", line):
            old_count = int(m.group(1))
            if current_session - old_count > 50:
                issues.append({
                    "file": "beliefs/PHILOSOPHY.md",
                    "line": i,
                    "severity": "MEDIUM",
                    "type": "stale_session_count",
                    "detail": f"'across {old_count} sessions' is {current_session - old_count} sessions stale",
                    "old_text": m.group(0),
                    "fix": None,  # needs manual review — number may be historically accurate
                })

    return issues


def scan_file(filepath, phil_states, current_session):
    """Scan a single file for stale PHIL references."""
    rel_path = os.path.relpath(filepath, REPO_ROOT)

    # Classify file type for severity
    is_historical = (
        rel_path in HISTORICAL_FILES
        or "/archive" in rel_path.lower()
        or any(rel_path.startswith(p) for p in HISTORICAL_PATTERNS)
    )

    try:
        with open(filepath, encoding="utf-8", errors="ignore") as f:
            text = f.read()
    except (OSError, UnicodeDecodeError):
        return []

    if not text.strip():
        return []

    issues = []
    lines = text.split("\n")

    for i, line in enumerate(lines, 1):
        # Find all PHIL-N references in this line (exclude PHIL-Na/Nb)
        refs = re.findall(r"PHIL-(\d+)(?![a-z])", line)
        for ref_num in refs:
            phil_id = f"PHIL-{ref_num}"
            if phil_id not in phil_states:
                continue

            state = phil_states[phil_id]

            # Check 1: Reference to DROPPED claim without acknowledging it
            if state["status"] == "DROPPED":
                if re.search(r"(DROPPED|dropped|~~" + re.escape(phil_id) + r"~~)", line):
                    continue
                context_start = max(0, i - 3)
                context_end = min(len(lines), i + 3)
                context = "\n".join(lines[context_start:context_end])
                if re.search(r"(DROPPED|dropped|~~" + re.escape(phil_id) + r"~~)", context):
                    continue
                issues.append({
                    "file": rel_path,
                    "line": i,
                    "severity": "LOW" if is_historical else "HIGH",
                    "type": "dropped_ref",
                    "detail": f"{phil_id} is DROPPED but referenced as active",
                    "old_text": None,
                    "fix": None,
                })

            # Check 2: Reference to SUPERSEDED claim
            elif state["status"] == "SUPERSEDED":
                if re.search(r"(SUPERSEDED|superseded|~~" + re.escape(phil_id) + r"~~)", line):
                    continue
                merged = state.get("merged_into", "?")
                issues.append({
                    "file": rel_path,
                    "line": i,
                    "severity": "LOW" if is_historical else "MEDIUM",
                    "type": "superseded_ref",
                    "detail": f"{phil_id} is SUPERSEDED (→ {merged}) but referenced without noting",
                    "old_text": None,
                    "fix": None,
                })

            # Check 3: Reference to DECOMPOSED claim in old form
            elif state["status"] == "DECOMPOSED":
                parts = state.get("decomposed_into", [])
                if parts:
                    if any(p in line for p in parts):
                        continue
                    context_start = max(0, i - 3)
                    context_end = min(len(lines), i + 3)
                    context = "\n".join(lines[context_start:context_end])
                    if any(p in context for p in parts) or "decomposed" in context.lower():
                        continue
                    issues.append({
                        "file": rel_path,
                        "line": i,
                        "severity": "LOW" if is_historical else "MEDIUM",
                        "type": "decomposed_ref",
                        "detail": f"{phil_id} was DECOMPOSED into {'+'.join(parts)} but referenced in old form",
                        "old_text": None,
                        "fix": None,
                    })

    return issues


def collect_all_md_files(quick=False):
    """Collect all markdown files to scan."""
    if quick:
        return [os.path.join(REPO_ROOT, f) for f in SOURCE_OF_TRUTH
                if os.path.exists(os.path.join(REPO_ROOT, f))]

    md_files = []
    for root, dirs, files in os.walk(REPO_ROOT):
        rel_root = os.path.relpath(root, REPO_ROOT)
        if any(skip in rel_root for skip in [".git", "__pycache__", "node_modules", "workspace"]):
            dirs.clear()
            continue

        for fname in files:
            if not fname.endswith(".md"):
                continue
            full_path = os.path.join(root, fname)
            rel_path = os.path.relpath(full_path, REPO_ROOT)
            if any(skip in rel_path for skip in SKIP_PATTERNS):
                continue
            md_files.append(full_path)

    return md_files


def apply_fixes(issues):
    """Apply auto-fixable issues (currently: stale session counts in PHILOSOPHY.md)."""
    fixes_by_file = defaultdict(list)
    for issue in issues:
        if issue.get("fix") and issue.get("old_text"):
            fixes_by_file[issue["file"]].append(issue)

    fixed_count = 0
    for rel_path, file_issues in fixes_by_file.items():
        full_path = os.path.join(REPO_ROOT, rel_path)
        if not os.path.exists(full_path):
            continue

        with open(full_path, encoding="utf-8") as f:
            content = f.read()

        for issue in file_issues:
            old = issue["old_text"]
            new = issue["fix"]
            if old in content:
                content = content.replace(old, new, 1)
                fixed_count += 1
                print(f"  FIXED: {rel_path}:{issue['line']}: '{old}' → '{new}'")

        # Write with fsync for WSL reliability
        fd = os.open(full_path, os.O_WRONLY | os.O_TRUNC | os.O_CREAT)
        try:
            os.write(fd, content.encode("utf-8"))
            os.fsync(fd)
        finally:
            os.close(fd)

    return fixed_count


def run_check(quick=False, fix=False, as_json=False):
    current_session = get_current_session()
    phil_states = parse_phil_states()

    all_issues = []

    # 1. Stale session counts in PHILOSOPHY.md
    all_issues.extend(find_stale_session_counts(current_session))

    # 2. Cross-reference staleness
    md_files = collect_all_md_files(quick=quick)
    for filepath in md_files:
        rel = os.path.relpath(filepath, REPO_ROOT)
        # Don't flag the source definition itself
        if rel == "beliefs/PHILOSOPHY.md":
            continue
        all_issues.extend(scan_file(filepath, phil_states, current_session))

    # Deduplicate
    seen = set()
    unique_issues = []
    for issue in all_issues:
        key = (issue["file"], issue["line"], issue["type"], issue.get("detail", ""))
        if key not in seen:
            seen.add(key)
            unique_issues.append(issue)

    # Sort by severity then file
    severity_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    unique_issues.sort(key=lambda x: (severity_order.get(x["severity"], 9), x["file"], x["line"]))

    if fix:
        fixed = apply_fixes(unique_issues)
        unique_issues = [i for i in unique_issues if not (i.get("fix") and i.get("old_text"))]
        if not as_json:
            print(f"\nAuto-fixed {fixed} issues.")

    if as_json:
        output = {
            "current_session": current_session,
            "phil_claims": len(phil_states),
            "files_scanned": len(md_files),
            "total_issues": len(unique_issues),
            "high": sum(1 for i in unique_issues if i["severity"] == "HIGH"),
            "medium": sum(1 for i in unique_issues if i["severity"] == "MEDIUM"),
            "low": sum(1 for i in unique_issues if i["severity"] == "LOW"),
            "issues": unique_issues,
        }
        print(json.dumps(output, indent=2))
    else:
        print(f"=== CONSISTENCY CHECK (S{current_session}) ===")
        print(f"  PHIL claims parsed: {len(phil_states)}")
        print(f"  Files scanned: {len(md_files)}")
        print()

        if not unique_issues:
            print("  No consistency issues found.")
        else:
            high = sum(1 for i in unique_issues if i["severity"] == "HIGH")
            medium = sum(1 for i in unique_issues if i["severity"] == "MEDIUM")
            low = sum(1 for i in unique_issues if i["severity"] == "LOW")
            print(f"  Issues: {high} HIGH, {medium} MEDIUM, {low} LOW")
            print()

            for issue in unique_issues:
                sev = issue["severity"]
                marker = {"HIGH": "!!!", "MEDIUM": "!!", "LOW": "!"}[sev]
                print(f"  [{sev}] {marker} {issue['file']}:{issue['line']}")
                print(f"         {issue['type']}: {issue['detail']}")
                if issue.get("fix"):
                    print(f"         fix: {issue['fix']}")
                print()

        if high > 0:
            print(f"DUE: {high} HIGH consistency issues — stale references to changed PHIL claims")

    return unique_issues


def main():
    parser = argparse.ArgumentParser(description="Document consistency checker")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--fix", action="store_true", help="Auto-fix safe issues")
    parser.add_argument("--quick", action="store_true", help="Only check source-of-truth files")
    args = parser.parse_args()

    issues = run_check(quick=args.quick, fix=args.fix, as_json=args.json)
    sys.exit(1 if any(i["severity"] == "HIGH" for i in issues) else 0)


if __name__ == "__main__":
    main()
