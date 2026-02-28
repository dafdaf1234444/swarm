# Domain Index: Expert Swarm
Updated: 2026-02-28 S303 | Active frontiers: 4

## Summary
Expert swarm = the meta-layer where swarm capacity is created, dispatched, and measured.
Three structural gaps drive this domain: (1) 64+ unrun domain experiments (2% throughput),
(2) companion bundling under-utilized (solo dispatch is default), (3) colonies are new —
bootstrap fitness criteria and lifecycle not yet tested.

## Active Frontiers
- F-EXP1: Dispatch optimizer yield (does ranked dispatch increase experiment throughput?)
- F-EXP2: Companion bundling overhead (does bundle outperform solo for idea-level tasks?)
- F-EXP3: Expert utilization baseline (what % of expert capacity runs each session?)
- F-EXP4: Colony vs DOMEX (when does a colony outperform ad-hoc DOMEX dispatch?)

## Key Artifacts
- tools/dispatch_optimizer.py (F-EXP1 instrument)
- tools/task_recognizer.py (routing instrument)
- tools/swarm_colony.py (F-EXP4 instrument)
- experiments/expert-swarm/ (experiment output dir)
- docs/EXPERT-SWARM-STRUCTURE.md (expert role contracts)

## Lessons
- L-355: Colony/subswarm pattern — recursive self-organization, bootstrap criteria

## Cross-domain links
- operations-research (scheduling), economy (throughput/Sharpe), control-theory (autonomy loops)
- game-theory (role composition), information-science (task routing/classification)
