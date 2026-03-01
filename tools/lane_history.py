#!/usr/bin/env python3
"""lane_history.py — cumulative SWARM-LANES history query tool.

SWARM-LANES.md uses merge-on-close (close_lane.py), which deletes rows on close.
Current file only contains ACTIVE lanes. This tool reads both the active file and
the archive to return complete cumulative lane history for accurate metrics.

Problem solved (L-876, S404c): ad-hoc scripts reading only SWARM-LANES.md inflate
cumulative Gini by ~25% because MERGED/ABANDONED rows are in the archive.

Usage:
  python3 tools/lane_history.py                        # summary
  python3 tools/lane_history.py --domain meta          # filter by domain
  python3 tools/lane_history.py --status MERGED        # filter by status
  python3 tools/lane_history.py --count-by-domain      # counts per domain
  python3 tools/lane_history.py --gini                 # dispatch Gini coefficient
  python3 tools/lane_history.py --json                 # JSON output
"""

import argparse
import json
import re
import sys
from pathlib import Path

LANES_FILE = Path("tasks/SWARM-LANES.md")
LANES_ARCHIVE = Path("tasks/SWARM-LANES-ARCHIVE.md")

ROW_RE = re.compile(r"^\| (\d{4}-\d{2}-\d{2}) \| ([\w-]+) \| (S\d+) \|")


def parse_lanes(files=None):
    """Parse lane rows from SWARM-LANES.md + archive. Returns list of dicts."""
    if files is None:
        files = [f for f in (LANES_FILE, LANES_ARCHIVE) if f.exists()]

    seen_ids = set()
    lanes = []
    for fpath in files:
        for line in fpath.read_text(encoding="utf-8").splitlines():
            if not line.startswith("| "):
                continue
            parts = [p.strip() for p in line.split("|")]
            if len(parts) < 13:
                continue
            date, lane_id, session = parts[1], parts[2], parts[3]
            if not lane_id or not re.match(r"DOMEX-", lane_id):
                continue
            if lane_id in seen_ids:
                continue
            seen_ids.add(lane_id)

            etc = parts[10] if len(parts) > 10 else ""
            status = parts[11].strip() if len(parts) > 11 else ""
            notes = parts[12].strip() if len(parts) > 12 else ""

            # extract domain from lane_id: DOMEX-<DOMAIN>-S<N>
            m = re.match(r"DOMEX-([A-Z0-9]+(?:-[A-Z0-9]+)*)-S\d+", lane_id)
            domain_raw = m.group(1) if m else "unknown"
            # normalize domain: DOMEX-META → meta, DOMEX-NK → nk-complexity
            DOMAIN_MAP = {
                "NK": "nk-complexity", "GT": "graph-theory", "SP": "stochastic-processes",
                "ECO": "economy", "EVO": "evolution", "AI": "ai-systems",
                "FAR": "far-transfer", "CACHE": "meta", "EVAL": "evaluation",
                "OPS": "operations-research", "PHY": "physics", "SEC": "security",
                "QC": "quality", "BRN": "brain", "IS": "information-science",
                "PSY": "psychology", "DS": "distributed-systems", "CAT": "catastrophic-risks",
                "COMP": "competitions", "CRYPTO": "cryptocurrency", "FIN": "finance",
                "GAME": "game-theory", "LING": "linguistics", "LNG": "linguistics",
                "STAT": "statistics", "STR": "strategy", "CT": "control-theory",
                "DRM": "dream", "GG": "gaming", "HLP": "helper-swarm",
                "HST": "history", "HUM": "human-systems", "SOC": "social-media",
                "FARM": "farming", "FLD": "evolution", "EXP": "expert-swarm",
                "SUB": "meta", "OR": "operations-research", "DEP": "meta",
                "SWM": "expert-swarm", "GOV": "governance", "DNA": "evolution",
                "CACHE": "meta", "CC": "claude-code", "FAR": "far-transfer",
            }
            domain = DOMAIN_MAP.get(domain_raw, domain_raw.lower().replace("-", "_"))
            if domain_raw == "META":
                domain = "meta"

            lanes.append({
                "date": date,
                "lane_id": lane_id,
                "session": session,
                "domain": domain,
                "status": status,
                "etc": etc,
                "notes": notes,
                "source": fpath.name,
            })
    return lanes


