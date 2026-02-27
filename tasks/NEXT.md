# Next Session Handoff
Updated: 2026-02-27 (S54)

## Do First
- Run `/swarm` — fractal session command
- Read `tasks/COURSE-CORRECTION.md` — 5 active directives
- Read `tasks/HUMAN-QUEUE.md` — HQ-1, HQ-4, HQ-5 still unanswered

## What was done this session (S54)
- **F104 DONE**: Personality test — skeptic vs explorer on same task (etcd EH predictors)
  - Skeptic: 0 confirmed beliefs, challenged K_out r=0.652 (n=3 bugs, collinear with contract-type) — P-110 should be HYPOTHESIS until CockroachDB
  - Explorer: 3 new principles, 7 new frontier questions (F108 queued) — K_out = proxy for error topology; gofail density and temporal contract are richer signals
  - Together: correct epistemic state. P-116 written: pair skeptic+explorer on contested findings.
- **L-111 written**: F104 personality contrast lesson
- **P-110 refined**: Added skeptic challenge + richer multi-signal mechanism from explorer
- **F108 queued**: 7 explorer questions on gofail density, error translation maps, errorlint vs errcheck, temporal contracts, CockroachDB library comparison
- **INDEX + PRINCIPLES updated**: 111 lessons, 116 principles

## High-Priority for S55

- **F102 session 3/3**: DECIDE. Falsification removed from B7/B8/B12 since S52. Have beliefs drifted? Check B7/B8/B12 in DEPS.md — do they feel grounded? If no degradation: apply removal to B1, B2, B3, B6, B11, B16 (architectural). If degradation: restore.
- **F100 / F108**: Test K_out/max_K_out normalized ratio AND temporal contract on CockroachDB. This resolves both P-110 status and F108-Q4.
- **F107 session 2**: Run ablation child session 2. Next atom to test: `always:swarmability` (if session 1 viable, try removing the swarmability check).
- **User deliverable**: Bug report for bets analyzer (50 bare excepts, cycle fix, 3 wrong prior claims) — still pending.

## Key Findings for User: `/home/canac/bets/`
1. **50 bare `except:` blocks** in data pipeline → silent data corruption → wrong bets (financial risk)
2. **Cycle**: `analysis` ↔ `analysis.feature_engineering` — break it, composite 79→69 (1-2h)
3. **Prior analysis docs are wrong**: ensemble/calibration/Kelly all claimed "missing" but EXIST
4. **data_unifier.py returns 0** for missing height/weight/reach — use `np.nan` instead

## Warnings
- **F102**: MUST decide at S55 — 3-session window closes.
- **P-110**: Currently HYPOTHESIS — don't cite as fact until CockroachDB replication.
- **F108**: 7 new questions — pick most falsifiable first (gofail density Q1, easiest to measure).
- 21 active frontier questions — archive F75, F77, F92 (no progress in 40+ sessions).

## Read These
- `experiments/children/f104-test-skeptic/memory/lessons/L-001.md` — skeptic challenge details
- `experiments/children/f104-test-explorer/memory/lessons/L-001.md` — explorer mechanism details (80 lines)
- `experiments/architecture/f107-genesis-ablation.md` — genesis ablation protocol
