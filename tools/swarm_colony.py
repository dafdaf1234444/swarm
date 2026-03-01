#!/usr/bin/env python3
"""
swarm_colony.py — Domain colony management.

A colony is a domain promoted to a self-directing swarm unit.
Each colony has its own orient→act→compress→handoff cycle, colony beliefs,
and colony-scoped coordination lanes. Colonies can spawn sub-colonies.

Distinct from tools/colony.py (which runs genetic-algorithm child experiments).
This tool manages persistent domain colonies.

Usage:
  python3 tools/swarm_colony.py bootstrap <domain>   -- seed COLONY.md + tasks/LANES.md
  python3 tools/swarm_colony.py status [domain]       -- show colony health
  python3 tools/swarm_colony.py list                  -- list all colonies + non-colonies
  python3 tools/swarm_colony.py orient <domain>       -- print colony orientation text
"""

import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOMAINS = ROOT / "domains"
MEMORY_LESSONS = ROOT / "memory" / "lessons"


# ── helpers ──────────────────────────────────────────────────────────────────

try:
    _tools_path = str(Path(__file__).resolve().parent)
    import sys as _sys; _sys.path.insert(0, _tools_path)
    from swarm_io import session_number as _sn_int
    def _current_session(): return f"S{_sn_int()}"
except ImportError:
    def _current_session() -> str:
        try:
            import subprocess
            r = subprocess.run(["git", "log", "--oneline", "-30"],
                               capture_output=True, text=True, cwd=ROOT)
            for line in r.stdout.splitlines():
                m = re.search(r'\[S(\d+)\]', line)
                if m:
                    return f"S{m.group(1)}"
        except Exception:
            pass
        return "S?"


def _today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _count_lessons(domain: str) -> int:
    pattern = domain.lower().replace("-", "[ -]")
    count = 0
    if MEMORY_LESSONS.exists():
        for f in MEMORY_LESSONS.glob("*.md"):
            try:
                if re.search(pattern, f.read_text(errors="ignore"), re.IGNORECASE):
                    count += 1
            except Exception:
                pass
    return count


def _count_open_frontiers(domain: str) -> int:
    fp = DOMAINS / domain / "tasks" / "FRONTIER.md"
    if not fp.exists():
        return 0
    return len(re.findall(r"^\s*-\s+\*\*F-", fp.read_text(errors="ignore"), re.MULTILINE))


def _count_active_lanes(domain: str) -> int:
    lp = DOMAINS / domain / "tasks" / "LANES.md"
    if not lp.exists():
        return 0
    active = 0
    for line in lp.read_text(errors="ignore").splitlines():
        parts = line.split("|")
        if len(parts) >= 3 and parts[2].strip() in ("OPEN", "PARTIAL", "BLOCKED"):
            active += 1
    return active


# ── templates ─────────────────────────────────────────────────────────────────

COLONY_TEMPLATE = """\
# Colony: {domain}
<!-- colony_md_version: 0.1 | founded: {session} | {date} -->
Status: ACTIVE | Founded: {session}

## Identity
Mission: Explore {domain} domain — extract structural isomorphisms to swarm,
  advance domain frontiers, feed lessons to global memory.
Scope: `domains/{domain}/` — cross-domain findings escalate to `tasks/FRONTIER.md`.
Parent: swarm (global) | Sub-colonies: none

## Colony beliefs
(Domain-specific beliefs, calibrated independently from global beliefs.)
- CB-1: {domain} structural patterns generalize to swarm coordination. [THEORIZED n=0]

## State
Last session: {session}
Lesson count (approx): ~{lessons}
Open frontiers: {frontiers}
Active colony lanes: 0

## Swarm protocol
This colony IS a swarm. Colony nodes orient with:
  1. This file (COLONY.md) — identity, beliefs, state
  2. `tasks/FRONTIER.md` — colony task queue
  3. `INDEX.md` — domain knowledge index
  4. `tasks/LANES.md` — colony-scoped coordination rows

Orient → Act → Compress → Handoff within colony scope.
Cross-domain findings → global `tasks/FRONTIER.md`.
Colony lessons → `memory/lessons/` (globally shared memory).
Colony state updates → this file (State section above).

## Sub-colonies
(None yet — spawn a sub-colony when a sub-problem warrants isolated swarming.)

## Handoff notes
(Latest session's context for next colony node — updated each session.)
"""

LANES_TEMPLATE = """\
# Colony Lanes: {domain}
# Format: ID | session | status | description | etc
# Status: OPEN | PARTIAL | BLOCKED | MERGED | ABANDONED
# Colony-scoped coordination. Global work → tasks/SWARM-LANES.md
"""


# ── commands ─────────────────────────────────────────────────────────────────

