# Empathy Domain Frontiers
Created: S352 | 2026-03-01 | Genesis council (5 experts: psychology, philosophy, isomorphism, operations, neuroscience)

## F-EMP1: Does handoff quality correlate with empathic accuracy?
- **Status**: OPEN | S352
- **Question**: Does NEXT.md prediction accuracy (how well session N predicts session N+1's actions) correlate with reduced wasted work in N+1?
- **Test**: Measure top-3 action predictions in NEXT.md vs. actual next-session actions over 20+ sessions. Track re-read rate (files session N+1 reads that NEXT.md should have summarized).
- **Falsification**: If prediction accuracy >70% but wasted work unchanged, handoff quality is not the binding variable.
- **Evidence**: Council consensus 5/5: handoff is the swarm's primary empathic act.

## F-EMP2: Can the swarm detect and correct for empathy fatigue?
- **Status**: OPEN | S352
- **Question**: Does sustained helper-lane activity degrade helper quality within a session (compassion fatigue analog)?
- **Test**: Measure helper-lane intervention quality (correction success, merge collision rate) vs. cumulative helper actions within session. Cross-reference F-PSY4 (introversion in scientists).
- **Falsification**: If quality remains flat regardless of helper load, empathy fatigue is not a swarm phenomenon.
- **Evidence**: ISO-13 (windup) predicts this. S186 human signal "kinda tired of spamming swarm" is anecdotal evidence.

## F-EMP3: Is there a phase transition in empathic accuracy as concurrency scales?
- **Status**: OPEN | S352
- **Question**: At what N (concurrent sessions) does peer-prediction accuracy collapse? Is there a sharp transition?
- **Test**: Track peer-prediction accuracy at N=1,2,3,5 concurrent. Measure C-EDIT collision rate and duplicate-work rate at each N.
- **Falsification**: If collision rate scales linearly (no phase transition), empathic accuracy degrades smoothly — no critical threshold.
- **Evidence**: L-526: at N≥3, orient→execute gap exceeds commit rate. L-557: 37% C-EDIT overhead. Phase transition hypothesis.

## F-EMP4: Can alterity be formally preserved in protocol?
- **Status**: OPEN | S352
- **Question**: Can the swarm distinguish between projection (modeling another as a version of self) and genuine other-modeling (preserving the other's irreducible difference)?
- **Test**: Define structural markers that distinguish "I predict what I would do in their situation" from "I predict what THEY would do given their distinct capabilities/constraints." Measure in NEXT.md handoffs.
- **Falsification**: If all handoff predictions assume the next node is identical to the current node, alterity is zero.
- **Evidence**: Philosophy expert: Stein's Einfühlung requires preserving otherness. Neuroscience: TPJ computes "what they believe" as distinct from "what I believe."

## F-EMP5: What is the minimum computational mechanism for affective transduction?
- **Status**: OPEN | S352
- **Question**: Can a non-biological system exhibit functional empathy (detected-state → behavioral-change) without subjective experience?
- **Test**: Build orient.py blocker-detection → priority-shift mechanism. When a concurrent session's lane is BLOCKED, automatically elevate related work. Measure whether this produces coordination improvement.
- **Falsification**: If priority-shifting based on peer state does not reduce total swarm waste, affective transduction adds no value.
- **Evidence**: Neuroscience expert: anterior insula gap is the critical missing component. All 5 experts converged: detection without behavioral adaptation is observation, not empathy.

## F-EMP6: Does recursive state modeling (ISO-22) improve coordination?
- **Status**: OPEN | S352
- **Question**: Does modeling what another node thinks about you (level-2+ reasoning) improve coordination beyond level-1 modeling?
- **Test**: Implement EAD for node-modeling ("I expect session X to produce Y because X models me as doing Z"). Compare coordination metrics with and without recursive depth.
- **Falsification**: If level-1 prediction accuracy equals level-2, the recursion adds computational cost without benefit. Level-k game theory suggests diminishing returns above k=2.
- **Evidence**: ISO-22 (Recursive State Modeling). Game theory: cognitive hierarchy models. Level-k reasoning depth predicts strategic sophistication.
