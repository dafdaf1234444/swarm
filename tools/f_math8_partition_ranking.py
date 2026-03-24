#!/usr/bin/env python3
"""Compare compaction rankings for F-MATH8.

The F-MATH8 question is whether the partition-function perspective is more
useful for compaction than simpler projections such as citation-only or
Sharpe-by-age ranking. This tool evaluates those rankings at a fixed token
compression target against the live lesson corpus.
"""

from __future__ import annotations

import argparse
import json
import math
import re
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LESSON_CACHE = ROOT / "experiments" / "compact-lesson-cache.json"
CITATION_CACHE = ROOT / "experiments" / "compact-citation-cache.json"
SESSION_LOG = ROOT / "memory" / "SESSION-LOG.md"
LESSONS_DIR = ROOT / "memory" / "lessons"

try:
    from swarm_io import session_number as _session_number
except ImportError:
    def _session_number() -> int:
        if SESSION_LOG.exists():
            matches = re.findall(r"^S(\d+)", SESSION_LOG.read_text(encoding="utf-8"), re.MULTILINE)
            if matches:
                return max(int(m) for m in matches)
        return 340


def _load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def _incoming_citations() -> Counter:
    citations = _load_json(CITATION_CACHE)
    incoming = Counter()
    for data in citations.values():
        if isinstance(data, dict) and isinstance(data.get("cites"), dict):
            for lid, count in data["cites"].items():
                if re.fullmatch(r"L-\d+", lid):
                    incoming[lid] += int(count)
    return incoming


def _lesson_session(text: str) -> int:
    match = re.search(r"\*{0,2}Session\*{0,2}:\s*\*{0,2}S(\d+)", text)
    return int(match.group(1)) if match else 0


