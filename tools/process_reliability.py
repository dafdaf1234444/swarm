#!/usr/bin/env python3
"""Process Reliability Tracker (F-EPIS1 reliabilism gap).

Measures truth-production rate per method, domain, and tool.
A lesson's "method" = its Confidence header (Measured, Theorized, etc.).
Reliability = 1 - (falsified lessons / total lessons) per method.

Usage:
    python3 tools/process_reliability.py              # summary report
    python3 tools/process_reliability.py --json       # JSON output
    python3 tools/process_reliability.py --detail     # per-lesson detail
"""

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

LESSON_DIR = Path("memory/lessons")
ARCHIVE_DIR = Path("memory/lessons/archive")


def parse_lesson(path: Path) -> dict | None:
    """Extract method, domain, session, and falsification status from a lesson."""
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return None

    lesson_id = path.stem  # e.g. L-1429

    # Extract confidence/method
    method = "unknown"
    m = re.search(r"Confidence:\s*(\S+)", text, re.IGNORECASE)
    if m:
        method = m.group(1).strip().lower().rstrip(",;")

    # Extract domain
    domain = "unknown"
    m = re.search(r"Domain:\s*([^\n|]+)", text, re.IGNORECASE)
    if m:
        domain = m.group(1).strip().lower().split(",")[0].strip()

    # Extract session
    session = 0
    m = re.search(r"Session:\s*S(\d+)", text)
    if m:
        session = int(m.group(1))

    # Extract evidence-type if present
    evidence_type = None
    m = re.search(r"Evidence-type:\s*(\S+)", text, re.IGNORECASE)
    if m:
        evidence_type = m.group(1).strip().lower()

    # Detect falsification: lesson contains FALSIFIED referring to its OWN claims
    # (not just mentioning that something else was falsified)
    title_line = text.split("\n")[0] if text.strip() else ""
    is_falsified = bool(re.search(r"FALSIFIED", title_line, re.IGNORECASE))

    # Also check for body-level self-falsification indicators
    body_falsified = bool(re.search(
        r"(claim|prediction|hypothesis|finding)\s+(was\s+)?FALSIFIED",
        text, re.IGNORECASE
    ))

    # Check if lesson has been superseded
    is_superseded = bool(re.search(
        r"(superseded|replaced|obsolete|withdrawn)", text, re.IGNORECASE
    ))

    # Extract level
    level = "unknown"
    m = re.search(r"Level:\s*(L\d)", text)
    if m:
        level = m.group(1)

    # Count citations (Cites: header)
    cites = []
    m = re.search(r"Cites:\s*([^\n]+)", text)
    if m:
        cites = re.findall(r"L-\d+", m.group(1))

    return {
        "id": lesson_id,
        "method": method,
        "domain": domain,
        "session": session,
        "evidence_type": evidence_type,
        "is_falsified": is_falsified or body_falsified,
        "is_superseded": is_superseded,
        "level": level,
        "n_cites": len(cites),
        "path": str(path),
    }


def normalize_method(method: str) -> str:
    """Normalize method names to canonical forms."""
    method = method.lower().strip()
    mapping = {
        "measured": "measured",
        "theorized": "theorized",
        "derived": "derived",
        "synthesized": "synthesized",
        "structural": "structural",
        "verified": "verified",
        "observed": "observed",
        "reasoned": "theorized",
        "designed": "measured",
        "built": "measured",
        "adversarial": "adversarial",
        "hypothesized": "theorized",
        "high": "measured",
        "medium": "measured",
        "low": "theorized",
    }
    return mapping.get(method, method)


def compute_reliability(lessons: list[dict]) -> dict:
    """Compute reliability metrics per method and domain."""
    # Per-method stats
    by_method = defaultdict(lambda: {"total": 0, "falsified": 0, "superseded": 0, "lessons": []})
    by_domain = defaultdict(lambda: {"total": 0, "falsified": 0, "superseded": 0})
    by_level = defaultdict(lambda: {"total": 0, "falsified": 0})

    for L in lessons:
        method = normalize_method(L["method"])
        domain = L["domain"]
        level = L["level"]

        by_method[method]["total"] += 1
        by_method[method]["lessons"].append(L["id"])
        if L["is_falsified"]:
            by_method[method]["falsified"] += 1
        if L["is_superseded"]:
            by_method[method]["superseded"] += 1

        by_domain[domain]["total"] += 1
        if L["is_falsified"]:
            by_domain[domain]["falsified"] += 1
        if L["is_superseded"]:
            by_domain[domain]["superseded"] += 1

        by_level[level]["total"] += 1
        if L["is_falsified"]:
            by_level[level]["falsified"] += 1

    # Compute reliability rates
    method_reliability = {}
    for method, stats in sorted(by_method.items(), key=lambda x: -x[1]["total"]):
        total = stats["total"]
        falsified = stats["falsified"]
        reliability = (total - falsified) / total if total > 0 else 0
        method_reliability[method] = {
            "total": total,
            "falsified": falsified,
            "superseded": stats["superseded"],
            "reliability": round(reliability, 3),
            "error_rate": round(falsified / total, 3) if total > 0 else 0,
        }

    domain_reliability = {}
    for domain, stats in sorted(by_domain.items(), key=lambda x: -x[1]["total"]):
        if stats["total"] < 3:
            continue  # skip tiny domains
        total = stats["total"]
        falsified = stats["falsified"]
        domain_reliability[domain] = {
            "total": total,
            "falsified": falsified,
            "reliability": round((total - falsified) / total, 3) if total > 0 else 0,
        }

    level_reliability = {}
    for level, stats in sorted(by_level.items()):
        total = stats["total"]
        falsified = stats["falsified"]
        level_reliability[level] = {
            "total": total,
            "falsified": falsified,
            "reliability": round((total - falsified) / total, 3) if total > 0 else 0,
        }

    return {
        "by_method": method_reliability,
        "by_domain": domain_reliability,
        "by_level": level_reliability,
        "total_lessons": len(lessons),
        "total_falsified": sum(1 for L in lessons if L["is_falsified"]),
        "total_superseded": sum(1 for L in lessons if L["is_superseded"]),
        "overall_reliability": round(
            (len(lessons) - sum(1 for L in lessons if L["is_falsified"])) / len(lessons), 3
        ) if lessons else 0,
    }


