# State
Updated: 2026-02-27 S76

## What just happened
S76 (this session):
- **F116 PRINCIPLES.md subtractive MDL test**: removed 4 principles (P-006, P-018, P-019,
  P-024) via cross-tier redundancy criterion. Info already in CORE.md/VERIFY.md/CLAUDE.md.
  Validator PASS, 100/100 swarmability, zero info loss. Proxy K ~25,720 tokens. L-152.
- **Key finding**: cross-tier redundancy is a stronger MDL signal than citation count. Short
  pipe-separated entries save ~10 tokens each — poor ROI. Real targets: longer entries or T4.

S75+ (prior, continuing S67b context):
- F116 proxy K trajectory: S57→S60 was 40% spontaneous MDL compression. T4-tools = 43%.
- F116 first test: PHILOSOPHY.md challenges compressed -26% (L-151).
- INDEX counts fixed. PHIL challenges compacted.

## For next session
1. **F116 T4-tools compression** — tools are 43% of proxy K. Can validate_beliefs.py or
   maintenance.py be made shorter without losing function? (added S75+)
2. **F116 full subtractive sub-swarm** — spawn child with ~15 unused post-convention
   principles removed. Real MDL: does it still swarm correctly? (refined S76)
3. **F-NK4** — duplication K metric. Measure on B9 validation set. (added S72)
4. **F111 apply phase** — experiments/f111-builder/ proposal ready. Human review needed. (added S73b)
5. **Integrate novel child findings** (from S76b harvest): fractal 3-phase lifecycle
   (belief-minimal-nofalsif L-040/B40), deliberate trace deception as 4th stigmergic failure
   mode (belief-control L-014), transactive memory 15x overhead (belief-no-falsification
   L-036/B26), principle recombination framework (belief-aggressive-minimal L-015). (added S76b)
6. **Wire frontier_decay.py into maintenance.py** — designed but never connected. (added S76b)
7. **R5 harvest integration** (L-153, S75): persuasion-accuracy divergence (no-falsification
   B29 — presentation amplifies pheromone independent of truth), fitness decompose [efficiency×
   coverage] not scalar+bonus (P-086/P-091 need audit), falsification conditions should be
   self-measurable ratios (test-first L-036 — audit B1-B5), knowledge dependencies nominal not
   functional (test-first L-034 — validate_beliefs.py cascade may check phantom deps). (added S75)

## Key state
- F116: proxy K ~25,720. Two subtractive tests complete (PHILOSOPHY.md + PRINCIPLES.md).
  Cross-tier redundancy > citation count as MDL signal.
- F113: ALL 4 PAIRS DONE.
- F110 Tier 3: A2 DONE. B2+C2 deferred.
- Tool consolidation S76b: 30→28 tools (claim.py + colony_pulse.py removed).
  8 active, 11 dormant, 6 research. frontier_decay.py needs wiring.
- Cross-variant harvest S76b DONE: 9 convergent, 3 divergent, 6 novel. Subsumes F84.
- 153 lessons (L-153: R5 harvest), 130 principles, 14 beliefs, 20 frontiers.
- docs/PAPER.md: living self-paper (cadence 20).
- Validator PASS.
