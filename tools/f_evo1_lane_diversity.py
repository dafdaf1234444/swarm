#!/usr/bin/env python3
"""
f_evo1_lane_diversity.py — F-EVO1: lane diversity cross-session analysis

Computes per-session lane diversity metrics (scope diversity ratio, focus HHI,
frontier count) from SWARM-LANES.md MERGED rows, then joins with SESSION-LOG
L+P yield to test the novelty-yield coupling hypothesis.

Hypothesis: sessions with higher diversity (more unique scope-keys, broader
focus spread) produce more L+P per session than low-diversity sessions.
"""
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from statistics import correlation, mean

REPO = Path(__file__).parent.parent
LANES_FILE = REPO / "tasks" / "SWARM-LANES.md"
SESSION_LOG = REPO / "memory" / "SESSION-LOG.md"
OUT_FILE = REPO / "experiments" / "evolution" / f"f-evo1-lane-diversity-s188.json"

# regex to extract session number from lane row (column 3)
SESSION_RE = re.compile(r"S(\d+)")
FRONTIER_RE = re.compile(r"\bF-[A-Z0-9]+-[A-Z0-9]+\b")


def _parse_etc(etc: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for part in re.split(r"[,;]\s*", etc):
        m = re.match(r"(\w+)=(.+)", part.strip())
        if m:
            fields[m.group(1)] = m.group(2).strip()
    return fields


def _hhi(counts: dict) -> float:
    """Herfindahl-Hirschman Index — 1.0 = monopoly, 1/n = perfect diversity."""
    total = sum(counts.values())
    if total == 0:
        return 0.0
    return sum((v / total) ** 2 for v in counts.values())


def parse_merged_lanes(lanes_text: str) -> dict[str, list[dict]]:
    """Return per-session list of MERGED/DONE lane dicts, using regex to avoid pipe-in-notes issue."""
    result: dict[str, list[dict]] = defaultdict(list)
    # Match rows with explicit MERGED or DONE status token
    status_re = re.compile(r'\| (MERGED|DONE) \|')
    session_col_re = re.compile(r'^\| [^|]+ \| [^|]+ \| (S\d+) \|')
    # Extract scope_key and Etc fields using positional parsing on first 10 columns
    for line in lanes_text.splitlines():
        if not line.startswith("|"):
            continue
        if not status_re.search(line):
            continue
        sm = session_col_re.match(line)
        if not sm:
            continue
        session = sm.group(1)
        # Parse first 10 pipe-delimited columns (safe: no pipes before notes)
        # Format: | date | lane | session | agent | branch | pr | model | platform | scope_key | Etc | Status | Notes |
        cols = line.split("|")
        if len(cols) < 12:
            continue
        scope_key = cols[9].strip()
        etc_raw = cols[10].strip()
        fields = _parse_etc(etc_raw)
        frontier = fields.get("frontier", "")
        focus = fields.get("focus", "global")
        result[session].append({
            "scope_key": scope_key,
            "frontier": frontier,
            "focus": focus,
        })
    return result


def diversity_metrics(lanes: list[dict]) -> dict:
    if not lanes:
        return {}
    scope_keys = [l["scope_key"] for l in lanes]
    unique_scope = len(set(scope_keys))
    total = len(scope_keys)
    scope_diversity_ratio = unique_scope / total if total > 0 else 0

    focus_counts: dict[str, int] = defaultdict(int)
    for l in lanes:
        focus_counts[l["focus"]] += 1
    focus_hhi = _hhi(dict(focus_counts))

    frontiers = set()
    for l in lanes:
        for f in FRONTIER_RE.findall(l["frontier"]):
            frontiers.add(f)
    return {
        "merged_lanes": total,
        "unique_scope_keys": unique_scope,
        "scope_diversity_ratio": round(scope_diversity_ratio, 4),
        "focus_hhi": round(focus_hhi, 4),
        "frontier_count": len(frontiers),
        "focus_distribution": dict(sorted(focus_counts.items(), key=lambda x: -x[1])[:5]),
    }


def parse_session_yields(log_text: str) -> dict[str, int]:
    """Parse +NL +NP per session from SESSION-LOG.md. Sum across sub-sessions."""
    yields: dict[str, int] = defaultdict(int)
    pattern = re.compile(r"^(S\d+)\t.*\+(\d+)L.*\+(\d+)P", re.MULTILINE)
    for m in pattern.finditer(log_text):
        session, L, P = m.group(1), int(m.group(2)), int(m.group(3))
        yields[session] += int(L) + int(P)
    return dict(yields)


def main() -> None:
    lanes_text = LANES_FILE.read_text(encoding="utf-8")
    log_text = SESSION_LOG.read_text(encoding="utf-8")

    per_session_lanes = parse_merged_lanes(lanes_text)
    per_session_yield = parse_session_yields(log_text)

    # Focus on sessions with both diversity and yield data (S175+)
    sessions_with_data = []
    for session in sorted(per_session_lanes, key=lambda s: int(s[1:])):
        snum = int(session[1:])
        if snum < 175:
            continue
        lanes = per_session_lanes[session]
        if not lanes:
            continue
        y = per_session_yield.get(session, 0)
        m = diversity_metrics(lanes)
        sessions_with_data.append({
            "session": session,
            "yield_lp": y,
            **m,
        })

    # Cross-session coupling: scope_diversity_ratio vs yield
    xs = [s["scope_diversity_ratio"] for s in sessions_with_data if s["merged_lanes"] >= 2]
    ys = [s["yield_lp"] for s in sessions_with_data if s["merged_lanes"] >= 2]
    # Also HHI vs yield (lower HHI = more diverse focus)
    hhi_xs = [s["focus_hhi"] for s in sessions_with_data if s["merged_lanes"] >= 2]

    diversity_yield_corr = None
    hhi_yield_corr = None
    if len(xs) >= 3:
        try:
            diversity_yield_corr = round(correlation(xs, ys), 4)
        except Exception:
            pass
    if len(hhi_xs) >= 3:
        try:
            hhi_yield_corr = round(correlation(hhi_xs, ys), 4)
        except Exception:
            pass

    eligible = [s for s in sessions_with_data if s["merged_lanes"] >= 2]
    result = {
        "frontier_id": "F-EVO1",
        "session": 188,
        "created_on": "2026-02-28",
        "description": "Cross-session diversity vs novelty-yield coupling (S175-S188)",
        "n_sessions_analyzed": len(sessions_with_data),
        "n_sessions_eligible": len(eligible),
        "diversity_yield_correlation": diversity_yield_corr,
        "hhi_yield_correlation": hhi_yield_corr,
        "interpretation": {
            "diversity_yield": "positive = diverse sessions produce more L+P; negative = focus wins",
            "hhi_yield": "negative = diverse focus (low HHI) produces more L+P",
        },
        "mean_scope_diversity": round(mean([s["scope_diversity_ratio"] for s in eligible]), 4) if eligible else None,
        "mean_yield_lp": round(mean([s["yield_lp"] for s in eligible]), 2) if eligible else None,
        "per_session": sessions_with_data,
        "s186_baseline_ref": "experiments/evolution/f-evo1-lane-diversity-s186.json",
        "next_step": "If |diversity_yield_corr| < 0.3: inconclusive (need more sessions); if positive: bias toward heterogeneous lane allocation; if negative: tight-focus allocation preferred",
    }

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(json.dumps(result, indent=2))
    print(f"Wrote {OUT_FILE}")
    print(f"Sessions analyzed: {len(sessions_with_data)}, eligible (≥2 MERGED): {len(eligible)}")
    print(f"Diversity-yield correlation: {diversity_yield_corr}")
    print(f"HHI-yield correlation: {hhi_yield_corr}")
    if eligible:
        print(f"Mean scope_diversity: {result['mean_scope_diversity']}")
        print(f"Mean yield: {result['mean_yield_lp']}")
    for s in sessions_with_data[-6:]:
        print(f"  {s['session']}: lanes={s['merged_lanes']} diversity={s['scope_diversity_ratio']} yield={s['yield_lp']}")


if __name__ == "__main__":
    main()
