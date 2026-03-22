#!/usr/bin/env python3
"""mutation_classifier.py — Classify lesson changes as point/structural/neutral.

Completes F-DNA1 slot 12/12: per-change mutation classification at knowledge-unit
level (vs session-level in change_quality.py). Enables Darwinian tracking of how
individual lessons evolve across sessions.

Mutation types:
  POINT      — Small correction/addition (≤5 content lines, meaning preserved)
  STRUCTURAL — Major rewrite, level/domain change, rule modification
  NEUTRAL    — Formatting, whitespace, template conformance only

Usage:
  python3 tools/mutation_classifier.py              # last 20 lesson changes
  python3 tools/mutation_classifier.py --last N     # last N commits with lesson changes
  python3 tools/mutation_classifier.py --json       # machine-readable output
  python3 tools/mutation_classifier.py --summary    # aggregate mutation statistics

Related: F-DNA1, L-1198, change_quality.py (session-level), L-601
"""

import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).parent.parent

# Sections that carry meaning (changes here are structural)
STRUCTURAL_SECTIONS = {"## Finding", "## What happened", "## What we learned",
                       "## Rule", "## Predictions", "# L-"}
# Header fields that carry metadata
HEADER_FIELDS = {"Session:", "Domain:", "Sharpe:", "Level:", "Confidence:",
                 "Cites:", "External:", "Frontier:"}


def get_lesson_diffs(last_n: int = 20) -> list[dict]:
    """Get git diffs of L-*.md files from recent commits."""
    # Get commits that touched lesson files
    result = subprocess.run(
        ["git", "log", f"--max-count={last_n * 3}", "--format=%H %s",
         "--diff-filter=M", "--", "memory/lessons/L-*.md"],
        capture_output=True, text=True, cwd=ROOT,
    )
    if result.returncode != 0:
        return []

    diffs = []
    seen = 0
    for line in result.stdout.strip().splitlines():
        if seen >= last_n:
            break
        parts = line.split(" ", 1)
        if len(parts) < 2:
            continue
        commit_hash, message = parts

        # Get diff for this commit's lesson files
        diff_result = subprocess.run(
            ["git", "diff", f"{commit_hash}~1", commit_hash, "--",
             "memory/lessons/L-*.md"],
            capture_output=True, text=True, cwd=ROOT,
        )
        if diff_result.returncode != 0 or not diff_result.stdout.strip():
            continue

        # Parse per-file diffs
        current_file = None
        file_diffs: dict[str, dict] = {}
        for dline in diff_result.stdout.splitlines():
            if dline.startswith("diff --git"):
                m = re.search(r"b/(memory/lessons/L-\d+\.md)", dline)
                if m:
                    current_file = m.group(1)
                    file_diffs[current_file] = {
                        "added": [], "removed": [], "file": current_file
                    }
            elif current_file and dline.startswith("+") and not dline.startswith("+++"):
                file_diffs[current_file]["added"].append(dline[1:])
            elif current_file and dline.startswith("-") and not dline.startswith("---"):
                file_diffs[current_file]["removed"].append(dline[1:])

        for path, fd in file_diffs.items():
            fd["commit"] = commit_hash[:8]
            fd["message"] = message
            diffs.append(fd)
            seen += 1

    return diffs


