#!/usr/bin/env python3
"""Fractional INAR model for F-SP8: discrete-native long memory.

After bounded fOU FAILED (L-1533), this tests whether integer-valued
autoregressive processes with power-law thinning weights can reproduce
the near-constant ACF plateau (0.896) observed in lesson Sharpe scores.

Models tested:
1. INAR(1) — baseline: ACF decays as α^k (exponential)
2. Fractional INAR(∞) — power-law thinning: ACF decays as k^(2d-1) (long memory)
3. Random-intercept — constant ACF = σ²_U / (σ²_U + σ²_ε) (null model for flat plateau)

Ref: Weiss (2018) INAR models; Monteiro et al. (2010) fractional INAR.
"""

from __future__ import annotations

import argparse
import json
import math
import re
from collections import Counter
from datetime import date
from pathlib import Path

import numpy as np
from scipy.optimize import minimize_scalar, minimize

from swarm_io import lesson_paths, read_text, session_number

REPO_ROOT = Path(__file__).resolve().parent.parent
LESSON_RE = re.compile(r"L-(\d+)")
SHARPE_RE = re.compile(r"Sharpe\*{0,2}:\s*(\d+)")


def load_sharpe_series() -> np.ndarray:
    pairs: list[tuple[int, float]] = []
    for path in lesson_paths():
        text = read_text(path)
        sharpe_match = SHARPE_RE.search(text)
        lesson_match = LESSON_RE.search(path.stem)
        if not sharpe_match or not lesson_match:
            continue
        pairs.append((int(lesson_match.group(1)), float(sharpe_match.group(1))))
    pairs.sort()
    if not pairs:
        raise ValueError("no Sharpe values found")
    return np.array([value for _, value in pairs], dtype=float)


def acf(series: np.ndarray, max_lag: int = 10) -> np.ndarray:
    centered = series - series.mean()
    c0 = float(np.dot(centered, centered) / len(series))
    if c0 == 0:
        return np.zeros(max_lag, dtype=float)
    return np.array(
        [
            float(np.dot(centered[: len(series) - lag], centered[lag:]) / len(series) / c0)
            for lag in range(1, max_lag + 1)
        ],
        dtype=float,
    )


def plateau_ratio(values: np.ndarray) -> float:
    if len(values) <= 5 or values[0] == 0:
        return 0.0
    return float(np.mean(values[5:]) / values[0])


def rmse(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.sqrt(np.mean((a - b) ** 2)))


# --- Model 1: INAR(1) with binomial thinning ---

def binomial_thin(x: int, alpha: float, rng: np.random.RandomState) -> int:
    """Binomial thinning: α ∘ x = Binomial(x, α)."""
    if x <= 0 or alpha <= 0:
        return 0
    return int(rng.binomial(x, min(alpha, 1.0)))


def simulate_inar1(
    n: int, alpha: float, lam: float, seed: int, burn: int = 200
) -> np.ndarray:
    """INAR(1): X_t = α ∘ X_{t-1} + ε_t, ε_t ~ Poisson(λ)."""
    rng = np.random.RandomState(seed)
    x = int(lam / (1 - alpha)) if alpha < 1 else int(lam)
    for _ in range(burn):
        x = binomial_thin(x, alpha, rng) + rng.poisson(lam)
    result = np.empty(n, dtype=int)
    for t in range(n):
        x = binomial_thin(x, alpha, rng) + rng.poisson(lam)
        result[t] = x
    return result.astype(float)


def fit_inar1(observed: np.ndarray) -> dict:
    """Fit INAR(1) via method of moments: α = ACF(1), λ = mean*(1-α)."""
    obs_acf = acf(observed, max_lag=1)
    alpha = float(np.clip(obs_acf[0], 0.01, 0.99))
    lam = max(0.1, float(np.mean(observed)) * (1 - alpha))
    return {"alpha": alpha, "lambda": lam}


# --- Model 2: Fractional INAR(∞) with power-law thinning ---

