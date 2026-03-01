#!/usr/bin/env python3
"""
Expect Harvest — Expectation Calibration Tracker
Parses session notes (NEXT.md, NEXT-ARCHIVE.md) and lane Etc fields
(SWARM-LANES.md) for expect/actual/diff records, then computes
calibration metrics: hit rate, direction bias, per-domain, temporal trend.

Usage:
    python3 tools/expect_harvest.py --report   # Full calibration report
    python3 tools/expect_harvest.py --json     # Machine-readable JSON
"""

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NEXT_MD = ROOT / "tasks" / "NEXT.md"
NEXT_ARCHIVE = ROOT / "tasks" / "NEXT-ARCHIVE.md"
LANES_FILE = ROOT / "tasks" / "SWARM-LANES.md"

# Classification keywords found in diff text (checked in priority order)
WRONG_KW = ["WRONG", "FALSIFIED", "FAIL", "INVERTED", "WORSENED"]
PARTIAL_KW = ["PARTIALLY CONFIRMED", "PARTIALLY", "PARTIAL", "partially"]
CONFIRMED_KW = ["CONFIRMED", "confirmed", "PASS", "exceeded", "precisely",
                "matches", "Ratio matches", "Correctly predicted"]
# Regex patterns for implicit confirmation: "Expected X — got Y"
CONFIRM_RE = re.compile(
    r"(?:Expected|Predicted)\b.{3,80}(?:got|—)\s.{3,80}"
    r"(?:stronger|exceeded|better|larger|precisely|within|exonerated"
    r"|EXCEEDED|confirmed|PASS|close|correct)", re.IGNORECASE)
# "Expected X — got Y" without qualifier = assume at least partial
EXPECT_GOT_RE = re.compile(
    r"(?:Expected|Predicted)\b.{3,80}(?:got\b|—\s*got)", re.IGNORECASE)

# Overconfidence signals: predicted better than actual
OVER_KW = ["WRONG", "WORSE than expected", "got transient", "INVERTED",
           "WORSENED", "6x worse"]
# Underconfidence signals: actual exceeded prediction
UNDER_KW = ["exceeded", "stronger", "better", "larger", "FAR exceeded",
            "EXCEEDED", "precisely"]


def classify_diff(diff_text: str) -> str:
    """Classify a diff as confirmed / partial / wrong / unclassified."""
    if not diff_text:
        return "unclassified"
    # Explicit wrong takes priority
    for kw in WRONG_KW:
        if kw in diff_text:
            # Check if WRONG is paired with CONFIRMED (mixed outcome)
            has_confirm = any(k in diff_text for k in CONFIRMED_KW)
            if has_confirm:
                return "partial"
            return "wrong"
    # Check partial before confirmed (it contains "CONFIRMED")
    for kw in PARTIAL_KW:
        if kw in diff_text:
            return "partial"
    for kw in CONFIRMED_KW:
        if kw in diff_text:
            return "confirmed"
    # Regex fallback: "Expected/Predicted X — got Y (stronger/exceeded/...)"
    if CONFIRM_RE.search(diff_text):
        return "confirmed"
    # Heuristic: "Did NOT predict" without WRONG usually means partial
    if "Did NOT predict" in diff_text or "NOT predicted" in diff_text:
        return "partial"
    # Broad fallback: any "Expected/Predicted X — got Y" = partial
    if EXPECT_GOT_RE.search(diff_text):
        return "partial"
    return "unclassified"


def direction_bias(diff_text: str) -> str:
    """Detect overconfident vs underconfident vs neutral."""
    if not diff_text:
        return "neutral"
    over = sum(1 for kw in OVER_KW if kw in diff_text)
    under = sum(1 for kw in UNDER_KW if kw in diff_text)
    # "Did NOT predict" = underconfident (missed a positive finding)
    under += len(re.findall(r"Did NOT predict|NOT predicted", diff_text))
    if over > under:
        return "overconfident"
    if under > over:
        return "underconfident"
    return "neutral"


def extract_session(header: str) -> int:
    """Extract session number from '## S390 session note ...' or lane row."""
    m = re.search(r"\bS(\d+)", header)
    return int(m.group(1)) if m else 0


def extract_domain_from_lane(lane_line: str) -> str:
    """Extract domain from **lane**: DOMEX-DOMAIN-S... or dispatch field."""
    m = re.search(r"DOMEX-([A-Z]+\d*)-S\d+", lane_line)
    if m:
        return m.group(1).lower()
    m = re.search(r"\*\*dispatch\*\*:\s*(\S+)", lane_line)
    if m:
        return m.group(1).lower()
    return "unknown"


