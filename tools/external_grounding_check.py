#!/usr/bin/env python3
"""external_grounding_check.py — Detect lessons without external grounding (F-GND1, L-1192, L-1125).

Scans lesson files for external references: URLs, paper citations, named external
benchmarks, DOIs, or other non-swarm evidence sources. Emits NOTICE when a lesson
has zero external references — structural pressure toward grounded knowledge.

Usage:
  python3 tools/external_grounding_check.py                    # scan all recent
  python3 tools/external_grounding_check.py --staged           # check.sh hook mode
  python3 tools/external_grounding_check.py --baseline N       # measure last N lessons
  python3 tools/external_grounding_check.py --json             # machine-readable

Related: F-GND1, L-1192, L-1125, L-1118, L-601, F-COMP1, grounding_audit.py
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
LESSON_DIR = ROOT / "memory" / "lessons"

# Patterns that indicate external grounding (not self-referential)
EXTERNAL_PATTERNS = [
    (r'https?://\S+', "URL"),
    (r'arXiv[:\s]\d{4}\.\d+', "arXiv"),
    (r'doi[:\s]10\.\d{4,}', "DOI"),
    (r'\b\w+ et al\.?\b', "paper citation"),
    (r'\b(?:IEEE|ACM|NeurIPS|NIPS|ICML|ICLR|AAAI|Nature|Science|PNAS|OSDI|SOSP)\b', "venue"),
    (r'\b(?:MMLU|HumanEval|GPQA|SWE-bench|ARC|HellaSwag|TruthfulQA|BigBench)\b', "benchmark"),
    (r'\b(?:Kauffman|Anderson|Shannon|Bayes|Pareto|Zipf|Lorenz|Nash|von Neumann)\b', "named theory"),
    (r'\bISBN\s*[\d-]+', "ISBN"),
    (r'\bISSN\s*[\d-]+', "ISSN"),
    (r'\b(?:Wikipedia|Stack Overflow|GitHub\.com|arxiv\.org)\b', "external source"),
    (r'\b(?:Jepsen|TPC-C|SPEC|MLPerf)\b', "external benchmark"),
]

# Patterns that are self-referential (swarm-internal)
INTERNAL_PATTERNS = re.compile(
    r'\b(?:L-\d+|P-\d+|B-\w+|F-\w+|PHIL-\d+|ISO-\d+|SIG-\d+|FM-\d+|S\d{3,4}|'
    r'tools/\w+|orient\.py|compact\.py|check\.sh|CORE\.md|INDEX\.md|SWARM\.md|'
    r'FRONTIER\.md|LANES\.md|COLONY\.md|DOMAIN\.md)\b'
)


def scan_lesson(path: Path) -> dict:
    """Scan a single lesson for external references."""
    try:
        content = path.read_text(encoding="utf-8")
    except Exception:
        return {"file": path.name, "error": "unreadable"}

    external_refs = []
    for pattern, label in EXTERNAL_PATTERNS:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            external_refs.append({"type": label, "count": len(matches), "examples": matches[:2]})

    internal_refs = INTERNAL_PATTERNS.findall(content)

    return {
        "file": path.name,
        "has_external": len(external_refs) > 0,
        "external_refs": external_refs,
        "external_count": sum(r["count"] for r in external_refs),
        "internal_count": len(internal_refs),
        "grounding_ratio": (
            sum(r["count"] for r in external_refs)
            / max(1, sum(r["count"] for r in external_refs) + len(internal_refs))
        ),
    }


def get_staged_lessons() -> list[Path]:
    """Get lesson files staged for commit."""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--diff-filter=A", "--name-only"],
            capture_output=True, text=True, cwd=ROOT,
        )
        return [
            ROOT / p.strip()
            for p in result.stdout.splitlines()
            if p.strip().startswith("memory/lessons/L-") and p.strip().endswith(".md")
        ]
    except Exception:
        return []


def get_recent_lessons(n: int = 20) -> list[Path]:
    """Get last N lesson files by number."""
    files = sorted(
        [f for f in LESSON_DIR.iterdir() if f.name.startswith("L-") and f.suffix == ".md"],
        key=lambda f: int(re.search(r"L-(\d+)", f.name).group(1)) if re.search(r"L-(\d+)", f.name) else 0,
        reverse=True,
    )
    return files[:n]


def main():
    args = sys.argv[1:]
    staged_mode = "--staged" in args
    as_json = "--json" in args
    baseline_n = 20

    for i, a in enumerate(args):
        if a == "--baseline" and i + 1 < len(args):
            baseline_n = int(args[i + 1])

    if staged_mode:
        lessons = get_staged_lessons()
        if not lessons:
            return  # nothing staged, silent exit for check.sh
    else:
        lessons = get_recent_lessons(baseline_n)

    results = [scan_lesson(p) for p in lessons]

    if as_json:
        summary = {
            "total": len(results),
            "with_external": sum(1 for r in results if r.get("has_external")),
            "without_external": sum(1 for r in results if not r.get("has_external")),
            "grounding_rate": (
                sum(1 for r in results if r.get("has_external")) / max(1, len(results))
            ),
            "lessons": results,
        }
        print(json.dumps(summary, indent=2, default=str))
        return

    if staged_mode:
        # check.sh hook mode: emit NOTICE for ungrounded lessons
        ungrounded = [r for r in results if not r.get("has_external")]
        if ungrounded:
            for r in ungrounded:
                print(f"  F-GND1 NOTICE: {r['file']} has no external references — "
                      f"consider adding URL, paper cite, or benchmark (L-1125, F-GND1)")
                print(f"    Internal refs: {r['internal_count']} | External: 0")
                print(f"    Add: Related URL, arXiv ref, named external benchmark, or empirical source")
        # report pass/notice
        total = len(results)
        grounded = total - len(ungrounded)
        if ungrounded:
            print(f"  F-GND1 external grounding: {len(ungrounded)}/{total} lesson(s) "
                  f"without external refs (NOTICE — not blocking)")
        else:
            print(f"  F-GND1 external grounding: PASS ({total} lesson(s), all have external refs)")
        return

    # Baseline report mode
    with_ext = sum(1 for r in results if r.get("has_external"))
    without_ext = len(results) - with_ext
    rate = with_ext / max(1, len(results)) * 100

    print(f"=== EXTERNAL GROUNDING CHECK — F-GND1, L-1125 ===\n")
    print(f"  Lessons scanned: {len(results)} (most recent)")
    print(f"  With external refs: {with_ext} ({rate:.0f}%)")
    print(f"  Without external refs: {without_ext} ({100-rate:.0f}%)")
    print()

    # Show ungrounded lessons
    if without_ext > 0:
        print(f"--- Ungrounded lessons (no external references) ---")
        for r in results:
            if not r.get("has_external"):
                print(f"  {r['file']}  (internal: {r['internal_count']}, external: 0)")

    # Show grounded lessons with what they cite
    if with_ext > 0:
        print(f"\n--- Grounded lessons (have external references) ---")
        for r in results:
            if r.get("has_external"):
                types = ", ".join(f"{ref['type']}({ref['count']})" for ref in r["external_refs"])
                ratio = r["grounding_ratio"]
                print(f"  {r['file']}  ext: {r['external_count']} [{types}]  ratio: {ratio:.2f}")

    print(f"\n  Grounding rate: {rate:.0f}% (target: increase from baseline)")
    print(f"  Wired into check.sh: --staged mode emits NOTICE for ungrounded lessons")


if __name__ == "__main__":
    main()
