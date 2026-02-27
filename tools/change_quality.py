#!/usr/bin/env python3
"""
change_quality.py - Assess per-session change quality vs. historical baseline.

Investigates whether the swarm is improving, stable, or declining over time
by comparing knowledge production and overhead signals across sessions.

Usage:
  python3 tools/change_quality.py              # Recent 5 sessions vs. baseline
  python3 tools/change_quality.py --trend      # Full session trend table
  python3 tools/change_quality.py --session N  # Detail for session N
  python3 tools/change_quality.py --recent N   # Compare last N sessions (default 5)
"""

import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).parent.parent

SESSION_RE = re.compile(r'\[S(\d+)\]')
LESSON_RE = re.compile(r'\bL-(\d{3})\b')
PRINCIPLE_RE = re.compile(r'\bP-(\d{3})\b')
BELIEF_RE = re.compile(r'\bPHIL-(\d+)\b')
FRONTIER_ADVANCE_RE = re.compile(r'\bF\d+\b.*\b(RESOLVED|PARTIAL)\b|\b(RESOLVED|PARTIAL)\b.*\bF\d+\b', re.IGNORECASE)
FRONTIER_OPEN_RE = re.compile(r'\bF\d+\b.*\bOPEN\b|\bOPEN\b.*\bF\d+\b|\bF\d+\s+filed\b|\bfiled\s+F\d+\b', re.IGNORECASE)

# Patterns that indicate administrative overhead (state-sync, not knowledge work)
OVERHEAD_PATTERNS = [
    r'\bstate-sync\b',
    r'\bscale sync\b',
    r'\bcount sync\b',
    r'\bheader sync\b',
    r'\bcounts corrected\b',
    r'\bprinciple-count sync\b',
    r'\bsession log\b',
    r'\bhandoff\b',
]
OVERHEAD_RE = re.compile('|'.join(OVERHEAD_PATTERNS), re.IGNORECASE)

# Patterns that indicate real knowledge work
KNOWLEDGE_PATTERNS = [
    r'\bL-\d{3}\b',        # lesson reference
    r'\bP-\d{3}\b',        # principle reference
    r'\bF\d+\b.*\bOPEN\b', # frontier opened
    r'\blessson\b',        # typo-tolerant
    r'\bharvest\b',
    r'\bdistill\b',
    r'\bexperiment\b',
]
KNOWLEDGE_RE = re.compile('|'.join(KNOWLEDGE_PATTERNS), re.IGNORECASE)


def get_commits():
    """Extract all commits with session numbers from git log."""
    result = subprocess.run(
        ['git', 'log', '--format=%H|%s', '--no-merges'],
        capture_output=True, text=True, cwd=ROOT
    )
    commits = []
    for line in result.stdout.strip().split('\n'):
        if '|' not in line:
            continue
        hash_, msg = line.split('|', 1)
        m = SESSION_RE.search(msg)
        if not m:
            continue
        commits.append({
            'hash': hash_,
            'msg': msg,
            'session': int(m.group(1)),
        })
    return commits


def extract_session_signals(commits):
    """Group commits by session and extract quality signals."""
    sessions = defaultdict(lambda: {
        'commits': 0,
        'lessons': set(),
        'principles': set(),
        'beliefs': set(),
        'frontier_advances': 0,
        'frontiers_opened': 0,
        'overhead_commits': 0,
        'knowledge_commits': 0,
        'msgs': [],
    })

    for c in commits:
        s = c['session']
        msg = c['msg']
        d = sessions[s]

        d['commits'] += 1
        d['msgs'].append(msg)

        for lid in LESSON_RE.findall(msg):
            d['lessons'].add(lid)
        for pid in PRINCIPLE_RE.findall(msg):
            d['principles'].add(pid)
        for bid in BELIEF_RE.findall(msg):
            d['beliefs'].add(bid)
        if FRONTIER_ADVANCE_RE.search(msg):
            d['frontier_advances'] += 1
        if FRONTIER_OPEN_RE.search(msg):
            d['frontiers_opened'] += 1
        if OVERHEAD_RE.search(msg):
            d['overhead_commits'] += 1
        elif KNOWLEDGE_RE.search(msg):
            d['knowledge_commits'] += 1

    return dict(sessions)


