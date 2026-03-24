#!/usr/bin/env python3
"""science_quality.py — P-243: Score experiment quality for the swarm.

Scans experiment JSON artifacts and scores each on 5 science-quality criteria:
1. Pre-registered hypothesis (expect field present + quantitative)
2. Control/baseline (before/after, train/test, or explicit comparison)
3. Significance testing (p-value, BIC, CI, effect size reported)
4. External validation (tests against non-swarm data or independent system)
5. Falsification design (explicit conditions under which hypothesis fails)

Also reports:
- Confirm/discover ratio across recent sessions
- Falsification lane count (mode=falsification in SWARM-LANES.md)
- % of experiments with vague thresholds

Usage:
    python3 tools/science_quality.py                  # full report
    python3 tools/science_quality.py --recent 20      # last 20 sessions only
    python3 tools/science_quality.py --json            # machine-readable output
"""

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
EXPERIMENTS_DIR = REPO_ROOT / "experiments"
LANES_FILE = REPO_ROOT / "tasks" / "SWARM-LANES.md"
LANES_ARCHIVE = REPO_ROOT / "tasks" / "SWARM-LANES-ARCHIVE.md"
LESSONS_DIR = REPO_ROOT / "memory" / "lessons"

try:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from swarm_io import session_number as _shared_session_number
except ImportError:
    _shared_session_number = None


def extract_session_number(filename: str) -> int:
    """Extract session number from filename like f-str1-hardening-sNNN.json."""
    m = re.search(r"[sS](\d+)", filename)
    return int(m.group(1)) if m else 0


def _current_session() -> int:
    """Resolve the current session without depending on stale NEXT headers."""
    if _shared_session_number is not None:
        try:
            return int(_shared_session_number())
        except Exception:
            pass

    session_log = REPO_ROOT / "memory" / "SESSION-LOG.md"
    if session_log.exists():
        matches = re.findall(r"\bS(\d+)\b", session_log.read_text(encoding="utf-8", errors="replace"))
        if matches:
            return int(matches[-1])

    next_md = REPO_ROOT / "tasks" / "NEXT.md"
    if next_md.exists():
        matches = re.findall(r"\bS(\d+)\b", next_md.read_text(encoding="utf-8", errors="replace")[:500])
        if matches:
            return int(matches[0])

    return 506


def _artifact_path(session: int) -> Path:
    """Canonical periodic artifact path for science-quality audits."""
    return EXPERIMENTS_DIR / "meta" / f"science-quality-audit-s{session}.json"


def _is_periodic_audit_artifact(path: Path) -> bool:
    """Exclude the tool's own saved audit artifacts from future scoring runs."""
    return bool(re.fullmatch(r"science-quality-audit-s\d+\.json", path.name))


