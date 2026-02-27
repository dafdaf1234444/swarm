#!/usr/bin/env python3
"""
propagate_challenges.py — Pull belief-challenges from child bulletins into PHILOSOPHY.md.

Usage:
    python3 tools/propagate_challenges.py          # dry-run: show pending challenges
    python3 tools/propagate_challenges.py --apply  # write new challenges to PHILOSOPHY.md

Children write challenges with:
    python3 tools/bulletin.py write <child-name> belief-challenge "PHIL-N: challenge text"

This tool closes the bidirectional challenge loop: children can challenge parent philosophy,
not just report discoveries. Run at harvest time or any session start.
"""

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BULLETINS_DIR = REPO_ROOT / "experiments" / "inter-swarm" / "bulletins"
PHILOSOPHY_PATH = REPO_ROOT / "beliefs" / "PHILOSOPHY.md"


def collect_challenges() -> list[dict]:
    """Read all bulletins and return belief-challenge entries not yet in PHILOSOPHY.md."""
    if not BULLETINS_DIR.exists():
        return []

    found = []
    for f in sorted(BULLETINS_DIR.glob("*.md")):
        child = f.stem
        text = f.read_text()
        for m in re.finditer(
            r"# Bulletin from: .+?\nDate: (\S+)\nType: belief-challenge\n\n## Content\n(.+?)(?:\n---|\Z)",
            text, re.DOTALL
        ):
            date_str = m.group(1)
            content = m.group(2).strip()
            # Expect "PHIL-N: challenge text"
            claim_m = re.match(r"(PHIL-\d+):\s*(.+)", content, re.DOTALL)
            if claim_m:
                found.append({
                    "claim": claim_m.group(1),
                    "child": child,
                    "date": date_str,
                    "text": claim_m.group(2).strip(),
                })
    return found


def already_in_philosophy(child: str, claim: str) -> bool:
    """Check if this child+claim combo is already in the Challenges table."""
    if not PHILOSOPHY_PATH.exists():
        return False
    text = PHILOSOPHY_PATH.read_text()
    # Look for the child name AND the claim ID in the same table row
    return bool(re.search(rf"\|\s*{re.escape(claim)}\s*\|\s*{re.escape(child)}\s*\|", text))


def add_to_philosophy(challenges: list[dict]):
    """Append new challenges to the Challenges table in PHILOSOPHY.md."""
    text = PHILOSOPHY_PATH.read_text()
    # Find the last row of the challenges table (last | ... | line before end)
    table_end = text.rfind("\n| ")
    if table_end == -1:
        print("Could not find Challenges table in PHILOSOPHY.md")
        return 0

    insert_at = text.index("\n", table_end + 1) + 1
    rows = ""
    for c in challenges:
        # Truncate challenge text to keep table readable
        short = c["text"][:80] + ("…" if len(c["text"]) > 80 else "")
        rows += f"| {c['claim']} | {c['child']} | {short} | open |\n"

    new_text = text[:insert_at] + rows + text[insert_at:]
    PHILOSOPHY_PATH.write_text(new_text)
    return len(challenges)


def main():
    apply = "--apply" in sys.argv

    all_challenges = collect_challenges()
    pending = [c for c in all_challenges if not already_in_philosophy(c["child"], c["claim"])]

    if not pending:
        print("No new belief-challenges from children.")
        return

    print(f"Found {len(pending)} new belief-challenge(s) from children:")
    for c in pending:
        print(f"  {c['claim']} from {c['child']} ({c['date']}): {c['text'][:60]}…")

    if not apply:
        print("\nDry run. Use --apply to write to PHILOSOPHY.md.")
        return

    added = add_to_philosophy(pending)
    print(f"\nAdded {added} challenge(s) to PHILOSOPHY.md.")


if __name__ == "__main__":
    main()
