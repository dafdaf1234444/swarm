#!/usr/bin/env python3
"""Classify swarm knowledge into epistemological states (L-707, F-META10).

Five states: MUST-KNOW, ACTIVE, SHOULD-KNOW, DECAYED, BLIND-SPOT.
Produces per-domain profiles and transition diagnostics.

Usage:
  python3 tools/knowledge_state.py           # full report
  python3 tools/knowledge_state.py --domain meta  # single domain
  python3 tools/knowledge_state.py --json    # machine-readable output
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from swarm_io import REPO_ROOT, read_text, lesson_paths, session_number

# --- Configuration ---
STALE_WINDOW = 50  # sessions without citation → DECAYED candidate
BOOT_FILES = [
    "beliefs/CORE.md", "memory/INDEX.md", "SWARM.md",
    "CLAUDE.md", "AGENTS.md", "GEMINI.md",
]
ACTIVE_TOOL_DIR = REPO_ROOT / "tools"


def parse_lesson(path: Path, current_session: int) -> dict:
    """Parse a lesson file into structured data."""
    text = read_text(path)
    num = int(re.search(r"\d+", path.stem).group())
    title_m = re.search(r"^#\s+L-\d+[:\s]*(.+)", text, re.M)
    session_m = re.search(r"Session:\s*S?(\d+)", text)
    domain_m = re.search(r"[Dd]omain:\s*([^\n|]+)", text)
    conf_m = re.search(r"Confidence:\s*(\w+)", text, re.I)
    cites_m = re.search(r"Cites?:\s*(.+)", text)

    session = int(session_m.group(1)) if session_m else 0
    age = current_session - session if session else current_session

    cited_lessons = set()
    if cites_m:
        cited_lessons = set(re.findall(r"\bL-(\d+)\b", cites_m.group(1)))

    domain = domain_m.group(1).strip().split(",")[0].strip() if domain_m else "unknown"

    return {
        "id": f"L-{num}",
        "num": num,
        "title": title_m.group(1).strip() if title_m else "",
        "session": session,
        "age": age,
        "domain": domain.lower(),
        "confidence": conf_m.group(1).lower() if conf_m else "unknown",
        "cites": cited_lessons,
        "type": "lesson",
    }


def parse_principles(current_session: int) -> list[dict]:
    """Parse principles from PRINCIPLES.md."""
    text = read_text(REPO_ROOT / "memory" / "PRINCIPLES.md")
    results = []
    for m in re.finditer(r"\*\*(P-(\d+))\*\*:?\s*([^|*\n]+)", text):
        pid, pnum, ptext = m.group(1), int(m.group(2)), m.group(3).strip()
        # Extract evidence annotation
        ev_m = re.search(r"\(L-(\d+).*?(OBSERVED|THEORIZED|MEASURED)", ptext, re.I)
        session = 0
        if ev_m:
            # Approximate session from the lesson it cites
            session = 0  # would need to look up the lesson
        results.append({
            "id": pid,
            "num": pnum,
            "title": ptext[:80],
            "session": session,
            "age": current_session,  # approximate
            "domain": "cross-domain",
            "confidence": "distilled",
            "cites": set(),
            "type": "principle",
        })
    return results


def parse_beliefs(current_session: int) -> list[dict]:
    """Parse beliefs from DEPS.md."""
    text = read_text(REPO_ROOT / "beliefs" / "DEPS.md")
    results = []
    for m in re.finditer(r"###\s+(B[\w-]+):\s*(.+?)(?=\n###|\Z)", text, re.S):
        bid = m.group(1)
        block = m.group(2).strip()
        summary = block.split("\n")[0]
        last_m = re.search(r"Last tested.*?S(\d+)", block)
        last_tested = int(last_m.group(1)) if last_m else 0
        evidence_m = re.search(r"Evidence.*?:\s*(\w+)", block)
        evidence = evidence_m.group(1).lower() if evidence_m else "unknown"

        results.append({
            "id": bid,
            "num": 0,
            "title": summary[:80],
            "session": last_tested,
            "age": current_session - last_tested if last_tested else current_session,
            "domain": "meta",
            "confidence": evidence,
            "cites": set(),
            "type": "belief",
        })
    return results


def find_must_know_refs() -> set[str]:
    """Find knowledge IDs referenced by boot files and active tools."""
    refs = set()
    # Boot files
    for rel in BOOT_FILES:
        text = read_text(REPO_ROOT / rel)
        refs.update(re.findall(r"\bL-\d+\b", text))
        refs.update(re.findall(r"\bP-\d+\b", text))
        refs.update(re.findall(r"\bB\d+\b", text))

    # Active tools (non-archived)
    archive_dir = REPO_ROOT / "tools" / "archive"
    for py in ACTIVE_TOOL_DIR.glob("*.py"):
        if archive_dir in py.parents:
            continue
        text = read_text(py)
        refs.update(re.findall(r"\bL-\d+\b", text))
        refs.update(re.findall(r"\bP-\d+\b", text))
    return refs


def build_citation_index(lessons: list[dict]) -> dict[str, set[int]]:
    """Build reverse citation index: which sessions cite each lesson ID."""
    cited_by_session = defaultdict(set)
    for lsn in lessons:
        for cited_num in lsn["cites"]:
            cited_by_session[f"L-{cited_num}"].add(lsn["session"])
    return cited_by_session


def count_repo_citations(lesson_id: str) -> int:
    """Count how many times a lesson ID appears across the repo (fast grep)."""
    # Use git grep for speed
    try:
        import subprocess
        result = subprocess.run(
            ["git", "grep", "-c", f"\\b{lesson_id}\\b", "--", "memory/", "beliefs/", "domains/"],
            capture_output=True, text=True, cwd=REPO_ROOT, timeout=5,
        )
        total = 0
        for line in result.stdout.strip().split("\n"):
            if ":" in line:
                parts = line.rsplit(":", 1)
                if len(parts) == 2:
                    try:
                        total += int(parts[1])
                    except ValueError:
                        pass
        return total
    except Exception:
        return 0


def classify(item: dict, must_know_refs: set, cited_by_session: dict,
             current_session: int) -> str:
    """Classify a knowledge item into an epistemological state."""
    item_id = item["id"]

    # 1. MUST-KNOW: referenced by boot/tools
    if item_id in must_know_refs:
        return "MUST-KNOW"

    # 2. For beliefs: use last-tested + evidence
    if item["type"] == "belief":
        if item["age"] <= STALE_WINDOW:
            return "ACTIVE"
        return "DECAYED"

    # 3. Check citation recency
    citing_sessions = cited_by_session.get(item_id, set())
    recent_citations = {s for s in citing_sessions if s > current_session - STALE_WINDOW}

    # 4. ACTIVE: created recently OR cited recently
    if item["age"] <= STALE_WINDOW or len(recent_citations) > 0:
        return "ACTIVE"

    # 5. DECAYED: old + no recent citations
    return "DECAYED"


def count_frontiers_per_domain() -> dict[str, int]:
    """Count open frontiers per domain (= SHOULD-KNOW count)."""
    counts = defaultdict(int)
    # Domain frontier files
    domains_dir = REPO_ROOT / "domains"
    if domains_dir.exists():
        for domain_dir in domains_dir.iterdir():
            if not domain_dir.is_dir():
                continue
            frontier_file = domain_dir / "tasks" / "FRONTIER.md"
            if frontier_file.exists():
                text = read_text(frontier_file)
                # Count active frontier entries (lines starting with - **F-)
                active_section = text.split("## Dead Ends")[0] if "## Dead Ends" in text else text
                active_section = active_section.split("## Resolved")[0] if "## Resolved" in active_section else active_section
                active_section = active_section.split("## Legacy")[0] if "## Legacy" in active_section else active_section
                domain_name = domain_dir.name
                count = len(re.findall(r"^- \*\*F-", active_section, re.M))
                counts[domain_name] = count

    # Global frontier file
    global_frontier = read_text(REPO_ROOT / "tasks" / "FRONTIER.md")
    active_part = global_frontier.split("## Resolved")[0] if "## Resolved" in global_frontier else global_frontier
    counts["global"] = len(re.findall(r"^- \*\*F\d+\*\*", active_part, re.M))

    return counts


def main():
    parser = argparse.ArgumentParser(description="Knowledge state classifier (L-707)")
    parser.add_argument("--domain", help="Filter to specific domain")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show per-item details")
    args = parser.parse_args()

    current_session = session_number()
    print(f"=== KNOWLEDGE STATE CLASSIFIER — S{current_session} ===\n")

    # Parse all knowledge
    lessons = [parse_lesson(p, current_session) for p in lesson_paths()]
    principles = parse_principles(current_session)
    beliefs = parse_beliefs(current_session)
    all_items = lessons + principles + beliefs

    # Build indices
    must_know_refs = find_must_know_refs()
    cited_by_session = build_citation_index(lessons)
    frontiers_per_domain = count_frontiers_per_domain()

    # Classify each item
    for item in all_items:
        item["state"] = classify(item, must_know_refs, cited_by_session, current_session)

    # Filter by domain if requested
    if args.domain:
        all_items = [i for i in all_items if args.domain.lower() in i.get("domain", "").lower()]

    # Aggregate by state
    state_counts = defaultdict(int)
    for item in all_items:
        state_counts[item["state"]] += 1

    # Add SHOULD-KNOW from frontiers
    total_should_know = sum(frontiers_per_domain.values())
    state_counts["SHOULD-KNOW"] = total_should_know

    # Global summary
    total = sum(state_counts.values())
    print("--- Global Knowledge State Distribution ---")
    for state in ["MUST-KNOW", "ACTIVE", "SHOULD-KNOW", "DECAYED", "BLIND-SPOT"]:
        count = state_counts.get(state, 0)
        pct = (count / total * 100) if total > 0 else 0
        bar = "█" * int(pct / 2)
        print(f"  {state:12s}  {count:4d}  ({pct:5.1f}%)  {bar}")
    print(f"  {'TOTAL':12s}  {total:4d}")
    print()

    # Per-domain profiles
    domain_profiles = defaultdict(lambda: defaultdict(int))
    for item in all_items:
        domain_profiles[item["domain"]][item["state"]] += 1

    # Add frontier counts to domain profiles
    for domain, fcount in frontiers_per_domain.items():
        domain_profiles[domain]["SHOULD-KNOW"] += fcount

    # Sort domains by total knowledge
    sorted_domains = sorted(domain_profiles.items(),
                            key=lambda x: sum(x[1].values()), reverse=True)

    print("--- Per-Domain Knowledge State Profiles ---")
    print(f"  {'Domain':25s} {'MUST':>5} {'ACTV':>5} {'SHLD':>5} {'DECY':>5} {'BLND':>5} {'Total':>6}  Diagnosis")
    print(f"  {'-'*25} {'-'*5} {'-'*5} {'-'*5} {'-'*5} {'-'*5} {'-'*6}  {'-'*20}")

    for domain, counts in sorted_domains:
        mk = counts.get("MUST-KNOW", 0)
        ac = counts.get("ACTIVE", 0)
        sk = counts.get("SHOULD-KNOW", 0)
        dc = counts.get("DECAYED", 0)
        bs = counts.get("BLIND-SPOT", 0)
        tot = mk + ac + sk + dc + bs
        if tot == 0:
            continue

        # Diagnosis
        diagnosis = ""
        if tot > 0:
            decay_ratio = dc / tot
            if decay_ratio > 0.5:
                diagnosis = "DECAY-HEAVY: needs revival"
            elif sk > ac and sk > 2:
                diagnosis = "EXPLORE-RICH: needs experiments"
            elif ac > 10 and dc < 3:
                diagnosis = "HEALTHY"
            elif mk > ac:
                diagnosis = "OPERATIONAL: infrastructure-critical"
            elif tot <= 2:
                diagnosis = "NASCENT"
            else:
                diagnosis = "MIXED"

        print(f"  {domain:25s} {mk:5d} {ac:5d} {sk:5d} {dc:5d} {bs:5d} {tot:6d}  {diagnosis}")

    print()

    # State transition diagnostics
    print("--- State Transition Diagnostics ---")
    active_items = [i for i in all_items if i["state"] == "ACTIVE"]
    decayed_items = [i for i in all_items if i["state"] == "DECAYED"]
    must_know_items = [i for i in all_items if i["state"] == "MUST-KNOW"]

    print(f"  ACTIVE items:    {len(active_items)} (avg age: {sum(i['age'] for i in active_items) / max(len(active_items), 1):.0f} sessions)")
    print(f"  DECAYED items:   {len(decayed_items)} (avg age: {sum(i['age'] for i in decayed_items) / max(len(decayed_items), 1):.0f} sessions)")
    print(f"  MUST-KNOW items: {len(must_know_items)}")
    print(f"  SHOULD-KNOW:     {total_should_know} open frontiers across {len(frontiers_per_domain)} domains")

    # DECAYED→ACTIVE revival rate (items that were old but got cited recently)
    revival_candidates = 0
    for item in all_items:
        if item["age"] > STALE_WINDOW:
            citing = cited_by_session.get(item["id"], set())
            recent = {s for s in citing if s > current_session - STALE_WINDOW}
            if len(recent) > 0:
                revival_candidates += 1

    old_items = len([i for i in all_items if i["age"] > STALE_WINDOW])
    revival_rate = (revival_candidates / old_items * 100) if old_items > 0 else 0
    print(f"  Revival rate:    {revival_candidates}/{old_items} old items recently cited ({revival_rate:.1f}%)")
    print()

    # Verbose: show specific items
    if args.verbose:
        print("--- MUST-KNOW Items ---")
        for item in sorted(must_know_items, key=lambda x: x["id"]):
            print(f"  {item['id']:10s} {item['type']:10s} {item['title'][:60]}")
        print()

        print("--- DECAYED Items (sample) ---")
        for item in sorted(decayed_items, key=lambda x: x["age"], reverse=True)[:15]:
            print(f"  {item['id']:10s} age={item['age']:3d}s  {item['title'][:55]}")
        print()

    # JSON output
    if args.json:
        output = {
            "session": current_session,
            "global_states": dict(state_counts),
            "domain_profiles": {d: dict(c) for d, c in domain_profiles.items()},
            "revival_rate": revival_rate,
            "total_items": len(all_items),
            "frontier_count": total_should_know,
        }
        json_path = REPO_ROOT / "experiments" / "meta" / f"knowledge-state-s{current_session}.json"
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(json.dumps(output, indent=2))
        print(f"JSON written to {json_path.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