def score_experiment(data: dict) -> dict:
    """Score a single experiment artifact on P-243 criteria."""
    scores = {}
    text = json.dumps(data, default=str).lower()

    # 1. Pre-registered hypothesis (quantitative expect)
    expect = str(data.get("expect", data.get("hypothesis", "")))
    has_number = bool(re.search(r"\d", expect))
    has_threshold = any(kw in expect.lower() for kw in (
        ">", "<", ">=", "<=", "~", "within", "threshold", "%", "bic", "r=", "rho",
        "p<", "n=", "n>=", "δ", "delta",
    ))
    scores["pre_registration"] = 1.0 if (has_number and has_threshold) else (0.5 if has_number else 0.0)

    # 2. Control/baseline
    control_keywords = ("baseline", "control", "before", "train/test", "train_", "test_",
                        "comparison", "counterfactual", "pre-", "post-", "treatment",
                        "split", "holdout", "oos", "out-of-sample")
    scores["control"] = 1.0 if any(kw in text for kw in control_keywords) else 0.0

    # 3. Significance testing
    stat_keywords = ("p-value", "p<", "p =", "bic", "aic", "confidence interval",
                     "effect size", "cohen", "t-test", "chi-square", "anova",
                     "regression", "r²", "r-squared", "significance", "z-score",
                     "log-likelihood", "permutation test", "bootstrap")
    stat_count = sum(1 for kw in stat_keywords if kw in text)
    scores["significance"] = min(1.0, stat_count / 2.0)  # need at least 2 indicators

    # 4. External validation
    external_keywords = ("external", "independent", "non-swarm", "wikipedia", "arxiv",
                         "other repo", "outside", "cross-system", "real-world",
                         "ground truth", "benchmark")
    scores["external_validation"] = 1.0 if any(kw in text for kw in external_keywords) else 0.0

    # 5. Falsification design
    falsify_keywords = ("falsified if", "falsification", "reject if", "would fail if",
                        "contradicted if", "null hypothesis", "h0", "disprove",
                        "conditions for failure", "drop if", "wrong if")
    scores["falsification"] = 1.0 if any(kw in text for kw in falsify_keywords) else 0.0

    # Falsification outcome bonus (L-900: actual falsifications get 2.4x citation attractor —
    # reward experiments that produced a genuine null/falsified/overturned outcome beyond just
    # having a falsification condition planned in the design)
    outcome_text = str(data.get("actual", data.get("verdict", ""))).lower()
    outcome_mode = str(data.get("mode", "")).lower()
    is_falsified_outcome = any(kw in outcome_text for kw in (
        " falsified", "null result", "overturned", "rejected", "null:", "falsified:",
        "falsified —", "no effect", "zero effect",
    ))
    is_falsification_mode = outcome_mode == "falsification"
    scores["falsification_outcome"] = 1.0 if (is_falsified_outcome or is_falsification_mode) else 0.0

    # 6. Test severity (Popper corroboration — L-1390 gap #2, F-EPIS1)
    # Severe test = quantitative threshold + narrow tolerance + prior risk of failure.
    # Trivial test = vague direction ("will improve") or tautological threshold.
    severity = 0.0
    if has_number and has_threshold:
        # Quantitative prediction with threshold = baseline severity
        severity = 0.33
        # Narrow tolerance (±, within X%, confidence interval) = higher severity
        narrow_tolerance = any(kw in expect.lower() for kw in (
            "±", "+-", "within", "between", "ci ", "confidence interval",
            "margin", "tolerance", "range [", "range(",
        ))
        if narrow_tolerance:
            severity += 0.34
        # Explicit risk of failure or bold prediction = highest severity
        bold_indicators = any(kw in text for kw in (
            "bold prediction", "risky prediction", "surprising if",
            "would be surprising", "counter-intuitive", "against prior",
            "falsified if", "reject if", "wrong if",
        ))
        if bold_indicators:
            severity += 0.33
    scores["test_severity"] = severity

    base = sum(scores[k] for k in ("pre_registration", "control", "significance",
                                   "external_validation", "falsification")) / 5.0
    # Add test severity as bonus — weight 0.15 reflects r=+0.603 correlation with quality (L-1646)
    scores["total"] = min(1.0, base + scores["falsification_outcome"] * 0.10
                          + scores["test_severity"] * 0.15)
    return scores


def _has_filled_ead(etc: str) -> bool:
    """Check if lane Etc field has filled EAD (expect/actual/diff) — not skeleton/TBD.

    FM-39 defense (L-1164): lanes without real predictions should not count toward
    discovery ratio. A lane is experimental only if it has expect= with content AND
    actual= with non-TBD content.
    """
    has_expect = bool(re.search(r"expect=[^;]{5,}", etc))  # non-trivial expect
    has_actual = bool(re.search(r"actual=(?!TBD)[^;]{5,}", etc))  # actual != TBD
    return has_expect and has_actual


def count_confirmation_ratio() -> tuple[int, int, int]:
    """Count CONFIRMED vs FALSIFIED/OVERTURNED/NULL lane outcomes — measures discovery rate.

    FM-39 fix (L-1164): only counts lanes with filled EAD fields (expect + actual).
    Non-experimental lanes (no prediction) are excluded to prevent baseline contamination
    that inflated 54:1 → true ratio 9.2:1.

    Returns (confirmed, discovered, skipped_no_ead).
    """
    confirmed = 0
    discovered = 0  # falsified + null + overturned outcomes
    skipped = 0
    for lanes_file in (LANES_FILE, LANES_ARCHIVE):
        if not lanes_file.exists():
            continue
        for line in lanes_file.read_text().splitlines():
            if not line.startswith("|") or line.startswith("| ---") or line.startswith("| Date"):
                continue
            cols = [c.strip() for c in line.split("|")]
            if len(cols) < 12:
                continue
            etc = cols[10] if len(cols) > 10 else ""
            note = cols[11] if len(cols) > 11 else ""
            # FM-39: skip lanes without real predictions (L-1164)
            if not _has_filled_ead(etc):
                skipped += 1
                continue
            combined = (etc + " " + note).lower()
            if "confirmed" in combined and "falsified" not in combined and "null" not in combined:
                confirmed += 1
            elif any(kw in combined for kw in ("falsified", "null result", "overturned",
                                                "unexpected", "inverted", "wrong", "failed")):
                discovered += 1
    return confirmed, max(1, discovered), skipped


