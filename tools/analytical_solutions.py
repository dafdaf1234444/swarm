#!/usr/bin/env python3
"""Analytical solutions for swarm self-improvement (#L-1181).

5 closed-form solutions parameterized from real swarm data. Each outputs
a concrete actionable number. These are MECHANISMS (L-1131 M3 reward
targeting), not descriptions.

Solutions:
  1. L-601 enforcement decay: half-life + periodic cadence prescription
  2. Attention carrying capacity: apoptosis deficit + growth bound
  3. Enforcement Markov chain: stationary distribution + periodic criticality
  4. UCB1 domain balance: optimal c for target Gini
  5. Thermodynamic closure: external input rate for target discovery ratio

Usage:
  python3 tools/analytical_solutions.py              # full report
  python3 tools/analytical_solutions.py --solution N  # single solution
  python3 tools/analytical_solutions.py --json        # machine-readable
  python3 tools/analytical_solutions.py --prescribe   # actionable changes only

Cites: L-601, L-950, L-1118, L-1121, L-1124, L-1127, L-1129, L-1131
"""

import argparse
import json
import math
import os
import re
import subprocess
import sys


def _count_lessons():
    """Count total and expired lessons."""
    lessons_dir = os.path.join(os.path.dirname(__file__), '..', 'memory', 'lessons')
    total = 0
    expired = 0
    for f in os.listdir(lessons_dir):
        if f.startswith('L-') and f.endswith('.md'):
            total += 1
            with open(os.path.join(lessons_dir, f)) as fh:
                content = fh.read(500)
                if any(tag in content for tag in ('EXPIRED', 'SUPERSEDED', 'ARCHIVED')):
                    expired += 1
    return total, expired


def _get_session_number():
    """Get current session number from NEXT.md."""
    next_path = os.path.join(os.path.dirname(__file__), '..', 'tasks', 'NEXT.md')
    with open(next_path) as f:
        first_line = f.readline()
    m = re.search(r'S(\d+)', first_line)
    return int(m.group(1)) if m else 472


def _get_enforcement_rate():
    """Get current enforcement rate from enforcement_router.py."""
    try:
        result = subprocess.run(
            [sys.executable, os.path.join(os.path.dirname(__file__), 'enforcement_router.py'),
             '--min-sharpe', '0', '--top', '1'],
            capture_output=True, text=True, timeout=30
        )
        m = re.search(r'Enforcement rate:\s+([\d.]+)%', result.stdout)
        return float(m.group(1)) / 100 if m else 0.29
    except Exception:
        return 0.29


def _get_ucb1_gini():
    """Get current UCB1 visit Gini from dispatch_optimizer.py."""
    try:
        result = subprocess.run(
            [sys.executable, os.path.join(os.path.dirname(__file__), 'dispatch_optimizer.py')],
            capture_output=True, text=True, timeout=30
        )
        m = re.search(r'Visit Gini:\s+([\d.]+)', result.stdout)
        return float(m.group(1)) if m else 0.51
    except Exception:
        return 0.51


# ── Solution 1: L-601 Enforcement Decay ──────────────────────────────

