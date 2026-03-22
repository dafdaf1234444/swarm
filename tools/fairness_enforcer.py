#!/usr/bin/env python3
"""fairness_enforcer.py — Remediate fairness gaps (PHIL-25, L-1193)

Computes per-domain neglect scores from visit recency, lesson count,
principle representation, and frontier count. Generates remediation actions.

Usage:
  python3 tools/fairness_enforcer.py --report   # analysis only
  python3 tools/fairness_enforcer.py --apply    # write action file + lane commands
  python3 tools/fairness_enforcer.py --json     # machine-readable
"""
import argparse, json, re, sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from swarm_io import REPO_ROOT, read_text, session_number, lesson_paths

DOMAINS_DIR = REPO_ROOT / "domains"
LANES_FILE = REPO_ROOT / "tasks" / "SWARM-LANES.md"
PRINCIPLES_FILE = REPO_ROOT / "memory" / "PRINCIPLES.md"
VISIT_NEGLECT = 50; LESSON_MIN = 2; PRINCIPLE_MIN = 1; FRONTIER_MIN = 1; TOP_N = 10


def list_domains():
    if not DOMAINS_DIR.exists(): return []
    return sorted(d.name for d in DOMAINS_DIR.iterdir() if d.is_dir() and not d.name.startswith("."))


def parse_lane_visits(lanes_text):
    """Map domain abbrev -> max session from DOMEX lanes."""
    visits = defaultdict(int)
    for m in re.finditer(r'DOMEX-(\w+)-S(\d+)', lanes_text):
        abbrev, sess = m.group(1).lower(), int(m.group(2))
        visits[abbrev] = max(visits[abbrev], sess)
    return dict(visits)


def build_abbrev_map():
    try:
        from domain_map import LANE_ABBREV_TO_DOMAIN
        return {k.lower(): v for k, v in LANE_ABBREV_TO_DOMAIN.items()}
    except ImportError:
        return {}


def scan_lessons():
    """Single pass: return (domain->count, domain->max_session)."""
    counts, recency = Counter(), defaultdict(int)
    for lp in lesson_paths():
        text = read_text(lp)[:500]
        dm = re.search(r'[Dd]omain:\s*(\S+)', text)
        if not dm: continue
        dom = dm.group(1).lower().strip()
        counts[dom] += 1
        sm = re.search(r'[Ss]ession:\s*S?(\d+)', text)
        if sm: recency[dom] = max(recency[dom], int(sm.group(1)))
    return counts, dict(recency)


def count_domain_principles():
    text = read_text(PRINCIPLES_FILE).lower()
    return Counter({dom: len(re.findall(dom.replace("-", r"[\s-]"), text)) for dom in list_domains()})


def count_domain_frontiers():
    results = {}
    for dom in list_domains():
        fp = DOMAINS_DIR / dom / "tasks" / "FRONTIER.md"
        if not fp.exists():
            results[dom] = (0, 0); continue
        text = read_text(fp)
        results[dom] = (
            len(re.findall(r'Status:\s*OPEN', text, re.I)),
            len(re.findall(r'Status:\s*(CLOSED|RESOLVED|CONFIRMED|FALSIFIED)', text, re.I)),
        )
    return results


def compute_neglect_scores():
    cur = session_number(); domains = list_domains()
    lane_visits = parse_lane_visits(read_text(LANES_FILE))
    amap = build_abbrev_map()
    dom_visit = {}
    for abbrev, sess in lane_visits.items():
        d = amap.get(abbrev, abbrev)
        dom_visit[d] = max(dom_visit.get(d, 0), sess)
    lesson_counts, lesson_recency = scan_lessons()
    princ_counts = count_domain_principles()
    frontier_data = count_domain_frontiers()
    scores = []
    for dom in domains:
        lv = dom_visit.get(dom, 0)
        vgap = cur - lv if lv > 0 else cur
        lessons = lesson_counts.get(dom, 0)
        lr = lesson_recency.get(dom, 0)
        lgap = cur - lr if lr > 0 else cur
        princ = princ_counts.get(dom, 0)
        af, rf = frontier_data.get(dom, (0, 0))
        # Composite: higher = more neglected (0-100 scale)
        composite = (min(vgap / VISIT_NEGLECT, 2.0) * 25  # 0-50 visit
                     + max(0, (LESSON_MIN - lessons) / LESSON_MIN) * 15  # 0-15 lesson
                     + (15 if princ < PRINCIPLE_MIN else 0)  # 0-15 principle
                     + (20 if af < FRONTIER_MIN else 0))  # 0-20 frontier
        scores.append({"domain": dom, "neglect_score": round(composite, 1),
                        "last_visit_session": lv, "visit_gap": vgap,
                        "lesson_count": lessons, "lesson_gap": lgap,
                        "principle_refs": princ, "active_frontiers": af, "resolved_frontiers": rf})
    scores.sort(key=lambda x: x["neglect_score"], reverse=True)
    return scores