def gini(values):
    """Compute Gini coefficient for a list of values."""
    if not values:
        return 0.0
    arr = sorted(values)
    n = len(arr)
    total = sum(arr)
    if total == 0:
        return 0.0
    cum = sum((i + 1) * v for i, v in enumerate(arr))
    return (2 * cum) / (n * total) - (n + 1) / n


def main():
    parser = argparse.ArgumentParser(description="Cumulative SWARM-LANES history query")
    parser.add_argument("--domain", help="Filter by domain")
    parser.add_argument("--status", help="Filter by status (MERGED, ABANDONED, ACTIVE)")
    parser.add_argument("--count-by-domain", action="store_true", help="Show lane counts per domain")
    parser.add_argument("--gini", action="store_true", help="Compute dispatch Gini coefficient")
    parser.add_argument("--json", dest="json_out", action="store_true", help="JSON output")
    parser.add_argument("--active-only", action="store_true", help="Read only SWARM-LANES.md (not archive)")
    args = parser.parse_args()

    files = [LANES_FILE] if args.active_only else None
    lanes = parse_lanes(files)

    # filters
    if args.domain:
        lanes = [l for l in lanes if args.domain.lower() in l["domain"].lower()]
    if args.status:
        lanes = [l for l in lanes if args.status.upper() in l["status"].upper()]

    if args.json_out:
        print(json.dumps(lanes, indent=2))
        return

    if args.count_by_domain:
        from collections import Counter
        counts = Counter(l["domain"] for l in lanes)
        merged = Counter(l["domain"] for l in lanes if "MERGED" in l["status"])
        print(f"{'Domain':<30} {'Total':>6} {'Merged':>7} {'Rate':>6}")
        print("-" * 52)
        for dom, cnt in counts.most_common():
            m = merged.get(dom, 0)
            rate = f"{m/cnt*100:.0f}%" if cnt else "-"
            print(f"{dom:<30} {cnt:>6} {m:>7} {rate:>6}")
        print(f"\nTotal lanes: {len(lanes)} (active+archive)")
        return

    if args.gini:
        from collections import Counter
        counts = Counter(l["domain"] for l in lanes)
        g = gini(list(counts.values()))
        print(f"Dispatch Gini (cumulative, {len(lanes)} lanes): {g:.3f}")
        print(f"Source: {LANES_FILE.name} + {LANES_ARCHIVE.name}")
        print(f"Domains visited: {len(counts)}")
        return

    # default: summary
    from collections import Counter
    status_counts = Counter(l["status"].split()[0] for l in lanes if l["status"])
    domain_counts = Counter(l["domain"] for l in lanes)
    print(f"=== LANE HISTORY (cumulative) ===")
    print(f"Total lanes: {len(lanes)}")
    print(f"  MERGED:    {status_counts.get('MERGED', 0)}")
    print(f"  ABANDONED: {status_counts.get('ABANDONED', 0)}")
    print(f"  active:    {sum(v for k,v in status_counts.items() if k not in ('MERGED','ABANDONED'))}")
    print(f"Domains: {len(domain_counts)}")
    top5 = domain_counts.most_common(5)
    for dom, cnt in top5:
        print(f"  {dom}: {cnt}")
    g = gini(list(domain_counts.values()))
    print(f"Dispatch Gini: {g:.3f}")
    print(f"Sources: {LANES_FILE.name} ({LANES_FILE.exists()}) + {LANES_ARCHIVE.name} ({LANES_ARCHIVE.exists()})")


if __name__ == "__main__":
    main()