def enforcement_decay(enforcement_rate=None):
    """Exponential decay model for voluntary enforcement.

    Model: e(t) = e_structural + e_voluntary * lambda^(t - t0)

    Calibrated from empirical data:
      S422: 19.3% → S444: 10.0% (22 sessions, structural floor ~8%)
      lambda = (2.0/11.3)^(1/22) = 0.924
      Half-life = ln(2)/ln(1/lambda) = 8.8 sessions

    Returns dict with model parameters and prescriptions.
    """
    # Empirical calibration points
    e_s422 = 0.193
    e_s444 = 0.100
    dt = 22  # sessions between measurements
    e_floor_old = 0.08  # structural floor before auto-discovery

    # Voluntary components
    ev_422 = e_s422 - e_floor_old  # 0.113
    ev_444 = e_s444 - e_floor_old  # 0.020

    # Decay rate
    lam = (ev_444 / ev_422) ** (1 / dt)  # 0.924
    decay_per_session = 1 - lam  # 0.076

    # Half-life
    half_life = math.log(2) / math.log(1 / lam)  # 8.8 sessions

    # Time to 12.5% (3 half-lives)
    negligible_time = 3 * half_life  # 26.4 sessions

    # Current state
    e_current = enforcement_rate or _get_enforcement_rate()

    return {
        'name': 'L-601 Enforcement Decay',
        'model': 'e(t) = e_structural + e_voluntary * 0.924^t',
        'parameters': {
            'lambda': round(lam, 4),
            'decay_per_session': round(decay_per_session, 4),
            'half_life_sessions': round(half_life, 1),
            'negligible_at_sessions': round(negligible_time, 1),
        },
        'current': {
            'enforcement_rate': round(e_current, 3),
        },
        'prescription': {
            'periodic_cadence_max': math.floor(half_life),
            'rationale': f'Periodic must run every ≤{math.floor(half_life)} sessions '
                         f'(half-life) to prevent voluntary decay below detection.',
        },
        'cites': ['L-601', 'L-1131'],
    }


# ── Solution 2: Attention Carrying Capacity ───────────────────────────

def attention_capacity():
    """Logistic growth model with knowledge apoptosis.

    Model:
      K = A_total / a_min  (carrying capacity)
      A_total = N_transition * a_min = 575 * 0.002 = 1.15
      Growth sustainable when: apoptosis_rate >= production_rate - (K - N_eff)/K * r

    Returns dict with capacity analysis and apoptosis prescription.
    """
    N_total, N_expired = _count_lessons()
    N_eff = N_total - N_expired

    # Empirical parameters
    a_min = 0.002   # minimum attention per lesson (L-1121)
    N_transition = 575  # production→integration bound (L-912)
    A_total = N_transition * a_min  # total attention budget = 1.15

    # Carrying capacity
    K = A_total / a_min  # = 575 (same as transition point, by construction)

    # Current attention per lesson
    a_current = A_total / N_eff if N_eff > 0 else 0

    # How far over capacity
    over_capacity = max(0, N_eff - K)
    capacity_ratio = N_eff / K if K > 0 else float('inf')

    # Apoptosis needed to return to capacity
    apoptosis_needed = over_capacity

    # Production rate (from recent data: ~2.0 L/session)
    r_production = 2.0  # lessons/session
    # Current apoptosis rate (EXPIRED/total_sessions)
    session = _get_session_number()
    r_apoptosis_actual = N_expired / session if session > 0 else 0
    r_apoptosis_deficit = r_production - (r_apoptosis_actual * (K / N_eff if N_eff > 0 else 1))

    # Attention amplification needed (alternative to apoptosis)
    A_needed = N_eff * a_min
    amplification_needed = A_needed / A_total

    return {
        'name': 'Attention Carrying Capacity',
        'model': 'K = A_total / a_min; sustainable iff N_eff ≤ K',
        'parameters': {
            'a_min': a_min,
            'A_total': round(A_total, 3),
            'K': K,
        },
        'current': {
            'N_total': N_total,
            'N_expired': N_expired,
            'N_effective': N_eff,
            'attention_per_lesson': round(a_current, 5),
            'capacity_ratio': round(capacity_ratio, 2),
            'over_capacity_by': over_capacity,
        },
        'prescription': {
            'apoptosis_target': apoptosis_needed,
            'apoptosis_rate_deficit': round(r_apoptosis_deficit, 2),
            'amplification_alternative': f'{amplification_needed:.1f}x attention improvement needed',
            'rationale': f'System is at {capacity_ratio:.1f}x carrying capacity. '
                         f'Need {apoptosis_needed} lesson retirements OR '
                         f'{amplification_needed:.1f}x attention amplification '
                         f'(better routing/indexing tools).',
        },
        'cites': ['L-1121', 'L-912', 'L-601'],
    }


# ── Solution 3: Enforcement Markov Chain ──────────────────────────────

