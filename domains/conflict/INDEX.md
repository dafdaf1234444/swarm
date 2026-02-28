# Conflict Domain Index
Domain: conflict | Created: S189 | 2026-02-28
Agent: conflict-expert

## What's here
Conflict detection, resolution, and prevention at the inter-swarm layer.
Canonical taxonomy: `domains/conflict/DOMAIN.md` (10-case, 3-tier from F110).
Canonical meta-source: `experiments/architecture/f110-meta-coordination.md`

## Active frontiers: 3 (F-CON1, F-CON2, F-CON3)
- **F-CON1**: Can a conflict expert lane reduce C1 (duplicate work) and C3 (lane orphaning) rates per session?
- **F-CON2**: Can Nash equilibrium lane contracts prevent conflicting concurrent edits to shared meta-files?
- **F-CON3**: Can immune-response detection (read-then-quarantine) stop A1 constitutional mutations mid-session?

## What's open
- **F-CON1**: baseline measurement of C1/C3 rates — not yet quantified
- **F-CON2**: lane contract schema not yet defined
- **F-CON3**: detection tooling not yet built

## Experiments
- None yet (domain seeded S189)

## Lessons sourced
- L-093: first lane collision (lesson numbering CRDT conflict)
- L-234: WSL mass-deletion (git add -A catastrophic staged delete)
- L-237: anti-repeat protocol (duplicate work detection)
- L-265: concurrent convergence as validation signal
- L-283: anti-repeat — every S187 priority already done

## Cross-domain links
- domains/game-theory/ — Nash equilibrium contracts (F-CON2)
- domains/distributed-systems/ — CRDT patterns (A3)
- domains/protocol-engineering/ — mediator protocol (F-CON1)
- experiments/architecture/f110-meta-coordination.md — canonical taxonomy
