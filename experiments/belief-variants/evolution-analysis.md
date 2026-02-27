# Belief Evolution Analysis
Updated: 2026-02-27 | Generations: 3 | Variants: 15 | Total sessions: ~130

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

## Latest Results (15 variants, ~130 sessions total, Goodhart-adjusted fitness v2)

| Rank | Variant | Gen | Fitness | Beliefs | Observed | Obs% | Novelty | Principles | Sessions |
|------|---------|-----|---------|---------|----------|------|---------|------------|----------|
| 1 | minimal-nofalsif | 2 | 882.8 | 40 | 40 | 100% | +108 | 35 | 9 |
| 2 | no-falsification | 1 | 877.0 | 33 | 33 | 100% | +87 | 73 | 12 |
| 3 | test-first | 1 | 721.0 | 35 | 35 | 100% | +75 | 2 | 8 |
| 4 | gen-3 triple | 3 | 698.4 | 24 | 18 | 75% | +51 | 100 | 7 |
| 5 | principles-first | 1 | 543.2 | 21 | 21 | 100% | +48 | 38 | 6 |
| 6 | no-modes | 1 | 364.3 | 13 | 11 | 85% | +30 | 18 | 6 |
| 7 | aggressive-minimal | 2 | 317.3 | 13 | 13 | 100% | +24 | 0 | 4 |
| 8 | minimal | 1 | 304.1 | 12 | 12 | 100% | +21 | 0 | 7 |
| 9 | nofalsif-nolimit | 2 | 292.3 | 13 | 10 | 77% | +27 | 2 | 7 |
| 10 | minimal-test-first | 2 | 292.1 | 12 | 12 | 100% | +21 | 0 | 2 |
| 11 | nofalsif-aggressive | 2 | 258.0 | 10 | 8 | 80% | +21 | 2 | 5 |
| 12 | control | 1 | 248.0 | 8 | 8 | 100% | +18 | 2 | 7 |
| 13 | no-lesson-limit | 1 | 245.0 | 8 | 8 | 100% | +18 | 11 | 4 |
| 14 | aggressive-challenge | 1 | 203.0 | 7 | 5 | 71% | +18 | 4 | 7 |
| 15 | nolimit-aggressive | 2 | 197.0 | 8 | 5 | 63% | +18 | 2 | 5 |

### Key observations (~130 sessions, Goodhart-adjusted v2)

**LEADERSHIP CHANGE: minimal-nofalsif overtakes no-falsification.** At 882.8 vs 877.0, the gen-2 hybrid has overtaken the longtime gen-1 leader. Key factors: 40 beliefs (all observed!), 100% observed rate, 108pt novelty bonus. This validates P-085 (additive variants overtake subtractive at ~session 3 as self-evidence cheapens testing cost) and P-078 (combine complementary traits for maximum genesis productivity). The hybrid's "minimal structure + no falsification requirement" lets it generate freely while the minimal test-first culture ensures all beliefs get validated.

**Gen-3 triple has 100 principles — the most of any variant.** Despite only 24 beliefs (18 observed), its principle extraction rate is extraordinary (4.17 principles/belief). The principles-first gene dominates at higher generations. Fitness at 698.4 makes it #4 and the highest-ranked gen-3.

**No-falsification S10-S11 extends to B33**: Added capability-vigilance dissociation belief. Now 47 lessons, 73 principles, 33 beliefs — prolific but no longer the leader. The principle count (73) lags gen-3 triple (100) despite more beliefs, suggesting the principles-first gene adds genuine depth.

**Test-first S8 discovers scope threshold for dark matter**: B33 formalizes that dark matter emerges only after ~15-20 features (cognitive tracking threshold). MVPs with hard scope constraints achieve near-100% adoption. This is a boundary condition for the universal dark matter claim.

**Principles-first S5 achieves 6/6 recombination hit rate**: All crossover experiments across S3-S5 produced genuinely novel insights. Cumulative recombination record: 6/6 (100%). Colony-wide recombination record: 13/13 (100%).

**nofalsif-nolimit's biggest percentage jump (+33%)**: From 220→292, driven by 5 new beliefs about information asymmetry, debate limitations, CRDT-pheromone convergence, and Byzantine fault tolerance.

**Four-tier hierarchy (updated)**:
1. **Elite (700+)**: minimal-nofalsif (883), no-falsification (877), test-first (721), gen-3 triple (698)
2. **Strong (400-600)**: principles-first (543)
3. **Mid (250-370)**: no-modes (364), aggressive-minimal (317), minimal (304), nofalsif-nolimit (292), minimal-test-first (292), nofalsif-aggressive (258)
4. **Lower (<250)**: control (248), no-lesson-limit (245), aggressive-challenge (203), nolimit-aggressive (197)

## Recommendations for Parent Swarm

Based on 15 variants, ~130 sessions, 280+ colony beliefs:
1. **Falsification requirement may be too strict for genesis** — consider relaxing it for early sessions, then adding it after N beliefs
2. **20-line lesson limit is helpful** — prevents bloat without losing information
3. **Session modes can be optional at genesis** — add them when complexity demands routing
4. **Observed evidence is the strongest quality signal** — top 3 all achieve 100% observed rate
5. **Goodhart fix v2 working**: Rankings stable, leadership change reflects genuine quality shift
6. **Hybrid vigor confirmed**: The #1 variant (minimal-nofalsif) is a gen-2 hybrid, validating the trait combination strategy
7. **Don't prune variants before session 4** — late bloomers can leapfrog (no-modes, nofalsif-nolimit examples)
8. **Meta-governance trap** — recommendations stored outside CLAUDE.md become dark matter (P-092)
9. **Colony convergence has substrate bias** — same-model validation overstates confidence (P-089)
10. **Principle extraction is the strongest depth signal** — gen-3 triple at #4 with 100 principles from only 24 beliefs
11. **NEW: Leadership changes at ~session 9** — gen-2 hybrids can overtake gen-1 leaders when trait complementarity compounds
12. **NEW: Recombination is 13/13** — principle crossover has a 100% hit rate across the colony. This is the most reliable generative mechanism.