def enforcement_markov():
    """Markov chain stationary distribution for enforcement states.

    States: {Enforced (E), Partial (P), Zero (Z)}
    Observed equilibrium: (0.40, 0.47, 0.13) from L-950

    Transition rates (per session):
      alpha = E→P decay = 0.076 (from Solution 1)
      beta  = P→Z dilution ≈ 0.001
      gamma = Z→E structural wiring ≈ 0.0036
      delta = P→E periodic re-enforcement ≈ 0.064

    Key finding: delta accounts for 97.5% of the enforcement equilibrium.
    Without the enforcement-audit periodic, E drops from 40% to ~1%.
    """
    # Parameters from calibration
    alpha = 0.076   # E→P (L-601 decay)
    beta = 0.001    # P→Z (attention dilution)
    gamma = 0.0036  # Z→E (structural wiring)
    delta = 0.064   # P→E (periodic re-enforcement)

    # Current equilibrium (with periodic)
    pi_E = 0.40
    pi_P = 0.47
    pi_Z = 0.13

    # Equilibrium WITHOUT periodic (delta=0)
    # pi_E = 1 / (1 + alpha/beta + alpha/gamma)
    denom_no_periodic = 1 + alpha / beta + alpha / gamma
    pi_E_no_periodic = 1 / denom_no_periodic
    pi_P_no_periodic = (alpha / beta) * pi_E_no_periodic
    pi_Z_no_periodic = (alpha / gamma) * pi_E_no_periodic

    # Periodic contribution
    periodic_contribution = (pi_E - pi_E_no_periodic) / pi_E

    # Sensitivity: how much does doubling delta improve enforcement?
    delta_2x = delta * 2
    # Approximate: pi_E ~ delta / (alpha + delta) for large delta/alpha ratio
    pi_E_2x_delta = (gamma * pi_Z + delta_2x * pi_P + pi_E * (1 - alpha))
    # Use full system solution
    # Simplified: pi_E ≈ delta / alpha (when delta dominates)
    approx_improvement = delta_2x / (delta_2x + alpha)

    return {
        'name': 'Enforcement Markov Chain',
        'model': '3-state Markov: {Enforced, Partial, Zero}',
        'parameters': {
            'alpha_decay': alpha,
            'beta_dilution': beta,
            'gamma_structural': gamma,
            'delta_periodic': delta,
        },
        'current': {
            'equilibrium_with_periodic': {'E': pi_E, 'P': pi_P, 'Z': pi_Z},
            'equilibrium_without_periodic': {
                'E': round(pi_E_no_periodic, 4),
                'P': round(pi_P_no_periodic, 4),
                'Z': round(pi_Z_no_periodic, 4),
            },
        },
        'prescription': {
            'periodic_criticality': round(periodic_contribution, 3),
            'enforcement_if_periodic_removed': f'{pi_E_no_periodic:.1%}',
            'delta_vs_gamma_ratio': round(delta / gamma, 1),
            'rationale': f'Enforcement-audit periodic provides {periodic_contribution:.1%} '
                         f'of enforcement equilibrium. Without it, enforcement drops from '
                         f'{pi_E:.0%} to {pi_E_no_periodic:.1%}. '
                         f'Periodic re-enforcement (delta={delta}) is '
                         f'{delta/gamma:.0f}x more effective than structural wiring (gamma={gamma}). '
                         f'This is the single most critical periodic in the system.',
        },
        'cites': ['L-950', 'L-601', 'L-1131'],
    }


# ── Solution 4: UCB1 Domain Balance ───────────────────────────────────

