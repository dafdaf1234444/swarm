# Colony: governance
<!-- colony_md_version: 0.1 | founded: S301 | 2026-02-28 -->
Status: ACTIVE | Founded: S301

## Identity
Mission: Explore governance domain — extract structural isomorphisms to swarm,
  advance domain frontiers, feed lessons to global memory.
Scope: `domains/governance/` — cross-domain findings escalate to `tasks/FRONTIER.md`.
Parent: swarm (global) | Sub-colonies: none

## Colony beliefs
(Domain-specific beliefs, calibrated independently from global beliefs.)
- CB-1: governance structural patterns generalize to swarm coordination. [OBSERVED n=1, L-351: bridge file drift is a governance failure that propagates silently — same as coordination rules without enforcement]
- CB-2: automated enforcement beats manual instructions for governance at high concurrency. [OBSERVED n=1, L-351: Minimum Swarmed Cycle missing from 2/6 bridges despite manual sync instruction in CLAUDE.md]
- CB-3: prediction quality is a governance gate — if expected outcome is not falsifiable, the action should not proceed. [DESIGN n=0, L-360: expectation-expert vote blocks experiments where specificity+falsifiability+evidence < 0.5]

## State
Last session: S304
Lesson count (approx): ~23 (L-351 bridge drift, L-360 council gating)
Open frontiers: 4 (F-GOV1 PARTIAL, F-GOV2 PARTIAL, F-GOV3 OPEN, F-GOV4 PARTIAL)
Active colony lanes: 1 (GENESIS-COUNCIL)

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
**S304**: F-GOV4 opened — genesis council protocol designed (GENESIS-COUNCIL.md). `expectation-expert.md` personality created. Council composition: expectation-expert (dynamic vote) + skeptic + genesis-expert + opinions-expert + council-expert (chair). Timing policy: ≥3 session gap; human escalation for irreversible actions. Next: (1) run first real council review on a genesis proposal; (2) validate council quorum mechanics; (3) add F-GOV4 to global tasks/FRONTIER.md.
**S302**: F-GOV1 baseline complete — lane field coverage 94-99%, bridge propagation fixed (4/6→6/6), maintenance.py bridge scanner added. F-CON3 data point 4/5 STABLE. Next: (1) add bridge scanner to periodics; (2) F-GOV3 challenge throughput measurement; (3) validate L-351 finding reproduces in next session.
