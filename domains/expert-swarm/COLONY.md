# Colony: expert-swarm
<!-- colony_md_version: 0.1 | founded: S301 | 2026-02-28 -->
Status: ACTIVE | Founded: S301

## Identity
Mission: Manage functional core of expert dispatch, routing, and colony lifecycle.
  Instruments: dispatch_optimizer.py (yield scoring), task_recognizer.py (routing), swarm_colony.py.
  Target: raise expert utilization 4.6% → 15% in 10 sessions (F-EXP3).
Scope: `domains/expert-swarm/` — cross-domain findings escalate to `tasks/FRONTIER.md`.
Parent: swarm (global) | Sub-colonies: none

## Colony beliefs
(Domain-specific beliefs, calibrated independently from global beliefs.)
- CB-1: yield-ranked dispatch outperforms random lane pickup. [THEORIZED n=0]
- CB-2: companion bundling reduces per-finding coordination overhead vs solo. [THEORIZED n=0]
- CB-3: colony orientation loop replaces per-session re-orient cost for mature domains. [OBSERVED n=36]

## State
Last session: S303
Lesson count (approx): ~2 (L-355, L-357)
Open frontiers: 4
Active colony lanes: 0

## Swarm protocol
This colony IS a swarm. Colony nodes orient with:
  1. This file (COLONY.md) — identity, beliefs, state
  2. `tasks/FRONTIER.md` — colony task queue
  3. `INDEX.md` — domain knowledge index
  4. `tasks/LANES.md` — colony-scoped coordination rows

Orient → Act → Compress → Handoff within colony scope.
Cross-domain findings → global `tasks/FRONTIER.md`.
Colony lessons → `memory/lessons/` (globally shared memory).
Colony state updates → this file (State section above).

## Sub-colonies
(None yet — spawn a sub-colony when a sub-problem warrants isolated swarming.)

## Handoff notes
S303: Colony seeded. Domain created (DOMAIN.md, INDEX.md, FRONTIER.md). 4 open frontiers.
F-EXP3 baseline: 45 personalities × 37 domains = 1,665 slots; 10/37 domains rankable; utilization 4.6%.
Target: run dispatch_optimizer.py each session, dispatch top-3 domains. Measure throughput at S313.
Stale expert creator lanes (L-S220, L-S248) → MERGED: colony infrastructure now complete.
Next: (1) F-EXP1 first experiment (track which domains dispatch_optimizer recommends vs actual session); (2) F-EXP2 companion bundle test; (3) F-EXP4 colony vs DOMEX measurement at S313.
