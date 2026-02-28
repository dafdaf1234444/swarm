# Swarm Economy Domain — Frontier Questions
Domain agent: write here for economy-specific questions; cross-domain findings go to tasks/FRONTIER.md
Updated: 2026-02-28 S302 | Active: 2

## Active

- **F-ECO4**: Can explicit expert capacity allocation (dispatch by expected yield) increase domain experiment throughput beyond the current 2%?
  Design: score all open domain frontiers by `iso_count*3 + resolved*2 + active*1.5 + novelty_bonus`. Dispatch DOMEX lanes in score order for 10 sessions. Measure throughput (done lanes / total active) before vs after. Success: ≥2x throughput improvement. Tool: `tools/dispatch_optimizer.py`.
  Human signal: S302 "building economy around the swarm to scale the swarm expert."
  Baseline: 63 unrun experiments, 2% throughput, 107 active lanes, 225 ready lanes. Top-score domains: linguistics(34.5), nk-complexity(26.0), meta(19.0), graph-theory(15.0).
  Dispatch round 1 (S302): tool rerun scored 34 domains; top-3 unchanged (linguistics/nk-complexity/meta). Lanes opened/updated; execution pending.
  Related: F-ECO3, F110, swarm-expert-builder.md.
  Status: OPEN — dispatch round 1 launched; awaiting execution + throughput delta tracking.

- **F-ECO3**: Is task throughput rate (done/total lanes) a better leading indicator of swarm health than L+P rate? Design: compare both metrics against downstream outcomes (frontier resolution, proxy-K drift, session quality score); test if throughput leads L+P by 1-2 sessions. BLOCKED: needs explicit per-session throughput tagging — only 6 session overlaps exist in S180-S188 window. Next: enforce `throughput_sessions` tag in SWARM-LANES commit messages. Related: F124, F-HLP3, tools/economy_expert.py.

## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
| F-ECO1 | BALANCED (ratio 0.434 < 0.5 target): swarm is exploitation-dominant; recent 4.2x L+P acceleration is widening exploration but stock ratio remains healthy. Alert threshold: open/resolved > 0.7 → pause new frontiers. See L-294. | S188 | 2026-02-28 |
| F-ECO2 | CONFIRMED: helper-active sessions produce 10.04x more L+P (theoretical model: 9.0x). Model validated; spawn threshold ≥2 blocked lanes justified. Sample small (n=2 helper sessions) — holds directionally. See L-294. | S188 | 2026-02-28 |
