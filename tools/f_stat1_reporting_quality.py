#!/usr/bin/env python3
"""F-STAT1: baseline how well active lanes report actionable swarm state."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from statistics import fmean, median
from typing import Any

ACTIVE_STATUSES = {"CLAIMED", "ACTIVE", "BLOCKED", "READY"}
PLACEHOLDERS = {"", "-", "n/a", "na", "pending", "tbd", "unknown"}

REPORT_KEYS = (
    "capabilities",
    "intent",
    "progress",
    "available",
    "blocked",
    "next_step",
    "human_open_item",
)

KEY_WEIGHTS: dict[str, float] = {
    "capabilities": 0.20,
    "intent": 0.20,
    "progress": 0.15,
    "available": 0.15,
    "blocked": 0.10,
    "next_step": 0.10,
    "human_open_item": 0.10,
}

LANE_KEYS = (
    "date",
    "lane",
    "session",
    "agent",
    "branch",
    "pr",
    "model",
    "platform",
    "scope_key",
    "etc",
    "status",
    "notes",
)


def _is_placeholder(value: str) -> bool:
    return (value or "").strip().lower() in PLACEHOLDERS


def _parse_lane_tags(value: str) -> dict[str, str]:
    return {
        k.strip().lower(): v.strip()
        for k, v in re.findall(r"([A-Za-z][A-Za-z0-9_-]*)\s*=\s*([^\s,;|]+)", value or "")
    }


def _parse_session_number(raw: str) -> int | None:
    m = re.search(r"S(\d+)", raw or "")
    return int(m.group(1)) if m else None


def parse_lane_rows(text: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line.startswith("|") or re.match(r"^\|\s*(Date\s*\||[-: ]+\|)", line, re.IGNORECASE):
            continue
        parts = [part.strip() for part in line.strip("|").split("|")]
        if len(parts) < len(LANE_KEYS):
            continue
        row = dict(zip(LANE_KEYS, parts))
        row["status"] = row["status"].upper()
        rows.append(row)
    return rows


def latest_active_lanes(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    latest_by_lane: dict[str, dict[str, str]] = {}
    for row in rows:
        lane = row.get("lane", "").strip()
        if lane:
            latest_by_lane[lane] = row
    active = [row for row in latest_by_lane.values() if row.get("status", "") in ACTIVE_STATUSES]
    return sorted(active, key=lambda item: item.get("lane", ""))


def detect_reporting_fields(row: dict[str, str]) -> dict[str, bool]:
    tags = _parse_lane_tags(row.get("etc", ""))
    notes = (row.get("notes", "") or "").lower()
    status = (row.get("status", "") or "").upper()

    capabilities = (
        (not _is_placeholder(row.get("model", "")) and not _is_placeholder(row.get("platform", "")))
        or any(k in tags for k in ("setup", "capability", "capabilities", "tool", "tools"))
    )
    intent = (
        any(k in tags for k in ("intent", "objective", "goal", "frontier", "dispatch", "task"))
        or bool(re.search(r"\b(intent|objective|goal|frontier|queued|run|execute|measure|investigate)\b", notes))
    )
    progress = status in ACTIVE_STATUSES or bool(
        re.search(r"\b(added|ran|implemented|produced|verified|updated|queued|ready|fixed|executed)\b", notes)
    )
    available = (
        any(k in tags for k in ("available", "capacity", "availability", "ready"))
        or bool(re.search(r"\b(available|ready|queued)\b", notes))
        or status in {"CLAIMED", "ACTIVE", "READY"}
    )
    # Presence of blocked/human_open_item key counts even when value is "none":
    # that explicit "no blocker/no human ask" state is useful coordination signal.
    blocked = (
        "blocked" in tags
        or "blocker" in tags
        or status == "BLOCKED"
        or bool(re.search(r"\b(blocked|blocker|waiting|stuck|dependency|depends|requires)\b", notes))
        or bool(re.search(r"\b(no|none|unblocked)\s+(?:blocker|blockers)\b", notes))
    )
    next_step = (
        any(k in tags for k in ("next", "next_step", "action", "dispatch", "plan"))
        or bool(re.search(r"\b(next|follow-up|queued|run|execute|measure|rerun|investigate)\b", notes))
    )
    human_open_item = (
        "human_open_item" in tags
        or "human_open" in tags
        or bool(re.search(r"\bhuman[_ -]?open[_ -]?item\b", notes))
        or bool(re.search(r"\bhuman\b.*\b(needed|required|review|decision|ask|none|not needed)\b", notes))
    )

    return {
        "capabilities": capabilities,
        "intent": intent,
        "progress": progress,
        "available": available,
        "blocked": blocked,
        "next_step": next_step,
        "human_open_item": human_open_item,
    }


def detect_explicit_reporting_fields(row: dict[str, str]) -> dict[str, bool]:
    tags = _parse_lane_tags(row.get("etc", ""))

    return {
        "capabilities": (
            "setup" in tags
            and not _is_placeholder(row.get("model", ""))
            and not _is_placeholder(row.get("platform", ""))
        ),
        "intent": any(k in tags for k in ("intent", "objective", "goal", "frontier", "dispatch", "task")),
        "progress": any(k in tags for k in ("progress", "status_note", "evidence", "artifact")),
        "available": "available" in tags,
        "blocked": "blocked" in tags or "blocker" in tags,
        "next_step": any(k in tags for k in ("next_step", "next", "action", "plan")),
        "human_open_item": "human_open_item" in tags or "human_open" in tags,
    }


def reporting_score(fields: dict[str, bool]) -> float:
    return round(sum(KEY_WEIGHTS[k] for k in REPORT_KEYS if fields.get(k)), 4)


def build_report(active_rows: list[dict[str, str]]) -> dict[str, Any]:
    lane_rows: list[dict[str, Any]] = []
    key_counts = {key: 0 for key in REPORT_KEYS}
    explicit_key_counts = {key: 0 for key in REPORT_KEYS}
    scores: list[float] = []
    explicit_scores: list[float] = []
    contract_ready = 0
    explicit_contract_ready = 0
    sessions: list[int] = []

    for row in active_rows:
        fields = detect_reporting_fields(row)
        explicit_fields = detect_explicit_reporting_fields(row)
        score = reporting_score(fields)
        explicit_score = reporting_score(explicit_fields)
        missing = [key for key in REPORT_KEYS if not fields.get(key)]
        explicit_missing = [key for key in REPORT_KEYS if not explicit_fields.get(key)]
        present = [key for key in REPORT_KEYS if fields.get(key)]
        explicit_present = [key for key in REPORT_KEYS if explicit_fields.get(key)]
        if not missing:
            contract_ready += 1
        if not explicit_missing:
            explicit_contract_ready += 1
        for key in present:
            key_counts[key] += 1
        for key in explicit_present:
            explicit_key_counts[key] += 1
        scores.append(score)
        explicit_scores.append(explicit_score)
        session_no = _parse_session_number(row.get("session", ""))
        if session_no is not None:
            sessions.append(session_no)
        lane_rows.append(
            {
                "lane": row.get("lane", ""),
                "status": row.get("status", ""),
                "session": row.get("session", ""),
                "scope_key": row.get("scope_key", ""),
                "score": score,
                "explicit_score": explicit_score,
                "present_keys": present,
                "missing_keys": missing,
                "explicit_present_keys": explicit_present,
                "explicit_missing_keys": explicit_missing,
            }
        )

    lane_count = len(active_rows)
    coverage = {key: round(key_counts[key] / lane_count, 4) if lane_count else 0.0 for key in REPORT_KEYS}
    explicit_coverage = {
        key: round(explicit_key_counts[key] / lane_count, 4) if lane_count else 0.0
        for key in REPORT_KEYS
    }
    deficit_rank = sorted(coverage.items(), key=lambda item: (item[1], item[0]))
    explicit_deficit_rank = sorted(explicit_coverage.items(), key=lambda item: (item[1], item[0]))

    session_range = {
        "start": min(sessions) if sessions else None,
        "end": max(sessions) if sessions else None,
    }

    return {
        "lane_count": lane_count,
        "session_range": session_range,
        "mean_score": round(fmean(scores), 4) if scores else 0.0,
        "median_score": round(median(scores), 4) if scores else 0.0,
        "contract_ready_rate": round(contract_ready / lane_count, 4) if lane_count else 0.0,
        "explicit_mean_score": round(fmean(explicit_scores), 4) if explicit_scores else 0.0,
        "explicit_median_score": round(median(explicit_scores), 4) if explicit_scores else 0.0,
        "explicit_contract_ready_rate": (
            round(explicit_contract_ready / lane_count, 4) if lane_count else 0.0
        ),
        "key_coverage": coverage,
        "explicit_key_coverage": explicit_coverage,
        "lowest_coverage_keys": [name for name, _ in deficit_rank[:3]],
        "explicit_lowest_coverage_keys": [name for name, _ in explicit_deficit_rank[:3]],
        "recommended_contract": (
            "intent=... progress=... available=... blocked=none|... next_step=... "
            "human_open_item=none|HQ-N setup=... (plus model/platform columns)"
        ),
        "lanes": lane_rows,
    }


def run(lanes_path: Path, out_path: Path) -> dict[str, Any]:
    lanes_text = lanes_path.read_text(encoding="utf-8", errors="replace")
    rows = parse_lane_rows(lanes_text)
    active_rows = latest_active_lanes(rows)

    report = build_report(active_rows)
    result: dict[str, Any] = {
        "frontier_id": "F-STAT1",
        "title": "Agent reporting quality baseline for active lanes",
        "inputs": {
            "lanes_path": str(lanes_path).replace("\\", "/"),
            "active_statuses": sorted(ACTIVE_STATUSES),
            "report_keys": list(REPORT_KEYS),
            "weights": KEY_WEIGHTS,
        },
        "summary": {
            "active_lanes": report["lane_count"],
            "mean_score": report["mean_score"],
            "median_score": report["median_score"],
            "contract_ready_rate": report["contract_ready_rate"],
            "explicit_mean_score": report["explicit_mean_score"],
            "explicit_median_score": report["explicit_median_score"],
            "explicit_contract_ready_rate": report["explicit_contract_ready_rate"],
            "key_coverage": report["key_coverage"],
            "explicit_key_coverage": report["explicit_key_coverage"],
            "lowest_coverage_keys": report["lowest_coverage_keys"],
            "explicit_lowest_coverage_keys": report["explicit_lowest_coverage_keys"],
            "recommended_contract": report["recommended_contract"],
        },
        "session_range": report["session_range"],
        "lanes": report["lanes"],
        "interpretation": {
            "score_band": (
                "strong" if report["mean_score"] >= 0.85 else
                "partial" if report["mean_score"] >= 0.60 else
                "weak"
            ),
            "explicit_score_band": (
                "strong" if report["explicit_mean_score"] >= 0.85 else
                "partial" if report["explicit_mean_score"] >= 0.60 else
                "weak"
            ),
            "note": (
                "Inferred score can be optimistic from notes/status alone; use explicit score as the promotion "
                "gate and require blocked/human_open_item fields even when value is 'none'."
            ),
        },
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lanes", type=Path, default=Path("tasks/SWARM-LANES.md"))
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("experiments/statistics/f-stat1-reporting-quality-s186.json"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = run(args.lanes, args.out)
    summary = result["summary"]
    print(f"Wrote {args.out}")
    print(
        "active_lanes=",
        summary["active_lanes"],
        "mean_score=",
        summary["mean_score"],
        "contract_ready_rate=",
        summary["contract_ready_rate"],
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
