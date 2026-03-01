#!/usr/bin/env python3
"""
enforcement_router.py — Map meta-prescriptions to structural implementations.

L-831: L-601 not applied to itself — prescriptions without enforcement decay.
Finds lessons with ## Rule sections and classifies each as:
  STRUCTURAL  — lesson ID referenced in core tool files (enforced in code)
  PERIODIC    — lesson ID referenced in periodics.json / maintenance periodic section
  ASPIRATIONAL — lesson ID not found in any tool (decays per L-601)

Usage:
  python3 tools/enforcement_router.py [--json] [--min-sharpe N] [--top N]
"""

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent

# Core tool files that wire structural enforcement
STRUCTURAL_FILES = [
    "tools/maintenance.py",
    "tools/orient.py",
    "tools/open_lane.py",
    "tools/close_lane.py",
    "tools/check.sh",
    "tools/science_quality.py",
    "tools/dispatch_optimizer.py",
    "tools/contract_check.py",
    "tools/validate_beliefs.py",
]

# Periodic-tier files (softer enforcement)
PERIODIC_FILES = [
    "tools/periodics.json",
    "memory/OPERATIONS.md",
    "beliefs/CORE.md",
    "SWARM.md",
    "CLAUDE.md",
]


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


def scan_lessons(lessons_dir: Path, min_sharpe: int = 0) -> list[dict]:
    """Extract lessons with ## Rule sections."""
    rules = []
    for f in sorted(lessons_dir.glob("L-*.md")):
        content = _read(f)
        lesson_id = f.stem

        sharpe_m = re.search(r"Sharpe:\s*(\d+)", content)
        sharpe = int(sharpe_m.group(1)) if sharpe_m else 0
        if sharpe < min_sharpe:
            continue

        session_m = re.search(r"Session:\s*(S\d+)", content)
        session = session_m.group(1) if session_m else "?"

        domain_m = re.search(r"\|\s*Domain:\s*(\S+)", content)
        domain = domain_m.group(1) if domain_m else "?"

        rule_m = re.search(
            r"^## Rule\s*\n(.*?)(?=\n##|\Z)", content, re.MULTILINE | re.DOTALL
        )
        if not rule_m:
            continue

        rule_text = rule_m.group(1).strip()
        # Extract first meaningful sentence
        first_line = rule_text.split("\n")[0].strip()

        rules.append(
            {
                "lesson": lesson_id,
                "session": session,
                "domain": domain,
                "sharpe": sharpe,
                "rule": first_line[:200],
            }
        )
    return rules


def build_reference_maps(repo_root: Path) -> tuple[set[str], set[str]]:
    """Return (structural_refs, periodic_refs) — lesson IDs found in each tier."""
    structural_refs: set[str] = set()
    periodic_refs: set[str] = set()

    lesson_pattern = re.compile(r"\bL-(\d{3,4})\b")

    for rel_path in STRUCTURAL_FILES:
        content = _read(repo_root / rel_path)
        for m in lesson_pattern.finditer(content):
            structural_refs.add(f"L-{m.group(1)}")

    for rel_path in PERIODIC_FILES:
        content = _read(repo_root / rel_path)
        for m in lesson_pattern.finditer(content):
            if f"L-{m.group(1)}" not in structural_refs:
                periodic_refs.add(f"L-{m.group(1)}")

    return structural_refs, periodic_refs


def classify(
    lesson_id: str, structural_refs: set[str], periodic_refs: set[str]
) -> str:
    if lesson_id in structural_refs:
        return "STRUCTURAL"
    if lesson_id in periodic_refs:
        return "PERIODIC"
    return "ASPIRATIONAL"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument(
        "--min-sharpe", type=int, default=0, help="Minimum Sharpe threshold"
    )
    parser.add_argument(
        "--top", type=int, default=10, help="Top N aspirational prescriptions to show"
    )
    args = parser.parse_args()

    lessons_dir = REPO_ROOT / "memory" / "lessons"
    rules = scan_lessons(lessons_dir, min_sharpe=args.min_sharpe)
    structural_refs, periodic_refs = build_reference_maps(REPO_ROOT)

    classified = []
    for r in rules:
        tier = classify(r["lesson"], structural_refs, periodic_refs)
        classified.append({**r, "tier": tier})

    classified.sort(key=lambda x: (-x["sharpe"], x["lesson"]))

    counts = {
        "STRUCTURAL": sum(1 for r in classified if r["tier"] == "STRUCTURAL"),
        "PERIODIC": sum(1 for r in classified if r["tier"] == "PERIODIC"),
        "ASPIRATIONAL": sum(1 for r in classified if r["tier"] == "ASPIRATIONAL"),
        "total": len(classified),
    }

    aspirational = [r for r in classified if r["tier"] == "ASPIRATIONAL"]
    high_sharpe_asp = [r for r in aspirational if r["sharpe"] >= 8]

    if args.json:
        result = {
            "summary": counts,
            "enforcement_rate": round(
                counts["STRUCTURAL"] / counts["total"], 3
            ) if counts["total"] else 0,
            "prescription_gap_rate": round(
                counts["ASPIRATIONAL"] / counts["total"], 3
            ) if counts["total"] else 0,
            "high_sharpe_aspirational": high_sharpe_asp[:args.top],
            "all_aspirational_count": len(aspirational),
        }
        print(json.dumps(result, indent=2))
        return

    # Human-readable output
    total = counts["total"]
    print(f"=== ENFORCEMENT ROUTER (L-831) ===")
    print(f"Rule-bearing lessons: {total}")
    print(
        f"  STRUCTURAL  (wired in code): {counts['STRUCTURAL']} "
        f"({100*counts['STRUCTURAL']//total if total else 0}%)"
    )
    print(
        f"  PERIODIC    (in protocol):   {counts['PERIODIC']} "
        f"({100*counts['PERIODIC']//total if total else 0}%)"
    )
    print(
        f"  ASPIRATIONAL (unimplemented): {counts['ASPIRATIONAL']} "
        f"({100*counts['ASPIRATIONAL']//total if total else 0}%)"
    )

    enforcement_rate = counts["STRUCTURAL"] / total if total else 0
    print(f"\nEnforcement rate: {enforcement_rate:.1%} (structural only)")
    print(f"Prescription gap (aspirational): {len(aspirational)}/{total}")

    if high_sharpe_asp:
        print(f"\nTop ASPIRATIONAL prescriptions (Sharpe≥8, n={len(high_sharpe_asp)}):")
        for r in high_sharpe_asp[: args.top]:
            print(
                f"  [{r['tier']}] {r['lesson']} Sh={r['sharpe']} ({r['domain']}):"
            )
            print(f"    {r['rule'][:90]}")
    else:
        print("\nNo high-Sharpe aspirational prescriptions found.")

    if aspirational:
        print(
            f"\nFull aspirational list: {len(aspirational)} prescriptions lacking structural wiring."
        )
        print("Priority: enforce lessons with Sharpe≥9 first (highest meta-value).")


if __name__ == "__main__":
    main()
