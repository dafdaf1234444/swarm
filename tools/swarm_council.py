#!/usr/bin/env python3
"""
swarm_council.py — Data-driven council deliberation tool.

Convenes a multi-role council that reads actual corpus data (lessons, beliefs,
principles, frontiers) to produce evidence-based deliberation memos.

Three modes:
  Mode A — Domain deliberation: cross-domain expert synthesis on a question
  Mode B — Axiom sunset audit: flags axiom claims overdue for re-grounding
  Mode R — Repair deliberation: multi-role diagnosis of a swarm problem

Usage:
  python3 tools/swarm_council.py --domains meta,epistemology --question "What limits expert utilization?"
  python3 tools/swarm_council.py --axiom-audit              # Mode B: axiom sunset check
  python3 tools/swarm_council.py --target "forecasting calibration"  # Mode R: repair
  python3 tools/swarm_council.py --deference-ratio           # L-1507: human signal acceptance ratio
  python3 tools/swarm_council.py --list-roles
  python3 tools/swarm_council.py --last
  python3 tools/swarm_council.py --json                      # machine-readable output

L-1507 prescribed fixes implemented:
  - axiom_sunset: --axiom-audit flags PHIL claims >50 sessions without grounding challenge
  - rejection_quota: --deference-ratio measures human signal acceptance vs rejection
  - expectation_precision_gate: wired into open_lane.py (>10 words, numeric prediction)
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
PERSONALITIES_DIR = ROOT / "tools" / "personalities"
WORKSPACE_DIR = ROOT / "workspace"
DOMAINS_DIR = ROOT / "domains"
LESSONS_DIR = ROOT / "memory" / "lessons"
PHILOSOPHY_MD = ROOT / "beliefs" / "PHILOSOPHY.md"
SIGNALS_MD = ROOT / "tasks" / "SIGNALS.md"
LANES_FILE = ROOT / "tasks" / "SWARM-LANES.md"

ROLE_PERSPECTIVE_PROMPTS = {
    "skeptic": "What evidence is missing? What claims here are unsupported?",
    "adversary": "What is the worst-case outcome if we do nothing?",
    "synthesizer": "What cross-domain patterns apply? What is the minimal common structure?",
    "council-expert": "What are the top 3 prioritized actions? Who owns each one?",
    "vice-versa-expert": "Which reciprocal loops are broken here?",
    "reality-check": "Is this problem measured or inferred? What would falsify the diagnosis?",
    "historian": "Has this appeared before? What did prior sessions do?",
    "danger-expert": "What failure modes does this repair introduce?",
}

DEFAULT_REPAIR_ROLES = ["skeptic", "adversary", "synthesizer", "council-expert"]


def get_current_session() -> int:
    """Get current session number from git log."""
    try:
        import subprocess
        r = subprocess.run(
            ["git", "log", "--oneline", "-10"],
            capture_output=True, text=True, cwd=ROOT,
        )
        nums = [int(m) for m in re.findall(r"\[S(\d+)\]", r.stdout)]
        return max(nums) if nums else 0
    except Exception:
        return 0


def load_philosophy_claims() -> list[dict]:
    """Parse PHILOSOPHY.md for PHIL-N claims with metadata."""
    if not PHILOSOPHY_MD.exists():
        return []
    text = PHILOSOPHY_MD.read_text(errors="replace")
    claims = []

    # Parse challenge table
    in_table = False
    for line in text.splitlines():
        if "| PHIL-" in line and "|" in line:
            cols = [c.strip() for c in line.split("|")]
            if len(cols) >= 6:
                phil_id = cols[1].strip()
                description = cols[2].strip()[:120]
                classification = cols[3].strip()
                grounding = cols[4].strip()
                status_detail = cols[5].strip()

                # Extract last session mentioned
                sess_matches = re.findall(r"S(\d+)", status_detail)
                last_session = max(int(s) for s in sess_matches) if sess_matches else 0

                # Count challenges mentioned
                challenge_count = status_detail.lower().count("challenge")
                drop_count = status_detail.lower().count("drop")

                claims.append({
                    "id": phil_id,
                    "description": description,
                    "classification": classification,
                    "grounding": grounding,
                    "status": status_detail[:200],
                    "last_session": last_session,
                    "challenges": challenge_count,
                    "drops": drop_count,
                    "is_axiom": classification.strip().lower() == "axiom",
                    "is_dropped": "DROPPED" in status_detail.upper(),
                })
    return claims


def load_domain_context(domain: str) -> dict:
    """Load domain-specific context: vocab, top frontier, recent lessons."""
    domain_path = DOMAINS_DIR / domain
    ctx = {"domain": domain, "vocab": "", "top_frontier": "", "lesson_count": 0, "iso_links": []}

    domain_md = domain_path / "DOMAIN.md"
    if domain_md.exists():
        text = domain_md.read_text(errors="replace")
        # Extract ISO links
        ctx["iso_links"] = list(set(re.findall(r"ISO-\d+", text)))[:5]
        # Extract Adjacent: header
        adj_m = re.search(r"Adjacent:\s*(.+)", text)
        if adj_m:
            ctx["adjacent"] = adj_m.group(1).strip()[:200]

    frontier_md = domain_path / "tasks" / "FRONTIER.md"
    if frontier_md.exists():
        content = frontier_md.read_text(errors="replace")
        m = re.search(r"\*\*(F[^\*]+)\*\*[:\s]+(.*)", content)
        if m:
            ctx["top_frontier"] = f"{m.group(1)}: {m.group(2)[:120].strip()}"

    # Count domain lessons
    if LESSONS_DIR.exists():
        for lf in LESSONS_DIR.glob("L-*.md"):
            try:
                head = lf.read_text(errors="replace")[:300]
                if f"Domain: {domain}" in head or f"domain: {domain}" in head:
                    ctx["lesson_count"] += 1
            except Exception:
                pass

    return ctx


def load_recent_lessons(n: int = 30) -> list[dict]:
    """Load recent lessons with metadata."""
    if not LESSONS_DIR.exists():
        return []
    lessons = []
    files = sorted(LESSONS_DIR.glob("L-*.md"), key=lambda p: p.stat().st_mtime, reverse=True)[:n]
    for lf in files:
        try:
            text = lf.read_text(errors="replace")
            lines = text.splitlines()
            title = lines[0] if lines else lf.stem
            # Extract session
            sess_m = re.search(r"Session:\s*S?(\d+)", text[:500])
            session = int(sess_m.group(1)) if sess_m else 0
            # Extract domain
            dom_m = re.search(r"Domain:\s*(\S+)", text[:500])
            domain = dom_m.group(1) if dom_m else "unknown"
            # Extract Sharpe
            sh_m = re.search(r"Sharpe:\s*(\d+)", text[:500])
            sharpe = int(sh_m.group(1)) if sh_m else 0
            # Extract level
            lvl_m = re.search(r"level=(L\d)", text[:500])
            level = lvl_m.group(1) if lvl_m else "L2"
            lessons.append({
                "id": lf.stem,
                "title": title[:120],
                "session": session,
                "domain": domain,
                "sharpe": sharpe,
                "level": level,
            })
        except Exception:
            pass
    return lessons


# --- Mode A: Domain Deliberation ---

def domain_deliberate(domains: list[str], question: str) -> dict:
    """Mode A: cross-domain expert deliberation with real data."""
    cur_sess = get_current_session()
    domain_contexts = [load_domain_context(d) for d in domains]
    recent_lessons = load_recent_lessons(50)

    deliberation = {
        "mode": "domain",
        "question": question,
        "domains": domains,
        "session": f"S{cur_sess}",
        "timestamp": datetime.now().isoformat(),
        "domain_perspectives": {},
        "cross_domain_patterns": [],
        "evidence_base": {},
        "action_memo": [],
    }

    for ctx in domain_contexts:
        # Find domain-specific lessons
        dom_lessons = [l for l in recent_lessons if l["domain"] == ctx["domain"]]
        high_sharpe = [l for l in dom_lessons if l["sharpe"] >= 8]

        deliberation["domain_perspectives"][ctx["domain"]] = {
            "question_applied": question,
            "top_frontier": ctx.get("top_frontier") or "[no open frontier]",
            "iso_links": ", ".join(ctx["iso_links"]) or "none",
            "lesson_count": ctx["lesson_count"],
            "recent_lessons": len(dom_lessons),
            "high_sharpe_lessons": [l["id"] for l in high_sharpe[:5]],
            "adjacent": ctx.get("adjacent", "none"),
        }

    # Cross-domain patterns: shared ISO, shared lessons
    all_iso = []
    for ctx in domain_contexts:
        all_iso.extend(ctx["iso_links"])
    shared_iso = [iso for iso in set(all_iso) if all_iso.count(iso) > 1]

    if shared_iso:
        deliberation["cross_domain_patterns"].append(
            f"Shared ISO: {', '.join(sorted(shared_iso))} — structural convergence"
        )
    else:
        deliberation["cross_domain_patterns"].append(
            "No shared ISO — domains are orthogonal on this question"
        )

    # Evidence base: what lessons/principles are relevant
    relevant_lessons = [l for l in recent_lessons
                        if l["domain"] in domains and l["sharpe"] >= 6]
    deliberation["evidence_base"] = {
        "total_relevant_lessons": len(relevant_lessons),
        "top_evidence": [f"{l['id']} (Sh={l['sharpe']}, {l['domain']})"
                         for l in sorted(relevant_lessons, key=lambda x: -x["sharpe"])[:5]],
    }

    deliberation["action_memo"] = [
        {
            "rank": 1,
            "action": f"Open DOMEX lane for highest-score vacant domain on: {question[:60]}",
            "evidence": f"{len(relevant_lessons)} relevant lessons, {len(shared_iso)} shared ISO",
        },
        {
            "rank": 2,
            "action": "Cross-link findings: synthesis lesson citing 1 lesson per domain",
        },
        {
            "rank": 3,
            "action": "Run dream.py resonance scan across domain DOMAIN.md files",
        },
    ]

    return deliberation


# --- Mode B: Axiom Sunset Audit (L-1507 fix) ---

def axiom_sunset_audit() -> dict:
    """Audit axiom claims for re-grounding need. L-1507: axiom_sunset prescribed fix."""
    cur_sess = get_current_session()
    claims = load_philosophy_claims()
    SUNSET_THRESHOLD = 50  # sessions without grounding challenge

    audit = {
        "mode": "axiom_sunset",
        "session": f"S{cur_sess}",
        "timestamp": datetime.now().isoformat(),
        "threshold_sessions": SUNSET_THRESHOLD,
        "axiom_claims": [],
        "overdue": [],
        "summary": {},
    }

    axioms = [c for c in claims if c["is_axiom"] and not c["is_dropped"]]
    audit["axiom_claims"] = [
        {
            "id": c["id"],
            "description": c["description"],
            "grounding": c["grounding"],
            "last_session": c["last_session"],
            "age": cur_sess - c["last_session"] if c["last_session"] else cur_sess,
            "challenges": c["challenges"],
            "drops": c["drops"],
        }
        for c in axioms
    ]

    overdue = [
        a for a in audit["axiom_claims"]
        if a["age"] > SUNSET_THRESHOLD
    ]
    audit["overdue"] = overdue

    # Special detection: axiom shield (0 challenges or 0 DROPs despite challenges)
    shielded = [
        a for a in audit["axiom_claims"]
        if a["challenges"] >= 3 and a["drops"] == 0
    ]

    audit["summary"] = {
        "total_axioms": len(axioms),
        "overdue_count": len(overdue),
        "shielded_count": len(shielded),
        "shielded_ids": [a["id"] for a in shielded],
        "recommendation": (
            "SUNSET REQUIRED" if overdue else "ALL AXIOMS CURRENT"
        ),
        "axiom_shield_detected": bool(shielded),
    }

    return audit


# --- Deference Ratio (L-1507 fix: rejection_quota) ---

def compute_deference_ratio() -> dict:
    """Measure human signal acceptance vs rejection ratio. L-1507: rejection_quota."""
    cur_sess = get_current_session()
    result = {
        "mode": "deference_ratio",
        "session": f"S{cur_sess}",
        "timestamp": datetime.now().isoformat(),
        "total_signals": 0,
        "implemented": 0,
        "rejected": 0,
        "deferred": 0,
        "acceptance_rate": 0.0,
        "phil13_violation": False,
        "recommendation": "",
    }

    if not SIGNALS_MD.exists():
        result["recommendation"] = "No SIGNALS.md found"
        return result

    text = SIGNALS_MD.read_text(errors="replace")
    # Count human-sourced signals
    for line in text.splitlines():
        if not line.startswith("|") or "SIG-" not in line:
            continue
        cols = [c.strip() for c in line.split("|")]
        if len(cols) < 5:
            continue
        # Check if signal is from human
        sig_text = " ".join(cols).lower()
        if "human" in sig_text or "directive" in sig_text:
            result["total_signals"] += 1
            status = sig_text
            if "implemented" in status or "resolved" in status or "done" in status:
                result["implemented"] += 1
            elif "rejected" in status or "declined" in status:
                result["rejected"] += 1
            else:
                result["deferred"] += 1

    total = result["implemented"] + result["rejected"]
    if total > 0:
        result["acceptance_rate"] = result["implemented"] / total
    else:
        result["acceptance_rate"] = 1.0  # default to full acceptance if no resolved signals

    # PHIL-13 violation: >95% acceptance rate over >20 signals = deference loop
    result["phil13_violation"] = (
        result["acceptance_rate"] > 0.95 and total > 20
    )

    # Recommendation
    quota_sessions = 50
    if result["rejected"] == 0 and total > 0:
        result["recommendation"] = (
            f"QUOTA BREACH: {result['implemented']}/{total} signals accepted, "
            f"0 rejected. PHIL-13 requires epistemic independence — reject >=1 "
            f"signal per {quota_sessions} sessions to test behavioral independence."
        )
    elif result["phil13_violation"]:
        result["recommendation"] = (
            f"DEFERENCE LOOP: {result['acceptance_rate']:.0%} acceptance rate "
            f"({result['implemented']}/{total}). Epistemic equality is not behavioral."
        )
    else:
        result["recommendation"] = (
            f"Acceptance rate {result['acceptance_rate']:.0%} "
            f"({result['implemented']} implemented, {result['rejected']} rejected, "
            f"{result['deferred']} deferred)"
        )

    return result


# --- Mode R: Repair Deliberation ---

def repair_deliberate(target: str, roles: list[str]) -> dict:
    """Mode R: multi-role repair deliberation with corpus evidence."""
    cur_sess = get_current_session()
    recent_lessons = load_recent_lessons(30)
    claims = load_philosophy_claims()

    deliberation = {
        "mode": "repair",
        "target": target,
        "session": f"S{cur_sess}",
        "timestamp": datetime.now().isoformat(),
        "roles": roles,
        "perspectives": {},
        "evidence_scan": {},
        "action_memo": [],
    }

    # Load personality context for each role
    for role in roles:
        fname = PERSONALITIES_DIR / f"{role}.md"
        personality = ""
        if fname.exists():
            personality = fname.read_text(errors="replace")[:300]
        prompt = ROLE_PERSPECTIVE_PROMPTS.get(role, "What is your expert view?")

        deliberation["perspectives"][role] = {
            "prompt": prompt,
            "personality_excerpt": personality[:200] if personality else "[no personality file]",
        }

    # Evidence scan: lessons mentioning the target topic
    target_words = set(target.lower().split())
    relevant = []
    for l in recent_lessons:
        title_words = set(l["title"].lower().split())
        overlap = len(target_words & title_words)
        if overlap >= 1 or any(w in l["title"].lower() for w in target_words):
            relevant.append(l)

    # Scan beliefs for relevance
    relevant_beliefs = [
        c for c in claims
        if any(w in c["description"].lower() for w in target_words)
    ]

    deliberation["evidence_scan"] = {
        "relevant_lessons": [f"{l['id']} (Sh={l['sharpe']})" for l in relevant[:5]],
        "relevant_beliefs": [f"{c['id']}: {c['description'][:60]}" for c in relevant_beliefs[:3]],
        "corpus_coverage": f"{len(relevant)} lessons, {len(relevant_beliefs)} beliefs",
    }

    deliberation["action_memo"] = [
        {
            "rank": 1,
            "action": f"Measure current state of '{target}' with a concrete metric",
            "owner": "reality-check or current-node",
        },
        {
            "rank": 2,
            "action": f"Dispatch skeptic to stress-test proposed repair for '{target}'",
            "owner": "council-expert",
        },
        {
            "rank": 3,
            "action": "Write lesson on findings (max 20 lines) and update relevant frontier",
            "owner": "current-node",
        },
    ]

    return deliberation


# --- Rendering ---

def render_domain_memo(d: dict) -> str:
    lines = [
        "# Swarm Council Domain Memo (Mode A)",
        f"**Question**: {d['question']}",
        f"**Domains**: {', '.join(d['domains'])}",
        f"**Session**: {d['session']}",
        f"**Timestamp**: {d['timestamp']}",
        "",
        "## Domain Perspectives",
    ]
    for domain, p in d["domain_perspectives"].items():
        lines.append(f"### {domain}")
        lines.append(f"- **Top frontier**: {p['top_frontier']}")
        lines.append(f"- **ISO links**: {p['iso_links']}")
        lines.append(f"- **Lessons**: {p['lesson_count']} total, {p['recent_lessons']} recent")
        if p.get("high_sharpe_lessons"):
            lines.append(f"- **High-Sharpe**: {', '.join(p['high_sharpe_lessons'])}")
        if p.get("adjacent") and p["adjacent"] != "none":
            lines.append(f"- **Adjacent**: {p['adjacent']}")
        lines.append("")

    lines.append("## Cross-Domain Patterns")
    for pat in d["cross_domain_patterns"]:
        lines.append(f"- {pat}")

    lines.append("")
    lines.append("## Evidence Base")
    eb = d["evidence_base"]
    lines.append(f"- Relevant lessons: {eb['total_relevant_lessons']}")
    for e in eb.get("top_evidence", []):
        lines.append(f"  - {e}")

    lines.append("")
    lines.append("## Action Memo")
    for item in d["action_memo"]:
        lines.append(f"{item['rank']}. **{item['action']}**")
        if "evidence" in item:
            lines.append(f"   Evidence: {item['evidence']}")

    return "\n".join(lines)


def render_axiom_audit(d: dict) -> str:
    s = d["summary"]
    lines = [
        "# Axiom Sunset Audit (L-1507)",
        f"**Session**: {d['session']}",
        f"**Threshold**: {d['threshold_sessions']} sessions",
        f"**Total axioms**: {s['total_axioms']}",
        f"**Overdue**: {s['overdue_count']}",
        f"**Axiom-shielded**: {s['shielded_count']} ({', '.join(s['shielded_ids'])})" if s['shielded_ids'] else "",
        f"**Recommendation**: {s['recommendation']}",
        "",
    ]

    if d["overdue"]:
        lines.append("## Overdue Axioms (need re-grounding)")
        lines.append(f"| ID | Description | Age | Grounding | Challenges |")
        lines.append(f"|-----|-------------|-----|-----------|------------|")
        for a in sorted(d["overdue"], key=lambda x: -x["age"]):
            lines.append(
                f"| {a['id']} | {a['description'][:50]} | {a['age']}s | {a['grounding']} | {a['challenges']} |"
            )

    if not d["overdue"]:
        lines.append("All axiom claims within sunset threshold.")

    return "\n".join(lines)


def render_deference(d: dict) -> str:
    lines = [
        "# Human Signal Deference Ratio (L-1507)",
        f"**Session**: {d['session']}",
        f"**Total signals**: {d['total_signals']}",
        f"**Implemented**: {d['implemented']}",
        f"**Rejected**: {d['rejected']}",
        f"**Deferred**: {d['deferred']}",
        f"**Acceptance rate**: {d['acceptance_rate']:.0%}",
        f"**PHIL-13 violation**: {'YES' if d['phil13_violation'] else 'No'}",
        f"**Recommendation**: {d['recommendation']}",
    ]
    return "\n".join(lines)


def render_repair_memo(d: dict) -> str:
    lines = [
        "# Swarm Council Repair Memo (Mode R)",
        f"**Target**: {d['target']}",
        f"**Session**: {d['session']}",
        f"**Council**: {', '.join(d['roles'])}",
        "",
        "## Perspectives",
    ]
    for role, p in d["perspectives"].items():
        lines.append(f"### {role}")
        lines.append(f"*Prompt*: {p['prompt']}")
        lines.append("")

    lines.append("## Evidence Scan")
    es = d["evidence_scan"]
    lines.append(f"- Coverage: {es['corpus_coverage']}")
    if es["relevant_lessons"]:
        lines.append("- Lessons:")
        for l in es["relevant_lessons"]:
            lines.append(f"  - {l}")
    if es["relevant_beliefs"]:
        lines.append("- Beliefs:")
        for b in es["relevant_beliefs"]:
            lines.append(f"  - {b}")

    lines.append("")
    lines.append("## Action Memo")
    for item in d["action_memo"]:
        lines.append(f"{item['rank']}. **{item['action']}** — {item['owner']}")

    return "\n".join(lines)


def save_output(output: str, prefix: str) -> Path:
    WORKSPACE_DIR.mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_path = WORKSPACE_DIR / f"COUNCIL-{prefix}-{ts}.md"
    out_path.write_text(output)
    return out_path


def show_last() -> None:
    WORKSPACE_DIR.mkdir(exist_ok=True)
    files = sorted(WORKSPACE_DIR.glob("COUNCIL-*.md"), reverse=True)
    if not files:
        print("No council outputs found in workspace/")
        return
    print(files[0].read_text())


def list_roles() -> None:
    roles = sorted(p.stem for p in PERSONALITIES_DIR.glob("*.md"))
    print("Available council roles:")
    for r in roles:
        marker = " *" if r in DEFAULT_REPAIR_ROLES else ""
        print(f"  {r}{marker}")
    print(f"\n  (* = default repair council)")


def main() -> None:
    parser = argparse.ArgumentParser(description="Swarm Council — data-driven deliberation tool")
    parser.add_argument("--target", help="Problem/topic for repair deliberation (Mode R)")
    parser.add_argument("--roles", help="Comma-separated council roles")
    parser.add_argument("--domains", help="Comma-separated domains for Mode A deliberation")
    parser.add_argument("--question", help="Cross-domain question for Mode A")
    parser.add_argument("--axiom-audit", action="store_true",
                        help="Mode B: axiom sunset audit (L-1507)")
    parser.add_argument("--deference-ratio", action="store_true",
                        help="Measure human signal acceptance/rejection ratio (L-1507)")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--list-roles", action="store_true")
    parser.add_argument("--last", action="store_true")
    args = parser.parse_args()

    if args.list_roles:
        list_roles()
        return

    if args.last:
        show_last()
        return

    # Mode B: Axiom sunset audit
    if args.axiom_audit:
        result = axiom_sunset_audit()
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            output = render_axiom_audit(result)
            out_path = save_output(output, "AXIOM-SUNSET")
            print(output)
            print(f"\n[Saved to {out_path}]")
        return

    # Deference ratio
    if args.deference_ratio:
        result = compute_deference_ratio()
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            output = render_deference(result)
            out_path = save_output(output, "DEFERENCE")
            print(output)
            print(f"\n[Saved to {out_path}]")
        return

    # Mode A: Domain deliberation
    if args.domains:
        domains = [d.strip() for d in args.domains.split(",")]
        question = args.question or "What cross-domain patterns apply to swarm coordination?"
        result = domain_deliberate(domains, question)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            output = render_domain_memo(result)
            out_path = save_output(output, "DOMAIN")
            print(output)
            print(f"\n[Saved to {out_path}]")
        return

    # Mode R: Repair deliberation (default)
    target = args.target or "swarm general health"
    roles = [r.strip() for r in args.roles.split(",")] if args.roles else DEFAULT_REPAIR_ROLES
    result = repair_deliberate(target, roles)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        output = render_repair_memo(result)
        out_path = save_output(output, "REPAIR")
        print(output)
        print(f"\n[Saved to {out_path}]")


if __name__ == "__main__":
    main()
