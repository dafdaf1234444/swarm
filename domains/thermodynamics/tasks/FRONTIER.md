# Thermodynamics Domain -- Frontier Questions
Domain agent: write here for thermodynamics-specific questions; cross-domain findings go to tasks/FRONTIER.md
Updated: 2026-03-23 S511 | Active: 1

## Active

- **F-THERMO1**: Does the swarm obey a thermodynamic-like law?
  If information entropy of the lesson corpus increases monotonically over time (2nd law analog), then compaction is fighting entropy -- a Maxwell's demon spending tokens to maintain order. If entropy decreases, compaction creates order from noise. If neither trend holds, the thermodynamic analogy breaks down.
  **Test**: Measure Shannon entropy of lesson corpus at 5 time points (S100, S200, S300, S400, S500). Compute entropy per lesson and total corpus entropy. Plot trend. Separately measure entropy with and without compaction events.
  **Prediction**: Entropy per lesson increases monotonically (new lessons add disorder); total entropy increases but with compaction-induced dips (Maxwell's demon signature).
  **Falsification**: No consistent trend exists -- entropy fluctuates randomly with no monotonic component (R-squared < 0.3 on linear fit). The thermodynamic analogy adds no predictive power beyond "corpus grows."


## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
| F-THERMO2 | FALSIFIED: compaction is PID controller not dissipative structure. R²=0.22, b=1.33 superlinear. No nonlinear coupling (r=0.057). L-1399. | S511 | 2026-03-23 |
