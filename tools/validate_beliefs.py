#!/usr/bin/env python3
"""Validate structural integrity of the swarm belief graph in beliefs/DEPS.md."""

import re
import sys
from pathlib import Path


def parse_beliefs(path: str) -> list[dict]:
    """Parse beliefs from DEPS.md. Supports both table and heading-based formats."""
    text = Path(path).read_text()
    beliefs = []

    # Try heading-based format first (Phase 3 format):
    # ### B1: Statement
    # - **Evidence**: observed | theorized
    # - **Falsified if**: ...
    # - **Depends on**: ...
    # - **Last tested**: ...
    heading_pattern = re.compile(
        r"^###\s+(?P<id>B\d+):\s*(?P<statement>.+?)$", re.MULTILINE
    )
    matches = list(heading_pattern.finditer(text))

    if matches:
        for i, m in enumerate(matches):
            block_start = m.end()
            block_end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            block = text[block_start:block_end]

            evidence_m = re.search(
                r"\*\*Evidence\*\*:\s*(\S+)", block, re.IGNORECASE
            )
            falsified_m = re.search(
                r"\*\*Falsified if\*\*:\s*(.+?)$", block, re.MULTILINE | re.IGNORECASE
            )
            depends_m = re.search(
                r"\*\*Depends on\*\*:\s*(.+?)$", block, re.MULTILINE | re.IGNORECASE
            )
            tested_m = re.search(
                r"\*\*Last tested\*\*:\s*(.+?)$", block, re.MULTILINE | re.IGNORECASE
            )

            dep_ids = []
            if depends_m:
                dep_text = depends_m.group(1).strip()
                if dep_text.lower() not in ("none", "n/a", "-", ""):
                    dep_ids = re.findall(r"B\d+", dep_text)

            beliefs.append({
                "id": m.group("id"),
                "statement": m.group("statement").strip(),
                "evidence": evidence_m.group(1).strip().lower() if evidence_m else "",
                "falsification": falsified_m.group(1).strip() if falsified_m else "",
                "depends_on": dep_ids,
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
    """Check that every belief has the required epistemic fields."""
    issues = []
    for b in beliefs:
        bid = b["id"]
        if b["evidence"] not in ("observed", "theorized"):
            issues.append(f"FAIL FORMAT: {bid} missing or invalid evidence type "
                          f"(got '{b['evidence']}', need 'observed' or 'theorized')")
        if not b["falsification"] or b["falsification"].lower() in ("", "none", "n/a"):
            issues.append(f"FAIL FORMAT: {bid} missing falsification condition")
        if not b["last_tested"]:
            issues.append(f"FAIL FORMAT: {bid} missing 'Last tested' field")
    return issues


def check_existence(beliefs: list[dict]) -> list[str]:
    """Every belief ID in a 'Depends on' list must exist as a defined belief."""
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
    """Detect circular dependencies via DFS."""
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


def check_orphans(beliefs: list[dict]) -> list[str]:
    """Flag beliefs that nothing depends on AND have no falsification condition."""
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


def main() -> int:
    path = sys.argv[1] if len(sys.argv) > 1 else "beliefs/DEPS.md"
    if not Path(path).exists():
        print(f"ERROR: {path} not found")
        return 1

    beliefs = parse_beliefs(path)
    if not beliefs:
        print(f"ERROR: No beliefs found in {path}")
        return 1

    all_issues: list[str] = []
    all_issues.extend(check_existence(beliefs))
    all_issues.extend(check_cycles(beliefs))
    all_issues.extend(check_orphans(beliefs))
    all_issues.extend(check_format(beliefs))

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
        return 1
    print("RESULT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
