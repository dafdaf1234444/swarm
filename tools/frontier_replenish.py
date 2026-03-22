#!/usr/bin/env python3
"""Frontier Replenish — detect frontier-depleted domains and generate candidate questions.

Without active frontiers, dispatch_optimizer.py returns None, making domains invisible.
Usage: python3 tools/frontier_replenish.py [--top N] [--apply] [--json]
"""
import argparse, json, os, re, sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DOMAINS_DIR, LESSONS_DIR = REPO / "domains", REPO / "memory" / "lessons"


def get_active_frontier_count(frontier_path: Path) -> tuple[int, int, list[str]]:
    """Return (active_count, resolved_count, active_ids) from a FRONTIER.md."""
    if not frontier_path.exists():
        return 0, 0, []
    content = frontier_path.read_text()
    active_section = ""
    m = re.search(r"## (?:Active|Open)[^\S\n]*\n(.*?)(?=\n## |\Z)", content, re.DOTALL)
    if m:
        active_section = m.group(1)
    active_ids = re.findall(r"\*\*(F-[A-Z]+\d+)\*\*", active_section)
    resolved_count = 0
    rm = re.search(r"## Resolved.*", content, re.DOTALL)
    if rm:
        resolved_count = len(re.findall(r"^\| F-", rm.group(), re.MULTILINE))
    return len(active_ids), resolved_count, active_ids


def find_depleted_domains() -> list[dict]:
    """Find domains where all active frontiers are resolved or absent."""
    depleted = []
    if not DOMAINS_DIR.exists():
        return depleted
    for domain in sorted(os.listdir(DOMAINS_DIR)):
        domain_dir = DOMAINS_DIR / domain
        if not domain_dir.is_dir():
            continue
        frontier_path = domain_dir / "tasks" / "FRONTIER.md"
        if not frontier_path.exists():
            continue
        active, resolved, _ids = get_active_frontier_count(frontier_path)
        if active == 0:
            depleted.append({
                "domain": domain,
                "resolved_count": resolved,
                "frontier_path": str(frontier_path),
            })
    return depleted


def get_domain_context(domain: str) -> dict:
    """Gather context: DOMAIN.md info, domain-tagged lessons, principle references."""
    ctx = {"isos": [], "lessons": [], "beliefs": [], "principles": [], "topic": "",
           "domain_lessons": [], "domain_principles": []}
    domain_md = DOMAINS_DIR / domain / "DOMAIN.md"
    if domain_md.exists():
        dm = domain_md.read_text()
        tm = re.search(r"^Topic:\s*(.+)", dm, re.MULTILINE)
        if tm:
            ctx["topic"] = tm.group(1).strip()
        ctx["isos"] = sorted(set(re.findall(r"ISO-\d+", dm)))
        ctx["beliefs"] = sorted(set(re.findall(r"\bB-[A-Z]*\d+\b", dm)))
        ctx["principles"] = sorted(set(re.findall(r"\bP-\d{3}\b", dm)))
        ctx["lessons"] = sorted(set(re.findall(r"\bL-\d{3,4}\b", dm)))
    # Scan lessons for domain tags
    if LESSONS_DIR.exists():
        pat = re.compile(rf"Domain:.*\b{re.escape(domain)}\b", re.IGNORECASE)
        hits = [lf.stem for lf in LESSONS_DIR.glob("L-*.md")
                if pat.search(lf.read_text()[:500])]
        ctx["domain_lessons"] = sorted(hits, key=lambda x: int(x.split("-")[1]))[-10:]
    # Scan principles
    pf = REPO / "memory" / "PRINCIPLES.md"
    if pf.exists():
        ctx["domain_principles"] = sorted(set(
            m.group(1) for m in re.finditer(
                r"(P-\d{3})[^\n]*" + re.escape(domain), pf.read_text(), re.IGNORECASE)))
    return ctx


def get_existing_frontier_ids() -> set[str]:
    """Collect all frontier IDs across all domains to avoid collisions."""
    ids = set()
    if not DOMAINS_DIR.exists():
        return ids
    for domain in os.listdir(DOMAINS_DIR):
        fp = DOMAINS_DIR / domain / "tasks" / "FRONTIER.md"
        if fp.exists():
            ids.update(re.findall(r"F-[A-Z]+\d+", fp.read_text()))
    return ids


def domain_prefix(domain: str) -> str:
    """Derive frontier ID prefix from existing frontier IDs in domain's FRONTIER.md."""
    fp = DOMAINS_DIR / domain / "tasks" / "FRONTIER.md"
    if fp.exists():
        ids = re.findall(r"F-([A-Z]+)\d+", fp.read_text())
        if ids:
            return ids[0]  # use the prefix already in use
    # Fallback: uppercase first word, max 4 chars
    parts = domain.upper().replace("-", " ").split()
    return parts[0][:4] if parts else "UNK"


def next_frontier_id(prefix: str, existing: set[str]) -> str:
    """Find next available F-PREFIX# id."""
    for i in range(1, 100):
        fid = f"F-{prefix}{i}"
        if fid not in existing:
            return fid
    return f"F-{prefix}99"


