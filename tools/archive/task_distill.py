#!/usr/bin/env python3
"""task_distill.py — Convert task completions into structured lesson candidates.

When a task completes, this tool:
1. Takes the expected vs actual outcome
2. Computes surprise (how different actual was from expected)
3. If surprise > threshold, generates a lesson candidate with typed relations
4. If surprise = 0, outputs a confirmation signal for existing knowledge

This closes the task→lesson feedback gap: completed work structurally
produces learning artifacts, not just session-end manual distillation.

Usage:
  python3 tools/task_distill.py --task "what was done" \\
      --expect "what was expected" --actual "what actually happened" \\
      --domain meta --session S499

  # With typed relations
  python3 tools/task_distill.py --task "refactored dispatch" \\
      --expect "10% speedup" --actual "3% speedup + new bug" \\
      --supports L-601 --contradicts L-500 --extends L-450 \\
      --domain architecture --session S499

  # Generate lesson file directly
  python3 tools/task_distill.py --task "..." --expect "..." --actual "..." \\
      --domain meta --session S499 --write
"""

import argparse
import json
import re
import sys
from pathlib import Path
from datetime import date

REPO = Path(__file__).resolve().parent.parent
LESSONS_DIR = REPO / "memory" / "lessons"


def compute_surprise(expect: str, actual: str) -> float:
    """Estimate surprise from text similarity.

    0.0 = exact match (confirmed model)
    1.0 = completely different (model broken)

    Uses simple word overlap as proxy. Sessions should override
    with --surprise for precise control.
    """
    if not expect or not actual:
        return 0.5  # unknown = moderate surprise

    e_words = set(expect.lower().split())
    a_words = set(actual.lower().split())

    if not e_words or not a_words:
        return 0.5

    overlap = len(e_words & a_words)
    total = len(e_words | a_words)

    # Invert: high overlap = low surprise
    similarity = overlap / total if total > 0 else 0
    return round(1.0 - similarity, 2)


def next_lesson_number() -> int:
    """Find next available lesson number."""
    existing = []
    for f in LESSONS_DIR.glob("L-*.md"):
        m = re.match(r"L-(\d+)", f.stem)
        if m:
            existing.append(int(m.group(1)))
    return max(existing, default=0) + 1


def classify_evidence(surprise: float, has_measurement: bool) -> str:
    """Classify evidence type from surprise and measurement presence."""
    if surprise < 0.1:
        return "confirmation"
    if has_measurement:
        return "measurement"
    if surprise > 0.7:
        return "contradiction"
    return "observation"


def generate_lesson_candidate(args, surprise: float) -> str:
    """Generate a lesson candidate in knowledge-atom format."""
    num = next_lesson_number()
    ev_type = classify_evidence(surprise, bool(args.effect_size))

    # Build typed relation lines
    relations = []
    if args.supports:
        relations.append(f"Supports: {', '.join(args.supports)}")
    if args.contradicts:
        relations.append(f"Contradicts: {', '.join(args.contradicts)}")
    if args.extends:
        relations.append(f"Extends: {', '.join(args.extends)}")
    if args.requires:
        relations.append(f"Requires: {', '.join(args.requires)}")
    # Fallback: untyped Cites for backward compat
    if not relations and args.cites:
        relations.append(f"Cites: {', '.join(args.cites)}")

    rel_block = "\n".join(relations) if relations else "Cites: (none yet)"

    # Confidence from surprise
    if surprise < 0.2:
        confidence = "Verified"
    elif surprise < 0.5:
        confidence = "Observed"
    elif surprise < 0.8:
        confidence = "Directional"
    else:
        confidence = "Assumed"

    effect = f" | Effect-size: {args.effect_size}" if args.effect_size else ""
    sample = f" | Sample: n={args.sample}" if args.sample else ""

    return f"""# L-{num}: [CANDIDATE] {{claim from: {args.task}}}
{rel_block}
Domain: {args.domain} | Session: {args.session} | Confidence: {confidence} | Level: L2
Evidence-type: {ev_type}{sample}{effect} | Surprise: {surprise}

## Claim (1-2 lines)
<!-- Replace with falsifiable statement derived from the task outcome -->
Expected: {args.expect}
Actual: {args.actual}

## Evidence (3 lines max)
<!-- What specifically supports this claim? -->
Task: {args.task}
Surprise: {surprise} ({ev_type})

## Scope
<!-- Where does this apply? What are the boundary conditions? -->

## Falsified-if
<!-- Specific condition that would make this claim false -->
"""


