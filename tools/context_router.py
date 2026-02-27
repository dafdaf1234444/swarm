#!/usr/bin/env python3
"""
context_router.py — Intelligent context selection for spawn coordination.

Solves F69: when CLAUDE.md + INDEX.md + knowledge exceeds context limits,
this tool selects the minimal relevant context for a given task.

Usage:
    python3 tools/context_router.py <task-description>
    python3 tools/context_router.py <task-description> --budget 500
    python3 tools/context_router.py <task-description> --json
    python3 tools/context_router.py inventory

Problem: As the swarm grows, no single session can hold all context.
Solution: Route tasks to the right subset of knowledge.

Architecture:
    Task description → keyword extraction → file relevance scoring →
    ranked file list → budget-constrained selection → loading instructions

This is the foundation for distributed spawn coordination:
- Parent reads context_router output to plan spawns
- Each spawn gets only the files it needs
- No spawn needs to hold the full knowledge base
"""

import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


# Domain keyword maps: which terms suggest which files
DOMAIN_KEYWORDS = {
    "beliefs": {
        "files": ["beliefs/CORE.md", "beliefs/DEPS.md", "beliefs/CONFLICTS.md"],
        "keywords": [
            "belief", "evidence", "observed", "theorized", "falsif",
            "conviction", "hypothesis", "validate", "core", "principle",
        ],
    },
    "complexity": {
        "files": [
            "memory/PRINCIPLES.md",
            "experiments/complexity-applied/nk-cross-package-synthesis.md",
            "tools/nk_analyze.py",
        ],
        "keywords": [
            "nk", "complexity", "coupling", "cycle", "k_avg", "k_max",
            "composite", "module", "dependency", "import", "refactor",
            "architecture", "facade", "monolith", "tangled", "hub",
        ],
    },
    "evolution": {
        "files": [
            "tools/evolve.py", "tools/merge_back.py", "tools/swarm_test.py",
            "tools/colony.py", "tools/genesis_evolve.py",
            "tools/agent_swarm.py", "tools/self_evolve.py",
            "tools/novelty.py",
        ],
        "keywords": [
            "spawn", "child", "evolve", "harvest", "integrate", "merge",
            "genesis", "colony", "viability", "offspring", "novelty",
            "bulletin", "evolution", "selection",
        ],
    },
    "protocols": {
        "files": [
            "memory/DISTILL.md", "memory/HEALTH.md", "memory/VERIFY.md",
            "memory/OPERATIONS.md",
        ],
        "keywords": [
            "distill", "health", "verify", "protocol", "session",
            "handoff", "compaction", "lifecycle", "decay", "entropy",
        ],
    },
    "strategy": {
        "files": [
            "tasks/FRONTIER.md", "tasks/NEXT.md",
            "memory/INDEX.md",
        ],
        "keywords": [
            "frontier", "question", "task", "plan", "strategy",
            "next", "phase", "priority", "meta", "work",
        ],
    },
    "tools": {
        "files": [
            "tools/validate_beliefs.py", "tools/session_tracker.py",
            "tools/pulse.py", "tools/frontier_decay.py",
        ],
        "keywords": [
            "tool", "script", "automat", "validator", "track",
            "measure", "metric", "test", "check", "run",
        ],
    },
    "domain_ai": {
        "files": [
            "domains/ai/DOMAIN.md", "domains/ai/INDEX.md",
            "domains/ai/tasks/FRONTIER.md",
        ],
        "keywords": [
            "ai", "llm", "multi-agent", "mas", "coordination", "info",
            "asymmetry", "async", "sync", "cascade", "capability",
            "vigilance", "isomorphism", "f-ai", "expect",
        ],
    },
    "domain_finance": {
        "files": [
            "domains/finance/DOMAIN.md", "domains/finance/INDEX.md",
            "domains/finance/tasks/FRONTIER.md",
        ],
        "keywords": [
            "finance", "portfolio", "diversif", "variance", "sharpe",
            "systematic", "idiosyncratic", "risk", "return", "f-fin",
            "compaction", "lesson", "citation",
        ],
    },
    "domain_health": {
        "files": [
            "domains/health/DOMAIN.md", "domains/health/INDEX.md",
            "domains/health/tasks/FRONTIER.md",
        ],
        "keywords": [
            "health", "immune", "immunology", "memory", "cell", "adaptive",
            "innate", "homeostasis", "cascade", "autoimmune", "f-hlt",
            "reactivation", "persistence", "proxy",
        ],
    },
}

