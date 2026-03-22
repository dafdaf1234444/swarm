#!/usr/bin/env python3
"""
pheromone_trace.py — Digital pheromone formalization for swarm stigmergy.

Based on Heylighen (2016) "Stigmergy as a universal coordination mechanism"
and Alphanome.ai digital pheromone model. Formalizes swarm's 5/6 Heylighen
primitives and closes the amplification loop (the missing 6th primitive).

Digital pheromones are (value, time, location) tuples with exponential decay.
Every git commit = pheromone deposit. Citation in-degree = accumulated trace.
File modification frequency × citation weight = pheromone concentration.

Usage:
    python3 tools/pheromone_trace.py              # full trail report
    python3 tools/pheromone_trace.py --hot 10     # top 10 hot trails
    python3 tools/pheromone_trace.py --cold 10    # top 10 cold sinks
    python3 tools/pheromone_trace.py --json       # machine-readable

Part of F-ABSORB1 + F-STIG1. L-1304, L-1296.
"""

import argparse
import json
import re
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LESSONS_DIR = ROOT / "memory" / "lessons"

DECAY_RATE = 0.9  # per-day decay factor (matches frontier_decay.py)


class TraceType(Enum):
    PERMANENT = "permanent"     # git commits — never evaporate
    PERSISTENT = "persistent"   # lessons, principles, beliefs — slow decay
    TEMPORARY = "temporary"     # claims, signals, heartbeats — fast decay


def classify_trace(path):
    """Classify a file path into trace type."""
    p = str(path)
    if p.startswith("memory/lessons/") or p.startswith("memory/PRINCIPLES"):
        return TraceType.PERSISTENT
    if p.startswith("beliefs/") or p.startswith("tasks/FRONTIER"):
        return TraceType.PERSISTENT
    if p.startswith("workspace/claims/") or p.startswith("tasks/SIGNALS"):
        return TraceType.TEMPORARY
    return TraceType.PERMANENT


def git_pheromones(days=30):
    """Compute file modification frequency from git log with exponential decay."""
    since = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    r = subprocess.run(
        ["git", "log", f"--since={since}", "--name-only", "--pretty=format:%ad",
         "--date=short"],
        capture_output=True, text=True, cwd=ROOT
    )
    if r.returncode != 0:
        return {}

    today = datetime.now()
    file_scores = defaultdict(float)
    current_date = None

    for line in r.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        if re.match(r'^\d{4}-\d{2}-\d{2}$', line):
            try:
                current_date = datetime.strptime(line, "%Y-%m-%d")
            except ValueError:
                current_date = None
            continue
        if current_date:
            age_days = (today - current_date).days
            decay = DECAY_RATE ** age_days
            file_scores[line] += decay

    return dict(file_scores)


def citation_pheromones():
    """Load citation in-degrees from citation cache."""
    cache_path = ROOT / "experiments" / "compact-citation-cache.json"
    cite_counts = {}

    if cache_path.exists():
        try:
            with open(cache_path) as f:
                cache = json.load(f)
            for path_key, entry in cache.items():
                cites = entry.get("cites", {})
                for lid, count in cites.items():
                    if lid.startswith("L-"):
                        cite_counts[lid] = cite_counts.get(lid, 0) + count
        except (json.JSONDecodeError, KeyError):
            pass

    return cite_counts


def recent_cites(n=50):
    """Find which lessons are cited in recent N lessons (from Cites: headers)."""
    cited = set()
    lessons = sorted(LESSONS_DIR.glob("L-*.md"), key=lambda p: p.name)
    for lf in lessons[-n:]:
        try:
            text = lf.read_text(errors="replace")
            for line in text.splitlines()[:10]:
                if line.startswith("Cites:"):
                    cited.update(re.findall(r'L-\d+', line))
        except Exception:
            pass
    return cited


