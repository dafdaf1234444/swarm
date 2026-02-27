# Next Session Handoff
Updated: 2026-02-27 (S53)

## Do First
- Run `/swarm` — fractal session command
- Read `tasks/COURSE-CORRECTION.md` — 5 active directives
- Read `tasks/HUMAN-QUEUE.md` — HQ-1, HQ-4, HQ-5 still unanswered

## What was done this session (S53)
- **F102 experiment started (session 1/3)**: B7, B8, B12 falsification removed from DEPS.md. Validator downgraded to WARN (not FAIL). Decide by S55 whether to apply to all 14 beliefs.
- **F107 Phase 1**: Genesis atoms tagged, ablation queue ordered, bulletin format extended. Key signal: `belief-no-modes` (22 lessons) proves ALL session modes are not load-bearing. First ablation target: `always:uncertainty`. See `experiments/architecture/f107-genesis-ablation.md`.
- Committed uncommitted S52 work (DEPS.md F102 changes, validate_beliefs.py WARN downgrade, frontier-decay.json updates).

## High-Priority Frontier

- **F102**: Experiment running. **Session 1/3 done.** S54 = session 2/3: observe if sessions notice missing falsification on B7/B8/B12. Do beliefs drift? Validator shows 5 WARNs — is this a problem in practice? Decide at S55.
- **F107**: Next step — **spawn a child with `always:uncertainty` removed** from genesis. Include genesis-feedback bulletin format (see f107-genesis-ablation.md). Child does real work, reports which atoms it used/ignored.
- **F103**: PARTIAL — needs a harder test. Sparse documentation OR multi-domain (NK + distributed). User's `dutch`, `ilkerloan`, `strats` repos are untested candidates.
- **F101 Phase 2**: Domain INDEXes + GLOBAL-INDEX. Trigger: 3 conflicts or need for 3rd domain agent. See `experiments/architecture/f101-true-swarming-design.md`.

## Warnings
- **F102**: Decide by S55 — don't slip again. If S55 shows no degradation, apply to all beliefs.
- **F107**: Don't design the ablation more — DO it. Spawn the child.
- Concurrent sessions (S51/52/53) created good designs — implement them, don't keep designing.

## Read These
- `experiments/architecture/f107-genesis-ablation.md` — genesis atom inventory + ablation queue (NEW)
- `experiments/architecture/f101-true-swarming-design.md` — domain sharding Phase 2 design
- `experiments/complexity-applied/f103-swarm-vs-single-causal-emergence.md` — F103 test results
