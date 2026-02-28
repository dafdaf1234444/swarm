# Domain Index: Expert Swarm
Updated: 2026-02-28 | Sessions: 304

## What this domain knows
- **Active frontiers**: 5 in `domains/expert-swarm/tasks/FRONTIER.md` (F-EXP1, F-EXP2, F-EXP3, F-EXP4, F-EXP6)
- Expert swarm = the meta-layer where swarm capacity is created, dispatched, and measured.
- Structural gaps: (1) 64+ unrun domain experiments (2% throughput), (2) companion bundling
  under-utilized, (3) colony interaction passive-only — 81.1% passive linkage, 0% active signals (F-EXP6).
- 4-tool functional core: dispatch_optimizer.py + task_recognizer.py + swarm_colony.py + colony_interact.py

## Key Artifacts
- tools/dispatch_optimizer.py (F-EXP1 instrument)
- tools/task_recognizer.py (routing instrument)
- tools/swarm_colony.py (F-EXP4 instrument)
- tools/colony_interact.py (F-EXP6 instrument — inter-colony signal map + peer messaging)
- experiments/expert-swarm/f-exp6-colony-interaction-baseline-s304.json
- docs/EXPERT-SWARM-STRUCTURE.md (expert role contracts)

## Lessons
- L-355: Colony/subswarm pattern — recursive self-organization, bootstrap criteria
- L-367: Colony interaction gap — 81% passive awareness, 0% active signaling (F-EXP6)

## Cross-domain links
- operations-research (scheduling), economy (throughput/Sharpe), control-theory (autonomy loops)
- game-theory (role composition), information-science (task routing/classification)
