#!/usr/bin/env python3
"""doc_freshness.py — Detect stale numerical claims in documentation files.

Scans key docs (README.md, docs/*.md, bridge files) for hardcoded session counts,
lesson counts, principle counts, and other metrics that drift as the swarm grows.
Compares against live counts from the repo.

Only flags "current-state" claims (e.g. "498 sessions", "1181 lessons") — skips
historical references, version logs, small numbers (<50), and lines with temporal
markers like "by S305" or "at session 10".

Usage:
    python3 tools/doc_freshness.py            # report stale claims
    python3 tools/doc_freshness.py --fix      # auto-fix what it can
    python3 tools/doc_freshness.py --dry-run  # show fixes without applying

Suggested periodic: every 15 sessions.
"""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIX = "--fix" in sys.argv
DRY = "--dry-run" in sys.argv

# Files to scan for stale metrics
SCAN_FILES = [
    "README.md",
    "docs/HOW-TO-SWARM.md",
    "docs/QUESTIONS.md",
    "docs/HUMAN-GUIDE.md",
    "AGENTS.md",
    "GEMINI.md",
]

# Files with version history — only scan header/summary sections
HEADER_ONLY_FILES = {
    "docs/PAPER.md",  # version log lines are historical, not current claims
}

# Minimum number to flag — small numbers like "10 sessions" are usually
# references to intervals/thresholds, not current-state claims
MIN_FLAGGABLE = {
    "sessions": 200,
    "lessons": 200,
    "principles": 50,
    "beliefs": 10,
    "domains": 20,
    "tools": 30,
    "commits": 500,
}

# Line patterns that indicate historical/contextual reference, not current claim
HISTORICAL_PATTERNS = [
    re.compile(r"\b(?:by|at|after|before|around|since|until|from)\s+S\d+", re.I),
    re.compile(r"\bfrom\s+[\d,]+\s+sessions?\b", re.I),  # "from 1,000 sessions of..."
    re.compile(r"\bS\d+[-–]\s*S\d+", re.I),  # "S100-S200" range
    re.compile(r"\bv\d+\.\d+", re.I),  # version numbers
    re.compile(r"\bevery\s+\d+\s+sessions?\b", re.I),  # "every 20 sessions"
    re.compile(r"\bper\s+\d+\s+sessions?\b", re.I),  # "per 10 sessions"
    re.compile(r"\blast\s+\d+\s+sessions?\b", re.I),  # "last 10 sessions"
    re.compile(r"\bnext\s+\d+\s+sessions?\b", re.I),  # "next 50 sessions"
    re.compile(r"\b\d+[-–]\d+\s+sessions?\b", re.I),  # "10-20 sessions" range
    re.compile(r"^\s*\|.*\|.*\|", re.I),  # table rows with multiple columns (version tables)
    re.compile(r"n\s*[=≈~]\s*\d+", re.I),  # "n=849" sample sizes
]


def live_counts():
    """Get current counts from the repo."""
    counts = {}

    # Lessons: count L-*.md files
    lesson_dir = ROOT / "memory" / "lessons"
    if lesson_dir.is_dir():
        counts["lessons"] = len(list(lesson_dir.glob("L-*.md")))

    # Principles: parse header count from PRINCIPLES.md (authoritative)
    princ_file = ROOT / "memory" / "PRINCIPLES.md"
    if princ_file.exists():
        header = princ_file.read_text(errors="replace")[:500]
        m = re.search(r"(\d+)\s+live\s+principles", header)
        if m:
            counts["principles"] = int(m.group(1))

    # Beliefs: count PHIL-N entries in PHILOSOPHY.md
    phil_file = ROOT / "beliefs" / "PHILOSOPHY.md"
    if phil_file.exists():
        text = phil_file.read_text(errors="replace")
        counts["beliefs"] = len(re.findall(r"\*\*\[PHIL-\d+\]\*\*", text))

    # Domains: count directories
    domains_dir = ROOT / "domains"
    if domains_dir.is_dir():
        counts["domains"] = len([d for d in domains_dir.iterdir() if d.is_dir()])

    # Sessions: from recent git log (scan last 10 commits for S-number)
    try:
        r = subprocess.run(
            ["git", "-C", str(ROOT), "log", "--oneline", "-10", "--format=%s"],
            capture_output=True, text=True, timeout=10
        )
        if r.returncode == 0:
            for line in r.stdout.strip().split("\n"):
                m = re.search(r"\[S(\d+)", line)
                if m:
                    counts["sessions"] = int(m.group(1))
                    break
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    # Commits
    try:
        r = subprocess.run(
            ["git", "-C", str(ROOT), "rev-list", "--count", "HEAD"],
            capture_output=True, text=True, timeout=10
        )
        if r.returncode == 0:
            counts["commits"] = int(r.stdout.strip())
    except (subprocess.TimeoutExpired, FileNotFoundError, ValueError):
        pass

    # Tools: count active .py and .sh in tools/ (exclude archive, tests)
    tools_dir = ROOT / "tools"
    if tools_dir.is_dir():
        py = len([f for f in tools_dir.glob("*.py") if not f.name.startswith("test_")])
        sh = len(list(tools_dir.glob("*.sh")))
        counts["tools"] = py + sh

    return counts