def quality_score(sig):
    """
    Composite quality score for a session. Higher = better.

    Components:
      - Knowledge production: lessons + principles touched, frontier advances
      - Focus: low overhead ratio
      - Commit granularity: 2-8 commits is ideal
    """
    n = sig['commits']
    if n == 0:
        return 0.0

    lessons = len(sig['lessons'])
    principles = len(sig['principles'])
    beliefs = len(sig.get('beliefs', set()))
    frontier_advances = sig['frontier_advances']
    frontiers_opened = sig['frontiers_opened']
    overhead_ratio = sig['overhead_commits'] / n

    # Knowledge production (scale: 0-8+)
    knowledge = (
        lessons * 1.2
        + principles * 0.6
        + beliefs * 1.5          # belief changes are high-signal
        + frontier_advances * 2.0
        + frontiers_opened * 1.5
    )

    # Focus penalty: overhead > 25% is waste (baseline ~4% per L-216)
    focus_multiplier = max(0.5, 1.0 - max(0, overhead_ratio - 0.04) * 2)

    # Commit granularity bonus (too few = monolithic; too many = noise)
    if 2 <= n <= 8:
        granularity = 1.0
    elif n == 1:
        granularity = 0.7
    else:
        granularity = max(0.6, 1.0 - (n - 8) * 0.03)

    return knowledge * focus_multiplier * granularity


def compute_baseline(sessions_data, exclude_last_n=5):
    """Compute historical baseline stats, excluding the most recent N sessions."""
    sorted_sessions = sorted(sessions_data.keys())
    if exclude_last_n == 0 or len(sorted_sessions) <= exclude_last_n:
        baseline_sessions = sorted_sessions
    else:
        baseline_sessions = sorted_sessions[:-exclude_last_n]

    if not baseline_sessions:
        return None

    scores = [quality_score(sessions_data[s]) for s in baseline_sessions]
    lessons = [len(sessions_data[s]['lessons']) for s in baseline_sessions]
    principles = [len(sessions_data[s]['principles']) for s in baseline_sessions]
    overhead = [sessions_data[s]['overhead_commits'] / max(1, sessions_data[s]['commits'])
                for s in baseline_sessions]

    n = len(scores)
    return {
        'mean_score': sum(scores) / n,
        'mean_lessons': sum(lessons) / n,
        'mean_principles': sum(principles) / n,
        'mean_overhead': sum(overhead) / n,
        'sessions': n,
    }


def rating(score, baseline_mean):
    """Return human-readable rating vs. baseline."""
    if baseline_mean <= 0:
        return '?'
    ratio = score / baseline_mean
    if ratio >= 1.4:
        return 'STRONG'
    if ratio >= 1.1:
        return 'ABOVE'
    if ratio >= 0.9:
        return 'ON PAR'
    if ratio >= 0.6:
        return 'BELOW'
    return 'WEAK'


def show_comparison(sessions_data, n_recent=5):
    sorted_s = sorted(sessions_data.keys())
    if len(sorted_s) < 2:
        print("Not enough session history to compare.")
        return

    recent = sorted_s[-n_recent:]
    baseline = compute_baseline(sessions_data, exclude_last_n=n_recent)

    if not baseline:
        print("Not enough history for baseline.")
        return

    print(f"=== CHANGE QUALITY: RECENT {n_recent} vs. BASELINE ({baseline['sessions']} sessions) ===")
    print(f"Baseline averages: score={baseline['mean_score']:.2f} | "
          f"L/session={baseline['mean_lessons']:.1f} | "
          f"P/session={baseline['mean_principles']:.1f} | "
          f"overhead={baseline['mean_overhead']:.0%}")
    print()
    print(f"{'Session':>8}  {'Commits':>7}  {'Lessons':>7}  {'Princ':>6}  "
          f"{'FAdv':>5}  {'Overhead':>9}  {'Score':>6}  {'Rating':>8}")
    print("-" * 78)

    for s in recent:
        sig = sessions_data[s]
        score = quality_score(sig)
        overhead_pct = sig['overhead_commits'] / max(1, sig['commits'])
        r = rating(score, baseline['mean_score'])
        print(f"  S{s:>5}  {sig['commits']:>7}  {len(sig['lessons']):>7}  "
              f"{len(sig['principles']):>6}  {sig['frontier_advances']:>5}  "
              f"{overhead_pct:>8.0%}  {score:>6.2f}  {r:>8}")

    # Trend signal
    print()
    if len(sorted_s) >= 10:
        mid = len(sorted_s) // 2
        early = [quality_score(sessions_data[s]) for s in sorted_s[:mid]]
        late = [quality_score(sessions_data[s]) for s in sorted_s[mid:]]
        avg_early = sum(early) / len(early)
        avg_late = sum(late) / len(late)
        ratio = avg_late / avg_early if avg_early > 0 else 1.0
        if ratio >= 1.15:
            trend = f"IMPROVING (+{(ratio-1):.0%})"
        elif ratio <= 0.85:
            trend = f"DECLINING ({(ratio-1):.0%})"
        else:
            trend = f"STABLE ({(ratio-1):+.0%})"
        print(f"Long-term trend: {trend}  "
              f"(early avg={avg_early:.2f}, recent avg={avg_late:.2f})")


