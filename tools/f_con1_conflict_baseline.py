#!/usr/bin/env python3
"""Refresh the strict F-CON1 conflict baseline from current lane history."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from dataclasses import dataclass
from datetime import date
from pathlib import Path

try:
    from swarm_io import session_number
except ImportError:  # pragma: no cover
    session_number = None


REPO_ROOT = Path(__file__).resolve().parent.parent
LANE_FILES = (
    REPO_ROOT / "tasks" / "SWARM-LANES-ARCHIVE.md",
    REPO_ROOT / "tasks" / "SWARM-LANES.md",
)

STRICT_C1_PATTERNS = (
    re.compile(r"\bpre-?empt(?:ed)?\b.*\bconcurrent\b", re.IGNORECASE),
    re.compile(r"\bconcurrent\b.*\bpre-?empt(?:ed)?\b", re.IGNORECASE),
    re.compile(r"\bduplicate of\b", re.IGNORECASE),
    re.compile(r"\bconcurrent duplicate\b", re.IGNORECASE),
    re.compile(r"\bconcurrent session preempted\b", re.IGNORECASE),
    re.compile(r"\bsame finding\b.*\bconcurrent\b", re.IGNORECASE),
)


@dataclass
class LaneRow:
    lane_id: str
    session: int
    status: str
    etc: str
    note: str

    @property
    def text(self) -> str:
        return f"{self.etc} {self.note}".strip()


def _default_session() -> int:
    if session_number is not None:
        try:
            return int(session_number())
        except Exception:
            pass
    index_text = (REPO_ROOT / "memory" / "INDEX.md").read_text(encoding="utf-8", errors="replace")
    match = re.search(r"Sessions:\s*(\d+)", index_text)
    return int(match.group(1)) if match else 0


def parse_lane_rows() -> dict[str, LaneRow]:
    latest: dict[str, LaneRow] = {}
    for path in LANE_FILES:
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            if not line.startswith("|") or line.startswith("| Date") or line.startswith("|----"):
                continue
            cols = [c.strip() for c in line.split("|")]
            if len(cols) < 13:
                continue
            session_match = re.search(r"S?(\d+)", cols[3])
            latest[cols[2]] = LaneRow(
                lane_id=cols[2],
                session=int(session_match.group(1)) if session_match else 0,
                status=cols[11],
                etc=cols[10],
                note=cols[12],
            )
    return latest


def is_strict_c1(row: LaneRow) -> bool:
    text = row.text
    if "swarm evolution" in text.lower():
        return False
    return any(pattern.search(text) for pattern in STRICT_C1_PATTERNS)


def classify_abandonment(row: LaneRow) -> str:
    text = row.text.lower()
    if is_strict_c1(row):
        return "strict_c1_concurrent_duplicate"
    if "stale >3 sessions" in text or "no execution" in text or "pending" in text:
        return "stale_no_progress"
    if "session ended" in text or "session cycle complete" in text or "reopen via dispatch" in text:
        return "administrative_branch_lifecycle"
    if "swarm evolution" in text or "superseded" in text:
        return "evolutionary_supersession"
    return "other"


def load_prior_baseline(current_session: int) -> tuple[dict, str] | tuple[None, None]:
    candidates = []
    for path in sorted((REPO_ROOT / "experiments" / "conflict").glob("f-con1-baseline-s*.json")):
        match = re.search(r"[sS](\d{3,})", path.name)
        if match and int(match.group(1)) < current_session:
            candidates.append((int(match.group(1)), path))
    if not candidates:
        return None, None
    _, path = candidates[-1]
    return json.loads(path.read_text(encoding="utf-8")), str(path.relative_to(REPO_ROOT)).replace("\\", "/")


def build_report(current_session: int) -> dict:
    latest_rows = parse_lane_rows()
    rows = list(latest_rows.values())
    merged = sum(1 for row in rows if row.status == "MERGED")
    active = sum(1 for row in rows if row.status in {"ACTIVE", "READY", "CLAIMED", "BLOCKED"})
    productive = merged + active

    strict_c1_rows = [row for row in rows if is_strict_c1(row)]
    abandonment = Counter(
        classify_abandonment(row)
        for row in rows
        if row.status in {"ABANDONED", "SUPERSEDED"}
    )

    prior_report, prior_path = load_prior_baseline(current_session)
    prior_session = 0
    prior_rate = None
    prior_count = None
    prior_total = None
    if prior_report:
        prior_session_match = re.search(r"S?(\d+)", str(prior_report.get("session", "")))
        prior_session = int(prior_session_match.group(1)) if prior_session_match else 0
        prior_rate = prior_report.get("c1_duplicate_work", {}).get("rate_lane_level")
        prior_count = prior_report.get("c1_duplicate_work", {}).get("count_strict_c1")
        prior_total = prior_report.get("data", {}).get("total_unique_lanes")

    newer_rows = [row for row in rows if row.session > prior_session] if prior_session else []
    newer_strict = [row for row in newer_rows if is_strict_c1(row)]
    rate = (len(strict_c1_rows) / len(rows)) if rows else 0.0

    report = {
        "experiment": "F-CON1",
        "description": f"Strict C1 conflict rate rebaseline at N={len(rows)} lanes — S{current_session} refresh",
        "session": f"S{current_session}",
        "date": date.today().isoformat(),
        "method": (
            "Parse SWARM-LANES.md + SWARM-LANES-ARCHIVE.md; keep the latest row per lane ID. "
            "Strict C1 counts only explicit concurrent-duplicate work signals "
            "(pre-empted/preempted by concurrent work, duplicate-of, or equivalent same-task language). "
            "Exclude evolutionary supersession, stale/no-progress closures, branch lifecycle, and generic "
            "administrative cleanup."
        ),
        "data": {
            "total_unique_lanes": len(rows),
            "merged": merged,
            "abandoned": sum(1 for row in rows if row.status == "ABANDONED"),
            "superseded": sum(1 for row in rows if row.status == "SUPERSEDED"),
            "active": active,
            "productive": productive,
            "merge_rate": round((merged / productive), 4) if productive else None,
        },
        "c1_duplicate_work": {
            "rate_lane_level": round(rate, 4),
            "count_strict_c1": len(strict_c1_rows),
            "lanes": [f"{row.lane_id} ({row.note})" for row in strict_c1_rows],
            "since_prior_baseline": {
                "prior_session": f"S{prior_session}" if prior_session else None,
                "prior_path": prior_path,
                "newer_latest_rows": len(newer_rows),
                "new_strict_c1": len(newer_strict),
                "new_strict_lanes": [row.lane_id for row in newer_strict],
                "prior_rate": prior_rate,
                "prior_count": prior_count,
                "prior_total": prior_total,
            },
            "note": (
                "Strict C1 is the narrow concurrent-duplicate class, not general supersession or stale closures. "
                "This keeps the baseline aligned with L-1171's corrected methodology."
            ),
        },
        "abandonment_taxonomy": {
            "strict_c1_concurrent_duplicate": abandonment["strict_c1_concurrent_duplicate"],
            "administrative_branch_lifecycle": abandonment["administrative_branch_lifecycle"],
            "evolutionary_supersession": abandonment["evolutionary_supersession"],
            "stale_no_progress": abandonment["stale_no_progress"],
            "other": abandonment["other"],
            "total_abandoned_or_superseded": sum(abandonment.values()),
        },
        "actual": (
            f"Strict C1 rebaseline at S{current_session}: {len(strict_c1_rows)}/{len(rows)} latest lanes = "
            f"{rate:.4f}. Since the prior S{prior_session} baseline, {len(newer_strict)} new strict-C1 lanes were "
            f"found across {len(newer_rows)} newer latest rows."
        ) if prior_session else (
            f"Strict C1 rebaseline at S{current_session}: {len(strict_c1_rows)}/{len(rows)} latest lanes = {rate:.4f}."
        ),
        "diff": (
            f"Expected the baseline to stay near the prior {prior_rate:.4f} floor; observed {rate:.4f} "
            f"({len(strict_c1_rows)} lanes), a delta of {rate - float(prior_rate):+.4f}."
        ) if prior_rate is not None else (
            "First strict-C1 baseline for this methodology."
        ),
        "cites": ["L-297", "L-527", "L-820", "L-1171", "F-CON1"],
    }
    if prior_session:
        report["c1_duplicate_work"]["comparison"] = {
            "prior_session": f"S{prior_session}",
            "prior_rate": prior_rate,
            "prior_count": prior_count,
            "prior_total": prior_total,
            "delta_rate": round(rate - float(prior_rate), 4) if prior_rate is not None else None,
        }
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--session", type=int, default=_default_session(), help="Session number to stamp in output")
    parser.add_argument(
        "--output",
        default="",
        help="Write JSON report to this path (defaults to experiments/conflict/f-con1-baseline-s<session>.json)",
    )
    args = parser.parse_args()

    output = (Path(args.output) if args.output else REPO_ROOT / "experiments" / "conflict" / f"f-con1-baseline-s{args.session}.json").resolve()
    report = build_report(args.session)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(output.relative_to(REPO_ROOT.resolve()).as_posix())
    print(json.dumps(report["c1_duplicate_work"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
