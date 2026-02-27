#!/usr/bin/env python3
"""F-CTL2: measure expect-act-diff to correction latency from session evidence."""

from __future__ import annotations

import argparse
import json
import math
import re
from datetime import datetime, timezone
from pathlib import Path
from statistics import fmean, median
from typing import Any

import change_quality as cq

REPO_ROOT = Path(__file__).resolve().parent.parent

EXPECT_RE = re.compile(
    r"\b(expect(?:ation|ed|ing|[- ]next)?|predict(?:ion|ed|s)?)\b|\bF123\b",
    re.IGNORECASE,
)
LARGE_DIFF_RE = re.compile(
    r"\b(diff|drift|mismatch|wrong|fail(?:ed|ure)?|refut(?:ed|e)|challenge|debt|gap|stale|collision|corrupt(?:ion)?)\b",
    re.IGNORECASE,
)
NO_EXPECT_RE = re.compile(r"\b(?:no|without)\s+expect(?:ation|ed|ing|[- ]next)?\b", re.IGNORECASE)
NO_LARGE_DIFF_RE = re.compile(
    r"\b(?:no|without)\s+(?:diff|drift|mismatch|wrong|fail(?:ed|ure)?|refut(?:ed|e)|challenge|debt|gap|stale|collision|corrupt(?:ion)?)\b",
    re.IGNORECASE,
)
CORRECTION_RE = re.compile(
    r"\b(fix(?:ed)?|repair(?:ed)?|correct(?:ed)?|clear(?:ed)?|resolve(?:d)?|sync(?:_state|ed)?|revalidat(?:e|ed)|harden(?:ed)?|restore(?:d)?|pass(?:ed)?\b)\b",
    re.IGNORECASE,
)

ID_RE = re.compile(r"\b(F(?:-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*|\d+(?:-[A-Za-z0-9]+)?|123)|L-\d+|P-\d+|PHIL-\d+)\b", re.IGNORECASE)


def _session_text(sig: dict[str, Any]) -> str:
    return " | ".join(sig.get("msgs", []))


def extract_anchors(text: str) -> list[str]:
    anchors = {m.group(1).upper() for m in ID_RE.finditer(text)}
    if "EXPECT-NEXT" in text.upper():
        anchors.add("EXPECT-NEXT")
    return sorted(anchors)


def is_diff_event(text: str) -> bool:
    if NO_EXPECT_RE.search(text) or NO_LARGE_DIFF_RE.search(text):
        return False
    return bool(EXPECT_RE.search(text) and LARGE_DIFF_RE.search(text))


def is_correction_event(text: str) -> bool:
    return bool(CORRECTION_RE.search(text))


def _anchor_overlap(anchors: list[str], text: str) -> bool:
    if not anchors:
        return True
    upper = text.upper()
    return any(anchor in upper for anchor in anchors)


def build_session_rows(sessions_data: dict[int, dict[str, Any]], session_min: int) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for session in sorted(s for s in sessions_data if s >= session_min):
        text = _session_text(sessions_data[session])
        rows.append(
            {
                "session": session,
                "text": text,
                "anchors": extract_anchors(text),
                "is_diff_event": is_diff_event(text),
                "is_correction_event": is_correction_event(text),
            }
        )
    return rows


