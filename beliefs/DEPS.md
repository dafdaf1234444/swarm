# Belief Dependencies

Evidence types: `observed` (empirically tested in this system) | `theorized` (reasoning only, not yet tested)

When a belief is disproven: check dependents below → update those too.

## Interconnection model
N=14 beliefs (12 observed, 2 theorized), target K≈1. See L-025.
K=0 is frozen (no cascades, no adaptation). K=N-1 is chaotic (everything affects everything).

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
- **Depended on by**: B11
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
- **Depended on by**: B12, B16
- **Last tested**: 2026-02-26 (34 sessions: belief accuracy 0%→83%, swarmability 85→100, mandatory load 200→115 lines. Distill/verify/validator clearly compound; conflicts/health invoked rarely — no evidence for those)

### B8: The frontier is a self-sustaining task generation mechanism
- **Evidence**: observed
- **Falsified if**: The system runs 10 consecutive sessions where no new frontier questions are generated from completed work, indicating the generative loop has stalled
- **Depends on**: B6
- **Last tested**: 2026-02-25 (L-015, measured 2.5x amplification over 13 sessions)

### B9: K_avg*N+Cycles is a reliable predictor of software maintenance burden across different codebases and languages
- **Evidence**: observed
- **Falsified if**: K_avg*N+Cycles fails to correctly rank maintenance burden on 3+ non-Python codebases (e.g., npm packages, Go modules, Rust crates), OR a simpler metric (like raw line count) proves equally predictive
- **Depends on**: none
- **Depended on by**: B10
- **Last tested**: 2026-02-26 (Validated across 14 packages in 4 languages — Python, JavaScript, Go, Rust. Express 6.0/15.0, Go net/http 89.0, Rust serde 30.0 — all correctly ranked. 3 non-Python codebases exceed falsification threshold. Caveats: npm supply-chain blind spot (P-047), Go invisible coupling, Rust guaranteed zero cycles)

### B10: Cycle count is a stronger predictor of unresolvable (long-lived) bugs than K_avg or K_max
- **Evidence**: observed
- **Falsified if**: A codebase with high cycle count (>5) has fewer long-lived bugs than a codebase with zero cycles but similar composite score, OR cycle count adds no predictive power beyond K_avg*N alone across 5+ packages
- **Depends on**: B9
- **Last tested**: 2026-02-26 (9 CPython stdlib modules: multiprocessing 19 cycles→176 open/99 long-lived bugs, email 9 cycles→156/73, asyncio 1 cycle→52/8 despite highest composite. Cycles rank-correlate with open bugs better than K_avg, K_max, or composite. See experiments/complexity-applied/b10-cycle-bug-correlation.md)

### B11: Knowledge files are monotonic/CRDT-like structures — append-only with supersession markers enables safe concurrent agent writes
- **Evidence**: observed
- **Falsified if**: Two concurrent agents writing to the same knowledge file produce an irreconcilable conflict that append-only + supersession cannot resolve, OR a system using destructive edits on knowledge files shows better consistency than append-only
- **Depends on**: B3
- **Last tested**: 2026-02-27 (Cross-variant harvest R3: 6/6 top variants independently converged on this. Parent has 0 merge conflicts across 150+ commits. minimal variant: 0 conflicts in 4 sessions. The "correct, don't delete" practice is structurally a CRDT — concurrent writes are safe on append-only files. L-083)

### B12: Coordination tool adoption follows a power law — workflow-embedded tools achieve ~100% adoption while invocation tools achieve <20%
- **Evidence**: observed
- **Falsified if**: An invocation-only tool (not mandated in CLAUDE.md session protocol) achieves >50% session adoption rate over 10+ sessions, OR embedding a low-adoption tool in CLAUDE.md does not significantly increase its adoption
- **Depends on**: B7
- **Last tested**: 2026-02-27 (test-first child B20-B22: 3 tools near 100% (NEXT.md, FRONTIER.md, validate_beliefs.py) vs 6 tools at <20% (bulletin.py, frontier_claim.py, colony.py, etc. ~1524 LOC total). L-084)