def extract_domain_from_etc(etc: str) -> str:
    """Extract domain from lane Etc intent= or focus= field."""
    m = re.search(r"intent=advance-F-([A-Z]+)", etc)
    if m:
        return m.group(1).lower()
    m = re.search(r"focus=domains/([^;]+)", etc)
    if m:
        return m.group(1).strip().lower()
    m = re.search(r"frontier=F-([A-Z]+)", etc)
    if m:
        return m.group(1).lower()
    return "unknown"


def parse_session_notes(path: Path) -> list:
    """Parse session note blocks from NEXT.md or NEXT-ARCHIVE.md."""
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8", errors="replace")
    records = []
    blocks = re.split(r"(?=^## S\d+)", text, flags=re.MULTILINE)
    for block in blocks:
        if not block.strip():
            continue
        header_m = re.match(r"^## (S\d+\S*)\s+session note\s*\(([^)]*)\)", block)
        if not header_m:
            continue
        session = extract_session(header_m.group(1))
        title = header_m.group(2)
        # Extract lane/domain from check_mode line
        lane_line = ""
        for line in block.splitlines():
            if "**lane**:" in line or "**dispatch**:" in line:
                lane_line = line
                break
        domain = extract_domain_from_lane(lane_line or title)
        lane_m = re.search(r"DOMEX-\S+-S\d+\w*", lane_line or title)
        lane = lane_m.group(0) if lane_m else ""
        expect = actual = diff = ""
        for line in block.splitlines():
            if line.startswith("- **expect**:"):
                expect = line.split(":", 1)[1].strip()
            elif line.startswith("- **actual**:"):
                actual = line.split(":", 1)[1].strip()
            elif line.startswith("- **diff**:"):
                diff = line.split(":", 1)[1].strip()
        if not expect and not actual:
            continue
        records.append({
            "source": "session_note",
            "session": session,
            "domain": domain,
            "lane": lane,
            "expect": expect,
            "actual": actual,
            "diff": diff,
            "classification": classify_diff(diff),
            "bias": direction_bias(diff),
        })
    return records


def parse_lane_etc(path: Path) -> list:
    """Parse lane rows from SWARM-LANES.md for expect=/actual=/diff= in Etc."""
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8", errors="replace")
    records = []
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cols = [c.strip() for c in line.split("|")]
        if len(cols) < 12:
            continue
        etc = cols[10] if len(cols) > 10 else ""
        if "expect=" not in etc:
            continue
        session = extract_session(cols[3] if len(cols) > 3 else "")
        lane = cols[2] if len(cols) > 2 else ""
        domain = extract_domain_from_etc(etc)
        # Parse key=value from Etc (semicolon-delimited)
        fields = {}
        for part in etc.split("; "):
            if "=" in part:
                k, v = part.split("=", 1)
                fields[k.strip()] = v.strip()
        expect = fields.get("expect", "")
        actual = fields.get("actual", "")
        diff = fields.get("diff", "")
        if not expect:
            continue
        records.append({
            "source": "lane_etc",
            "session": session,
            "domain": domain,
            "lane": lane.strip(),
            "expect": expect,
            "actual": actual,
            "diff": diff,
            "classification": classify_diff(diff),
            "bias": direction_bias(diff),
        })
    return records


