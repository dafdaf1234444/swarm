#!/usr/bin/env python3
"""
correction_propagation.py — Detect and queue correction gaps in the lesson graph.

When a lesson is falsified or superseded, citers may still treat the original
framing as valid. This tool walks the citation graph to find those gaps.

Usage:
  python3 tools/correction_propagation.py                  # report mode
  python3 tools/correction_propagation.py --json           # machine-readable
  python3 tools/correction_propagation.py --save           # save artifact
  python3 tools/correction_propagation.py --fix-cites      # add Cites: back-refs

Related: F-IC1, L-734, L-025, L-613
"""

import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).parent.parent
LESSONS_DIR = ROOT / "memory" / "lessons"

# Markers that indicate a lesson has been falsified or corrected
FALSIFIED_MARKERS = re.compile(
    r"\bFALSIFIED\b|\bfalsified\b|\bretracted\b|\bwrong\b.*?\bclaim\b"
    r"|\bclaim\b.*?\bwrong\b|\bincorrect\b.*?\bfinding\b"
)
CORRECTION_MARKERS = re.compile(
    r"\bsupersed|\bcorrect(?:s|ed|ion)\b|\breplac(?:es|ed)\b"
    r"|\bovertur|\brefut|\binvalid",
    re.IGNORECASE,
)


def _parse_lessons() -> dict[str, dict]:
    """Parse all lessons: extract citations, title, and text."""
    lessons = {}
    cite_pat = re.compile(r"\bL-(\d+)\b")
    for f in sorted(LESSONS_DIR.glob("L-*.md")):
        lid = f.stem
        text = f.read_text(encoding="utf-8")
        lines = text.splitlines()
        title = lines[0].lstrip("# ").strip() if lines else ""

        # Extract Cites: header
        cites_header: list[str] = []
        for line in lines:
            m = re.match(r"^Cites:\s*(.*)", line)
            if m:
                cites_header = [f"L-{x}" for x in cite_pat.findall(m.group(1))]
                break

        # Extract all L-NNN references in body
        all_refs = set(f"L-{x}" for x in cite_pat.findall(text))
        all_refs.discard(lid)  # don't count self-reference

        lessons[lid] = {
            "title": title,
            "text": text,
            "cites_header": cites_header,
            "all_refs": all_refs,
        }
    return lessons


def _find_falsified(lessons: dict[str, dict]) -> list[dict]:
    """Identify lessons with falsification markers and their correctors."""
    falsified = []
    for lid, data in lessons.items():
        text = data["text"]
        if not FALSIFIED_MARKERS.search(text):
            continue

        # Find which other lessons this one falsifies (or was falsified by)
        # Look for patterns like "L-025 falsified" or "falsified by L-613"
        targets = set()
        correctors = set()
        for ref in data["all_refs"]:
            ref_text = lessons.get(ref, {}).get("text", "")
            # If THIS lesson mentions falsifying another
            if re.search(rf"\b{re.escape(ref)}\b.*?falsif", text, re.IGNORECASE):
                targets.add(ref)
            # If another lesson falsifies THIS one
            if re.search(rf"\b{re.escape(lid)}\b.*?falsif", ref_text, re.IGNORECASE):
                correctors.add(ref)

        falsified.append({
            "id": lid,
            "title": data["title"][:80],
            "targets_falsified": sorted(targets),
            "corrected_by": sorted(correctors),
        })
    return falsified


def _build_citation_graph(lessons: dict[str, dict]) -> dict[str, set[str]]:
    """Build reverse citation graph: for each lesson, who cites it."""
    cited_by: dict[str, set[str]] = defaultdict(set)
    for lid, data in lessons.items():
        for ref in data["all_refs"]:
            cited_by[ref].add(lid)
    return dict(cited_by)


