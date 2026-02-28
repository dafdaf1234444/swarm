#!/usr/bin/env python3
"""
gather_council.py — Activate council seats by scanning top-10 domains for vacancy.

Reads dispatch_optimizer rankings, checks active DOMEX lanes, outputs seat status
+ open_lane.py commands for vacant seats.

Usage:
  python3 tools/gather_council.py            # show seat status table
  python3 tools/gather_council.py --auto     # print open_lane.py commands for vacant seats
  python3 tools/gather_council.py --json     # machine-readable JSON output
  python3 tools/gather_council.py --session S336  # tag generated lanes with session
"""

import argparse
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent.parent
LANES_FILE = ROOT / "tasks" / "SWARM-LANES.md"
DOMAINS_DIR = ROOT / "domains"

# Council seat health thresholds (from docs/COUNCIL-STRUCTURE.md)
HEALTHY_SEATS = 5
DEGRADED_SEATS = 3
HEALTHY_DOMEX_PER_WINDOW = 3


def get_top10_domains() -> list[dict]:
    """Get top-10 domains from dispatch_optimizer."""
    result = subprocess.run(
        ["python3", "tools/dispatch_optimizer.py", "--json"],
        capture_output=True, text=True, cwd=ROOT
    )
    if result.returncode != 0:
        print(f"[WARN] dispatch_optimizer failed: {result.stderr[:200]}", file=sys.stderr)
        return []
    data = json.loads(result.stdout)
    return data[:10]


def get_active_domex_lanes() -> dict[str, str]:
    """Return {domain_keyword: lane_id} for all ACTIVE DOMEX lanes."""
    if not LANES_FILE.exists():
        return {}
    content = LANES_FILE.read_text()
    active = {}
    for line in content.splitlines():
        if "| ACTIVE |" in line and "DOMEX" in line:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 3:
                lane_id = parts[2]  # e.g. DOMEX-NK-S336
                # Extract domain keyword from lane ID
                m = re.search(r"DOMEX-([A-Z]+)-", lane_id)
                if m:
                    active[m.group(1).lower()] = lane_id
    return active


def domain_to_abbrev(domain: str) -> str:
    """Map domain name to DOMEX abbreviation used in lane IDs."""
    mapping = {
        "meta": "META",
        "nk-complexity": "NK",
        "linguistics": "LNG",
        "expert-swarm": "EXP",
        "graph-theory": "GT",
        "distributed-systems": "DS",
        "information-science": "IS",
        "physics": "PHY",
        "brain": "BRN",
        "helper-swarm": "HLP",
        "human-systems": "HS",
        "economy": "ECO",
        "evaluation": "EVAL",
        "claude-code": "CC",
        "fluid-dynamics": "FLD",
        "quality": "QC",
    }
    return mapping.get(domain, domain.upper().replace("-", "")[:4])


def get_domain_frontier(domain: str) -> str:
    """Get top open frontier question for a domain."""
    fp = DOMAINS_DIR / domain / "tasks" / "FRONTIER.md"
    if not fp.exists():
        return "No frontier file found"
    content = fp.read_text()
    m = re.search(r"\*\*(F[^\*]+)\*\*[:\s]+(.*)", content)
    if m:
        return f"{m.group(1)}: {m.group(2)[:80].strip()}"
    return "Open frontier work available"


def build_open_lane_cmd(domain: str, score: float, session: str, frontier_hint: str) -> str:
    """Build an open_lane.py command for a vacant seat."""
    abbrev = domain_to_abbrev(domain)
    lane_id = f"DOMEX-{abbrev}-{session}"
    domain_path = f"domains/{domain}/tasks/FRONTIER.md"
    # Derive expect/artifact from domain frontier
    artifact = f"experiments/{domain}/f-{abbrev.lower()}-council-{session.lower()}.json"
    expect = f"Produce ≥1 verified finding on {domain} frontier; open or advance at least 1 F-item"
    return (
        f"python3 tools/open_lane.py"
        f" --lane {lane_id}"
        f" --domain {domain}"
        f" --frontier '{domain_path}'"
        f" --expect '{expect}'"
        f" --artifact '{artifact}'"
        f" --note 'Council seat fill: {domain} (score={score}). {frontier_hint[:60]}'"
    )