def compute_metrics(records: list) -> dict:
    """Compute calibration metrics from all records."""
    total = len(records)
    if total == 0:
        return {"total": 0}
    # Overall classification
    counts = {"confirmed": 0, "partial": 0, "wrong": 0, "unclassified": 0}
    bias_counts = {"overconfident": 0, "underconfident": 0, "neutral": 0}
    for r in records:
        counts[r["classification"]] = counts.get(r["classification"], 0) + 1
        bias_counts[r["bias"]] = bias_counts.get(r["bias"], 0) + 1
    classified = total - counts["unclassified"]
    hit_rate = counts["confirmed"] / classified if classified else 0
    partial_rate = counts["partial"] / classified if classified else 0
    wrong_rate = counts["wrong"] / classified if classified else 0
    # Per-domain
    domains = {}
    for r in records:
        d = r["domain"]
        if d not in domains:
            domains[d] = {"confirmed": 0, "partial": 0, "wrong": 0,
                          "unclassified": 0, "total": 0}
        domains[d][r["classification"]] += 1
        domains[d]["total"] += 1
    # Temporal trend: split into halves by session number
    sessions = sorted(set(r["session"] for r in records if r["session"] > 0))
    if len(sessions) >= 4:
        mid = sessions[len(sessions) // 2]
        early = [r for r in records if 0 < r["session"] <= mid]
        late = [r for r in records if r["session"] > mid]
        def _hit(recs):
            c = sum(1 for r in recs if r["classification"] == "confirmed")
            cl = sum(1 for r in recs if r["classification"] != "unclassified")
            return c / cl if cl else 0
        trend = {"early_sessions": f"S1-S{mid}", "late_sessions": f"S{mid+1}+",
                 "early_hit_rate": round(_hit(early), 3),
                 "late_hit_rate": round(_hit(late), 3),
                 "early_n": len(early), "late_n": len(late),
                 "improving": _hit(late) > _hit(early)}
    else:
        trend = {"note": "insufficient data for trend (need >=4 sessions)"}
    return {
        "total": total, "classified": classified,
        "confirmed": counts["confirmed"], "partial": counts["partial"],
        "wrong": counts["wrong"], "unclassified": counts["unclassified"],
        "hit_rate": round(hit_rate, 3),
        "partial_rate": round(partial_rate, 3),
        "wrong_rate": round(wrong_rate, 3),
        "bias": bias_counts, "per_domain": domains, "trend": trend,
    }


def print_report(metrics: dict, records: list) -> None:
    """Print human-readable calibration report."""
    print("=" * 60)
    print("  EXPECTATION CALIBRATION REPORT")
    print("=" * 60)
    if metrics["total"] == 0:
        print("\n  No expect/actual records found.")
        return
    t = metrics
    print(f"\n  Records:      {t['total']} ({t['classified']} classified)")
    print(f"  Hit rate:     {t['hit_rate']:.1%} confirmed")
    print(f"  Partial:      {t['partial_rate']:.1%}")
    print(f"  Wrong:        {t['wrong_rate']:.1%}")
    print(f"  Unclassified: {t['unclassified']}")
    # Direction bias
    b = t["bias"]
    print(f"\n  Direction bias:")
    print(f"    Overconfident:  {b['overconfident']}")
    print(f"    Underconfident: {b['underconfident']}")
    print(f"    Neutral:        {b['neutral']}")
    # Temporal trend
    tr = t["trend"]
    if "note" not in tr:
        arrow = "IMPROVING" if tr["improving"] else "DECLINING"
        print(f"\n  Temporal trend: {arrow}")
        print(f"    {tr['early_sessions']} (n={tr['early_n']}): "
              f"{tr['early_hit_rate']:.1%} hit rate")
        print(f"    {tr['late_sessions']} (n={tr['late_n']}): "
              f"{tr['late_hit_rate']:.1%} hit rate")
    # Per-domain (sorted by total, top 10)
    dom = t["per_domain"]
    ranked = sorted(dom.items(), key=lambda x: x[1]["total"], reverse=True)
    print(f"\n  Per-domain calibration (top 10 of {len(ranked)}):")
    print(f"    {'Domain':<20} {'Total':>5} {'Hit%':>6} {'Wrong%':>7}")
    print(f"    {'-'*20} {'-'*5} {'-'*6} {'-'*7}")
    for name, d in ranked[:10]:
        cl = d["total"] - d["unclassified"]
        hr = d["confirmed"] / cl if cl else 0
        wr = d["wrong"] / cl if cl else 0
        print(f"    {name:<20} {d['total']:>5} {hr:>5.0%} {wr:>6.0%}")
    print()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Expect Harvest — expectation calibration tracker")
    parser.add_argument("--report", action="store_true",
                        help="Full human-readable calibration report")
    parser.add_argument("--json", action="store_true",
                        help="Machine-readable JSON output")
    args = parser.parse_args()
    if not args.report and not args.json:
        args.report = True
    # Harvest records from all sources
    records = []
    records.extend(parse_session_notes(NEXT_MD))
    records.extend(parse_session_notes(NEXT_ARCHIVE))
    records.extend(parse_lane_etc(LANES_FILE))
    # Deduplicate: same session+lane from notes and lanes
    seen = set()
    deduped = []
    for r in records:
        key = (r["session"], r["lane"], r["source"])
        if key not in seen:
            seen.add(key)
            deduped.append(r)
    records = deduped
    metrics = compute_metrics(records)
    if args.json:
        print(json.dumps({"metrics": metrics, "record_count": len(records)},
                         indent=2))
    if args.report:
        print_report(metrics, records)


if __name__ == "__main__":
    main()
