#!/usr/bin/env python3
"""grounding_audit.py — Structural pressure toward groundedness (F-GND1, L-1192).

Computes per-claim grounding scores for beliefs and PHIL claims.
Claims auto-degrade without re-verification — analogous to compact.py for growth.

Grounding score = evidence_weight × recency_factor × independence_factor
- evidence_weight: external=1.0, measured/observed=0.7, theorized=0.3, unverified=0.0
- recency_factor: decays by 0.02/session since last tested (floor 0.2)
- independence_factor: 0.5 if only self-referential evidence, 1.0 if external

Usage:
  python3 tools/grounding_audit.py              # summary report
  python3 tools/grounding_audit.py --json        # machine-readable
  python3 tools/grounding_audit.py --detail      # per-claim breakdown

Related: L-1192, F-GND1, eval_sufficiency.py, knowledge_state.py
"""

import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent

# Evidence type weights (how close to external reality?)
EVIDENCE_WEIGHTS = {
    "external": 1.0,
    "grounded": 0.8,
    "observed": 0.7,
    "measured": 0.7,
    "partial": 0.5,
    "theorized": 0.3,
    "axiom": 0.3,       # definitional, not empirical
    "aspirational": 0.1,
    "conceptual": 0.1,
    "metaphor": 0.1,
    "unverified": 0.0,
}

# Decay rate per session since last tested
DECAY_RATE = 0.02
DECAY_FLOOR = 0.2
STALE_THRESHOLD = 50  # sessions without retest = stale


def _current_session() -> int:
    """Get current session number from INDEX.md."""
    try:
        text = (ROOT / "memory" / "INDEX.md").read_text(encoding="utf-8")
        m = re.search(r"Sessions:\s*(\d+)", text)
        return int(m.group(1)) if m else 475
    except Exception:
        return 475


def _parse_phil_claims() -> list[dict]:
    """Parse PHILOSOPHY.md claims table."""
    claims = []
    try:
        text = (ROOT / "beliefs" / "PHILOSOPHY.md").read_text(encoding="utf-8")
    except Exception:
        return claims

    # Find the claims table
    in_table = False
    for line in text.splitlines():
        if "| ID |" in line and "Grounding" in line:
            in_table = True
            continue
        if in_table and line.startswith("|---"):
            continue
        if in_table and line.startswith("|"):
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 7:
                claim_id = parts[1]
                claim_short = parts[2]
                claim_type = parts[3].lower()
                grounding = parts[4].lower()
                status = parts[5] if len(parts) > 5 else ""
                # Extract last-tested session from status column
                # Status contains patterns like "CONFIRMED S394", "S458 REFINED"
                sessions = [int(m) for m in re.findall(r'S(\d+)', status)]
                last_tested = max(sessions) if sessions else None
                claims.append({
                    "id": claim_id,
                    "short": claim_short,
                    "type": claim_type,
                    "grounding": grounding,
                    "status": status,
                    "last_tested_session": last_tested,
                    "source": "PHILOSOPHY.md",
                })
        elif in_table and not line.startswith("|"):
            break
    return claims


def _parse_deps_beliefs() -> list[dict]:
    """Parse DEPS.md beliefs with evidence types and last-tested dates."""
    beliefs = []
    try:
        text = (ROOT / "beliefs" / "DEPS.md").read_text(encoding="utf-8")
    except Exception:
        return beliefs

    current = None
    current_text = []
    for line in text.splitlines():
        # Detect belief headers like "### B1: ..." or "### B-EVAL1: ..."
        m = re.match(r"###\s+(B[-\w]+):\s+(.+)", line)
        if m:
            if current:
                current["full_text"] = "\n".join(current_text)
                beliefs.append(current)
            current = {
                "id": m.group(1),
                "short": m.group(2)[:80],
                "evidence_type": "observed",
                "last_tested_session": None,
                "source": "DEPS.md",
            }
            current_text = [line]
            continue

        if current:
            current_text.append(line)

            # Evidence type
            em = re.search(r"\*\*Evidence\*\*:\s*(\w+)", line)
            if em:
                current["evidence_type"] = em.group(1).lower()

            # Last tested
            tm = re.search(r"\*\*Last tested\*\*:\s*S(\d+)", line)
            if tm:
                current["last_tested_session"] = int(tm.group(1))

            # Falsified
            if "FALSIFIED" in line.upper() and "falsified if" not in line.lower():
                current["evidence_type"] = "falsified"

    if current:
        current["full_text"] = "\n".join(current_text)
        beliefs.append(current)
    return beliefs