def check_instrument_validity(data: dict) -> dict:
    """FM-38 defense (L-1165): detect potential false-instrument experiments.

    At N>500, 33% of experiments had wrong measurement criteria (measured the
    wrong variable). This check flags experiments where:
    1. expect/hypothesis has no quantifiable metric (vague prediction)
    2. actual/result measures a metric not mentioned in the hypothesis
    3. metric_name is declared but doesn't appear in the hypothesis

    Returns {"valid": bool, "flags": list[str], "expect_metrics": list, "actual_metrics": list}.
    """
    expect = str(data.get("expect", data.get("hypothesis", "")))
    actual = str(data.get("actual", data.get("result", data.get("verdict", ""))))
    flags = []

    # Extract metric-like tokens: numbers with units, percentages, ratios, named metrics
    metric_re = re.compile(r"""
        \d+\.?\d*\s*%          |  # percentages
        \d+\.?\d*x             |  # multipliers
        \d+:\d+                |  # ratios like 9.2:1
        [rR]²?\s*[=<>]        |  # correlation coefficients
        [pP]\s*[<>=]           |  # p-values
        \b(?:rate|ratio|score|count|percentage|mean|median|correlation|coefficient)\b  |
        \b(?:n\s*[=<>]\s*\d+)\b  # sample sizes
    """, re.VERBOSE | re.IGNORECASE)

    expect_metrics = metric_re.findall(expect)
    actual_metrics = metric_re.findall(actual)

    # Flag 1: vague hypothesis (no quantifiable metric in expect)
    if expect and not expect_metrics and actual_metrics:
        flags.append("vague_hypothesis: expect has no quantifiable metric but actual does")

    # Flag 2: actual present with no expect
    if actual and actual.lower() not in ("tbd", "", "none") and not expect:
        flags.append("orphan_measurement: actual has data but no expect/hypothesis declared")

    # Flag 3: explicit metric_name field that doesn't match expect text
    metric_name = data.get("metric_name", data.get("metric", ""))
    if metric_name and expect and metric_name.lower() not in expect.lower():
        flags.append(f"metric_mismatch: declared metric '{metric_name}' not found in expect")

    return {
        "valid": len(flags) == 0,
        "flags": flags,
        "expect_metrics": expect_metrics,
        "actual_metrics": actual_metrics,
    }


def count_falsification_lanes(recent_sessions: int = 20) -> tuple[int, int]:
    """Count falsification-mode lanes in recent sessions."""
    falsification = 0
    total = 0
    for lanes_file in (LANES_FILE, LANES_ARCHIVE):
        if not lanes_file.exists():
            continue
        for line in lanes_file.read_text().splitlines():
            if not line.startswith("|") or line.startswith("| ---") or line.startswith("| Date"):
                continue
            cols = [c.strip() for c in line.split("|")]
            if len(cols) < 12:
                continue
            total += 1
            etc = cols[10] if len(cols) > 10 else ""
            if "mode=falsification" in etc:
                falsification += 1
    return falsification, total


