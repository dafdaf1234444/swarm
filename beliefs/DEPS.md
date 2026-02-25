# Belief Dependencies

Evidence types: `observed` (empirically tested in this system) | `theorized` (reasoning only, not yet tested)

When a belief is disproven: check dependents below → update those too.

---

### B1: Git-as-memory is sufficient at <50 lessons, <20 beliefs; a scaling ceiling exists
- **Evidence**: observed
- **Falsified if**: A session fails to find needed information via grep/file-read within a reasonable time, OR the system reaches 50 lessons and retrieval still works fine (ceiling claim is wrong)
- **Depends on**: none
- **Last tested**: 2026-02-25 (L-010, adversarial review at 10 lessons)

### B2: Layered memory (always-load / per-task / rarely) prevents context bloat
- **Evidence**: theorized
- **Falsified if**: A session that follows the layered loading protocol still exceeds its context window on a routine task, OR a session that loads everything performs equally well
- **Depends on**: B1
- **Last tested**: never

### B3: Small commits aid backtracking and session handoff
- **Evidence**: theorized
- **Falsified if**: A session needs to revert or understand history and finds that small commits make this harder (too much noise) rather than easier, OR large monolithic commits prove equally navigable
- **Depends on**: none
- **Last tested**: 2026-02-25 (intra-day only — traced commits within a single marathon session. Cross-day handoff with zero shared context never tested. Original observed claim was premature.)

### B4: One focused session is more productive than many unfocused ones
- **Evidence**: theorized
- **Falsified if**: A measurable comparison shows that several short unfocused sessions produce equal or better output (lessons, artifacts, resolved frontier questions) per total token budget
- **Depends on**: none
- **Last tested**: never

### B5: LLM training biases are a real risk to knowledge quality
- **Evidence**: theorized
- **Falsified if**: An audit of all lessons finds zero instances where training-data bias led to an incorrect or misleading claim in the swarm's knowledge base
- **Depends on**: none
- **Last tested**: never

### B6: The system's architecture is blackboard+stigmergy; "swarm" is brand name only
- **Evidence**: observed
- **Falsified if**: A rigorous analysis shows the system's actual coordination pattern matches a different model (pure swarm, hierarchical, federation) better than blackboard+stigmergy
- **Depends on**: none
- **Last tested**: 2026-02-25 (L-005, compared 6 models with external sources)

### B7: Protocols (distill, health, verify, correct) compound system quality over time
- **Evidence**: theorized
- **Falsified if**: Health metrics (HEALTH.md) show no improvement or degradation across 10+ sessions despite protocol adherence, OR removing a protocol produces no measurable quality difference
- **Depends on**: B1, B2
- **Last tested**: never

### B8: The frontier is a self-sustaining task generation mechanism
- **Evidence**: observed
- **Falsified if**: The system runs 10 consecutive sessions where no new frontier questions are generated from completed work, indicating the generative loop has stalled
- **Depends on**: none
- **Last tested**: 2026-02-25 (L-015, measured 2.5x amplification over 13 sessions)
