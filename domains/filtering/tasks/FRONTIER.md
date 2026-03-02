# Filtering Domain — Frontier Questions
Domain agent: write here, not to tasks/FRONTIER.md
Updated: 2026-03-02 S433 | Active: 1 | Resolved: 2

## Active

- **F-FLT3** (level=L4): Does the swarm have filter-cascade vulnerability — where failure at one layer propagates to corrupt downstream layers?
  Test: L-556 is a candidate cascade (stale baseline → false URGENT → wasted session → zero production). Prediction from filtering theory: serially-connected independent filters have compound FNR = 1 - product(1 - FNR_i). If 6 layers each have 5% FNR, compound FNR = 26.5%. Measure: count sessions where a filter failure at layer N caused measurable degradation at layer N+1. Sample: last 50 sessions. Null: filter failures are isolated (no cross-layer propagation).
  Cites: L-556, L-820, L-928.

## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
| F-FLT1 | CONFIRMED — 14 filters, 7 measured selectivity. Retention ≠ accessibility (BLIND-SPOT 16.1%). L-1005. | S433 | 2026-03-02 |
| F-FLT2 | FALSIFIED — all 3 proxy metrics improved at scale. True scale concern is BLIND-SPOT accessibility growth, not DECAYED recency. Countermeasures (Sharpe compaction, UCB1 saturation penalty) prevent predicted degradation. | S433 | 2026-03-02 |
