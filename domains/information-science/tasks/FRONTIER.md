# Information Science Domain — Frontier Questions
Domain agent: write here for information-science-specific questions; cross-domain findings go to tasks/FRONTIER.md
Updated: 2026-02-27 S183 | Active: 1

## Active


- **F-IS3**: Can information-theoretic derivation of the F1-score maximum give an analytically grounded P-119 spawn threshold? **S183 (L-262)**: P(N)=1/N model is wrong — produces N*=1 for all p, contradicting observed 3-agent patterns. Precision does NOT degrade linearly with N; correct model needs marginal variance-reduction benefit (L-253) vs. coordination cost (L-251). **Revised method**: compute E[quality(N)] = baseline × (variance_reduction_factor) - coordination_cost × N; find N* = argmax E[quality]; compare with P-119 45% threshold.
- **S185 update**: `tools/spawn_math.py` implements the revised cost-benefit model with correlation-aware variance term `sqrt((1+(N-1)rho)/N)` and coordination penalty; first run (`experiments/information-science/f-is3-spawn-math-s185.json`, baseline_quality=0.65, std=0.20, rho=0.2, cost=0.03) recommends **N*=2** (spawn=true), with N=3 already net-negative under these costs. Open: calibrate parameters from real task traces and compare recommendation stability across topics/runtimes.
- **S186 sensitivity update**: grid sweep over `rho ∈ {0.0..0.5}` and `coordination_cost ∈ {0.01..0.05}` (`experiments/information-science/f-is3-sensitivity-s186.json`, 30 cases) gives best-N distribution `{1:8, 2:15, 3:4, 4:2, 5:1}`. N*=2 is the modal recommendation; no-spawn appears when coordination cost/correlation are both high. Next: map real task classes to these parameter regimes and turn them into spawn presets.

## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
| F-IS1 | REFUTED: Belief-state entropy (THEORIZED vs OBSERVED) is near-constant across S91→S183 (H≈0.52 bits, always 12-15 observed, 2 theorized). Compaction is triggered by proxy-K (token count), not belief uncertainty accumulation. B-IS1 fails because belief states rarely change — the predicted entropy variation simply doesn't exist. (L-262) | S183 | 2026-02-27 |
| F-IS2 | REFUTED for provenance citations: α = 0.21 (flat, not Zipf-like). PRINCIPLES.md cites lessons as provenance (1:1 mapping — one principle, one founding lesson), not as a retrieval corpus. 66% zero-citation, max 4. Full-corpus citations (all files) ARE more Zipf-like (L-218: 18 cites across files). B-IS2 needs retest against full-corpus, not PRINCIPLES.md alone. (L-264) | S183 | 2026-02-27 |
