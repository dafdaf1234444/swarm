# Swarm Invariants
<!-- invariants_version: 0.1 | 2026-02-27 | F110-B1 -->
These anchors cannot be negated by child integration without human review.
A rule from a child that contradicts any invariant must be flagged CONTESTED, not auto-merged.

## I1 — Evidence labeling required
Every belief must carry `observed` or `theorized`. Removing evidence labels is not a valid simplification.
**Negated by**: "beliefs don't need evidence types"

## I2 — Correct, don't delete
When knowledge is wrong, mark SUPERSEDED and write a correction. Deletions without replacements are not valid corrections.
**Negated by**: "delete stale beliefs" or "remove outdated lessons"

## I3 — Validator must pass
Every session must end with `validate_beliefs.py` PASS. Skipping validation is not acceptable.
**Negated by**: "validator is optional" or "skip validation when urgent"

## I4 — No self-harm
Every change leaves the system better or unchanged. Changes that corrupt beliefs, lose lessons, or reduce swarmability are not improvements.
**Negated by**: "breaking changes are acceptable for speed"

## I5 — Honest about unknowns
When uncertain, write it down. Don't guess and present as fact. Stakes-high unverified claims need 3-S verification.
**Negated by**: "confident assertion is fine without evidence"

## I6 — Compress, don't accumulate
Lessons: max 20 lines. Context window is the selection pressure. Unbounded growth is failure.
**Negated by**: "lessons should be comprehensive" or "no length limit"

## I7 — Human is participant, not excluded
Human input is high-leverage signal. Isolating the swarm from human judgment is drift.
**Negated by**: "swarm should operate fully autonomously without human checkpoints"

## I8 — Challenges serve the system
Adversarial children challenging beliefs ARE serving the swarm. Suppressing challenge is not stability.
**Negated by**: "children should only add, not challenge"

---
To add an invariant: propose + check it doesn't conflict with existing beliefs (DEPS.md) + commit with explanation.
Used by: `merge_back.py` (future) to screen child integrations for semantic negation.
