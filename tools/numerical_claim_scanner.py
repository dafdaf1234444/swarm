#!/usr/bin/env python3
"""FM-27 hardening: detect unstamped/stale numerical claims in lesson body text.

Body-text numerical claims decay at ~0.7%/session (L-894, L-887). Header counts
are guarded by check_count_drift() but body-text numbers are invisible to GC.

Two modes:
  --staged   : pre-commit check — scan staged lessons for unstamped claims (NOTICE)
  --audit    : periodic scan — find stale @S{NNN} timestamps across all lessons
  --session S : current session number (for staleness calculation)

Wires into check.sh as NOTICE-level advisory. #L-894 #L-887 #FM-27
"""

import argparse
import glob
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Numerical claim patterns (capture the claim text for reporting)
CLAIM_PATTERNS = [
    (r'(\d+\.?\d*)\s*%', 'percentage'),          # "35.2%"
    (r'(\d+)/(\d+)\s', 'ratio'),                  # "3/9 " (with trailing space to avoid paths)
    (r'(\d+\.?\d*)x\b', 'multiplier'),            # "4.76x"
    (r'[Nn]\s*[=≈~]\s*(\d+)', 'sample_size'),     # "N=1000", "n≈50"
]

# Timestamp pattern: @S{NNN} or @SNNN
TIMESTAMP_RE = re.compile(r'@S\{?(\d+)\}?')

# Lines to skip (headers, metadata, code blocks, cites)
SKIP_LINE_RE = re.compile(
    r'^(#|Session:|Domain:|Frontier:|Sharpe:|Level:|Confidence:|Cites:|'
    r'Falsified if:|Message:|```|--)'
)

# Patterns that look numerical but aren't claims (lesson IDs, session refs, file paths)
FALSE_POSITIVE_RE = re.compile(
    r'L-\d+|S\d{3}|P-\d+|B-\d+|F-\w+|FM-\d+|PHIL-\d+|SIG-\d+|'
    r'line \d+|v\d+\.\d+|tools/|memory/|domains/|experiments/'
)


def extract_claims(text: str) -> list[dict]:
    """Extract numerical claims from lesson body text."""
    claims = []
    in_code_block = False

    for line_num, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith('```'):
            in_code_block = not in_code_block
            continue
        if in_code_block or SKIP_LINE_RE.match(stripped):
            continue
        if not stripped or stripped.startswith('|---'):
            continue

        for pattern, claim_type in CLAIM_PATTERNS:
            for match in re.finditer(pattern, stripped):
                claim_text = match.group(0)
                # Skip if embedded in a false-positive context
                start = max(0, match.start() - 20)
                end = min(len(stripped), match.end() + 20)
                context = stripped[start:end]
                if FALSE_POSITIVE_RE.search(context):
                    # Check if the match itself IS the false positive
                    if FALSE_POSITIVE_RE.search(claim_text):
                        continue

                # Check for nearby @S timestamp
                nearby = stripped[max(0, match.start() - 40):min(len(stripped), match.end() + 40)]
                ts_match = TIMESTAMP_RE.search(nearby)
                timestamp = int(ts_match.group(1)) if ts_match else None

                claims.append({
                    'line': line_num,
                    'claim': claim_text,
                    'type': claim_type,
                    'timestamp': timestamp,
                    'context': stripped[:80],
                })

    return claims


def scan_lesson(path: Path, current_session: int = 0) -> dict:
    """Scan a single lesson for numerical claims."""
    text = path.read_text(encoding='utf-8', errors='replace')
    claims = extract_claims(text)

    unstamped = [c for c in claims if c['timestamp'] is None]
    stale = [c for c in claims if c['timestamp'] is not None
             and current_session > 0
             and current_session - c['timestamp'] > 50]

    return {
        'path': str(path),
        'total_claims': len(claims),
        'unstamped': len(unstamped),
        'stale': len(stale),
        'unstamped_claims': unstamped[:5],  # cap for readability
        'stale_claims': stale[:5],
    }


