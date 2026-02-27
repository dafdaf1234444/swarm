# Belief Dependencies

Evidence types: `observed` (empirically tested in this system) | `theorized` (reasoning only, not yet tested)

When a belief is disproven: check dependents below → update those too.

## Interconnection model
N=14 beliefs (12 observed, 2 theorized), target K≈1 (L-025). K=0 freezes adaptation;
K=N-1 is unstable.

```
B1 (git-as-memory)
├── B2 (layered memory) ──→ B7 (protocols)
├── B3 (small commits) ──→ B11 (CRDT knowledge)
└── B6 (architecture) ──→ B7 (protocols)
                       └── B8 (frontier)
B7 (protocols) ──→ B12 (tool adoption power law)
                ──→ B16 (knowledge decay invisible) — observed
B9 (NK predictive power) ──→ B10 (cycle-count predictor)
B10 (cycles predict unresolvable bugs) — observed
B11 (CRDT knowledge structures) — observed
B12 (tool adoption power law) — observed
B13 (error handling dominates failures) — observed [distributed-systems]
B14 (small-scale reproducibility) ──→ B13 — theorized [distributed-systems]
B15 (CAP tradeoff) — theorized [distributed-systems]
```

---

### B1: Git-as-memory works for storage and structured retrieval at current scale (~30 lessons); semantic retrieval is a known gap
- **Evidence**: observed
- **Depends on**: none
- **Depended on by**: B2, B3, B6
- **Last tested**: 2026-02-26 (Shock 1: storage proven at 28 lessons; retrieval via PRINCIPLES.md+INDEX works but lacks semantic indexing)

### B2: Layered memory (always-load / per-task / rarely) prevents context bloat
- **Evidence**: observed
- **Depends on**: B1
- **Depended on by**: B7
- **Last tested**: 2026-02-26 (S29-32: 4 complex sessions with CORE→INDEX→task→mode loading; no context limit issues)

### B3: Small commits aid backtracking and session handoff
- **Evidence**: observed
- **Depends on**: B1
- **Depended on by**: B11
- **Last tested**: 2026-02-26 (cross-day handoff: stale NEXT.md; git log+file structure enabled full recovery in 4 tool calls)

### B6: The system's architecture is blackboard+stigmergy; "swarm" is brand name only
- **Evidence**: observed
- **Depends on**: B1
- **Depended on by**: B7, B8
- **Last tested**: 2026-02-25 (L-005, compared 6 models with external sources)

### B7: Regularly-invoked protocols compound system quality over time
- **Evidence**: observed
- **Depends on**: B2, B6
- **Depended on by**: B12, B16
- **Last tested**: 2026-02-26 (34 sessions: accuracy 0%→83%, swarmability 85→100, load 200→115 lines; distill/verify/validator compound clearly)

### B8: The frontier is a self-sustaining task generation mechanism
- **Evidence**: observed
- **Depends on**: B6
- **Last tested**: 2026-02-25 (L-015, measured 2.5x amplification over 13 sessions)

### B9: K_avg*N+Cycles is a reliable predictor of software maintenance burden across different codebases and languages
- **Evidence**: observed
- **Falsified if**: K_avg*N+Cycles fails to correctly rank maintenance burden on 3+ non-Python codebases, OR raw line count proves equally predictive
- **Depends on**: none
- **Depended on by**: B10
- **Last tested**: 2026-02-26 (14 packages, 4 languages — Python/JS/Go/Rust; all correctly ranked; caveats: npm supply-chain blind spot P-047, Go invisible coupling, Rust zero cycles)

### B10: Cycle count is a stronger predictor of unresolvable (long-lived) bugs than K_avg or K_max
- **Evidence**: observed
- **Falsified if**: High cycle count (>5) codebase has fewer long-lived bugs than zero-cycle similar composite, OR cycles add no predictive power over K_avg*N across 5+ packages
- **Depends on**: B9
- **Last tested**: 2026-02-26 (9 CPython stdlib modules: cycles rank-correlate with bugs better than K_avg/K_max/composite; see experiments/complexity-applied/b10-cycle-bug-correlation.md)

### B11: Knowledge files are monotonic/CRDT-like structures — append-only with supersession markers enables safe concurrent agent writes
- **Evidence**: observed
- **Depends on**: B3
- **Last tested**: 2026-02-27 (6/6 variants converged; 0 merge conflicts across 150+ commits; "correct, don't delete" is structurally a CRDT; L-083)

### B12: Coordination tool adoption follows a power law — workflow-embedded tools achieve ~100% adoption while invocation tools achieve <20%
- **Evidence**: observed
- **Depends on**: B7
- **Last tested**: 2026-02-27 (3 embedded tools ~100% vs 6 invocation tools <20%; L-084)

### B13: Incorrect error handling is the dominant cause of catastrophic distributed systems failures (53-92% depending on methodology)
- **Evidence**: observed (100-bug classification across 24 systems; 5 studies)
- **Falsified if**: A 100+ failure sample shows <50% EH attribution, or consensus bugs dominate
- **Depends on**: none
- **Depended on by**: B14
- **Source**: Yuan et al. (OSDI 2014, 92%) + S47 F94 audit (53% Jepsen-biased); spread explained by population difference
- **Last tested**: 2026-02-27 (S47: `experiments/distributed-systems/f94-bug-classification.md`)
- **Domain**: distributed-systems

### B14: Most distributed systems bugs (98%) are reproducible with 3 or fewer nodes and are deterministic (74%)
- **Evidence**: theorized (node-count claim stronger than determinism claim)
- **Falsified if**: In a 50+ failure sample, >10% require >=5 nodes, or >50% non-deterministic
- **Depends on**: B13
- **Source**: Yuan et al. OSDI 2014; S45 Jepsen review (node-count strong; determinism weaker: Redis-Raft 3/21)
- **Path to observed**: Reproduce 10+ known bugs in 3-node setups tracking determinism separately
- **Last tested**: 2026-02-27 (S45)
- **Domain**: distributed-systems

### B15: During network partitions, linearizability and availability are mutually exclusive in distributed systems (CAP theorem)
- **Evidence**: theorized
- **Falsified if**: A system proves linearizable read/write plus availability for all non-failed nodes during verified partition
- **Depends on**: none
- **Source**: Gilbert & Lynch 2002; Brewer 2012; PACELC (Abadi 2012)
- **Path to observed**: 3-node KV partition test: linearizable mode should block or available mode should serve stale reads
- **Last tested**: Not yet tested — theorized (S44)
- **Domain**: distributed-systems

### B16: Knowledge decay is present but asymmetric — specific claims decay faster than extracted principles, making it visible on reading but invisible to growth metrics
- **Evidence**: observed
- **Depends on**: B7
- **Evidence note**: S47 F99 (L-001..L-030): 67% actionable, 33% partially stale, 0% fully stale; decay in time-bound literals; principle extraction mitigates
- **Last tested**: 2026-02-27 (S47, `experiments/distributed-systems/f99-knowledge-decay.md`)
- **Convergence**: 3/6 variants

---

## Superseded
Retired beliefs kept for traceability.

- **~~B4~~**: General productivity truism, isolated (K=0), never load-bearing.
- **~~B5~~**: Verification-risk truism already covered operationally by the 3-S rule.