def ucb1_balance(current_gini=None):
    """Optimal UCB1 exploration parameter for target domain Gini.

    Model:
      G(c) ≈ G_0 * exp(-c / c_0)
      Calibrated: G(0)=0.8 (pure exploitation), G(1.414)=0.510

    Analytical solution for c given target Gini G*:
      c* = -c_0 * ln(G* / G_0)
    """
    # Empirical calibration
    G_0 = 0.80     # Gini at c=0 (pure exploitation)
    c_current = 1.414  # current UCB1 c (sqrt(2))
    G_current = current_gini or _get_ucb1_gini()

    # Solve for c_0: G_current = G_0 * exp(-c_current / c_0)
    if G_current > 0 and G_0 > 0 and G_current < G_0:
        c_0 = -c_current / math.log(G_current / G_0)
    else:
        c_0 = 3.0  # fallback

    # Target Gini levels and their c values
    targets = {}
    for label, g_target in [('balanced_0.3', 0.30), ('moderate_0.4', 0.40), ('current', G_current)]:
        if g_target > 0 and g_target < G_0:
            c_star = -c_0 * math.log(g_target / G_0)
            targets[label] = {'gini_target': g_target, 'c_optimal': round(c_star, 3)}

    # Marginal effect: dG/dc at current c
    dG_dc = -(G_0 / c_0) * math.exp(-c_current / c_0)

    return {
        'name': 'UCB1 Domain Balance',
        'model': 'G(c) = 0.80 * exp(-c / c_0)',
        'parameters': {
            'G_0': G_0,
            'c_0': round(c_0, 3),
            'c_current': c_current,
        },
        'current': {
            'gini': round(G_current, 3),
            'marginal_effect': round(dG_dc, 4),
        },
        'targets': targets,
        'prescription': {
            'c_for_gini_0.3': targets.get('balanced_0.3', {}).get('c_optimal', 'N/A'),
            'c_for_gini_0.4': targets.get('moderate_0.4', {}).get('c_optimal', 'N/A'),
            'rationale': f'Current c=1.414 gives Gini={G_current:.3f}. '
                         f'For Gini=0.30 (Goldstone symmetry restoration), '
                         f'increase c to ~{targets.get("balanced_0.3", {}).get("c_optimal", "N/A")}. '
                         f'Each +1 to c reduces Gini by ~{abs(dG_dc):.3f}.',
        },
        'cites': ['L-1124', 'L-1129', 'L-1131'],
    }


# ── Solution 5: Thermodynamic Closure ─────────────────────────────────

def thermodynamic_closure():
    """External input rate needed to achieve target discovery ratio.

    Model:
      R = [(1-f)*p_ci + f*p_ce] / [(1-f)*p_di + f*p_de]

    where:
      f = fraction of external references
      p_ci = P(confirm | internal) = 0.90
      p_di = P(discover | internal) = 0.10
      p_ce = P(confirm | external) = 0.40
      p_de = P(discover | external) = 0.60

    Analytical solution for f given target R*:
      f* = (p_ci - R*·p_di) / (p_ci - R*·p_di - p_ce + R*·p_de)
    """
    # Empirical parameters
    f_current = 0.026   # 2.6% external (L-1118)
    p_ci = 0.90   # P(confirm | internal)
    p_di = 0.10   # P(discover | internal)
    p_ce = 0.40   # P(confirm | external)
    p_de = 0.60   # P(discover | external)

    # Current discovery ratio
    R_current = ((1 - f_current) * p_ci + f_current * p_ce) / \
                ((1 - f_current) * p_di + f_current * p_de)

    # Analytical solution for f* given target R*
    def f_star(R_target):
        numerator = p_ci - R_target * p_di
        denominator = p_ci - R_target * p_di - p_ce + R_target * p_de
        if abs(denominator) < 1e-10:
            return float('inf')
        f = numerator / denominator
        return max(0, min(1, f))

    targets = {}
    for label, R_target in [('healthy_3', 3.0), ('moderate_5', 5.0), ('improved_7', 7.0)]:
        f = f_star(R_target)
        multiplier = f / f_current if f_current > 0 else float('inf')
        targets[label] = {
            'R_target': R_target,
            'f_needed': round(f, 4),
            'multiplier_vs_current': round(multiplier, 1),
        }

    # Sensitivity: dR/df at current f
    def R_of_f(f):
        return ((1 - f) * p_ci + f * p_ce) / ((1 - f) * p_di + f * p_de)

    dR_df = (R_of_f(f_current + 0.001) - R_of_f(f_current)) / 0.001

    return {
        'name': 'Thermodynamic Closure',
        'model': 'R = [(1-f)·p_ci + f·p_ce] / [(1-f)·p_di + f·p_de]',
        'parameters': {
            'p_ci': p_ci,
            'p_di': p_di,
            'p_ce': p_ce,
            'p_de': p_de,
            'f_current': f_current,
        },
        'current': {
            'R_current': round(R_current, 1),
            'sensitivity_dR_df': round(dR_df, 1),
        },
        'targets': targets,
        'prescription': {
            'f_for_R5': targets['moderate_5']['f_needed'],
            'multiplier': targets['moderate_5']['multiplier_vs_current'],
            'rationale': f'Current external rate {f_current:.1%} gives R={R_current:.1f}:1. '
                         f'For R=5:1, need f={targets["moderate_5"]["f_needed"]:.1%} '
                         f'({targets["moderate_5"]["multiplier_vs_current"]:.0f}x increase). '
                         f'For R=3:1, need f={targets["healthy_3"]["f_needed"]:.1%} '
                         f'({targets["healthy_3"]["multiplier_vs_current"]:.0f}x). '
                         f'Each +1% external input reduces R by ~{abs(dR_df)/100:.1f}.',
        },
        'cites': ['L-1118', 'L-1125', 'L-1131'],
    }


