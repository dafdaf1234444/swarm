#!/usr/bin/env python3
"""Rate-distortion analysis for knowledge systems.

Derives optimal compression strategies from information-theoretic bounds.
Works on ANY collection of items with sizes and utility scores.

Internal use: analyze swarm lesson corpus compaction.
External use: analyze any knowledge/document/record collection.

Mathematical foundation:
  - Compaction optimality: fractional knapsack (Dantzig 1957)
  - R(D) power law: D(α) = A·α^β where β depends on utility distribution
  - Information bottleneck: F_max = max{F : T_W(F) ≤ W} (Tishby 1999)

References: L-XXXX (rate-distortion theorem), Shannon (1959), Dantzig (1957)
"""

import argparse
import json
import math
import sys
from pathlib import Path


def load_swarm_data():
    """Load swarm lesson and citation data."""
    root = Path(__file__).parent.parent
    lesson_cache = root / "experiments" / "compact-lesson-cache.json"
    citation_cache = root / "experiments" / "compact-citation-cache.json"

    with open(lesson_cache) as f:
        lessons = json.load(f)
    with open(citation_cache) as f:
        citations = json.load(f)

    # Count incoming citations per lesson
    from collections import Counter
    cited_by = Counter()
    for _path, data in citations.items():
        if isinstance(data, dict) and "cites" in data:
            for lid, count in data["cites"].items():
                cited_by[lid] += count

    items = []
    for lid, ldata in lessons.items():
        if isinstance(ldata, dict) and "tokens" in ldata:
            t = ldata["tokens"]
            c = cited_by.get(lid, 0)
            items.append({"id": lid, "size": t, "utility": c})

    return items


def load_external_data(path):
    """Load external JSON data: list of {id, size, utility}."""
    with open(path) as f:
        return json.load(f)