### B13: Incorrect error handling is the dominant cause of catastrophic distributed systems failures (53-92% depending on methodology)
- **Evidence**: observed (100-bug classification across 24 systems, 5 independent studies)
- **Falsified if**: A comparable study of 100+ failures in distributed systems finds that fewer than 50% trace to error handling, OR finds that consensus algorithm bugs dominate catastrophic failures
- **Depends on**: none
- **Depended on by**: B14
- **Source**: Yuan et al. OSDI 2014 — 198 failures across Cassandra, HBase, HDFS, MapReduce, Redis: 92% EH. Three anti-patterns: swallowed errors, TODO handlers, overly-broad catch-then-abort
- **Evidence (S47)**: 100 bugs classified across 24 systems (Jepsen analyses + GitHub + postmortems): EH=53%, AP=26%, CFG=10%, CC=5%. Falsification condition NOT met even in Jepsen-biased sample (which over-selects protocol bugs). EH+CFG (config failures often EH-adjacent) = 63%. See experiments/distributed-systems/f94-bug-classification.md
- **Reconciliation**: 92% (Yuan) vs 53% (Jepsen) gap explained by population difference: Yuan studied user-reported catastrophic failures; Jepsen proactively tests consensus protocols (over-samples AP category). Both studies confirm EH is the dominant category.
- **Corroboration**: 5 independent studies agree — Gunawi SoCC 2014 (18% of all bugs, #2 behind logic), Liu & Lu HotOS 2019 (31% of Azure incidents), Chang NSDI 2020 (top-3 partial failure causes all EH-related), Ganesan FAST 2017 (crash-instead-of-recover dominates), Yuan OSDI 2014 (92%).
- **Last tested**: 2026-02-27 (S47: F94 — 100 bugs, 24 systems classified)
- **Domain**: distributed-systems

### B14: Most distributed systems bugs (98%) are reproducible with 3 or fewer nodes and are deterministic (74%)
- **Evidence**: theorized (node-count well-supported; determinism weaker)
- **Falsified if**: A study of 50+ production failures finds more than 10% require ≥5 nodes to reproduce, OR finds more than 50% are non-deterministic
- **Depends on**: B13 (same study population)
- **Source**: Yuan et al. OSDI 2014. Also: 84% had all triggering events logged, 58% preventable by simple pre-release testing
- **Corroboration (S45)**: Jepsen analysis shows etcd lock bug needs 1 node + expired lease, CockroachDB timestamp collision needs 2 nodes, Redis-Raft data loss needs 2 nodes. All conceptually ≤3 nodes. BUT: Redis-Raft Jepsen found only 3/21 (14%) deterministic, challenging 74% claim (Jepsen targets non-deterministic edge cases, biased sample).
- **Path to observed**: Reproduce 10+ known Jepsen bugs in 3-node setups. Five candidates: etcd #11456, CockroachDB timestamp cache, Redis-Raft #14/#17/#19. Track determinism separately.
- **Last tested**: 2026-02-27 (S45: theoretical node-requirement analysis of Jepsen bugs)
- **Domain**: distributed-systems

### B15: During network partitions, linearizability and availability are mutually exclusive in distributed systems (CAP theorem)
- **Evidence**: theorized
- **Falsified if**: A distributed system demonstrates linearizable reads/writes AND availability (all non-failed nodes respond) during a verified network partition under Jepsen-like testing
- **Depends on**: none
- **Source**: Gilbert & Lynch 2002 (formal proof). Brewer 2012 retrospective. Note: weaker consistency models (causal, eventual) escape this constraint. PACELC (Abadi 2012) extends to latency-consistency tradeoff during normal operation
- **Path to observed**: Set up a 3-node distributed KV store, induce partition via iptables, verify that linearizable mode becomes unavailable OR available mode returns stale reads
- **Last tested**: Not yet tested — theorized from external research (S44)
- **Domain**: distributed-systems

### B16: Knowledge decay is present but asymmetric — specific claims decay faster than extracted principles, making it visible on reading but invisible to growth metrics
- **Evidence**: observed
- **Falsified if**: A systematic review of lessons older than 10 sessions finds >80% still actionable and fully current (not just rule-level actionable), OR growth metrics (lesson count, belief count) correlate with a measured quality metric (e.g., session productivity) at r>0.7
- **Depends on**: B7 (protocols compound, but decay is the counterforce)
- **Evidence (S47)**: F99 — systematic review of L-001 to L-030 (30 lessons, 30+ sessions old). Result: 67% ACTIONABLE, 33% PARTIALLY_STALE, 0% STALE. Falsification threshold (>80% fully current) NOT met — decay exists. BUT "invisible" overstated: staleness is visible when reading (outdated session counts, version labels, measurements). Mitigation works: PRINCIPLES.md strips decaying context → 100% actionable at rule level. See experiments/distributed-systems/f99-knowledge-decay.md
- **Refined understanding**: Decay patterns: (1) session-count references age immediately, (2) version labels stale when thing evolves, (3) specific measurements are point-in-time. Protocols and architecture validations are least vulnerable (no expiry).
- **Last tested**: 2026-02-27 (S47: F99 — 30-lesson systematic review)
- **Convergence**: 3/6 variants (test-first, minimal-nofalsif, no-falsification)

---

## Superseded
Retired beliefs. Kept for error trail per CORE.md principle 8.

- **~~B4~~**: "One focused session is more productive than many unfocused ones" — Isolated (K=0), never tested, general productivity truism. No structural decision depended on it. L-003, L-007, L-021 referenced it but their insights stand independently.
- **~~B5~~**: "LLM training biases are a real risk to knowledge quality" — Isolated (K=0), never tested, truistic. The 3-S Rule (L-006) already operationalizes verification. The belief added no unique structural information.
