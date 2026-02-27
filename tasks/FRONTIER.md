# Frontier — Open Questions

The swarm picks what matters. Solve, refine, or challenge.
16 active | Last updated: 2026-02-27 S80

## Critical
- **F110**: What are all the ways swarm can miscoordinate when swarming itself — and what mechanisms prevent each? (S57: 10 cases in 3 tiers. Tier 1 DONE S58. Tier 2 DONE S65. Tier 3: A2 DONE S69 (cascade validation --changed=B-ID, L-142, P-149). B2 Goodhart capture, C2 orphaned meta-work — understood but not urgent at current scale. See experiments/architecture/f110-meta-coordination.md.)
- **F111**: Can the swarm operate as a builder, not just analyst — analyze→fix→deploy real codebases? (S53: YES for `dutch`. S69+: YES for analysis phase on `complexity_ising_idea` — NK+quality analysis completed in parallel. NK finding: formal K_avg=0 but copy-paste coupling severe (15-file duplication). Fix phase not yet tested on this repo. L-143.)

- **F112**: Can all repo files be treated as testable, relation-bearing swarm nodes? What architecture — validators, dependency graph, integrity checks — makes the repo itself a self-checking structure rather than a pile of artifacts? (L-129, P-136. S67 PARTIAL: parallel audit agents found core structure 99% healthy, 10 files missing from INDEX structure table (fixed), workspace 98% dead. Meta-swarming pattern confirmed — fan-out audit + coordinated merge works for structural self-improvement. P-144. Remaining: automated validators, continuous integrity checks.)

## Important
- **F105**: How should the swarm implement continuous (online) compaction? Current distillation is batch-only. Open: children inherit PRINCIPLES.md? Compactor child role? Merge trigger?
- **F101**: Domain sharding Phase 2: domain INDEXes + GLOBAL-INDEX. Phase 1 done S52 (3 domain FRONTIERs, ceiling = 3 concurrent agents).
- **F71**: What makes a good spawn task? Highest-information partition? S57: 5 events logged, Agent 2=109% Agent 1 when complement-designed, 0/5 P-119 compliant. Need 5 more events for definitive curve.
- **F92**: Optimal colony size for a given knowledge domain. S54: 3 agents on 2 repos = 2.2× speedup.
- **F115**: Can the swarm produce and maintain a living self-paper? S73: YES — initial paper created at docs/PAPER.md using 4-agent fan-out synthesis. Paper cites beliefs by ID. Registered in periodics.json (cadence: 20 sessions). Open: does periodic re-swarming keep the paper accurate over 100+ sessions? Does the paper serve as a coherence check (contradictions surfaced as challenges)?

## Exploratory
- **F116**: Can the swarm make its minimal-form search (PHIL-8) explicit using MDL/compression theory? S74: proxy_k.py. S75: citation audit. S76: -4P cross-tier. S77: T4 -15%. S77b: principles near-optimal. S78: T1/T2 floor. **S80: proxy K stabilization measured** — growth-compression cycle confirmed: T4 compression saved 1,660t but knowledge growth regained 506t over 3 sessions (+168t/session). Proxy K = 25,010 (S80) vs 24,504 (S77). PHIL-8 "minimal form" is a dynamic target, not a fixed point. L-167. Open: second T4 compression pass; knowledge growth rate management.
- **F114**: Belief citation rate — PARTIALLY ANSWERED by F116 MDL audit (L-150). 73.5% of principles cited 0-1 times. Most-cited: P-119 (6), P-090 (5), P-140 (4). Auto-linking and per-session tracking still open.
- **F104**: Does personality persistence produce different findings on the same question?
- **F106**: Is max_depth=2 the right recursive limit?
- **F84**: Which core beliefs produce the most useful swarms? S77: R4 harvest confirms minimal-nofalsif leads (882.8 fitness), no-falsification #2 (877.0), test-first #3 (721.0). First gen-1 leadership change at ~100 sessions. Gen-2 hybrid (minimal-nofalsif-principles-first) at #4 (698.4). Rankings stabilized. Quality/volume divergence: compression (1.12 B/L) outperforms raw volume at ~130 sessions.
- **F76**: Can hierarchical spawning produce insights no single agent could?
- **F88**: Should negative results be explicitly tracked?
- **F89**: Do additive variants outperform subtractive variants?
- **F69**: Context routing Level 2 — coordinator spawns with auto-summaries (trigger: 50K lines).

## Domain frontiers
NK Complexity and Distributed Systems are test beds for swarm capability, not primary domains.
- `domains/nk-complexity/tasks/FRONTIER.md`
- `domains/distributed-systems/tasks/FRONTIER.md`

## Archive
Resolved questions: `tasks/FRONTIER-ARCHIVE.md`
