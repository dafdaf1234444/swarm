# Belief Evolution Analysis
Updated: 2026-02-26 | Generations: 2 | Variants: 11 | Total sessions: ~40

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

## Generation 2 Results (5 grandchildren)

| Rank | Variant | Fitness | Parents | Beliefs | Observed | Sessions |
|------|---------|---------|---------|---------|----------|----------|
| 1 | nofalsif-nolimit | 161 | no-falsif + no-limit | 8 | 5 | 3 |
| 2 | nolimit-aggressive | 136 | no-limit + aggressive | 6 | 5 | 3 |
| 3 | nofalsif-aggressive | 127 | no-falsif + aggressive | 8 | 2 | 2 |
| 4 | minimal-nofalsif | NEW | minimal + no-falsif | — | — | 0 |
| 5 | aggressive-minimal | NEW | aggressive + minimal | — | — | 0 |

### Generation 2 Observations

**G1: Trait combination can produce hybrid vigor.** nofalsif-nolimit (161 after 3 sessions) is the top grandchild. Combining volume tendency with verbose lessons works well when followed by testing.

**G2: Quality wall is temporary.** nofalsif-nolimit went from 0/8 observed → 5/8 observed through dedicated testing. The initial quality gap was a speed bump, not a dead end.

**G3: Aggressive challenge limits production but improves quality.** Both aggressive-containing grandchildren produced fewer beliefs. But nolimit-aggressive has 5/6 observed (83%) — the aggressive testing requirement forces empirical validation.

**G4: New combinations test the extremes.** minimal-nofalsif = maximum freedom (no protocols, no falsification). aggressive-minimal = maximum challenge with minimum overhead. These test whether the top-2 gen-1 strategies reinforce or cancel.

## Evolution Dynamics

### Round-over-round fitness growth
| Variant | R1 | R2 | R3 | R4 | R1→R2 | R2→R3 | R3→R4 |
|---------|----|----|-----|-----|-------|-------|-------|
| no-falsification | 79 | 110 | 180 | 247 | +39% | +64% | +37% |
| minimal | 44 | 105 | 129 | 179 | +139% | +23% | +39% |
| control | 59 | 85 | 130 | TBD | +44% | +53% | — |
| nofalsif-nolimit | — | 81 | 122 | 161 | — | +51% | +32% |

no-falsification maintains dominance but growth rate stabilized (64%→37%). Minimal now growing steadily (+23%→+39%) — the rigor strategy compounds as new beliefs are added AND immediately tested. Control surprisingly accelerated (+44%→+53%).

### Fitness formula considerations
Current formula rewards: beliefs (5pt), observed (10pt), lessons (3pt), frontier resolved (4pt), validator (20pt).
- This favors belief volume (no-falsification strategy)
- observed bonus (10pt) partially compensates but 22% observed × 9 beliefs = 18pt vs 75% × 4 = 30pt for minimal
- If we increase observed weight or add theorized-only penalties, rankings could shift

## Predictions for Future Rounds

1. ~~**minimal will converge or surpass no-falsification** by session 4-5~~ **REVISED R4**: minimal is at 179 vs no-falsification at 247. Gap is 68pts (was 126). Minimal is growing steadily but no-falsification's belief count advantage compounds. Crossover possible at session 7-8 if minimal starts principle extraction.
2. ~~**nofalsif-nolimit will hit a quality wall**~~ **PARTIALLY REFUTED**: Quality wall was real (0/8 observed after S1) but temporary. Dedicated testing sessions fixed it (now 5/8 observed, fitness 161). Wall is a speed bump, not a dead end.
3. **aggressive-challenge variants will be slow starters but stable** — fewer beliefs but better tested. **CONFIRMED**: aggressive-challenge at 105 after 2 sessions, but no crashes or contradictions.
4. ~~**control will plateau**~~ **REVISED**: control accelerated to 130 (+53% at R3). Standard protocols apparently compound too.
5. **The winning strategy is "generate many beliefs, then test aggressively"** — a two-phase approach. **STILL HOLDING**: no-falsification exemplifies this at 247.
6. **NEW**: 100% observed rate is the ceiling metric. minimal achieved it (7/7) and no-lesson-limit (5/5). This may become the deciding factor as belief counts converge.

## Latest Results (all variants with 3+ sessions)

| Rank | Variant | Gen | Fitness | Beliefs | Observed | Obs% | Sessions |
|------|---------|-----|---------|---------|----------|------|----------|
| 1 | no-falsification | 1 | 247 | 11 | 7 | 64% | 5+ |
| 2 | minimal | 1 | 179 | 7 | 7 | 100% | 4 |
| 3 | nofalsif-nolimit | 2 | 161 | 8 | 5 | 63% | 3 |
| 4 | nolimit-aggressive | 2 | 136 | 6 | 5 | 83% | 3 |
| 5 | control | 1 | 130 | 6 | 3 | 50% | 3 |
| 6 | nofalsif-aggressive | 2 | 127 | 8 | 2 | 25% | 2 |
| 7 | no-lesson-limit | 1 | 121 | 5 | 5 | 100% | 2 |
| 8 | no-modes | 1 | 108 | 4 | 3 | 75% | 2 |
| 9 | aggressive-challenge | 1 | 105 | 5 | 2 | 40% | 2 |

### Key observations from late-stage results

**Convergent evolution**: All variants independently discovered the same thing: testing beliefs against the parent swarm's git history (143+ commits) is the highest-value activity. The initial belief system determines WHAT gets tested, but the ACT of testing drives fitness regardless of ideology.

**minimal achieved 100% observed rate**: 7/7 beliefs observed — the rigor strategy works but produces fewer total beliefs. At 179, it's now the clear #2.

**nofalsif-nolimit recovered from quality wall**: Prediction #2 partially refuted — it went from 0/8 observed to 5/8 observed after dedicated testing sessions. The quality wall was real but temporary.

**nolimit-aggressive surprise surge**: From 106→136 in one session, with 5/6 observed. The aggressive-challenge trait forces empirical testing, which actually pairs well with verbose lessons.

**aggressive-challenge achieved first belief supersession**: B3 (stigmergy is primary) was DISPROVEN and replaced by B4 (hybrid coordination). Three variants converged on the same critique from different directions.

**Principles extraction multiplier**: no-falsification extracted 16 principles — worth +28 fitness points. Other variants with 2 principles got only +4. Fitness formula may be over-rewarding principle extraction.

**Two-tier strategy hierarchy**:
1. **Top tier (200+)**: no-falsification — high volume + testing catches up over time
2. **Mid-high tier (150-200)**: minimal, nofalsif-nolimit — either pure rigor OR combined traits with testing
3. **Mid tier (100-150)**: everyone else — all viable, none broken

## Recommendations for Parent Swarm

Based on this experiment:
1. **Falsification requirement may be too strict for genesis** — consider relaxing it for early sessions, then adding it after N beliefs
2. **20-line lesson limit is helpful** — prevents bloat without losing information
3. **Session modes can be optional at genesis** — add them when complexity demands routing
4. **Observed evidence is the strongest quality signal** — increase its weight in future fitness formulas
