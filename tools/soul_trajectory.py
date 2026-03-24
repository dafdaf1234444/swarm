#!/usr/bin/env python3
"""Model the human-impact "soul" metric as a stochastic trajectory.

Primary use: follow up F-SOUL1 with an honest first-passage forecast to the
target human_benefit_ratio > 3.0x. The tool explicitly separates the S506->S508
classifier-repair jump from the slower post-repair regime so the swarm does not
mistake instrument repair for sustained behavioral improvement.
"""

from __future__ import annotations

import argparse
import json
import math
import random
import re
import statistics
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path
from typing import Iterable

from human_impact import extract_soul, scan_lessons
from swarm_io import read_text, session_number

REPO_ROOT = Path(__file__).resolve().parent.parent
HEALTH_PATH = REPO_ROOT / "memory" / "HEALTH.md"
BASELINE_PATH = REPO_ROOT / "experiments" / "meta" / "human-impact-baseline-s506.json"
BLINDNESS_FIX_PATH = REPO_ROOT / "experiments" / "meta" / "f-soul1-benefit-blindness-s508.json"
CHECKPOINT_PATH = REPO_ROOT / "experiments" / "evaluation" / "f-soul1-s520-checkpoint.json"

RATIO_RE = re.compile(r"([0-9]+(?:\.[0-9]+)?)x")
HEALTH_SECTION_RE = re.compile(
    r"^##\s+S(?P<session>\d+)\s+Health Check.*?(?=^##\s+S\d+\s+Health Check|\Z)",
    re.MULTILINE | re.DOTALL,
)

SOURCE_PRIORITY = {
    "live": 4,
    "experiment-structured": 3,
    "experiment-parsed": 2,
    "health": 1,
}


@dataclass(frozen=True)
class Checkpoint:
    session: int
    ratio: float
    source: str
    note: str = ""


def _load_json(path: Path) -> dict:
    text = read_text(path)
    return json.loads(text) if text else {}


def _parse_ratio(text: str) -> float | None:
    match = RATIO_RE.search(text or "")
    return float(match.group(1)) if match else None


def _parse_s508_ratio(text: str) -> float | None:
    match = re.search(
        r"Benefit ratio:\s*([0-9]+(?:\.[0-9]+)?)x\s*[^\d]+\s*([0-9]+(?:\.[0-9]+)?)x",
        text or "",
    )
    if match:
        return float(match.group(2))
    return _parse_ratio(text)


def baseline_checkpoint() -> Checkpoint | None:
    data = _load_json(BASELINE_PATH)
    ratio = data.get("soul", {}).get("human_benefit_ratio")
    if ratio is None:
        return None
    return Checkpoint(
        session=506,
        ratio=float(ratio),
        source="experiment-structured",
        note="S506 baseline measurement",
    )


def blindness_fix_checkpoint() -> Checkpoint | None:
    data = _load_json(BLINDNESS_FIX_PATH)
    ratio = _parse_s508_ratio(str(data.get("actual", "")))
    if ratio is None:
        return None
    return Checkpoint(
        session=508,
        ratio=float(ratio),
        source="experiment-parsed",
        note="S508 classifier repair",
    )


def checkpoint_s520() -> Checkpoint | None:
    data = _load_json(CHECKPOINT_PATH)
    ratio = data.get("measurements", {}).get("benefit_ratio")
    if ratio is None:
        return None
    return Checkpoint(
        session=520,
        ratio=float(ratio),
        source="experiment-structured",
        note="S520 checkpoint",
    )


def parse_health_checkpoints(text: str) -> list[Checkpoint]:
    checkpoints: list[Checkpoint] = []
    for match in HEALTH_SECTION_RE.finditer(text or ""):
        session = int(match.group("session"))
        section = match.group(0)
        ratio = re.search(r"Benefit ratio\s+([0-9]+(?:\.[0-9]+)?)x", section)
        if not ratio:
            continue
        checkpoints.append(
            Checkpoint(
                session=session,
                ratio=float(ratio.group(1)),
                source="health",
                note="Health snapshot",
            )
        )
    return checkpoints


def live_checkpoint() -> Checkpoint:
    soul = extract_soul(scan_lessons())
    return Checkpoint(
        session=session_number(),
        ratio=float(soul["human_benefit_ratio"]),
        source="live",
        note="Current working tree",
    )