def generate_actions(scores, cur):
    actions = []
    for e in scores[:TOP_N]:
        dom = e["domain"]
        if e["visit_gap"] >= VISIT_NEGLECT:
            lv = e["last_visit_session"]
            actions.append({"type": "open_domex_lane", "domain": dom,
                "reason": f"neglected {e['visit_gap']}s (last S{lv or 'never'})",
                "cmd": (f"python3 tools/open_lane.py --lane DOMEX-{dom.upper()[:4]}-S{cur} "
                        f"--session S{cur} --focus domains/{dom} "
                        f"--intent 'fairness-enforced: neglected {e['visit_gap']}s' "
                        f"--expect 'at-least-1-lesson-from-{dom}' "
                        f"--artifact 'experiments/{dom}/fairness-s{cur}.json'")})
        if e["active_frontiers"] < FRONTIER_MIN:
            actions.append({"type": "generate_frontier", "domain": dom, "reason": "0 active frontiers"})
        if e["principle_refs"] < PRINCIPLE_MIN:
            actions.append({"type": "create_principle", "domain": dom, "reason": "0 principles reference domain"})
    return actions


def print_report(scores, actions, cur):
    neglected = sum(1 for s in scores if s["neglect_score"] >= 50)
    print(f"=== FAIRNESS ENFORCER — S{cur} ===\n")
    print(f"Domains: {len(scores)} | Neglected (>=50): {neglected}\n")
    print(f"{'Domain':<25} {'Score':>6} {'LastVisit':>10} {'Lessons':>8} {'Princ':>6} {'Front':>6}")
    print("-" * 67)
    for e in scores[:TOP_N]:
        vg = f"S{e['last_visit_session']}" if e["last_visit_session"] else "never"
        print(f"{e['domain']:<25} {e['neglect_score']:>6.1f} {vg:>10} "
              f"{e['lesson_count']:>8} {e['principle_refs']:>6} {e['active_frontiers']:>6}")
    if actions:
        print(f"\n--- Remediation actions ({len(actions)}) ---")
        for a in actions:
            label = {"open_domex_lane": "LANE", "generate_frontier": "FRONTIER",
                     "create_principle": "PRINCIPLE"}.get(a["type"], a["type"])
            print(f"  {label}: {a['domain']} — {a['reason']}")


def apply_actions(actions, cur):
    out = REPO_ROOT / "experiments" / "meta" / f"fairness-actions-s{cur}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w") as f:
        json.dump({"session": cur, "actions": actions}, f, indent=2)
    print(f"\nActions written to {out}")
    cmds = [a["cmd"] for a in actions if a.get("cmd")]
    if cmds:
        print(f"\nLane commands ({len(cmds)}):")
        for c in cmds[:5]: print(f"  {c}")
        if len(cmds) > 5: print(f"  ... +{len(cmds)-5} more (see JSON)")


def main():
    ap = argparse.ArgumentParser(description="Fairness gap remediation (PHIL-25)")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--report", action="store_true", help="Analysis only")
    g.add_argument("--apply", action="store_true", help="Write action file + lane commands")
    g.add_argument("--json", action="store_true", help="Machine-readable JSON")
    args = ap.parse_args()
    cur = session_number(); scores = compute_neglect_scores(); actions = generate_actions(scores, cur)
    if args.json:
        print(json.dumps({"session": cur, "scores": scores[:TOP_N], "actions": actions}, indent=2))
    elif args.report:
        print_report(scores, actions, cur)
    elif args.apply:
        print_report(scores, actions, cur)
        apply_actions(actions, cur)


if __name__ == "__main__":
    main()
