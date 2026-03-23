#!/usr/bin/env python3
"""Popperian degree-of-corroboration scorer for swarm experiments.

Fills the "degree of corroboration" gap identified in F-EPIS1 (S514/S518):
Popper distinguished corroboration (survived severe tests) from confirmation
(accumulated positive evidence). A claim that survived a severe test should
get more credit than one that survived a trivial test.

Scores each experiment on 4 severity dimensions:
  1. Specificity  — how precise/quantitative is the prediction?
  2. Riskiness    — how far from the safe/obvious answer?
  3. Falsifiability — how concrete are the falsification criteria?
  4. Surprise     — did the actual outcome differ from prediction? (diff quality)

Degree of corroboration = severity × outcome:
  - CONFIRMED with high severity = STRONG corroboration
  - CONFIRMED with low severity  = WEAK corroboration (tautological)
  - FALSIFIED with high severity  = informative failure (high epistemic value)
  - FALSIFIED with low severity   = uninformative failure

Usage:
  python3 tools/test_severity.py                    # full report
  python3 tools/test_severity.py --json             # machine-readable
  python3 tools/test_severity.py --worst 10         # 10 weakest tests
  python3 tools/test_severity.py --best 10          # 10 strongest tests
"""

import json
import os
import re
import sys
import argparse
from pathlib import Path

EXPERIMENTS_DIR = Path(__file__).parent.parent / "experiments"

# Indicators of quantitative specificity
NUMERIC_PATTERN = re.compile(r'[<>=≥≤]\s*\d+|[\d.]+[%x×]|\d+/\d+|\b\d+\.\d+\b|[+-]?\d+\s*(sessions?|lines?|lessons?|items?|tools?)')
VAGUE_WORDS = re.compile(r'\b(some|several|many|few|various|roughly|approximately|maybe|might|could|possibly|generally|often|tends?|usually)\b', re.I)
PRECISE_WORDS = re.compile(r'\b(exactly|precisely|must|always|never|zero|none|all|every|strict|≥|≤|>=|<=|threshold|minimum|maximum|at least|at most)\b', re.I)

# Risk indicators
SAFE_PREDICTIONS = re.compile(r'\b(will (continue|remain|stay|persist)|still|same as|no change|consistent with|as expected|incremental)\b', re.I)
BOLD_PREDICTIONS = re.compile(r'\b(will (reverse|drop|fail|collapse|diverge|break)|opposite|contrary|falsif|against|unexpected|novel|surprising|counterintuitive|impossible|paradox)\b', re.I)


def score_specificity(text: str) -> float:
    """Score 0-1: how specific/quantitative is the prediction?"""
    if not text:
        return 0.0
    score = 0.0
    # Numeric content
    numerics = len(NUMERIC_PATTERN.findall(text))
    score += min(numerics * 0.15, 0.45)
    # Precision language
    precise = len(PRECISE_WORDS.findall(text))
    score += min(precise * 0.1, 0.3)
    # Penalize vagueness
    vague = len(VAGUE_WORDS.findall(text))
    score -= min(vague * 0.08, 0.25)
    # Length bonus (more specific predictions tend to be longer)
    words = len(text.split())
    if words > 30:
        score += 0.1
    if words > 60:
        score += 0.1
    return max(0.0, min(1.0, score))


def score_riskiness(prediction: str, falsification: str) -> float:
    """Score 0-1: how bold/risky is the prediction?"""
    text = (prediction or '') + ' ' + (falsification or '')
    if not text.strip():
        return 0.0
    score = 0.3  # baseline
    # Bold language
    bold = len(BOLD_PREDICTIONS.findall(text))
    score += min(bold * 0.15, 0.4)
    # Safe language
    safe = len(SAFE_PREDICTIONS.findall(text))
    score -= min(safe * 0.1, 0.3)
    # Predicting own failure is very bold
    if re.search(r'falsif|fail|wrong|incorrect|broken|not work', prediction or '', re.I):
        score += 0.2
    return max(0.0, min(1.0, score))


def score_falsifiability(falsification: str, prediction: str) -> float:
    """Score 0-1: how concrete are the falsification criteria?"""
    text = falsification or prediction or ''
    if not text:
        return 0.0
    score = 0.0
    # Has explicit falsification field
    if falsification:
        score += 0.3
    # Quantitative falsification criteria
    numerics = len(NUMERIC_PATTERN.findall(text))
    score += min(numerics * 0.15, 0.4)
    # Clear conditions
    if re.search(r'\bif\b.*\bthen\b|\bwhen\b.*\bthen\b|\biff\b', text, re.I):
        score += 0.1
    # Precise threshold language
    precise = len(PRECISE_WORDS.findall(text))
    score += min(precise * 0.1, 0.2)
    return max(0.0, min(1.0, score))


