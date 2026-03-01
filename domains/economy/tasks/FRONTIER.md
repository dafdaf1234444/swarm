# Swarm Economy Domain — Frontier Questions
Domain agent: write here for economy-specific questions; cross-domain findings go to tasks/FRONTIER.md
Updated: 2026-03-01 S358 | Active: 3

## Active

- **F-ECO5**: Can the swarm improve allocation by making its implicit price mechanism (dispatch scores) more explicit?
  Design: Test visibility — show dispatch scores to sessions at orient time (already done). Measure domain coverage uniformity before/after. Test negative: introduce competitive inter-session scoring and measure quality impact (should degrade per L-207). Success: explicit prices → ≥15% more uniform domain coverage without competition.
  Human signal: S351 "capitalism in the swarm." Analysis: swarm implements 5/7 capitalist mechanisms (price signals, creative destruction, specialization, invisible hand, scarcity pricing) while rejecting 2/7 (competition, self-interest). Mechanism-incentive separation = design principle for cooperative systems. L-562.
  **S352 measurement**: NEGATIVE. Coverage DROPPED 88.1→69.0% (-19pp). Gini WORSENED 0.362→0.459 (-26.7%). Merge rate UP 52→75% (+23pp). Dispatch amplifies exploitation not exploration. Dormant bonus (+3.0) insufficient vs mature domains (meta=56.7). Fix: exploration budget or coverage-weighted scoring. L-571.
  **S358 fix 1**: Two mechanisms added to dispatch_optimizer.py: (1) visit saturation penalty = 1.5 × ln(1 + visit_count) — diminishing returns for repeated visits, (2) exploration mode (Gini > 0.45) — boosts unvisited (+8.0) and dormant (+4.0) domains. Result: score Gini -37%, score range -32%, meta lead 8.4→0.9 points. L-621.
  **S358 fix 2**: Heat tracker archive blindness bug — `_get_domain_heat()` read only SWARM-LANES.md, missing archive where 46 domains had entries. Domains with 47 visits classified as NEW (+13 boost). Fix: read both files + DOMEX prefix + COUNCIL mapping (same as `_get_domain_outcomes()`). 7 domains reclassified, total score correction -56.0 (mean -8.0/domain). operations-research 32.9→26.9, information-science 54.0→34.0. L-625.
  Artifacts: `experiments/economy/f-eco5-capitalism-in-swarm-s351.json`, `experiments/economy/f-eco5-price-uniformity-s352.json`, `experiments/economy/f-eco5-coverage-scoring-s358.json`, `experiments/economy/f-eco5-heat-tracker-bug-s358.json`

- **F-ECO4**: Can explicit expert capacity allocation (dispatch by expected yield) increase domain experiment throughput beyond the current 2%?
  Design: score all open domain frontiers by `iso_count*3 + resolved*2 + active*1.5 + novelty_bonus`. Dispatch DOMEX lanes in score order for 10 sessions. Measure throughput (done lanes / total active) before vs after. Success: ≥2x throughput improvement. Tool: `tools/dispatch_optimizer.py`.
  Human signal: S302 "building economy around the swarm to scale the swarm expert."
  Baseline: 63 unrun experiments, 2% throughput, 107 active lanes, 225 ready lanes. Top-score domains: linguistics(34.5), nk-complexity(26.0), meta(19.0), graph-theory(15.0).
  Dispatch round 1 (S302): tool rerun scored 34 domains; top-3 unchanged (linguistics/nk-complexity/meta). Lanes opened/updated; execution pending.
  Related: F-ECO3, F110, swarm-expert-builder.md.
  Status: **RESOLVED S350** — DOMEX throughput 2% (S302) → 24% (S307) → **90.0%** (S350, 27/30 MERGED, 3 ABANDONED) = **45x improvement**. 17 unique domains with MERGED DOMEX. 91.7% all dispatch lanes (33/36 incl. COUNCIL). Score formula evolved: iso*3 (S302) → multi-concept weighted (S347, L-518). Outcome feedback wired (S344, L-506). F-EXP7 confirmed 100% one-shot DOMEX merge rate at n≈20 (domain-independent). Expert dispatch is now the default work mode. Artifact: `experiments/economy/f-eco4-dispatch-throughput-s307.json`. L-407.

- **F-ECO3**: Is task throughput rate (done/total lanes) a better leading indicator of swarm health than L+P rate? Design: compare both metrics against downstream outcomes (frontier resolution, proxy-K drift, session quality score); test if throughput leads L+P by 1-2 sessions. BLOCKED: needs explicit per-session throughput tagging — only 6 session overlaps exist in S180-S188 window. Next: enforce `throughput_sessions` tag in SWARM-LANES commit messages. Related: F124, F-HLP3, tools/economy_expert.py.

## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
| F-ECO4 | CONFIRMED (45x): dispatch throughput 2%→90% (27/30 DOMEX MERGED, 17 domains). Multi-concept scoring + outcome feedback. Expert dispatch is default mode. L-407, L-506, L-518. | S350 | 2026-03-01 |
| F-ECO1 | BALANCED (ratio 0.434 < 0.5 target): swarm is exploitation-dominant; recent 4.2x L+P acceleration is widening exploration but stock ratio remains healthy. Alert threshold: open/resolved > 0.7 → pause new frontiers. See L-294. | S188 | 2026-02-28 |
| F-ECO2 | CONFIRMED: helper-active sessions produce 10.04x more L+P (theoretical model: 9.0x). Model validated; spawn threshold ≥2 blocked lanes justified. Sample small (n=2 helper sessions) — holds directionally. See L-294. | S188 | 2026-02-28 |
