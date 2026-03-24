#!/usr/bin/env python3
"""signal_integrity.py — audit HUMAN.md signal references against SIGNALS.md.

Purpose:
  - detect missing signal rows for directives already referenced in HUMAN.md
  - detect source drift when HUMAN.md cites a human directive but SIGNALS.md
    records it as some other source
  - detect session drift between the human-model log and the signal ledger

Usage:
    python3 tools/signal_integrity.py
    python3 tools/signal_integrity.py --json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    from swarm_io import REPO_ROOT, read_text
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from swarm_io import REPO_ROOT, read_text

try:
    from swarm_signal import parse_signals
except ImportError:
    from tools.swarm_signal import parse_signals


HUMAN_FILE = REPO_ROOT / "memory" / "HUMAN.md"
SIG_RE = re.compile(r"\bSIG-\d+\b")
SESSION_RE = re.compile(r"^S\d+$")


def parse_human_signal_references(text: str) -> list[dict[str, object]]:
    """Extract directive-log rows that explicitly reference SIG ids."""
    rows: list[dict[str, object]] = []
    in_directive_log = False
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith("## Directive Log"):
            in_directive_log = True
            continue
        if not in_directive_log:
            continue
        if line.startswith("---"):
            break
        if not line.startswith("|"):
            continue
        parts = [p.strip() for p in line.strip("|").split("|")]
        if len(parts) < 3 or not SESSION_RE.match(parts[0]):
            continue
        sig_ids = SIG_RE.findall(parts[2])
        if not sig_ids:
            continue
        rows.append({
            "session": parts[0],
            "directive": parts[1],
            "impact": parts[2],
            "signal_ids": sig_ids,
        })
    return rows


def audit_signal_integrity(
    human_text: str | None = None,
    signals: list[dict[str, str]] | None = None,
) -> dict[str, object]:
    """Cross-check HUMAN.md signal references against SIGNALS.md rows."""
    if human_text is None:
        human_text = read_text(HUMAN_FILE)
    if signals is None:
        signals = parse_signals()

    references = parse_human_signal_references(human_text)
    signal_by_id = {signal["id"]: signal for signal in signals}
    issues: list[dict[str, str]] = []

    for ref in references:
        for sig_id in ref["signal_ids"]:
            signal = signal_by_id.get(sig_id)
            if signal is None:
                issues.append({
                    "issue": "missing_signal",
                    "signal_id": sig_id,
                    "human_session": str(ref["session"]),
                    "directive": str(ref["directive"]),
                    "detail": "HUMAN.md references a SIG id that is absent from SIGNALS.md",
                })
                continue
            if signal["source"] != "human":
                issues.append({
                    "issue": "wrong_source",
                    "signal_id": sig_id,
                    "human_session": str(ref["session"]),
                    "signal_session": signal["session"],
                    "directive": str(ref["directive"]),
                    "expected_source": "human",
                    "actual_source": signal["source"],
                })
            if signal["session"] != ref["session"]:
                issues.append({
                    "issue": "session_mismatch",
                    "signal_id": sig_id,
                    "human_session": str(ref["session"]),
                    "signal_session": signal["session"],
                    "directive": str(ref["directive"]),
                })

    return {
        "human_rows_with_signal_refs": len(references),
        "audited_signal_refs": sum(len(ref["signal_ids"]) for ref in references),
        "issue_count": len(issues),
        "issues": issues,
    }


def _print_report(report: dict[str, object]) -> None:
    issue_count = int(report["issue_count"])
    refs = int(report["audited_signal_refs"])
    rows = int(report["human_rows_with_signal_refs"])
    print(f"Signal integrity: {issue_count} issue(s) across {refs} HUMAN.md signal reference(s) in {rows} directive row(s)")
    for issue in report["issues"]:
        detail = issue["issue"]
        sig_id = issue["signal_id"]
        if detail == "wrong_source":
            print(
                f"  - {sig_id}: source {issue['actual_source']} != {issue['expected_source']} "
                f"(HUMAN {issue['human_session']}, SIGNAL {issue['signal_session']})"
            )
        elif detail == "session_mismatch":
            print(
                f"  - {sig_id}: HUMAN session {issue['human_session']} != SIGNAL session {issue['signal_session']}"
            )
        else:
            print(f"  - {sig_id}: missing from SIGNALS.md (HUMAN {issue['human_session']})")


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit HUMAN.md signal references against SIGNALS.md")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    args = parser.parse_args()

    report = audit_signal_integrity()
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        _print_report(report)
    return 1 if report["issue_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