def hot_trails(n=10):
    """Files with highest combined git-activity × citation score."""
    git_scores = git_pheromones()
    cite_scores = citation_pheromones()

    # Combine: for lesson files, use citation in-degree as multiplier
    combined = {}
    for path, git_score in git_scores.items():
        lid_match = re.search(r'L-(\d+)', path)
        cite_boost = 1.0
        if lid_match:
            lid = f"L-{lid_match.group(1)}"
            cite_boost = 1.0 + cite_scores.get(lid, 0) * 0.1
        combined[path] = git_score * cite_boost

    sorted_trails = sorted(combined.items(), key=lambda x: x[1], reverse=True)
    return sorted_trails[:n]


def cold_sinks(n=10):
    """High in-degree lessons with zero recent re-citations."""
    cite_scores = citation_pheromones()
    recently_cited = recent_cites()

    sinks = []
    for lid, in_degree in cite_scores.items():
        if in_degree >= 5 and lid not in recently_cited:
            sinks.append((lid, in_degree))

    sinks.sort(key=lambda x: x[1], reverse=True)
    return sinks[:n]


def trail_audit():
    """Classify all traces by type and compute summary stats."""
    git_scores = git_pheromones()
    stats = {t.value: {"count": 0, "total_score": 0.0} for t in TraceType}

    for path, score in git_scores.items():
        tt = classify_trace(path)
        stats[tt.value]["count"] += 1
        stats[tt.value]["total_score"] += score

    return stats


def format_report(hot_n=10, cold_n=10):
    """Full formatted pheromone trail report."""
    lines = [
        "=== PHEROMONE TRAIL REPORT ===",
        f"  Decay model: {DECAY_RATE}^days (Heylighen exponential evaporation)",
        "",
    ]

    # Hot trails
    hot = hot_trails(hot_n)
    lines.append(f"--- Hot trails (top {hot_n}, git-activity × citation) ---")
    for path, score in hot:
        tt = classify_trace(path)
        lines.append(f"  {score:7.2f}  [{tt.value[:4]}]  {path}")
    lines.append("")

    # Cold sinks
    cold = cold_sinks(cold_n)
    lines.append(f"--- Cold sinks (in-degree ≥5, zero recent citations) ---")
    for lid, in_deg in cold:
        lines.append(f"  {lid} (in-degree={in_deg}) — high-cited but not in recent Cites: headers")
    lines.append("")

    # Audit
    audit = trail_audit()
    lines.append("--- Trace classification ---")
    for tt, stats in audit.items():
        lines.append(f"  {tt:12s}: {stats['count']:4d} files, concentration {stats['total_score']:.1f}")
    lines.append("")

    # Recently cited count
    rc = recent_cites()
    cite_scores = citation_pheromones()
    high_cite = sum(1 for v in cite_scores.values() if v >= 5)
    lines.append(f"--- Amplification loop status ---")
    lines.append(f"  Recently cited (last 50 lessons): {len(rc)} unique lessons")
    lines.append(f"  High in-degree (≥5): {high_cite} lessons")
    lines.append(f"  Cold sinks: {len(cold_sinks(999))} (high-cited, zero recent re-citation)")
    lines.append(f"  Re-citation rate: {len(rc)}/{high_cite} = {len(rc)/max(high_cite,1)*100:.1f}%")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Digital pheromone trail analysis")
    parser.add_argument("--hot", type=int, default=0, help="Show top N hot trails")
    parser.add_argument("--cold", type=int, default=0, help="Show top N cold sinks")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    if args.json:
        data = {
            "hot_trails": [{"path": p, "score": round(s, 3)} for p, s in hot_trails(args.hot or 10)],
            "cold_sinks": [{"lesson": l, "in_degree": d} for l, d in cold_sinks(args.cold or 10)],
            "audit": trail_audit(),
        }
        print(json.dumps(data, indent=2))
    elif args.hot:
        for path, score in hot_trails(args.hot):
            print(f"  {score:7.2f}  {path}")
    elif args.cold:
        for lid, in_deg in cold_sinks(args.cold):
            print(f"  {lid} (in-degree={in_deg})")
    else:
        print(format_report())


if __name__ == "__main__":
    main()