def fractional_weights(d: float, p: int) -> np.ndarray:
    """ARFIMA-style fractional differencing weights (for thinning probabilities).

    π_j = Γ(j+d) / (Γ(d) * Γ(j+1)) for j=1,...,p
    These are the coefficients of the AR(∞) representation of (1-B)^{-d}.
    Normalized to sum ≤ 1 for use as thinning probabilities.
    """
    weights = np.zeros(p, dtype=float)
    weights[0] = d
    for j in range(1, p):
        weights[j] = weights[j - 1] * (j - 1 + d) / (j + 1)
    # Normalize: total thinning probability must be < 1
    total = float(np.sum(weights))
    if total >= 1.0:
        weights *= 0.95 / total
    return weights


def simulate_finar(
    n: int, d: float, lam: float, p: int, seed: int, burn: int = 300,
    lo: int | None = None, hi: int | None = None,
) -> np.ndarray:
    """Fractional INAR(∞) truncated at lag p.

    X_t = Σ_{j=1}^{p} π_j ∘ X_{t-j} + ε_t
    where π_j are power-law thinning weights and ∘ is binomial thinning.
    If lo/hi are provided, clips to bounded support at each step.
    """
    rng = np.random.RandomState(seed)
    weights = fractional_weights(d, p)
    buf_len = p + burn + n
    buf = np.zeros(buf_len, dtype=int)
    # Initialize with stationary mean estimate
    mean_est = int(lam / max(1 - np.sum(weights), 0.05))
    buf[:p] = mean_est

    for t in range(p, buf_len):
        thinned = 0
        for j in range(min(p, t)):
            thinned += binomial_thin(int(buf[t - 1 - j]), float(weights[j]), rng)
        val = thinned + rng.poisson(lam)
        if lo is not None and hi is not None:
            val = max(lo, min(hi, val))
        buf[t] = val

    return buf[p + burn:].astype(float)


def finar_nll(params: np.ndarray, observed: np.ndarray, max_lag: int, p: int) -> float:
    """Negative log-likelihood proxy: ACF RMSE between model and observed."""
    d, lam = params
    if not 0.01 < d < 0.49 or lam < 0.01:
        return 1e6
    obs_acf = acf(observed, max_lag=max_lag)
    # Average ACF over multiple sims for stability
    sim_acfs = []
    for seed in range(5):
        try:
            sim = simulate_finar(len(observed), d, lam, p, seed=seed + 42)
            sim_acfs.append(acf(sim, max_lag=max_lag))
        except Exception:
            return 1e6
    if not sim_acfs:
        return 1e6
    mean_sim_acf = np.mean(sim_acfs, axis=0)
    return float(rmse(mean_sim_acf, obs_acf))


def fit_finar(observed: np.ndarray, max_lag: int = 10, p: int = 50) -> dict:
    """Fit fractional INAR via grid search + Nelder-Mead on ACF RMSE."""
    best_d, best_lam, best_score = 0.3, 1.0, 1e6
    obs_mean = float(np.mean(observed))

    # Grid search
    for d in [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45]:
        w_sum = float(np.sum(fractional_weights(d, p)))
        lam_est = max(0.1, obs_mean * (1 - w_sum))
        score = finar_nll(np.array([d, lam_est]), observed, max_lag, p)
        if score < best_score:
            best_d, best_lam, best_score = d, lam_est, score

    # Refine with Nelder-Mead
    result = minimize(
        finar_nll,
        np.array([best_d, best_lam]),
        args=(observed, max_lag, p),
        method="Nelder-Mead",
        options={"maxiter": 200, "xatol": 0.005, "fatol": 0.001},
    )
    if result.fun < best_score:
        best_d = float(np.clip(result.x[0], 0.01, 0.49))
        best_lam = max(0.01, float(result.x[1]))
        best_score = float(result.fun)

    return {"d": best_d, "lambda": best_lam, "p": p, "acf_rmse": best_score}


# --- Model 3: Random-intercept (null model for constant ACF) ---