def score_surprise(diff_text: str, verdict: str) -> float:
    """Score 0-1: how surprising/informative was the outcome?"""
    if not diff_text:
        return 0.2  # no diff = low information
    score = 0.2
    # Surprise language
    if re.search(r'surpris|unexpect|not predict|unanticipat|novel|counter|opposite|exceeded|wrong', diff_text, re.I):
        score += 0.3
    # Exceeded expectations (partially surprising even if confirmed)
    if re.search(r'exceeded|higher than|more than|beyond|stronger|larger', diff_text, re.I):
        score += 0.15
    # Falsified = inherently surprising (you were wrong)
    if verdict and 'FALSIF' in verdict.upper():
        score += 0.25
    # PARTIALLY = nuanced result
    if verdict and 'PARTIAL' in verdict.upper():
        score += 0.15
    return max(0.0, min(1.0, score))


def classify_verdict(exp: dict) -> str:
    """Extract verdict classification from experiment."""
    verdict = _str(exp.get('verdict'))
    result = _str(exp.get('result'))
    text = (verdict + ' ' + result).upper()
    if 'FALSIF' in text:
        return 'FALSIFIED'
    if 'PARTIAL' in text:
        return 'PARTIAL'
    if 'CONFIRMED' in text:
        return 'CONFIRMED'
    if text.strip():
        return 'OTHER'
    return 'UNKNOWN'


def _str(val) -> str:
    """Coerce any value to string for text analysis."""
    if isinstance(val, str):
        return val
    if val is None:
        return ''
    return json.dumps(val) if isinstance(val, (dict, list)) else str(val)


def score_experiment(exp: dict) -> dict:
    """Score a single experiment's test severity."""
    prediction = _str(exp.get('prediction')) or _str(exp.get('expect')) or ''
    falsification = _str(exp.get('falsification')) or ''
    diff = _str(exp.get('diff')) or ''
    verdict_text = _str(exp.get('verdict')) or _str(exp.get('result')) or ''

    specificity = score_specificity(prediction)
    riskiness = score_riskiness(prediction, falsification)
    falsifiability = score_falsifiability(falsification, prediction)
    surprise = score_surprise(diff, verdict_text)

    # Composite severity (equal weights)
    severity = (specificity + riskiness + falsifiability + surprise) / 4.0

    verdict = classify_verdict(exp)

    # Degree of corroboration: severity × direction
    if verdict == 'CONFIRMED':
        corroboration = severity  # high severity confirmation = strong corroboration
    elif verdict == 'FALSIFIED':
        corroboration = severity * 0.8  # falsification is epistemically valuable
    elif verdict == 'PARTIAL':
        corroboration = severity * 0.6
    else:
        corroboration = 0.0  # unknown outcome = no corroboration

    return {
        'specificity': round(specificity, 3),
        'riskiness': round(riskiness, 3),
        'falsifiability': round(falsifiability, 3),
        'surprise': round(surprise, 3),
        'severity': round(severity, 3),
        'verdict': verdict,
        'corroboration': round(corroboration, 3),
    }


def load_experiments() -> list:
    """Load all experiment JSONs that have prediction/verdict fields."""
    results = []
    for path in sorted(EXPERIMENTS_DIR.rglob("*.json")):
        # Skip cache/meta files
        if path.name.startswith('compact-') or 'cache' in path.name:
            continue
        try:
            with open(path) as f:
                data = json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue

        # Skip non-dict structures (arrays, etc.)
        if not isinstance(data, dict):
            continue

        # Must have some form of prediction AND verdict
        has_prediction = any(data.get(k) for k in ['prediction', 'expect'])
        has_verdict = any(data.get(k) for k in ['verdict', 'result', 'actual'])
        if not (has_prediction or has_verdict):
            continue

        rel = str(path.relative_to(EXPERIMENTS_DIR))
        domain = rel.split('/')[0] if '/' in rel else 'unknown'
        results.append({
            'path': rel,
            'domain': domain,
            'data': data,
        })
    return results