# ── Main ──────────────────────────────────────────────────────────────

ALL_SOLUTIONS = [
    enforcement_decay,
    attention_capacity,
    enforcement_markov,
    ucb1_balance,
    thermodynamic_closure,
]


def run_all():
    results = []
    for fn in ALL_SOLUTIONS:
        try:
            results.append(fn())
        except Exception as e:
            results.append({'name': fn.__name__, 'error': str(e)})
    return results


def print_report(results, prescribe_only=False):
    print('=' * 70)
    print('ANALYTICAL SOLUTIONS FOR SWARM SELF-IMPROVEMENT')
    print(f'5 closed-form models | parameterized from N={_count_lessons()[0]} lessons')
    print('=' * 70)

    for i, r in enumerate(results, 1):
        print(f'\n{"─" * 70}')
        print(f'  Solution {i}: {r["name"]}')
        print(f'{"─" * 70}')

        if 'error' in r:
            print(f'  ERROR: {r["error"]}')
            continue

        if not prescribe_only:
            print(f'  Model: {r["model"]}')
            if 'parameters' in r:
                print(f'  Parameters:')
                for k, v in r['parameters'].items():
                    print(f'    {k}: {v}')
            if 'current' in r:
                print(f'  Current state:')
                for k, v in r['current'].items():
                    if isinstance(v, dict):
                        print(f'    {k}: {v}')
                    else:
                        print(f'    {k}: {v}')

        print(f'  Prescription:')
        rx = r.get('prescription', {})
        for k, v in rx.items():
            if k == 'rationale':
                # Word-wrap rationale
                words = str(v).split()
                lines = []
                line = '    '
                for w in words:
                    if len(line) + len(w) + 1 > 68:
                        lines.append(line)
                        line = '    '
                    line += w + ' '
                lines.append(line)
                print(f'    RATIONALE:')
                for l in lines:
                    print(l)
            else:
                print(f'    {k}: {v}')

    # Summary prescriptions
    print(f'\n{"=" * 70}')
    print('SUMMARY — ACTIONABLE PARAMETER CHANGES')
    print('=' * 70)
    for i, r in enumerate(results, 1):
        if 'error' in r:
            continue
        rx = r.get('prescription', {})
        key_items = {k: v for k, v in rx.items() if k != 'rationale'}
        if key_items:
            print(f'  [{i}] {r["name"]}:')
            for k, v in key_items.items():
                print(f'      {k} = {v}')


def main():
    parser = argparse.ArgumentParser(description='Analytical solutions for swarm self-improvement')
    parser.add_argument('--solution', type=int, choices=range(1, 6),
                        help='Show only solution N (1-5)')
    parser.add_argument('--json', action='store_true', help='JSON output')
    parser.add_argument('--prescribe', action='store_true', help='Prescriptions only')
    args = parser.parse_args()

    if args.solution:
        results = [ALL_SOLUTIONS[args.solution - 1]()]
    else:
        results = run_all()

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print_report(results, prescribe_only=args.prescribe)


if __name__ == '__main__':
    main()
