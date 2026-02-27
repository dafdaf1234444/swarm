#!/usr/bin/env python3
"""F-EVO3: protocol mutation cadence vs. stability/throughput signals.

Builds a session-level baseline that links protocol mutation intensity
to quality and destabilization proxies (maintenance DUE/URGENT and validator
PASS/FAIL mentions from session narratives).
"""

from __future__ import annotations

import argparse
import json
import math
import re
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SESSION_TAG_RE = re.compile(r"\[S(\d+)\]")
SESSION_LINE_RE = re.compile(r"^\s*\|?\s*S(\d+)\b")

SIGNAL_PATTERNS = {
    "maintenance_due_mentions": re.compile(r"\bDUE\b", re.IGNORECASE),
    "maintenance_urgent_mentions": re.compile(r"\bURGENT\b", re.IGNORECASE),
    "maintenance_notice_mentions": re.compile(r"\bNOTICE-only\b|\bNOTICE\b", re.IGNORECASE),
    "validator_pass_mentions": re.compile(r"\bvalidator PASS\b|\bBeliefs PASS\b", re.IGNORECASE),
    "validator_fail_mentions": re.compile(r"\bvalidator FAIL\b|\bBeliefs FAIL\b", re.IGNORECASE),
}

PROTOCOL_FILES = [
    "SWARM.md",
    "beliefs/CORE.md",
    "tools/maintenance.py",
    "tools/check.sh",
    "tools/check.ps1",
    "tools/orient.py",
    "tools/orient.ps1",
]


def _safe_corr(xs: list[float], ys: list[float]) -> float | None:
    if len(xs) != len(ys) or len(xs) < 3:
        return None
    mx = sum(xs) / len(xs)
    my = sum(ys) / len(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    denx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    deny = math.sqrt(sum((y - my) ** 2 for y in ys))
    if denx == 0 or deny == 0:
        return None
    return num / (denx * deny)


def _avg(rows: list[dict], key: str) -> float | None:
    if not rows:
        return None
    return sum(float(r[key]) for r in rows) / len(rows)


def _round_or_none(value: float | None, digits: int = 4) -> float | None:
    return round(value, digits) if value is not None else None


def parse_protocol_mutations(protocol_files: list[str]) -> dict[int, dict]:
    """Return per-session mutation intensity for protocol files."""
    cmd = [
        "git",
        "log",
        "--no-merges",
        "--name-only",
        "--format=__COMMIT__%H|%s",
        "--",
        *protocol_files,
    ]
    raw = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=True).stdout.splitlines()
    per_session: dict[int, dict] = defaultdict(
        lambda: {"mutation_commits": 0, "files_touched": Counter(), "commit_hashes": []}
    )
    current_session: int | None = None
    current_hash: str | None = None

    for line in raw:
        if line.startswith("__COMMIT__"):
            payload = line[len("__COMMIT__") :]
            if "|" not in payload:
                current_session = None
                current_hash = None
                continue
            commit_hash, subject = payload.split("|", 1)
            m = SESSION_TAG_RE.search(subject)
            if not m:
                current_session = None
                current_hash = None
                continue
            current_session = int(m.group(1))
            current_hash = commit_hash
            per_session[current_session]["mutation_commits"] += 1
            per_session[current_session]["commit_hashes"].append(commit_hash)
            continue

        if current_session is None or current_hash is None:
            continue

        file_path = line.strip()
        if not file_path:
            continue
        per_session[current_session]["files_touched"][file_path] += 1

    return dict(per_session)


def parse_stability_signals(session_files: list[Path]) -> dict[int, dict]:
    """Extract maintenance/validator mentions from session narrative lines."""
    per_session: dict[int, dict] = defaultdict(
        lambda: {
            "line_hits": 0,
            "maintenance_due_mentions": 0,
            "maintenance_urgent_mentions": 0,
            "maintenance_notice_mentions": 0,
            "validator_pass_mentions": 0,
            "validator_fail_mentions": 0,
        }
    )

    for rel_path in session_files:
        full_path = ROOT / rel_path
        if not full_path.exists():
            continue
        for raw_line in full_path.read_text(encoding="utf-8", errors="replace").splitlines():
            m = SESSION_LINE_RE.search(raw_line)
            if not m:
                continue
            session = int(m.group(1))
            row = per_session[session]
            row["line_hits"] += 1
            for key, pattern in SIGNAL_PATTERNS.items():
                if pattern.search(raw_line):
                    row[key] += 1

    return dict(per_session)


