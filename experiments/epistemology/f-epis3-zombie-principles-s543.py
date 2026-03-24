#!/usr/bin/env python3
"""F-EPIS3 zombie principle detector — find P-claims standing on dead evidence.

Hypothesis: P-claims achieve 100% confirmation (L-1649) partly because they
are never relabeled when their evidence base collapses. This scanner checks
whether P-claim citations still reference ACTIVE lessons, or whether the
foundation has eroded (SUPERSEDED, FALSIFIED, missing).

Expect: ≥10% of P-claims cite at least one dead lesson. If true, the "fortress"
is partly a labeling artifact, not genuine robustness.
"""
import json
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parents[2]
PRINCIPLES_FILE = REPO / "memory" / "PRINCIPLES.md"
LESSONS_DIR = REPO / "memory" / "lessons"

def parse_principles():
    """Extract P-NNN claims with their cited L-NNN lessons."""
    text = PRINCIPLES_FILE.read_text(encoding="utf-8")
    principles = {}
    # Match P-NNN patterns with surrounding context
    for m in re.finditer(r'P-(\d+)\s+([^|]+?)(?:\s*\(([^)]+)\)|\s*\|)', text):
        pid = f"P-{m.group(1)}"
        body = m.group(2).strip()
        cite_part = m.group(3) or ""
        lessons = re.findall(r'L-(\d+)', body + " " + cite_part)
        principles[pid] = {
            "text": body[:120],
            "lessons_cited": [f"L-{l}" for l in lessons],
        }
    # Also parse the compact format: P-NNN text (L-NNN, ..., STATUS)
    for m in re.finditer(r'P-(\d+)\s+(.+?)(?=P-\d+|\Z)', text, re.DOTALL):
        pid = f"P-{m.group(1)}"
        body = m.group(2).strip()
        if pid not in principles:
            lessons = re.findall(r'L-(\d+)', body)
            principles[pid] = {
                "text": body[:120],
                "lessons_cited": [f"L-{l}" for l in lessons],
            }
        else:
            # Merge any additional L-NNN citations
            extra = re.findall(r'L-(\d+)', body)
            existing = {l for l in principles[pid]["lessons_cited"]}
            for l in extra:
                lid = f"L-{l}"
                if lid not in existing:
                    principles[pid]["lessons_cited"].append(lid)
                    existing.add(lid)
    return principles


def check_lesson_health(lesson_id: str):
    """Check if a lesson file exists and whether it's been superseded or falsified."""
    num = lesson_id.replace("L-", "")
    path = LESSONS_DIR / f"L-{num}.md"
    if not path.exists():
        # Try with leading zeros
        for p in LESSONS_DIR.glob(f"L-{num}*.md"):
            path = p
            break
        else:
            return {"exists": False, "status": "MISSING"}

    content = path.read_text(encoding="utf-8", errors="replace")
    content_upper = content.upper()

    if "SUPERSEDED" in content_upper:
        return {"exists": True, "status": "SUPERSEDED"}
    if "FALSIFIED" in content_upper:
        return {"exists": True, "status": "FALSIFIED"}
    if "REJECTED" in content_upper:
        return {"exists": True, "status": "REJECTED"}
    if "DEPRECATED" in content_upper:
        return {"exists": True, "status": "DEPRECATED"}
    if "RETRACTED" in content_upper:
        return {"exists": True, "status": "RETRACTED"}
    return {"exists": True, "status": "ACTIVE"}


def main():
    principles = parse_principles()
    print(f"Parsed {len(principles)} P-claims from PRINCIPLES.md\n")

    zombies = []  # P-claims citing dead lessons
    orphans = []  # P-claims citing no lessons at all
    healthy = []  # P-claims with all citations alive

    for pid, info in sorted(principles.items(), key=lambda x: int(x[0].split("-")[1])):
        cited = info["lessons_cited"]
        if not cited:
            orphans.append(pid)
            continue

        dead_citations = []
        for lid in cited:
            health = check_lesson_health(lid)
            if health["status"] != "ACTIVE":
                dead_citations.append((lid, health["status"]))

        if dead_citations:
            zombies.append({
                "principle": pid,
                "text": info["text"],
                "dead_citations": dead_citations,
                "total_citations": len(cited),
                "dead_fraction": len(dead_citations) / len(cited),
            })
        else:
            healthy.append(pid)

    # Report
    total = len(principles)
    print(f"=== ZOMBIE PRINCIPLE SCAN ===")
    print(f"Total P-claims: {total}")
    print(f"With citations: {total - len(orphans)}")
    print(f"Orphans (no L-NNN citations): {len(orphans)} ({100*len(orphans)/total:.1f}%)")
    print(f"Healthy (all citations alive): {len(healthy)} ({100*len(healthy)/total:.1f}%)")
    print(f"ZOMBIES (≥1 dead citation): {len(zombies)} ({100*len(zombies)/total:.1f}%)")

    if zombies:
        print(f"\n--- Zombie principles (standing on dead evidence) ---")
        # Sort by dead fraction descending
        zombies.sort(key=lambda z: z["dead_fraction"], reverse=True)
        for z in zombies[:20]:
            dead_str = ", ".join(f"{lid}={status}" for lid, status in z["dead_citations"])
            print(f"  {z['principle']}: {z['dead_fraction']*100:.0f}% dead ({len(z['dead_citations'])}/{z['total_citations']})")
            print(f"    Dead: {dead_str}")
            print(f"    Text: {z['text'][:100]}")
            print()

    # Summary statistics
    zombie_rate = len(zombies) / total if total > 0 else 0
    print(f"\n=== VERDICT ===")
    print(f"Zombie rate: {zombie_rate*100:.1f}%")
    if zombie_rate >= 0.10:
        print("HYPOTHESIS SUPPORTED: ≥10% of P-claims cite dead evidence.")
        print("The P-claim fortress is partly a labeling artifact.")
    else:
        print("HYPOTHESIS NOT SUPPORTED: <10% zombie rate.")
        print("P-claim evidence base is genuinely robust.")

    # Save results
    results = {
        "experiment": "f-epis3-zombie-principles-s543",
        "session": "S543",
        "frontier": "F-EPIS3",
        "hypothesis": ">=10% of P-claims cite dead (SUPERSEDED/FALSIFIED) lessons",
        "expect": "zombie_rate >= 0.10",
        "actual": {
            "total_principles": total,
            "orphans": len(orphans),
            "healthy": len(healthy),
            "zombies": len(zombies),
            "zombie_rate": round(zombie_rate, 4),
        },
        "zombie_details": zombies[:20],
        "verdict": "SUPPORTED" if zombie_rate >= 0.10 else "NOT_SUPPORTED",
    }
    out = REPO / "experiments" / "epistemology" / "f-epis3-zombie-principles-s543.json"
    out.write_text(json.dumps(results, indent=2, default=str), encoding="utf-8")
    print(f"\nResults saved to {out.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
