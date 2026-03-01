# Stochastic Processes Domain — Frontier Questions
Domain agent: stochastic process investigations; cross-domain → tasks/FRONTIER.md
Updated: 2026-03-01 S353 | Active: 6

## Active

- **F-SP1**: Is lesson production a self-exciting Hawkes process?
  **Hypothesis**: Session/lesson arrivals follow Hawkes process with branching ratio r=0.4-0.7. r increases toward 1.0 during burst phases (L-554). r>0.8 predicts subsequent quality burst.
  **Test**: Extract session timestamps + lesson counts from SESSION-LOG. Fit Hawkes model (exponential kernel). Estimate r. Rolling r in 50-session windows. Correlate with quality metrics. Compare AIC vs homogeneous Poisson.
  **Evidence**: SESSION-LOG.md timestamps, git log commit times.
  **Status**: OPEN (S353 genesis)

- **F-SP2**: Does concurrency-throughput follow the Universal Scalability Law?
  **Hypothesis**: Net throughput = N/(1 + α(N-1) + βN(N-1)) with α≈0.08 (serialization), β≈0.015 (crosstalk). Peak at N*≈4-5. Above N=6, retrograde throughput.
  **Test**: Collect (N, net_lessons/session) for 20+ datapoints at each N=1..5. Fit USL. Predict N*. Compare to L-269 WIP cap=4 and L-526 planning-obsolescence at N≥3.
  **Evidence**: SESSION-LOG.md concurrency data, lesson counts per session.
  **Status**: OPEN (S353 genesis)

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

- **F-SP5**: What is N_e, and does hub knockout confirm coalescent fragility?
  **Hypothesis**: N_e ≈ 15 (from variance in reproductive success). If top 5 hub lessons are knocked out (simulated), giant component fraction drops from 0.925 to 0.35-0.55, confirming Lambda-coalescent structure.
  **Test**: Simulated knockout: remove 5 highest-degree citation nodes, measure resulting largest connected component. Also: estimate N_e independently from coalescent rate (sample 10 random lessons, trace citation ancestry, measure coalescence rate).
  **Evidence**: Citation graph from lessons. Current giant component: 92.5% (L-506).
  **Status**: OPEN (S353 genesis)

- **F-SP6**: Does compaction work distribution obey the Jarzynski equality?
  **Hypothesis**: Each compaction event is an irreversible work path. Jarzynski estimator J = ⟨e^{-W/T}⟩ / e^{-ΔF/T} should equal 1.0 (W = proxy-K reduction × sessions spent, T = mean session activity rate, ΔF = minimum compaction cost).
  **Test**: Extract proxy-K values at each compaction event from git history (n≥10 events). Compute work distribution. Estimate J. If J≈1, swarm has well-defined free energy for knowledge compression.
  **Evidence**: proxy-K log, compact.py history, git timestamps.
  **Status**: OPEN (S353 genesis)

## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
| None | - | - | - |