def compute_rd_curve(items, n_points=20):
    """Compute the optimal rate-distortion curve.

    Returns list of (compression_ratio, distortion) points.
    Optimal strategy: remove items in ascending order of utility/size.
    """
    total_size = sum(it["size"] for it in items)
    total_utility = sum(it["utility"] for it in items)
    if total_size == 0 or total_utility == 0:
        return []

    # Sort by utility density ascending (remove worst first)
    sorted_items = sorted(items, key=lambda x: x["utility"] / x["size"] if x["size"] > 0 else 0)

    points = []
    cum_size = 0
    cum_util = 0
    N = len(sorted_items)
    step = max(1, N // n_points)

    for i, it in enumerate(sorted_items):
        cum_size += it["size"]
        cum_util += it["utility"]
        if (i + 1) % step == 0 or i == N - 1:
            alpha = cum_size / total_size
            D = cum_util / total_utility
            points.append((alpha, D))

    return points


def fit_power_law(points):
    """Fit D(α) = A·α^β via log-log regression. Returns (A, beta, R²)."""
    filtered = [(a, d) for a, d in points if a > 0.01 and d > 0.001 and a < 0.99]
    if len(filtered) < 3:
        return None, None, 0.0

    log_a = [math.log(a) for a, d in filtered]
    log_d = [math.log(d) for a, d in filtered]
    n = len(log_a)

    mean_la = sum(log_a) / n
    mean_ld = sum(log_d) / n
    cov = sum((log_a[i] - mean_la) * (log_d[i] - mean_ld) for i in range(n)) / n
    var_la = sum((log_a[i] - mean_la) ** 2 for i in range(n)) / n

    if var_la == 0:
        return None, None, 0.0

    beta = cov / var_la
    log_A = mean_ld - beta * mean_la
    A = math.exp(log_A)

    ss_res = sum((log_d[i] - (beta * log_a[i] + log_A)) ** 2 for i in range(n))
    ss_tot = sum((log_d[i] - mean_ld) ** 2 for i in range(n))
    r_sq = 1 - ss_res / ss_tot if ss_tot > 0 else 0

    return A, beta, r_sq


def compute_working_set(items, capacity):
    """Compute working set: how many items fit in capacity, ordered by utility density."""
    sorted_items = sorted(items, key=lambda x: x["utility"] / x["size"] if x["size"] > 0 else 0, reverse=True)
    total_utility = sum(it["utility"] for it in items)

    results = {}
    cum_size = 0
    cum_util = 0
    targets = [0.50, 0.80, 0.90, 0.95, 0.99]
    target_idx = 0

    for i, it in enumerate(sorted_items):
        cum_size += it["size"]
        cum_util += it["utility"]
        while target_idx < len(targets) and cum_util >= targets[target_idx] * total_utility:
            f = targets[target_idx]
            results[f] = {
                "items": i + 1,
                "size": cum_size,
                "fits_in_capacity": cum_size <= capacity,
                "capacity_fraction": cum_size / capacity if capacity > 0 else float("inf"),
            }
            target_idx += 1

    # F_max: maximum utility fraction that fits in capacity
    cum_size = 0
    cum_util = 0
    f_max = 0.0
    for it in sorted_items:
        if cum_size + it["size"] > capacity:
            break
        cum_size += it["size"]
        cum_util += it["utility"]
        f_max = cum_util / total_utility

    results["F_max"] = f_max
    results["inaccessible"] = 1 - f_max

    return results


def compute_compression_budget(A, beta, distortion_budgets=None):
    """Given R(D) parameters, compute max compression for distortion budgets."""
    if distortion_budgets is None:
        distortion_budgets = [0.01, 0.05, 0.10, 0.15, 0.20]

    results = {}
    for D in distortion_budgets:
        alpha_max = (D / A) ** (1 / beta) if A > 0 and beta > 0 else 0
        alpha_max = min(alpha_max, 1.0)
        results[f"D_{int(100*D)}pct"] = {
            "distortion_budget": D,
            "max_compression": alpha_max,
        }
    return results


def analyze(items, capacity=180000, label="corpus"):
    """Full rate-distortion analysis."""
    N = len(items)
    total_size = sum(it["size"] for it in items)
    total_utility = sum(it["utility"] for it in items)
    mean_size = total_size / N if N else 0

    # Citation entropy
    probs = [it["utility"] / total_utility for it in items if it["utility"] > 0 and total_utility > 0]
    H = -sum(p * math.log2(p) for p in probs if p > 0) if probs else 0
    H_max = math.log2(N) if N > 1 else 0

    # Gini coefficient
    utilities = sorted(it["utility"] for it in items)
    n = len(utilities)
    if n > 0 and sum(utilities) > 0:
        numerator = sum((2 * (i + 1) - n - 1) * utilities[i] for i in range(n))
        gini = numerator / (n * sum(utilities))
    else:
        gini = 0

    # R(D) curve
    rd_points = compute_rd_curve(items)
    A, beta, r_sq = fit_power_law(rd_points)

    # Working set
    ws = compute_working_set(items, capacity)

    # Compression budgets
    budgets = compute_compression_budget(A, beta) if A and beta else {}

    # Growth limit
    ws_frac_50 = ws.get(0.50, {}).get("items", N * 0.2) / N
    N_critical = capacity / (ws_frac_50 * mean_size) if ws_frac_50 > 0 and mean_size > 0 else float("inf")

    result = {
        "label": label,
        "summary": {
            "N": N,
            "total_size": total_size,
            "total_utility": total_utility,
            "mean_size": round(mean_size, 1),
            "utility_entropy_bits": round(H, 2),
            "max_entropy_bits": round(H_max, 2),
            "entropy_efficiency": round(H / H_max, 4) if H_max > 0 else 0,
            "utility_gini": round(gini, 4),
        },
        "rate_distortion": {
            "model": f"D(α) = {A:.4f}·α^{beta:.4f}" if A else "insufficient data",
            "A": round(A, 4) if A else None,
            "beta": round(beta, 4) if beta else None,
            "R_squared": round(r_sq, 4),
            "favorable": beta is not None and beta > 1,
            "interpretation": (
                f"β={beta:.2f}>1: compression is favorable (distortion grows slower than compression)"
                if beta and beta > 1
                else f"β={beta:.2f}≤1: compression is unfavorable" if beta else "insufficient data"
            ),
        },
        "information_bottleneck": {
            "capacity": capacity,
            "F_max": round(ws.get("F_max", 0), 4),
            "inaccessible_fraction": round(ws.get("inaccessible", 1), 4),
            "N_critical_50pct": round(N_critical),
            "growth_ratio": round(N / N_critical, 3) if N_critical < float("inf") else 0,
        },
        "working_set": {
            f"{int(100*f)}pct": v for f, v in ws.items() if isinstance(f, float) and f < 1
        },
        "compression_budgets": budgets,
        "strategy_comparison_at_30pct": {},
    }

    # Compare strategies at 30% compression
    if N > 10 and total_utility > 0:
        import random

        random.seed(42)
        sorted_optimal = sorted(items, key=lambda x: x["utility"] / x["size"] if x["size"] > 0 else 0)
        sorted_random = items[:]
        random.shuffle(sorted_random)
        sorted_size = sorted(items, key=lambda x: x["size"], reverse=True)

        target = int(0.3 * N)
        for name, order in [("optimal", sorted_optimal), ("random", sorted_random), ("size_only", sorted_size)]:
            removed_util = sum(it["utility"] for it in order[:target])
            d = removed_util / total_utility
            result["strategy_comparison_at_30pct"][name] = round(100 * d, 1)

    return result


def main():
    parser = argparse.ArgumentParser(description="Rate-distortion analysis for knowledge systems")
    parser.add_argument("--swarm", action="store_true", help="Analyze swarm lesson corpus")
    parser.add_argument("--input", type=str, help="Path to external JSON: [{id, size, utility}, ...]")
    parser.add_argument("--capacity", type=int, default=180000, help="Channel capacity (tokens/bytes)")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--budget", type=float, nargs="*", help="Distortion budgets to evaluate")
    args = parser.parse_args()

    if args.swarm:
        items = load_swarm_data()
        label = "swarm-lessons"
    elif args.input:
        items = load_external_data(args.input)
        label = Path(args.input).stem
    else:
        parser.print_help()
        sys.exit(1)

    result = analyze(items, capacity=args.capacity, label=label)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        s = result["summary"]
        rd = result["rate_distortion"]
        ib = result["information_bottleneck"]

        print(f"=== Rate-Distortion Analysis: {result['label']} ===")
        print(f"Items: {s['N']} | Total size: {s['total_size']:,} | Mean: {s['mean_size']:.0f}")
        print(f"Utility entropy: {s['utility_entropy_bits']:.2f} / {s['max_entropy_bits']:.2f} bits ({100*s['entropy_efficiency']:.1f}% efficient)")
        print(f"Utility Gini: {s['utility_gini']:.4f}")
        print()
        print(f"--- R(D) Model ---")
        print(f"  {rd['model']}")
        print(f"  R² = {rd['R_squared']:.4f}")
        print(f"  {rd['interpretation']}")
        print()
        print(f"--- Information Bottleneck ---")
        print(f"  F_max = {ib['F_max']:.1%} (max utility per session)")
        print(f"  Inaccessible: {ib['inaccessible_fraction']:.1%}")
        print(f"  N_critical (50% utility): {ib['N_critical_50pct']:,} items")
        print(f"  Current growth ratio: {ib['growth_ratio']:.3f}")
        print()
        print(f"--- Working Set ---")
        for pct, ws in result["working_set"].items():
            fits = "✓" if ws.get("fits_in_capacity") else "✗"
            print(f"  {pct} utility: {ws['items']} items, {ws['size']:,} size ({ws['capacity_fraction']:.1%} of capacity) [{fits}]")
        print()
        print(f"--- Compression Budgets ---")
        for name, budget in result["compression_budgets"].items():
            print(f"  D ≤ {budget['distortion_budget']:.0%}: compress up to {budget['max_compression']:.1%}")
        print()
        cmp = result.get("strategy_comparison_at_30pct", {})
        if cmp:
            print(f"--- Strategy Comparison at 30% removal ---")
            for strategy, d in cmp.items():
                print(f"  {strategy}: {d:.1f}% distortion")


if __name__ == "__main__":
    main()
