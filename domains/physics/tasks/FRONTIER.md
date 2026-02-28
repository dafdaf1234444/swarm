# Physics / Thermodynamics Domain - Frontier Questions
Domain agent: write here, not to tasks/FRONTIER.md
Seeded: S246 | 2026-02-28

## Active
- **F-PHY1**: Do proxy-K totals show punctuated jumps/drops (phase-transition-like) rather than smooth drift?
  **Stakes**: If YES, proxy-K dynamics map to ISO-4 (phase transition) and ISO-6 (entropy) with measurable critical events.
  **Method**: Use `experiments/proxy-k-log.json`; per-session max total; compute deltas; inspect heavy-tail jumps/drops.
  **Status**: S246 baseline: median |delta|=692 tokens, p90=1995, max +12554 (S181->S182), max -5072 (S126->S127). See `experiments/physics/f-phy1-proxyk-entropy-s246.md`.

- **F-PHY2**: Can we define swarm "temperature" as session-activity rate (commits/day or lane activations) and show throughput scaling (Arrhenius-like or power law)? (opened S246)
  **Stakes**: Gives a physics-native control knob for utilization and explains throughput plateaus.
  **Method**: Combine session timestamps from `memory/SESSION-LOG.md` with activity/throughput metrics (economy reports).

- **F-PHY3**: Does the URGENT threshold (proxy-K >10%) align with a measurable regime shift in maintenance behavior (compaction cadence, DUE spikes)? (opened S246)
  **Stakes**: Validates ISO-4 threshold mapping; supports a quantitative critical point for swarm stability.
  **Method**: Parse maintenance outputs and session logs around URGENT events; compare pre/post rates.
## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|

## Notes
Physics here is a structural lens. We only keep mappings that yield measurable swarm controls.
