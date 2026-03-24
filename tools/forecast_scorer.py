#!/usr/bin/env python3
"""Forecast scorer — computes Brier scores, calibration curves, and bias analysis.

Loads prediction data from experiment JSONs in experiments/forecasting/,
scores resolved + in-progress predictions, and outputs calibration diagnostics.

Usage:
    python3 tools/forecast_scorer.py              # full report
    python3 tools/forecast_scorer.py --json       # machine-readable output
    python3 tools/forecast_scorer.py --update     # refresh with latest prices (manual)
"""
import json, glob, os, sys, math
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent
EXPERIMENT_DIR = ROOT / "experiments" / "forecasting"


def load_latest_scoring():
    """Load the most recent f-fore1-scoring experiment JSON with structured predictions."""
    candidates = sorted(
        list(EXPERIMENT_DIR.glob("f-fore1-scoring-s*.json"))
        + list(EXPERIMENT_DIR.glob("f-fore1-full-scoring-s*.json")),
        key=lambda p: p.stat().st_mtime,
    )
    if not candidates:
        print("ERROR: No scoring experiment JSONs found in experiments/forecasting/")
        sys.exit(1)
    # Walk backwards to find the latest with structured actual.predictions_scored
    for candidate in reversed(candidates):
        with open(candidate) as f:
            data = json.load(f)
        actual = data.get("actual", {})
        if isinstance(actual, dict) and "predictions_scored" in actual:
            return data, candidate.name
    # Fallback: return the latest anyway (will fail gracefully downstream)
    latest = candidates[-1]
    with open(latest) as f:
        return json.load(f), latest.name


def extract_predictions(data):
    """Extract prediction records from experiment JSON."""
    preds = []
    scored = data.get("actual", {}).get("predictions_scored", {})
    for pred_id, info in scored.items():
        pred = {
            "id": pred_id,
            "confidence": info.get("conf", 0.5),
            "status": info.get("status", "UNKNOWN"),
            "pct_move": info.get("pct", 0.0),
        }
        # Determine directional correctness
        status = info.get("status", "").upper()
        if status in ("ON_TRACK", "ON_TARGET", "WITH"):
            pred["correct_direction"] = True
        elif status in ("AGAINST", "STRONGLY_AGAINST", "NEAR_CERTAIN_INCORRECT"):
            pred["correct_direction"] = False
        elif status in ("EARLY", "WEAKENING"):
            pred["correct_direction"] = None  # indeterminate
        else:
            pred["correct_direction"] = None

        # Classify prediction type
        name = pred_id.upper()
        if "BEAR" in name:
            pred["type"] = "bear"
        elif "BULL" in name:
            pred["type"] = "bull"
        elif "NEUTRAL" in name:
            pred["type"] = "neutral"
        elif "VS" in name:
            pred["type"] = "relative"
        else:
            pred["type"] = "other"

        # Extract target range
        target = info.get("target", "")
        pred["target"] = target

        preds.append(pred)
    return preds


def compute_brier_scores(preds):
    """Compute Brier scores for predictions with known outcomes.

    Brier score = (forecast_probability - outcome)^2
    For directional predictions: outcome=1 if correct direction, 0 if not.
    Confidence = P(prediction is correct).
    """
    scored = []
    for p in preds:
        if p["correct_direction"] is None:
            continue
        outcome = 1.0 if p["correct_direction"] else 0.0
        conf = p["confidence"]
        brier = (conf - outcome) ** 2
        scored.append({
            "id": p["id"],
            "confidence": conf,
            "outcome": outcome,
            "brier": round(brier, 4),
            "type": p["type"],
        })
    return scored


def calibration_curve(scored, n_bins=5):
    """Compute calibration curve — binned predicted vs actual frequencies."""
    if not scored:
        return []
    bins = defaultdict(lambda: {"total": 0, "correct": 0, "sum_conf": 0.0})
    for s in scored:
        bin_idx = min(int(s["confidence"] * n_bins), n_bins - 1)
        bins[bin_idx]["total"] += 1
        bins[bin_idx]["correct"] += s["outcome"]
        bins[bin_idx]["sum_conf"] += s["confidence"]

    curve = []
    for i in range(n_bins):
        b = bins[i]
        if b["total"] == 0:
            continue
        curve.append({
            "bin": f"{i/n_bins:.1f}-{(i+1)/n_bins:.1f}",
            "n": b["total"],
            "mean_confidence": round(b["sum_conf"] / b["total"], 3),
            "actual_frequency": round(b["correct"] / b["total"], 3),
            "gap": round(b["sum_conf"] / b["total"] - b["correct"] / b["total"], 3),
        })
    return curve


def bias_analysis(scored):
    """Analyze systematic biases by prediction type."""
    by_type = defaultdict(list)
    for s in scored:
        by_type[s["type"]].append(s)

    analysis = {}
    for ptype, items in by_type.items():
        n = len(items)
        mean_conf = sum(i["confidence"] for i in items) / n
        mean_outcome = sum(i["outcome"] for i in items) / n
        mean_brier = sum(i["brier"] for i in items) / n
        overconfidence = mean_conf - mean_outcome  # positive = overconfident
        analysis[ptype] = {
            "n": n,
            "mean_confidence": round(mean_conf, 3),
            "accuracy": round(mean_outcome, 3),
            "mean_brier": round(mean_brier, 4),
            "overconfidence": round(overconfidence, 3),
            "verdict": "overconfident" if overconfidence > 0.1 else
                       "underconfident" if overconfidence < -0.1 else "calibrated",
        }
    return analysis


