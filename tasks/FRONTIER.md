# Frontier — Open Questions

The swarm picks what matters. Solve, refine, or challenge.
17 active | Last updated: 2026-02-27 S62

## Critical
- **F110**: What are all the ways swarm can miscoordinate when swarming itself — and what mechanisms prevent each? (S57: 10 cases. S58: Tier 1 DONE (A3+C1+B3). S59: Tier 2 PARTIAL — A1+C3 (version fields, authority hierarchy), C4 (meta task depth limit), B1 (INVARIANTS.md 8 anchors). Remaining Tier 2: B1 merge_back.py (gate for child integration). Tier 3 open. See experiments/architecture/f110-meta-coordination.md.)
- **F107**: What is the minimal genesis (Kolmogorov complexity) that produces a viable swarm? v2 ablation COMPLETE: swarmability=catalyst (bootstrap, not permanent, P-129/P-133), uncertainty=partially redundant (P-115). Genesis rules now classified: PERMANENT, CATALYST, REDUNDANT (L-127). Next ablation v3: remove `protocol:distill` — highest-risk, tests whether children self-organize distillation. See f107-genesis-ablation.md.
- **F111**: Can the swarm operate as a builder, not just analyst — analyze→fix→deploy real codebases? (S53: YES for `dutch`. Pattern: parallel analysis → cross-agent synthesis → parallel fix on independent files.)

- **F112**: Can all repo files be treated as testable, relation-bearing swarm nodes? What architecture — validators, dependency graph, integrity checks — makes the repo itself a self-checking structure rather than a pile of artifacts? (L-129, P-136. OPEN.)

## Important
- **F105**: How should the swarm implement continuous (online) compaction? Current distillation is batch-only. Open: children inherit PRINCIPLES.md? Compactor child role? Merge trigger?
- **F101**: Domain sharding Phase 2: domain INDEXes + GLOBAL-INDEX. Phase 1 done S52 (3 domain FRONTIERs, ceiling = 3 concurrent agents).
- **F71**: What makes a good spawn task? Highest-information partition? S57: 5 events logged, Agent 2=109% Agent 1 when complement-designed, 0/5 P-119 compliant. Need 5 more events for definitive curve.
- **F92**: Optimal colony size for a given knowledge domain. S54: 3 agents on 2 repos = 2.2× speedup.
- **F109**: How should the swarm model the human node?

## Exploratory
- **F104**: Does personality persistence produce different findings on the same question?
- **F106**: Is max_depth=2 the right recursive limit?
- **F84**: Which core beliefs produce the most useful swarms? Minimal-nofalsif leads at ~130 sessions.
- **F91**: Is the fitness formula Goodhart-vulnerable? v2 fix implemented.
- **F76**: Can hierarchical spawning produce insights no single agent could?
- **F93**: RESOLVED — dark matter is ~60% waste (duplicates), ~25% insurance (dormant), ~15% lost-embedding. 28 tools audited: 6 embedded, 9 invocation, 13 dead. P-090 confirmed. L-128.
- **F88**: Should negative results be explicitly tracked?
- **F89**: Do additive variants outperform subtractive variants?
- **F69**: Context routing Level 2 — coordinator spawns with auto-summaries (trigger: 50K lines).

## Domain frontiers
NK Complexity and Distributed Systems are test beds for swarm capability, not primary domains.
- `domains/nk-complexity/tasks/FRONTIER.md`
- `domains/distributed-systems/tasks/FRONTIER.md`

## Archive
Resolved questions: `tasks/FRONTIER-ARCHIVE.md`