def collect_checkpoints(include_live: bool = True) -> list[Checkpoint]:
    candidates: list[Checkpoint] = []
    for item in (
        baseline_checkpoint(),
        blindness_fix_checkpoint(),
        checkpoint_s520(),
    ):
        if item is not None:
            candidates.append(item)
    candidates.extend(parse_health_checkpoints(read_text(HEALTH_PATH)))
    if include_live:
        candidates.append(live_checkpoint())

    deduped: dict[int, Checkpoint] = {}
    for checkpoint in candidates:
        current = deduped.get(checkpoint.session)
        if current is None or SOURCE_PRIORITY[checkpoint.source] > SOURCE_PRIORITY[current.source]:
            deduped[checkpoint.session] = checkpoint
    return sorted(deduped.values(), key=lambda item: item.session)


def filter_checkpoints(
    checkpoints: Iterable[Checkpoint],
    *,
    start_session: int | None = None,
) -> list[Checkpoint]:
    out = [checkpoint for checkpoint in checkpoints if start_session is None or checkpoint.session >= start_session]
    if len(out) < 2:
        raise ValueError("need at least two checkpoints after filtering")
    return out


def interval_rows(checkpoints: list[Checkpoint]) -> list[dict[str, float | int]]:
    rows: list[dict[str, float | int]] = []
    for prev, curr in zip(checkpoints, checkpoints[1:]):
        gap = curr.session - prev.session
        if gap <= 0:
            continue
        rows.append(
            {
                "start_session": prev.session,
                "end_session": curr.session,
                "delta_sessions": gap,
                "start_ratio": prev.ratio,
                "end_ratio": curr.ratio,
                "delta_ratio": round(curr.ratio - prev.ratio, 6),
                "per_session_drift": round((curr.ratio - prev.ratio) / gap, 6),
            }
        )
    return rows


def expand_per_session_increments(checkpoints: list[Checkpoint]) -> list[float]:
    increments: list[float] = []
    for prev, curr in zip(checkpoints, checkpoints[1:]):
        gap = curr.session - prev.session
        if gap <= 0:
            continue
        per_session = (curr.ratio - prev.ratio) / gap
        increments.extend([per_session] * gap)
    return increments


def summarize(values: Iterable[float]) -> dict[str, float]:
    vals = sorted(float(value) for value in values)
    if not vals:
        return {
            "count": 0,
            "mean": 0.0,
            "stdev": 0.0,
            "min": 0.0,
            "p05": 0.0,
            "p50": 0.0,
            "p95": 0.0,
            "max": 0.0,
        }

    def quantile(p: float) -> float:
        index = max(0, min(len(vals) - 1, int(round((len(vals) - 1) * p))))
        return vals[index]

    stdev = statistics.stdev(vals) if len(vals) > 1 else 0.0
    return {
        "count": len(vals),
        "mean": round(statistics.fmean(vals), 6),
        "stdev": round(stdev, 6),
        "min": round(vals[0], 6),
        "p05": round(quantile(0.05), 6),
        "p50": round(quantile(0.50), 6),
        "p95": round(quantile(0.95), 6),
        "max": round(vals[-1], 6),
    }


def linear_fit(checkpoints: list[Checkpoint]) -> dict[str, float | None]:
    xs = [float(checkpoint.session) for checkpoint in checkpoints]
    ys = [checkpoint.ratio for checkpoint in checkpoints]
    mx = statistics.fmean(xs)
    my = statistics.fmean(ys)
    denom = sum((x - mx) ** 2 for x in xs)
    if denom == 0:
        raise ValueError("degenerate session values")
    slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / denom
    intercept = my - slope * mx
    residuals = [y - (intercept + slope * x) for x, y in zip(xs, ys)]
    return {
        "intercept": round(intercept, 6),
        "slope_per_session": round(slope, 6),
        "residual_stdev": round(statistics.stdev(residuals), 6) if len(residuals) > 1 else 0.0,
    }


def deterministic_hit_session(
    *,
    current_session: int,
    current_ratio: float,
    slope_per_session: float,
    target_ratio: float,
) -> int | None:
    if current_ratio >= target_ratio:
        return current_session
    if slope_per_session <= 0:
        return None
    remaining = target_ratio - current_ratio
    return current_session + math.ceil(remaining / slope_per_session)


