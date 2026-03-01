#!/usr/bin/env python3
"""
Dispatch Optimizer — Expert Economy Tool (F-ECO4)
Scores and ranks domain experiments by expected yield (Sharpe × ISO × maturity).
Addresses structural unemployment of expert capacity (63 unrun experiments, 2% throughput).

Usage:
    python3 tools/dispatch_optimizer.py                 # Top-10 recommendations
    python3 tools/dispatch_optimizer.py --all           # Full ranked list
    python3 tools/dispatch_optimizer.py --domain X      # Score single domain
    python3 tools/dispatch_optimizer.py --json          # JSON output
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path


DOMAINS_DIR = Path("domains")
EXPERIMENTS_DIR = Path("experiments")
LANES_FILE = Path("tasks/SWARM-LANES.md")

# Domain heat: evaporation constant per session gap (S340 council: 5/5 convergence)
# Domains touched recently get a penalty; dormant domains get a bonus.
HEAT_DECAY = 0.85  # pheromone decays by 15% per session gap
HEAT_PENALTY_MAX = 6.0  # max score penalty for hot domains
DORMANT_BONUS = 3.0  # bonus for domains untouched >5 sessions
SELF_DISPATCH_INTERVAL = 10  # expert-swarm must dispatch to itself every N sessions (L-501 P6)

# Outcome feedback (F-EXP10, L-501 P1): reward consistently productive domains.
# Closes PHIL-2 self-application gap — expert dispatch learns from its own outcomes.
LANE_ABBREV_TO_DOMAIN = {
    "NK": "nk-complexity", "LNG": "linguistics", "EXP": "expert-swarm",
    "STAT": "statistics", "PHI": "philosophy", "CTX": "meta", "MECH": "meta",
    "FLD": "fluid-dynamics", "BRN": "brain", "HLP": "helper-swarm",
    "ECO": "economy", "PHY": "physics", "SCI": "evaluation", "EVO": "philosophy",
    "DNA": "meta", "IS": "information-science", "HS": "human-systems",
    "COMP": "competitions", "INFO": "information-science",
}
# COUNCIL-TOPIC-SN: map council topic to domain (F-EXP10 L-506: COUNCIL lanes were
# previously unattributed, causing ~30-40% outcome data loss for meta/expert-swarm)
COUNCIL_TOPIC_TO_DOMAIN = {
    "AGENT-AWARE": "meta", "SCIENCE": "evaluation", "DNA": "meta",
    "EXPERT-SWARM": "expert-swarm", "USE-CASES": "meta",
}
OUTCOME_MIN_N = 3          # minimum completed lanes before feedback kicks in
OUTCOME_SUCCESS_THRESHOLD = 0.75  # MERGED rate above which domain is PROVEN
OUTCOME_FAILURE_THRESHOLD = 0.50  # MERGED rate below which domain is STRUGGLING
OUTCOME_BONUS = 1.5        # score bonus for PROVEN domains
OUTCOME_PENALTY = 1.0      # score penalty for STRUGGLING domains


def _get_domain_heat() -> dict[str, int]:
    """Parse SWARM-LANES.md to find the most recent session each domain was active.

    Returns {domain_name: last_active_session_number}.
    Used for anti-clustering: recently active domains get a score penalty.
    """
    heat = {}
    if not LANES_FILE.exists():
        return heat
    content = LANES_FILE.read_text()
    for line in content.splitlines():
        if not line.startswith("|") or line.startswith("| ---") or line.startswith("| Date"):
            continue
        cols = [c.strip() for c in line.split("|")]
        if len(cols) < 12:
            continue
        etc = cols[10] if len(cols) > 10 else ""
        status = cols[11] if len(cols) > 11 else ""
        # Extract domain from focus= field
        focus_m = re.search(r"focus=(?:domains/)?([a-z0-9-]+)", etc)
        if not focus_m:
            continue
        dom = focus_m.group(1)
        # Extract session number
        sess_str = cols[3] if len(cols) > 3 else ""
        sess_m = re.search(r"S?(\d+)", sess_str)
        if not sess_m:
            continue
        sess = int(sess_m.group(1))
        if dom not in heat or sess > heat[dom]:
            heat[dom] = sess
    return heat


def _get_current_session() -> int:
    """Get current session number from INDEX.md."""
    idx = Path("memory/INDEX.md")
    if not idx.exists():
        return 340
    text = idx.read_text()[:500]
    m = re.search(r"Sessions:\s*(\d+)", text)
    return int(m.group(1)) if m else 340


def _get_claimed_domains() -> set[str]:
    """Get domains currently claimed by active agents (from agent_state.py)."""
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("agent_state", Path("tools/agent_state.py"))
        if spec and spec.loader:
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            return set(mod.get_active_domains())
    except Exception:
        pass
    return set()


def _get_domain_outcomes() -> dict[str, dict]:
    """Parse SWARM-LANES.md for MERGED/ABANDONED counts and lesson yield per domain (F-EXP10).

    Returns {domain_name: {"merged": int, "abandoned": int, "lessons": int}}.
    - merged/abandoned: binary outcome (existing)
    - lessons: L-NNN references in notes column (yield quality signal — L-506)
    Outcome feedback: reward proven domains, flag struggling ones.
    """
    outcomes: dict[str, dict] = {}
    if not LANES_FILE.exists():
        return outcomes
    content = LANES_FILE.read_text()
    for line in content.splitlines():
        if not line.startswith("|") or line.startswith("| ---") or line.startswith("| Date"):
            continue
        cols = [c.strip() for c in line.split("|")]
        if len(cols) < 12:
            continue
        lane_id = cols[2] if len(cols) > 2 else ""
        status = cols[11] if len(cols) > 11 else ""
        if status not in ("MERGED", "ABANDONED"):
            continue

        # Try domain from DOMEX lane name: DOMEX-ABBREV-SN
        domain = None
        m = re.match(r"DOMEX-([A-Z]+)", lane_id)
        if m:
            domain = LANE_ABBREV_TO_DOMAIN.get(m.group(1))

        # COUNCIL-TOPIC-SN: attribute council lanes to domain (L-506: was causing
        # ~30-40% outcome data loss for meta/expert-swarm — COUNCIL lanes unattributed)
        if not domain:
            m = re.match(r"COUNCIL-([A-Z-]+)-S\d+", lane_id)
            if m:
                domain = COUNCIL_TOPIC_TO_DOMAIN.get(m.group(1))

        # Fallback: focus= field (skip if "global")
        if not domain:
            etc = cols[10] if len(cols) > 10 else ""
            fm = re.search(r"focus=(?:domains/)?([a-z0-9-]+)", etc)
            if fm and fm.group(1) not in ("global", ""):
                domain = fm.group(1)

        if domain:
            if domain not in outcomes:
                outcomes[domain] = {"merged": 0, "abandoned": 0, "lessons": 0}
            outcomes[domain]["merged" if status == "MERGED" else "abandoned"] += 1
            # Lesson yield: count L-NNN references in notes column
            notes = cols[12] if len(cols) > 12 else ""
            lesson_count = len(re.findall(r"\bL-\d{3,4}\b", notes))
            outcomes[domain]["lessons"] += lesson_count
    return outcomes


def score_domain(domain: str) -> dict | None:
    """Compute expected yield score for a domain's open frontiers."""
    frontier_path = DOMAINS_DIR / domain / "tasks" / "FRONTIER.md"
    domain_md_path = DOMAINS_DIR / domain / "DOMAIN.md"
    index_path = DOMAINS_DIR / domain / "INDEX.md"

    if not frontier_path.exists():
        return None

    content = frontier_path.read_text()

    # Active frontier count (lines with - **F or - **F-prefix)
    active_count = len(re.findall(r"^- \*\*F", content, re.MULTILINE))
    if active_count == 0:
        return None  # Skip domains with no open work

    # Resolved count (rows in Resolved table)
    resolved_count = 0
    resolved_match = re.search(r"## Resolved.*", content, re.DOTALL)
    if resolved_match:
        resolved_count = len(re.findall(r"^\| F", resolved_match.group(), re.MULTILINE))

    # Concept counts from DOMAIN.md (multi-concept expertise — S346 human signal)
    iso_count = 0
    lesson_count = 0
    belief_count = 0
    principle_count = 0
    if domain_md_path.exists():
        dm = domain_md_path.read_text()
        iso_count = len(set(re.findall(r"ISO-\d+", dm)))
        lesson_count = len(set(re.findall(r"\bL-\d{3,4}\b", dm)))
        belief_count = len(set(re.findall(r"\bB-?\d+\b", dm)))
        principle_count = len(set(re.findall(r"\bP-\d{3}\b", dm)))

    # Experiment count (JSON artifacts produced)
    exp_dir = EXPERIMENTS_DIR / domain
    exp_count = 0
    if exp_dir.exists():
        exp_count = len(list(exp_dir.glob("*.json")))

    # Has domain INDEX (team has oriented and knows state)
    has_index = index_path.exists()

    # --- Yield score formula ---
    # Multi-concept scoring (S346 human signal: expertise beyond isomorphisms)
    # iso_count * 2.0     : cross-domain leverage (rebalanced from 3.0)
    # lesson_count * 0.5  : empirical grounding (domain has generated findings)
    # belief_count * 2.0  : tested claims (high-value knowledge)
    # resolved * 2.0      : domain maturity (team knows how to extract lessons here)
    # active * 1.5        : open work (demand signal)
    # novelty +2.0        : uncharted territory bonus (exp_count == 0)
    # has_index +1.0      : orientation artifact present
    # concept_diversity * 2.0 : breadth reward (how many concept types present)
    novelty_bonus = 2.0 if exp_count == 0 else 0.0
    concept_types = sum([
        iso_count > 0,
        lesson_count > 0,
        belief_count > 0,
        principle_count > 0,
        exp_count > 0,
    ])
    score = (
        iso_count * 2.0
        + lesson_count * 0.5
        + belief_count * 2.0
        + concept_types * 2.0
        + resolved_count * 2.0
        + active_count * 1.5
        + novelty_bonus
        + (1.0 if has_index else 0.0)
    )

    # Extract first open frontier description (dispatch target)
    first_frontier = ""
    match = re.search(r"^- (\*\*F[^*\n]+\*\*.*?)(?=^- \*\*F|\Z)", content, re.MULTILINE | re.DOTALL)
    if match:
        first_frontier = match.group(1).strip()[:120].replace("\n", " ")

    return {
        "domain": domain,
        "score": round(score, 1),
        "active": active_count,
        "resolved": resolved_count,
        "iso": iso_count,
        "lessons": lesson_count,
        "beliefs": belief_count,
        "principles": principle_count,
        "concept_types": concept_types,
        "experiments": exp_count,
        "has_index": has_index,
        "novelty_bonus": novelty_bonus > 0,
        "top_frontier": first_frontier,
    }