def classify_mutation(diff: dict) -> dict:
    """Classify a single lesson diff as point/structural/neutral."""
    added = diff["added"]
    removed = diff["removed"]

    # Filter out blank lines for content analysis
    content_added = [l for l in added if l.strip()]
    content_removed = [l for l in removed if l.strip()]

    # Check if only whitespace/blank-line changes
    added_stripped = {l.strip() for l in added}
    removed_stripped = {l.strip() for l in removed}
    if added_stripped == removed_stripped or (not content_added and not content_removed):
        return {**diff, "type": "NEUTRAL", "reason": "whitespace/formatting only"}

    # Check if structural sections were modified
    structural_hit = False
    structural_reasons = []
    for line in content_added + content_removed:
        for section in STRUCTURAL_SECTIONS:
            if line.strip().startswith(section):
                structural_hit = True
                structural_reasons.append(section)

    # Check for title change (line starting with "# L-")
    title_changed = any(l.strip().startswith("# L-") for l in content_added + content_removed)

    # Check for level/domain/sharpe changes in header
    header_changes = []
    for line in content_added + content_removed:
        for field in HEADER_FIELDS:
            if field in line:
                header_changes.append(field)

    # Count content line changes
    n_content = len(content_added) + len(content_removed)

    # Classification logic
    if title_changed:
        return {**diff, "type": "STRUCTURAL", "reason": "title changed",
                "content_lines": n_content}

    # Level or domain change in header = structural
    level_domain_change = any(f in header_changes
                             for f in ["Level:", "Domain:", "Sharpe:"])
    if level_domain_change:
        return {**diff, "type": "STRUCTURAL",
                "reason": f"header metadata changed: {header_changes}",
                "content_lines": n_content}

    # Rule or Finding section content changed with >3 content lines = structural
    if structural_hit and n_content > 3:
        return {**diff, "type": "STRUCTURAL",
                "reason": f"core section(s) modified: {structural_reasons}",
                "content_lines": n_content}

    # Large change volume = structural
    if n_content > 10:
        return {**diff, "type": "STRUCTURAL",
                "reason": f"large change volume ({n_content} content lines)",
                "content_lines": n_content}

    # Cites/External header additions = point mutation
    if all(f in ("Cites:", "External:") for f in header_changes) and not structural_hit:
        return {**diff, "type": "POINT",
                "reason": "citation/external reference update",
                "content_lines": n_content}

    # Small content changes = point
    if n_content <= 5:
        return {**diff, "type": "POINT",
                "reason": f"small edit ({n_content} content lines)",
                "content_lines": n_content}

    # Medium changes touching structural sections = structural
    if structural_hit:
        return {**diff, "type": "STRUCTURAL",
                "reason": f"core section(s) modified: {structural_reasons}",
                "content_lines": n_content}

    # Default: point mutation for moderate non-structural changes
    return {**diff, "type": "POINT",
            "reason": f"moderate edit ({n_content} content lines, non-structural)",
            "content_lines": n_content}


def main():
    args = sys.argv[1:]
    as_json = "--json" in args
    summary_mode = "--summary" in args
    last_n = 20

    for i, a in enumerate(args):
        if a == "--last" and i + 1 < len(args):
            last_n = int(args[i + 1])

    diffs = get_lesson_diffs(last_n)
    if not diffs:
        print("No lesson modifications found in recent git history.")
        return

    classified = [classify_mutation(d) for d in diffs]

    if as_json:
        output = {
            "total": len(classified),
            "counts": dict(Counter(c["type"] for c in classified)),
            "mutations": [
                {"file": c["file"], "type": c["type"], "reason": c["reason"],
                 "commit": c["commit"], "content_lines": c.get("content_lines", 0)}
                for c in classified
            ],
        }
        print(json.dumps(output, indent=2))
        return

    counts = Counter(c["type"] for c in classified)
    total = len(classified)

    print(f"=== MUTATION CLASSIFIER — F-DNA1 slot 12/12 ===\n")
    print(f"  Analyzed: {total} lesson modifications")
    print(f"  POINT:      {counts.get('POINT', 0):3d} ({counts.get('POINT', 0)/max(1,total)*100:.0f}%)")
    print(f"  STRUCTURAL: {counts.get('STRUCTURAL', 0):3d} ({counts.get('STRUCTURAL', 0)/max(1,total)*100:.0f}%)")
    print(f"  NEUTRAL:    {counts.get('NEUTRAL', 0):3d} ({counts.get('NEUTRAL', 0)/max(1,total)*100:.0f}%)")

    if summary_mode:
        return

    print(f"\n--- Recent mutations ---")
    for c in classified:
        fname = Path(c["file"]).name
        lines = c.get("content_lines", 0)
        print(f"  [{c['type']:10s}] {fname:15s} ({lines:2d}L) {c['reason']}")
        print(f"             commit: {c['commit']} {c['message'][:60]}")


if __name__ == "__main__":
    main()
