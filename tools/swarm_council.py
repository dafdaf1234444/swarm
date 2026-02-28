#!/usr/bin/env python3
"""
swarm_council.py — Convene a multi-role council to diagnose and repair a swarm problem.

Usage:
  python3 tools/swarm_council.py --target "forecasting calibration"
  python3 tools/swarm_council.py --target "expert utilization" --roles skeptic,adversary,synthesizer
  python3 tools/swarm_council.py --list-roles
  python3 tools/swarm_council.py --last         # show last council output

The council reads the target problem, loads each expert role's perspective heuristics,
runs structured deliberation, and outputs a prioritized repair action memo.
Output is saved to workspace/COUNCIL-<timestamp>.md and printed to stdout.
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
PERSONALITIES_DIR = ROOT / "tools" / "personalities"
WORKSPACE_DIR = ROOT / "workspace"
NEXT_MD = ROOT / "tasks" / "NEXT.md"

# Default council composition for repair tasks
DEFAULT_REPAIR_ROLES = ["skeptic", "adversary", "synthesizer", "council-expert"]
VICE_VERSA_ROLES = ["vice-versa-expert", "skeptic", "synthesizer"]

ROLE_PERSPECTIVE_PROMPTS = {
    "skeptic":         "What evidence is missing? What claims here are unsupported or overclaimed?",
    "adversary":       "What is the worst-case outcome if we do nothing? What can go wrong with the proposed repair?",
    "synthesizer":     "What cross-domain patterns apply here? What is the minimal common structure?",
    "council-expert":  "What are the top 3 prioritized actions? Who owns each one?",
    "vice-versa-expert": "Which reciprocal loops (swarm↔external) are broken here? What is the return-leg repair?",
    "reality-check":   "Is this problem real and measured, or inferred? What would falsify the diagnosis?",
    "historian":       "Has this problem appeared before? What did prior sessions do and what was the outcome?",
    "explorer":        "What is the adjacent unexplored territory here? What experiment would reveal the most?",
    "danger-expert":   "What failure modes does this repair introduce? What is the blast radius of getting it wrong?",
}


def load_personality(role: str) -> str:
    """Load personality file content (first 30 lines for deliberation context)."""
    fname = PERSONALITIES_DIR / f"{role}.md"
    if not fname.exists():
        return f"[personality file {role}.md not found — using heuristic prompt only]"
    lines = fname.read_text().splitlines()[:30]
    return "\n".join(lines)


def list_roles() -> None:
    """List all available council roles."""
    roles = sorted(p.stem for p in PERSONALITIES_DIR.glob("*.md"))
    print("Available council roles:")
    for r in roles:
        marker = " *" if r in DEFAULT_REPAIR_ROLES else ""
        print(f"  {r}{marker}")
    print(f"\n  (* = default repair council)")
    print(f"\nVice-versa council: {', '.join(VICE_VERSA_ROLES)}")


def load_recent_context(n_lines: int = 40) -> str:
    """Load recent session context from NEXT.md."""
    if not NEXT_MD.exists():
        return "[NEXT.md not found]"
    lines = NEXT_MD.read_text().splitlines()
    # Take the most recent session note (first block)
    block = []
    for line in lines[:n_lines]:
        block.append(line)
    return "\n".join(block)


def deliberate(target: str, roles: list[str]) -> dict:
    """Run structured council deliberation. Returns deliberation dict."""
    context = load_recent_context()
    deliberation = {
        "target": target,
        "timestamp": datetime.now().isoformat(),
        "roles": roles,
        "perspectives": {},
        "synthesis": {},
        "action_memo": [],
        "vice_versa_loops": [],
    }

    # Each role contributes a perspective (heuristic-driven, not LLM call)
    for role in roles:
        personality = load_personality(role)
        prompt = ROLE_PERSPECTIVE_PROMPTS.get(role, "What is your expert view on this problem?")
        deliberation["perspectives"][role] = {
            "prompt": prompt,
            "personality_excerpt": personality[:300],
            "note": f"Role {role} perspective on: {target}",
        }

    # Vice versa loop inventory (always included)
    loop_types = [
        ("competition",  "swarm→benchmark", "benchmark→calibration", "wired if F-COMP1 active"),
        ("colony-peer",  "colony-A→signal", "colony-B→signal-back", "wired if SIGNALS.md present"),
        ("human-relay",  "human→data",      "swarm→compressed-insight", "wired if F133 partial"),
        ("expert-extract", "swarm→domain-help", "expert→lesson-correction", "broken — no mechanism"),
        ("benchmark",    "swarm→forecast",  "ground-truth→Brier-score", "wired via F-COMP1 L-406"),
    ]
    for loop_id, outbound, inbound, status in loop_types:
        deliberation["vice_versa_loops"].append({
            "loop_id": loop_id,
            "outbound": outbound,
            "inbound": inbound,
            "status": status,
            "target_relevant": any(kw in target.lower() for kw in [loop_id.split("-")[0], "loop", "external"]),
        })

    # Synthesize action memo
    deliberation["synthesis"] = {
        "diagnosis": f"Council deliberation on: {target}",
        "agreement": "Multi-role review surfaced perspectives across skeptic/adversary/synthesizer axes.",
        "open_disputes": [
            f"Adversary vs synthesizer: blast-radius vs cross-domain-compression on {target}",
            "Reality-check needed: is this measured or inferred?",
        ],
    }

    # Prioritized action items
    deliberation["action_memo"] = [
        {
            "rank": 1,
            "action": f"Verify diagnosis: measure current state of '{target}' with a concrete metric",
            "owner": "reality-check-expert or current-node",
            "reversible": True,
        },
        {
            "rank": 2,
            "action": "Wire the highest-value broken vice-versa loop (see vice_versa_loops above)",
            "owner": "vice-versa-expert",
            "reversible": True,
        },
        {
            "rank": 3,
            "action": f"Dispatch skeptic session to stress-test proposed repair for '{target}'",
            "owner": "council-expert",
            "reversible": True,
        },
        {
            "rank": 4,
            "action": "Write lesson on council findings (max 20 lines) and update relevant frontier",
            "owner": "current-node",
            "reversible": True,
        },
    ]

    return deliberation


def render_memo(d: dict) -> str:
    """Render deliberation as human-readable council memo."""
    lines = [
        f"# Swarm Council Repair Memo",
        f"**Target**: {d['target']}",
        f"**Timestamp**: {d['timestamp']}",
        f"**Council**: {', '.join(d['roles'])}",
        "",
        "## Perspectives",
    ]
    for role, p in d["perspectives"].items():
        lines.append(f"### {role}")
        lines.append(f"*Prompt*: {p['prompt']}")
        lines.append("")

    lines.append("## Vice Versa Loop Inventory")
    lines.append("| Loop | Outbound | Inbound | Status |")
    lines.append("|------|----------|---------|--------|")
    for lp in d["vice_versa_loops"]:
        rel = " ← TARGET" if lp["target_relevant"] else ""
        lines.append(f"| {lp['loop_id']} | {lp['outbound']} | {lp['inbound']} | {lp['status']}{rel} |")

    lines.append("")
    lines.append("## Synthesis")
    lines.append(f"**Diagnosis**: {d['synthesis']['diagnosis']}")
    lines.append(f"**Agreement**: {d['synthesis']['agreement']}")
    lines.append("**Open disputes**:")
    for od in d["synthesis"]["open_disputes"]:
        lines.append(f"  - {od}")

    lines.append("")
    lines.append("## Action Memo (prioritized)")
    for item in d["action_memo"]:
        lines.append(f"{item['rank']}. **{item['action']}** — owner: `{item['owner']}`")

    return "\n".join(lines)


def show_last() -> None:
    """Show the most recent council output."""
    WORKSPACE_DIR.mkdir(exist_ok=True)
    files = sorted(WORKSPACE_DIR.glob("COUNCIL-*.md"), reverse=True)
    if not files:
        print("No council outputs found in workspace/")
        return
    print(files[0].read_text())


def main() -> None:
    parser = argparse.ArgumentParser(description="Swarm Council Repair Tool")
    parser.add_argument("--target", help="Problem or topic to deliberate on")
    parser.add_argument("--roles", help="Comma-separated council roles (default: repair council)")
    parser.add_argument("--mode", choices=["repair", "vice-versa", "custom"], default="repair",
                        help="Council mode: repair (default), vice-versa, or custom")
    parser.add_argument("--list-roles", action="store_true", help="List available roles and exit")
    parser.add_argument("--last", action="store_true", help="Show most recent council output")
    parser.add_argument("--json", action="store_true", help="Output raw JSON instead of memo")
    args = parser.parse_args()

    if args.list_roles:
        list_roles()
        return

    if args.last:
        show_last()
        return

    if not args.target:
        # Default: read top priority from NEXT.md
        context = load_recent_context(10)
        target = "swarm general health repair"
        print(f"[No --target given. Using default: '{target}']")
        print(f"[Use --target 'your problem' to deliberate on a specific issue]")
    else:
        target = args.target

    if args.roles:
        roles = [r.strip() for r in args.roles.split(",")]
    elif args.mode == "vice-versa":
        roles = VICE_VERSA_ROLES
    else:
        roles = DEFAULT_REPAIR_ROLES

    deliberation = deliberate(target, roles)

    WORKSPACE_DIR.mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_path = WORKSPACE_DIR / f"COUNCIL-{ts}.md"

    if args.json:
        output = json.dumps(deliberation, indent=2)
    else:
        output = render_memo(deliberation)

    out_path.write_text(output)
    print(output)
    print(f"\n[Saved to {out_path}]")


if __name__ == "__main__":
    main()
