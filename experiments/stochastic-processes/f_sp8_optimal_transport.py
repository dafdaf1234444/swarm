#!/usr/bin/env python3
"""F-SP8 Optimal Transport Experiment (S519)

Measures Wasserstein-1 (W₁) distance between era-level topic distributions
to detect growth/consolidation phases in swarm evolution.

Eras: ~50-session windows. For each era, build domain frequency distribution.
W₁ between adjacent eras measures how much the topic landscape shifted.

Prediction (L-1401): W₁ trajectory is non-monotone (phases exist).
Falsified if: W₁ is monotone (steady drift or constant).
"""

import json
import os
import re
import sys
from collections import Counter

import numpy as np
from scipy.stats import wasserstein_distance, spearmanr

LESSONS_DIR = os.path.join(os.path.dirname(__file__), "../../memory/lessons")
OUTPUT_PATH = os.path.join(os.path.dirname(__file__),
                           "f-sp8-optimal-transport-s519.json")

# Known burst windows from F-SP3 (HMM Viterbi)
BURST_WINDOWS = [57, 186, 347]
ERA_SIZE = 50


def parse_lessons():
    """Extract (lesson_id, session, domains) from all lesson files."""
    records = []
    for fname in sorted(os.listdir(LESSONS_DIR)):
        if not fname.startswith("L-") or not fname.endswith(".md"):
            continue
        lid = fname.replace(".md", "")
        path = os.path.join(LESSONS_DIR, fname)
        with open(path, "r", errors="ignore") as fh:
            text = fh.read(2000)

        # Extract session number
        session = None
        m = re.search(r"[Ss]ession:?\s*S?(\d+)", text)
        if m:
            session = int(m.group(1))

        # Extract domain(s) — normalize
        domain_str = None
        dm = re.search(r"[Dd]omain:?\s*([^\n|]+)", text)
        if dm:
            domain_str = dm.group(1).strip().rstrip("|").strip()
        if not domain_str:
            tm = re.search(r"[Tt]heme:?\s*([^\n|]+)", text)
            if tm:
                domain_str = tm.group(1).strip().rstrip("|").strip()

        # Parse multi-domain entries ("meta, evaluation" → ["meta", "evaluation"])
        domains = []
        if domain_str:
            # Remove bold markers
            domain_str = domain_str.replace("**", "").strip()
            # Remove leading ": " artifacts
            domain_str = re.sub(r"^:\s*", "", domain_str)
            for d in re.split(r"[,;/]", domain_str):
                d = d.strip().lower()
                if d and len(d) < 40:
                    domains.append(d)

        if session is not None and domains:
            records.append((lid, session, domains))

    return records


def build_era_distributions(records, era_size=ERA_SIZE):
    """Group lessons into eras, build domain frequency distributions."""
    max_session = max(r[1] for r in records)
    era_starts = list(range(1, max_session + 1, era_size))
    eras = {}

    for start in era_starts:
        end = start + era_size - 1
        label = f"S{start}-S{end}"
        domain_counts = Counter()
        n_lessons = 0
        for lid, session, domains in records:
            if start <= session <= end:
                n_lessons += 1
                for d in domains:
                    domain_counts[d] += 1
        if n_lessons > 0:
            eras[label] = {
                "start": start,
                "end": end,
                "n_lessons": n_lessons,
                "domain_counts": dict(domain_counts),
            }

    return eras


