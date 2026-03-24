#!/usr/bin/env python3
"""Test whether bounded/discrete observations explain the residual fOU plateau gap.

F-SP8 / DOMEX-SP-S529: prior work showed that latent fractional-OU captures the
qualitative long-memory shape of lesson Sharpe scores but underestimates the
flat autocorrelation tail on the observed integer-bounded series. This tool
adds a bounded observation layer by rank-mapping latent fOU draws onto the
empirical Sharpe distribution.
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
from scipy.optimize import minimize

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


def rmse(lhs: np.ndarray, rhs: np.ndarray) -> float:
    return float(np.sqrt(np.mean((lhs - rhs) ** 2)))


def _periodogram(series: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    centered = series - series.mean()
    ft = np.fft.rfft(centered)[1:]
    w = np.fft.rfftfreq(len(series))[1:] * 2 * np.pi
    return w, np.abs(ft) ** 2 / len(series)


def _fou_spec(w: np.ndarray, hurst: float, theta: float, sigma2: float) -> np.ndarray:
    return sigma2 * np.abs(w) ** (1 - 2 * hurst) / (theta**2 + w**2)


def _whittle(params: np.ndarray, w: np.ndarray, periodogram: np.ndarray) -> float:
    hurst, log_theta, log_sigma2 = params
    if not 0.5 < hurst < 1.0:
        return 1e12
    theta = float(np.exp(np.clip(log_theta, -10, 10)))
    sigma2 = float(np.exp(np.clip(log_sigma2, -20, 40)))
    spec = np.maximum(_fou_spec(w, hurst, theta, sigma2), 1e-30)
    return float(np.sum(np.log(spec) + periodogram / spec))


def _fou_acf(hurst: float, theta: float, sigma2: float, n: int, max_lag: int = 10) -> np.ndarray:
    fft_n = min(max(n, 64), 4096)
    w = np.arange(1, fft_n // 2 + 1) * 2 * np.pi / fft_n
    spec = _fou_spec(w, hurst, theta, sigma2)
    cov = [np.sum(spec * np.cos(w * lag)) for lag in range(max_lag + 1)]
    if cov[0] == 0:
        return np.zeros(max_lag, dtype=float)
    return np.array(cov[1:], dtype=float) / float(cov[0])


def fit_fou(series: np.ndarray, max_lag: int = 10) -> dict[str, float | list[float]]:
    w, periodogram = _periodogram(series)
    best = None
    for hurst0 in [0.6, 0.75, 0.85, 0.92]:
        for log_theta0 in [-2, 0, 2]:
            start = np.array([hurst0, log_theta0, np.log(np.var(series) + 1e-6)], dtype=float)
            result = minimize(
                _whittle,
                start,
                args=(w, periodogram),
                method="Nelder-Mead",
                options={"maxiter": 8000, "xatol": 1e-8, "fatol": 1e-8},
            )
            if best is None or result.fun < best.fun:
                best = result
    if best is None:
        raise RuntimeError("fOU fit failed")
    hurst = float(np.clip(best.x[0], 0.501, 0.999))
    theta = float(np.exp(best.x[1]))
    sigma2 = float(np.exp(best.x[2]))
    predicted_acf = _fou_acf(hurst, theta, sigma2, len(series), max_lag=max_lag)
    return {
        "H": hurst,
        "theta": theta,
        "sigma2": sigma2,
        "nll": float(best.fun),
        "pred_acf": [float(value) for value in predicted_acf],
        "pred_plateau": plateau_ratio(predicted_acf),
    }


def simulate_fou_latent(n: int, hurst: float, theta: float, sigma2: float, seed: int) -> np.ndarray:
    rng = np.random.RandomState(seed)
    freqs = np.fft.rfftfreq(n)
    coeffs = np.zeros(len(freqs), dtype=complex)
    if len(freqs) > 1:
        w = np.maximum(freqs[1:] * 2 * np.pi, 1e-6)
        spec = np.maximum(_fou_spec(w, hurst, theta, sigma2), 1e-12)
        coeffs[1:] = (rng.normal(size=len(spec)) + 1j * rng.normal(size=len(spec))) * np.sqrt(spec / 2.0)
        if n % 2 == 0:
            coeffs[-1] = rng.normal() * math.sqrt(float(spec[-1]))
    latent = np.fft.irfft(coeffs, n=n)
    latent -= latent.mean()
    std = float(latent.std()) or 1.0
    return latent / std


def empirical_rank_map(latent: np.ndarray, observed: np.ndarray) -> np.ndarray:
    mapped = np.empty_like(latent, dtype=float)
    mapped[np.argsort(latent, kind="mergesort")] = np.sort(observed)
    return mapped


def evaluate_bounded_fou(
    observed: np.ndarray,
    fit: dict[str, float | list[float]],
    *,
    sims: int = 200,
    seed: int = 123,
    max_lag: int = 10,
) -> dict[str, float | list[float]]:
    observed_sorted = np.sort(observed)
    acf_paths: list[np.ndarray] = []
    plateau_paths: list[float] = []
    for offset in range(sims):
        latent = simulate_fou_latent(
            len(observed),
            float(fit["H"]),
            float(fit["theta"]),
            float(fit["sigma2"]),
            seed + offset,
        )
        bounded = empirical_rank_map(latent, observed_sorted)
        bounded_acf = acf(bounded, max_lag=max_lag)
        acf_paths.append(bounded_acf)
        plateau_paths.append(plateau_ratio(bounded_acf))
    mean_acf = np.mean(acf_paths, axis=0)
    plateau_arr = np.array(plateau_paths, dtype=float)
    return {
        "pred_acf": [float(value) for value in mean_acf],
        "pred_plateau_mean": float(np.mean(plateau_arr)),
        "pred_plateau_p05": float(np.quantile(plateau_arr, 0.05)),
        "pred_plateau_p50": float(np.quantile(plateau_arr, 0.50)),
        "pred_plateau_p95": float(np.quantile(plateau_arr, 0.95)),
    }


def build_report(*, session: str, artifact: str, sims: int, seed: int, max_lag: int) -> dict[str, object]:
    observed = load_sharpe_series()
    observed_acf = acf(observed, max_lag=max_lag)
    observed_plateau = plateau_ratio(observed_acf)
    fou_fit = fit_fou(observed, max_lag=max_lag)
    bounded = evaluate_bounded_fou(observed, fou_fit, sims=sims, seed=seed, max_lag=max_lag)

    unbounded_acf = np.array(fou_fit["pred_acf"], dtype=float)
    bounded_acf = np.array(bounded["pred_acf"], dtype=float)
    unbounded_rmse = rmse(unbounded_acf, observed_acf)
    bounded_rmse = rmse(bounded_acf, observed_acf)
    unbounded_plateau = float(fou_fit["pred_plateau"])
    bounded_plateau = float(bounded["pred_plateau_mean"])
    baseline_gap = abs(observed_plateau - unbounded_plateau)
    bounded_gap = abs(observed_plateau - bounded_plateau)
    gap_reduction = 0.0 if baseline_gap == 0 else float((baseline_gap - bounded_gap) / baseline_gap)
    expectation_met = bounded_plateau >= 0.55 and bounded_rmse < 0.20

    if expectation_met:
        actual = (
            "Bounded/quantized fOU PARTIALLY CONFIRMED the residual-gap hypothesis: observed plateau "
            f"{observed_plateau:.3f}; unbounded fOU {unbounded_plateau:.3f} (RMSE {unbounded_rmse:.3f}); "
            f"bounded empirical-rank fOU {bounded_plateau:.3f} (RMSE {bounded_rmse:.3f}). Discrete bounded "
            "observations recover most of the flat ACF tail without changing the latent long-memory family."
        )
        diff = (
            "Expected bounded plateau >=0.55 and RMSE <0.20. Got plateau "
            f"{bounded_plateau:.3f} and RMSE {bounded_rmse:.3f}. Gap reduction vs unbounded fOU = "
            f"{gap_reduction:.1%}. Next step is to formalize the observation layer, not abandon latent fOU."
        )
    else:
        actual = (
            "Bounded/quantized fOU FAILED as a full explanation of the residual gap: observed plateau "
            f"{observed_plateau:.3f}; unbounded fOU {unbounded_plateau:.3f} (RMSE {unbounded_rmse:.3f}); "
            f"bounded empirical-rank fOU {bounded_plateau:.3f} (RMSE {bounded_rmse:.3f}). Discrete bounded "
            "support changes the fit, but it does not close the plateau gap enough on its own."
        )
        diff = (
            "Expected bounded plateau >=0.55 and RMSE <0.20. Got plateau "
            f"{bounded_plateau:.3f} and RMSE {bounded_rmse:.3f}. Gap reduction vs unbounded fOU = "
            f"{gap_reduction:.1%}. Bounded support alone is insufficient; fractional INAR remains the next "
            "discriminator."
        )

    counts = Counter(int(value) for value in observed.tolist())
    support = {str(key): counts[key] for key in sorted(counts)}
    return {
        "experiment": "DOMEX-SP-S529",
        "frontier": "F-SP8",
        "session": session,
        "domain": "stochastic-processes",
        "date": date.today().isoformat(),
        "expect": (
            "Bounded/quantized fOU lifts predicted plateau ratio to >=0.55 and lowers ACF RMSE below 0.20; "
            "if not, bounded support alone is insufficient and fractional INAR is the next discriminator."
        ),
        "actual": actual,
        "diff": diff,
        "results": {
            "series": {
                "n": int(len(observed)),
                "min": float(np.min(observed)),
                "max": float(np.max(observed)),
                "mean": float(np.mean(observed)),
                "support": support,
            },
            "config": {
                "artifact": artifact,
                "sims": sims,
                "seed": seed,
                "max_lag": max_lag,
            },
            "observed": {
                "acf": [float(value) for value in observed_acf],
                "plateau": float(observed_plateau),
            },
            "unbounded_fou": {
                "H": float(fou_fit["H"]),
                "theta": float(fou_fit["theta"]),
                "sigma2": float(fou_fit["sigma2"]),
                "nll": float(fou_fit["nll"]),
                "acf": [float(value) for value in unbounded_acf],
                "plateau": float(unbounded_plateau),
                "acf_rmse": float(unbounded_rmse),
            },
            "bounded_fou": {
                "acf": [float(value) for value in bounded_acf],
                "plateau_mean": float(bounded_plateau),
                "plateau_p05": float(bounded["pred_plateau_p05"]),
                "plateau_p50": float(bounded["pred_plateau_p50"]),
                "plateau_p95": float(bounded["pred_plateau_p95"]),
                "acf_rmse": float(bounded_rmse),
            },
            "diagnostics": {
                "expectation_met": expectation_met,
                "gap_reduction": float(gap_reduction),
                "baseline_gap": float(baseline_gap),
                "bounded_gap": float(bounded_gap),
            },
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Bounded-observation fOU test for F-SP8.")
    parser.add_argument("--session", default=f"S{session_number()}", help="Session tag")
    parser.add_argument("--artifact", default="", help="Write JSON report to this path")
    parser.add_argument("--sims", type=int, default=200, help="Number of bounded fOU simulations")
    parser.add_argument("--seed", type=int, default=123, help="Simulation seed")
    parser.add_argument("--max-lag", type=int, default=10, help="Max lag for ACF comparison")
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