def bootstrap_brier(scored, n_boot=1000):
    """Bootstrap 95% CI for mean Brier score."""
    import random
    if not scored:
        return None, None
    briers = [s["brier"] for s in scored]
    n = len(briers)
    means = []
    for _ in range(n_boot):
        sample = [random.choice(briers) for _ in range(n)]
        means.append(sum(sample) / n)
    means.sort()
    lo = means[int(0.025 * n_boot)]
    hi = means[int(0.975 * n_boot)]
    return round(lo, 4), round(hi, 4)


def main():
    json_mode = "--json" in sys.argv

    data, source_file = load_latest_scoring()
    preds = extract_predictions(data)
    scored = compute_brier_scores(preds)

    # Overall metrics
    n_total = len(preds)
    n_scored = len(scored)
    n_correct = sum(1 for s in scored if s["outcome"] == 1.0)
    n_incorrect = n_scored - n_correct
    mean_brier = sum(s["brier"] for s in scored) / n_scored if scored else None
    ci_lo, ci_hi = bootstrap_brier(scored)

    # Calibration curve
    curve = calibration_curve(scored)

    # Bias analysis
    bias = bias_analysis(scored)

    # Evidence-immunization check (L-1504): predictions with conf < 0.15
    immunized = [p for p in preds if p["confidence"] < 0.15]

    # Best/worst predictions by Brier
    if scored:
        best = min(scored, key=lambda s: s["brier"])
        worst = max(scored, key=lambda s: s["brier"])
    else:
        best = worst = None

    result = {
        "source": source_file,
        "n_predictions": n_total,
        "n_scored": n_scored,
        "n_correct": n_correct,
        "n_incorrect": n_incorrect,
        "directional_accuracy": round(n_correct / n_scored, 3) if n_scored else None,
        "mean_brier": round(mean_brier, 4) if mean_brier is not None else None,
        "brier_ci_95": [ci_lo, ci_hi] if ci_lo is not None else None,
        "calibration_verdict": (
            "good" if mean_brier and mean_brier < 0.25 else
            "baseline" if mean_brier and mean_brier < 0.35 else
            "poor" if mean_brier else "insufficient_data"
        ),
        "calibration_curve": curve,
        "bias_by_type": bias,
        "evidence_immunized": len(immunized),
        "best_prediction": best,
        "worst_prediction": worst,
    }

    if json_mode:
        print(json.dumps(result, indent=2))
        return

    # Human-readable report
    print(f"\n=== FORECAST SCORER — F-FORE1 Calibration Report ===")
    print(f"Source: {source_file}")
    print(f"Predictions: {n_total} total, {n_scored} scored, {n_total - n_scored} indeterminate")
    print(f"Directional accuracy: {n_correct}/{n_scored} ({result['directional_accuracy']:.1%})" if n_scored else "")
    print(f"\nMean Brier score: {mean_brier:.4f}" if mean_brier else "\nMean Brier: insufficient data")
    if ci_lo is not None:
        print(f"  95% CI: [{ci_lo:.4f}, {ci_hi:.4f}]")
    print(f"  Verdict: {result['calibration_verdict'].upper()}")

    # F-FORE1 comparison
    if mean_brier:
        if mean_brier < 0.25:
            print(f"  → PASSES F-FORE1 criterion (Brier < 0.25 = expert-level)")
        elif mean_brier < 0.35:
            print(f"  → WITHIN F-FORE1 prediction range (0.20-0.30)")
        else:
            print(f"  → FAILS F-FORE1 falsification threshold (Brier > 0.35)")

    if immunized:
        print(f"\n⚠ Evidence-immunized: {len(immunized)} prediction(s) with conf < 0.15")
        for p in immunized:
            print(f"  {p['id']}: conf={p['confidence']}")

    print(f"\n--- Calibration Curve ---")
    print(f"{'Bin':>10} {'N':>4} {'Mean Conf':>10} {'Actual Freq':>12} {'Gap':>8}")
    for row in curve:
        gap_str = f"{row['gap']:+.3f}"
        print(f"{row['bin']:>10} {row['n']:>4} {row['mean_confidence']:>10.3f} {row['actual_frequency']:>12.3f} {gap_str:>8}")

    print(f"\n--- Bias Analysis by Prediction Type ---")
    for ptype, stats in sorted(bias.items()):
        print(f"  {ptype:>10}: n={stats['n']}, conf={stats['mean_confidence']:.2f}, "
              f"acc={stats['accuracy']:.2f}, Brier={stats['mean_brier']:.3f}, "
              f"overconf={stats['overconfidence']:+.3f} [{stats['verdict']}]")

    if best:
        print(f"\n  Best:  {best['id']} (Brier={best['brier']:.4f})")
    if worst:
        print(f"  Worst: {worst['id']} (Brier={worst['brier']:.4f})")

    # Self-calibration check (self-apply)
    print(f"\n--- Self-Calibration Check ---")
    if mean_brier:
        predicted_range = (0.20, 0.30)  # F-FORE1 prediction
        in_range = predicted_range[0] <= mean_brier <= predicted_range[1]
        print(f"  F-FORE1 predicted Brier: 0.20-0.30")
        print(f"  Actual mean Brier: {mean_brier:.4f}")
        print(f"  Meta-prediction: {'CONFIRMED' if in_range else 'OUTSIDE RANGE'}")


if __name__ == "__main__":
    main()