def show_trend(sessions_data):
    """Full session-by-session trend table."""
    sorted_s = sorted(sessions_data.keys())
    all_scores = [quality_score(sessions_data[s]) for s in sorted_s]
    if not all_scores:
        print("No session data found.")
        return

    global_mean = sum(all_scores) / len(all_scores)

    print(f"=== CHANGE QUALITY TREND ({len(sorted_s)} sessions) ===")
    print(f"Global mean score: {global_mean:.2f}")
    print()
    print(f"{'Session':>8}  {'Commits':>7}  {'Lessons':>7}  {'Princ':>6}  "
          f"{'FAdv':>5}  {'Overhead':>9}  {'Score':>6}  Bar")
    print("-" * 80)

    for s in sorted_s:
        sig = sessions_data[s]
        score = quality_score(sig)
        overhead_pct = sig['overhead_commits'] / max(1, sig['commits'])
        bar_len = min(20, int(score * 2))
        bar = '#' * bar_len
        marker = '*' if score > global_mean * 1.3 else (' ' if score >= global_mean * 0.7 else '!')
        print(f"  S{s:>5}  {sig['commits']:>7}  {len(sig['lessons']):>7}  "
              f"{len(sig['principles']):>6}  {sig['frontier_advances']:>5}  "
              f"{overhead_pct:>8.0%}  {score:>6.2f}  {marker}{bar}")


def show_session_detail(sessions_data, session_num):
    """Detailed breakdown for a specific session."""
    if session_num not in sessions_data:
        available = sorted(sessions_data.keys())
        print(f"Session S{session_num} not found.")
        print(f"Available: {available[-10:]}")
        return

    sig = sessions_data[session_num]
    score = quality_score(sig)
    baseline = compute_baseline(sessions_data, exclude_last_n=0)
    r = rating(score, baseline['mean_score']) if baseline else '?'

    print(f"=== SESSION S{session_num} QUALITY DETAIL ===")
    print(f"Score: {score:.2f}  Rating: {r}  (global mean: {baseline['mean_score']:.2f})")
    print()
    print(f"Commits:             {sig['commits']}")
    print(f"Lessons referenced:  {sorted(sig['lessons'])} ({len(sig['lessons'])} unique)")
    print(f"Principles ref'd:    {sorted(sig['principles'])} ({len(sig['principles'])} unique)")
    print(f"Beliefs changed:     PHIL-{sorted(sig.get('beliefs', set()))} ({len(sig.get('beliefs', set()))} unique)")
    print(f"Frontier advances:   {sig['frontier_advances']}")
    print(f"Frontiers opened:    {sig['frontiers_opened']}")
    print(f"Overhead commits:    {sig['overhead_commits']} "
          f"({sig['overhead_commits']/max(1,sig['commits']):.0%})")
    print(f"Knowledge commits:   {sig['knowledge_commits']}")
    print()
    print("Commit messages:")
    for m in sig['msgs']:
        tag = '[overhead]' if OVERHEAD_RE.search(m) else '[  work  ]'
        print(f"  {tag} {m[:80]}")


def main():
    args = sys.argv[1:]
    commits = get_commits()
    if not commits:
        print("No sessions found in git log.")
        sys.exit(1)

    sessions_data = extract_session_signals(commits)

    if '--trend' in args:
        show_trend(sessions_data)
    elif '--session' in args:
        idx = args.index('--session')
        if idx + 1 < len(args):
            try:
                target = int(args[idx + 1])
                show_session_detail(sessions_data, target)
            except ValueError:
                print("--session requires a numeric session number")
                sys.exit(1)
        else:
            print("--session requires a session number")
            sys.exit(1)
    else:
        n_recent = 5
        if '--recent' in args:
            idx = args.index('--recent')
            if idx + 1 < len(args):
                try:
                    n_recent = int(args[idx + 1])
                except ValueError:
                    pass
        show_comparison(sessions_data, n_recent=n_recent)


if __name__ == '__main__':
    main()