def fit_random_intercept(observed: np.ndarray) -> dict:
    """Random-intercept model: X_t = U + ε_t.

    ACF(k) = Var(U) / (Var(U) + Var(ε)) = constant for all k > 0.
    Estimated as mean of observed ACF.
    """
    obs_acf = acf(observed, max_lag=10)
    rho = float(np.mean(obs_acf))
    total_var = float(np.var(observed))
    var_u = rho * total_var
    var_eps = (1 - rho) * total_var
    return {"rho": rho, "var_u": var_u, "var_eps": var_eps}


def simulate_random_intercept(
    n: int, mean: float, var_u: float, var_eps: float, seed: int
) -> np.ndarray:
    """Simulate discrete random-intercept: X_t = round(U + ε_t)."""
    rng = np.random.RandomState(seed)
    u = rng.normal(mean, math.sqrt(max(var_u, 0.01)))
    eps = rng.normal(0, math.sqrt(max(var_eps, 0.01)), size=n)
    return np.clip(np.round(u + eps), 0, 12).astype(float)


# --- Evaluation ---

def evaluate_model(
    name: str,
    observed: np.ndarray,
    simulate_fn,
    n_sims: int = 200,
    max_lag: int = 10,
) -> dict:
    """Run simulations and compute ACF statistics."""
    obs_acf = acf(observed, max_lag=max_lag)
    obs_plateau = plateau_ratio(obs_acf)

    sim_acfs = []
    sim_plateaus = []
    for seed in range(n_sims):
        try:
            sim = simulate_fn(seed)
            sim_a = acf(sim, max_lag=max_lag)
            sim_acfs.append(sim_a)
            sim_plateaus.append(plateau_ratio(sim_a))
        except Exception:
            continue

    if not sim_acfs:
        return {"name": name, "error": "all simulations failed"}

    mean_acf = np.mean(sim_acfs, axis=0)
    mean_plateau = float(np.mean(sim_plateaus))
    acf_rmse = rmse(mean_acf, obs_acf)

    return {
        "name": name,
        "n_sims": len(sim_acfs),
        "pred_acf": [float(v) for v in mean_acf],
        "pred_plateau_mean": mean_plateau,
        "pred_plateau_p05": float(np.quantile(sim_plateaus, 0.05)),
        "pred_plateau_p50": float(np.quantile(sim_plateaus, 0.50)),
        "pred_plateau_p95": float(np.quantile(sim_plateaus, 0.95)),
        "acf_rmse": acf_rmse,
        "obs_acf_rmse_improvement_vs_fou": None,  # filled later
    }


