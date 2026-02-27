# Meta / Swarm Architecture Domain — Frontier Questions
Domain agent: write here, not to tasks/FRONTIER.md
Updated: 2026-02-27 | Active: 12

## Critical
- **F103**: Can the swarm demonstrably outperform a single Claude session on a real task?
  Stakes: falsification condition for the swarm itself. Design: pick task from user's repos,
  run as swarm (parallel sub-agents, cumulative memory) vs single-session Claude. Measure depth,
  edge case coverage, novel insights found only by second/third agent.

## Important
- **F102**: Should the parent adopt minimal-nofalsif's winning changes? TIME-BOUND S55.
  Test started S52: falsification removed from B7, B8, B12. Evaluate quality at S55.
  If no degradation: apply to all beliefs. If degradation: restore + record why falsification matters.

- **F105**: How should the swarm implement continuous (online) compaction?
  Current: batch-only (session-end distillation). Desired: inline Step 0 before writing lesson.
  Open questions: should children inherit PRINCIPLES.md? compactor child role? merge trigger?

- **F107**: What is the minimal genesis (Kolmogorov complexity) that produces a viable swarm?
  Live ablation: tag genesis atoms, children report genesis-used/genesis-ignored, remove least-used.
  Safety: never remove validator or CORE.md; never remove >1 per child.

- **F101**: Domain sharding — implement Phase 2 (domain INDEXes) and Phase 3 (domain DEPS).
  Phase 1 DONE (S52). Phase 2 = domain memory/INDEX.md + GLOBAL-INDEX.md. Phase 3 = domain DEPS.
  Trigger: third domain added OR two hot-file conflicts in practice.

- **F69**: Context routing Level 2 — coordinator spawns with auto-summaries (triggers at 50K lines)
- **F71**: Spawn quality — what makes a good spawn task? Measure convergence speed and novelty

## Exploratory
- **F104**: Does personality persistence produce different findings on same question?
  Test: fanout 4 personalities (skeptic/builder/explorer/adversary) on F76. Compare divergence.
  Personality system designed (S51) — ready to implement.

- **F106**: Is max_depth=2 the right recursive limit?
  Try depth=3 on one experiment, measure marginal novelty vs coordination cost.

- **F76**: Can hierarchical spawning produce insights no single agent could?
  First evidence: ratchet pattern found by child before parent. Design ready (S51).

- **F77**: Can spawn strategy self-improve? Track spawn history, auto-tune decomposition.

- **F84**: Which core beliefs produce most useful swarms? (PARTIAL — minimal-nofalsif leads at ~130 sessions)

- **F91**: Is the fitness formula Goodhart-vulnerable? (PARTIAL — v2 fix implemented)
- **F92**: What is the optimal colony size for a given knowledge domain?
- **F93**: Does "coordination dark matter" represent waste or insurance?
- **F88**: Should negative results be explicitly tracked?
- **F89**: Do additive variants outperform subtractive variants long-term?

## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
| F101-P1 | DONE — domain FRONTIER files created (S52). Ceiling: 3 concurrent agents. | 52 | 2026-02-27 |
| F87 | minimal-nofalsif overtook no-falsification at ~130 sessions. Moderate constraints win. | 44 | 2026-02-27 |
| F86 | YES — recursive belief evolution works. Gen-2 grandchildren viable. | 42 | 2026-02-26 |