def main():
    parser = argparse.ArgumentParser(description='Popperian degree-of-corroboration scorer')
    parser.add_argument('--json', action='store_true', help='JSON output')
    parser.add_argument('--worst', type=int, default=0, help='Show N weakest-tested experiments')
    parser.add_argument('--best', type=int, default=0, help='Show N strongest-tested experiments')
    args = parser.parse_args()

    experiments = load_experiments()
    scored = []
    for exp in experiments:
        scores = score_experiment(exp['data'])
        scored.append({
            'path': exp['path'],
            'domain': exp['domain'],
            **scores,
        })

    if not scored:
        print("No scorable experiments found.")
        return

    # Statistics
    severities = [s['severity'] for s in scored]
    corroborations = [s['corroboration'] for s in scored]
    verdicts = {}
    for s in scored:
        verdicts[s['verdict']] = verdicts.get(s['verdict'], 0) + 1

    # Severity by verdict
    by_verdict = {}
    for s in scored:
        by_verdict.setdefault(s['verdict'], []).append(s['severity'])

    # Domain averages
    by_domain = {}
    for s in scored:
        by_domain.setdefault(s['domain'], []).append(s['severity'])
    domain_avgs = {d: round(sum(v)/len(v), 3) for d, v in by_domain.items()}

    # Weak vs strong corroboration among CONFIRMED
    confirmed = [s for s in scored if s['verdict'] == 'CONFIRMED']
    weak_confirmed = [s for s in confirmed if s['severity'] < 0.35]
    strong_confirmed = [s for s in confirmed if s['severity'] >= 0.5]

    median_sev = sorted(severities)[len(severities) // 2]

    summary = {
        'total_experiments': len(scored),
        'median_severity': round(median_sev, 3),
        'mean_severity': round(sum(severities) / len(severities), 3),
        'mean_corroboration': round(sum(corroborations) / len(corroborations), 3),
        'verdict_distribution': verdicts,
        'severity_by_verdict': {k: round(sum(v)/len(v), 3) for k, v in by_verdict.items()},
        'confirmed_count': len(confirmed),
        'weak_confirmed': len(weak_confirmed),
        'strong_confirmed': len(strong_confirmed),
        'weak_confirmed_pct': round(len(weak_confirmed) / max(len(confirmed), 1) * 100, 1),
        'domain_severity': dict(sorted(domain_avgs.items(), key=lambda x: -x[1])[:10]),
    }

    if args.json:
        output = {
            'summary': summary,
            'experiments': sorted(scored, key=lambda x: x['severity']),
        }
        json.dump(output, sys.stdout, indent=2)
        return

    # Human-readable report
    print(f"=== POPPERIAN TEST SEVERITY (F-EPIS1, degree of corroboration) ===")
    print(f"Scored: {summary['total_experiments']} experiments")
    print(f"Median severity: {summary['median_severity']} | Mean: {summary['mean_severity']}")
    print(f"Mean corroboration: {summary['mean_corroboration']}")
    print()

    print("--- Verdict distribution ---")
    for v, n in sorted(verdicts.items(), key=lambda x: -x[1]):
        avg_sev = summary['severity_by_verdict'].get(v, 0)
        print(f"  {v:12s}: {n:3d} experiments (avg severity {avg_sev:.3f})")
    print()

    print("--- Corroboration quality (CONFIRMED only) ---")
    print(f"  Total CONFIRMED: {len(confirmed)}")
    print(f"  Weak  (severity < 0.35): {len(weak_confirmed)} ({summary['weak_confirmed_pct']}%)")
    print(f"  Strong (severity >= 0.5): {len(strong_confirmed)} ({round(len(strong_confirmed)/max(len(confirmed),1)*100,1)}%)")
    print()

    print("--- Top domains by severity ---")
    for d, avg in list(sorted(domain_avgs.items(), key=lambda x: -x[1]))[:8]:
        n = len(by_domain[d])
        print(f"  {d:25s}: {avg:.3f} (n={n})")
    print()

    if args.worst:
        print(f"--- {args.worst} weakest-tested experiments ---")
        for s in sorted(scored, key=lambda x: x['severity'])[:args.worst]:
            print(f"  {s['severity']:.3f} [{s['verdict']:10s}] {s['path']}")
        print()

    if args.best:
        print(f"--- {args.best} strongest-tested experiments ---")
        for s in sorted(scored, key=lambda x: -x['severity'])[:args.best]:
            print(f"  {s['severity']:.3f} [{s['verdict']:10s}] corr={s['corroboration']:.3f}  {s['path']}")
        print()


if __name__ == '__main__':
    main()
