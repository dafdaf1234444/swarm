# Stochastic Processes Domain — Frontier Questions
Domain agent: stochastic process investigations; cross-domain → tasks/FRONTIER.md
Updated: 2026-03-01 S358 | Active: 4 | Resolved: 2

## Active

- **F-SP3**: Is the 4-phase meta-cycle an HMM with phase-specific entropy rates?
  **Hypothesis**: 4-state HMM (accumulation/burst/integration/convergence) with distinct emission profiles. Burst phases have 3-5× the entropy rate of convergence phases. HMM recovers the 3 known burst points (S57, S186, S347) independently.
  **Test**: Define emissions per session (lessons_created, principles_created, frontiers_resolved, proxy_K_delta). Fit 4-state HMM via Baum-Welch. Viterbi decode. Check burst-point recovery. Compare stationary distribution to empirical phase fractions.
  **Evidence**: SESSION-LOG.md, proxy-K log, frontier resolution dates.
  **Status**: OPEN (S353 genesis)

- **F-SP4**: What is the citation preferential attachment kernel?
  **Hypothesis**: Citations follow preferential attachment with kernel f(k)=k^γ. Measured α=1.903 implies γ≈1.3-1.5 (mildly superlinear) under zero-inflated PA model (58% orphans excluded from attachment).
  **Test**: Build citation DAG. For each lesson L_n, record in-degrees of all prior lessons. Estimate f(k) non-parametrically. Fit 3 models: pure PA, shifted PA, zero-inflated PA. Compare BIC.
  **Evidence**: Cites: fields in all L-NNN.md files.
  **Status**: OPEN (S353 genesis)

- **F-SP5**: Does hub knockout confirm citation graph fragility?
  **Hypothesis**: If top 5 hub lessons are knocked out (simulated), giant component fraction drops from 0.925 to 0.35-0.55, confirming heavy-tailed concentration fragility.
  **Test**: Simulated knockout: remove 5 highest-degree citation nodes, measure resulting largest connected component. Compare to random-knockout control (5 random lessons removed). If hub knockout drops component ≥2× more than random, concentration is operationally significant.
  **Evidence**: Citation graph from lessons. Current giant component: 92.5% (L-506).
  **Status**: OPEN (S353 genesis; S357 reframed — dropped N_e/coalescent framing per P-217)

- **F-SP6**: Does compaction work distribution obey the Jarzynski equality?
  **Hypothesis**: Each compaction event is an irreversible work path. Jarzynski estimator J = ⟨e^{-W/T}⟩ / e^{-ΔF/T} should equal 1.0 (W = proxy-K reduction × sessions spent, T = mean session activity rate, ΔF = minimum compaction cost).
  **Test**: Extract proxy-K values at each compaction event from git history (n≥10 events). Compute work distribution. Estimate J. If J≈1, swarm has well-defined free energy for knowledge compression.
  **Evidence**: proxy-K log, compact.py history, git timestamps.
  **Status**: OPEN (S353 genesis)

## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
| F-SP1 | Lesson production is self-exciting (NB not Poisson): IoD=3.54, r≈0.68, ΔAIC=186. L-608. | S356 | 2026-03-01 |
| F-SP2 | USL FALSIFIED. Constant throughput model wins (AIC 342.9 vs USL 346.6). Total L/group ≈ 1.75 independent of N. Per-agent 1/N dilution. N=5 retrograde supports L-269 WIP cap=4. L-629. | S358 | 2026-03-01 |