def assess_health(occupied: int, top10: list[dict]) -> str:
    if occupied >= HEALTHY_SEATS:
        return "HEALTHY"
    elif occupied >= DEGRADED_SEATS:
        return "DEGRADED"
    else:
        return "CRITICAL"


def main() -> None:
    parser = argparse.ArgumentParser(description="Swarm Council Seat Status + Activation")
    parser.add_argument("--auto", action="store_true",
                        help="Print open_lane.py commands for all vacant seats")
    parser.add_argument("--json", action="store_true", help="Machine-readable JSON output")
    parser.add_argument("--session", default=f"S{date.today().strftime('%y%m%d')}",
                        help="Session tag for generated lane IDs (e.g. S336)")
    parser.add_argument("--top", type=int, default=10, help="How many seats to show (default 10)")
    args = parser.parse_args()

    top10 = get_top10_domains()
    if not top10:
        print("[ERROR] Could not load domain rankings.")
        sys.exit(1)

    active_lanes = get_active_domex_lanes()
    seats = []
    for i, d in enumerate(top10[:args.top], 1):
        domain = d["domain"]
        abbrev = domain_to_abbrev(domain)
        # Check vacancy: look for matching abbreviation in active lanes
        lane_id = active_lanes.get(abbrev.lower()) or active_lanes.get(domain.split("-")[0])
        # Also check by domain keyword directly
        for key, lid in active_lanes.items():
            if key in domain.lower() or domain.lower() in key:
                lane_id = lid
                break
        frontier = get_domain_frontier(domain)
        seats.append({
            "seat": f"C-{i:02d}",
            "domain": domain,
            "abbrev": abbrev,
            "score": d["score"],
            "active_lane": lane_id,
            "status": "OCCUPIED" if lane_id else "VACANT",
            "frontier": frontier,
        })

    occupied = sum(1 for s in seats if s["status"] == "OCCUPIED")
    health = assess_health(occupied, top10)

    if args.json:
        print(json.dumps({
            "health": health,
            "occupied": occupied,
            "total": len(seats),
            "seats": seats,
        }, indent=2))
        return

    # Human-readable table
    print(f"=== COUNCIL SEAT STATUS | Health: {health} | {occupied}/{len(seats)} seats occupied ===\n")
    print(f"{'Seat':<6} {'Domain':<22} {'Score':>6} {'Status':<10} {'Active Lane':<24} Frontier")
    print("-" * 100)
    for s in seats:
        lane_str = s["active_lane"] or "-"
        f_short = s["frontier"][:40]
        marker = "  " if s["status"] == "OCCUPIED" else "★ "
        print(f"{marker}{s['seat']:<4} {s['domain']:<22} {s['score']:>6.1f} {s['status']:<10} {lane_str:<24} {f_short}")

    print(f"\n★ = vacant seat (needs DOMEX lane)")
    vacant = [s for s in seats if s["status"] == "VACANT"]
    print(f"\nVacant seats: {len(vacant)} / {len(seats)}")

    if vacant:
        print("\n--- Council activation commands (run to fill vacant seats) ---")
        for s in vacant:
            cmd = build_open_lane_cmd(s["domain"], s["score"], args.session, s["frontier"])
            print(f"\n# {s['seat']} — {s['domain']} (score={s['score']})")
            print(cmd)

    if args.auto:
        print("\n\n=== AUTO MODE: pipe these to bash ===")
        for s in vacant:
            cmd = build_open_lane_cmd(s["domain"], s["score"], args.session, s["frontier"])
            print(cmd)


if __name__ == "__main__":
    main()
