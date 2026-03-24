#!/usr/bin/env python3
"""F-EPIS3: Grounding-survival correlation — does evidence quality predict claim fate?

If the confirmation attractor is real, poorly grounded claims survive challenges
just as well as well-grounded ones. If healthy, grounding predicts outcomes.

Pre-registered predictions:
  H1: Grounding score does NOT correlate with challenge probability (|r| < 0.2)
  H2: Grounding score does NOT correlate with survival (challenged but not dropped)
  H3: Claim AGE predicts challenge probability better than grounding (|r_age| > |r_ground|)

Method:
  1. Extract all PHIL/DEPS claims with grounding scores from grounding_audit.py (detail=True)
  2. Parse PHILOSOPHY.md for challenge history (challenged, revised, dropped, confirmed)
  3. Compute Spearman correlations: grounding vs challenge_probability, grounding vs survival
  4. Compare age vs grounding as predictors

Cites: L-1581, L-1580, L-1571
"""

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO / "tools"))


def get_grounding_scores():
    """Get ALL claim grounding scores using detail=True."""
    import grounding_audit
    data = grounding_audit.run_audit(detail=True)
    all_claims = {}
    if data.get("all_claims"):
        for c in data["all_claims"]:
            all_claims[c["id"]] = c
    else:
        for group in ["bottom_5", "top_5"]:
            for c in data.get(group, []):
                all_claims[c["id"]] = c
    return all_claims, data


def parse_challenge_history():
    """Parse PHILOSOPHY.md tracker table for challenge outcomes."""
    phil_path = REPO / "beliefs" / "PHILOSOPHY.md"
    text = phil_path.read_text()
    claims = {}
    row_pattern = re.compile(r"\|\s*(PHIL-\d+|B-[A-Z]+\d*)\s*\|(.+)")

    for m in row_pattern.finditer(text):
        claim_id = m.group(1)
        full_row = m.group(2)
        if "Claim (short)" in full_row or "---" in full_row:
            continue

        challenged = bool(re.search(
            r"CHALLENG|FALSIF|REVISED|MECHANISM.REVISED|PARTIALLY.FALSIF|FIRST.CHALLENGE|DOWNGRADED",
            full_row, re.I
        ))
        dropped = bool(re.search(r"DROPPED|SUPERSEDED", full_row, re.I))
        revised = bool(re.search(
            r"REVISED|MECHANISM.REVISED|REFINED|RENAMED|REFRAMED|NARROWED|DOWNGRADED",
            full_row, re.I
        ))
        confirmed = bool(re.search(r"CONFIRMED", full_row, re.I))
        challenge_sessions = re.findall(r"S(\d+)", full_row)

        claims[claim_id] = {
            "id": claim_id,
            "challenged": challenged,
            "dropped": dropped,
            "revised": revised,
            "confirmed": confirmed,
            "n_challenge_sessions": len(set(challenge_sessions)),
        }
    return claims


def parse_claim_ages():
    """Estimate claim ages from session references in PHILOSOPHY.md tracker."""
    phil_path = REPO / "beliefs" / "PHILOSOPHY.md"
    text = phil_path.read_text()
    ages = {}
    current_session = 541
    row_pattern = re.compile(r"\|\s*(PHIL-\d+|B-[A-Z]+\d*)\s*\|(.+)")

    for m in row_pattern.finditer(text):
        claim_id = m.group(1)
        full_row = m.group(2)
        if "Claim (short)" in full_row:
            continue
        sessions = [int(s) for s in re.findall(r"S(\d+)", full_row)]
        ages[claim_id] = current_session - min(sessions) if sessions else current_session
    return ages


def spearman(x, y):
    """Compute Spearman rank correlation without scipy."""
    n = len(x)
    if n < 3:
        return 0.0, n

    def rank(vals):
        sorted_idx = sorted(range(n), key=lambda i: vals[i])
        ranks = [0.0] * n
        i = 0
        while i < n:
            j = i
            while j < n - 1 and vals[sorted_idx[j]] == vals[sorted_idx[j + 1]]:
                j += 1
            avg_rank = (i + j) / 2.0 + 1
            for k in range(i, j + 1):
                ranks[sorted_idx[k]] = avg_rank
            i = j + 1
        return ranks

    rx, ry = rank(x), rank(y)
    d_sq = sum((rx[i] - ry[i]) ** 2 for i in range(n))
    rho = 1 - 6 * d_sq / (n * (n * n - 1))
    return round(rho, 3), n