def main():
    p = argparse.ArgumentParser(description="Convert task completion to lesson candidate")
    p.add_argument("--task", required=True, help="What was done")
    p.add_argument("--expect", required=True, help="What was expected")
    p.add_argument("--actual", required=True, help="What actually happened")
    p.add_argument("--domain", required=True, help="Domain tag")
    p.add_argument("--session", required=True, help="Session ID (e.g. S499)")

    # Typed relations (new)
    p.add_argument("--supports", nargs="*", help="L-NNN/P-NNN this confirms")
    p.add_argument("--contradicts", nargs="*", help="L-NNN/P-NNN this weakens")
    p.add_argument("--extends", nargs="*", help="L-NNN/P-NNN this builds on")
    p.add_argument("--requires", nargs="*", help="L-NNN/P-NNN this depends on")
    p.add_argument("--cites", nargs="*", help="Untyped citations (backward compat)")

    # Evidence metadata
    p.add_argument("--effect-size", help="Effect size if measured")
    p.add_argument("--sample", type=int, help="Sample size if measured")
    p.add_argument("--surprise", type=float, help="Override auto-computed surprise (0-1)")

    # Output control
    p.add_argument("--write", action="store_true", help="Write lesson file (otherwise just print)")
    p.add_argument("--threshold", type=float, default=0.3,
                   help="Surprise threshold for lesson generation (default: 0.3)")
    p.add_argument("--json", action="store_true", help="Output as JSON")

    args = p.parse_args()

    # Compute or use provided surprise
    surprise = args.surprise if args.surprise is not None else compute_surprise(args.expect, args.actual)

    result = {
        "task": args.task,
        "expected": args.expect,
        "actual": args.actual,
        "surprise": surprise,
        "evidence_type": classify_evidence(surprise, bool(args.effect_size)),
        "threshold": args.threshold,
        "generates_lesson": surprise >= args.threshold,
    }

    if surprise < args.threshold:
        # Low surprise = confirmation, not a new lesson
        result["action"] = "confirmation"
        result["message"] = (
            f"Surprise {surprise:.2f} < threshold {args.threshold:.2f}. "
            f"Model confirmed — no lesson needed. "
            f"Strengthen existing knowledge in domain '{args.domain}'."
        )
        if args.supports:
            result["strengthens"] = args.supports
            result["message"] += f" Confirmed: {', '.join(args.supports)}"

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"[CONFIRM] {result['message']}")
        return

    # High surprise = generate lesson candidate
    candidate = generate_lesson_candidate(args, surprise)
    result["action"] = "lesson_candidate"

    if args.write:
        num = next_lesson_number()
        path = LESSONS_DIR / f"L-{num:04d}.md"
        path.write_text(candidate)
        result["written_to"] = str(path)
        print(f"[LESSON] Written candidate to {path}")
        print(f"  Surprise: {surprise:.2f} | Type: {result['evidence_type']}")
        print(f"  IMPORTANT: Edit the candidate to fill in claim, scope, and falsification criteria")
    elif args.json:
        result["candidate"] = candidate
        print(json.dumps(result, indent=2))
    else:
        print(f"[CANDIDATE] Surprise {surprise:.2f} >= threshold {args.threshold:.2f}")
        print(f"Evidence type: {result['evidence_type']}")
        print()
        print(candidate)


if __name__ == "__main__":
    main()