def build_report(*, session: str, artifact: str, sims: int, seed: int, max_lag: int) -> dict:
    observed = load_sharpe_series()
    obs_acf = acf(observed, max_lag=max_lag)
    obs_plateau = plateau_ratio(obs_acf)
    n = len(observed)
    obs_mean = float(np.mean(observed))

    # Fit models
    print(f"Fitting INAR(1) on n={n} observations...")
    inar1_fit = fit_inar1(observed)

    print(f"Fitting fractional INAR (this takes ~30s)...")
    finar_fit = fit_finar(observed, max_lag=max_lag, p=50)

    print("Fitting random-intercept model...")
    ri_fit = fit_random_intercept(observed)

    # Evaluate INAR(1)
    inar1_result = evaluate_model(
        "INAR(1)",
        observed,
        lambda s: simulate_inar1(n, inar1_fit["alpha"], inar1_fit["lambda"], seed=seed + s),
        n_sims=sims,
        max_lag=max_lag,
    )

    # Evaluate fractional INAR (unbounded)
    finar_result = evaluate_model(
        "Fractional INAR",
        observed,
        lambda s: simulate_finar(n, finar_fit["d"], finar_fit["lambda"], finar_fit["p"], seed=seed + s),
        n_sims=sims,
        max_lag=max_lag,
    )

    # Evaluate bounded fractional INAR (clipped to observed support)
    obs_lo, obs_hi = int(np.min(observed)), int(np.max(observed))
    bfinar_result = evaluate_model(
        "Bounded Fractional INAR",
        observed,
        lambda s: simulate_finar(n, finar_fit["d"], finar_fit["lambda"], finar_fit["p"],
                                 seed=seed + s, lo=obs_lo, hi=obs_hi),
        n_sims=sims,
        max_lag=max_lag,
    )

    # Evaluate random intercept
    ri_result = evaluate_model(
        "Random intercept",
        observed,
        lambda s: simulate_random_intercept(n, obs_mean, ri_fit["var_u"], ri_fit["var_eps"], seed=seed + s),
        n_sims=sims,
        max_lag=max_lag,
    )

    # Reference: bounded fOU from S529
    fou_rmse = 0.275  # from f-sp8-bounded-fou-s529.json
    fou_plateau = 0.251

    all_results = [inar1_result, finar_result, bfinar_result, ri_result]
    for result in all_results:
        if "acf_rmse" in result:
            result["obs_acf_rmse_improvement_vs_fou"] = float(
                (fou_rmse - result["acf_rmse"]) / fou_rmse
            )

    # Verdict
    models_by_rmse = sorted(
        all_results,
        key=lambda r: r.get("acf_rmse", 999),
    )
    best = models_by_rmse[0]
    best_name = best["name"]
    best_rmse = best.get("acf_rmse", 999)
    best_plateau = best.get("pred_plateau_mean", 0)

    finar_plateau = finar_result.get("pred_plateau_mean", 0)
    finar_rmse_val = finar_result.get("acf_rmse", 999)
    bfinar_plateau = bfinar_result.get("pred_plateau_mean", 0)
    bfinar_rmse_val = bfinar_result.get("acf_rmse", 999)

    if bfinar_plateau > 0.5 and bfinar_rmse_val < fou_rmse:
        verdict = "CONFIRMED"
        actual = (
            f"Bounded fractional INAR explains the plateau: plateau {bfinar_plateau:.3f} "
            f"(fOU: {fou_plateau:.3f}, unbounded FINAR: {finar_plateau:.3f}), "
            f"RMSE {bfinar_rmse_val:.3f} (fOU: {fou_rmse:.3f}). Discrete bounded support + "
            "long memory together produce the near-constant ACF tail. Neither alone suffices: "
            f"INAR(1) plateau={inar1_result.get('pred_plateau_mean', 0):.3f} (no long memory), "
            f"unbounded FINAR plateau={finar_plateau:.3f} (no support constraint)."
        )
    elif finar_plateau > 0.5 and finar_rmse_val < fou_rmse:
        verdict = "PARTIALLY_CONFIRMED"
        actual = (
            f"Fractional INAR improves over fOU: plateau {finar_plateau:.3f} (fOU: {fou_plateau:.3f}), "
            f"RMSE {finar_rmse_val:.3f} (fOU: {fou_rmse:.3f}). Discrete-native thinning recovers "
            "more of the flat ACF tail."
        )
    elif best_name == "Random intercept":
        verdict = "FALSIFIED"
        actual = (
            f"Random-intercept model wins: plateau {best_plateau:.3f}, RMSE {best_rmse:.3f}. "
            f"Fractional INAR plateau {finar_plateau:.3f}, RMSE {finar_rmse_val:.3f}. "
            "The near-constant ACF reflects a shared quality component, not autoregressive memory."
        )
    else:
        verdict = "INCONCLUSIVE"
        actual = (
            f"Best model: {best_name} (plateau {best_plateau:.3f}, RMSE {best_rmse:.3f}). "
            f"Unbounded FINAR plateau {finar_plateau:.3f}, bounded FINAR plateau {bfinar_plateau:.3f}. "
            f"Observed plateau {obs_plateau:.3f}. Gap narrowing but not closed."
        )

    counts = Counter(int(v) for v in observed.tolist())
    support = {str(k): counts[k] for k in sorted(counts)}

    report = {
        "experiment": f"DOMEX-SP-{session}",
        "frontier": "F-SP8",
        "session": session,
        "domain": "stochastic-processes",
        "date": date.today().isoformat(),
        "expect": (
            "Fractional INAR (discrete-native long memory) produces plateau >0.5 and RMSE < 0.275. "
            "But random-intercept (constant ACF) may outperform both AR-family models, suggesting "
            "the plateau reflects a shared quality component rather than temporal memory."
        ),
        "actual": actual,
        "verdict": verdict,
        "diff": (
            f"fOU plateau {fou_plateau:.3f} → unbounded FINAR {finar_plateau:.3f} → "
            f"bounded FINAR {bfinar_plateau:.3f} → observed {obs_plateau:.3f}. "
            f"Best RMSE: {best_name} at {best_rmse:.3f}."
        ),
        "results": {
            "series": {
                "n": n,
                "mean": obs_mean,
                "support": support,
            },
            "observed": {
                "acf": [float(v) for v in obs_acf],
                "plateau": obs_plateau,
            },
            "reference_fou": {
                "plateau": fou_plateau,
                "acf_rmse": fou_rmse,
            },
            "inar1": {
                "fit": inar1_fit,
                **{k: v for k, v in inar1_result.items() if k != "name"},
            },
            "fractional_inar": {
                "fit": finar_fit,
                **{k: v for k, v in finar_result.items() if k != "name"},
            },
            "bounded_fractional_inar": {
                "fit": {**finar_fit, "lo": obs_lo, "hi": obs_hi},
                **{k: v for k, v in bfinar_result.items() if k != "name"},
            },
            "random_intercept": {
                "fit": ri_fit,
                **{k: v for k, v in ri_result.items() if k != "name"},
            },
        },
    }

    # Print summary
    print(f"\n=== F-SP8 Fractional INAR Results ===")
    print(f"Observed: ACF plateau {obs_plateau:.3f}, mean Sharpe {obs_mean:.1f}")
    print(f"  INAR(1):    α={inar1_fit['alpha']:.3f}  plateau={inar1_result.get('pred_plateau_mean', 0):.3f}  RMSE={inar1_result.get('acf_rmse', 999):.3f}")
    print(f"  Frac INAR:  d={finar_fit['d']:.3f}  plateau={finar_plateau:.3f}  RMSE={finar_rmse_val:.3f}")
    print(f"  Bnd FINAR:  d={finar_fit['d']:.3f}  plateau={bfinar_plateau:.3f}  RMSE={bfinar_rmse_val:.3f}  [{obs_lo},{obs_hi}]")
    print(f"  Rand intcpt: ρ={ri_fit['rho']:.3f}  plateau={ri_result.get('pred_plateau_mean', 0):.3f}  RMSE={ri_result.get('acf_rmse', 999):.3f}")
    print(f"  Ref fOU:     plateau={fou_plateau:.3f}  RMSE={fou_rmse:.3f}")
    print(f"Verdict: {verdict}")

    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Fractional INAR experiment for F-SP8.")
    parser.add_argument("--session", default=f"S{session_number()}", help="Session tag")
    parser.add_argument("--artifact", default="", help="Write JSON report to path")
    parser.add_argument("--sims", type=int, default=200, help="Simulations per model")
    parser.add_argument("--seed", type=int, default=42, help="Base seed")
    parser.add_argument("--max-lag", type=int, default=10, help="Max ACF lag")
    parser.add_argument("--json", action="store_true", help="Print JSON report")
    args = parser.parse_args()

    report = build_report(
        session=args.session,
        artifact=args.artifact,
        sims=args.sims,
        seed=args.seed,
        max_lag=args.max_lag,
    )

    if args.artifact:
        artifact_path = REPO_ROOT / args.artifact
        artifact_path.parent.mkdir(parents=True, exist_ok=True)
        artifact_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote {artifact_path.relative_to(REPO_ROOT)}")

    if args.json or not args.artifact:
        print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
