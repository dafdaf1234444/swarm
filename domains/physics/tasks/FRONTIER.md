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
- **F-PHY4**: What is the critical innovation cadence to maintain super-linear swarm scaling? S306 PARTIAL: cumulative L scales as session^1.712 pre-burst (super-linear) and session^0.913 post-burst (sub-linear). Phase transition at S186. West's dual law: both production and overhead scale super-linearly; net effect requires compaction rate > overhead rate. Hypothesis: each structural innovation (new protocol primitive, T4 compaction burst, domain class) temporarily restores super-linear scaling. Design: fit rolling 50-session power-law exponent; measure alpha before/after each structural innovation event; identify the cadence needed to keep alpha > 1.0. Observable: rolling alpha < 1.0 = sub-linear = structural innovation DUE. Artifact: L-393, ISO-8 extension (West's dual law). Cross-link: F-PHY1, F-PHY3, ISO-4, ISO-8.

- **F-PHY5**: Does the RG fixed-point interpretation of swarm quality metrics (Sharpe~0.80, yield~35%) hold across compaction events and domain seeding bursts? Stakes: if Sharpe and yield are truly scale-invariant (fixed points), they are the only reliable quality signals at any scale. If they drift, the swarm has no invariant quality measure. Method: compute Sharpe and session_yield per epoch (E1-E6); test for drift vs stability. Cross-link: ISO-14 (self-similarity), F-PHY4.

- **F-PHY6**: Is the symmetry-breaking cascade (ISO-4 × ISO-14 + directionality) a genuinely distinct structure worthy of ISO-18, or reducible to existing entries? (opened S340)
  **Stakes**: If distinct, cosmology becomes a top-5 atlas hub domain (11/17 ISOs) and the cascade pattern applies to swarm bootstrap, embryonic differentiation, linguistic diversification, and mathematical specialization (5+ domains). If reducible, the cascade is just "repeated ISO-4."
  **Method**: (1) Identify a formal property of the cascade NOT captured by ISO-4 or ISO-14 alone. Candidate: prerequisite ordering (transition N requires transition N-1's products). (2) Test: does removing directionality collapse the cascade to ISO-4 + ISO-14? If yes, reducible. If no, distinct. (3) Search for a counter-example: a symmetry-breaking cascade with no prerequisite structure (random order would refute directionality as essential).
  **Status**: S340 OPEN. ISO-18 candidate proposed. 5 domains identified. Sharpe ~3. Experiment: `experiments/physics/f-phy6-universe-genesis-s340.json`. L-486.
  **Cross-link**: F126 (atlas), ISO-4, ISO-14, F-PHY4.

## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|

## Notes
Physics here is a structural lens. We only keep mappings that yield measurable swarm controls.
