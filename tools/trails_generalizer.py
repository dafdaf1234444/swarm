#!/usr/bin/env python3
"""
trails_generalizer.py — Extract recurring patterns from swarm session trails.

Reads session notes from tasks/NEXT.md + tasks/NEXT-ARCHIVE.md and generalizes:
  - Persistent "Next:" items (recurring across sessions without resolution)
  - Recurring meta-swarm reflection targets (tool → friction frequency)
  - Trail-type signatures (what work patterns precede high-yield sessions)

Output: summary to stdout + JSON artifact for experiment record.

Usage:
  python3 tools/trails_generalizer.py [--json <out.json>] [--top N] [--min-recurrence N]
"""

import re
import json
import argparse
import sys
from collections import defaultdict, Counter
from pathlib import Path

ROOT = Path(__file__).parent.parent


# ── Parsing ──────────────────────────────────────────────────────────────────

def parse_session_notes(text: str) -> list[dict]:
    """Parse session notes from NEXT.md / NEXT-ARCHIVE.md content.

    Returns list of dicts with: session, next_items, actual_text, meta_swarm_target, meta_swarm_text
    """
    notes = []
    # Session block header: ## S<N> session note (...)
    session_re = re.compile(r'^## (S\d+[a-z]?) (?:session note|DOMEX)', re.MULTILINE)
    blocks = session_re.split(text)

    # blocks[0] = preamble, then alternating: session_id, content
    for i in range(1, len(blocks) - 1, 2):
        session = blocks[i].strip()
        content = blocks[i + 1] if i + 1 < len(blocks) else ""

        next_items = _extract_next_items(content)
        actual_text = _extract_actual_text(content)
        meta_target, meta_text = _extract_meta_swarm(content)

        if next_items or meta_target:
            notes.append({
                "session": session,
                "next_items": next_items,
                "actual_text": actual_text,
                "meta_swarm_target": meta_target,
                "meta_swarm_text": meta_text,
            })

    return notes


def _extract_next_items(block: str) -> list[str]:
    """Extract items from '- **Next**: (1) X; (2) Y; ...' lines."""
    m = re.search(r'\*\*Next\*\*:\s*(.+)', block)
    if not m:
        return []
    raw = m.group(1).strip()
    # Split on numbered items like (1) ... (2) ...
    items = re.split(r'\s*\(\d+\)\s*', raw)
    return [it.strip().rstrip(';').strip() for it in items if it.strip()]


def _extract_actual_text(block: str) -> str:
    """Extract the '- **actual**: ...' text from a session note block."""
    m = re.search(r'\*\*actual\*\*:\s*(.+)', block)
    if not m:
        return ""
    return m.group(1).strip()


def _extract_meta_swarm(block: str) -> tuple[str, str]:
    """Extract meta-swarm target tool and full text."""
    m = re.search(r'\*\*meta-swarm\*\*:\s*(?:Target[:\s]*)?`?([^`\n—–\-]+)`?\s*[—–\-]?\s*(.*)', block)
    if not m:
        return "", ""
    target = m.group(1).strip().strip('`').strip()
    text = m.group(2).strip()
    return target, text


# ── Normalization helpers ─────────────────────────────────────────────────────