def check_staged(current_session: int = 0) -> list[tuple[str, str]]:
    """Pre-commit check: scan staged lesson files for unstamped claims."""
    results = []
    try:
        staged = subprocess.check_output(
            ['git', 'diff', '--cached', '--name-only', '--diff-filter=AM'],
            cwd=REPO_ROOT, text=True
        ).strip().splitlines()
    except subprocess.CalledProcessError:
        return results

    lesson_files = [f for f in staged if re.match(r'memory/lessons/L-\d+\.md$', f)]
    if not lesson_files:
        return results

    total_unstamped = 0
    flagged = []
    for f in lesson_files:
        path = REPO_ROOT / f
        if not path.exists():
            continue
        result = scan_lesson(path, current_session)
        if result['unstamped'] > 0:
            total_unstamped += result['unstamped']
            flagged.append(f"{Path(f).name}({result['unstamped']})")

    if flagged:
        results.append((
            'NOTICE',
            f"FM-27: {total_unstamped} unstamped numerical claim(s) in {', '.join(flagged)} — "
            f"add @S{{{current_session or 'NNN'}}} timestamps (L-894)"
        ))

    return results


def audit_all(current_session: int) -> dict:
    """Periodic audit: scan all lessons for stale timestamps."""
    lessons_dir = REPO_ROOT / 'memory' / 'lessons'
    if not lessons_dir.exists():
        return {'error': 'lessons directory not found'}

    total_claims = 0
    total_unstamped = 0
    total_stale = 0
    lesson_count = 0
    worst = []

    for path in sorted(lessons_dir.glob('L-*.md')):
        result = scan_lesson(path, current_session)
        lesson_count += 1
        total_claims += result['total_claims']
        total_unstamped += result['unstamped']
        total_stale += result['stale']
        if result['stale'] > 0:
            worst.append((result['stale'], path.name))

    worst.sort(reverse=True)
    stamped = total_claims - total_unstamped
    stamp_rate = stamped / total_claims * 100 if total_claims > 0 else 0

    return {
        'session': current_session,
        'lessons_scanned': lesson_count,
        'total_claims': total_claims,
        'unstamped': total_unstamped,
        'stamped': stamped,
        'stale': total_stale,
        'stamp_rate_pct': round(stamp_rate, 1),
        'stale_rate_pct': round(total_stale / max(stamped, 1) * 100, 1),
        'worst_stale': worst[:10],
    }


def main():
    parser = argparse.ArgumentParser(description='FM-27: numerical claim scanner')
    parser.add_argument('--staged', action='store_true', help='Pre-commit: check staged lessons')
    parser.add_argument('--audit', action='store_true', help='Periodic: audit all lessons')
    parser.add_argument('--session', type=int, default=0, help='Current session number')
    parser.add_argument('--file', type=str, help='Scan a single file')
    args = parser.parse_args()

    if args.staged:
        results = check_staged(args.session)
        for level, msg in results:
            print(f"  [{level}] {msg}")
        sys.exit(0)

    if args.file:
        result = scan_lesson(Path(args.file), args.session)
        print(f"Claims: {result['total_claims']} | Unstamped: {result['unstamped']} | Stale: {result['stale']}")
        for c in result['unstamped_claims']:
            print(f"  L{c['line']}: {c['claim']} ({c['type']}) — {c['context'][:60]}")
        sys.exit(0)

    if args.audit:
        if args.session == 0:
            print("Error: --session required for --audit (staleness calculation)")
            sys.exit(1)
        report = audit_all(args.session)
        print(f"FM-27 Audit @ S{report['session']}")
        print(f"  Lessons scanned: {report['lessons_scanned']}")
        print(f"  Total claims: {report['total_claims']}")
        print(f"  Stamped: {report['stamped']} ({report['stamp_rate_pct']}%)")
        print(f"  Unstamped: {report['unstamped']}")
        print(f"  Stale (>50s): {report['stale']} ({report['stale_rate_pct']}% of stamped)")
        if report.get('worst_stale'):
            print(f"  Worst stale: {', '.join(f'{n}:{c}' for c,n in report['worst_stale'][:5])}")
        sys.exit(0)

    parser.print_help()


if __name__ == '__main__':
    main()