QUESTION_TEMPLATES = [
    ("self-application",
     "Does {domain}'s core mechanism ({mechanism}) improve swarm operation when applied reflexively?",
     "Applying {domain} concepts to swarm protocol produces measurable improvement (>10% on target metric).",
     "Identify 3 {domain} concepts, apply each to one swarm subsystem, measure before/after on a concrete metric (lesson quality, dispatch accuracy, or compaction ratio)."),
    ("cross-domain",
     "Which other domains share structural mechanisms with {domain}, and do cross-citations between them predict higher lesson quality?",
     "Domain pairs with >3 cross-citations have >15% higher mean Sharpe than isolated domains.",
     "Build co-citation matrix for {domain} vs all other domains from lesson Domain: headers. Compare mean Sharpe for high-cross-cite vs low-cross-cite pairs."),
    ("scaling",
     "Does {domain}'s knowledge quality degrade, plateau, or improve as the swarm grows past current scale?",
     "{domain} lesson quality (Sharpe) follows a specific scaling regime (log, linear, or saturating).",
     "Plot {domain} lesson Sharpe vs session number. Fit log, linear, and saturating models. Report best-fit regime and predicted quality at 2x current lesson count."),
]


def generate_candidates(domain: str, ctx: dict, existing: set[str]) -> list[dict]:
    """Generate 2 candidate frontier questions for a depleted domain."""
    prefix = domain_prefix(domain)
    mechanism = ctx["topic"][:60] if ctx["topic"] else domain
    candidates = []
    for tmpl_name, q_tmpl, h_tmpl, t_tmpl in QUESTION_TEMPLATES:
        if len(candidates) >= 2:
            break
        fid = next_frontier_id(prefix, existing)
        existing.add(fid)
        question = q_tmpl.format(domain=domain, mechanism=mechanism)
        hypothesis = h_tmpl.format(domain=domain, mechanism=mechanism)
        test = t_tmpl.format(domain=domain, mechanism=mechanism)
        candidates.append({
            "id": fid,
            "type": tmpl_name,
            "question": question,
            "hypothesis": hypothesis,
            "test": test,
        })
    return candidates


def format_frontier_entry(c: dict) -> str:
    """Format a candidate as a FRONTIER.md entry."""
    return (
        f"- **{c['id']}**: {c['question']}\n"
        f"  Hypothesis: {c['hypothesis']}\n"
        f"  Test: {c['test']}\n"
    )


def apply_to_frontier(domain: str, candidates: list[dict]) -> None:
    """Write candidates into the domain's FRONTIER.md under ## Active."""
    fp = DOMAINS_DIR / domain / "tasks" / "FRONTIER.md"
    if not fp.exists():
        return
    content = fp.read_text()
    block = "\n".join(format_frontier_entry(c) for c in candidates) + "\n"
    # Insert after ## Active header line
    m = re.search(r"(## (?:Active|Open)[^\n]*\n)", content)
    if m:
        insert_pos = m.end()
        content = content[:insert_pos] + "\n" + block + content[insert_pos:]
    else:
        # No Active section — add one before ## Resolved
        rm = re.search(r"## Resolved", content)
        if rm:
            content = content[:rm.start()] + "## Active\n\n" + block + "\n" + content[rm.start():]
        else:
            content += "\n## Active\n\n" + block
    # Update Active count in header
    content = re.sub(r"Active: \d+", f"Active: {len(candidates)}", content, count=1)
    fp.write_text(content)


def main():
    parser = argparse.ArgumentParser(description="Detect frontier-depleted domains and generate candidates")
    parser.add_argument("--top", type=int, default=5, help="Max domains to replenish (default 5)")
    parser.add_argument("--apply", action="store_true", help="Write candidates to FRONTIER.md files")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    depleted = find_depleted_domains()
    if not depleted:
        print("No frontier-depleted domains found.")
        return

    existing_ids = get_existing_frontier_ids()
    results = []

    for info in depleted[:args.top]:
        domain = info["domain"]
        ctx = get_domain_context(domain)
        candidates = generate_candidates(domain, ctx, existing_ids)
        info["context"] = {
            "topic": ctx["topic"],
            "iso_count": len(ctx["isos"]),
            "lesson_count": len(ctx["domain_lessons"]),
            "recent_lessons": ctx["domain_lessons"][-5:],
            "principles": ctx["domain_principles"][:5],
        }
        info["candidates"] = candidates
        results.append(info)

        if args.apply:
            apply_to_frontier(domain, candidates)

    if args.json:
        print(json.dumps(results, indent=2))
        return

    # Human-readable report
    print(f"Frontier-depleted domains: {len(depleted)} total, showing {len(results)}\n")
    for r in results:
        domain = r["domain"]
        ctx = r["context"]
        print(f"  {domain} (resolved={r['resolved_count']}, lessons={ctx['lesson_count']}, "
              f"isos={ctx['iso_count']})")
        if ctx["topic"]:
            print(f"    Topic: {ctx['topic'][:80]}")
        if ctx["recent_lessons"]:
            print(f"    Recent lessons: {', '.join(ctx['recent_lessons'])}")
        for c in r["candidates"]:
            print(f"    {c['id']} [{c['type']}]: {c['question'][:90]}...")
            print(f"      Test: {c['test'][:90]}...")
        print()
    if args.apply:
        print(f"Applied {sum(len(r['candidates']) for r in results)} frontier entries to {len(results)} domains.")
    else:
        remaining = len(depleted) - len(results)
        print(f"Run with --apply to write candidates. "
              f"{'(' + str(remaining) + ' more depleted domains not shown)' if remaining > 0 else ''}")


if __name__ == "__main__":
    main()