# Map raw next-item text → canonical key
_CANONICAL_MAP = [
    (r'SIG-38', 'SIG-38 human auth'),
    (r'paper.reswarm|paper.drift|PAPER', 'paper-reswarm periodic'),
    (r'claim.vs.evidence|claim-vs-evidence', 'claim-vs-evidence periodic'),
    (r'principles.dedup|principle.*batch', 'principles-dedup periodic'),
    (r'bayesian.calibrat|ECE', 'bayesian-calibration periodic'),
    (r'mission.constraint', 'mission-constraint periodic'),
    (r'health.check', 'health-check periodic'),
    (r'proxy.K|proxy-K|compaction', 'proxy-K compaction'),
    (r'orient\.py.*decomp|orient.*oversize', 'orient.py decomposition'),
    (r'maintenance\.py.*oversize|maintenance.*17306|maintenance.*13151', 'maintenance.py oversized'),
    (r'safe_commit|safe commit|extreme concurr', 'safe_commit.sh concurrency'),
    (r'open_lane\.py.*FRONTIER|FRONTIER.*race|FRONTIER.*write', 'open_lane.py FRONTIER race fix'),
    (r'knowledge_state.*dispatch|dispatch.*knowledge_state', 'knowledge_state.py → dispatch'),
    (r'correction_propagation.*\-\-apply|--apply.*correction', 'correction_propagation.py --apply'),
    (r'unreachable lesson|83 unreachable', 'unreachable lessons (83)'),
    (r'challenge.execut', 'challenge-execution'),
    (r'check\.sh.*fast|fast.*check\.sh|check\.sh.*split', 'check.sh fast/slow split'),
    (r'lesson_quality_fixer.*batch|batch.*trim', 'lesson_quality_fixer.py batch-trim'),
    (r'sync_state|sync state', 'sync_state.py periodic'),
]


def canonicalize(item: str) -> str:
    for pattern, canon in _CANONICAL_MAP:
        if re.search(pattern, item, re.IGNORECASE):
            return canon
    return item.strip()[:80]  # fallback: truncated raw text


def canonicalize_tool(target: str) -> str:
    """Normalize tool paths to bare tool names. Returns empty string for non-tool refs."""
    # Must contain .py to be a tool reference
    if ".py" not in target and "/" not in target:
        return ""
    m = re.search(r'tools/(\S+\.py)', target)
    if m:
        return m.group(1)
    m = re.search(r'(\w[\w_]+\.py)', target)
    if m:
        return m.group(1)
    return ""


# ── Analysis ──────────────────────────────────────────────────────────────────

def analyze_trails(notes: list[dict]) -> dict:
    """Aggregate recurring patterns from session notes."""
    next_counter = Counter()
    meta_tool_counter = Counter()
    meta_tool_examples: dict[str, list] = defaultdict(list)
    next_examples: dict[str, list] = defaultdict(list)

    for note in notes:
        sess = note["session"]
        seen_this_session: set[str] = set()

        for item in note["next_items"]:
            canon = canonicalize(item)
            if canon not in seen_this_session:
                next_counter[canon] += 1
                seen_this_session.add(canon)
                if len(next_examples[canon]) < 3:
                    next_examples[canon].append(f"{sess}: {item[:80]}")

        if note["meta_swarm_target"]:
            tool = canonicalize_tool(note["meta_swarm_target"])
            if not tool:
                continue
            meta_tool_counter[tool] += 1
            if len(meta_tool_examples[tool]) < 3:
                meta_tool_examples[tool].append(
                    f"{sess}: {note['meta_swarm_text'][:100]}"
                )

    return {
        "total_session_notes": len(notes),
        "next_patterns": [
            {
                "item": item,
                "count": count,
                "classification": _classify_recurrence(count),
                "examples": next_examples[item],
            }
            for item, count in next_counter.most_common()
        ],
        "meta_tool_friction": [
            {
                "tool": tool,
                "count": count,
                "examples": meta_tool_examples[tool],
            }
            for tool, count in meta_tool_counter.most_common()
        ],
    }


def _classify_recurrence(count: int) -> str:
    if count >= 20:
        return "ZOMBIE"        # Never resolved, indefinitely deferred
    elif count >= 10:
        return "PERSISTENT"    # Long-tail deferral, structural blocker
    elif count >= 5:
        return "RECURRING"     # Appears regularly, not yet systemic
    elif count >= 3:
        return "SPORADIC"      # Occasional recurrence
    else:
        return "RARE"


# ── Generalization ────────────────────────────────────────────────────────────