def _compute_grounding_score(claim: dict, current_session: int) -> dict:
    """Compute grounding score for a single claim."""
    # Evidence weight
    grounding = claim.get("grounding", claim.get("evidence_type", "observed"))
    weight = EVIDENCE_WEIGHTS.get(grounding, 0.3)

    # Recency factor (decay since last test)
    # Axioms decay slower — they're definitional, not empirical
    claim_type = claim.get("type", "")
    decay_rate = DECAY_RATE * 0.5 if claim_type == "axiom" else DECAY_RATE
    last_tested = claim.get("last_tested_session")
    if last_tested is not None:
        sessions_since = current_session - last_tested
        recency = max(DECAY_FLOOR, 1.0 - (sessions_since * decay_rate))
        stale = sessions_since > STALE_THRESHOLD
    else:
        recency = DECAY_FLOOR  # never tested = maximum decay
        sessions_since = None
        stale = True

    # Independence factor — check for external evidence markers
    # Check both status field (PHIL claims) and full_text (DEPS beliefs)
    search_text = (claim.get("status", "") + " " + claim.get("full_text", "")).lower()
    has_external = any(kw in search_text for kw in [
        "external", "independent", "non-swarm", "benchmark",
        "arxiv", "jepsen", "peer", "replication", "osdi",
        "gilbert", "lynch", "yuan", "anderson", "kauffman",
    ])
    independence = 1.0 if has_external else 0.5

    score = weight * recency * independence

    result = {
        "id": claim["id"],
        "short": claim.get("short", "")[:60],
        "source": claim.get("source", "unknown"),
        "evidence_weight": round(weight, 2),
        "recency_factor": round(recency, 2),
        "independence_factor": round(independence, 2),
        "score": round(score, 3),
        "stale": stale,
    }
    if sessions_since is not None:
        result["sessions_since_test"] = sessions_since
    return result


def run_audit(detail: bool = False) -> dict:
    """Run the full grounding audit."""
    current_session = _current_session()
    phil_claims = _parse_phil_claims()
    deps_beliefs = _parse_deps_beliefs()

    results = []

    # Score PHIL claims (use grounding label, no last_tested for most)
    for claim in phil_claims:
        if "SUPERSEDED" in claim.get("status", ""):
            continue
        scored = _compute_grounding_score(claim, current_session)
        results.append(scored)

    # Score DEPS beliefs (have evidence type + last_tested)
    for belief in deps_beliefs:
        if belief.get("evidence_type") == "falsified":
            continue
        scored = _compute_grounding_score(belief, current_session)
        results.append(scored)

    results.sort(key=lambda x: x["score"])

    # Aggregate stats
    total = len(results)
    if total == 0:
        return {"error": "no claims found"}

    avg_score = sum(r["score"] for r in results) / total
    stale_count = sum(1 for r in results if r["stale"])
    well_grounded = sum(1 for r in results if r["score"] >= 0.4)
    poorly_grounded = sum(1 for r in results if r["score"] < 0.2)

    return {
        "session": f"S{current_session}",
        "total_claims": total,
        "avg_grounding_score": round(avg_score, 3),
        "well_grounded": well_grounded,
        "well_grounded_pct": round(well_grounded / total * 100, 1),
        "poorly_grounded": poorly_grounded,
        "poorly_grounded_pct": round(poorly_grounded / total * 100, 1),
        "stale": stale_count,
        "stale_pct": round(stale_count / total * 100, 1),
        "bottom_5": results[:5],
        "top_5": results[-5:],
        "all_claims": results if detail else None,
    }


def main():
    args = sys.argv[1:]
    detail = "--detail" in args
    as_json = "--json" in args

    audit = run_audit(detail=detail or as_json)

    if as_json:
        print(json.dumps(audit, indent=2))
        return

    print(f"=== GROUNDING AUDIT — {audit['session']} (F-GND1, L-1192) ===\n")
    print(f"  Claims assessed: {audit['total_claims']}")
    print(f"  Avg grounding score: {audit['avg_grounding_score']:.3f} (0=ungrounded, 1=fully grounded)")
    print(f"  Well-grounded (≥0.4): {audit['well_grounded']} ({audit['well_grounded_pct']}%)")
    print(f"  Poorly grounded (<0.2): {audit['poorly_grounded']} ({audit['poorly_grounded_pct']}%)")
    print(f"  Stale (>{STALE_THRESHOLD}s without retest): {audit['stale']} ({audit['stale_pct']}%)")

    print(f"\n--- Bottom 5 (least grounded — need attention) ---")
    for r in audit["bottom_5"]:
        stale_flag = " [STALE]" if r["stale"] else ""
        since = f" ({r['sessions_since_test']}s ago)" if "sessions_since_test" in r else " (never tested)"
        print(f"  {r['score']:.3f}  {r['id']}: {r['short']}{since}{stale_flag}")

    print(f"\n--- Top 5 (most grounded) ---")
    for r in audit["top_5"]:
        since = f" ({r['sessions_since_test']}s ago)" if "sessions_since_test" in r else ""
        print(f"  {r['score']:.3f}  {r['id']}: {r['short']}{since}")

    if detail and audit.get("all_claims"):
        print(f"\n--- All claims ---")
        for r in audit["all_claims"]:
            stale_flag = " [STALE]" if r["stale"] else ""
            since = f" ({r.get('sessions_since_test', '?')}s)" if "sessions_since_test" in r else ""
            print(f"  {r['score']:.3f}  {r['id']:<12} e={r['evidence_weight']:.1f} r={r['recency_factor']:.2f} i={r['independence_factor']:.1f}  {r['short'][:50]}{since}{stale_flag}")

    print(f"\n  Formula: score = evidence_weight × recency_factor × independence_factor")
    print(f"  Decay: {DECAY_RATE}/session, floor {DECAY_FLOOR}. Stale: >{STALE_THRESHOLD}s without retest.")
    print(f"  Evidence weights: external=1.0, grounded/observed=0.7, partial=0.5, theorized=0.3, aspirational=0.1")


if __name__ == "__main__":
    main()
