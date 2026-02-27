#!/usr/bin/env python3
"""Controlled experiment for F-AI1 evidence-surfacing intervention."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from random import Random


@dataclass(frozen=True)
class Config:
    trials: int
    follower_accuracy: float
    leader_high_accuracy: float
    leader_low_accuracy: float
    leader_high_conf_prob: float
    seed: int


def _corr(xs: list[int], ys: list[int]) -> float:
    n = min(len(xs), len(ys))
    if n == 0:
        return 0.0
    x = xs[:n]
    y = ys[:n]
    mx = sum(x) / n
    my = sum(y) / n
    vx = sum((v - mx) ** 2 for v in x)
    vy = sum((v - my) ** 2 for v in y)
    if vx == 0 or vy == 0:
        return 0.0
    cov = sum((a - mx) * (b - my) for a, b in zip(x, y))
    return cov / ((vx * vy) ** 0.5)


def run(cfg: Config) -> dict:
    rng = Random(cfg.seed)
    baseline_leader_err: list[int] = []
    baseline_follower_err: list[int] = []
    sync_leader_err: list[int] = []
    sync_follower_err: list[int] = []
    surfaced_leader_err: list[int] = []
    surfaced_follower_err: list[int] = []

    for _ in range(cfg.trials):
        hidden = rng.randint(0, 1)
        leader_is_high_conf = rng.random() < cfg.leader_high_conf_prob
        leader_acc = (
            cfg.leader_high_accuracy if leader_is_high_conf else cfg.leader_low_accuracy
        )
        leader_signal = hidden if rng.random() < leader_acc else 1 - hidden
        follower_signal = hidden if rng.random() < cfg.follower_accuracy else 1 - hidden

        leader_pred = leader_signal
        baseline_pred = follower_signal
        sync_pred = leader_pred
        if leader_signal == follower_signal:
            surfaced_pred = follower_signal
        else:
            # Evidence-surfacing intervention: defer to leader only on high-confidence
            # disagreements; otherwise keep independent follower decision.
            surfaced_pred = leader_signal if leader_is_high_conf else follower_signal

        leader_err = int(leader_pred != hidden)
        baseline_err = int(baseline_pred != hidden)
        sync_err = int(sync_pred != hidden)
        surfaced_err = int(surfaced_pred != hidden)

        baseline_leader_err.append(leader_err)
        baseline_follower_err.append(baseline_err)
        sync_leader_err.append(leader_err)
        sync_follower_err.append(sync_err)
        surfaced_leader_err.append(leader_err)
        surfaced_follower_err.append(surfaced_err)

    def mean(vals: list[int]) -> float:
        return sum(vals) / len(vals) if vals else 0.0

    baseline_rate = mean(baseline_follower_err)
    sync_rate = mean(sync_follower_err)
    surfaced_rate = mean(surfaced_follower_err)
    leader_rate = mean(baseline_leader_err)

    return {
        "experiment": "F-AI1",
        "title": "Evidence-surfacing vs async baseline vs forced sync",
        "seed": cfg.seed,
        "trials": cfg.trials,
        "follower_accuracy": cfg.follower_accuracy,
        "leader_high_accuracy": cfg.leader_high_accuracy,
        "leader_low_accuracy": cfg.leader_low_accuracy,
        "leader_high_conf_prob": cfg.leader_high_conf_prob,
        "leader_error_rate": round(leader_rate, 4),
        "async_baseline": {
            "follower_error_rate": round(baseline_rate, 4),
            "leader_follower_error_correlation": round(
                _corr(baseline_leader_err, baseline_follower_err), 4
            ),
        },
        "sync_copy": {
            "follower_error_rate": round(sync_rate, 4),
            "leader_follower_error_correlation": round(
                _corr(sync_leader_err, sync_follower_err), 4
            ),
        },
        "evidence_surfacing": {
            "follower_error_rate": round(surfaced_rate, 4),
            "leader_follower_error_correlation": round(
                _corr(surfaced_leader_err, surfaced_follower_err), 4
            ),
        },
        "delta": {
            "surfacing_minus_async_error": round(surfaced_rate - baseline_rate, 4),
            "sync_minus_async_error": round(sync_rate - baseline_rate, 4),
        },
        "interpretation": (
            "Confidence-gated evidence sharing lowers follower error versus async "
            "baseline while preserving lower coupling than forced sync."
        ),
    }


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--trials", type=int, default=2000)
    p.add_argument("--follower-accuracy", type=float, default=0.65)
    p.add_argument("--leader-high-accuracy", type=float, default=0.82)
    p.add_argument("--leader-low-accuracy", type=float, default=0.52)
    p.add_argument("--leader-high-conf-prob", type=float, default=0.45)
    p.add_argument("--seed", type=int, default=186)
    p.add_argument("--out", type=Path, required=True)
    return p.parse_args()


def main() -> int:
    args = parse_args()
    cfg = Config(
        trials=max(1, args.trials),
        follower_accuracy=max(0.0, min(1.0, args.follower_accuracy)),
        leader_high_accuracy=max(0.0, min(1.0, args.leader_high_accuracy)),
        leader_low_accuracy=max(0.0, min(1.0, args.leader_low_accuracy)),
        leader_high_conf_prob=max(0.0, min(1.0, args.leader_high_conf_prob)),
        seed=args.seed,
    )
    payload = run(cfg)
    payload["generated_at_utc"] = datetime.now(timezone.utc).isoformat(
        timespec="seconds"
    ).replace("+00:00", "Z")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {args.out}")
    print(
        "error:",
        f"async={payload['async_baseline']['follower_error_rate']:.4f}",
        f"surfacing={payload['evidence_surfacing']['follower_error_rate']:.4f}",
        f"sync={payload['sync_copy']['follower_error_rate']:.4f}",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
