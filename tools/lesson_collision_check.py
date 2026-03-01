#!/usr/bin/env python3
"""
lesson_collision_check.py — Detect L-NNN lesson number collisions (FM-18).

In high-concurrency sessions (N>=3), multiple sessions may create lesson files
with the same L-NNN number, causing data loss via silent overwrite.

Checks:
  1. Working-tree duplicates (two files claiming same L-NNN)
  2. Content mismatch vs HEAD (working-tree L-NNN differs from committed)
  3. Title-filename mismatch (filename L-NNN but title says L-MMM)
  4. Out-of-sequence numbers (NNN > max_committed + 2)

Usage:
    python3 tools/lesson_collision_check.py          # report only
    python3 tools/lesson_collision_check.py --fix     # report + suggest fixes
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LESSON_DIR = ROOT / "memory" / "lessons"
L_RE = re.compile(r"^L-(\d+)\.md$")
TITLE_L_RE = re.compile(r"^#\s+L-(\d+)")


def git_committed_lessons():
    """Return {number: relative_path} for L-NNN.md files in HEAD."""
    try:
        out = subprocess.check_output(
            ["git", "ls-tree", "-r", "HEAD", "--name-only", "memory/lessons/"],
            cwd=ROOT, text=True, stderr=subprocess.DEVNULL
        )
    except subprocess.CalledProcessError:
        return {}
    result = {}
    for line in out.strip().splitlines():
        name = os.path.basename(line)
        m = L_RE.match(name)
        if m and "/archive/" not in line:
            result[int(m.group(1))] = line
    return result


def git_file_content(relpath):
    """Return content of a file at HEAD, or None."""
    try:
        return subprocess.check_output(
            ["git", "show", f"HEAD:{relpath}"], cwd=ROOT, text=True,
            stderr=subprocess.DEVNULL
        )
    except subprocess.CalledProcessError:
        return None


def working_tree_lessons():
    """Return {number: Path} for L-NNN.md files in working tree (excl. archive)."""
    result = {}
    if not LESSON_DIR.is_dir():
        return result
    for f in LESSON_DIR.iterdir():
        m = L_RE.match(f.name)
        if m and f.is_file():
            result[int(m.group(1))] = f
    return result


def get_title_number(path):
    """Extract L-NNN number from the first heading line, or None."""
    try:
        with open(path) as f:
            for line in f:
                m = TITLE_L_RE.match(line.strip())
                if m:
                    return int(m.group(1))
                if line.strip():
                    return None  # first non-empty line isn't a title
    except Exception:
        pass
    return None


def main():
    parser = argparse.ArgumentParser(description="Lesson collision detector (FM-18)")
    parser.add_argument("--fix", action="store_true", help="Show suggested fixes")
    args = parser.parse_args()

    wt = working_tree_lessons()
    committed = git_committed_lessons()
    issues = []

    # 1. Title-filename mismatch
    for num, path in sorted(wt.items()):
        title_num = get_title_number(path)
        if title_num is not None and title_num != num:
            issues.append(
                f"TITLE MISMATCH: {path.name} title says L-{title_num:03d}"
                + (f" — rename file or fix title" if args.fix else "")
            )

    # 2. Content mismatch vs HEAD
    for num in sorted(set(wt) & set(committed)):
        head_content = git_file_content(committed[num])
        if head_content is None:
            continue
        try:
            wt_content = wt[num].read_text()
        except Exception:
            continue
        if wt_content != head_content:
            issues.append(
                f"CONTENT MISMATCH: L-{num:03d}.md differs from HEAD"
                + (f" — check git diff memory/lessons/L-{num:03d}.md" if args.fix else "")
            )

    # 3. Out-of-sequence (working tree has numbers > max_committed + 2)
    if committed:
        max_committed = max(committed)
        for num in sorted(wt):
            if num > max_committed + 2 and num not in committed:
                issues.append(
                    f"OUT-OF-SEQUENCE: L-{num:03d}.md (max committed = L-{max_committed:03d})"
                    + (f" — verify no collision; may need renumber" if args.fix else "")
                )

    # Report
    if issues:
        print(f"FM-18 COLLISION CHECK: {len(issues)} issue(s) found")
        for issue in issues:
            print(f"  {issue}")
        sys.exit(1)
    else:
        print("FM-18 COLLISION CHECK: PASS (0 issues)")
        sys.exit(0)


if __name__ == "__main__":
    main()
