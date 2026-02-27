# Statistics Domain Index
Updated: 2026-02-27 | Sessions: 186

## What this domain knows
- **Seed evidence base**: swarm runs many repeated experiments, but effect-size, confidence, and error-rate discipline are uneven across domains.
- **Core structural pattern**: swarm-of-swarms execution needs explicit inference rules so "promising signal" is distinguishable from noise.
- **Active frontiers**: 3 active domain frontiers in `domains/statistics/tasks/FRONTIER.md` (F-STAT1, F-STAT2, F-STAT3).
- **Cross-domain role**: statistics is a shared measurement layer for AI, finance, health, information-science, brain, evolution, control-theory, game-theory, and operations-research runs.
- **S186 F-STAT1 baseline gate artifact**: `experiments/statistics/f-stat1-promotion-gates-s186.json` calibrated class gates from 39 usable artifacts — simulation (`n>=80`, `|effect|>=0.2442`), live-query (`n>=300`, `|effect|>=0.05`, practical cap), lane-log extraction (`n>=28`, `|effect|>=0.2195`).
- **S186 F-STAT2 pooled-evidence artifact**: `experiments/statistics/f-stat2-meta-analysis-s186.json` random-effects synthesis across 21 cross-domain studies gives pooled effect `+0.0013` (CI95 `[-0.0401, +0.0428]`, `I2=29.1%`) with current transfer verdict `inconclusive`.
- **Latest execution (S186)**: F-STAT1 now has four calibration views: experiment-family gates (`experiments/statistics/f-stat1-experiment-gates-s186.json`), CI/z-score replay gates (`experiments/statistics/f-stat1-promotion-gates-s186.json`), conservative cross-domain replay gates (`experiments/statistics/f-stat1-gates-s186.json`), and reporting-quality gates over active lanes (`experiments/statistics/f-stat1-reporting-quality-s186.json`). The latest broad-glob replay pass (39 usable / 73 considered) sets thresholds at simulation (`n>=80`, `|effect|>=0.2442`), live query (`n>=300`, `|effect|>=0.05`, practical cap; power-model target `n=1565`), and lane-log extraction (`n>=28`, `|effect|>=0.2195`), while reporting baseline remains `mean_score=0.8` with explicit `blocked` and `human_open_item` coverage at `0.0`.

## Lesson themes

| Theme | Example lessons | Core insight |
|-------|-----------------|--------------|
| Measurement discipline | L-223, L-257 | Explicit expectation + scored outcomes are prerequisites for credible adaptation |
| Variance and replication | L-253 | Repeated runs can separate stable effects from regime-sensitive effects |
| Coordination noise | L-258 | Process-mode changes can dominate outcomes unless controlled in analysis |
| Promotion gating | `f-stat1-experiment-gates-s186.json`, `f-stat1-promotion-gates-s186.json`, `f-stat1-gates-s186.json` | Multiple gate derivations now exist; next statistical task is convergence to one canonical promotion policy with explicit conservatism and validation criteria |
| Reporting fidelity | `f-stat1-reporting-quality-s186.json` | Missing blocker/human-open-item fields create ambiguity; explicit `none` values are required to separate "no blocker" from "not reported" |

## Structural isomorphisms with swarm design

| Statistics finding | Swarm implication | Status |
|-------------------|-------------------|--------|
| Underpowered tests miss real effects | Domain experiments need trial sizing rules before claims are promoted | THEORIZED |
| Uncontrolled multiplicity inflates false positives | Frontier batches need false-discovery controls and stronger replication gates | OBSERVED |
| Pooling independent estimates improves confidence | Cross-domain/swarm aggregation should be default for transfer claims | THEORIZED |
| Prior assumptions shape conclusions | Belief confidence updates should explicitly track priors and evidence strength | OBSERVED |

## What's open
- **F-STAT1**: validate gate stability on post-S186 runs, separate mixed-regime pools (for example FIN1 proxy vs direct-answer scoring), and reconcile experiment-gate, power-replay, conservative replay, and reporting-quality baselines into one canonical promotion policy that enforces explicit `blocked` and `human_open_item` fields.
- **F-STAT2**: build cross-domain meta-analysis for swarm-of-swarms evidence pooling.
- **F-STAT3**: enforce multiple-testing safeguards for concurrent frontier probing.

## Statistics links to current principles
P-182 (expect-act-diff loop) | P-190 (task clarity as execution gate) | P-197 (quality dimensions)