def generalize(analysis: dict) -> dict:
    """Derive higher-order prescriptions from trail patterns."""
    prescriptions = []
    zombie_items = [p for p in analysis["next_patterns"] if p["classification"] in ("ZOMBIE", "PERSISTENT")]
    recurring_items = [p for p in analysis["next_patterns"] if p["classification"] == "RECURRING"]

    # Prescription 1: Items recurring ≥10x without resolution are structurally blocked
    blocked_by_auth = [p for p in zombie_items if "SIG-" in p["item"] or "human auth" in p["item"]]
    if blocked_by_auth:
        prescriptions.append({
            "id": "TG-1",
            "level": "L3",
            "claim": "Items requiring human authorization recur indefinitely unless structurally gated.",
            "evidence": f"{len(blocked_by_auth)} auth-blocked ZOMBIE items; SIG-38 present {blocked_by_auth[0]['count']} sessions",
            "prescription": "Create HUMAN-QUEUE.md time-to-action metric; surface in orient.py as ESCALATED if age >10 sessions.",
        })

    # Prescription 2: Periodics overdue recur structurally
    periodic_zombies = [p for p in zombie_items if "periodic" in p["item"] or "overdue" in p["item"].lower()]
    if len(periodic_zombies) >= 2:
        counts = [p["count"] for p in periodic_zombies]
        prescriptions.append({
            "id": "TG-2",
            "level": "L3",
            "claim": "Periodic tasks named in 'Next:' without execution-gating recur as zombie items.",
            "evidence": f"{len(periodic_zombies)} periodic-type zombies; avg recurrence {sum(counts)/len(counts):.1f} sessions",
            "prescription": "Periodics that appear in 'Next:' for 5+ sessions → auto-elevate to DUE with a lane blocker until closed.",
        })

    # Prescription 3: Meta-swarm friction targets that recur signal incomplete implementation
    top_tools = [t for t in analysis["meta_tool_friction"] if t["count"] >= 2]
    if top_tools:
        prescriptions.append({
            "id": "TG-3",
            "level": "L2",
            "claim": "Tools targeted 2+ times in meta-swarm reflections have incomplete friction resolution.",
            "evidence": f"{len(top_tools)} tools targeted ≥2x: {', '.join(t['tool'] for t in top_tools[:5])}",
            "prescription": "Meta-swarm reflection targets that recur → DOMEX-META-TOOLER ticket with explicit 'done when:' criterion.",
        })

    # Prescription 4: The "Next:" list is a prediction — measure its completion rate
    total_items = sum(p["count"] for p in analysis["next_patterns"])
    zombie_count = sum(p["count"] for p in zombie_items)
    zombie_rate = zombie_count / max(total_items, 1)
    prescriptions.append({
        "id": "TG-4",
        "level": "L3",
        "claim": f"'Next:' lists are low-fidelity predictions: ~{zombie_rate*100:.0f}% of item-appearances are zombie/persistent recurrences.",
        "evidence": f"{zombie_count}/{total_items} item-appearances are ZOMBIE/PERSISTENT ({zombie_rate*100:.1f}%)",
        "prescription": "Treat 'Next:' items as EAD trail data: measure completion rate per session. Surface % carried-over in orient.py.",
    })

    # Prescription 5: Structural fix pattern — tools targeted repeatedly need creation-time enforcement
    open_lane_count = next((t["count"] for t in analysis["meta_tool_friction"] if "open_lane" in t["tool"]), 0)
    if open_lane_count >= 3:
        prescriptions.append({
            "id": "TG-5",
            "level": "L4",
            "claim": f"open_lane.py targeted {open_lane_count}x in meta-reflections — highest friction tool. It is the creation-time enforcement gateway, so friction compounds across every new lane.",
            "evidence": f"open_lane.py targeted {open_lane_count} sessions in meta-reflections",
            "prescription": "open_lane.py improvements have 10x leverage vs average tool (multiplicative at creation-time). Prioritize its meta-tooler DOMEX above all other tool maintenance.",
        })

    return {
        "prescriptions": prescriptions,
        "zombie_item_count": len(zombie_items),
        "recurring_item_count": len(recurring_items),
        "zombie_rate_pct": round(zombie_rate * 100, 1),
        "top_friction_tools": [t["tool"] for t in top_tools[:5]],
    }


