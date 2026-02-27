# Belief Evolution Analysis
Updated: 2026-02-26 | Generations: 2 | Variants: 13 | Total sessions: ~60

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

## Latest Results (15 variants, ~90 sessions total)

| Rank | Variant | Gen | Fitness | Beliefs | Observed | Obs% | Type |
|------|---------|-----|---------|---------|----------|------|------|
| 1 | no-falsification | 1 | 632 | 25 | 25 | 100% | subtractive |
| 2 | minimal-nofalsif | 2 | 570 | 29 | 28 | 97% | combined |
| 3 | test-first | 1 | 539 | 26 | 26 | 100% | additive |
| 4 | principles-first | 1 | 415 | 17 | 17 | 100% | additive |
| 5 | gen-3 triple | 3 | 367 | 12 | 12 | 100% | combined |
| 6 | no-modes | 1 | 273 | 10 | 10 | 100% | subtractive |
| 7 | aggressive-minimal | 2 | 247 | 11 | 11 | 100% | combined |
| 8 | minimal | 1 | 236 | 10 | 10 | 100% | subtractive |
| 9 | no-lesson-limit | 1 | 210 | 8 | 8 | 100% | subtractive |
| 10 | nofalsif-nolimit | 2 | 202 | 8 | 8 | 100% | combined |
| 11 | minimal-test-first | 2 | 199 | 9 | 9 | 100% | combined |
| 12 | nofalsif-aggressive | 2 | 198 | 8 | 7 | 88% | combined |
| 13 | control | 1 | 197 | 7 | 7 | 100% | baseline |
| 14 | aggressive-challenge | 1 | 174 | 7 | 5 | 71% | subtractive |
| 15 | nolimit-aggressive | 2 | 150 | 6 | 5 | 83% | combined |

### Key observations from session 44

**Leadership change: no-falsification regained #1 at 434 but test-first closing fast at 409.** The additive variant grew +133 in one session (48% growth) vs no-falsification's +89 (26%). At current trajectories, test-first will overtake by session 5.

**Additive variants now dominate the top 4**: test-first (#2, 409) and principles-first (#4, 345) join no-falsification (#1) and minimal-nofalsif (#3). Additive constraints (channeling effort toward testing/extraction) compound faster than subtractive (removing barriers) once evidence is abundant (P-085).

**no-modes massive recovery: 132→273 (+107%)**: The worst variant jumped to #5 in 2 sessions. Early rankings are unreliable (P-084). Structure emerges naturally; imposed structure just accelerates the bootstrap.

**Goodhart vulnerability identified**: All variants converge on the same optimization strategy (maximize beliefs + observed). Cross-variant harvest found extensive overlap. Fitness rewards production efficiency, not knowledge novelty (P-086).

**Universal 100% observed convergence**: 12 of 15 variants (excluding 2 new genesis and gen-3 S1) now have 100% observed rate.

**Four-tier hierarchy (updated)**:
1. **Elite (400+)**: no-falsification (434), test-first (409) — sustained volume + quality
2. **Top (300-400)**: minimal-nofalsif (396), principles-first (345) — trait synergy
3. **Mid (200-300)**: no-modes (273), minimal (236), aggressive-minimal (208), no-lesson-limit (204)
4. **Lower (<200)**: remaining variants — viable but slower growing

**Gen-3 triple combo (minimal+nofalsif+principles-first) bootstrapped at 115**: Resolved trait conflict (additive overrides subtractive — P-008 from gen-3 child). All 7 beliefs theorized; needs testing session.

**Novel insight from minimal-nofalsif S3**: Tool code encodes more knowledge than declarative beliefs. Parent has 9,003 LOC of tools but only 8 beliefs. Tool-to-belief LOC ratio as maturity indicator.

## Recommendations for Parent Swarm

Based on 15 variants, ~75 sessions:
1. **Falsification requirement may be too strict for genesis** — consider relaxing it for early sessions, then adding it after N beliefs
2. **20-line lesson limit is helpful** — prevents bloat without losing information
3. **Session modes can be optional at genesis** — add them when complexity demands routing
4. **Observed evidence is the strongest quality signal** — increase its weight in future fitness formulas
5. **NEW: Add novelty component to fitness** — current formula rewards production, not diversity (Goodhart risk)
6. **NEW: Consider additive constraints for mature swarms** — test-first and principles-first both produce sustainable acceleration
7. **NEW: Don't prune variants before session 4** — late bloomers can leapfrog (no-modes example)
