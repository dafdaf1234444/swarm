#!/usr/bin/env python3
"""FM-25 defense: detect level concentration in lesson production.

Monitors rolling-window level distribution to surface concentration risk.
When L2 concentration exceeds threshold or L3+ diversity drops, fires NOTICE.
Cross-references FM-37 inflation flags when available.

Usage:
  python3 tools/level_concentration_check.py              # full report
  python3 tools/level_concentration_check.py --staged      # check staged lessons only (for check.sh)
  python3 tools/level_concentration_check.py --window 20   # rolling window size (sessions)
  python3 tools/level_concentration_check.py --json        # JSON output
"""
import argparse
import glob
import os
import re
import subprocess
import sys
import json
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent.parent
LESSONS_DIR = ROOT / "memory" / "lessons"

# Thresholds
L2_CONCENTRATION_WARN = 0.50   # Warn if L2 > 50% of recent labeled lessons
L3PLUS_DIVERSITY_WARN = 0.25   # Warn if L3+ < 25% (suggests measurement dominance)
NO_LEVEL_WARN = 0.20           # Warn if >20% recent lessons lack Level header
WINDOW_SESSIONS = 20           # Default rolling window


def parse_lesson_metadata(path):
    """Extract session number and level from a lesson file."""
    try:
        with open(path, encoding="utf-8") as f:
            content = f.read(2000)  # Only need header
    except (OSError, UnicodeDecodeError):
        return None, None

    session_match = re.search(r'Session:\s*S(\d+)', content)
    session = int(session_match.group(1)) if session_match else None

    level_match = re.search(r'Level:\s*(L[1-5])', content)
    level = level_match.group(1) if level_match else None

    return session, level


def get_current_session():
    """Derive current session from NEXT.md or git log."""
    next_path = ROOT / "tasks" / "NEXT.md"
    if next_path.exists():
        text = next_path.read_text(encoding="utf-8")
        m = re.search(r'S(\d+)', text[:200])
        if m:
            return int(m.group(1))
    # Fallback: git log
    try:
        out = subprocess.check_output(
            ["git", "log", "--oneline", "-1"],
            cwd=str(ROOT), text=True, timeout=5
        )
        m = re.search(r'\[S(\d+)\]', out)
        if m:
            return int(m.group(1))
    except Exception:
        pass
    return 475  # Safe fallback


def get_staged_lessons():
    """Get list of staged lesson files from git."""
    try:
        out = subprocess.check_output(
            ["git", "diff", "--cached", "--name-only"],
            cwd=str(ROOT), text=True, timeout=5
        )
        return [
            ROOT / line.strip()
            for line in out.strip().split('\n')
            if line.strip().startswith("memory/lessons/L-")
        ]
    except Exception:
        return []


def scan_lessons(window=WINDOW_SESSIONS, staged_only=False):
    """Scan lessons in rolling window and compute level distribution."""
    current = get_current_session()
    min_session = current - window

    if staged_only:
        files = get_staged_lessons()
    else:
        files = sorted(LESSONS_DIR.glob("L-*.md"))

    results = []
    for f in files:
        session, level = parse_lesson_metadata(f)
        if session is None:
            continue
        if not staged_only and session < min_session:
            continue
        results.append({
            "file": f.name,
            "session": session,
            "level": level,
        })

    return results


def compute_distribution(lessons):
    """Compute level distribution and concentration metrics."""
    total = len(lessons)
    if total == 0:
        return {"total": 0, "distribution": {}, "warnings": []}

    level_counts = Counter()
    no_level = 0
    for l in lessons:
        if l["level"]:
            level_counts[l["level"]] += 1
        else:
            no_level += 1

    labeled = total - no_level
    distribution = {}
    for lvl in ["L1", "L2", "L3", "L4", "L5"]:
        count = level_counts.get(lvl, 0)
        pct = count / labeled * 100 if labeled > 0 else 0
        distribution[lvl] = {"count": count, "pct": round(pct, 1)}

    # Concentration metrics
    l2_pct = distribution["L2"]["pct"] / 100 if labeled > 0 else 0
    l3plus = sum(level_counts.get(f"L{i}", 0) for i in range(3, 6))
    l3plus_pct = l3plus / labeled if labeled > 0 else 0
    no_level_pct = no_level / total if total > 0 else 0

    warnings = []
    if labeled >= 5:  # Only warn with enough data
        if l2_pct > L2_CONCENTRATION_WARN:
            warnings.append(
                f"L2 concentration {l2_pct:.0%} exceeds {L2_CONCENTRATION_WARN:.0%} threshold"
            )
        if l3plus_pct < L3PLUS_DIVERSITY_WARN:
            warnings.append(
                f"L3+ diversity {l3plus_pct:.0%} below {L3PLUS_DIVERSITY_WARN:.0%} threshold"
            )
    if no_level_pct > NO_LEVEL_WARN and no_level >= 3:
        warnings.append(
            f"{no_level}/{total} lessons ({no_level_pct:.0%}) lack Level header"
        )

    return {
        "total": total,
        "labeled": labeled,
        "no_level": no_level,
        "distribution": distribution,
        "l2_pct": round(l2_pct * 100, 1),
        "l3plus_pct": round(l3plus_pct * 100, 1),
        "l3plus_count": l3plus,
        "warnings": warnings,
    }


def main():
    parser = argparse.ArgumentParser(description="FM-25 level concentration check")
    parser.add_argument("--staged", action="store_true", help="Check staged lessons only")
    parser.add_argument("--window", type=int, default=WINDOW_SESSIONS, help="Rolling window (sessions)")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    lessons = scan_lessons(window=args.window, staged_only=args.staged)
    result = compute_distribution(lessons)

    if args.json:
        print(json.dumps(result, indent=2))
        return 1 if result["warnings"] else 0

    # Human-readable output
    if result["total"] == 0:
        print("No lessons found in window.")
        return 0

    window_label = "staged" if args.staged else f"last {args.window} sessions"
    print(f"FM-25 Level Concentration ({window_label}): {result['total']} lessons, {result['labeled']} labeled")
    print()

    for lvl in ["L1", "L2", "L3", "L4", "L5"]:
        d = result["distribution"][lvl]
        if d["count"] > 0:
            bar = "#" * max(1, int(d["pct"] / 2))
            print(f"  {lvl}: {d['count']:3d} ({d['pct']:5.1f}%) {bar}")

    if result["no_level"] > 0:
        pct = result["no_level"] / result["total"] * 100
        print(f"  ??: {result['no_level']:3d} ({pct:5.1f}%) (no Level header)")

    print()
    print(f"  L2 concentration: {result['l2_pct']:.1f}%")
    print(f"  L3+ diversity:    {result['l3plus_pct']:.1f}% ({result['l3plus_count']} lessons)")

    if result["warnings"]:
        print()
        for w in result["warnings"]:
            print(f"  ⚠ NOTICE: {w}")
        return 1

    print()
    print("  ✓ Level distribution within healthy range")
    return 0


if __name__ == "__main__":
    sys.exit(main())