# Files always included (mandatory load)
MANDATORY_FILES = [
    "beliefs/CORE.md",
    "memory/INDEX.md",
]


def extract_task_keywords(task_description: str) -> set[str]:
    """Extract meaningful keywords from a task description."""
    # Lowercase, split on non-alphanumeric
    words = set(re.findall(r"[a-z][a-z_]+", task_description.lower()))
    # Remove very common words
    stopwords = {"the", "and", "for", "with", "that", "this", "from", "have",
                 "will", "are", "was", "been", "being", "should", "could",
                 "would", "not", "but", "can", "does", "how", "what", "when",
                 "where", "which", "about", "into", "also", "just", "more"}
    return words - stopwords


def score_domain(task_keywords: set[str], domain_info: dict) -> float:
    """Score how relevant a domain is to the task."""
    domain_kws = set(domain_info["keywords"])
    overlap = task_keywords & domain_kws
    if not overlap:
        return 0.0
    # Jaccard-like score weighted by overlap count
    return len(overlap) / len(domain_kws)


def count_file_lines(filepath: Path) -> int:
    """Count lines in a file."""
    try:
        return len(filepath.read_text().splitlines())
    except Exception:
        return 0


def route_context(task_description: str, budget_lines: int = 500) -> dict:
    """Route a task to its relevant context files.

    Args:
        task_description: What the task is about.
        budget_lines: Maximum total lines to include.

    Returns:
        Dict with ranked files, domains, and loading instructions.
    """
    task_kws = extract_task_keywords(task_description)

    # Score each domain
    domain_scores = {}
    for domain, info in DOMAIN_KEYWORDS.items():
        score = score_domain(task_kws, info)
        if score > 0:
            domain_scores[domain] = score

    # Rank domains
    ranked_domains = sorted(domain_scores.items(), key=lambda x: -x[1])

    # Collect files from relevant domains
    file_scores: dict[str, float] = {}
    for domain, score in ranked_domains:
        for f in DOMAIN_KEYWORDS[domain]["files"]:
            if f not in file_scores:
                file_scores[f] = score
            else:
                file_scores[f] = max(file_scores[f], score)

    # Always include mandatory files
    for f in MANDATORY_FILES:
        if f not in file_scores:
            file_scores[f] = 1.0  # Mandatory = highest priority

    # Rank files by score
    ranked_files = sorted(file_scores.items(), key=lambda x: -x[1])

    # Budget-constrained selection
    selected_files = []
    total_lines = 0
    excluded_files = []

    for filepath, score in ranked_files:
        full_path = REPO_ROOT / filepath
        lines = count_file_lines(full_path)
        if total_lines + lines <= budget_lines:
            selected_files.append({
                "path": filepath,
                "lines": lines,
                "score": round(score, 3),
                "domain": next(
                    (d for d, info in DOMAIN_KEYWORDS.items() if filepath in info["files"]),
                    "general"
                ),
            })
            total_lines += lines
        else:
            excluded_files.append({
                "path": filepath,
                "lines": lines,
                "score": round(score, 3),
                "reason": "budget exceeded",
            })

    # Also check for lesson files matching keywords
    lessons_dir = REPO_ROOT / "memory" / "lessons"
    relevant_lessons = []
    if lessons_dir.exists():
        for lesson_file in sorted(lessons_dir.glob("L-*.md")):
            try:
                title = lesson_file.read_text().split("\n")[0].lower()
                title_words = set(re.findall(r"[a-z][a-z_]+", title))
                if task_kws & title_words:
                    lines = count_file_lines(lesson_file)
                    rel_path = str(lesson_file.relative_to(REPO_ROOT))
                    if total_lines + lines <= budget_lines:
                        relevant_lessons.append({
                            "path": rel_path,
                            "lines": lines,
                            "match": list(task_kws & title_words),
                        })
                        total_lines += lines
            except Exception:
                pass

    return {
        "task": task_description,
        "keywords": sorted(task_kws),
        "domains": [{"name": d, "score": round(s, 3)} for d, s in ranked_domains],
        "selected_files": selected_files,
        "relevant_lessons": relevant_lessons[:5],
        "excluded_files": excluded_files,
        "total_lines": total_lines,
        "budget": budget_lines,
        "budget_used_pct": round(total_lines / budget_lines * 100, 1) if budget_lines > 0 else 0,
    }


