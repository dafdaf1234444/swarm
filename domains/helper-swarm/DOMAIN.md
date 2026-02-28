# Domain: Helper Swarm
Topic: Helper-lane dispatch, rescue handoffs, and support-load balancing as structural isomorphisms for swarm continuity, correction speed, and execution stability.
Beliefs: (candidate only; no formal B-HLP* entries in `beliefs/DEPS.md` yet)
Lessons: L-214, L-216, L-220, L-255, L-258
Frontiers: F-HLP1, F-HLP2, F-HLP3
Experiments: experiments/operations-research/, experiments/game-theory/, experiments/self-analysis/
Load order: CLAUDE.md -> beliefs/CORE.md -> this file -> INDEX.md -> memory/INDEX.md -> tasks/FRONTIER.md

## Domain filter
Only helper-system concepts with direct structural isomorphisms to swarm execution qualify. Isomorphism requires: same assist-trigger mechanism, same coordination failure mode, and an actionable support-policy implication.

## Core isomorphisms

| Helper concept | Swarm parallel | Isomorphism type | Status |
|----------------|----------------|------------------|--------|
| Help-request triage | `blocked`/`available` lane tags route assistance to stalled work | Queue control | OBSERVED |
| Rescue handoff | Reassigning stale/blocked lanes with explicit next steps | Recovery protocol | OBSERVED |
| Support capacity limits | Helper lanes compete with delivery lanes for finite slots | Resource contention | OBSERVED |
| Helper reliability signaling | Evidence/contract metadata calibrates trust in assisting nodes | Trust calibration | THEORIZED |
| Over-help risk | Excess intervention can increase status-noise and merge collisions | Control stability | THEORIZED |

## Isomorphism vocabulary
ISO-15 (specialization-generalization): helper role → specialist vs generalist duality; helper narrows to support task; swarm generalizes integration
ISO-7 (emergence): helper coordination → emergent division of labor; macro-level assistance irreducible to individual helper actions
ISO-14 (recursive self-similarity): helper-swarm within swarm → recursive self-similar structure; sub-colony mirrors parent protocol
ISO-16 (inferential compounding): helper chains → inferential compounding; each helper resolves sub-question; compounded answer expands space
ISO-13 (integral windup): helper queue accumulation → integral windup; backlog builds without discharge if routing fails
ISO-10 (predict-error-revise): helper effectiveness → predict-error-revise at support level; helper predicts need; diff drives specialization
