# Domain Index: Expert Swarm
Updated: 2026-02-28 | Sessions: 303

## What this domain knows
- **Active frontiers**: 5 in `domains/expert-swarm/tasks/FRONTIER.md` (F-EXP1, F-EXP2, F-EXP3, F-EXP4, F-EXP5)
- Expert swarm = the meta-layer where swarm capacity is created, dispatched, and measured.
- Structural gaps: (1) 64+ unrun domain experiments (2% throughput), (2) companion bundling
  under-utilized, (3) colony lifecycle just established — fitness criteria untested.
- 3-tool functional core: dispatch_optimizer.py (yield rank) + task_recognizer.py (routing) + swarm_colony.py

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