def load_quality_signals() -> dict[int, dict]:
    """Use change_quality.py as source of session quality proxies."""
    sys.path.insert(0, str((ROOT / "tools").resolve()))
    from change_quality import extract_session_signals, get_commits, quality_score  # type: ignore

    raw_sessions = extract_session_signals(get_commits())
    result: dict[int, dict] = {}
    for session, sig in raw_sessions.items():
        commits = int(sig.get("commits", 0))
        overhead_commits = int(sig.get("overhead_commits", 0))
        result[session] = {
            "quality_score": float(quality_score(sig)),
            "overhead_ratio": (overhead_commits / commits) if commits else 0.0,
            "frontier_advances": int(sig.get("frontier_advances", 0)),
            "lessons_refd": len(sig.get("lessons", set())),
            "principles_refd": len(sig.get("principles", set())),
            "total_commits": commits,
        }
    return result


def build_report(
    *,
    protocol_files: list[str],
    mutation: dict[int, dict],
    stability: dict[int, dict],
    quality: dict[int, dict],
    analysis_start_session: int | None,
    analysis_end_session: int | None,
) -> dict:
    sessions = sorted(quality)
    if not sessions:
        raise RuntimeError("No quality sessions available from git log")

    start = analysis_start_session if analysis_start_session is not None else min(mutation or {sessions[0]: {}})
    end = analysis_end_session if analysis_end_session is not None else sessions[-1]
    rows = []
    for session in sessions:
        if session < start or session > end:
            continue
        q = quality[session]
        m = mutation.get(session, {"mutation_commits": 0, "files_touched": Counter(), "commit_hashes": []})
        s = stability.get(
            session,
            {
                "line_hits": 0,
                "maintenance_due_mentions": 0,
                "maintenance_urgent_mentions": 0,
                "maintenance_notice_mentions": 0,
                "validator_pass_mentions": 0,
                "validator_fail_mentions": 0,
            },
        )
        row = {
            "session": session,
            "protocol_mutation_commits": int(m["mutation_commits"]),
            "protocol_files_touched_unique": len(m["files_touched"]),
            "protocol_files_touched_total": int(sum(m["files_touched"].values())),
            "quality_score": round(float(q["quality_score"]), 4),
            "overhead_ratio": round(float(q["overhead_ratio"]), 4),
            "frontier_advances": int(q["frontier_advances"]),
            "lessons_refd": int(q["lessons_refd"]),
            "principles_refd": int(q["principles_refd"]),
            "total_commits": int(q["total_commits"]),
            "session_signal_lines": int(s["line_hits"]),
            "maintenance_due_mentions": int(s["maintenance_due_mentions"]),
            "maintenance_urgent_mentions": int(s["maintenance_urgent_mentions"]),
            "maintenance_notice_mentions": int(s["maintenance_notice_mentions"]),
            "validator_pass_mentions": int(s["validator_pass_mentions"]),
            "validator_fail_mentions": int(s["validator_fail_mentions"]),
        }
        row["destabilization_mentions"] = (
            row["maintenance_due_mentions"]
            + row["maintenance_urgent_mentions"]
            + row["validator_fail_mentions"]
        )
        row["has_due_or_urgent"] = 1 if (row["maintenance_due_mentions"] > 0 or row["maintenance_urgent_mentions"] > 0) else 0
        row["has_validator_fail"] = 1 if row["validator_fail_mentions"] > 0 else 0
        rows.append(row)

    if not rows:
        raise RuntimeError("No sessions in selected analysis window")

    recent = rows[-20:] if len(rows) > 20 else rows
    x = [float(r["protocol_mutation_commits"]) for r in rows]
    destabilization = [float(r["destabilization_mentions"]) for r in rows]
    due_or_urgent = [float(r["has_due_or_urgent"]) for r in rows]
    validator_fail = [float(r["has_validator_fail"]) for r in rows]
    quality_score = [float(r["quality_score"]) for r in rows]
    overhead = [float(r["overhead_ratio"]) for r in rows]
    frontier_adv = [float(r["frontier_advances"]) for r in rows]

    rx = [float(r["protocol_mutation_commits"]) for r in recent]
    rdestabilization = [float(r["destabilization_mentions"]) for r in recent]
    rdue_or_urgent = [float(r["has_due_or_urgent"]) for r in recent]
    rvalidator_fail = [float(r["has_validator_fail"]) for r in recent]
    rquality_score = [float(r["quality_score"]) for r in recent]
    roverhead = [float(r["overhead_ratio"]) for r in recent]
    rfrontier_adv = [float(r["frontier_advances"]) for r in recent]

    bins = {
        "zero_mutation": [r for r in rows if r["protocol_mutation_commits"] == 0],
        "single_mutation": [r for r in rows if r["protocol_mutation_commits"] == 1],
        "multi_mutation": [r for r in rows if r["protocol_mutation_commits"] >= 2],
    }

    protocol_file_touches = Counter()
    for data in mutation.values():
        protocol_file_touches.update(data["files_touched"])

    report = {
        "frontier_id": "F-EVO3",
        "session": 186,
        "created_on": str(date.today()),
        "protocol_files": protocol_files,
        "window": {
            "start_session": rows[0]["session"],
            "end_session": rows[-1]["session"],
            "session_count": len(rows),
        },
        "summary": {
            "mutation_sessions": sum(1 for r in rows if r["protocol_mutation_commits"] > 0),
            "non_mutation_sessions": sum(1 for r in rows if r["protocol_mutation_commits"] == 0),
            "sessions_with_due_or_urgent_mentions": sum(1 for r in rows if r["has_due_or_urgent"] > 0),
            "sessions_with_validator_fail_mentions": sum(1 for r in rows if r["has_validator_fail"] > 0),
            "top_protocol_files_by_touch": [
                {"path": path, "touches": touches} for path, touches in protocol_file_touches.most_common()
            ],
        },
        "correlation_global": {
            "mutation_vs_quality_score": _round_or_none(_safe_corr(x, quality_score)),
            "mutation_vs_overhead_ratio": _round_or_none(_safe_corr(x, overhead)),
            "mutation_vs_frontier_advances": _round_or_none(_safe_corr(x, frontier_adv)),
        },
        "correlation_stability_global": {
            "mutation_vs_destabilization_mentions": _round_or_none(_safe_corr(x, destabilization)),
            "mutation_vs_due_or_urgent_flag": _round_or_none(_safe_corr(x, due_or_urgent)),
            "mutation_vs_validator_fail_flag": _round_or_none(_safe_corr(x, validator_fail)),
        },
        "correlation_recent_window": {
            "window_size": len(recent),
            "mutation_vs_quality_score": _round_or_none(_safe_corr(rx, rquality_score)),
            "mutation_vs_overhead_ratio": _round_or_none(_safe_corr(rx, roverhead)),
            "mutation_vs_frontier_advances": _round_or_none(_safe_corr(rx, rfrontier_adv)),
            "mutation_vs_destabilization_mentions": _round_or_none(_safe_corr(rx, rdestabilization)),
            "mutation_vs_due_or_urgent_flag": _round_or_none(_safe_corr(rx, rdue_or_urgent)),
            "mutation_vs_validator_fail_flag": _round_or_none(_safe_corr(rx, rvalidator_fail)),
        },
        "bin_comparison": {
            name: {
                "sessions": len(group),
                "avg_quality": _round_or_none(_avg(group, "quality_score")),
                "avg_overhead": _round_or_none(_avg(group, "overhead_ratio")),
                "avg_frontier_adv": _round_or_none(_avg(group, "frontier_advances")),
                "avg_destabilization_mentions": _round_or_none(_avg(group, "destabilization_mentions")),
                "due_or_urgent_rate": _round_or_none(_avg(group, "has_due_or_urgent")),
                "validator_fail_rate": _round_or_none(_avg(group, "has_validator_fail")),
            }
            for name, group in bins.items()
        },
        "sessions": rows,
        "interpretation": {
            "baseline_note": (
                "Protocol mutation cadence is measured via commit touches on SWARM/CORE/maintenance/check/orient files. "
                "Destabilization proxies are session narrative mentions of DUE/URGENT and validator FAIL."
            ),
            "next_step": (
                "Replace narrative-mention proxies with structured maintenance output snapshots per session "
                "for stronger stability causality tests."
            ),
        },
    }
    return report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("experiments/evolution/f-evo3-protocol-cadence-s186.json"),
        help="Output JSON artifact path.",
    )
    parser.add_argument(
        "--session-files",
        nargs="+",
        default=["tasks/NEXT.md", "memory/SESSION-LOG.md"],
        help="Session narrative files used for stability signal extraction.",
    )
    parser.add_argument(
        "--start-session",
        type=int,
        default=None,
        help="Optional explicit start session for analysis window.",
    )
    parser.add_argument(
        "--end-session",
        type=int,
        default=None,
        help="Optional explicit end session for analysis window.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    mutation = parse_protocol_mutations(PROTOCOL_FILES)
    stability = parse_stability_signals([Path(p) for p in args.session_files])
    quality = load_quality_signals()
    report = build_report(
        protocol_files=PROTOCOL_FILES,
        mutation=mutation,
        stability=stability,
        quality=quality,
        analysis_start_session=args.start_session,
        analysis_end_session=args.end_session,
    )
    out_path = args.out if args.out.is_absolute() else ROOT / args.out
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    summary = {
        "out": str(out_path.relative_to(ROOT)),
        "window": report["window"],
        "correlation_global": report["correlation_global"],
        "correlation_stability_global": report["correlation_stability_global"],
        "correlation_recent_window": report["correlation_recent_window"],
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

