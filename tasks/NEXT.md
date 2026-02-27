# Next Session Handoff
Updated: 2026-02-27 (S54 — extended: F103 resolved, repo census, darts analysis, colony ops)

## Do First
- Run `/swarm` — fractal session command
- Read `tasks/COURSE-CORRECTION.md` — 5 active directives
- Read `tasks/HUMAN-QUEUE.md` — HQ-1, HQ-4, HQ-5 still unanswered

## What was done this session (S54 extended)
- **F103 RESOLVED**: 3rd test (ilkerloan, multi-domain sparse-docs) — MULTIPLICATIVE advantage confirmed. P-114 refined: swarm advantage = f(domain_count × doc_sparsity). L-110.
- **F102 session 2/3**: Missing falsification NOT noticed during routine work. No drift.
- **F104 DONE** (concurrent): Personality test — skeptic vs explorer on etcd EH. P-116 written.
- **Repo census complete**: 9 repos analyzed. All user code = zero cycles (except bets: 1). Star topology dominance. Bimodal docs. See repo-census-2026-02-27.md.
- **darts deep analysis**: CRITICAL data leakage (bfill on features + target), non-stationary target, unadjusted prices, no early stopping. See darts-quant-framework-analysis.md.
- **HUMAN.md extended**: Cognitive patterns documented, F108 opened (human modeling).

## Key Findings for User

### darts/quant_framework (CRITICAL)
1. **`bfill()` = data leakage** (feature_engineering.py:43 + backtesting.py:200): Future data leaks into features AND target prices. All backtest results unreliable. **Fix: remove bfill()**.
2. **Training on raw prices** (non-stationary): Should use returns/log-returns.
3. **`auto_adjust=False`**: Stock splits create phantom price drops.
4. **No early stopping**: TFT at 50 epochs on ~250 days likely overfits.

### bets analyzer (from S53)
1. **50 bare `except:` blocks** → silent data corruption
2. **Cycle**: `analysis ↔ feature_engineering` — break it (1-2h)
3. **Prior analysis docs wrong**: 3 features claimed "missing" but exist

### ilkerloan (from S54)
1. **Missing jurisdiction clause**: Forces Belgian litigation under Dutch law
2. **Box 3 hidden tax**: ~EUR 432/year on the receivable
3. **Date inconsistency**: `date.today()` vs hardcoded Feb 14, 2036

## High-Priority for S55

- **F102 DECISION**: Session 3/3. Check B7/B8/B12 for drift. Decide: apply to all or revert.
- **Push repo**: 75+ commits ahead. Every session = more catastrophic loss risk.
- **F107**: Ablation child session 2. Next atom: `always:swarmability`.
- **F100/F108**: CockroachDB K_out replication (resolves P-110 + F108-Q4).
- **Archive stale frontiers**: F75, F77, F92 (40+ sessions, no progress).

## Warnings
- **F102**: S55 = FINAL deadline. Decide or lose the experiment's data.
- **P-110**: HYPOTHESIS until CockroachDB replication.
- **Push the repo**: Directive #4 in COURSE-CORRECTION. Still not done.
- **24 open frontier questions**: trim the stale ones.

## Read These
- `experiments/complexity-applied/repo-census-2026-02-27.md` — NEW: full repo inventory
- `experiments/complexity-applied/darts-quant-framework-analysis.md` — NEW: critical bugs
- `experiments/complexity-applied/f103-ilkerloan-multi-domain.md` — NEW: F103 test 3
- `experiments/architecture/f107-genesis-ablation.md` — genesis ablation protocol
