#!/usr/bin/env python3
"""F-THERMO1 Phase Transition Analysis — S514
Measures Shannon entropy growth RATE across the swarm timeline
and tests for discontinuities (phase transitions).

Prediction: entropy growth rate has at least one discontinuity
aligned with known structural transitions (N≈550 integration bound).
Falsification: growth rate is smooth/linear — no phase transitions.
"""

import json, math, subprocess, sys
from collections import Counter
from pathlib import Path

# Session checkpoints with their commits and known lesson counts
CHECKPOINTS = [
    ("S50",  "e2d192de", 101),
    ("S100", "0b240cc6", 194),
    ("S150", "855d1017", 207),
    ("S199", "bf076259", 304),
    ("S300", "15bddb59", 304),
    ("S325", "a52fc7d6", 362),
    ("S350", "ca50b963", 477),
    ("S375", "3cf77159", 627),
    ("S400", "03a98da4", 764),
    ("S425", "8c459cf0", 867),
    ("S450", "cbeb80f1", 998),
    ("S475", "c5631bb4", 1079),
    ("S500", "c5f305e8", 1193),
    ("S510", "dc841375", 1154),
    ("S514", "754765f1", 1175),
]

def get_lesson_texts(commit: str) -> list[str]:
    """Extract all lesson file contents from a given commit."""
    try:
        files = subprocess.check_output(
            ["git", "ls-tree", "-r", "--name-only", commit, "--", "memory/lessons/"],
            text=True, stderr=subprocess.DEVNULL
        ).strip().split("\n")
    except subprocess.CalledProcessError:
        return []

    lesson_files = [f for f in files if f.startswith("memory/lessons/L-") and f.endswith(".md")]
    texts = []
    for lf in lesson_files:
        try:
            content = subprocess.check_output(
                ["git", "show", f"{commit}:{lf}"],
                text=True, stderr=subprocess.DEVNULL
            )
            texts.append(content)
        except subprocess.CalledProcessError:
            continue
    return texts


def word_entropy(texts: list[str]) -> dict:
    """Compute word-level Shannon entropy metrics."""
    all_words = []
    per_lesson_entropies = []

    for text in texts:
        words = text.lower().split()
        all_words.extend(words)
        if len(words) > 5:
            counts = Counter(words)
            total = len(words)
            h = -sum((c/total) * math.log2(c/total) for c in counts.values())
            per_lesson_entropies.append(h)

    # Corpus-level entropy
    corpus_counts = Counter(all_words)
    corpus_total = len(all_words)
    if corpus_total == 0:
        return {"corpus_entropy": 0, "per_lesson_mean": 0, "vocab_size": 0, "total_words": 0}

    corpus_h = -sum((c/corpus_total) * math.log2(c/corpus_total) for c in corpus_counts.values())
    per_lesson_mean = sum(per_lesson_entropies) / len(per_lesson_entropies) if per_lesson_entropies else 0
    per_lesson_sd = (sum((h - per_lesson_mean)**2 for h in per_lesson_entropies) / len(per_lesson_entropies))**0.5 if len(per_lesson_entropies) > 1 else 0

    return {
        "corpus_entropy": round(corpus_h, 4),
        "per_lesson_mean": round(per_lesson_mean, 4),
        "per_lesson_sd": round(per_lesson_sd, 4),
        "vocab_size": len(corpus_counts),
        "total_words": corpus_total,
        "n_lessons": len(texts),
        "vocab_ratio": round(len(corpus_counts) / corpus_total, 4) if corpus_total > 0 else 0,
    }