def cmd_bootstrap(domain: str) -> None:
    dp = DOMAINS / domain
    if not dp.exists():
        print(f"ERROR: domains/{domain}/ not found. Seed the domain first.")
        sys.exit(1)

    session = _current_session()
    date = _today()
    lessons = _count_lessons(domain)
    frontiers = _count_open_frontiers(domain)

    cp = dp / "COLONY.md"
    if cp.exists():
        print(f"  SKIP: {cp.relative_to(ROOT)} already exists.")
    else:
        cp.write_text(COLONY_TEMPLATE.format(
            domain=domain, session=session, date=date,
            lessons=lessons, frontiers=frontiers,
        ))
        print(f"  Created: {cp.relative_to(ROOT)}")

    lp = dp / "tasks" / "LANES.md"
    lp.parent.mkdir(parents=True, exist_ok=True)
    if lp.exists():
        print(f"  SKIP: {lp.relative_to(ROOT)} already exists.")
    else:
        lp.write_text(LANES_TEMPLATE.format(domain=domain))
        print(f"  Created: {lp.relative_to(ROOT)}")

    print(f"\nColony '{domain}' ready ({session}).")
    print(f"  orient:   python3 tools/swarm_colony.py orient {domain}")
    print(f"  status:   python3 tools/swarm_colony.py status {domain}")


def cmd_status(domain: str = None) -> None:
    session = _current_session()
    if domain:
        targets = [domain]
    else:
        targets = sorted(
            d.name for d in DOMAINS.iterdir()
            if d.is_dir() and (d / "COLONY.md").exists()
        )
    if not targets:
        print("No bootstrapped colonies. Run: python3 tools/swarm_colony.py bootstrap <domain>")
        return
    print(f"=== Colony Status ({session}) ===")
    for d in targets:
        cp = DOMAINS / d / "COLONY.md"
        if not cp.exists():
            print(f"  {d}: NOT_BOOTSTRAPPED")
            continue
        status_m = re.search(r"Status:\s*(\w+)", cp.read_text(errors="ignore"))
        status = status_m.group(1) if status_m else "?"
        lessons = _count_lessons(d)
        frontiers = _count_open_frontiers(d)
        lanes = _count_active_lanes(d)
        print(f"  {d}: {status} | {frontiers}F open | {lanes}L active | ~{lessons} lessons")


def cmd_list() -> None:
    session = _current_session()
    all_domains = sorted(
        d.name for d in DOMAINS.iterdir()
        if d.is_dir() and not d.name.startswith("_") and d.name != "experiments"
    )
    colonies = [d for d in all_domains if (DOMAINS / d / "COLONY.md").exists()]
    non_colonies = [d for d in all_domains if d not in colonies]

    print(f"=== Colony Registry ({session}) ===")
    print(f"Active colonies ({len(colonies)}):")
    for c in colonies:
        print(f"  + {c}")
    print(f"\nNon-colony domains ({len(non_colonies)}) — promotable with 'bootstrap':")
    for d in non_colonies:
        print(f"  - {d}")


def cmd_orient(domain: str) -> None:
    dp = DOMAINS / domain
    if not dp.exists():
        print(f"ERROR: domains/{domain}/ not found.")
        sys.exit(1)

    session = _current_session()
    cp = dp / "COLONY.md"
    lessons = _count_lessons(domain)
    frontiers = _count_open_frontiers(domain)
    lanes = _count_active_lanes(domain)

    print(f"=== Colony Orient: {domain} | {session} ===")
    print(f"Lessons: ~{lessons} | Open frontiers: {frontiers} | Active lanes: {lanes}")
    print()

    if not cp.exists():
        print(f"WARN: Not bootstrapped — run: python3 tools/swarm_colony.py bootstrap {domain}")
    else:
        text = cp.read_text(errors="ignore")
        in_section = False
        for line in text.splitlines():
            if line.startswith("## Colony beliefs") or line.startswith("## State") \
                    or line.startswith("## Handoff"):
                in_section = True
            elif line.startswith("## ") and in_section:
                if not any(line.startswith(f"## {s}") for s in
                           ("Colony beliefs", "State", "Handoff")):
                    in_section = False
            if in_section:
                print(line)
        print()

    fp = dp / "tasks" / "FRONTIER.md"
    if fp.exists():
        print("--- Open Frontiers ---")
        for line in fp.read_text(errors="ignore").splitlines():
            if re.match(r"^\s*-\s+\*\*F-", line):
                print(line[:120])
    print()
    print("Protocol: orient(COLONY.md → FRONTIER.md → INDEX.md) → act → compress → handoff")


# ── main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    cmd = sys.argv[1]
    if cmd == "bootstrap":
        if len(sys.argv) < 3:
            print("Usage: swarm_colony.py bootstrap <domain>")
            sys.exit(1)
        cmd_bootstrap(sys.argv[2])
    elif cmd == "status":
        cmd_status(sys.argv[2] if len(sys.argv) > 2 else None)
    elif cmd == "list":
        cmd_list()
    elif cmd == "orient":
        if len(sys.argv) < 3:
            print("Usage: swarm_colony.py orient <domain>")
            sys.exit(1)
        cmd_orient(sys.argv[2])
    else:
        print(f"Unknown: {cmd}")
        print("Commands: bootstrap, status, list, orient")
        sys.exit(1)


if __name__ == "__main__":
    main()