def build_report(recent: int = 0) -> dict | None:
    """Build the science-quality report payload."""
    if not EXPERIMENTS_DIR.exists():
        raise FileNotFoundError("experiments/ directory not found")

    current_session = _current_session()

    # Score experiment JSON files
    # Use os.scandir for WSL performance (rglob on 1000+ files takes >30s on NTFS mount)
    min_session = max(1, current_session - recent) if recent else 0
    json_files = []
    for subdir in sorted(EXPERIMENTS_DIR.iterdir()):
        if not subdir.is_dir():
            continue
        for entry in subdir.iterdir():
            if not entry.name.endswith(".json"):
                continue
            if _is_periodic_audit_artifact(entry):
                continue
            session = extract_session_number(entry.name)
            if min_session and session < min_session:
                continue
            json_files.append((entry, session))
    json_files.sort(key=lambda x: x[0].name)

    results = []
    for json_file, session in json_files:
        try:
            data = json.loads(json_file.read_text())
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue
        if not isinstance(data, dict):
            continue
        scores = score_experiment(data)
        instrument = check_instrument_validity(data)
        results.append({
            "file": str(json_file.relative_to(REPO_ROOT)),
            "session": session,
            "scores": scores,
            "instrument_valid": instrument["valid"],
            "instrument_flags": instrument["flags"],
        })

    if not results:
        return None

    # Aggregate statistics
    totals = [r["scores"]["total"] for r in results]
    criteria_means = {}
    for criterion in ("pre_registration", "control", "significance", "external_validation",
                      "falsification", "falsification_outcome"):
        vals = [r["scores"][criterion] for r in results]
        criteria_means[criterion] = sum(vals) / len(vals) if vals else 0

    confirmed, discovered, skipped_no_ead = count_confirmation_ratio()
    falsif_lanes, total_lanes = count_falsification_lanes()

    n_falsif_outcome = sum(1 for r in results if r["scores"]["falsification_outcome"] > 0)
    n_instrument_flags = sum(1 for r in results if not r["instrument_valid"])
    flagged_experiments = [r for r in results if not r["instrument_valid"]]
    report = {
        "session": f"S{current_session}",
        "mode": "periodic",
        "tool": "science_quality.py",
        "recent_arg": recent,
        "n_experiments": len(results),
        "mean_quality": sum(totals) / len(totals),
        "median_quality": sorted(totals)[len(totals) // 2],
        "criteria_means": criteria_means,
        "confirm_discover_ratio": f"{confirmed}:{discovered}",
        "skipped_no_ead": skipped_no_ead,
        "falsification_lanes": f"{falsif_lanes}/{total_lanes}",
        "falsification_outcome_rate": round(n_falsif_outcome / len(results), 3) if results else 0,
        "falsification_outcome_count": n_falsif_outcome,
        "instrument_flags": n_instrument_flags,
        "instrument_flag_rate": round(n_instrument_flags / len(results), 3) if results else 0,
        "mean_test_severity": round(sum(r["scores"].get("test_severity", 0) for r in results) / len(results), 3) if results else 0,
        "sessions_observed": sorted({r["session"] for r in results}),
        "bottom_5": sorted(results, key=lambda r: r["scores"]["total"])[:5],
        "top_5": sorted(results, key=lambda r: r["scores"]["total"], reverse=True)[:5],
        "weak_severity_count": sum(1 for r in results if r["scores"].get("test_severity", 0) < 0.3),
        "weak_severity_rate": round(sum(1 for r in results if r["scores"].get("test_severity", 0) < 0.3) / len(results), 3) if results else 0,
    }
    return report


def print_report(report: dict) -> None:
    """Render the human-readable report."""
    criteria_means = report["criteria_means"]
    confirmed, discovered = [int(x) for x in report["confirm_discover_ratio"].split(":")]
    skipped_no_ead = report["skipped_no_ead"]
    falsif_lanes, total_lanes = [int(x) for x in report["falsification_lanes"].split("/")]
    n_falsif_outcome = report["falsification_outcome_count"]
    n_instrument_flags = report["instrument_flags"]
    n_experiments = report["n_experiments"]
    flagged_experiments = [r for r in report["bottom_5"] if r["instrument_flags"]]

    print(f"=== SCIENCE QUALITY REPORT (P-243) ===")
    print(f"Experiments scored: {n_experiments}")
    print(f"Mean quality:  {report['mean_quality']:.1%}")
    print(f"Median quality: {report['median_quality']:.1%}")
    print()
    print("--- Criteria breakdown ---")
    for criterion, mean in criteria_means.items():
        bar = "█" * int(mean * 20) + "░" * (20 - int(mean * 20))
        status = "PASS" if mean >= 0.5 else "FAIL"
        print(f"  {criterion:<25} {bar} {mean:.0%} [{status}]")
    print()
    print(f"Confirm/discover ratio:    {confirmed}:{discovered} ({confirmed/discovered:.0f}:1) [EAD-filtered, {skipped_no_ead} non-experimental skipped]")
    print(f"Falsification lanes:       {falsif_lanes}/{total_lanes} (target: 1-in-5 = 20%)")
    print(f"Falsified outcomes (bonus): {n_falsif_outcome}/{n_experiments} (L-900: +10% quality bonus)")
    weak_count = report.get("weak_severity_count", 0)
    weak_rate = report.get("weak_severity_rate", 0)
    sev_mean = report.get("mean_test_severity", 0)
    print(f"Test severity (Popper):    mean={sev_mean:.3f}, WEAK (<0.3): {weak_count}/{n_experiments} ({weak_rate:.0%}) [L-1646: r=+0.603]")
    print()
    print("--- Top 5 (best science) ---")
    for r in report["top_5"]:
        print(f"  {r['scores']['total']:.0%}  {r['file']}")
    print()
    print("--- Bottom 5 (weakest science) ---")
    for r in report["bottom_5"]:
        print(f"  {r['scores']['total']:.0%}  {r['file']}")
    if flagged_experiments:
        print()
        print(f"--- FM-38 Instrument validity (L-1165) ---")
        print(f"Flagged: {n_instrument_flags}/{n_experiments} ({n_instrument_flags/n_experiments:.0%})")
        for r in flagged_experiments[:5]:
            for flag in r["instrument_flags"]:
                print(f"  ⚠ {r['file']}: {flag}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="P-243: Score swarm experiment quality")
    parser.add_argument("--recent", type=int, default=0, help="Only score experiments from last N sessions")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--save", action="store_true", help="Save report to experiments/meta/")
    args = parser.parse_args(argv)

    try:
        report = build_report(recent=args.recent)
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if report is None:
        print("No experiment artifacts found.")
        return 0

    output = json.dumps(report, indent=2)
    if args.save:
        session_num = int(report["session"][1:])
        out_path = _artifact_path(session_num)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output + "\n", encoding="utf-8")
        print(f"Artifact saved: {out_path}")
    elif args.json:
        print(output)
    else:
        print_report(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