def compute_w1_trajectory(eras):
    """Compute W₁ between adjacent era distributions.

    We represent each era as a probability distribution over all domains.
    W₁ is computed using scipy.stats.wasserstein_distance with:
    - values = domain indices (0, 1, 2, ...)
    - weights = normalized frequencies
    This treats domains as points on a line (ordered alphabetically).
    The metric is sensitive to how much probability mass must move.
    """
    # Build global domain vocabulary (sorted for consistency)
    all_domains = set()
    for era in eras.values():
        all_domains.update(era["domain_counts"].keys())
    vocab = sorted(all_domains)
    domain_idx = {d: i for i, d in enumerate(vocab)}

    era_labels = sorted(eras.keys(), key=lambda x: eras[x]["start"])
    w1_distances = []

    for i in range(len(era_labels) - 1):
        era_a = eras[era_labels[i]]
        era_b = eras[era_labels[i + 1]]

        # Build distribution vectors
        vals = np.arange(len(vocab), dtype=float)

        weights_a = np.array([era_a["domain_counts"].get(d, 0)
                              for d in vocab], dtype=float)
        weights_b = np.array([era_b["domain_counts"].get(d, 0)
                              for d in vocab], dtype=float)

        # Normalize to probability distributions
        if weights_a.sum() > 0:
            weights_a /= weights_a.sum()
        if weights_b.sum() > 0:
            weights_b /= weights_b.sum()

        w1 = wasserstein_distance(vals, vals, weights_a, weights_b)
        w1_distances.append({
            "era_pair": f"{era_labels[i]} → {era_labels[i+1]}",
            "w1": round(float(w1), 4),
            "n_a": era_a["n_lessons"],
            "n_b": era_b["n_lessons"],
        })

    return w1_distances, vocab


def check_monotonicity(w1_values):
    """Check if W₁ trajectory is monotone (increasing or decreasing)."""
    if len(w1_values) < 3:
        return "INSUFFICIENT_DATA"

    diffs = [w1_values[i + 1] - w1_values[i] for i in range(len(w1_values) - 1)]
    all_increasing = all(d >= 0 for d in diffs)
    all_decreasing = all(d <= 0 for d in diffs)

    if all_increasing:
        return "MONOTONE_INCREASING"
    elif all_decreasing:
        return "MONOTONE_DECREASING"
    else:
        # Count direction changes
        sign_changes = sum(
            1 for i in range(len(diffs) - 1)
            if diffs[i] * diffs[i + 1] < 0
        )
        return f"NON_MONOTONE ({sign_changes} direction changes in {len(diffs)} steps)"


def check_burst_correlation(w1_trajectory, eras):
    """Check if W₁ spikes correlate with known burst windows."""
    era_labels = sorted(eras.keys(), key=lambda x: eras[x]["start"])

    # For each burst window, find which era transition contains it
    burst_era_indices = []
    for burst_session in BURST_WINDOWS:
        for i, label in enumerate(era_labels):
            era = eras[label]
            if era["start"] <= burst_session <= era["end"]:
                # The transition INTO or OUT OF this era
                burst_era_indices.append(i)
                break

    w1_values = [t["w1"] for t in w1_trajectory]
    if not w1_values:
        return None

    median_w1 = float(np.median(w1_values))
    mean_w1 = float(np.mean(w1_values))

    # Check W₁ at burst-adjacent transitions
    burst_w1 = []
    for idx in burst_era_indices:
        # Check transition leaving this era (idx-1 to idx, or idx to idx+1)
        if idx > 0 and idx - 1 < len(w1_values):
            burst_w1.append(w1_values[idx - 1])
        if idx < len(w1_values):
            burst_w1.append(w1_values[idx])

    if not burst_w1:
        return {"detected": False, "reason": "no burst-adjacent transitions found"}

    burst_mean = float(np.mean(burst_w1))
    non_burst_w1 = [w for i, w in enumerate(w1_values)
                    if i not in burst_era_indices
                    and i - 1 not in burst_era_indices]
    non_burst_mean = float(np.mean(non_burst_w1)) if non_burst_w1 else mean_w1

    return {
        "burst_sessions": BURST_WINDOWS,
        "burst_era_indices": burst_era_indices,
        "burst_adjacent_w1_mean": round(burst_mean, 4),
        "non_burst_w1_mean": round(non_burst_mean, 4),
        "ratio": round(burst_mean / non_burst_mean, 3) if non_burst_mean > 0 else None,
        "detected": burst_mean > non_burst_mean * 1.2,
    }


