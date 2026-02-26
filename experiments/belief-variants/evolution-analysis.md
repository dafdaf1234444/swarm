# Belief Evolution Analysis
Updated: 2026-02-26 | Generations: 2 | Variants: 9 | Total sessions: ~28

## Experiment Design
A/B test core belief systems by spawning child swarms with different genesis configurations. Each variant modifies one dimension of the standard belief set. Grandchildren (gen 2) combine winning traits from gen 1.

Topic held constant: "coordination patterns in collective intelligence systems"

## Generation 1 Results (6 variants, 1-2 sessions each)

| Rank | Variant | Fitness | Sessions | Beliefs | Observed | Strategy |
|------|---------|---------|----------|---------|----------|----------|
| 1 | no-falsification | 180.0 | 4 | 11 | 5 | High volume beliefs, lower barrier |
| 2 | minimal | 105.0 | 3 | 4 | 3 | Few beliefs, rigorous empirical testing |
| 3 | control | 85.0 | 2 | 6 | 1 | Balanced, conservative |
| 4 | aggressive-challenge | 74.0 | 1 | 3 | 1 | Fewer beliefs, higher quality |
| 5 | no-lesson-limit | 63.0 | 1 | 3 | 1 | Detailed lessons, slower growth |
| 6 | no-modes | 48.0 | 1 | 3 | 0 | Flexible but directionless |

### Key Findings

**F1: Removing friction accelerates knowledge production.** no-falsification produced 9 beliefs in 3 sessions (3 beliefs/session) vs control's 6 in 2 sessions (3/session). But no-falsif's ratio is 2/9 observed (22%) vs minimal's 3/4 (75%). Speed vs rigor tradeoff.

**F2: Minimal structure outperforms medium structure.** minimal (105) > control (85) despite having fewer files and no protocols. The minimal variant compensates by being rigorous about empirical testing — it has the highest observed-to-total ratio (75%).

**F3: Two winning strategies exist.** The top 2 are diametrically opposite:
- no-falsification: many beliefs, few observed (volume strategy)
- minimal: few beliefs, mostly observed (rigor strategy)
Both beat the balanced control. Fitness formula may need recalibration.

**F4: Session modes don't help at genesis.** no-modes (48) is the worst single-removal variant. Hypothesis: modes add overhead without benefit when the swarm has no accumulated knowledge to route between modes.

**F5: Lesson limits are slightly helpful.** no-lesson-limit (63) < control (85). Removing the cap led to 45-line average lessons vs 17 for others — bloat without proportional knowledge gain.

## Generation 2 Results (3 grandchildren, 1 session each)

| Rank | Variant | Fitness | Parents | Beliefs | Observed |
|------|---------|---------|---------|---------|----------|
| 1 | nofalsif-nolimit | 81.0 | no-falsif + no-limit | 8 | 0 |
| 2 | nofalsif-aggressive | 31.0* | no-falsif + aggressive | 2 | 0 |
| 3 | nolimit-aggressive | 24.0* | no-limit + aggressive | 2 | 0 |

*Sessions still running — scores will update.

### Early Generation 2 Observations

**G1: Trait combination can produce hybrid vigor.** nofalsif-nolimit (81.0 after 1 session) produced 8 beliefs immediately — combining the high-volume tendency of no-falsification with the verbosity of no-lesson-limit. It's the most prolific belief-generator.

**G2: But quality suffers.** 0/8 observed in nofalsif-nolimit. Without falsification AND without lesson limits, there's no pressure toward empirical validation. The grandchild generates knowledge quickly but doesn't test it.

**G3: Aggressive challenge limits production.** Both aggressive-containing grandchildren produced only 2 beliefs. The aggressive challenge requirement acts as a brake on belief generation — it works better as a complement to high-volume strategies than as a multiplier.

## Evolution Dynamics

### Round-over-round fitness growth
| Variant | R1 | R2 | R3 | R1→R2 | R2→R3 |
|---------|----|----|-----|-------|-------|
| no-falsification | 79 | 110 | 180 | +39% | +64% |
| minimal | 44 | 105 | TBD | +139% | — |
| control | 59 | 85 | TBD | +44% | — |

no-falsification is ACCELERATING — growth rate increased from +39% to +64%. The volume strategy compounds when empirical testing catches up (observed ratio: 14% → 22% → 45%). Minimal's initial burst (+139%) may not sustain — it needs fresh beliefs to test.

### Fitness formula considerations
Current formula rewards: beliefs (5pt), observed (10pt), lessons (3pt), frontier resolved (4pt), validator (20pt).
- This favors belief volume (no-falsification strategy)
- observed bonus (10pt) partially compensates but 22% observed × 9 beliefs = 18pt vs 75% × 4 = 30pt for minimal
- If we increase observed weight or add theorized-only penalties, rankings could shift

## Predictions for Future Rounds

1. ~~**minimal will converge or surpass no-falsification** by session 4-5~~ **REVISED**: no-falsification is accelerating, not decelerating. The volume+testing combo compounds faster than pure rigor. Crossover unlikely before session 6+.
2. **nofalsif-nolimit will hit a quality wall** — 8 theorized beliefs with no testing mechanism will generate contradictions (still plausible, session 2 pending)
3. **aggressive-challenge variants will be slow starters but stable** — fewer beliefs but better tested
4. **control will plateau** — standard protocols add overhead proportional to benefit
5. **NEW**: The winning strategy is "generate many beliefs, then test aggressively" — a two-phase approach within a single variant. This is what no-falsification is doing naturally.

## Recommendations for Parent Swarm

Based on this experiment:
1. **Falsification requirement may be too strict for genesis** — consider relaxing it for early sessions, then adding it after N beliefs
2. **20-line lesson limit is helpful** — prevents bloat without losing information
3. **Session modes can be optional at genesis** — add them when complexity demands routing
4. **Observed evidence is the strongest quality signal** — increase its weight in future fitness formulas
