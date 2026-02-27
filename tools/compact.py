#!/usr/bin/env python3
"""compact.py — Compression target analysis (F105).

Identifies specific files and techniques when proxy K drift exceeds threshold.
Separates analysis from mutation (P-144): this tool diagnoses, session acts.

Usage:
    python3 tools/compact.py           # show compression targets
    python3 tools/compact.py --save    # record measurement + save floor if lower
"""

import json
import hashlib
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

TIERS = {
    "T0-mandatory": ["SWARM.md", "CLAUDE.md", "beliefs/CORE.md", "memory/INDEX.md"],
    "T1-identity": ["beliefs/PHILOSOPHY.md", "beliefs/DEPS.md", "beliefs/INVARIANTS.md"],
    "T2-protocols": ["memory/DISTILL.md", "memory/VERIFY.md", "memory/OPERATIONS.md",
                      "beliefs/CONFLICTS.md"],
    "T3-knowledge": ["memory/PRINCIPLES.md", "tasks/FRONTIER.md"],
    "T4-tools": ["tools/validate_beliefs.py", "tools/maintenance.py", "tools/paper_drift.py", "tools/swarm_parse.py"],
}

LOG_PATH = REPO_ROOT / "experiments" / "proxy-k-log.json"

# Compression techniques per file type (proven in S77b, S83++, S85, S90b)
TECHNIQUES = {
    "memory/PRINCIPLES.md": [
        "Evidence annotation trimming (highest ROI — S83++ saved 10.9%)",
        "Merge semantically adjacent principles (check P-NNN pairs in same subsection)",
        "Remove genuinely orphaned: run maintenance.py check_utility",
    ],
    "tasks/FRONTIER.md": [
        "Compress resolved-but-kept question descriptions",
        "Archive questions below frontier-decay threshold",
    ],
    "memory/INDEX.md": [
        "Theme table row consolidation (merge small themes)",
    ],
    "beliefs/PHILOSOPHY.md": [
        "Challenge table: keep verdicts, trim deliberation prose",
    ],
    "tools/validate_beliefs.py": [
        "Combine related check functions (S77b: -15%)",
        "Docstring and dead-code removal",
    ],
    "tools/maintenance.py": [
        "Combine small check functions with shared patterns",
        "Inline utility functions used only once",
    ],
    "tools/paper_drift.py": [
        "Keep parser rules compact; avoid duplicate regex/scan paths",
        "Prefer small helpers reused across checks over repeated inline logic",
    ],
    "tools/swarm_parse.py": [
        "Keep parser helpers single-purpose and shared across tools",
        "Prefer table-driven regex extraction over duplicated per-tool variants",
    ],
}


def _read(path: Path) -> str:
    """Read text as UTF-8 across runtimes/locales."""
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