def run_experiment():
    records = parse_lessons()
    print(f"Parsed {len(records)} lessons with session + domain info")

    eras = build_era_distributions(records)
    print(f"Built {len(eras)} era distributions (era_size={ERA_SIZE})")
    for label in sorted(eras.keys(), key=lambda x: eras[x]["start"]):
        era = eras[label]
        top3 = Counter(era["domain_counts"]).most_common(3)
        print(f"  {label}: {era['n_lessons']} lessons, "
              f"top domains: {top3}")

    w1_trajectory, vocab = compute_w1_trajectory(eras)
    print(f"\nW₁ trajectory ({len(w1_trajectory)} transitions):")
    w1_values = []
    for t in w1_trajectory:
        w1_values.append(t["w1"])
        print(f"  {t['era_pair']}: W₁ = {t['w1']:.4f}")

    monotonicity = check_monotonicity(w1_values)
    print(f"\nMonotonicity: {monotonicity}")

    burst_corr = check_burst_correlation(w1_trajectory, eras)
    print(f"Burst correlation: {burst_corr}")

    # Summary stats
    w1_arr = np.array(w1_values)
    summary = {
        "mean_w1": round(float(w1_arr.mean()), 4),
        "std_w1": round(float(w1_arr.std()), 4),
        "min_w1": round(float(w1_arr.min()), 4),
        "max_w1": round(float(w1_arr.max()), 4),
        "cv": round(float(w1_arr.std() / w1_arr.mean()), 4) if w1_arr.mean() > 0 else None,
        "range_ratio": round(float(w1_arr.max() / w1_arr.min()), 2) if w1_arr.min() > 0 else None,
    }

    # Trend test: Spearman correlation of W₁ vs time index
    if len(w1_values) >= 4:
        rho, p_val = spearmanr(range(len(w1_values)), w1_values)
        summary["spearman_rho"] = round(float(rho), 4)
        summary["spearman_p"] = round(float(p_val), 4)
        summary["trend"] = ("increasing" if rho > 0.3 else
                            "decreasing" if rho < -0.3 else "no_trend")

    # Verdict
    is_non_monotone = "NON_MONOTONE" in monotonicity
    prediction_confirmed = is_non_monotone

    verdict = {
        "prediction": "W₁ trajectory non-monotone (phases exist)",
        "result": "CONFIRMED" if prediction_confirmed else "FALSIFIED",
        "evidence": monotonicity,
        "interpretation": (
            "Topic distribution shifts vary across eras, confirming "
            "growth/consolidation phases in swarm evolution. "
            "The swarm is NOT a steady-state random walk."
            if prediction_confirmed else
            "Topic distribution shifts are monotone, suggesting "
            "steady drift rather than distinct phases."
        ),
    }

    # Build era distributions for output (convert to serializable)
    era_dists_out = {}
    for label in sorted(eras.keys(), key=lambda x: eras[x]["start"]):
        era = eras[label]
        total = sum(era["domain_counts"].values())
        era_dists_out[label] = {
            "n_lessons": era["n_lessons"],
            "n_domain_mentions": total,
            "top_5": dict(Counter(era["domain_counts"]).most_common(5)),
            "unique_domains": len(era["domain_counts"]),
        }

    result = {
        "experiment": "F-SP8-optimal-transport",
        "frontier": "F-SP8",
        "session": "S519",
        "domain": "stochastic-processes",
        "date": "2026-03-23",
        "context": (
            "L-1401 (S511) predicted W₁ trajectory non-monotone based on "
            "optimal transport substrate distance 0.8. This experiment "
            "computes W₁ between adjacent era topic distributions using "
            "real lesson data."
        ),
        "method": {
            "description": (
                "Parse all lessons for session number and domain tags. "
                "Group into 50-session eras. Build domain frequency "
                "distributions per era. Compute W₁ (Wasserstein-1) "
                "between adjacent era distributions using "
                "scipy.stats.wasserstein_distance. Domains ordered "
                "alphabetically; W₁ measures earth-mover distance "
                "on this 1D embedding."
            ),
            "era_size": ERA_SIZE,
            "n_lessons_parsed": len(records),
            "n_eras": len(eras),
            "domain_vocabulary_size": len(vocab),
        },
        "era_distributions": era_dists_out,
        "w1_trajectory": w1_trajectory,
        "summary_statistics": summary,
        "monotonicity_test": monotonicity,
        "burst_correlation": burst_corr,
        "verdict": verdict,
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\nResults written to {OUTPUT_PATH}")
    print(f"\nVERDICT: {verdict['result']} — {verdict['interpretation']}")

    return result


if __name__ == "__main__":
    run_experiment()
