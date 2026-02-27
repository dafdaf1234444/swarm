#!/usr/bin/env python3
"""
proxy_k.py — Measure the swarm's description length (F116).

Usage:
    python3 tools/proxy_k.py              # print current measurement
    python3 tools/proxy_k.py --save       # append to experiments/proxy-k-log.json
    python3 tools/proxy_k.py --history    # show trend

Proxy K = token count of bootstrap files. Tracks PHIL-8's "shortest program."
Lower = more compressed. But too low = information loss (MDL tradeoff).
"""

import json
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Bootstrap tiers (F107 + operational)
TIERS = {
    "T0-mandatory": [
        "CLAUDE.md",
        "beliefs/CORE.md",
        "memory/INDEX.md",
    ],
    "T1-identity": [
        "beliefs/PHILOSOPHY.md",
        "beliefs/DEPS.md",
        "beliefs/INVARIANTS.md",
    ],
    "T2-protocols": [
        "memory/DISTILL.md",
        "memory/VERIFY.md",
        "memory/OPERATIONS.md",
        "beliefs/CONFLICTS.md",
    ],
    "T3-knowledge": [
        "memory/PRINCIPLES.md",
        "tasks/FRONTIER.md",
    ],
    "T4-tools": [
        "tools/validate_beliefs.py",
        "tools/maintenance.py",
    ],
}

GENESIS_FILES = [
    "CLAUDE.md", "beliefs/CORE.md", "memory/INDEX.md",
    "tasks/FRONTIER.md", "memory/DISTILL.md",
    "tools/validate_beliefs.py", "memory/lessons/TEMPLATE.md",
]

LOG_PATH = REPO_ROOT / "experiments" / "proxy-k-log.json"


def _tokens(path: Path) -> int:
    """Estimate token count (chars / 4)."""
    try:
        return len(path.read_text()) // 4
    except Exception:
        return 0


def _session_number() -> int:
    try:
        text = (REPO_ROOT / "memory" / "SESSION-LOG.md").read_text()
        import re
        numbers = re.findall(r"^S(\d+)", text, re.MULTILINE)
        return max(int(n) for n in numbers) if numbers else 0
    except Exception:
        return 0


def measure():
    """Return current proxy K measurement."""
    result = {"tiers": {}, "total": 0, "genesis": 0}

    for tier_name, files in TIERS.items():
        tier_tokens = 0
        for f in files:
            tier_tokens += _tokens(REPO_ROOT / f)
        result["tiers"][tier_name] = tier_tokens
        result["total"] += tier_tokens

    for f in GENESIS_FILES:
        result["genesis"] += _tokens(REPO_ROOT / f)

    return result


def show(m):
    print("=== PROXY K (F116) ===\n")
    for tier, tokens in m["tiers"].items():
        pct = tokens / m["total"] * 100 if m["total"] else 0
        print(f"  {tier:20s}  {tokens:6d} tokens  ({pct:4.1f}%)")
    print(f"  {'':20s}  {'------':>6s}")
    print(f"  {'TOTAL':20s}  {m['total']:6d} tokens")
    print(f"  {'Genesis (F107)':20s}  {m['genesis']:6d} tokens  ({m['genesis']/m['total']*100:.1f}%)")


def save(m):
    log = []
    if LOG_PATH.exists():
        try:
            log = json.loads(LOG_PATH.read_text())
        except Exception:
            pass

    entry = {
        "date": date.today().isoformat(),
        "session": _session_number(),
        **m,
    }
    log.append(entry)

    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    LOG_PATH.write_text(json.dumps(log, indent=2))
    print(f"\nSaved to {LOG_PATH} ({len(log)} entries)")


def history():
    if not LOG_PATH.exists():
        print("No history yet. Run with --save first.")
        return

    log = json.loads(LOG_PATH.read_text())
    print("=== PROXY K HISTORY ===\n")
    print(f"  {'Session':>8s}  {'Total':>8s}  {'Genesis':>8s}  {'T4-tools':>8s}  {'Date':>12s}")
    print(f"  {'--------':>8s}  {'--------':>8s}  {'--------':>8s}  {'--------':>8s}  {'------------':>12s}")

    for entry in log:
        t4 = entry.get("tiers", {}).get("T4-tools", 0)
        session = str(entry.get('session', '?'))
        print(f"  S{session:>6s}  {entry['total']:>8d}  {entry['genesis']:>8d}  {t4:>8d}  {entry['date']:>12s}")

    if len(log) >= 2:
        first, last = log[0], log[-1]
        delta = last["total"] - first["total"]
        direction = "+" if delta > 0 else ""
        print(f"\n  Trend: {direction}{delta} tokens over {len(log)} measurements")


def main():
    m = measure()
    show(m)

    if "--save" in sys.argv:
        save(m)
    if "--history" in sys.argv:
        history()


if __name__ == "__main__":
    main()
