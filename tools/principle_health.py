#!/usr/bin/env python3
"""Principle health checker — detect zombie and orphan P-claims.

Zombie: P-claim whose cited lessons are SUPERSEDED/FALSIFIED/MISSING.
Orphan: P-claim with zero lesson citations (untestable assertion).

Usage:
  python3 tools/principle_health.py              # summary report
  python3 tools/principle_health.py --json       # machine-readable output
  python3 tools/principle_health.py --worst 10   # top N worst zombies
  python3 tools/principle_health.py --threshold 0.5  # flag if zombie_rate > threshold

Wires into orient.py as a periodic health check (F-EPIS3).
Based on S543 experiment (L-1653): 30.5% zombie rate, zero reverse invalidation flow.
"""
import argparse
import json
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
PRINCIPLES_FILE = REPO / "memory" / "PRINCIPLES.md"
LESSONS_DIR = REPO / "memory" / "lessons"

# Cache lesson health to avoid re-reading files
_lesson_cache: dict[str, str] = {}


def get_lesson_status(lesson_id: str) -> str:
    """Return ACTIVE, SUPERSEDED, FALSIFIED, or MISSING for a lesson."""
    if lesson_id in _lesson_cache:
        return _lesson_cache[lesson_id]

    num = lesson_id.replace("L-", "")
    path = LESSONS_DIR / f"L-{num}.md"
    if not path.exists():
        _lesson_cache[lesson_id] = "MISSING"
        return "MISSING"

    content = path.read_text(encoding="utf-8", errors="replace").upper()
    for status in ("SUPERSEDED", "FALSIFIED", "REJECTED", "DEPRECATED", "RETRACTED"):
        if status in content:
            _lesson_cache[lesson_id] = status
            return status

    _lesson_cache[lesson_id] = "ACTIVE"
    return "ACTIVE"


def parse_principles() -> dict:
    """Extract P-NNN claims with their L-NNN citations from PRINCIPLES.md."""
    text = PRINCIPLES_FILE.read_text(encoding="utf-8")
    principles = {}

    # Find all P-NNN references with surrounding text
    # Format: P-NNN description (L-NNN, L-NNN, STATUS)
    for m in re.finditer(r'P-(\d+)\s', text):
        pid = f"P-{m.group(1)}"
        if pid in principles:
            continue
        # Get text from this P-NNN to the next P-NNN or end of line block
        start = m.start()
        next_p = re.search(r'\bP-\d+\s', text[m.end():])
        end = m.end() + next_p.start() if next_p else min(start + 500, len(text))
        body = text[start:end]

        lessons = list(dict.fromkeys(f"L-{l}" for l in re.findall(r'L-(\d+)', body)))
        # Extract short description
        desc_match = re.match(r'P-\d+\s+(.+?)(?:\(L-|\||$)', body.split('\n')[0])
        desc = desc_match.group(1).strip() if desc_match else body[len(pid):len(pid)+100].strip()

        principles[pid] = {
            "description": desc[:120],
            "lessons_cited": lessons,
        }

    return principles


def classify_principles(principles: dict) -> dict:
    """Classify each principle as HEALTHY, ZOMBIE, or ORPHAN."""
    results = {"healthy": [], "zombie": [], "orphan": []}

    for pid, info in sorted(principles.items(), key=lambda x: int(x[0].split("-")[1])):
        cited = info["lessons_cited"]
        if not cited:
            results["orphan"].append({"id": pid, "description": info["description"]})
            continue

        dead = []
        alive = []
        for lid in cited:
            status = get_lesson_status(lid)
            if status == "ACTIVE":
                alive.append(lid)
            else:
                dead.append((lid, status))

        if not dead:
            results["healthy"].append({"id": pid, "alive": len(alive)})
        else:
            dead_fraction = len(dead) / len(cited)
            results["zombie"].append({
                "id": pid,
                "description": info["description"],
                "dead": dead,
                "alive_count": len(alive),
                "total_citations": len(cited),
                "dead_fraction": round(dead_fraction, 3),
            })

    return results


def print_report(results: dict, worst_n: int = 20):
    """Print human-readable health report."""
    n_healthy = len(results["healthy"])
    n_zombie = len(results["zombie"])
    n_orphan = len(results["orphan"])
    total = n_healthy + n_zombie + n_orphan

    print(f"=== PRINCIPLE HEALTH ({total} principles) ===")
    print(f"  Healthy: {n_healthy} ({100*n_healthy/total:.1f}%)")
    print(f"  Zombie:  {n_zombie} ({100*n_zombie/total:.1f}%) — cite dead lessons")
    print(f"  Orphan:  {n_orphan} ({100*n_orphan/total:.1f}%) — no citations")
    print()

    # Fully-dead zombies (100% dead citations)
    fully_dead = [z for z in results["zombie"] if z["dead_fraction"] == 1.0]
    partially_dead = [z for z in results["zombie"] if z["dead_fraction"] < 1.0]

    print(f"  Fully dead (100% dead evidence): {len(fully_dead)}")
    print(f"  Partially dead (some alive):     {len(partially_dead)}")
    print()

    # Sort worst first
    worst = sorted(results["zombie"], key=lambda z: (-z["dead_fraction"], -len(z["dead"])))
    print(f"--- Worst {min(worst_n, len(worst))} zombies ---")
    for z in worst[:worst_n]:
        dead_str = ", ".join(f"{lid}={st}" for lid, st in z["dead"])
        print(f"  {z['id']} ({z['dead_fraction']*100:.0f}% dead, {z['alive_count']} alive): {dead_str}")
        print(f"    {z['description'][:100]}")
    print()

    # Actionable summary
    if fully_dead:
        print(f"ACTION: {len(fully_dead)} principles have ZERO living evidence — review for DROP/REVISE:")
        for z in fully_dead[:10]:
            print(f"  {z['id']}: {z['description'][:80]}")
        if len(fully_dead) > 10:
            print(f"  ... and {len(fully_dead) - 10} more")


def main():
    parser = argparse.ArgumentParser(description="Principle health checker")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--worst", type=int, default=20, help="Show N worst zombies")
    parser.add_argument("--threshold", type=float, default=None,
                        help="Exit 1 if zombie_rate exceeds threshold")
    args = parser.parse_args()

    principles = parse_principles()
    results = classify_principles(principles)

    total = len(results["healthy"]) + len(results["zombie"]) + len(results["orphan"])
    zombie_rate = len(results["zombie"]) / total if total else 0

    if args.json:
        output = {
            "total": total,
            "healthy": len(results["healthy"]),
            "zombie": len(results["zombie"]),
            "orphan": len(results["orphan"]),
            "zombie_rate": round(zombie_rate, 4),
            "fully_dead": len([z for z in results["zombie"] if z["dead_fraction"] == 1.0]),
            "zombies": results["zombie"],
            "orphans": results["orphan"],
        }
        json.dump(output, sys.stdout, indent=2)
        print()
    else:
        print_report(results, worst_n=args.worst)

    if args.threshold is not None and zombie_rate > args.threshold:
        print(f"\nFAIL: zombie_rate {zombie_rate:.3f} > threshold {args.threshold}")
        sys.exit(1)


if __name__ == "__main__":
    main()