def compute_growth_rates(measurements: list[dict]) -> list[dict]:
    """Compute entropy growth rate between consecutive measurements."""
    rates = []
    for i in range(1, len(measurements)):
        prev = measurements[i-1]
        curr = measurements[i]
        session_delta = curr["session_num"] - prev["session_num"]
        if session_delta == 0:
            continue
        corpus_rate = (curr["corpus_entropy"] - prev["corpus_entropy"]) / session_delta
        per_lesson_rate = (curr["per_lesson_mean"] - prev["per_lesson_mean"]) / session_delta
        lesson_rate = (curr["n_lessons"] - prev["n_lessons"]) / session_delta
        rates.append({
            "interval": f"{prev['session']}→{curr['session']}",
            "session_midpoint": (prev["session_num"] + curr["session_num"]) / 2,
            "n_lessons_midpoint": (prev["n_lessons"] + curr["n_lessons"]) / 2,
            "corpus_entropy_rate": round(corpus_rate, 6),
            "per_lesson_entropy_rate": round(per_lesson_rate, 6),
            "lesson_production_rate": round(lesson_rate, 2),
            "vocab_ratio_delta": round(curr["vocab_ratio"] - prev["vocab_ratio"], 4),
        })
    return rates


def detect_regime_changes(rates: list[dict], key: str) -> list[dict]:
    """Detect points where growth rate changes sign or magnitude significantly."""
    changes = []
    values = [r[key] for r in rates]
    if len(values) < 3:
        return changes

    for i in range(1, len(values) - 1):
        # Sign change
        if values[i-1] * values[i] < 0:
            changes.append({
                "type": "sign_change",
                "at": rates[i]["interval"],
                "midpoint_session": rates[i]["session_midpoint"],
                "from": values[i-1],
                "to": values[i],
            })
        # Magnitude jump (>2x change)
        if abs(values[i-1]) > 0.000001:
            ratio = values[i] / values[i-1]
            if abs(ratio) > 2.0 or abs(ratio) < 0.5:
                changes.append({
                    "type": "magnitude_jump",
                    "at": rates[i]["interval"],
                    "midpoint_session": rates[i]["session_midpoint"],
                    "ratio": round(ratio, 2),
                    "from": values[i-1],
                    "to": values[i],
                })
    return changes


def linear_fit(xs, ys):
    """Simple least-squares linear regression."""
    n = len(xs)
    if n < 2:
        return 0, 0, 0
    x_mean = sum(xs) / n
    y_mean = sum(ys) / n
    ss_xy = sum((x - x_mean) * (y - y_mean) for x, y in zip(xs, ys))
    ss_xx = sum((x - x_mean)**2 for x in xs)
    ss_yy = sum((y - y_mean)**2 for y in ys)
    slope = ss_xy / ss_xx if ss_xx > 0 else 0
    r_sq = (ss_xy**2 / (ss_xx * ss_yy)) if ss_xx > 0 and ss_yy > 0 else 0
    intercept = y_mean - slope * x_mean
    return slope, intercept, r_sq


def piecewise_fit(sessions, values, breakpoint):
    """Fit two separate linear segments at a breakpoint and compare to single fit."""
    # Single fit
    _, _, r2_single = linear_fit(sessions, values)

    # Two-segment fit
    seg1_x = [s for s in sessions if s <= breakpoint]
    seg1_y = [v for s, v in zip(sessions, values) if s <= breakpoint]
    seg2_x = [s for s in sessions if s > breakpoint]
    seg2_y = [v for s, v in zip(sessions, values) if s > breakpoint]

    if len(seg1_x) < 2 or len(seg2_x) < 2:
        return None

    slope1, _, r2_1 = linear_fit(seg1_x, seg1_y)
    slope2, _, r2_2 = linear_fit(seg2_x, seg2_y)

    # Weighted average R² for piecewise
    n1, n2 = len(seg1_x), len(seg2_x)
    r2_piecewise = (r2_1 * n1 + r2_2 * n2) / (n1 + n2)

    return {
        "breakpoint": breakpoint,
        "r2_single": round(r2_single, 4),
        "r2_piecewise": round(r2_piecewise, 4),
        "improvement": round(r2_piecewise - r2_single, 4),
        "slope_before": round(slope1, 6),
        "slope_after": round(slope2, 6),
        "slope_ratio": round(slope2 / slope1, 3) if abs(slope1) > 1e-8 else None,
    }


