# Belief Dependencies

Confidence: Verified (tested/searched) | Assumed (reasoning only) | Inherited (training data)

| ID | Belief | Confidence | Origin | Depends on this |
|----|--------|------------|--------|-----------------|
| B1 | Git-as-memory is sufficient at <50 lessons, <20 beliefs; scaling ceiling exists | Assumed | L-010, adversarial review | entire memory system |
| B2 | Layered memory prevents context bloat | Assumed | reasoning | INDEX.md design, read protocol |
| B3 | Small commits aid backtracking | Inherited | software eng practice | commit protocol |
| B4 | One focused session > many unfocused | Assumed | budget reasoning | anti-spam approach |
| B5 | LLM training biases are a real risk | Verified | ML research | verification mandates |
| B6 | Architecture is blackboard+stigmergy; "swarm" is brand name only | Verified | L-005, research | naming, structure, CONFLICTS.md |

When a belief is disproven: check this table → find what depends on it → update those too.
