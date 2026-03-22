#!/usr/bin/env python3
"""Knowledge Swarm Engine — make knowledge self-organize (S457).

The swarm's knowledge is passive substrate. This tool gives knowledge its own
orient-act-compress cycle:
  - REVIVE: surface DECAYED items connected to ACTIVE knowledge
  - COMPRESS: flag EXPIRED lessons (zero citations, old, low Sharpe)
  - CROSSLINK: find BLIND-SPOT items with ACTIVE neighbors
  - ORPHAN: detect principles with no live evidence chain

Diagnose, don't mutate (P-144). Outputs recommendations + JSON artifact.

Usage:
  python3 tools/knowledge_swarm.py           # full report
  python3 tools/knowledge_swarm.py --json    # machine-readable artifact
  python3 tools/knowledge_swarm.py --brief   # summary for orient.py
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from swarm_io import REPO_ROOT, read_text, session_number, lesson_paths

STALE_WINDOW = 50
TTL_SESSIONS = 100
BOOT_FILES = [
    "beliefs/CORE.md", "memory/INDEX.md", "SWARM.md",
    "CLAUDE.md", "AGENTS.md", "GEMINI.md",
]


def parse_lesson_meta(path):
    """Parse lesson file for metadata."""
    text = read_text(path)
    if not text:
        return None
    lines = text.split("\n")
    m = re.search(r"L-(\d+)", path.name)
    if not m:
        return None
    lid = f"L-{m.group(1)}"
    title = ""
    for line in lines[:5]:
        tm = re.match(r"#\s+L-\d+[:\s]+(.*)", line)
        if tm:
            title = tm.group(1).strip()
            break
    session = 0
    domain = "unknown"
    sharpe = -1
    cites = set()
    from lesson_header import parse_domain_field
    for line in lines[:5]:  # header only — body text can contain false Domain: matches
        sm = re.search(r"Session:\s*S?(\d+)", line)
        if sm:
            session = int(sm.group(1))
        if domain == "unknown":  # only take first Domain: match
            _doms = parse_domain_field(line)
            if _doms:
                domain = _doms[0]
        shm = re.search(r"Sharpe:\s*(\d+)", line)
        if shm:
            sharpe = int(shm.group(1))
    for line in lines:
        cites.update(re.findall(r"\bL-(\d+)\b", line))
    normalized = {f"L-{c}" for c in cites}
    normalized.discard(lid)
    return {"id": lid, "title": title[:80], "session": session,
            "domain": domain, "sharpe": sharpe, "cites": normalized,
            "line_count": len(lines)}


def build_citation_maps(lessons):
    """Build outbound and inbound citation maps."""
    outbound = {}
    inbound = defaultdict(set)
    all_ids = set(lessons.keys())
    for lid, meta in lessons.items():
        out = meta["cites"] & all_ids
        outbound[lid] = out
        for target in out:
            inbound[target].add(lid)
    return outbound, dict(inbound)


def find_boot_refs():
    """Find L-NNN references in boot files and tools."""
    refs = set()
    for bf in BOOT_FILES:
        text = read_text(REPO_ROOT / bf)
        if text:
            refs.update(re.findall(r"\bL-\d+\b", text))
    tools_dir = REPO_ROOT / "tools"
    if tools_dir.exists():
        for f in tools_dir.glob("*.py"):
            text = read_text(f)
            if text:
                refs.update(re.findall(r"\bL-\d+\b", text))
    return refs


def find_indexed_refs():
    """Find L-NNN references in INDEX.md."""
    text = read_text(REPO_ROOT / "memory" / "INDEX.md")
    return set(re.findall(r"\bL-\d+\b", text)) if text else set()


def find_frontier_refs():
    """Find L-NNN references in FRONTIER.md."""
    text = read_text(REPO_ROOT / "tasks" / "FRONTIER.md")
    return set(re.findall(r"\bL-\d+\b", text)) if text else set()


def classify_items(lessons, inbound, current_session):
    """Classify lessons into 5 epistemological states."""
    boot_refs = find_boot_refs()
    indexed_refs = find_indexed_refs()
    frontier_refs = find_frontier_refs()
    states = {}
    # First pass: definitive classifications
    for lid, meta in lessons.items():
        age = current_session - meta["session"]
        in_count = len(inbound.get(lid, set()))
        if lid in boot_refs:
            states[lid] = "MUST-KNOW"
        elif in_count == 0 and lid not in indexed_refs:
            states[lid] = "BLIND-SPOT"
        elif age <= STALE_WINDOW:
            states[lid] = "ACTIVE"
        else:
            states[lid] = None
    # Second pass: cited-by-active check
    for lid in list(lessons.keys()):
        if states.get(lid) is not None:
            continue
        citers = inbound.get(lid, set())
        has_active = any(states.get(c) in ("ACTIVE", "MUST-KNOW") for c in citers)
        if has_active:
            states[lid] = "ACTIVE"
        elif lid in frontier_refs:
            states[lid] = "SHOULD-KNOW"
        else:
            states[lid] = "DECAYED"
    return states


def revive_candidates(lessons, states, inbound, current_session, limit=5):
    """Find DECAYED items connected to ACTIVE knowledge."""
    candidates = []
    for lid, state in states.items():
        if state != "DECAYED":
            continue
        meta = lessons[lid]
        citers = inbound.get(lid, set())
        active_citers = sum(1 for c in citers if states.get(c) in ("ACTIVE", "MUST-KNOW"))
        if active_citers == 0:
            continue
        age = max(1, current_session - meta["session"])
        sharpe = max(1, meta["sharpe"]) if meta["sharpe"] > 0 else 1
        score = sharpe * active_citers / (age / 50)
        action = ("cite_in_active_lane" if sharpe >= 4
                  else "merge_into_principle" if age > 200
                  else "archive")
        candidates.append({"id": lid, "title": meta["title"], "sharpe": meta["sharpe"],
                          "age": age, "active_citers": active_citers,
                          "score": round(score, 2), "action": action})
    candidates.sort(key=lambda x: x["score"], reverse=True)
    return candidates[:limit]


def compress_candidates(lessons, states, inbound, current_session, ttl=TTL_SESSIONS):
    """Find EXPIRED lessons safe to archive."""
    candidates = []
    for lid, state in states.items():
        if state not in ("DECAYED", "BLIND-SPOT"):
            continue
        meta = lessons[lid]
        in_count = len(inbound.get(lid, set()))
        age = current_session - meta["session"]
        if in_count > 0 or age < ttl:
            continue
        if meta["sharpe"] >= 2 and meta["sharpe"] != -1:
            continue
        candidates.append({"id": lid, "title": meta["title"], "sharpe": meta["sharpe"],
                          "age": age, "est_tokens": meta["line_count"] * 5, "action": "archive"})
    candidates.sort(key=lambda x: x["age"], reverse=True)
    return candidates


def crosslink_suggestions(lessons, states, inbound, outbound, limit=10):
    """Find BLIND-SPOT items with ACTIVE neighbors."""
    suggestions = []
    domain_map = defaultdict(list)
    for lid, meta in lessons.items():
        domain_map[meta["domain"]].append(lid)
    for lid, state in states.items():
        if state != "BLIND-SPOT":
            continue
        meta = lessons[lid]
        if meta["domain"] == "unknown":
            continue  # skip untagged early lessons
        best = None
        for peer in domain_map.get(meta["domain"], []):
            if states.get(peer) in ("ACTIVE", "MUST-KNOW") and peer != lid:
                best = {"blind_id": lid, "active_id": peer,
                        "reason": f"same domain ({meta['domain']})"}
                break
        if not best:
            for target in outbound.get(lid, set()):
                for citer in inbound.get(target, set()):
                    if states.get(citer) in ("ACTIVE", "MUST-KNOW") and citer != lid:
                        best = {"blind_id": lid, "active_id": citer,
                                "reason": f"shared target {target}"}
                        break
                if best:
                    break
        if best:
            suggestions.append(best)
    return suggestions[:limit]


def detect_orphaned_principles(lessons, states):
    """Find principles with no live evidence chain."""
    text = read_text(REPO_ROOT / "memory" / "PRINCIPLES.md")
    if not text:
        return []
    orphaned = []
    current_p = None
    p_text = ""
    for line in text.split("\n"):
        pm = re.match(r"[-*]\s*\*?\*?P-(\d+)\*?\*?[:\s]+(.*)", line)
        if pm:
            if current_p:
                _check_principle(current_p, p_text, lessons, states, orphaned)
            current_p = f"P-{pm.group(1)}"
            p_text = line
        elif current_p and line.strip() and not line.startswith("#"):
            p_text += "\n" + line
        elif line.startswith("#"):
            if current_p:
                _check_principle(current_p, p_text, lessons, states, orphaned)
            current_p = None
            p_text = ""
    if current_p:
        _check_principle(current_p, p_text, lessons, states, orphaned)
    return orphaned


def _check_principle(p_id, text, lessons, states, orphaned):
    """Check if a principle has live evidence."""
    refs = set(re.findall(r"\bL-\d+\b", text))
    if not refs:
        orphaned.append({"id": p_id, "title": text.split("\n")[0][:60],
                        "evidence_state": "no_references", "action": "re-ground"})
        return
    live = any(states.get(r) in ("ACTIVE", "MUST-KNOW", "SHOULD-KNOW") for r in refs)
    if not live:
        p_num = re.search(r"\d+", p_id).group()
        for lid, state in states.items():
            if state in ("ACTIVE", "MUST-KNOW"):
                lt = read_text(REPO_ROOT / "memory" / "lessons" / f"{lid}.md")
                if lt and f"P-{p_num}" in lt:
                    live = True
                    break
        if not live:
            all_decayed = all(states.get(r) == "DECAYED" for r in refs if r in states)
            orphaned.append({"id": p_id, "title": text.split("\n")[0][:60],
                            "evidence_state": "all_decayed" if all_decayed else "mixed_dead",
                            "action": "retire" if all_decayed else "challenge"})


def compute_domain_gaps(lessons, states):
    """Compute per-domain knowledge gap rates."""
    domains = defaultdict(lambda: {"total": 0, "blind_spot": 0, "decayed": 0,
                                     "active": 0, "must_know": 0})
    for lid, meta in lessons.items():
        dom = meta["domain"]
        state = states.get(lid, "DECAYED")
        domains[dom]["total"] += 1
        key = {"BLIND-SPOT": "blind_spot", "DECAYED": "decayed",
               "ACTIVE": "active", "MUST-KNOW": "must_know"}.get(state)
        if key:
            domains[dom][key] += 1
    result = {}
    for dom, c in domains.items():
        t = max(1, c["total"])
        result[dom] = {**c, "blind_spot_rate": round(c["blind_spot"] / t, 3),
                       "decayed_rate": round(c["decayed"] / t, 3)}
    return dict(sorted(result.items(),
                       key=lambda x: x[1]["blind_spot_rate"] + x[1]["decayed_rate"],
                       reverse=True))


def section_output(results, current_session):
    """Format for orient.py integration — only show when action needed."""
    lines = []
    parts = []
    if results["revival"]:
        parts.append(f"Revival: {len(results['revival'])} DECAYED items with ACTIVE connections")
    if results["compress"]:
        tok = sum(c["est_tokens"] for c in results["compress"])
        parts.append(f"Compress: {len(results['compress'])} EXPIRED lessons (~{tok} tokens)")
    if results["crosslinks"]:
        parts.append(f"Crosslink: {len(results['crosslinks'])} BLIND-SPOT items have ACTIVE neighbors")
    if results["orphaned_principles"]:
        ids = ", ".join(o["id"] for o in results["orphaned_principles"][:5])
        parts.append(f"Orphaned principles: {len(results['orphaned_principles'])} ({ids})")
    if parts:
        lines.append(f"--- Knowledge Swarm (S{current_session}) ---")
        for p in parts:
            lines.append(f"  {p}")
        lines.append("")
    return lines


def full_report(results, domain_gaps, current_session, total):
    """Print full text report."""
    print(f"=== KNOWLEDGE SWARM S{current_session} | {total}L ===\n")
    for name, items, fmt in [
        ("Revival Candidates", results["revival"],
         lambda r: f"  {r['id']} (Sh={r['sharpe']}, age={r['age']}s, cited-by={r['active_citers']}): \"{r['title']}\" -> {r['action']}"),
        ("Compress Candidates", results["compress"],
         lambda c: f"  {c['id']} (Sh={c['sharpe']}, age={c['age']}s): \"{c['title']}\" -> {c['action']}"),
        ("Crosslink Suggestions", results["crosslinks"],
         lambda x: f"  {x['blind_id']} -> add to Cites: of {x['active_id']} ({x['reason']})"),
        ("Orphaned Principles", results["orphaned_principles"],
         lambda o: f"  {o['id']}: \"{o['title']}\" — {o['evidence_state']} -> {o['action']}"),
    ]:
        print(f"--- {name} ({len(items)}) ---")
        for item in items[:15]:
            print(fmt(item))
        if len(items) > 15:
            print(f"  ... and {len(items) - 15} more")
        print()
    print("--- Domain Knowledge Gaps ---")
    for dom, g in list(domain_gaps.items())[:15]:
        if g["total"] >= 3:
            print(f"  {dom}: BLIND={g['blind_spot_rate']*100:.1f}%, "
                  f"DECAYED={g['decayed_rate']*100:.1f}% ({g['total']} items)")
    print()


def main():
    parser = argparse.ArgumentParser(description="Knowledge Swarm Engine")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--brief", action="store_true")
    parser.add_argument("--domain", help="Filter domain")
    args = parser.parse_args()

    current = session_number()

    # Load all lessons
    lessons = {}
    for path in lesson_paths():
        meta = parse_lesson_meta(path)
        if meta:
            if args.domain and meta["domain"] != args.domain:
                continue
            lessons[meta["id"]] = meta
    if not lessons:
        print("No lessons found.")
        return

    # Build citation maps and classify
    outbound, inbound = build_citation_maps(lessons)
    states = classify_items(lessons, inbound, current)

    # Run all operations
    results = {
        "revival": revive_candidates(lessons, states, inbound, current),
        "compress": compress_candidates(lessons, states, inbound, current),
        "crosslinks": crosslink_suggestions(lessons, states, inbound, outbound),
        "orphaned_principles": detect_orphaned_principles(lessons, states),
    }
    domain_gaps = compute_domain_gaps(lessons, states)

    # State summary
    counts = defaultdict(int)
    for s in states.values():
        counts[s] += 1
    summary = {
        "total": len(lessons),
        "decayed_pct": round(counts["DECAYED"] / max(1, len(lessons)) * 100, 1),
        "blind_spot_pct": round(counts["BLIND-SPOT"] / max(1, len(lessons)) * 100, 1),
    }

    if args.brief:
        for line in section_output(results, current):
            print(line)
        return

    if args.json:
        artifact = {
            "session": current, "timestamp": datetime.now(timezone.utc).isoformat(),
            **{k: v for k, v in results.items()},
            "domain_gaps": domain_gaps, "summary": summary,
        }
        out_dir = REPO_ROOT / "experiments" / "meta"
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"knowledge-swarm-s{current}.json"
        with open(out_path, "w") as f:
            json.dump(artifact, f, indent=2, default=str)
        print(f"Artifact: {out_path}")

    full_report(results, domain_gaps, current, len(lessons))


if __name__ == "__main__":
    main()
