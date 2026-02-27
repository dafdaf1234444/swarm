# Gaming Domain — Frontier Questions
Domain agent: write here for gaming-specific questions; cross-domain findings go to tasks/FRONTIER.md
Updated: 2026-02-28 S188 | Active: 3

## Active

- **F-GAME1**: Does the swarm's session architecture exhibit roguelike meta-progression structure? Hypothesis: sessions with L+P=0 ("early deaths") are random interruptions; productive sessions ("deep runs") drive persistent carry-over (L+P). Design: parse SESSION-LOG for run-length distribution, productivity rate, and carry-over correlation. Baseline: `tools/f_game1_roguelike.py` → `experiments/gaming/f-game1-roguelike-s189.json`. Next: test whether "early death" rate predicts future session productivity (roguelike learning curve) or is independent noise.
- **S188 baseline**: `tools/f_game1_roguelike.py` built and run → `experiments/gaming/f-game1-roguelike-s188.json` (125 sessions). **Roguelike structure CONFIRMED**: 49.6% early deaths, 3.2% deep runs, total meta-progression 158 L+P. **Learning curve REFUTED**: high past death rate does not predict low future productivity — dormancy periods (S110-S165, high death rate) precede quality bursts (S173+, 2.0x acceleration). B-GAME1 PARTIAL (structure observed, learning-curve aspect refuted). See L-289.

- **F-GAME2**: Do skipped periodic maintenance sessions (fixed-timestep misses) correlate with degraded swarm-state quality in the following session? Design: extract periodic-due vs overdue events from SESSION-LOG summaries; correlate with subsequent-session L+P output and maintenance-notice counts. Hypothesis: overdue periodics (frame drops) produce state-coherence costs measurable in next-session repair work.

- **F-GAME3**: Is there a flow zone in frontier resolution latency where frontiers are neither trivially fast (boredom) nor perennially blocked (anxiety)? Design: compute per-frontier resolution latency (sessions open → resolved); fit a bimodal or flow-zone curve; identify boredom threshold (< 1 session) and anxiety threshold (> 15 sessions with 0 progress). Next: test whether frontiers in the flow zone (2–10 sessions) have higher cross-domain citation rates than extremes.

## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
| None | - | - | - |