def load_live_lessons() -> list[dict]:
    lesson_cache = _load_json(LESSON_CACHE)
    incoming = _incoming_citations()
    current_session = _session_number()

    lessons = []
    for lesson_path in sorted(LESSONS_DIR.glob("L-*.md")):
        lesson_id = lesson_path.stem
        cache_entry = lesson_cache.get(lesson_id, {})
        if isinstance(cache_entry, dict) and "tokens" in cache_entry and "session" in cache_entry:
            tokens = int(cache_entry["tokens"])
            session = int(cache_entry["session"])
        else:
            text = lesson_path.read_text(encoding="utf-8")
            tokens = max(len(text) // 4, 1)
            session = _lesson_session(text)

        age = max(current_session - session, 1)
        citations = int(incoming.get(lesson_id, 0))
        sharpe = citations / age
        # Exclude current-session lessons so the measurement does not grade the
        # report it just wrote. F-MATH8 is about selector quality on the
        # antecedent corpus, not the reflexive artifact of this replay itself.
        if session >= current_session:
            continue
        lessons.append(
            {
                "id": lesson_id,
                "tokens": tokens,
                "session": session,
                "age": age,
                "citations": citations,
                "sharpe": sharpe,
            }
        )
    return lessons


def _score_item(item: dict, strategy: str, beta: float) -> float:
    citations = item["citations"]
    tokens = max(item["tokens"], 1)
    age = max(item["age"], 1)

    if strategy == "citation_only":
        return float(citations)
    if strategy == "sharpe_only":
        return float(citations) / age
    if strategy == "z_partition":
        return ((citations + 1) ** beta) / tokens
    if strategy == "citation_density_oracle":
        return float(citations) / tokens
    raise ValueError(f"Unknown strategy: {strategy}")


def simulate_strategy(items: list[dict], strategy: str, beta: float, target_compression: float) -> dict:
    total_tokens = sum(item["tokens"] for item in items)
    total_citations = sum(item["citations"] for item in items)
    total_sharpe = sum(item["sharpe"] for item in items)
    total_z_mass = sum((item["citations"] + 1) ** beta for item in items)
    target_tokens = total_tokens * target_compression

    ordered = sorted(
        items,
        key=lambda item: (_score_item(item, strategy, beta), item["tokens"], item["id"]),
    )

    removed = []
    removed_tokens = 0
    removed_citations = 0
    removed_sharpe = 0.0
    removed_z_mass = 0.0
    for item in ordered:
        if removed_tokens >= target_tokens:
            break
        removed.append(item)
        removed_tokens += item["tokens"]
        removed_citations += item["citations"]
        removed_sharpe += item["sharpe"]
        removed_z_mass += (item["citations"] + 1) ** beta

    achieved = removed_tokens / total_tokens if total_tokens else 0.0
    citation_distortion = removed_citations / total_citations if total_citations else 0.0
    sharpe_distortion = removed_sharpe / total_sharpe if total_sharpe else 0.0
    z_distortion = removed_z_mass / total_z_mass if total_z_mass else 0.0

    return {
        "strategy": strategy,
        "removed_lessons": [item["id"] for item in removed[:20]],
        "removed_count": len(removed),
        "removed_tokens": removed_tokens,
        "achieved_compression": round(achieved, 4),
        "citation_distortion": round(citation_distortion, 4),
        "sharpe_distortion": round(sharpe_distortion, 4),
        "z_mass_distortion": round(z_distortion, 4),
        "mean_removed_citations": round(removed_citations / len(removed), 3) if removed else 0.0,
        "mean_removed_age": round(sum(item["age"] for item in removed) / len(removed), 3) if removed else 0.0,
    }


def compare_strategies(items: list[dict], beta: float, target_compression: float) -> dict:
    strategies = {}
    for strategy in (
        "z_partition",
        "sharpe_only",
        "citation_only",
        "citation_density_oracle",
    ):
        strategies[strategy] = simulate_strategy(items, strategy, beta, target_compression)

    winner = min(
        ("z_partition", "sharpe_only", "citation_only"),
        key=lambda name: strategies[name]["citation_distortion"],
    )
    z_vs_sharpe = (
        strategies["z_partition"]["citation_distortion"]
        - strategies["sharpe_only"]["citation_distortion"]
    )
    falsified = z_vs_sharpe > 0.05

    return {
        "winner": winner,
        "z_vs_sharpe_citation_gap": round(z_vs_sharpe, 4),
        "falsified": falsified,
        "strategies": strategies,
    }


def build_report(beta: float, target_compression: float) -> dict:
    items = load_live_lessons()
    comparison = compare_strategies(items, beta, target_compression)
    z_result = comparison["strategies"]["z_partition"]
    sharpe_result = comparison["strategies"]["sharpe_only"]
    citation_result = comparison["strategies"]["citation_only"]
    oracle_result = comparison["strategies"]["citation_density_oracle"]

    if comparison["falsified"]:
        verdict = "FALSIFIED"
        actual = (
            f"{verdict}: Z-based partition ranking underperformed Sharpe-only at "
            f"{target_compression:.0%} compression. Citation distortion: "
            f"Z={z_result['citation_distortion']:.1%}, "
            f"Sharpe={sharpe_result['citation_distortion']:.1%}, "
            f"citation-only={citation_result['citation_distortion']:.1%}, "
            f"oracle-density={oracle_result['citation_distortion']:.1%}. "
            f"Z lost to Sharpe by {comparison['z_vs_sharpe_citation_gap']:.1%}."
        )
        diff = (
            "Expected Z to match or beat simpler rankings. Instead it preserved citation "
            "utility worse than Sharpe-only by more than the 5% falsification margin, so "
            "the partition-function story stays descriptive rather than prescriptive for "
            "compaction selection."
        )
    else:
        beat_word = "beat" if comparison["winner"] == "z_partition" else "matched"
        verdict = "CONFIRMED" if comparison["winner"] == "z_partition" else "PARTIALLY CONFIRMED"
        actual = (
            f"{verdict}: Z-based partition ranking {beat_word} the projection baselines at "
            f"{target_compression:.0%} compression. Citation distortion: "
            f"Z={z_result['citation_distortion']:.1%}, "
            f"Sharpe={sharpe_result['citation_distortion']:.1%}, "
            f"citation-only={citation_result['citation_distortion']:.1%}, "
            f"oracle-density={oracle_result['citation_distortion']:.1%}."
        )
        diff = (
            "Expected Z to at least match the simpler projections. It did, which means the "
            "partition-function framing is not just post-hoc unification and can be treated "
            "as an executable compaction heuristic."
        )

    return {
        "experiment": "DOMEX-MATH-S527b",
        "frontier": "F-MATH8",
        "session": f"S{_session_number()}",
        "domain": "mathematics",
        "date": date.today().isoformat(),
        "expect": (
            "If the partition-function claim is structurally stronger than its projections, "
            "Z-based ranking at beta=2.0 will match or beat Sharpe-only and citation-only "
            "distortion at the same 10% compression target; otherwise the unification result "
            "stays descriptive only."
        ),
        "actual": actual,
        "diff": diff,
        "method": (
            "Live-corpus replay on current non-archived lessons, excluding current-session "
            "lessons so the metric does not grade the report that describes it. Each strategy "
            "removes the lowest-ranked lessons until 10% of tokens are freed. Primary score is "
            "citation distortion relative to the full corpus; Sharpe and partition-mass "
            "distortion are reported as secondary diagnostics. Z-ranking is interpreted as "
            "partition density ((citations+1)^beta)/tokens with beta=2.0."
        ),
        "parameters": {
            "beta": beta,
            "target_compression": target_compression,
            "lesson_count": len(items),
            "total_tokens": sum(item["tokens"] for item in items),
            "total_citations": sum(item["citations"] for item in items),
        },
        "comparison": comparison,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate F-MATH8 partition-function compaction ranking")
    parser.add_argument("--beta", type=float, default=2.0)
    parser.add_argument("--target-compression", type=float, default=0.10)
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()

    report = build_report(args.beta, args.target_compression)
    payload = json.dumps(report, indent=2)

    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(payload + "\n", encoding="utf-8")
    else:
        print(payload)


if __name__ == "__main__":
    main()
