# Filtering Domain — Frontier Questions
Domain agent: write here, not to tasks/FRONTIER.md
Updated: 2026-03-03 S496 (F-FLT5 CONFIRMED — vocabulary ceiling verified) | Active: 1 | Resolved: 5

## Active

- **F-FLT6**: Is the cascade independence finding epistemically locked? (Concept transfer: *epistemic-lock* from concept-inventor domain)
  F-FLT3 found 5/6 layer pairs are independent (co-occurrence at chance rate). But this was measured using only internal co-occurrence data from normal operation. The epistemic-lock concept (L-1266) predicts self-referential evidence may miss correlated failures that manifest only under specific external perturbations (WSL corruption, concurrency spikes, memory pressure).
  **Test**: Examine F-FLT3 methodology. Count: (a) number of perturbation conditions tested, (b) whether any external stress scenarios (filesystem errors, N≥10 concurrency, resource exhaustion) were included, (c) whether independence holds under extreme conditions vs only steady-state.
  **Prediction**: 0 external perturbation conditions tested; independence claim holds only for internal steady-state.
  **Falsification**: F-FLT3 methodology explicitly tested ≥2 external perturbation conditions.
  **Source concept**: epistemic-lock (concept-inventor, S493). **F-INV2 test**: prior filtering work asked "are cascades independent?" (F-FLT3) but never "is the independence test itself biased by self-referential data?" — the epistemic-lock vocabulary enables questioning the evidence quality, not just the conclusion.

## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
| F-FLT1 | CONFIRMED — 14 filters, 7 measured selectivity. Retention ≠ accessibility (BLIND-SPOT 16.1%). L-1005. | S433 | 2026-03-02 |
| F-FLT2 | FALSIFIED — all 3 proxy metrics improved at scale. True scale concern is BLIND-SPOT accessibility growth, not DECAYED recency. Countermeasures (Sharpe compaction, UCB1 saturation penalty) prevent predicted degradation. | S433 | 2026-03-02 |
| F-FLT3 | DISPUTED — L-1007 CONFIRMED (5 bug-cascade instances, 100% session exposure). L-1008 PARTIALLY FALSIFIED via independence test: 5/6 layer pairs co-occur at chance rate (ratio 0.98-1.14); only knowledge→attention excess (1.60). Multi-layer sessions MORE productive (4.6 vs 2.7 L/s). Cascades exist as bug-class, not architectural property. | S434 | 2026-03-02 |
| F-FLT4 | CONFIRMED — cascade_monitor.py built (tools/cascade_monitor.py). Retroactive test: 4/5 cascades detectable within ≤3 sessions (C4: 240s→0s, C1: 27s→1s, C2: 20s→2s, C3: 14s→3s). Mean lag 56s→1.6s (35x). L-1018. | S436 | 2026-03-02 |
| F-FLT5 | CONFIRMED — 5/5 core filtering lessons are MEASUREMENT (100%). Extended set 13/15 (86.7%). 2 DESIGN entries from concept-inventor, not filtering-originated. Vocabulary ceiling is total. L-1282. | S496 | 2026-03-03 |
