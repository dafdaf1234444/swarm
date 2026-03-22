#!/usr/bin/env python3
"""
candidate_rank.py — Multi-candidate approach ranking for swarm tasks.

Inspired by Darwin Gödel Machine (Sakana AI, 2025, https://sakana.ai/dgm/)
which generates multiple candidate patches and ranks them before applying.
Also informed by SICA (arXiv:2504.15228) self-benchmarking pattern.

Swarm's orient→act cycle picks ONE approach. This tool scores pre-defined
candidate approaches against evidence, novelty, risk, grounding, and frontier
alignment — enabling pre-execution ranking instead of post-hoc expect-act-diff.

Usage:
    python3 tools/candidate_rank.py --approaches "A;B;C" --task "description"
    python3 tools/candidate_rank.py --approaches "A;B;C" --task "desc" --json

Part of F-ABSORB1 (external innovation absorption). L-1302.
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LESSONS_DIR = ROOT / "memory" / "lessons"
FRONTIER_FILE = ROOT / "tasks" / "FRONTIER.md"


def _git_recent(n=20):
    """Get recent commit messages to check novelty."""
    r = subprocess.run(
        ["git", "log", f"--oneline", f"-{n}"],
        capture_output=True, text=True, cwd=ROOT
    )
    return r.stdout.strip().lower()


def _recent_lesson_text(n=30):
    """Load text from recent lessons for evidence matching."""
    lessons = sorted(LESSONS_DIR.glob("L-*.md"), key=lambda p: p.name)
    texts = []
    for lf in lessons[-n:]:
        try:
            texts.append(lf.read_text(errors="replace").lower())
        except Exception:
            pass
    return " ".join(texts)


def _frontier_text():
    """Load frontier questions for alignment scoring."""
    try:
        return FRONTIER_FILE.read_text(errors="replace").lower()
    except Exception:
        return ""


def _word_overlap(text_a, text_b):
    """Compute word overlap ratio between two texts."""
    words_a = set(re.findall(r'\b\w{4,}\b', text_a.lower()))
    words_b = set(re.findall(r'\b\w{4,}\b', text_b.lower()))
    if not words_a or not words_b:
        return 0.0
    return len(words_a & words_b) / max(len(words_a), 1)


EXTERNAL_MARKERS = [
    r'https?://', r'arXiv:', r'doi:', r'et al\.', r'\(\d{4}\)',
    r'IEEE|ACM|NeurIPS|Nature|Science', r'Wikipedia|GitHub\.com',
]


def score_approach(approach, task, lesson_text, git_recent, frontier_text):
    """Score a single approach on 5 dimensions."""
    approach_lower = approach.lower()
    task_lower = task.lower()
    combined = f"{approach_lower} {task_lower}"

    # Evidence strength: how much lesson text supports this approach?
    evidence = min(_word_overlap(combined, lesson_text) * 5, 1.0)

    # Novelty: inverse of overlap with recent git log
    git_overlap = _word_overlap(approach_lower, git_recent)
    novelty = max(1.0 - git_overlap * 3, 0.0)

    # Scope risk: heuristic — fewer file-like references = lower risk
    file_refs = len(re.findall(r'\b\w+\.\w{2,4}\b', approach))
    scope_risk = max(1.0 - file_refs * 0.15, 0.2)

    # External grounding: does the approach mention external sources?
    ext_count = sum(1 for p in EXTERNAL_MARKERS if re.search(p, approach))
    grounding = min(ext_count * 0.25, 1.0)

    # Frontier alignment: overlap with open frontier questions
    frontier_align = min(_word_overlap(combined, frontier_text) * 4, 1.0)

    # Composite: weighted average
    composite = (
        evidence * 0.25 +
        novelty * 0.20 +
        scope_risk * 0.15 +
        grounding * 0.15 +
        frontier_align * 0.25
    )

    return {
        "approach": approach,
        "composite": round(composite, 3),
        "evidence": round(evidence, 2),
        "novelty": round(novelty, 2),
        "scope_risk": round(scope_risk, 2),
        "grounding": round(grounding, 2),
        "frontier_align": round(frontier_align, 2),
    }


def rank_approaches(approaches, task):
    """Score and rank all candidate approaches."""
    lesson_text = _recent_lesson_text()
    git_recent = _git_recent()
    frontier_text = _frontier_text()

    scores = [
        score_approach(a.strip(), task, lesson_text, git_recent, frontier_text)
        for a in approaches if a.strip()
    ]
    scores.sort(key=lambda s: s["composite"], reverse=True)
    return scores


def format_report(scores, task):
    """Format human-readable ranking report."""
    lines = [
        "=== CANDIDATE RANKING ===",
        f"Task: \"{task}\"",
        "",
    ]
    for i, s in enumerate(scores, 1):
        lines.append(f"#{i} [score: {s['composite']:.2f}] {s['approach']}")
        lines.append(
            f"  evidence: {s['evidence']} | novelty: {s['novelty']} | "
            f"risk: {s['scope_risk']} | grounding: {s['grounding']} | "
            f"frontier: {s['frontier_align']}"
        )
        lines.append("")
    if scores:
        best = scores[0]
        lines.append(f"→ Recommended: #{1} ({best['approach'][:60]}...)" if len(best['approach']) > 60
                      else f"→ Recommended: #{1} ({best['approach']})")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Rank candidate approaches for a task")
    parser.add_argument("--task", required=True, help="Task description")
    parser.add_argument("--approaches", required=True,
                        help="Semicolon-separated candidate approaches")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    approaches = [a for a in args.approaches.split(";") if a.strip()]
    if len(approaches) < 2:
        print("ERROR: Need at least 2 approaches (semicolon-separated)", file=sys.stderr)
        sys.exit(1)

    scores = rank_approaches(approaches, args.task)

    if args.json:
        print(json.dumps({"task": args.task, "rankings": scores}, indent=2))
    else:
        print(format_report(scores, args.task))


if __name__ == "__main__":
    main()