def main():
    measurements = []
    print("Measuring entropy at each checkpoint...")

    for session, commit, expected_n in CHECKPOINTS:
        session_num = int(session[1:])
        print(f"  {session} ({commit[:8]})...", end=" ", flush=True)
        texts = get_lesson_texts(commit)
        m = word_entropy(texts)
        m["session"] = session
        m["session_num"] = session_num
        m["commit"] = commit[:8]
        measurements.append(m)
        print(f"{m['n_lessons']}L, H={m['corpus_entropy']:.4f}, h={m['per_lesson_mean']:.4f}")

    # Compute growth rates
    rates = compute_growth_rates(measurements)

    # Detect regime changes in corpus entropy rate
    corpus_changes = detect_regime_changes(rates, "corpus_entropy_rate")
    per_lesson_changes = detect_regime_changes(rates, "per_lesson_entropy_rate")
    production_changes = detect_regime_changes(rates, "lesson_production_rate")

    # Test piecewise fit at known structural transition points
    sessions = [m["session_num"] for m in measurements]
    corpus_vals = [m["corpus_entropy"] for m in measurements]
    per_lesson_vals = [m["per_lesson_mean"] for m in measurements]

    piecewise_results = {}
    for bp_name, bp in [("N550_integration", 400), ("N750_waypoint", 450), ("S300_era", 300)]:
        pw = piecewise_fit(sessions, corpus_vals, bp)
        if pw:
            piecewise_results[bp_name] = pw

    # Lesson production rate piecewise
    lesson_counts = [m["n_lessons"] for m in measurements]
    production_piecewise = {}
    for bp_name, bp in [("N550_integration", 400), ("S300_era", 300)]:
        pw = piecewise_fit(sessions, lesson_counts, bp)
        if pw:
            production_piecewise[bp_name] = pw

    # Build results
    results = {
        "experiment": "DOMEX-THERMO-S514",
        "frontier": "F-THERMO1",
        "session": "S514",
        "domain": "thermodynamics",
        "date": "2026-03-23",
        "expect": "Entropy growth rate has at least one discontinuity aligned with known structural transitions (N≈550 integration bound). Piecewise fit R² improvement >0.05 over single linear fit.",
        "measurements": measurements,
        "growth_rates": rates,
        "regime_changes": {
            "corpus_entropy": corpus_changes,
            "per_lesson_entropy": per_lesson_changes,
            "lesson_production": production_changes,
        },
        "piecewise_fits": {
            "corpus_entropy": piecewise_results,
            "lesson_count": production_piecewise,
        },
    }

    # Compute verdict
    any_significant_break = False
    best_improvement = 0
    best_bp = None
    for name, pw in piecewise_results.items():
        if pw["improvement"] > best_improvement:
            best_improvement = pw["improvement"]
            best_bp = name
        if pw["improvement"] > 0.05:
            any_significant_break = True

    n_regime_changes = len(corpus_changes) + len(per_lesson_changes)
    production_regime = len(production_changes)

    if any_significant_break:
        verdict = f"CONFIRMED: Phase transition detected. Best breakpoint: {best_bp} (R² improvement: {best_improvement:.4f})"
    elif best_improvement > 0.02:
        verdict = f"PARTIAL: Weak phase transition at {best_bp} (R² improvement: {best_improvement:.4f}, below 0.05 threshold)"
    else:
        verdict = f"FALSIFIED: No significant phase transitions in entropy. Best R² improvement: {best_improvement:.4f}. Growth is smooth."

    results["verdict"] = verdict
    results["diff"] = f"Regime changes detected: {n_regime_changes} in entropy, {production_regime} in production. Best piecewise improvement: {best_improvement:.4f} at {best_bp}. Slope ratio at best break: {piecewise_results.get(best_bp, {}).get('slope_ratio', 'N/A')}"

    # Save
    outpath = Path("experiments/thermodynamics/phase-transition-s514.json")
    outpath.parent.mkdir(parents=True, exist_ok=True)
    with open(outpath, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved: {outpath}")
    print(f"\nVerdict: {verdict}")
    print(f"Diff: {results['diff']}")

    return results


if __name__ == "__main__":
    main()