def _find_correction_gaps(
    lessons: dict[str, dict],
    cited_by: dict[str, set[str]],
) -> list[dict]:
    """Find lessons that cite falsified content without acknowledging corrections."""
    gaps = []

    # Known falsified lessons and their corrections (from lesson text analysis)
    falsified_corrections = {}
    for lid, data in lessons.items():
        text = data["text"]
        if not FALSIFIED_MARKERS.search(text):
            continue

        # This lesson mentions FALSIFIED — it's either the corrector or the corrected
        # Check if it says "L-NNN ... FALSIFIED" (this lesson falsifies L-NNN)
        for ref in data["all_refs"]:
            # Check if the falsification is about ref
            context = text
            if re.search(
                rf"(?:{re.escape(ref)}.*?(?:FALSIFIED|falsified|wrong|incorrect))"
                rf"|(?:(?:FALSIFIED|falsified).*?{re.escape(ref)})",
                context,
            ):
                if ref not in falsified_corrections:
                    falsified_corrections[ref] = set()
                falsified_corrections[ref].add(lid)

    # Also add manually known cases
    if "L-025" not in falsified_corrections:
        falsified_corrections["L-025"] = set()
    falsified_corrections["L-025"].update({"L-613", "L-618"})

    # For each falsified lesson, check its citers
    for falsified_lid, correctors in sorted(falsified_corrections.items()):
        if falsified_lid not in lessons:
            continue

        citers = cited_by.get(falsified_lid, set())
        uncorrected = []

        for citer in sorted(citers):
            if citer == falsified_lid:
                continue
            if citer in correctors:
                continue  # the corrector itself

            citer_data = lessons.get(citer, {})
            citer_refs = citer_data.get("all_refs", set())
            citer_text = citer_data.get("text", "")

            # Check if citer acknowledges the correction
            acknowledges = False
            # 1. Does citer cite any of the correcting lessons?
            if citer_refs & correctors:
                acknowledges = True
            # 2. Does citer mention falsification of the target?
            if re.search(
                rf"{re.escape(falsified_lid)}.*?(?:falsif|supersed|wrong|correct)",
                citer_text,
                re.IGNORECASE,
            ):
                acknowledges = True
            # 3. Does citer contain correction markers about the falsified lesson?
            if CORRECTION_MARKERS.search(citer_text) and falsified_lid in str(citer_refs):
                acknowledges = True

            if not acknowledges:
                uncorrected.append(citer)

        if uncorrected:
            gaps.append({
                "falsified": falsified_lid,
                "falsified_title": lessons[falsified_lid]["title"][:60],
                "correctors": sorted(correctors),
                "total_citers": len(citers),
                "uncorrected_citers": uncorrected,
                "uncorrected_count": len(uncorrected),
                "correction_rate": round(
                    1 - len(uncorrected) / len(citers), 3
                ) if citers else 1.0,
            })

    return sorted(gaps, key=lambda g: -g["uncorrected_count"])


def run_analysis() -> dict:
    """Run full correction propagation analysis."""
    lessons = _parse_lessons()
    cited_by = _build_citation_graph(lessons)
    gaps = _find_correction_gaps(lessons, cited_by)

    total_gaps = sum(g["uncorrected_count"] for g in gaps)
    total_falsified = len(gaps)
    avg_correction_rate = (
        sum(g["correction_rate"] for g in gaps) / len(gaps)
        if gaps else 1.0
    )

    return {
        "session": "S382",
        "computed_at": datetime.now(timezone.utc).isoformat(),
        "frontier": "F-IC1",
        "total_lessons": len(lessons),
        "total_falsified_with_gaps": total_falsified,
        "total_uncorrected_citations": total_gaps,
        "avg_correction_rate": round(avg_correction_rate, 3),
        "gaps": gaps,
        "correction_queue": [
            {
                "citer": citer,
                "needs_correction_about": g["falsified"],
                "correctors_to_cite": g["correctors"],
                "priority": "HIGH" if g["uncorrected_count"] >= 5 else "MEDIUM",
            }
            for g in gaps
            for citer in g["uncorrected_citers"]
        ][:50],  # top 50
    }


def print_report(result: dict) -> None:
    """Human-readable correction propagation report."""
    print(f"=== CORRECTION PROPAGATION ANALYSIS — {result['session']} ===\n")
    print(f"Total lessons: {result['total_lessons']}")
    print(f"Falsified with uncorrected citers: {result['total_falsified_with_gaps']}")
    print(f"Total uncorrected citations: {result['total_uncorrected_citations']}")
    print(f"Average correction rate: {result['avg_correction_rate']:.0%}\n")

    for g in result["gaps"]:
        print(f"  {g['falsified']} ({g['falsified_title']})")
        print(f"    Correctors: {', '.join(g['correctors'])}")
        print(f"    Citers: {g['total_citers']} total, {g['uncorrected_count']} uncorrected")
        print(f"    Correction rate: {g['correction_rate']:.0%}")
        print(f"    Uncorrected: {', '.join(g['uncorrected_citers'][:10])}")
        if len(g["uncorrected_citers"]) > 10:
            print(f"      ... and {len(g['uncorrected_citers']) - 10} more")
        print()

    print(f"--- Correction queue (top {min(20, len(result['correction_queue']))}) ---")
    for item in result["correction_queue"][:20]:
        print(f"  {item['citer']} ← needs {item['needs_correction_about']} "
              f"(cite {', '.join(item['correctors_to_cite'])})")


if __name__ == "__main__":
    result = run_analysis()

    save = "--save" in sys.argv
    as_json = "--json" in sys.argv or save

    if as_json:
        output = json.dumps(result, indent=2)
        if save:
            out_path = (
                ROOT / "experiments" / "security"
                / f"f-ic1-correction-propagation-{result['session'].lower()}.json"
            )
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(output + "\n", encoding="utf-8")
            print(f"Artifact saved: {out_path}")
        else:
            print(output)
    else:
        print_report(result)