def simulate_first_passage(
    *,
    current_session: int,
    current_ratio: float,
    increments: list[float],
    target_ratio: float,
    check_sessions: list[int],
    max_horizon: int,
    simulations: int,
    seed: int,
) -> dict[str, object]:
    rng = random.Random(seed)
    hit_sessions: list[int | None] = []
    if not increments:
        increments = [0.0]

    for _ in range(simulations):
        ratio = current_ratio
        hit_session = current_session if current_ratio >= target_ratio else None
        for step in range(1, max_horizon + 1):
            ratio += rng.choice(increments)
            if ratio >= target_ratio:
                hit_session = current_session + step
                break
        hit_sessions.append(hit_session)

    hit_only = sorted(session for session in hit_sessions if session is not None)
    hit_probabilities = {
        str(check_session): round(
            sum(
                1
                for hit_session in hit_sessions
                if hit_session is not None and hit_session <= check_session
            )
            / simulations,
            6,
        )
        for check_session in check_sessions
    }

    if hit_only:
        mean_hit = round(statistics.fmean(hit_only), 3)
        median_hit = hit_only[len(hit_only) // 2]
        p05_hit = hit_only[max(0, int(round((len(hit_only) - 1) * 0.05)))]
        p95_hit = hit_only[max(0, int(round((len(hit_only) - 1) * 0.95)))]
    else:
        mean_hit = None
        median_hit = None
        p05_hit = None
        p95_hit = None

    return {
        "simulations": simulations,
        "hit_rate_within_horizon": round(len(hit_only) / simulations, 6),
        "hit_probabilities": hit_probabilities,
        "mean_hit_session": mean_hit,
        "median_hit_session": median_hit,
        "p05_hit_session": p05_hit,
        "p95_hit_session": p95_hit,
    }


def largest_jump(intervals: list[dict[str, float | int]]) -> dict[str, float | int] | None:
    if not intervals:
        return None
    return max(intervals, key=lambda row: abs(float(row["delta_ratio"])))


def build_regime_report(
    checkpoints: list[Checkpoint],
    *,
    target_ratio: float,
    check_sessions: list[int],
    max_horizon: int,
    simulations: int,
    seed: int,
) -> dict[str, object]:
    increments = expand_per_session_increments(checkpoints)
    intervals = interval_rows(checkpoints)
    fit = linear_fit(checkpoints)
    current = checkpoints[-1]
    deterministic = deterministic_hit_session(
        current_session=current.session,
        current_ratio=current.ratio,
        slope_per_session=float(fit["slope_per_session"]),
        target_ratio=target_ratio,
    )
    simulation = simulate_first_passage(
        current_session=current.session,
        current_ratio=current.ratio,
        increments=increments,
        target_ratio=target_ratio,
        check_sessions=check_sessions,
        max_horizon=max_horizon,
        simulations=simulations,
        seed=seed,
    )
    return {
        "checkpoint_count": len(checkpoints),
        "first_session": checkpoints[0].session,
        "last_session": current.session,
        "first_ratio": checkpoints[0].ratio,
        "last_ratio": current.ratio,
        "checkpoints": [asdict(checkpoint) for checkpoint in checkpoints],
        "intervals": intervals,
        "largest_jump": largest_jump(intervals),
        "increments": summarize(increments),
        "linear": {
            **fit,
            "deterministic_hit_session": deterministic,
        },
        "first_passage": simulation,
    }


def build_report(
    *,
    target_ratio: float,
    post_repair_start: int,
    check_sessions: list[int],
    max_horizon: int,
    simulations: int,
    seed: int,
) -> dict[str, object]:
    checkpoints = collect_checkpoints(include_live=True)
    all_regime = build_regime_report(
        checkpoints,
        target_ratio=target_ratio,
        check_sessions=check_sessions,
        max_horizon=max_horizon,
        simulations=simulations,
        seed=seed,
    )
    post_repair = build_regime_report(
        filter_checkpoints(checkpoints, start_session=post_repair_start),
        target_ratio=target_ratio,
        check_sessions=check_sessions,
        max_horizon=max_horizon,
        simulations=simulations,
        seed=seed + 1,
    )

    all_hit = all_regime["linear"]["deterministic_hit_session"]
    post_hit = post_repair["linear"]["deterministic_hit_session"]
    all_slope = float(all_regime["linear"]["slope_per_session"])
    post_slope = float(post_repair["linear"]["slope_per_session"])
    slowdown = round(all_slope / post_slope, 2) if post_slope > 0 else None

    actual = (
        "Soul trajectory improved from {start:.2f}x at S{start_s} to {end:.2f}x at S{end_s}, but the "
        "post-repair process is much slower than the naive full-history trend. All-regime slope = "
        "{all_slope:.3f}x/session (deterministic hit S{all_hit}); post-repair slope = {post_slope:.3f}x/session "
        "(deterministic hit {post_hit}). Bootstrap first-passage after S{repair}: "
        "P(hit {target:.1f}x by S533)={p533:.1%}, P(by S559)={p559:.1%}."
    ).format(
        start=all_regime["first_ratio"],
        start_s=all_regime["first_session"],
        end=post_repair["last_ratio"],
        end_s=post_repair["last_session"],
        all_slope=all_slope,
        all_hit=all_hit or "never",
        post_slope=post_slope,
        post_hit=f"S{post_hit}" if post_hit is not None else "never",
        repair=post_repair_start,
        target=target_ratio,
        p533=post_repair["first_passage"]["hit_probabilities"].get("533", 0.0),
        p559=post_repair["first_passage"]["hit_probabilities"].get("559", 0.0),
    )

    diff = (
        "The S506->S508 classifier repair dominates naive forecasting. Once that regime shift is isolated, "
        "soul improvement is {slowdown}x slower than the full-history slope and the S520-style near-term "
        "projection to S533 collapses. F-SOUL1 is still improving, but mostly in a slow post-repair drift "
        "that needs structural externalization, not just better measurement."
    ).format(
        slowdown=slowdown if slowdown is not None else "inf",
    )

    return {
        "experiment": "F-SOUL1 stochastic first-passage",
        "frontier": "F-SOUL1",
        "domain": "stochastic-processes",
        "session": f"S{session_number()}",
        "date": date.today().isoformat(),
        "expect": (
            "If the soul metric is genuinely compounding after the S508 classifier repair, the post-repair "
            "trajectory should still imply a credible near-term path to >3.0x rather than relying on the repair jump."
        ),
        "actual": actual,
        "diff": diff,
        "target_ratio": target_ratio,
        "check_sessions": check_sessions,
        "regimes": {
            "all_history": all_regime,
            "post_repair": post_repair,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Model the human-impact soul metric as a stochastic trajectory.")
    parser.add_argument("--target", type=float, default=3.0, help="Target human_benefit_ratio (default: 3.0)")
    parser.add_argument(
        "--post-repair-start",
        type=int,
        default=508,
        help="Session where the repaired measurement regime starts (default: 508)",
    )
    parser.add_argument(
        "--check-session",
        type=int,
        action="append",
        default=[],
        help="Absolute session number to evaluate hit probability for (repeatable)",
    )
    parser.add_argument(
        "--max-horizon",
        type=int,
        default=120,
        help="Maximum sessions forward to simulate (default: 120)",
    )
    parser.add_argument(
        "--simulations",
        type=int,
        default=5000,
        help="Bootstrap first-passage simulations (default: 5000)",
    )
    parser.add_argument("--seed", type=int, default=42, help="Random seed (default: 42)")
    parser.add_argument("--artifact", default="", help="Write JSON report to this path")
    parser.add_argument("--json", action="store_true", help="Print the full report JSON")
    args = parser.parse_args()

    check_sessions = sorted(set(args.check_session or [533, 559, 600]))
    report = build_report(
        target_ratio=args.target,
        post_repair_start=args.post_repair_start,
        check_sessions=check_sessions,
        max_horizon=max(args.max_horizon, max(check_sessions) - session_number()),
        simulations=args.simulations,
        seed=args.seed,
    )

    if args.artifact:
        artifact = REPO_ROOT / args.artifact
        artifact.parent.mkdir(parents=True, exist_ok=True)
        artifact.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote {artifact.relative_to(REPO_ROOT)}")

    if args.json or not args.artifact:
        print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
