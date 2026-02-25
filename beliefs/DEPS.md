# Belief Dependencies

Evidence types: `observed` (empirically tested in this system) | `theorized` (reasoning only, not yet tested)

When a belief is disproven: check dependents below → update those too.

## Interconnection model
N=6 beliefs, target K≈1 (edge of chaos for small N per Kauffman's NK model). See L-025.
K=0 is frozen (no cascades, no adaptation). K=N-1 is chaotic (everything affects everything).

```
B1 (git-as-memory)
├── B2 (layered memory) ──→ B7 (protocols)
├── B3 (small commits)
└── B6 (architecture) ──→ B7 (protocols)
                       └── B8 (frontier)
```

---

### B1: Git-as-memory works for storage and structured retrieval at current scale (~30 lessons); semantic retrieval is a known gap
- **Evidence**: observed
- **Falsified if**: A session following the loading protocol misses information that PRINCIPLES.md or INDEX.md should have surfaced, OR the system reaches 50 lessons and compaction+principles still provide adequate retrieval
- **Depends on**: none
- **Depended on by**: B2, B3, B6
- **Last tested**: 2026-02-26 (Shock 1: refined scope to distinguish storage from retrieval. Storage proven at 28 lessons. Retrieval works via PRINCIPLES.md + INDEX theme table but lacks semantic indexing. See experiments/adaptability/shocks/shock1.md)

### B2: Layered memory (always-load / per-task / rarely) prevents context bloat
- **Evidence**: observed
- **Falsified if**: A session that follows the layered loading protocol still exceeds its context window on a routine task, OR a session that loads everything performs equally well
- **Depends on**: B1
- **Depended on by**: B7
- **Last tested**: 2026-02-26 (Session 29-32: completed 4 complex sessions following layered protocol without context issues. Loaded CORE→INDEX→task→mode per session; never hit context limits despite heavy tool usage)

### B3: Small commits aid backtracking and session handoff
- **Evidence**: observed
- **Falsified if**: A session needs to revert or understand history and finds that small commits make this harder (too much noise) rather than easier, OR large monolithic commits prove equally navigable
- **Depends on**: B1
- **Last tested**: 2026-02-26 (cross-day handoff: NEXT.md was stale/wrong but git log + file structure enabled full recovery within 4 tool calls)

### B6: The system's architecture is blackboard+stigmergy; "swarm" is brand name only
- **Evidence**: observed
- **Falsified if**: A rigorous analysis shows the system's actual coordination pattern matches a different model (pure swarm, hierarchical, federation) better than blackboard+stigmergy
- **Depends on**: B1
- **Depended on by**: B7, B8
- **Last tested**: 2026-02-25 (L-005, compared 6 models with external sources)

### B7: Regularly-invoked protocols compound system quality over time
- **Evidence**: observed
- **Falsified if**: Health metrics show no improvement or degradation across 10+ sessions despite protocol adherence, OR removing a protocol produces no measurable quality difference
- **Depends on**: B2, B6
- **Last tested**: 2026-02-26 (34 sessions: belief accuracy 0%→83%, swarmability 85→100, mandatory load 200→115 lines. Distill/verify/validator clearly compound; conflicts/health invoked rarely — no evidence for those)

### B8: The frontier is a self-sustaining task generation mechanism
- **Evidence**: observed
- **Falsified if**: The system runs 10 consecutive sessions where no new frontier questions are generated from completed work, indicating the generative loop has stalled
- **Depends on**: B6
- **Last tested**: 2026-02-25 (L-015, measured 2.5x amplification over 13 sessions)

---

## Superseded
Retired beliefs. Kept for error trail per CORE.md principle 8.

- **~~B4~~**: "One focused session is more productive than many unfocused ones" — Isolated (K=0), never tested, general productivity truism. No structural decision depended on it. L-003, L-007, L-021 referenced it but their insights stand independently.
- **~~B5~~**: "LLM training biases are a real risk to knowledge quality" — Isolated (K=0), never tested, truistic. The 3-S Rule (L-006) already operationalizes verification. The belief added no unique structural information.
