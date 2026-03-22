#!/usr/bin/env python3
"""FM-38 defense: detect false measurement instruments in experiment artifacts.

At N>500 sessions, 33% of experiments measured the wrong variable (L-1165).
This scanner checks experiment JSONs for measurement-criterion validity:
1. Vague hypothesis: expect has no quantifiable metric but actual does
2. Orphan measurement: actual has data but no expect declared
3. Metric mismatch: declared metric_name doesn't appear in expect text
4. Expect-actual drift: actual introduces metrics absent from expect

Usage:
  python3 tools/false_instrument_check.py              # scan all experiments
  python3 tools/false_instrument_check.py --staged      # scan only staged experiments (for check.sh)
  python3 tools/false_instrument_check.py --json        # JSON output
  python3 tools/false_instrument_check.py --recent 20   # last 20 sessions only
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
EXPERIMENTS_DIR = REPO_ROOT / "experiments"

# Metric-like patterns in experiment text
METRIC_RE = re.compile(r"""
    \d+\.?\d*\s*%          |  # percentages
    \d+\.?\d*x             |  # multipliers
    \d+:\d+                |  # ratios like 9.2:1
    [rR]²?\s*[=<>]        |  # correlation coefficients
    [pP]\s*[<>=]           |  # p-values
    \b(?:rate|ratio|score|count|percentage|mean|median|correlation|coefficient)\b  |
    \b(?:n\s*[=<>]\s*\d+)\b  # sample sizes
""", re.VERBOSE | re.IGNORECASE)

# Named metric patterns (more specific than raw numbers)
NAMED_METRIC_RE = re.compile(
    r'\b(gini|sharpe|entropy|proxy.?k|citation|enforcement|merge.?rate|'
    r'discovery.?ratio|confirm|falsif|precision|recall|accuracy|f1|auc|'
    r'coverage|utilization|throughput|latency|drift|decay|inflation)\b',
    re.IGNORECASE
)


def extract_session_number(filename: str) -> int:
    """Extract session number from filename like f-str1-hardening-sNNN.json."""
    m = re.search(r"[sS](\d+)", filename)
    return int(m.group(1)) if m else 0


def check_instrument(data: dict) -> dict:
    """Check a single experiment for false-instrument patterns.

    Returns {"valid": bool, "flags": list[str], "severity": str}.
    """
    expect = str(data.get("expect", data.get("hypothesis", "")))
    actual = str(data.get("actual", data.get("result", data.get("verdict", ""))))
    flags = []

    # Skip TBD experiments (not yet executed)
    if not actual or actual.lower() in ("tbd", "none", ""):
        return {"valid": True, "flags": [], "severity": "none"}

    expect_metrics = METRIC_RE.findall(expect)
    actual_metrics = METRIC_RE.findall(actual)
    expect_named = set(m.lower() for m in NAMED_METRIC_RE.findall(expect))
    actual_named = set(m.lower() for m in NAMED_METRIC_RE.findall(actual))

    # Flag 1: vague hypothesis (no quantifiable metric in expect, but actual has them)
    if expect and not expect_metrics and actual_metrics:
        flags.append("vague_hypothesis: expect has no quantifiable metric but actual does")

    # Flag 2: actual present with no expect
    if actual and not expect:
        flags.append("orphan_measurement: actual has data but no expect/hypothesis declared")

    # Flag 3: explicit metric_name field that doesn't match expect text
    metric_name = data.get("metric_name", data.get("metric", ""))
    if metric_name and expect and metric_name.lower() not in expect.lower():
        flags.append(f"metric_mismatch: declared metric '{metric_name}' not found in expect")

    # Flag 4: named metric drift — actual introduces domain metrics not in expect
    if expect_named and actual_named:
        novel_metrics = actual_named - expect_named
        if len(novel_metrics) > len(expect_named):
            flags.append(
                f"metric_drift: actual introduces {len(novel_metrics)} metrics "
                f"absent from expect ({', '.join(sorted(novel_metrics)[:3])}...)"
            )

    severity = "none"
    if flags:
        severity = "high" if len(flags) >= 2 else "medium"

    return {"valid": len(flags) == 0, "flags": flags, "severity": severity}


def get_staged_experiments() -> list[Path]:
    """Get experiment JSON files currently staged in git."""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            capture_output=True, text=True, cwd=REPO_ROOT
        )
        staged = []
        for line in result.stdout.strip().splitlines():
            if line.startswith("experiments/") and line.endswith(".json"):
                p = REPO_ROOT / line
                if p.exists():
                    staged.append(p)
        return staged
    except (subprocess.SubprocessError, FileNotFoundError):
        return []


def scan_experiments(files: list[Path]) -> list[dict]:
    """Scan experiment files and return results."""
    results = []
    for path in sorted(files):
        try:
            data = json.loads(path.read_text())
        except (json.JSONDecodeError, UnicodeDecodeError, OSError):
            continue
        if not isinstance(data, dict):
            continue
        check = check_instrument(data)
        if check["flags"]:
            results.append({
                "file": str(path.relative_to(REPO_ROOT)),
                "session": extract_session_number(path.name),
                "flags": check["flags"],
                "severity": check["severity"],
            })
    return results


def main():
    parser = argparse.ArgumentParser(description="FM-38: false instrument detector (L-1165)")
    parser.add_argument("--staged", action="store_true", help="Only check staged experiments")
    parser.add_argument("--recent", type=int, default=0, help="Only check last N sessions")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    if args.staged:
        files = get_staged_experiments()
        if not files:
            return
    else:
        if not EXPERIMENTS_DIR.exists():
            print("ERROR: experiments/ directory not found", file=sys.stderr)
            sys.exit(1)
        files = list(EXPERIMENTS_DIR.rglob("*.json"))
        if args.recent:
            max_session = max(extract_session_number(f.name) for f in files) if files else 0
            files = [f for f in files if extract_session_number(f.name) >= max_session - args.recent]

    flagged = scan_experiments(files)

    if args.json:
        print(json.dumps({"flagged": flagged, "total_scanned": len(files)}, indent=2))
        return

    if args.staged:
        # check.sh integration: compact output
        for r in flagged:
            for flag in r["flags"]:
                print(f"  FM-38 NOTICE: {r['file']}: {flag}")
    else:
        total = len(list(EXPERIMENTS_DIR.rglob("*.json"))) if not args.recent else len(files)
        print(f"=== FM-38 False Instrument Scanner (L-1165) ===")
        print(f"Scanned: {len(files)} experiments")
        print(f"Flagged: {len(flagged)} ({len(flagged)/len(files)*100:.1f}%)" if files else "Flagged: 0")
        if flagged:
            print()
            for r in flagged[:10]:
                print(f"  [{r['severity'].upper()}] {r['file']}:")
                for flag in r["flags"]:
                    print(f"    - {flag}")


if __name__ == "__main__":
    main()