# Patterns that embed specific counts in docs
# Each: (regex_pattern, count_key, description, threshold_pct)
CLAIM_PATTERNS = [
    (r"(\d[\d,]+)\s+sessions?\b", "sessions", "session count", 5),
    (r"(\d[\d,]+)\s+lessons?\b", "lessons", "lesson count", 5),
    (r"(\d[\d,]+)\s+principles?\b", "principles", "principle count", 5),
    (r"(\d[\d,]+)\s+beliefs?\b", "beliefs", "belief count", 15),
    (r"(\d[\d,]+)\s+(?:knowledge )?domains?\b", "domains", "domain count", 15),
    (r"(\d[\d,]+)\s+(?:active )?tools?\b", "tools", "tool count", 15),
    (r"([\d,]+)\+?\s+commits?\b", "commits", "commit count", 15),
]


def parse_number(s):
    return int(s.replace(",", ""))


def format_number(n, original):
    """Format number matching the style of the original (with/without commas)."""
    if "," in original:
        return f"{n:,}"
    return str(n)


def is_historical_line(line):
    """Check if a line contains historical/contextual references that shouldn't be updated."""
    for pat in HISTORICAL_PATTERNS:
        if pat.search(line):
            return True
    return False


def scan_file(filepath, counts, header_only=False):
    """Scan a file for stale numerical claims. Returns list of findings."""
    if not filepath.exists():
        return []

    text = filepath.read_text(errors="replace")
    lines = text.split("\n")
    findings = []
    in_code_block = False

    for i, line in enumerate(lines, 1):
        # Track code blocks
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        # For header-only files, stop after first ## section
        if header_only and i > 30:
            break

        # Skip historical/contextual lines
        if is_historical_line(line):
            continue

        for pattern, key, desc, threshold in CLAIM_PATTERNS:
            if key not in counts:
                continue
            for m in re.finditer(pattern, line, re.IGNORECASE):
                claimed = parse_number(m.group(1))
                actual = counts[key]
                if actual == 0:
                    continue

                # Skip small numbers (likely thresholds/intervals, not current-state claims)
                min_val = MIN_FLAGGABLE.get(key, 50)
                if claimed < min_val:
                    continue

                drift_pct = abs(claimed - actual) / actual * 100
                if drift_pct > threshold and abs(claimed - actual) > 5:
                    findings.append({
                        "file": str(filepath.relative_to(ROOT)),
                        "line": i,
                        "desc": desc,
                        "claimed": claimed,
                        "actual": actual,
                        "drift_pct": drift_pct,
                        "match_text": m.group(0),
                        "match_start": m.start(),
                        "original_number": m.group(1),
                    })

    return findings


def fix_file(filepath, findings, counts):
    """Apply fixes to a file."""
    if not findings:
        return False

    text = filepath.read_text(errors="replace")
    lines = text.split("\n")

    changes = 0
    for f in sorted(findings, key=lambda x: (x["line"], -x["match_start"]), reverse=True):
        line_idx = f["line"] - 1
        if line_idx >= len(lines):
            continue
        old_num = f["original_number"]
        new_num = format_number(f["actual"], old_num)
        old_line = lines[line_idx]
        new_line = old_line.replace(f["match_text"], f["match_text"].replace(old_num, new_num), 1)
        if new_line != old_line:
            lines[line_idx] = new_line
            changes += 1

    if changes > 0:
        new_text = "\n".join(lines)
        if not DRY:
            filepath.write_text(new_text)
        return True
    return False


def main():
    counts = live_counts()

    if not any(v for v in counts.values()):
        print("ERROR: Could not determine live counts")
        return 1

    print(f"Live counts: {', '.join(f'{k}={v}' for k, v in sorted(counts.items()))}")
    print()

    all_findings = []
    for rel_path in SCAN_FILES:
        filepath = ROOT / rel_path
        findings = scan_file(filepath, counts)
        all_findings.extend(findings)
    for rel_path in HEADER_ONLY_FILES:
        filepath = ROOT / rel_path
        findings = scan_file(filepath, counts, header_only=True)
        all_findings.extend(findings)

    if not all_findings:
        print("OK: No stale numerical claims detected")
        return 0

    print(f"STALE: {len(all_findings)} claim(s) drifted beyond threshold:\n")
    for f in all_findings:
        status = "FIXABLE" if FIX or DRY else "STALE"
        print(f"  [{status}] {f['file']}:{f['line']} — {f['desc']}: "
              f"claims {f['claimed']}, actual {f['actual']} "
              f"({f['drift_pct']:.0f}% drift)")

    if FIX or DRY:
        fixed_files = set()
        for rel_path in list(SCAN_FILES) + list(HEADER_ONLY_FILES):
            filepath = ROOT / rel_path
            file_findings = [f for f in all_findings if f["file"] == rel_path]
            if fix_file(filepath, file_findings, counts):
                fixed_files.add(rel_path)

        action = "Would fix" if DRY else "Fixed"
        if fixed_files:
            print(f"\n{action}: {', '.join(sorted(fixed_files))}")
        return 0

    print(f"\nRun with --fix to auto-update, or --dry-run to preview.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
