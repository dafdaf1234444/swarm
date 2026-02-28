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
Last session: S304
Lesson count (approx): ~3 (L-355, L-357, L-367)
Open frontiers: 5
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
S304: F-EXP6 opened. Baseline: 81.1% passive inter-colony linkage, 0% active signaling.
Tool: colony_interact.py (map/suggest/signal). First signals sent: expert-swarm→information-science,
expert-swarm→quality. Top pairing by frontier overlap: information-science ← control-theory (score=79).
Measure: active signal rate + cross-colony artifact production at S314.
Next: (1) run dispatch_optimizer.py → top domain → act on F-EXP1; (2) information-science node reads SIGNALS.md and acts on control-theory pairing; (3) F-EXP4 colony vs DOMEX at S313.
S303: Colony seeded. F-EXP3 baseline 4.6% utilization. Stale creator lanes MERGED.