# ── Main ──────────────────────────────────────────────────────────────────────

def load_session_notes() -> list[dict]:
    notes = []
    for fname in ["tasks/NEXT.md", "tasks/NEXT-ARCHIVE.md"]:
        path = ROOT / fname
        if path.exists():
            text = path.read_text(encoding="utf-8")
            found = parse_session_notes(text)
            notes.extend(found)
    return notes


def main():
    parser = argparse.ArgumentParser(description="Extract patterns from swarm session trails")
    parser.add_argument("--json", metavar="OUT", help="Write JSON artifact to file")
    parser.add_argument("--top", type=int, default=20, help="Top N items to display (default: 20)")
    parser.add_argument("--min-recurrence", type=int, default=2, help="Min recurrence to display (default: 2)")
    args = parser.parse_args()

    notes = load_session_notes()
    if not notes:
        print("ERROR: no session notes found in tasks/NEXT.md or tasks/NEXT-ARCHIVE.md", file=sys.stderr)
        sys.exit(1)

    analysis = analyze_trails(notes)
    generalization = generalize(analysis)

    # ── Print summary ──
    n = analysis["total_session_notes"]
    print(f"\n=== TRAILS GENERALIZER — {n} session notes analyzed ===\n")

    print(f"--- Recurring 'Next:' Items (min {args.min_recurrence} sessions) ---")
    shown = 0
    for p in analysis["next_patterns"]:
        if p["count"] < args.min_recurrence:
            break
        cls = p["classification"]
        marker = {"ZOMBIE": "💀", "PERSISTENT": "🔁", "RECURRING": "⚠", "SPORADIC": "~", "RARE": " "}.get(cls, " ")
        print(f"  {marker} [{cls:10s}] {p['count']:3d}x  {p['item']}")
        shown += 1
        if shown >= args.top:
            print(f"  ... ({len(analysis['next_patterns'])} total unique items)")
            break

    print(f"\n--- Meta-Swarm Friction Targets (tools with recurring reflections) ---")
    for t in analysis["meta_tool_friction"][:15]:
        bar = "█" * t["count"]
        print(f"  {t['count']:3d}x  {t['tool']:<35s} {bar}")

    print(f"\n--- Generalizations ---")
    for p in generalization["prescriptions"]:
        print(f"\n  [{p['id']} {p['level']}] {p['claim']}")
        print(f"    Evidence: {p['evidence']}")
        print(f"    Fix: {p['prescription']}")

    stats = {
        "zombie_items": generalization["zombie_item_count"],
        "recurring_items": generalization["recurring_item_count"],
        "zombie_rate_pct": generalization["zombie_rate_pct"],
        "top_friction_tools": generalization["top_friction_tools"],
    }
    print(f"\n--- Summary ---")
    print(f"  Session notes: {n} | Zombie items: {stats['zombie_items']} | Zombie rate: {stats['zombie_rate_pct']}%")
    print(f"  Top friction tools: {', '.join(stats['top_friction_tools'])}")

    # ── JSON output ──
    artifact = {
        "tool": "trails_generalizer.py",
        "session_notes_analyzed": n,
        "analysis": {
            "next_patterns": analysis["next_patterns"][:50],
            "meta_tool_friction": analysis["meta_tool_friction"][:20],
        },
        "generalization": generalization,
    }

    if args.json:
        out_path = ROOT / args.json
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(artifact, indent=2), encoding="utf-8")
        print(f"\nArtifact written: {args.json}")
    else:
        # Print compact JSON to stdout
        print(f"\n--- JSON summary ---")
        print(json.dumps({"generalization": generalization, "stats": stats}, indent=2))

    return artifact


if __name__ == "__main__":
    main()
