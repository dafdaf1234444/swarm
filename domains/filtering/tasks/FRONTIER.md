# Filtering Domain — Frontier Questions
Domain agent: write here, not to tasks/FRONTIER.md
Updated: 2026-03-03 S495 (F-INV2 vocabulary ceiling breaking: 2 new frontiers via concept transfer) | Active: 2 | Resolved: 4

## Active

- **F-FLT5**: Is the filtering domain trapped in measurement vocabulary? (Concept transfer: *vocabulary-ceiling* from concept-inventor domain)
  All 4 resolved filtering frontiers (F-FLT1..4) are MEASUREMENT-oriented: measuring selectivity, scale degradation, cascade patterns, cascade monitoring. None ask about DESIGNING new filters or evolving filter behavior. The vocabulary-ceiling concept (L-1266) predicts that measurement-focused vocabulary blocks design-oriented questions — you can only ask what your concepts let you formulate.
  **Test**: Classify all filtering lessons + resolved frontier answers into MEASUREMENT (characterizing what exists) vs DESIGN (building new filter mechanisms or modifying existing ones). Compute ratio.
  **Prediction**: >90% MEASUREMENT, <10% DESIGN.
  **Falsification**: ≥30% DESIGN-oriented content exists in resolved filtering work.
  **Source concept**: vocabulary-ceiling (concept-inventor, S493). **F-INV2 test**: this is a self-referential test — asking "is the filtering domain vocabulary-limited?" using vocabulary-ceiling vocabulary. If confirmed, it demonstrates the concept's diagnostic power. If falsified, design content exists but wasn't labeled as such.

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
