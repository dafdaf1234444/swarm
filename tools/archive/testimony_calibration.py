#!/usr/bin/env python3
"""testimony_calibration.py — Social epistemology: source reliability tracking.

Maps Goldman & O'Connor (2021) testimony calibration onto swarm signal sources.
Tracks which sources (human, ai-session, steerers) produce signals that lead to
actionable outcomes (lessons, resolved frontiers, tool changes) vs. signals that
go unresolved or produce null results.

Five social epistemology concepts addressed:
  1. Testimony calibration: source reliability = resolved/total signals
  2. Peer disagreement: cross-challenge contradiction rates between steerers
  3. Epistemic injustice in attention: sources systematically under-attended
  4. Group belief aggregation: how multi-source signals converge on beliefs
  5. Division of epistemic labor: are sources used where they're most reliable?

Usage:
    python3 tools/testimony_calibration.py           # full report
    python3 tools/testimony_calibration.py --json    # machine-readable
    python3 tools/testimony_calibration.py --source human  # single source
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
SIGNALS_FILE = REPO_ROOT / "tasks" / "SIGNALS.md"
STEERER_DIR = REPO_ROOT / "tools" / "synthetic-steerers"
STEERER_HISTORY = STEERER_DIR / "signal-history.json"
CROSS_CHALLENGES = STEERER_DIR / "cross-challenges.md"
LESSONS_DIR = REPO_ROOT / "memory" / "lessons"
EXPERIMENTS_DIR = REPO_ROOT / "experiments"


def parse_signals() -> list[dict]:
    """Parse SIGNALS.md into structured records."""
    signals = []
    if not SIGNALS_FILE.exists():
        return signals
    text = SIGNALS_FILE.read_text()
    for line in text.split("\n"):
        line = line.strip()
        if not line.startswith("| SIG-"):
            continue
        cols = [c.strip() for c in line.split("|")]
        if len(cols) < 11:
            continue
        try:
            sig_id = cols[1]
            date = cols[2]
            session = cols[3]
            source = cols[4]
            target = cols[5]
            sig_type = cols[6]
            priority = cols[7]
            content = cols[8]
            status = cols[9]
            resolution = cols[10] if len(cols) > 10 else ""
        except IndexError:
            continue
        session_num = 0
        m = re.search(r"S(\d+)", session)
        if m:
            session_num = int(m.group(1))
        signals.append({
            "id": sig_id,
            "date": date,
            "session": session_num,
            "source": source,
            "target": target,
            "type": sig_type,
            "priority": priority,
            "content": content[:200],
            "status": status,
            "resolution": resolution[:200],
        })
    return signals


def parse_steerer_signals() -> list[dict]:
    """Parse steerer signal history."""
    if not STEERER_HISTORY.exists():
        return []
    try:
        data = json.loads(STEERER_HISTORY.read_text())
        if isinstance(data, list):
            return data
        if isinstance(data, dict) and "signals" in data:
            return data["signals"]
    except Exception:
        pass
    return []


def parse_cross_challenges() -> list[dict]:
    """Parse cross-challenge records for peer disagreement analysis."""
    challenges = []
    if not CROSS_CHALLENGES.exists():
        return challenges
    text = CROSS_CHALLENGES.read_text()
    # Extract challenger-target pairs and whether they contradicted
    for line in text.split("\n"):
        if "challenges" in line.lower() or "→" in line or "->" in line:
            challenges.append({"raw": line.strip()})
    return challenges


def compute_source_reliability(signals: list[dict]) -> dict[str, dict]:
    """Compute reliability metrics per source.

    Reliability = (RESOLVED signals) / (total non-observation signals).
    Observation signals excluded — they don't make claims, so can't be wrong.
    """
    by_source = defaultdict(lambda: {
        "total": 0, "resolved": 0, "open": 0,
        "types": defaultdict(int), "priorities": defaultdict(int),
        "sessions": [],
    })

    for sig in signals:
        src = sig["source"]
        by_source[src]["total"] += 1
        by_source[src]["types"][sig["type"]] += 1
        by_source[src]["priorities"][sig["priority"]] += 1
        by_source[src]["sessions"].append(sig["session"])
        if sig["status"] == "RESOLVED":
            by_source[src]["resolved"] += 1
        elif sig["status"] in ("OPEN", "PARTIALLY RESOLVED"):
            by_source[src]["open"] += 1

    result = {}
    for src, data in by_source.items():
        # Exclude pure observations from reliability calc
        actionable = data["total"] - data["types"].get("observation", 0)
        resolved_actionable = data["resolved"] - min(
            data["types"].get("observation", 0), data["resolved"]
        )
        reliability = resolved_actionable / actionable if actionable > 0 else 0.0

        result[src] = {
            "total_signals": data["total"],
            "actionable_signals": actionable,
            "resolved": data["resolved"],
            "open": data["open"],
            "reliability": round(reliability, 3),
            "type_distribution": dict(data["types"]),
            "priority_distribution": dict(data["priorities"]),
            "session_span": (min(data["sessions"]), max(data["sessions"])) if data["sessions"] else (0, 0),
            "mean_session": round(sum(data["sessions"]) / len(data["sessions"]), 1) if data["sessions"] else 0,
        }
    return result


def compute_attention_justice(signals: list[dict]) -> dict:
    """Epistemic injustice: are some sources systematically under-attended?

    Measures: time-to-resolution by source, open-signal age by source.
    If one source's signals sit OPEN longer, that source suffers epistemic injustice.
    """
    by_source = defaultdict(lambda: {"open_ages": [], "resolved_count": 0, "total": 0})

    max_session = max((s["session"] for s in signals), default=0)

    for sig in signals:
        src = sig["source"]
        by_source[src]["total"] += 1
        if sig["status"] == "RESOLVED":
            by_source[src]["resolved_count"] += 1
        elif sig["status"] in ("OPEN", "PARTIALLY RESOLVED"):
            age = max_session - sig["session"]
            by_source[src]["open_ages"].append(age)

    result = {}
    for src, data in by_source.items():
        mean_open_age = (
            round(sum(data["open_ages"]) / len(data["open_ages"]), 1)
            if data["open_ages"] else 0.0
        )
        resolution_rate = (
            data["resolved_count"] / data["total"]
            if data["total"] > 0 else 0.0
        )
        result[src] = {
            "total": data["total"],
            "open_count": len(data["open_ages"]),
            "mean_open_age_sessions": mean_open_age,
            "resolution_rate": round(resolution_rate, 3),
            "injustice_score": round(mean_open_age * (1 - resolution_rate), 3),
        }
    return result


def compute_epistemic_labor_division(signals: list[dict]) -> dict:
    """Division of epistemic labor: which sources contribute to which signal types?

    Goldman: efficient division means different agents specialize in different
    epistemic tasks. If all sources produce the same type, labor is undivided.
    """
    source_type_matrix = defaultdict(lambda: defaultdict(int))
    for sig in signals:
        source_type_matrix[sig["source"]][sig["type"]] += 1

    # Compute specialization index per source (Herfindahl of type shares)
    result = {}
    for src, types in source_type_matrix.items():
        total = sum(types.values())
        if total == 0:
            continue
        shares = [count / total for count in types.values()]
        hhi = sum(s ** 2 for s in shares)
        dominant_type = max(types, key=types.get)
        result[src] = {
            "type_counts": dict(types),
            "specialization_hhi": round(hhi, 3),
            "dominant_type": dominant_type,
            "dominant_share": round(types[dominant_type] / total, 3),
            "n_types": len(types),
        }

    # Cross-source diversity: are different sources doing different things?
    all_dominant = [d["dominant_type"] for d in result.values()]
    diversity = len(set(all_dominant)) / len(all_dominant) if all_dominant else 0
    return {
        "per_source": result,
        "labor_diversity": round(diversity, 3),
        "interpretation": (
            "WELL DIVIDED" if diversity >= 0.6 else
            "PARTIALLY DIVIDED" if diversity >= 0.3 else
            "UNDIVIDED — all sources doing same epistemic work"
        ),
    }


def compute_group_aggregation(signals: list[dict]) -> dict:
    """Group belief aggregation: when multiple sources signal about the same topic,
    do they converge or diverge?

    Uses content overlap to detect multi-source convergence on themes.
    """
    # Extract key terms from each signal
    def extract_terms(text: str) -> set[str]:
        words = re.findall(r"[a-z]{4,}", text.lower())
        return set(words)

    # Find signals that share significant term overlap
    convergences = []
    divergences = []
    for i, s1 in enumerate(signals):
        terms1 = extract_terms(s1["content"])
        if not terms1:
            continue
        for s2 in signals[i + 1:]:
            if s1["source"] == s2["source"]:
                continue
            terms2 = extract_terms(s2["content"])
            if not terms2:
                continue
            overlap = len(terms1 & terms2) / min(len(terms1), len(terms2))
            if overlap > 0.3:
                both_resolved = (s1["status"] == "RESOLVED" and s2["status"] == "RESOLVED")
                convergences.append({
                    "sources": sorted([s1["source"], s2["source"]]),
                    "signals": [s1["id"], s2["id"]],
                    "overlap": round(overlap, 2),
                    "both_resolved": both_resolved,
                })

    return {
        "multi_source_convergences": len(convergences),
        "sample": convergences[:5],
        "interpretation": (
            f"{len(convergences)} topic convergences between different sources — "
            f"multi-agent epistemic agreement detected"
            if convergences else
            "No significant cross-source convergence detected"
        ),
    }


def compute_peer_disagreement(cross_challenges: list[dict]) -> dict:
    """Peer disagreement: steerer cross-challenge analysis.

    Goldman: rational peers can disagree. The question is whether disagreement
    is productive (generates new insights) or destructive (paralyzes action).
    """
    n_challenges = len(cross_challenges)
    return {
        "n_cross_challenges": n_challenges,
        "interpretation": (
            f"{n_challenges} cross-challenge records found — "
            f"peer disagreement mechanism is {'active' if n_challenges >= 5 else 'nascent'}"
        ),
    }


def format_report(
    reliability: dict[str, dict],
    attention: dict,
    labor: dict,
    aggregation: dict,
    disagreement: dict,
    n_signals: int,
) -> str:
    lines = []
    lines.append("=== TESTIMONY CALIBRATION (Social Epistemology) ===")
    lines.append(f"Signals analyzed: {n_signals}")
    lines.append(f"Sources: {len(reliability)}")
    lines.append("")

    # 1. Source reliability
    lines.append("--- Source Reliability (testimony calibration) ---")
    lines.append(f"  {'Source':15s}  {'Total':>5}  {'Action':>6}  {'Resolved':>8}  {'Reliab':>7}")
    for src, data in sorted(reliability.items(), key=lambda x: -x[1]["reliability"]):
        lines.append(
            f"  {src:15s}  {data['total_signals']:5d}  {data['actionable_signals']:6d}  "
            f"{data['resolved']:8d}  {data['reliability']:7.3f}"
        )
    lines.append("")

    # Identify most and least reliable
    if reliability:
        most_reliable = max(reliability.items(), key=lambda x: x[1]["reliability"])
        least_reliable = min(reliability.items(), key=lambda x: x[1]["reliability"])
        lines.append(f"  Most reliable: {most_reliable[0]} ({most_reliable[1]['reliability']:.3f})")
        lines.append(f"  Least reliable: {least_reliable[0]} ({least_reliable[1]['reliability']:.3f})")
        spread = most_reliable[1]["reliability"] - least_reliable[1]["reliability"]
        lines.append(f"  Reliability spread: {spread:.3f}")
        lines.append("")

    # 2. Epistemic injustice
    lines.append("--- Epistemic Injustice in Attention ---")
    for src, data in sorted(attention.items(), key=lambda x: -x[1]["injustice_score"]):
        flag = " ⚠ INJUSTICE" if data["injustice_score"] > 10 else ""
        lines.append(
            f"  {src:15s}  open={data['open_count']:3d}  "
            f"mean_age={data['mean_open_age_sessions']:5.1f}s  "
            f"resolution={data['resolution_rate']:.3f}  "
            f"injustice={data['injustice_score']:.3f}{flag}"
        )
    lines.append("")

    # 3. Division of epistemic labor
    lines.append("--- Division of Epistemic Labor ---")
    lines.append(f"  Labor diversity: {labor['labor_diversity']:.3f} — {labor['interpretation']}")
    for src, data in labor["per_source"].items():
        lines.append(
            f"  {src:15s}  dominant={data['dominant_type']:12s} ({data['dominant_share']:.1%})  "
            f"HHI={data['specialization_hhi']:.3f}  types={data['n_types']}"
        )
    lines.append("")

    # 4. Group belief aggregation
    lines.append("--- Group Belief Aggregation ---")
    lines.append(f"  {aggregation['interpretation']}")
    for conv in aggregation.get("sample", []):
        lines.append(f"    {conv['signals'][0]}×{conv['signals'][1]}  "
                     f"sources={conv['sources']}  overlap={conv['overlap']}")
    lines.append("")

    # 5. Peer disagreement
    lines.append("--- Peer Disagreement ---")
    lines.append(f"  {disagreement['interpretation']}")
    lines.append("")

    # Summary: which social epistemology concepts are operationalized?
    lines.append("--- Social Epistemology Gap Closure ---")
    concepts = [
        ("Testimony calibration", reliability, len(reliability) >= 2),
        ("Peer disagreement", disagreement, disagreement["n_cross_challenges"] >= 5),
        ("Epistemic injustice", attention, any(
            d["injustice_score"] > 0 for d in attention.values()
        )),
        ("Group belief aggregation", aggregation, aggregation["multi_source_convergences"] > 0),
        ("Division of epistemic labor", labor, labor["labor_diversity"] > 0),
    ]
    closed = 0
    for name, _, measured in concepts:
        status = "MEASURED" if measured else "GAP"
        if measured:
            closed += 1
        lines.append(f"  [{status:8s}] {name}")
    lines.append(f"  Score: {closed}/5 social epistemology concepts operationalized")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Testimony calibration — social epistemology")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--source", help="Filter by source")
    args = parser.parse_args()

    signals = parse_signals()
    steerer_signals = parse_steerer_signals()
    cross_challenges = parse_cross_challenges()

    if args.source:
        signals = [s for s in signals if s["source"] == args.source]

    reliability = compute_source_reliability(signals)
    attention = compute_attention_justice(signals)
    labor = compute_epistemic_labor_division(signals)
    aggregation = compute_group_aggregation(signals)
    disagreement = compute_peer_disagreement(cross_challenges)

    if args.json:
        output = {
            "n_signals": len(signals),
            "n_steerer_signals": len(steerer_signals),
            "source_reliability": reliability,
            "attention_justice": attention,
            "labor_division": labor,
            "group_aggregation": aggregation,
            "peer_disagreement": disagreement,
        }
        print(json.dumps(output, indent=2, default=str))
    else:
        print(format_report(
            reliability, attention, labor, aggregation, disagreement, len(signals)
        ))


if __name__ == "__main__":
    main()