def main():
    print("=" * 60)
    print("  F-EPIS3: GROUNDING-SURVIVAL CORRELATION — S541")
    print("=" * 60)

    # 1. Get ALL grounding scores
    grounding_claims, grounding_data = get_grounding_scores()
    print(f"\n--- Grounding data ---")
    print(f"  Total claims from audit: {grounding_data['total_claims']}")
    print(f"  Claims with individual scores: {len(grounding_claims)}")
    print(f"  Avg grounding: {grounding_data['avg_grounding_score']:.3f}")

    # 2. Parse challenge history
    challenge_data = parse_challenge_history()
    challenged_list = [c for c in challenge_data.values() if c["challenged"]]
    dropped_list = [c for c in challenge_data.values() if c["dropped"]]
    revised_list = [c for c in challenge_data.values() if c["revised"]]
    print(f"\n--- Challenge history ---")
    print(f"  Claims in tracker: {len(challenge_data)}")
    print(f"  Challenged: {len(challenged_list)}")
    print(f"  Dropped: {len(dropped_list)}")
    print(f"  Revised: {len(revised_list)}")

    # 3. Ages
    ages = parse_claim_ages()

    # 4. Merge — only include claims with REAL grounding scores
    merged_full = []
    merged_scored = []  # Only claims with actual grounding scores
    for cid, cdata in challenge_data.items():
        entry = {
            "id": cid,
            "grounding_score": grounding_claims.get(cid, {}).get("score"),
            "age_sessions": ages.get(cid, 0),
            "challenged": 1 if cdata["challenged"] else 0,
            "dropped": 1 if cdata["dropped"] else 0,
            "survived": 1 if (cdata["challenged"] and not cdata["dropped"]) else 0,
            "n_challenges": cdata["n_challenge_sessions"],
        }
        merged_full.append(entry)
        if entry["grounding_score"] is not None:
            merged_scored.append(entry)

    print(f"\n--- Merged dataset ---")
    print(f"  With grounding scores: {len(merged_scored)}")
    print(f"  Without scores (excluded from correlation): {len(merged_full) - len(merged_scored)}")

    # 5. Correlations on scored subset
    if len(merged_scored) >= 5:
        print(f"\n--- H1: Grounding vs challenge probability (n={len(merged_scored)}) ---")
        gs = [m["grounding_score"] for m in merged_scored]
        ch = [m["challenged"] for m in merged_scored]
        rho_gc, n_gc = spearman(gs, ch)
        print(f"  Spearman rho(grounding, challenged): {rho_gc}")
        h1_result = "CONFIRMED" if abs(rho_gc) < 0.2 else "FALSIFIED"
        print(f"  Prediction |r| < 0.2: {h1_result}")

        scored_challenged = [m for m in merged_scored if m["challenged"]]
        if len(scored_challenged) >= 3:
            gs_c = [m["grounding_score"] for m in scored_challenged]
            sv_c = [1 - m["dropped"] for m in scored_challenged]
            rho_gs, n_gs = spearman(gs_c, sv_c)
            h2_result = "CONFIRMED" if abs(rho_gs) < 0.2 else "FALSIFIED"
        else:
            rho_gs, n_gs, h2_result = None, len(scored_challenged), "INSUFFICIENT DATA"
        print(f"\n--- H2: Grounding vs survival (n={n_gs}) ---")
        print(f"  Spearman rho: {rho_gs}")
        print(f"  Prediction |r| < 0.2: {h2_result}")

        ag = [m["age_sessions"] for m in merged_scored]
        rho_ac, n_ac = spearman(ag, ch)
        age_beats = abs(rho_ac) > abs(rho_gc)
        h3_result = "CONFIRMED" if age_beats else "FALSIFIED"
        print(f"\n--- H3: Age vs challenge (n={n_ac}) ---")
        print(f"  Spearman rho(age, challenged): {rho_ac}")
        print(f"  |r_age|={abs(rho_ac):.3f} vs |r_ground|={abs(rho_gc):.3f}: {h3_result}")
    else:
        rho_gc = rho_gs = rho_ac = None
        n_gc = n_gs = n_ac = len(merged_scored)
        h1_result = h2_result = h3_result = "INSUFFICIENT DATA"
        age_beats = None
        print(f"\n  INSUFFICIENT SCORED CLAIMS ({len(merged_scored)}) — need ≥5 for correlation")

    # 6. Full-dataset analysis using ages only (available for all claims)
    print(f"\n--- Full-dataset age analysis (n={len(merged_full)}) ---")
    ag_all = [m["age_sessions"] for m in merged_full]
    ch_all = [m["challenged"] for m in merged_full]
    rho_age_full, n_age_full = spearman(ag_all, ch_all)
    print(f"  Spearman rho(age, challenged): {rho_age_full} (n={n_age_full})")

    nc_all = [m["n_challenges"] for m in merged_full]
    rho_age_nc, _ = spearman(ag_all, nc_all)
    print(f"  Spearman rho(age, n_challenges): {rho_age_nc}")

    # 7. Data quality assessment
    coverage = len(merged_scored) / len(merged_full) * 100 if merged_full else 0
    print(f"\n--- Data quality ---")
    print(f"  Grounding score coverage: {len(merged_scored)}/{len(merged_full)} ({coverage:.0f}%)")
    if coverage < 50:
        print(f"  ⚠ LOW COVERAGE: grounding_audit returns only extreme claims.")
        print(f"    Correlation on {len(merged_scored)} claims may not generalize to full set.")
        print(f"    → LESSON CANDIDATE: grounding audit's extreme-only output")
        print(f"      prevents full-distribution analysis of attractor behavior.")

    # 8. Tabulate
    print(f"\n--- Claim data (scored only) ---")
    sorted_scored = sorted(merged_scored, key=lambda m: m["grounding_score"])
    print(f"  {'ID':<12} {'Ground':>7} {'Age':>5} {'Chal':>5} {'Drop':>5} {'#Ch':>4}")
    for m in sorted_scored:
        print(f"  {m['id']:<12} {m['grounding_score']:>7.3f} {m['age_sessions']:>5} "
              f"{'YES' if m['challenged'] else '-':>5} {'YES' if m['dropped'] else '-':>5} "
              f"{m['n_challenges']:>4}")

    # 9. Summary
    print(f"\n{'=' * 60}")
    print(f"  SUMMARY")
    print(f"{'=' * 60}")
    print(f"  H1 (grounding ≠ challenge predictor): {h1_result} (r={rho_gc})")
    print(f"  H2 (grounding ≠ survival predictor):  {h2_result} (r={rho_gs})")
    print(f"  H3 (age > grounding as predictor):    {h3_result}")
    print(f"  Data coverage: {coverage:.0f}% ({len(merged_scored)}/{len(merged_full)} claims scored)")

    # 10. Save experiment
    experiment = {
        "id": "f-epis3-grounding-survival-s541",
        "session": "S541",
        "domain": "epistemology",
        "frontier": "F-EPIS3",
        "hypothesis": "Confirmation attractor prevents grounding quality from predicting challenge probability or survival",
        "method": "Spearman correlation on claims with grounding scores from grounding_audit.py (detail=True). Compare age as alternative predictor.",
        "predictions": {
            "H1_grounding_challenge_abs_r_lt_0.2": True,
            "H2_grounding_survival_abs_r_lt_0.2": True,
            "H3_age_beats_grounding": True,
        },
        "results": {
            "H1": {"rho": rho_gc, "n": n_gc, "result": h1_result},
            "H2": {"rho": rho_gs, "n": n_gs, "result": h2_result},
            "H3": {"rho_age": rho_ac, "rho_ground": rho_gc, "age_beats": age_beats, "result": h3_result},
            "age_full_dataset": {"rho": rho_age_full, "n": n_age_full},
            "age_intensity_full": {"rho": rho_age_nc},
        },
        "data_quality": {
            "scored_claims": len(merged_scored),
            "total_claims": len(merged_full),
            "coverage_pct": round(coverage, 1),
            "low_coverage_warning": coverage < 50,
        },
        "claims": sorted(merged_full, key=lambda m: m.get("grounding_score") or 0),
        "cites": ["L-1581", "L-1580", "L-1571"],
        "lesson_candidate": True,
    }

    out_path = REPO / "experiments" / "epistemology" / "f-epis3-grounding-survival-s541.json"
    with open(out_path, "w") as f:
        json.dump(experiment, f, indent=2, default=str)
    print(f"\n  Saved: {out_path.relative_to(REPO)}")


if __name__ == "__main__":
    main()
