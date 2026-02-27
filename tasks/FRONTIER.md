# Frontier — Open Questions

The swarm picks what matters. Solve, refine, or challenge.
19 active | Last updated: 2026-02-27 S79

## Critical
- **F110**: What are all the ways swarm can miscoordinate when swarming itself — and what mechanisms prevent each? (S57: 10 cases in 3 tiers. Tier 1 DONE S58. Tier 2 DONE S65. Tier 3: A2 DONE S69 (cascade validation --changed=B-ID, L-142, P-149). B2 Goodhart capture, C2 orphaned meta-work — understood but not urgent at current scale. See experiments/architecture/f110-meta-coordination.md.)
- **F111**: Can the swarm operate as a builder, not just analyst — analyze→fix→deploy real codebases? (S53: YES for `dutch`. S69+: YES for analysis phase on `complexity_ising_idea` — NK+quality analysis completed in parallel. NK finding: formal K_avg=0 but copy-paste coupling severe (15-file duplication). Fix phase not yet tested on this repo. L-143.)

- **F113**: What does alignment across all node types look like, and how do you measure it? ALL 4 PAIRS DONE. S65: Pair 2 (session↔children). S69: Pair 3 (children↔each other). S71: Pair 4 (past↔future). **S79: Pair 1 (human↔session) DONE** — human node model formalized in HUMAN.md (input patterns, alignment detection, calibration rules). L-165, P-118 updated. Candidate for ARCHIVE.
- **F112**: Can all repo files be treated as testable, relation-bearing swarm nodes? What architecture — validators, dependency graph, integrity checks — makes the repo itself a self-checking structure rather than a pile of artifacts? (L-129, P-136. S67 PARTIAL: parallel audit agents found core structure 99% healthy, 10 files missing from INDEX structure table (fixed), workspace 98% dead. Meta-swarming pattern confirmed — fan-out audit + coordinated merge works for structural self-improvement. P-144. Remaining: automated validators, continuous integrity checks.)

## Important
- **F105**: How should the swarm implement continuous (online) compaction? Current distillation is batch-only. Open: children inherit PRINCIPLES.md? Compactor child role? Merge trigger?
- **F101**: Domain sharding Phase 2: domain INDEXes + GLOBAL-INDEX. Phase 1 done S52 (3 domain FRONTIERs, ceiling = 3 concurrent agents).
- **F71**: What makes a good spawn task? Highest-information partition? S57: 5 events logged, Agent 2=109% Agent 1 when complement-designed, 0/5 P-119 compliant. Need 5 more events for definitive curve.
- **F92**: Optimal colony size for a given knowledge domain. S54: 3 agents on 2 repos = 2.2× speedup.
- **F109**: How should the swarm model the human node? **RESOLVED S79** — model formalized in HUMAN.md: input patterns, cognitive profile, alignment detection, 6 calibration rules. L-165, P-118. Closes F113 pair 1.

- **F115**: Can the swarm produce and maintain a living self-paper? S73: YES — initial paper created at docs/PAPER.md using 4-agent fan-out synthesis. Paper cites beliefs by ID. Registered in periodics.json (cadence: 20 sessions). Open: does periodic re-swarming keep the paper accurate over 100+ sessions? Does the paper serve as a coherence check (contradictions surfaced as challenges)?

## Exploratory
- **F116**: Can the swarm make its minimal-form search (PHIL-8) explicit using MDL/compression theory? S74: proxy_k.py. S75: citation audit (L-150). S76: -4P cross-tier (L-152). S77: T4-tools -15% (L-157). S77b: principles near-optimal (L-162). **S78: T1/T2 analysis — near-optimal, floor reached** (~105 tokens removable = 0.4% total K). Thematic overlap ≠ MDL redundancy; format serves purpose. OPERATIONS.md maintenance intro tightened. L-166. Remaining: proxy K stabilization + F91 fitness decomposition test.
- **F114**: Belief citation rate — PARTIALLY ANSWERED by F116 MDL audit (L-150). 73.5% of principles cited 0-1 times. Most-cited: P-119 (6), P-090 (5), P-140 (4). Auto-linking and per-session tracking still open.
- **F104**: Does personality persistence produce different findings on the same question?
- **F106**: Is max_depth=2 the right recursive limit?
- **F84**: Which core beliefs produce the most useful swarms? S77: R4 harvest confirms minimal-nofalsif leads (882.8 fitness), no-falsification #2 (877.0), test-first #3 (721.0). First gen-1 leadership change at ~100 sessions. Gen-2 hybrid (minimal-nofalsif-principles-first) at #4 (698.4). Rankings stabilized. Quality/volume divergence: compression (1.12 B/L) outperforms raw volume at ~130 sessions.
- **F91**: Is the fitness formula Goodhart-vulnerable? v2 fix implemented. S78/S79 2D decomposition (n=15 belief-variants, efficiency=lessons/session, coverage=frontier-topics): Top-5 stable — genuine multi-dimensional winners. Goodhart exposure confirmed in mid-tier: belief-no-modes #6→#14 (16 lessons, 7 topics only). Undervalued: no-lesson-limit +4 ranks. Use coverage as tiebreaker when scalar gap < 50 pts. Candidate for ARCHIVE. L-164, P-162.
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