def print_report(results: dict, detail: bool = False):
    """Print human-readable reliability report."""
    total = results["total_lessons"]
    falsified = results["total_falsified"]
    superseded = results["total_superseded"]

    print(f"=== PROCESS RELIABILITY REPORT (N={total}) ===")
    print(f"Overall: {results['overall_reliability']:.1%} reliable "
          f"({falsified} falsified, {superseded} superseded)")
    print()

    # Method table
    print("--- By Method (Confidence type) ---")
    print(f"{'Method':<16} {'N':>5} {'Falsif':>6} {'Reliab':>7} {'Err%':>5}")
    print("-" * 42)
    methods = results["by_method"]
    for method, stats in sorted(methods.items(), key=lambda x: -x[1]["total"]):
        if stats["total"] < 2:
            continue
        flag = " ⚠" if stats["reliability"] < 0.90 else ""
        print(f"{method:<16} {stats['total']:>5} {stats['falsified']:>6} "
              f"{stats['reliability']:>6.1%} {stats['error_rate']:>4.1%}{flag}")

    # Domain table (top 15)
    print()
    print("--- By Domain (top 15 by N) ---")
    print(f"{'Domain':<25} {'N':>5} {'Falsif':>6} {'Reliab':>7}")
    print("-" * 45)
    domains = results["by_domain"]
    for domain, stats in sorted(domains.items(), key=lambda x: -x[1]["total"])[:15]:
        flag = " ⚠" if stats["reliability"] < 0.90 else ""
        print(f"{domain:<25} {stats['total']:>5} {stats['falsified']:>6} "
              f"{stats['reliability']:>6.1%}{flag}")

    # Level table
    print()
    print("--- By Level ---")
    print(f"{'Level':<8} {'N':>5} {'Falsif':>6} {'Reliab':>7}")
    print("-" * 28)
    for level, stats in sorted(results["by_level"].items()):
        flag = " ⚠" if stats["reliability"] < 0.90 else ""
        print(f"{level:<8} {stats['total']:>5} {stats['falsified']:>6} "
              f"{stats['reliability']:>6.1%}{flag}")

    # Variance analysis
    print()
    reliabilities = [s["reliability"] for s in methods.values() if s["total"] >= 5]
    if len(reliabilities) >= 2:
        max_r = max(reliabilities)
        min_r = min(reliabilities)
        ratio = max_r / min_r if min_r > 0 else float("inf")
        print(f"Method reliability range: {min_r:.1%}–{max_r:.1%} (ratio {ratio:.1f}x)")
    else:
        print("Insufficient methods (N>=5) for variance analysis")

    # Prescriptions
    print()
    print("--- Prescriptions ---")
    low_reliability = [(m, s) for m, s in methods.items()
                       if s["total"] >= 5 and s["reliability"] < 0.90]
    if low_reliability:
        for method, stats in low_reliability:
            print(f"  ⚠ {method}: {stats['reliability']:.1%} reliability (n={stats['total']}) "
                  f"— add verification step before committing {method}-based claims")
    else:
        print("  No methods below 90% reliability threshold (n>=5)")


def main():
    parser = argparse.ArgumentParser(description="Process Reliability Tracker")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--detail", action="store_true", help="Per-lesson detail")
    parser.add_argument("--save", action="store_true", help="Save to experiments/")
    parser.add_argument("--session", type=str, default=None, help="Session tag for --save")
    args = parser.parse_args()

    # Scan lessons
    lessons = []
    for path in sorted(LESSON_DIR.glob("L-*.md")):
        parsed = parse_lesson(path)
        if parsed:
            lessons.append(parsed)

    # Also scan archive
    if ARCHIVE_DIR.exists():
        for path in sorted(ARCHIVE_DIR.glob("L-*.md")):
            parsed = parse_lesson(path)
            if parsed:
                lessons.append(parsed)

    results = compute_reliability(lessons)

    if args.json:
        # Compact output
        output = {
            "total_lessons": results["total_lessons"],
            "total_falsified": results["total_falsified"],
            "overall_reliability": results["overall_reliability"],
            "by_method": results["by_method"],
            "by_domain": results["by_domain"],
            "by_level": results["by_level"],
        }
        print(json.dumps(output, indent=2))
    else:
        print_report(results, detail=args.detail)

    if args.save:
        session = args.session or "unknown"
        out_dir = Path("experiments/epistemology")
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"process-reliability-{session}.json"
        output = {
            "session": session,
            "total_lessons": results["total_lessons"],
            "total_falsified": results["total_falsified"],
            "overall_reliability": results["overall_reliability"],
            "by_method": results["by_method"],
            "by_domain": results["by_domain"],
            "by_level": results["by_level"],
        }
        out_path.write_text(json.dumps(output, indent=2))
        print(f"\nSaved: {out_path}")


if __name__ == "__main__":
    main()