def inventory() -> dict:
    """Show inventory of all knowledge files and their line counts."""
    categories = defaultdict(list)

    for domain, info in DOMAIN_KEYWORDS.items():
        for filepath in info["files"]:
            full_path = REPO_ROOT / filepath
            lines = count_file_lines(full_path)
            categories[domain].append({
                "path": filepath,
                "lines": lines,
                "exists": full_path.exists(),
            })

    # Count lessons
    lessons_dir = REPO_ROOT / "memory" / "lessons"
    lesson_count = 0
    lesson_lines = 0
    if lessons_dir.exists():
        for f in lessons_dir.glob("L-*.md"):
            lesson_count += 1
            lesson_lines += count_file_lines(f)

    # Count total
    total_lines = sum(
        f["lines"] for files in categories.values() for f in files
    ) + lesson_lines

    return {
        "categories": dict(categories),
        "lessons": {"count": lesson_count, "total_lines": lesson_lines},
        "total_knowledge_lines": total_lines,
        "mandatory_lines": sum(
            count_file_lines(REPO_ROOT / f) for f in MANDATORY_FILES
        ),
    }


def print_route(result: dict):
    """Print routing results in human-readable format."""
    print(f"=== CONTEXT ROUTE ===\n")
    print(f"Task: {result['task']}")
    print(f"Keywords: {', '.join(result['keywords'][:10])}")
    print()

    if result["domains"]:
        print("Relevant domains:")
        for d in result["domains"]:
            bar = "█" * int(d["score"] * 20)
            print(f"  {d['name']:<15} {d['score']:.2f} {bar}")
        print()

    print(f"Selected files ({result['total_lines']}/{result['budget']} lines, {result['budget_used_pct']}%):")
    for f in result["selected_files"]:
        print(f"  {f['path']:<55} {f['lines']:>5} lines  [{f['domain']}]")

    if result["relevant_lessons"]:
        print(f"\nRelevant lessons:")
        for l in result["relevant_lessons"]:
            print(f"  {l['path']:<55} {l['lines']:>5} lines  (match: {', '.join(l['match'][:3])})")

    if result["excluded_files"]:
        print(f"\nExcluded (budget overflow):")
        for f in result["excluded_files"]:
            print(f"  {f['path']:<55} {f['lines']:>5} lines")

    # Generate spawn instruction
    print(f"\n--- SPAWN INSTRUCTION ---")
    files_to_load = [f["path"] for f in result["selected_files"]]
    files_to_load += [l["path"] for l in result["relevant_lessons"]]
    print(f"Read these files: {', '.join(files_to_load)}")
    print(f"Skip everything else — this spawn doesn't need it.")


def print_inventory(inv: dict):
    """Print knowledge inventory."""
    print("=== KNOWLEDGE INVENTORY ===\n")
    for category, files in inv["categories"].items():
        total = sum(f["lines"] for f in files)
        print(f"{category}: {total} lines across {len(files)} files")
        for f in files:
            status = "" if f["exists"] else " [MISSING]"
            print(f"  {f['path']:<55} {f['lines']:>5} lines{status}")
        print()

    print(f"Lessons: {inv['lessons']['count']} files, {inv['lessons']['total_lines']} lines")
    print(f"Total knowledge: {inv['total_knowledge_lines']} lines")
    print(f"Mandatory load: {inv['mandatory_lines']} lines")
    print(f"\nContext budget estimate:")
    print(f"  ~{inv['total_knowledge_lines'] * 4} tokens total knowledge")
    print(f"  ~{inv['mandatory_lines'] * 4} tokens mandatory")
    remaining = inv["total_knowledge_lines"] - inv["mandatory_lines"]
    print(f"  ~{remaining * 4} tokens optional (routed per task)")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    if sys.argv[1] == "inventory":
        inv = inventory()
        if "--json" in sys.argv:
            print(json.dumps(inv, indent=2))
        else:
            print_inventory(inv)
        return

    task = " ".join(a for a in sys.argv[1:] if not a.startswith("-"))
    budget = 500
    for i, a in enumerate(sys.argv):
        if a == "--budget" and i + 1 < len(sys.argv):
            budget = int(sys.argv[i + 1])

    result = route_context(task, budget)

    if "--json" in sys.argv:
        print(json.dumps(result, indent=2))
    else:
        print_route(result)


if __name__ == "__main__":
    main()
