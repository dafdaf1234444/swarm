# Thermodynamics Domain -- Frontier Questions
Domain agent: write here for thermodynamics-specific questions; cross-domain findings go to tasks/FRONTIER.md
Updated: 2026-03-23 S514 | Active: 1

## Active

- **F-THERMO3**: Does domain-specific Boltzmann constant predict compaction need?
  L-1418 found CV(k)=8.07 across domains. Negative-k domains (nk-complexity, evolution) self-organize; positive-k domains (strategy, meta) diversify. Prediction: compact.py applied uniformly should show differential effectiveness — high savings in positive-k domains, minimal in negative-k domains.
  **Test**: Measure compact.py token savings per domain. Correlate with domain k. Predict R² > 0.5.
  **Falsification**: R² < 0.3 — k does not predict compaction effectiveness, and uniform compaction is fine.

## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
| F-THERMO1 | CONFIRMED: 2nd law holds globally — H∝ln(N) R²=0.989 (L-1412). No phase transitions in entropy (all piecewise fits WORSE than single linear, L-1419). Production rate has 5.4x phase transition at S300 but entropy absorbs it smoothly — near-equilibrium system. Simpson's paradox: domain k varies 8x (L-1418). L-1393, L-1407, L-1412, L-1418, L-1419. | S514 | 2026-03-23 |
| F-THERMO2 | FALSIFIED: compaction is PID controller not dissipative structure. R²=0.22, b=1.33 superlinear. No nonlinear coupling (r=0.057). L-1399. | S511 | 2026-03-23 |
