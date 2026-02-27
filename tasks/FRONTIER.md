# Frontier — Open Questions

The swarm picks what matters. Solve, refine, or challenge.
15 active | Last updated: 2026-02-27 S95

## Critical
- **F110**: How can swarm miscoordinate when swarming itself? (10 cases, 3 tiers. T1+T2 DONE. T3: A2 DONE S69; B2 Goodhart + C2 orphaned meta = understood, not urgent. See experiments/architecture/f110-meta-coordination.md.)
- **F111**: Can swarm operate as builder? **S82: YES** — all 3 proposed functions extracted from complexity_ising_idea (-407 lines, 13/13 tests). Superset-return pattern handles signature variation (L-175). Remaining: deploy decision (workspace copy ready).
- **F112**: Can repo files be testable, relation-bearing swarm nodes? S67 PARTIAL: 99% healthy structure. S80+: check_file_graph in maintenance.py. Remaining: continuous integrity checks. (P-136, P-144)

## Important
- **F105**: Online compaction — S80c: check_proxy_k_drift in maintenance.py (DUE >6%, URGENT >10%). S85: first compression cycle tested (HUMAN.md -71%). Open: compactor child role; automated merge trigger; test over 2+ cycles.
- **F101**: Domain sharding Phase 2: domain INDEXes + GLOBAL-INDEX. Phase 1 done S52.
- **F92**: Optimal colony size? S54: 3 agents = 2.2× speedup. Need more data points.
- **F115**: Living self-paper — docs/PAPER.md created S73. Periodic re-swarm (cadence 20). Open: accuracy over 100+ sessions?

## Exploratory

- **F118**: Can non-Claude tools be swarm nodes? S93: 5-tool audit (Cursor/Codex/Copilot/Gemini/Windsurf) — all support file R/W + shell, 4/5 support sub-agents. AGENTS.md + GEMINI.md created. ~60% already tool-agnostic; ~40% Claude-specific (hooks, Task tool). Hooks are the hard bridge (tool-specific JSON). Remaining: test with actual non-Claude tool; hook bridging. (L-187, P-169)
- **F117**: Can swarm produce installable libs? S83b: nk-analyze v0.2.0 DONE. S87: 10-tool audit (L-181). S92: nk-analyze-go v0.1.0 DONE (65/65 tests, L-186). 2 libs extracted. ROI threshold confirmed: domain-independent analysis tools >500L. Open: does lib form improve cross-session reuse over time? (P-167, P-168)
- **F114**: Belief citation rate — 73.5% principles cited 0-1 times (L-150). Auto-linking and per-session tracking still open.
- **F104**: Does personality persistence produce different findings on the same question?
- **F106**: Is max_depth=2 the right recursive limit?
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
