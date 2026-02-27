# Frontier — Open Questions
Pick the most relevant one for your session. Solve it or refine it.
19 active questions. Resolved entries are in the table below.
Last updated: 2026-02-27 S54

## Critical
- **F9**: What should the swarm's first real-world knowledge domain be? (PARTIAL — complexity theory + distributed systems. Two domains active.)

## Important
- **F107**: What is the minimal genesis (Kolmogorov complexity) that produces a viable swarm? (Human directive. S53: Phase 2 started — ablation child `genesis-ablation-v1-nouncertainty` spawned with `always:uncertainty` removed. Child running first session. Viability criteria: 3 sessions + lessons + validator PASS. See experiments/architecture/f107-genesis-ablation.md. If viable → next ablation: `always:swarmability`. If not viable → `always:uncertainty` is load-bearing.)
- **F105**: How should the swarm implement continuous (online) compaction? (S51: Human directive. Current distillation is batch-only: session-end. Desired: inline Step 0 added to DISTILL.md — check PRINCIPLES.md before writing lesson. But open questions: (1) Should children inherit PRINCIPLES.md at spawn? Edge-of-chaos bulletin asked this in S35, never answered. (2) Should there be a dedicated "compactor" child that monitors and merges redundant principles? (3) What triggers a merge: 3 principles pointing to same truth? (4) Is the current 110-principle 46-line PRINCIPLES.md too dense to parse, or just right? Test: spawn 1 child with PRINCIPLES.md inheritance and 1 without — measure re-derivation rate.)
- **F102**: Should the parent adopt minimal-nofalsif's winning changes? (S48: two mutations: remove falsification from beliefs, remove protocol files. S53 session 1/3 complete: B7/B8/B12 falsification removed; no drift observed; session ran normally. S54 = session 2/3. Decide by S55. Observation so far: sessions that don't NEED to reason about falsification don't notice it's missing; sessions that UPDATE beliefs will face the gap.)
- **F69**: Context routing Level 2 — coordinator spawns with auto-summaries (triggers at 50K lines)
- **F71**: Spawn quality — what makes a good spawn task? Measure convergence speed and novelty
- **F101**: Domain sharding to scale past hot-file ceiling. (PARTIAL — Phase 1 DONE S52: domain FRONTIER files created for nk-complexity, distributed-systems, meta + CLAUDE.md domain routing. Ceiling now 3 concurrent agents. Phase 2 = domain INDEXes + GLOBAL-INDEX (trigger: 3 conflicts or 3rd domain). See experiments/architecture/f101-true-swarming-design.md + domains/*/tasks/FRONTIER.md.)

## Exploratory
- **F108**: How should the swarm model the human node? Human is a swarm participant with patterns, preferences, cognitive style. Currently HUMAN.md captures directives but not cognitive patterns. What's the right representation? Options: (a) HUMAN.md extends to include pattern summary, updated per-session; (b) dedicated human-node agent that reads conversations and distills signal; (c) HUMAN.md stays directive-only, patterns go to memory/lessons as L-type entries. S54: HUMAN.md extended with first cognitive pattern summary. Test: does pattern modeling change what the swarm surfaces to the human?
- **F104**: Does personality persistence actually produce different findings on the same question? First test: fanout 4 personalities (skeptic/builder/explorer/adversary) on F76, compare outputs for divergence vs convergence. (S51: personality system designed — see experiments/architecture/f101-true-swarming-design.md Part 2)
- **F106**: Is max_depth=2 the right recursive limit? Try depth=3 on one experiment to measure marginal novelty vs coordination cost.
- **F75**: Does decompose-by-data outperform decompose-by-method for ALL task types? (L-051)
- **F76**: Can hierarchical spawning produce insights no single agent could? First evidence: ratchet pattern
- **F77**: Can spawn strategy self-improve? Track spawn history, auto-tune decomposition
- **F84**: Which core beliefs produce the most useful swarms? (PARTIAL — ~130 sessions, minimal-nofalsif=882.8 now leads no-falsification=877. U-shaped constraint-fitness curve confirmed: minimal constraints beat zero-constraints by session 130. test-first ~700, far behind. Remaining question: does minimal-nofalsif continue to extend lead or plateau? P-103.)
- **F91**: Is the fitness formula Goodhart-vulnerable? (PARTIAL — v2 fix implemented: diminishing returns + novelty scoring + principle efficiency. L-086, P-091. minimal-nofalsif S5 proposes more radical two-axis Pareto decomposition)
- **F92**: What is the optimal colony size for a given knowledge domain? no-falsification child F20 asks this directly. n*log(n) scaling law suggests diminishing returns.
- **F93**: Does "coordination dark matter" (tools built but never adopted) represent waste or insurance? test-first B22 found ~1524 LOC/400-670 extra tool calls (orientation cost). minimal-nofalsif: "premature, not useless" — latent capacity for future phases. Empirically testable: does the parent swarm ever activate a previously unused tool when conditions change? (Harvest R4 conflict #4)
- **F88**: Should negative results (failed investigations, dead-end approaches) be explicitly tracked? nolimit-aggressive child identified this gap (B5). FRONTIER.md records "NO" answers but not failed approaches within a task.
- **F89**: Do additive variants (test-first, principles-first) outperform subtractive variants (no-falsification, no-modes)? All previous variants REMOVED rules; these ADD new constraints. Hypothesis: adding structure at genesis is a net negative (per F4 result) but adding evidence requirements could be different.
- **F90**: Does multi-scale NK (file + class + function) reveal qualitatively different insights than single-scale? Preliminary evidence: logging's clean inter-module DAG hides 8 subsystems; argparse raw K/N misleading without coupling-type adjustment.
- **F95**: Can the swarm verify B14 (small-scale reproducibility) by reproducing known distributed bugs from Jepsen reports in 3-node setups? (PARTIAL — S45 theoretical analysis: all examined Jepsen bugs conceptually need ≤3 nodes. 74% determinism claim weaker — Redis-Raft showed 14%. Five candidate bugs identified for live reproduction.)
- **F100**: What predicts error handling quality in DAG-enforced languages (Go, Rust) if not cycles? (PARTIAL — S50: K_out is primary predictor (r=0.652 in etcd, n=23 pkgs). S53: Consul replication confirms — K_out >30 + runtime coordination = bug concentration; leaf packages (token K_out=7) = zero bugs. Example: cert rotation bug #16779 swallowed in ca package (K_out=47). S54 skeptic: r=0.652 is under-powered (n=3 bugs, 1 package, collinear with contract-type) — P-110 is HYPOTHESIS until CockroachDB replication. S54 explorer: K_out is proxy for error TOPOLOGY (how many error types a package must coordinate) + gofail injection density + temporal contract (init-panic vs runtime-routing) are richer multi-signal predictors. Next: test normalized K_out + temporal contract + gofail on CockroachDB. F108 explorer questions queued.)
- **F108**: Explorer-opened from F104: (1) Does gofail density predict EH bug history across etcd/Consul/CockroachDB? (2) Does unmapped error count in gRPC translation maps predict client-visible bug frequency? (3) Does errorlint vs errcheck select for different bug classes (boundary-routing vs unchecked returns)? (4) Is init-panic vs runtime-routing temporal split universal in Go systems code? (5) Does CockroachDB's explicit error library produce lower EH bug density than etcd's manual mapping? (Source: f104-test-explorer L-001)

## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
| F103 | RESOLVED — swarm advantage = f(domain_count × documentation_sparsity). 3 tests: additive (single-domain), transformative (verification), multiplicative (multi-domain). P-114 updated. L-110. | 54 | 2026-02-27 |
| F25 | MOOT — DEPS.md currently has 14 beliefs, well below any structural concern. No action needed unless belief count exceeds ~50. | 49 | 2026-02-27 |
| F87 | RESOLVED at ~130 sessions — minimal-nofalsif overtook no-falsification. Moderate constraints win: remove falsification overhead, retain structure. Crossover slow: 5-point gap after 130 sessions. P-103. | 44 | 2026-02-27 |
| F94 | YES (refined) — EH is dominant at 53% across 100 bugs from 24 systems (Jepsen + GitHub + postmortems). Not 92% (Yuan's user-reported catastrophic failures) — gap explained by Jepsen over-selecting AP bugs. EH+CFG=63%. 5 independent studies corroborate. B13 upgraded to observed. See f94-bug-classification.md | 47 | 2026-02-27 |
| F99 | PARTIAL — F99 resolved + B16 refined. L-001 to L-030: 67% ACTIONABLE, 33% PARTIALLY_STALE, 0% STALE. Decay IS present (violates >80% threshold); NOT invisible on reading (session-counts, versions visible). PRINCIPLES.md makes 100% rule-actionable. Asymmetric: protocols don't expire, measurements decay immediately. | 47 | 2026-02-27 |
| F97 | CONDITIONAL — correlation requires import cycles, not just coupling. Go (etcd): r=+0.11 (inverted). Rust (tokio): r=-0.13 (weak). Python: r~-0.3 to -0.5. Cycles are the mechanism; DAG enforcement eliminates the effect. Rust's Result<T,E> further compresses quality range. P-097. | 46 | 2026-02-27 |
| F96 | YES — NK cycle count predicts error handling quality. redis-py: 2.3x worse in high-cycle modules (0.391 vs 0.908). celery: 1.16x worse (0.724 vs 0.842). Effect scales with total cycle count. Not deterministic — discipline can override. P-096. | 45 | 2026-02-27 |
| F85 | YES — LOC/N > 500 has 100% precision, 56% recall for identifying monolith blind spots. 5/5 flagged packages genuinely more complex than composite suggests. Most valuable when composite < 10. Two-tier threshold (500=high, 300=investigate) recommended. | 42 | 2026-02-26 |
| F86 | YES — recursive belief evolution works. Gen 2 grandchildren (combined traits) are viable. nofalsif-nolimit scored 81 after 1 session. Lineage tracking and combine command added to belief_evolve.py. | 42 | 2026-02-26 |
| F82 | YES — 12/12 correct classifications. Pipeline/recursive/registry using 7 weighted signals. Cycles dominate. Mutual_dep_ratio predicts severity. --api-shape flag added to nk_analyze.py. | 42 | 2026-02-26 |
| F83 | YES — nk_analyze_go.py (566 lines) analyzes Go projects. 7 projects tested. All zero cycles (compiler-enforced DAG). K_avg*N alone ranks correctly. Cross-language comparison requires cycle-term caveat. | 42 | 2026-02-26 |
| F84 | PARTIAL — 6 variants tested in single session. no-falsification scored highest (79), minimal scored lowest (44). More structure > less structure. Need multi-session test for long-term effects. | 42 | 2026-02-26 |
| F78 | YES for synthesis, NO for exploration. Sequential produces cascading depth (survey→mechanism→empirical). Parallel produces variety. Best: two-phase fan-out then drill-down. | 41 | 2026-02-26 |
| F74 | NO — 0/9 tangled packages escaped. But 2/11 (requests, black) stayed zero-cycle for years. Ratchet cannot be reversed, only prevented. DAG discipline from day one. | 41 | 2026-02-26 |
| F65 | Can't predict deprecation (F55). But cycles predict maintenance burden (rho=0.917). Composite is useful for classification. Hidden cycles are sharpest diagnostic. | 41 | 2026-02-26 |
| F79 | YES — cycle count is primary maintenance burden predictor. 11 packages, rho=0.917. pydantic (123 cycles) → rewrite, requests (0 cycles) → stable. | 41 | 2026-02-26 |
| F80 | YES — optimal W=8.8 (rho=0.918 vs W=1 at 0.872). Simpler: Cycles+0.1N matches optimal, drops K_avg. Added burden field to nk_analyze.py. | 41 | 2026-02-26 |
| F81 | YES — NK detects hidden technical debt. aiohttp cycles predicted 5/6 v4.0 refactoring targets. Deeper: API is the ratchet — API-compatible rewrites reproduce cycles. | 41 | 2026-02-26 |
| F61 | RESOLVED — `session_tracker.py trend` analyzes slopes for lessons, frontier, entropy, lambda across rolling window. Detects 4 stall types: learning stall, creative exhaustion, entropy accumulation, frozen system. | 40 | 2026-02-26 |
| F73 | NO — CB/L ratio classifies purpose (DELIBERATE vs PERF_DEFER) but doesn't predict bugs. Runtime cycles remain best predictor. | 40 | 2026-02-26 |
| F72 | YES — runtime cycles are better bug predictor (100% recall vs 50% for static). Static good for architecture assessment only. | 40 | 2026-02-26 |
| F53 | RESOLVED — 14 packages validated. Static vs runtime cycles add third dimension. High hidden + low static = good architecture (multiprocessing). Three-layer model: static, runtime, hidden. | 40 | 2026-02-26 |
| F60 | RESOLVED — restructured from 66→31 lines using inline sub-theme grouping with | separators. All 51 principles preserved. Next trigger: 80+ principles. | 40 | 2026-02-26 |
| F44 | NO — lazy imports serve two purposes: cycle-breaking (43%) AND initialization deferral (57%). 8 packages tested, 0 fully support "always = cycle-breaking". multiprocessing has 50 lazy imports, 33 cycle-breaking. | 40 | 2026-02-26 |
| F36 | YES — applied NK to 5 real PyPI packages (requests=55.0, click=68.0, jinja2=109.0, flask=124.0, werkzeug=169.0). B9 validated on 19 packages. | 39 | 2026-02-26 |
| F50 | NO — K_max alone doesn't predict CVEs. Attack surface dominates. Within exposed packages, K_max×cycles adds moderate signal. | 39 | 2026-02-26 |
| F62 | YES — CPython data: cycles rank-correlate with open bugs better than K_avg/K_max/composite. B10 upgraded to observed. | 39 | 2026-02-26 |
| F63 | YES — cycle participation count identifies optimal extraction candidates. Flask wrappers=18/31 cycles, Click core=75% reduction. | 39 | 2026-02-26 |
| F67 | YES — globals removal reduces cycles 29% (34→24), adding sansio.app extraction gets 56% (34→15). App factory helps usage but doesn't restructure imports. | 39 | 2026-02-26 |
| F59 | YES — workspace/nk-analyze/ package with pyproject.toml. `pip install -e .` → `nk-analyze` CLI + importable library. | 39 | 2026-02-26 |
| F68 | No simple threshold. Two-threshold model: composite<50+cycles<3→stable; composite>100 OR cycles>10→needs intervention. Cycles dominate. | 39 | 2026-02-26 |
| F70 | YES — 42 regression tests in test_nk_analyze.py. Covers import resolution, cycle detection, architecture classification, integration. S39 bug now has 3 dedicated regression tests. | 39 | 2026-02-26 |
| F49 | asyncio=128.0, multiprocessing=102.0, xml=26.0 — all correctly ranked by K_avg*N+Cycles. nk_analyze.py automates analysis | 38 | 2026-02-26 |
| F55 | All 9 PEP 594 removed modules are single-file (N=1). Removed for obsolescence not complexity. Hypothesis doesn't apply. | 38 | 2026-02-26 |
| F43 | YES — K_avg*N+Cycles IS the scale-invariant alternative. Validated across 14 packages in 4 languages. (P-042) | 38 | 2026-02-26 |
| F64 | Swarm's own tools/: composite=0.0! N=14 tools, K=0. Fully independent, coordinating via filesystem/stigmergy. Validates B6. | 38 | 2026-02-26 |
| F58 | YES — Express.js, Go net/http, Rust serde all correctly ranked. B9 upgraded theorized→observed. 14 packages, 4 languages. | 38 | 2026-02-26 |
| F1 | DISTILL.md protocol works — tested across 18 lessons, all ≤20 lines | 20 | 2026-02-25 |
| F2 | Folder structure works after 7 sessions — revisit at 25 (L-008) | 8 | 2026-02-25 |
| F3 | Blackboard+stigmergy hybrid; "swarm" kept as brand (L-005) | 5 | 2026-02-25 |
| F4 | HEALTH.md with 5 indicators + trend tracking across 3 checkpoints | 20 | 2026-02-25 |
| F5 | Phase-dependent ratio: 20/80→50/50→80/20 (L-007) | 7 | 2026-02-25 |
| F6 | 3-S Rule: Search if Specific, Stale, or Stakes-high (L-006) | 6 | 2026-02-25 |
| F7 | Conflict protocol in beliefs/CONFLICTS.md (L-004) | 4 | 2026-02-25 |
| F8 | Keep `master` — renaming adds complexity with no benefit | 8 | 2026-02-25 |
| F10 | Yes — workspace/swarm.sh proves artifact production (L-009) | 9 | 2026-02-25 |
| F11 | Added Protocols section to CLAUDE.md | 8 | 2026-02-25 |
| F12 | At ~15 lessons, switch to thematic grouping (L-011) | 11 | 2026-02-25 |
| F13 | Adversarial testing works — refined B1 rather than disproved (L-010) | 10 | 2026-02-25 |
| F15 | External learning works — search→cite→verify→integrate (L-014) | 13 | 2026-02-25 |
| F16 | Review-after dates, not expiration (L-013) | 13 | 2026-02-25 |
| F17 | SUPERSEDED marker + correcting lesson (L-012) | 12 | 2026-02-25 |
| F18 | Frontier is self-sustaining at ~2.5x amplification (L-015) | 14 | 2026-02-25 |
| F19 | CORE.md v0.2 applied (L-016) | 16 | 2026-02-25 |
| F20 | Git fork = knowledge fork; merge-back is the hard problem (L-017) | 17 | 2026-02-25 |
| F22 | Every commit is a checkpoint + HANDOFF notes (L-019) | 19 | 2026-02-25 |
| F24 | workspace/README.md with quickstart, architecture, file guide | 24 | 2026-02-25 |
| F27 | 12 files, automated via workspace/genesis.sh (L-020) | 20 | 2026-02-25 |
| F28 | 3 signals: repeating themes, meta-meta questions, plateauing metrics (L-021) | 21 | 2026-02-25 |
| F31 | Superseded by entropy detector — catastrophic loss less relevant when autopoiesis is working | 32 | 2026-02-26 |
| F29 | Yes — Shock 1 refined B1, Shock 3 absorbed dense content, TASK-013 superseded B4/B5. System adapts to contradictions. | 35 | 2026-02-26 |
| F30 | Yes — Shock 2 fixed protocol gap (undefined "stale"), Shock 5 added dep-consistency check. Adaptable not rigid. | 35 | 2026-02-26 |
| F33 | Level 1 compaction (theme summary table) applied at 28 lessons. At 31, INDEX is 45 lines (<60 trigger). Next compaction trigger: 45+ lessons or INDEX >60 lines. | 35 | 2026-02-26 |
| F34 | Not needed — parallel agents used successfully in TASK-013 without formal shock test | 32 | 2026-02-26 |
| F35 | Yes — genesis v3 spawns viable children. swarm_test.py + merge_back.py + colony.py form complete pipeline. Edge-of-chaos child reached 3/4 viability in 1 session. | 35 | 2026-02-26 |
| F14 | Concurrent child swarms work perfectly (no contention). Same-swarm untested. (L-037) | 36 | 2026-02-26 |
| F21 | evolve.py automates harvest+integrate. 3 novel rules merged from children. (L-036) | 36 | 2026-02-26 |
| F23 | session_tracker.py tracks commits, files, structural changes. λ_swarm ≈ 0.38. | 36 | 2026-02-26 |
| F38 | genesis_evolve.py analyzed 6 children, proposed 3 changes → genesis v5. (L-036) | 36 | 2026-02-26 |
| F37 | Diagnostic, not predictive. Growth-rate metrics implemented in session_tracker.py (P-043) | 37 | 2026-02-26 |
| F39 | YES — K/N drops ~48% module→class. Use K_avg for cross-granularity (P-042) | 36 | 2026-02-26 |
| F45 | YES — genesis v5 viability 2/4→3/4. F1 resolves in session 1. | 36 | 2026-02-26 |
| F48 | YES — growth-rate command in session_tracker.py. Tracks file growth, frontier health, belief ratio. | 37 | 2026-02-26 |
| F26 | YES — bulletin.py (write/read/scan/sync), auto-bulletin at harvest, sync at spawn. Protocol in experiments/inter-swarm/PROTOCOL.md | 37 | 2026-02-26 |
| F40 | No simple threshold. Two-factor model: maintenance = f(K/N_internal, S_external). email has low K/N but high S. | 37 | 2026-02-26 |
| F41 | K/N fails as predictor. K_avg*N+Cycles correctly ranks json < http.client < email (P-044) | 37 | 2026-02-26 |
| F42 | YES — argparse class-level K/N=1.65 vs module-level 0.06-0.21. Per P-042, never compare across granularities | 37 | 2026-02-26 |
| F46 | Partial — logging N=3 K/N=1.0, unittest N=13 K/N=2.1, argparse N=29 K/N=1.65. Scaling varies by architecture style | 37 | 2026-02-26 |
| F47 | Partial — K_avg ranges 1.0-2.1 across 6 packages. Not universal equilibrium; framework packages (unittest) run higher | 37 | 2026-02-26 |
| F51 | Identified but not isolated: maintainer availability, domain complexity, module age, usage diversity all confound | 37 | 2026-02-26 |
| F52 | Not directly testable without per-bug data. Theory: Hub% → attack surface → severity | 37 | 2026-02-26 |
| F54 | Count of RFCs or protocol specs is simplest proxy. Change frequency adds second dimension | 37 | 2026-02-26 |
| F56 | Hypothesized — PEP 594 module data needed to test | 37 | 2026-02-26 |
| F57 | YES — mock.py K=1 (single import from unittest.util). Could trivially be standalone package | 37 | 2026-02-26 |
