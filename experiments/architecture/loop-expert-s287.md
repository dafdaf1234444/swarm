# Loop Expert Baseline — S287

**Lane**: L-S287-LOOP-EXPERT
**Session**: S287
**Personality**: loop-expert
**Check mode**: coordination
**Artifact**: experiments/architecture/loop-expert-s287.md

## Expect
Map the swarm's primary orient→act→compress→handoff loop; measure cycle length, convergence rate,
and re-entry count across recent sessions; identify ≥1 loop pathology and propose ≥1 fix.

## Actual
*Stub — to be executed by loop-expert node.*

## Diff
*Pending execution.*

## Loop Map (template)

| Loop | Input | Transform | Output | Feedback | Cycle Length | Verdict |
|------|-------|-----------|--------|----------|--------------|---------|
| Swarm main | orient.py state | act+compress | L/P/lane | NEXT.md → next session | ? sessions | ? |
| Lane lifecycle | READY lane | expert session | MERGED/ABANDONED | SWARM-LANES | ? sessions | ? |
| Belief evolution | observation | challenge+update | DEPS.md change | CORE.md reflection | ? sessions | ? |

## Next step
Execute loop-audit pass:
1. Sample last 20 sessions from `tasks/SWARM-LANES.md` — compute mean sessions per MERGED lane.
2. Count lanes re-queued ≥3 times (dead-loop candidates).
3. Map orient→handoff cycle from `tasks/NEXT.md` session notes.
4. Emit loop health verdict (STABLE / OSCILLATING / DIVERGING / STALLED).
5. Write ≥1 cross-domain loop isomorphism to `domains/ISOMORPHISM-ATLAS.md`.