def run(args: argparse.Namespace) -> None:
    if not DOMAINS_DIR.exists():
        print("ERROR: domains/ directory not found. Run from repo root.", file=sys.stderr)
        sys.exit(1)

    results = []
    target_domains = [args.domain] if args.domain else sorted(os.listdir(DOMAINS_DIR))

    for domain in target_domains:
        r = score_domain(domain)
        if r:
            results.append(r)

    # Apply domain heat (anti-clustering: S340 council finding)
    current_session = _get_current_session()
    heat_map = _get_domain_heat()
    claimed = _get_claimed_domains()
    outcome_map = _get_domain_outcomes()
    sparse_domains = []
    saturated_domains = []

    for r in results:
        dom = r["domain"]
        last_active = heat_map.get(dom, 0)
        gap = current_session - last_active if last_active > 0 else 999

        # Heat penalty for recently active domains
        if gap <= 3:
            penalty = HEAT_PENALTY_MAX * (HEAT_DECAY ** gap)
            r["score"] -= penalty
            r["heat"] = "HOT"
            saturated_domains.append(dom)
        elif gap > 5:
            r["score"] += DORMANT_BONUS
            r["heat"] = "COLD"
            sparse_domains.append(dom)
        else:
            r["heat"] = "WARM"

        # Self-dispatch norm (L-501 P6, PHIL-2): expert-swarm must dispatch to itself
        # every SELF_DISPATCH_INTERVAL sessions. The dispatcher dispatching to itself
        # closes the self-application gap identified by 5-domain council (S343).
        if dom == "expert-swarm" and gap > SELF_DISPATCH_INTERVAL:
            self_bonus = DORMANT_BONUS * 2.0  # double dormant bonus for self-application
            r["score"] += self_bonus
            r["self_dispatch_due"] = True
        else:
            r["self_dispatch_due"] = False

        # Mark if currently claimed by another agent
        if dom in claimed:
            r["claimed"] = True
            r["score"] -= 10.0  # strong penalty — agent already there
        else:
            r["claimed"] = False

        # Outcome feedback (F-EXP10): adjust score based on historical lane success
        oc = outcome_map.get(dom, {"merged": 0, "abandoned": 0, "lessons": 0})
        n = oc["merged"] + oc["abandoned"]
        r["outcome_merged"] = oc["merged"]
        r["outcome_abandoned"] = oc["abandoned"]
        r["outcome_lessons"] = oc.get("lessons", 0)
        r["outcome_n"] = n
        if n >= OUTCOME_MIN_N:
            rate = oc["merged"] / n
            r["outcome_rate"] = round(rate, 2)
            if rate >= OUTCOME_SUCCESS_THRESHOLD:
                r["score"] += OUTCOME_BONUS
                r["outcome_label"] = "PROVEN"
            elif rate < OUTCOME_FAILURE_THRESHOLD:
                r["score"] -= OUTCOME_PENALTY
                r["outcome_label"] = "STRUGGLING"
            else:
                r["outcome_label"] = "MIXED"
        else:
            r["outcome_rate"] = None
            r["outcome_label"] = "NEW"

    results.sort(key=lambda x: x["score"], reverse=True)

    if not args.all and not args.domain:
        results = results[:10]

    if args.json:
        print(json.dumps(results, indent=2))
        return

    # Human-readable output
    print("\n=== DISPATCH OPTIMIZER (F-ECO4) ===")
    print(f"Expert economy: rank open frontiers by expected yield\n")

    # Domain gradient (S340 council: 4/5 convergence on visibility)
    if sparse_domains or saturated_domains:
        if sparse_domains:
            print(f"  SPARSE (bonus +{DORMANT_BONUS}): {', '.join(sparse_domains[:6])}")
        if saturated_domains:
            print(f"  SATURATED (penalty): {', '.join(saturated_domains[:6])}")
        if claimed:
            print(f"  CLAIMED (by active agent): {', '.join(claimed)}")
        print()

    print(f"{'Score':>6}  {'Domain':<25}  {'Act':>3}  {'Res':>3}  {'ISO':>3}  {'L':>3}  {'B':>2}  {'P':>3}  {'CT':>2}  {'Heat':>4}")
    print("-" * 85)

    for r in results:
        heat_icon = {"HOT": "🔥", "WARM": "~", "COLD": "❄"}.get(r.get("heat", ""), " ")
        claimed_mark = " [CLAIMED]" if r.get("claimed") else (" [SELF-DUE]" if r.get("self_dispatch_due") else "")
        label = r.get("outcome_label", "NEW")
        n = r.get("outcome_n", 0)
        lessons_str = f" {r.get('outcome_lessons', 0)}L" if r.get("outcome_lessons", 0) > 0 else ""
        outcome_tag = f" [{label} {r['outcome_merged']}/{n}{lessons_str}]" if n >= OUTCOME_MIN_N else ""
        print(
            f"{r['score']:6.1f}  {r['domain']:<25}  {r['active']:3d}  {r['resolved']:3d}  "
            f"{r['iso']:3d}  {r['lessons']:3d}  {r['beliefs']:2d}  {r['principles']:3d}  "
            f"{r['concept_types']:2d}  {heat_icon:>4}{claimed_mark}{outcome_tag}"
        )
        if r["top_frontier"]:
            print(f"         → {r['top_frontier'][:72]}")

    print("\n--- Scoring formula (multi-concept, S346) ---")
    print("  Columns: Act=active frontiers, Res=resolved, ISO=isomorphisms, L=lessons, B=beliefs, P=principles, CT=concept types")
    print("  score = iso*2 + lessons*0.5 + beliefs*2 + concept_types*2 + resolved*2 + active*1.5 + novelty(2) + index(1)")
    print(f"  + dormant_bonus(+{DORMANT_BONUS} if >5 sessions cold) - heat_penalty(up to -{HEAT_PENALTY_MAX} if <3 sessions)")
    print(f"  + outcome_bonus(+{OUTCOME_BONUS} PROVEN: ≥{OUTCOME_MIN_N} lanes, rate≥{OUTCOME_SUCCESS_THRESHOLD})")
    print(f"  - outcome_penalty(-{OUTCOME_PENALTY} STRUGGLING: ≥{OUTCOME_MIN_N} lanes, rate<{OUTCOME_FAILURE_THRESHOLD})")
    print(f"  Heat map: {len(saturated_domains)} HOT, {len(sparse_domains)} COLD, {len(claimed)} claimed")
    print(f"\n  Showing {'all' if args.all else 'top 10'} of {len(results)} domains with open work.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Dispatch Optimizer — rank domain experiments by expected yield")
    parser.add_argument("--all", action="store_true", help="Show all domains, not just top 10")
    parser.add_argument("--domain", metavar="NAME", help="Score a single domain")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()