def _tier_schema() -> str:
    payload = json.dumps(TIERS, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _tokens(path: Path) -> int:
    return len(_read(path)) // 4


def _lines(path: Path) -> int:
    return len(_read(path).splitlines())


def _find_floor() -> dict | None:
    if not LOG_PATH.exists():
        return None
    try:
        entries = json.loads(_read(LOG_PATH))
    except Exception:
        return None
    schema = _tier_schema()
    schema_entries = [e for e in entries if e.get("tier_schema") == schema]
    if len(schema_entries) >= 2:
        entries = schema_entries
    else:
        return None

    if len(entries) < 2:
        return entries[0] if entries else None
    floor_idx = 0
    for i in range(1, len(entries)):
        if entries[i]["total"] < entries[i - 1]["total"]:
            floor_idx = i
    return entries[floor_idx]


def _measure() -> dict:
    files = {}
    tiers = {}
    total = 0
    for tier, paths in TIERS.items():
        tier_t = 0
        for p in paths:
            t = _tokens(REPO_ROOT / p)
            files[p] = {"tier": tier, "tokens": t, "lines": _lines(REPO_ROOT / p)}
            tier_t += t
        tiers[tier] = tier_t
        total += tier_t
    return {"files": files, "tiers": tiers, "total": total}


def _section_sizes(filepath: str) -> list[tuple[str, int]]:
    """Return (section_name, token_count) for markdown ## sections."""
    path = REPO_ROOT / filepath
    text = _read(path)
    if not text:
        return []
    sections = []
    name = "(header)"
    chars = 0
    for line in text.splitlines():
        if line.startswith("## "):
            sections.append((name, chars // 4))
            name = line[3:].strip()
            chars = 0
        else:
            chars += len(line) + 1
    sections.append((name, chars // 4))
    return [(n, t) for n, t in sections if t > 50]


def analyze():
    floor = _find_floor()
    m = _measure()

    print("=== COMPRESSION ANALYSIS (F105) ===\n")

    if floor:
        drift = (m["total"] - floor["total"]) / floor["total"]
        status = "URGENT" if drift > 0.10 else "DUE" if drift > 0.06 else "healthy"
        print(f"  Floor: {floor['total']:,} tokens (S{floor.get('session', '?')})")
        print(f"  Current: {m['total']:,} tokens")
        print(f"  Drift: {drift:+.1%} ({status})")
        target_reduction = m["total"] - floor["total"] if drift > 0.06 else 0
        if target_reduction > 0:
            print(f"  Target: reduce by ~{target_reduction:,} tokens to reach floor")
    else:
        drift = 0
        print(f"  Current: {m['total']:,} tokens (no floor — run proxy_k.py --save)")

    # Tier-level deltas
    print("\n  Tier breakdown:")
    floor_tiers = floor.get("tiers", {}) if floor else {}
    growth_tiers = []
    for tier in sorted(TIERS.keys()):
        cur = m["tiers"][tier]
        prev = floor_tiers.get(tier, cur)
        delta = cur - prev
        pct = cur / m["total"] * 100
        flag = " <-- TARGET" if delta > 200 else ""
        print(f"    {tier:20s}  {cur:6,}t ({pct:4.1f}%)  {delta:+5d}{flag}")
        if delta > 100:
            growth_tiers.append((tier, delta))

    # Per-file in growth tiers
    if growth_tiers:
        print("\n  Growth files:")
        for filepath, info in sorted(m["files"].items(), key=lambda x: x[1]["tokens"], reverse=True):
            tier = info["tier"]
            if any(t == tier for t, _ in growth_tiers):
                print(f"    {filepath:40s}  {info['tokens']:6,}t  {info['lines']:4d}L")
                # Section breakdown for large .md files
                if filepath.endswith(".md") and info["tokens"] > 500:
                    for name, tokens in _section_sizes(filepath)[:3]:
                        print(f"      |- {name:36s}  {tokens:5,}t")

    # Compression recommendations
    print("\n  Techniques (proven):")
    ranked = sorted(m["files"].items(), key=lambda x: x[1]["tokens"], reverse=True)
    shown = 0
    for filepath, info in ranked:
        if shown >= 5:
            break
        techs = TECHNIQUES.get(filepath, [])
        if not techs:
            continue
        print(f"    {filepath} ({info['tokens']:,}t):")
        for t in techs:
            print(f"      - {t}")
        shown += 1

    return m, drift


def save(m):
    """Save current measurement to proxy-k-log.json."""
    log = []
    if LOG_PATH.exists():
        try:
            log = json.loads(_read(LOG_PATH))
        except Exception:
            pass

    # Get session number
    text = _read(REPO_ROOT / "memory" / "SESSION-LOG.md")
    numbers = re.findall(r"^S(\d+)", text, re.MULTILINE)
    session = max(int(n) for n in numbers) if numbers else 0

    from datetime import date
    entry = {
        "date": date.today().isoformat(),
        "session": session,
        "tier_schema": _tier_schema(),
        "tiers": m["tiers"],
        "total": m["total"],
        "genesis": sum(
            _tokens(REPO_ROOT / f)
            for f in ["CLAUDE.md", "beliefs/CORE.md", "memory/INDEX.md",
                       "tasks/FRONTIER.md", "memory/DISTILL.md",
                       "tools/validate_beliefs.py", "memory/lessons/TEMPLATE.md"]
        ),
    }
    log.append(entry)
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    LOG_PATH.write_text(json.dumps(log, indent=2))
    print(f"\n  Saved to proxy-k-log.json ({len(log)} entries)")


def main():
    m, drift = analyze()
    if "--save" in sys.argv:
        save(m)
    if drift > 0.06:
        print(f"\n  ACTION NEEDED: Drift {drift:.1%} exceeds 6%. Compress targets above.")
    else:
        print(f"\n  No compression needed. Drift {drift:.1%} is healthy.")


if __name__ == "__main__":
    main()
