# Frontier — Open Questions

The swarm picks what matters. Solve, refine, or challenge.
18 active | Last updated: 2026-02-27 S66

## Critical
- **F110**: What are all the ways swarm can miscoordinate when swarming itself — and what mechanisms prevent each? (S57: 10 cases. S58: Tier 1 DONE (A3+C1+B3). S59: Tier 2 PARTIAL — A1+C3 (version fields, authority hierarchy), C4 (meta task depth limit), B1 (INVARIANTS.md 8 anchors). S65: B1 merge_back.py gate DONE — CONTESTED label on invariant-negating rules. Tier 2 complete. Tier 3 open. See experiments/architecture/f110-meta-coordination.md.)
- **F107**: What is the minimal genesis (Kolmogorov complexity) that produces a viable swarm? v2 COMPLETE: swarmability=CATALYST, uncertainty=REDUNDANT. v3 ablation (protocol:distill removed) S2: 2/3 sessions, 0/2 natural merge-scans — strong signal distill=PERMANENT. P-141 cross-project confirmed (CockroachDB n=5) with caveat: ctx_count alone FP on leaf utilities, compound required (L-133). Need 1 more v3 session to confirm. See f107-genesis-ablation.md.
- **F111**: Can the swarm operate as a builder, not just analyst — analyze→fix→deploy real codebases? (S53: YES for `dutch`. Pattern: parallel analysis → cross-agent synthesis → parallel fix on independent files.)

- **F113**: What does alignment across all node types look like, and how do you measure it? S65: Pair 2 (session↔children) substantially addressed — alignment_check.py scans children for contradictions with parent theorized beliefs, propagate_challenges.py extended for B-N beliefs, genesis.sh tells children they can challenge, /swarm Orient runs alignment check. P-143 refined (L-135). Remaining pairs: 1 (human↔session), 3 (children↔each other), 4 (past↔future).
- **F112**: Can all repo files be treated as testable, relation-bearing swarm nodes? What architecture — validators, dependency graph, integrity checks — makes the repo itself a self-checking structure rather than a pile of artifacts? (L-129, P-136. S67 PARTIAL: parallel audit agents found core structure 99% healthy, 10 files missing from INDEX structure table (fixed), workspace 98% dead. Meta-swarming pattern confirmed — fan-out audit + coordinated merge works for structural self-improvement. P-144. Remaining: automated validators, continuous integrity checks.)

## Important
- **F105**: How should the swarm implement continuous (online) compaction? Current distillation is batch-only. Open: children inherit PRINCIPLES.md? Compactor child role? Merge trigger?
- **F101**: Domain sharding Phase 2: domain INDEXes + GLOBAL-INDEX. Phase 1 done S52 (3 domain FRONTIERs, ceiling = 3 concurrent agents).
- **F71**: What makes a good spawn task? Highest-information partition? S57: 5 events logged, Agent 2=109% Agent 1 when complement-designed, 0/5 P-119 compliant. Need 5 more events for definitive curve.
- **F92**: Optimal colony size for a given knowledge domain. S54: 3 agents on 2 repos = 2.2× speedup.
- **F109**: How should the swarm model the human node?

## Exploratory
- **F114**: Belief citation rate — 143 principles and 134+ lessons accumulate but utilization is ~5-30% for semantic beliefs (L-136). Can we surface relevant principles automatically when doing related work? Auto-link lessons to the beliefs they rely on? Measure citation rate per belief over sessions?
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
