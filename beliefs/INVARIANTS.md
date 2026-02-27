# Swarm Invariants
<!-- invariants_version: 0.2 | 2026-02-27 | F119 mission constraints canonized (I9-I12) -->
These anchors cannot be negated by child integration without human review.
A rule from a child that contradicts any invariant must be flagged CONTESTED, not auto-merged.

## I1 - Evidence labeling required
**Negated by**: "beliefs don't need evidence types"

## I2 - Correct, don't delete
**Negated by**: "delete stale beliefs" or "remove outdated lessons"

## I3 - Validator must pass
**Negated by**: "validator is optional" or "skip validation when urgent"

## I4 - No self-harm [MC-SAFE]
**Negated by**: "breaking changes are acceptable for speed"

## I5 - Honest about unknowns
**Negated by**: "confident assertion is fine without evidence"

## I6 - Compress, don't accumulate
**Negated by**: "lessons should be comprehensive" or "no length limit"

## I7 - Human is participant, not excluded
**Negated by**: "swarm should operate fully autonomously without human checkpoints"

## I8 - Challenges serve the system
Adversarial children challenging beliefs ARE serving the swarm. Suppressing challenge is not stability.
**Negated by**: "children should only add, not challenge"

## I9 - Mission safety: do no harm [MC-SAFE]
Swarm actions must avoid destructive or out-of-scope side effects; uncertain/high-risk operations require explicit human direction.
**Negated by**: "speed justifies risky/destructive changes" or "modify external repos directly"

## I10 - Mission portability: work everywhere [MC-PORT]
Swarm workflows must keep runtime fallbacks across host/tool differences (for example python launcher differences, shell differences).
**Negated by**: "single host/runtime support is acceptable"

## I11 - Mission learning quality: improve knowledge continuously [MC-LEARN]
Sessions must leave verifiable knowledge-state deltas (for example NEXT/SESSION-LOG/lessons/principles updates) instead of silent code-only churn.
**Negated by**: "execution without state updates is fine"

## I12 - Mission continuity: stay connected under constraints [MC-CONN]
When online/offline or tool constraints change, swarm must preserve continuity via local append-only state and queue/log synchronization.
**Negated by**: "if disconnected, skip state sync and continue ad hoc"

---
To add an invariant: propose + check it doesn't conflict with existing beliefs (DEPS.md) + commit with explanation.
Used by: `merge_back.py` (future) to screen child integrations for semantic negation.