def measure_latency(session_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []

    for i, row in enumerate(session_rows):
        if not row.get("is_diff_event"):
            continue

        anchors = row.get("anchors", [])
        matched: dict[str, Any] | None = None
        anchor_matched = False

        for candidate in session_rows[i + 1:]:
            if candidate.get("is_correction_event") and _anchor_overlap(anchors, candidate.get("text", "")):
                matched = candidate
                anchor_matched = True
                break

        if matched is None:
            for candidate in session_rows[i + 1:]:
                if candidate.get("is_correction_event"):
                    matched = candidate
                    break

        events.append(
            {
                "event_session": row["session"],
                "anchors": anchors,
                "matched_correction_session": matched["session"] if matched else None,
                "lag_sessions": (matched["session"] - row["session"]) if matched else None,
                "anchor_matched": anchor_matched if matched else False,
                "event_excerpt": row.get("text", "")[:220],
                "correction_excerpt": (matched.get("text", "")[:220] if matched else ""),
            }
        )

    return events


def _percentile(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    idx = max(0, min(len(ordered) - 1, math.ceil(pct * len(ordered)) - 1))
    return float(ordered[idx])


def summarize(events: list[dict[str, Any]]) -> dict[str, Any]:
    resolved = [e for e in events if e["lag_sessions"] is not None]
    unresolved = [e for e in events if e["lag_sessions"] is None]
    lags = [float(e["lag_sessions"]) for e in resolved]

    return {
        "diff_events_total": len(events),
        "resolved_events": len(resolved),
        "unresolved_events": len(unresolved),
        "anchor_matched_events": sum(1 for e in resolved if e.get("anchor_matched")),
        "mean_lag_sessions": round(fmean(lags), 4) if lags else 0.0,
        "median_lag_sessions": round(median(lags), 4) if lags else 0.0,
        "p90_lag_sessions": round(_percentile(lags, 0.9), 4) if lags else 0.0,
        "within_1_session_rate": round(sum(1 for x in lags if x <= 1.0) / len(lags), 4) if lags else 0.0,
    }


def simulate_auto_routing(events: list[dict[str, Any]], route_after_sessions: int) -> dict[str, Any]:
    route_after_sessions = max(0, int(route_after_sessions))
    lags = [int(e["lag_sessions"]) for e in events if e.get("lag_sessions") is not None]
    if not lags:
        return {
            "policy": {"route_after_sessions": route_after_sessions},
            "eligible_events": 0,
            "baseline_mean_lag": 0.0,
            "projected_mean_lag": 0.0,
            "estimated_mean_reduction": 0.0,
        }

    projected = [min(lag, route_after_sessions) for lag in lags]
    return {
        "policy": {
            "route_after_sessions": route_after_sessions,
            "rule": "If lag exceeds threshold, emit required follow-up for next session.",
        },
        "eligible_events": sum(1 for lag in lags if lag > route_after_sessions),
        "baseline_mean_lag": round(fmean(lags), 4),
        "projected_mean_lag": round(fmean(projected), 4),
        "estimated_mean_reduction": round(fmean(lags) - fmean(projected), 4),
    }


def run(session_min: int, out_path: Path, route_after_sessions: int) -> dict[str, Any]:
    commits = cq.get_commits()
    sessions_data = cq.extract_session_signals(commits)
    if not sessions_data:
        raise ValueError("no session data found in git history")

    rows = build_session_rows(sessions_data, session_min=session_min)
    if not rows:
        raise ValueError("no sessions after session-min filter")

    events = measure_latency(rows)
    summary = summarize(events)
    auto_routing = simulate_auto_routing(events, route_after_sessions=route_after_sessions)

    result = {
        "frontier_id": "F-CTL2",
        "title": "Expect-act-diff to correction latency baseline",
        "session_filter_min": session_min,
        "session_range": {"start": rows[0]["session"], "end": rows[-1]["session"]},
        "classification": {
            "diff_event_rule": "expectation signal + large-diff signal in session commit text",
            "correction_rule": "repair/sync/resolve/pass signal in session commit text",
            "anchor_linking": "prefer matching F/L/P/PHIL anchors; fallback to next correction event if no anchor match",
        },
        "summary": summary,
        "auto_routing": auto_routing,
        "events_sample": events[:30],
        "interpretation": {
            "caveat": (
                "Signals are inferred from commit messages, so silent or differently-worded corrections "
                "can inflate measured lag."
            ),
            "direction": (
                "healthy" if summary["mean_lag_sessions"] <= 1.5 and summary["unresolved_events"] == 0 else "attention-needed"
            ),
        },
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--session-min",
        type=int,
        default=150,
        help="Minimum session to include (default: 150)",
    )
    p.add_argument(
        "--out",
        type=Path,
        default=Path("experiments/control-theory/f-ctl2-diff-latency-s186.json"),
        help="Output artifact path",
    )
    p.add_argument(
        "--route-after-sessions",
        type=int,
        default=1,
        help="Auto-routing threshold for replay simulation",
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()
    result = run(
        session_min=args.session_min,
        out_path=args.out,
        route_after_sessions=args.route_after_sessions,
    )
    s = result["summary"]
    auto = result["auto_routing"]
    print(f"Wrote {args.out}")
    print(
        "events=",
        s["diff_events_total"],
        "resolved=",
        s["resolved_events"],
        "mean_lag=",
        s["mean_lag_sessions"],
        "projected_mean=",
        auto["projected_mean_lag"],
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
