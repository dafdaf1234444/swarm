#!/usr/bin/env python3
"""
self_inflation_index.py — Measures self-inflation risk across 4 axes.

FM-21 defense layer: automated detection of measurement self-inflation.
Concurrency-safe: read-only git/file analysis, no mutable state.

Axes:
  1. EAD confirmation ratio — lanes confirmed vs falsified
  2. External citation ratio — lessons citing external sources
  3. Positive conclusion rate — EAD diffs with net-positive outcomes
  4. Level inflation rate — L3+ claims without structural evidence

Usage:
  python3 tools/self_inflation_index.py           # full report
  python3 tools/self_inflation_index.py --json     # JSON output
  python3 tools/self_inflation_index.py --orient   # orient.py one-liner
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def parse_ead_verdicts(lanes_path=None):
    """Parse EAD actual= and diff= fields from SWARM-LANES.md."""
    lanes_path = lanes_path or ROOT / "tasks" / "SWARM-LANES.md"
    if not lanes_path.exists():
        return {"confirmed": 0, "falsified": 0, "partial": 0, "survived": 0, "total": 0}

    text = lanes_path.read_text(errors="replace")
    counts = {"confirmed": 0, "falsified": 0, "partial": 0, "survived": 0, "total": 0}

    # Extract actual= fields from lane rows
    actual_pattern = re.compile(r'actual=([^;|]+)', re.IGNORECASE)
    for match in actual_pattern.finditer(text):
        val = match.group(1).strip().upper()
        if val == "TBD" or not val:
            continue
        counts["total"] += 1
        if "FALSIF" in val:
            counts["falsified"] += 1
        elif "CONFIRM" in val:
            counts["confirmed"] += 1
        elif "PARTIAL" in val:
            counts["partial"] += 1
        elif "SURVIV" in val:
            counts["survived"] += 1
        else:
            # Classify based on keywords
            if any(w in val for w in ["YES", "PASS", "CORRECT", "MATCH"]):
                counts["confirmed"] += 1
            elif any(w in val for w in ["NO", "FAIL", "WRONG", "REJECT"]):
                counts["falsified"] += 1
            else:
                counts["partial"] += 1

    return counts


def parse_external_citations(n=50):
    """Check last N lessons for external grounding (both reported and structural)."""
    lessons_dir = ROOT / "memory" / "lessons"
    if not lessons_dir.exists():
        return {"ext_reported": 0, "ext_structural": 0, "internal_only": 0,
                "total": 0, "no_header": 0, "performative_gap": 0}

    # Get lesson files sorted by number descending
    lesson_files = []
    for f in lessons_dir.iterdir():
        m = re.match(r'L-(\d+)\.md', f.name)
        if m:
            lesson_files.append((int(m.group(1)), f))
    lesson_files.sort(key=lambda x: x[0], reverse=True)

    counts = {"ext_reported": 0, "ext_structural": 0, "internal_only": 0,
              "total": 0, "no_header": 0, "performative_gap": 0}

    for num, fpath in lesson_files[:n]:
        text = fpath.read_text(errors="replace")
        counts["total"] += 1

        # Check External: header (self-reported grounding)
        ext_match = re.search(r'^External:\s*(.+)', text, re.MULTILINE)
        has_ext_report = False
        if ext_match:
            ext_val = ext_match.group(1).strip().lower()
            is_none = (ext_val in ("none", "n/a", "internal", "self-referential", "")
                       or ("internal" in ext_val and "external" not in ext_val)
                       or ("none" in ext_val and "external" not in ext_val)
                       or "purely internal" in ext_val
                       or "no external" in ext_val)
            if not is_none:
                has_ext_report = True
                counts["ext_reported"] += 1
        else:
            counts["no_header"] += 1

        # Check Cites: header for non-internal references (structural grounding)
        cites_match = re.search(r'^Cites:\s*(.+)', text, re.MULTILINE)
        has_ext_structural = False
        if cites_match:
            cites_val = cites_match.group(1).strip()
            # Internal refs are L-NNN, P-NNN, B-NNN, PHIL-NNN, F-XXX
            non_internal = re.sub(r'\b[LPBF]-\d+\b', '', cites_val)
            non_internal = re.sub(r'\bPHIL-\d+\b', '', non_internal)
            non_internal = re.sub(r'\bSIG-\d+\b', '', non_internal)
            non_internal = non_internal.strip(' ,')
            if non_internal and len(non_internal) > 3:
                has_ext_structural = True
                counts["ext_structural"] += 1

        if not has_ext_report and not has_ext_structural:
            counts["internal_only"] += 1

        # Performative gap: claims external but Cites: is all internal
        if has_ext_report and not has_ext_structural:
            counts["performative_gap"] += 1

    return counts


def parse_diff_outcomes(lanes_path=None):
    """Parse diff= fields for net-positive vs net-negative outcomes."""
    lanes_path = lanes_path or ROOT / "tasks" / "SWARM-LANES.md"
    if not lanes_path.exists():
        return {"positive": 0, "negative": 0, "mixed": 0, "total": 0}

    text = lanes_path.read_text(errors="replace")
    counts = {"positive": 0, "negative": 0, "mixed": 0, "total": 0}

    diff_pattern = re.compile(r'diff=([^;|]+)', re.IGNORECASE)
    for match in diff_pattern.finditer(text):
        val = match.group(1).strip()
        if val.upper() == "TBD" or not val:
            continue
        counts["total"] += 1
        val_upper = val.upper()

        neg_signals = sum(1 for w in ["FALSIF", "WRONG", "WORSE", "FAILED", "UNEXPECTED",
                                       "EXCEEDED", "OVERESTIM", "MISS"] if w in val_upper)
        pos_signals = sum(1 for w in ["CONFIRM", "CORRECT", "MATCH", "EXPECTED",
                                       "IMPROVED", "PASS"] if w in val_upper)

        if neg_signals > pos_signals:
            counts["negative"] += 1
        elif pos_signals > neg_signals:
            counts["positive"] += 1
        else:
            counts["mixed"] += 1

    return counts


def parse_level_distribution(n=50):
    """Count level distribution in last N lessons."""
    lessons_dir = ROOT / "memory" / "lessons"
    if not lessons_dir.exists():
        return {"L1": 0, "L2": 0, "L3": 0, "L4": 0, "L5": 0, "total": 0, "no_level": 0}

    lesson_files = []
    for f in lessons_dir.iterdir():
        m = re.match(r'L-(\d+)\.md', f.name)
        if m:
            lesson_files.append((int(m.group(1)), f))
    lesson_files.sort(key=lambda x: x[0], reverse=True)

    counts = {"L1": 0, "L2": 0, "L3": 0, "L4": 0, "L5": 0, "total": 0, "no_level": 0}
    for num, fpath in lesson_files[:n]:
        text = fpath.read_text(errors="replace")
        counts["total"] += 1

        level_match = re.search(r'\bLevel:\s*(L[1-5])\b', text)
        if level_match:
            counts[level_match.group(1)] += 1
        else:
            counts["no_level"] += 1

    return counts


def compute_inflation_index(ead, ext, diff, level):
    """Compute composite self-inflation index (0-1, higher = more inflated)."""
    scores = {}

    # Axis 1: Confirmation ratio (healthy: 1:1 to 3:1, inflated: >5:1)
    if ead["total"] > 0:
        falsified_total = ead["falsified"]
        confirmed_total = ead["confirmed"] + ead["survived"]
        if falsified_total > 0:
            ratio = confirmed_total / falsified_total
        else:
            ratio = confirmed_total if confirmed_total > 0 else 0
        # Map: ratio 1 → score 0, ratio 5 → score 0.5, ratio 10+ → score 1.0
        scores["confirmation"] = min(1.0, max(0, (ratio - 1) / 9))
    else:
        scores["confirmation"] = 0.5  # unknown → neutral

    # Axis 2: External grounding (structural, not self-reported)
    if ext["total"] > 0:
        # Use structural grounding (Cites: with external refs), not self-reported External:
        struct_ratio = ext["ext_structural"] / ext["total"]
        # Map: 20%+ → score 0, 0% → score 1.0
        scores["external"] = min(1.0, max(0, (0.20 - struct_ratio) / 0.20))
        # Performative gap bonus: claiming external without structural backing = extra inflation
        if ext["ext_reported"] > 0:
            perf_gap_rate = ext["performative_gap"] / ext["ext_reported"]
            scores["performative"] = min(1.0, max(0, perf_gap_rate))
        else:
            scores["performative"] = 0.0
    else:
        scores["external"] = 0.5
        scores["performative"] = 0.0

    # Axis 3: Positive conclusion rate (healthy: 50-60%, inflated: >80%)
    if diff["total"] > 0:
        pos_rate = diff["positive"] / diff["total"]
        # Map: 50% → score 0, 80%+ → score 1.0
        scores["conclusion"] = min(1.0, max(0, (pos_rate - 0.50) / 0.30))
    else:
        scores["conclusion"] = 0.5

    # Axis 4: Level inflation (healthy: <30% L3+, inflated: >50% L3+)
    if level["total"] > 0:
        l3_plus = level["L3"] + level["L4"] + level["L5"]
        l3_rate = l3_plus / level["total"]
        # Map: 30% → score 0, 60%+ → score 1.0
        scores["level"] = min(1.0, max(0, (l3_rate - 0.30) / 0.30))
    else:
        scores["level"] = 0.5

    composite = sum(scores.values()) / len(scores)
    return scores, composite


def run(n=50, json_output=False, orient_mode=False):
    """Run full self-inflation index analysis."""
    ead = parse_ead_verdicts()
    ext = parse_external_citations(n)
    diff = parse_diff_outcomes()
    level = parse_level_distribution(n)
    scores, composite = compute_inflation_index(ead, ext, diff, level)

    # Risk level
    if composite >= 0.7:
        risk = "HIGH"
    elif composite >= 0.4:
        risk = "MODERATE"
    else:
        risk = "LOW"

    result = {
        "composite": round(composite, 3),
        "risk": risk,
        "axes": {k: round(v, 3) for k, v in scores.items()},
        "raw": {
            "ead": ead,
            "external": ext,
            "diff": diff,
            "level": level,
        },
        "sample_size": n,
    }

    if orient_mode:
        axis_str = " | ".join(f"{k}={v:.2f}" for k, v in scores.items())
        confirm_ratio = f"{ead['confirmed']}:{ead['falsified']}" if ead["total"] > 0 else "?"
        struct_pct = f"{100*ext['ext_structural']/max(1,ext['total']):.0f}%" if ext["total"] > 0 else "?"
        perf_gap = f"{ext['performative_gap']}/{ext['ext_reported']}" if ext["ext_reported"] > 0 else "0"
        print(f"  Inflation index: {composite:.2f} ({risk}) | {axis_str}")
        print(f"  Confirm:falsify={confirm_ratio} | Structural external={struct_pct} | Performative gap={perf_gap}")
        return result

    if json_output:
        print(json.dumps(result, indent=2))
        return result

    # Full report
    print(f"=== SELF-INFLATION INDEX (FM-21) | n={n} ===")
    print(f"  Composite: {composite:.3f} ({risk})")
    print()
    print("--- Axis Scores (0=healthy, 1=inflated) ---")
    for k, v in scores.items():
        bar = "█" * int(v * 20) + "░" * (20 - int(v * 20))
        print(f"  {k:14s} {v:.3f} [{bar}]")
    print()
    print("--- Raw Data ---")
    print(f"  EAD verdicts: {ead['confirmed']} confirmed, {ead['falsified']} falsified, "
          f"{ead['partial']} partial, {ead['survived']} survived (n={ead['total']})")
    if ead["falsified"] > 0:
        print(f"  Confirmation ratio: {ead['confirmed']/ead['falsified']:.1f}:1")
    elif ead["confirmed"] > 0:
        print(f"  Confirmation ratio: {ead['confirmed']}:0 (NO falsifications)")
    print()
    print(f"  External grounding (structural): {ext['ext_structural']}/{ext['total']} ({100*ext['ext_structural']/max(1,ext['total']):.1f}%)")
    print(f"  External grounding (reported):   {ext['ext_reported']}/{ext['total']} ({100*ext['ext_reported']/max(1,ext['total']):.1f}%)")
    print(f"  Performative gap: {ext['performative_gap']}/{max(1,ext['ext_reported'])} ({100*ext['performative_gap']/max(1,ext['ext_reported']):.1f}%)")
    print(f"    No External: header: {ext['no_header']}")
    print()
    print(f"  Diff outcomes: {diff['positive']} positive, {diff['negative']} negative, "
          f"{diff['mixed']} mixed (n={diff['total']})")
    if diff["total"] > 0:
        print(f"  Positive rate: {100*diff['positive']/diff['total']:.1f}%")
    print()
    print(f"  Level distribution (last {n}): ", end="")
    for lev in ["L1", "L2", "L3", "L4", "L5"]:
        if level[lev] > 0:
            print(f"{lev}={level[lev]} ", end="")
    print(f"(no_level={level['no_level']})")
    if level["total"] > 0:
        l3p = level["L3"] + level["L4"] + level["L5"]
        print(f"  L3+ rate: {100*l3p/level['total']:.1f}%")

    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Self-inflation index (FM-21)")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--orient", action="store_true", help="Orient one-liner")
    parser.add_argument("-n", type=int, default=50, help="Recent lessons to analyze")
    args = parser.parse_args()
    run(n=args.n, json_output=args.json, orient_mode=args.orient)
