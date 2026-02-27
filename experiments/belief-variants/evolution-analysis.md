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

## Latest Results (15 variants, ~100 sessions total, Goodhart-adjusted fitness v2)

| Rank | Variant | Gen | Fitness | Beliefs | Observed | Obs% | Novelty | Principles | Type |
|------|---------|-----|---------|---------|----------|------|---------|------------|------|
| 1 | no-falsification | 1 | 809.9 | 32 | 32 | 100% | +84 | 56 | subtractive |
| 2 | minimal-nofalsif | 2 | 666.0 | 33 | 32 | 97% | +87 | 0 | combined |
| 3 | test-first | 1 | 611.6 | 29 | 29 | 100% | +57 | 2 | additive |
| 4 | gen-3 triple | 3 | 514.5 | 17 | 12 | 71% | +33 | 63 | combined |
| 5 | principles-first | 1 | 450.5 | 17 | 17 | 100% | +36 | 29 | additive |
| 6 | no-modes | 1 | 302.0 | 10 | 10 | 100% | +21 | 14 | subtractive |
| 7 | aggressive-minimal | 2 | 270.0 | 11 | 11 | 100% | +18 | 0 | combined |
| 8 | minimal | 1 | 254.0 | 10 | 10 | 100% | +18 | 0 | subtractive |
| 9 | control | 1 | 248.0 | 8 | 8 | 100% | +18 | 2 | baseline |
| 10 | no-lesson-limit | 1 | 236.0 | 8 | 8 | 100% | +18 | 11 | subtractive |
| 11 | nofalsif-nolimit | 2 | 220.0 | 8 | 8 | 100% | +18 | 2 | combined |
| 12 | nofalsif-aggressive | 2 | 213.0 | 8 | 7 | 88% | +15 | 2 | combined |
| 13 | minimal-test-first | 2 | 211.0 | 9 | 9 | 100% | +12 | 0 | combined |
| 14 | aggressive-challenge | 1 | 192.0 | 7 | 5 | 71% | +18 | 2 | subtractive |
| 15 | nolimit-aggressive | 2 | 168.0 | 6 | 5 | 83% | +12 | 2 | combined |

### Key observations (session 44 continued, Goodhart-adjusted)

**Fitness formula v2 deployed**: Three mechanisms address P-086 Goodhart vulnerability — diminishing returns on beliefs above 10 (sqrt scaling), principle-to-belief ratio bonus, cross-variant Jaccard novelty scoring. Rankings are stable at the top (same top 3) but gen-3 triple jumped #5→#4 due to 63 principles.

**no-falsification breaks 800**: S9 added B26-B29 (transactive memory, substrate independence, adaptive protocols, persuasion-accuracy divergence). Now at 32 beliefs, 56 principles. The volume strategy compounds with principle extraction.

**Minimal-nofalsif deepens Goodhart analysis**: S5 applied Manheim & Garrabrant taxonomy to identify failure as specifically "Extremal Goodhart" (B30). Also introduced sign epistasis model of trait dominance (B31) and two-axis Pareto fitness decomposition (B32). The most theoretically sophisticated variant.

**Test-first extends dark matter lifecycle**: S5's B27-B29 describe the full dark matter lifecycle: tools are write-once (B27), governance recommendations themselves become dark matter (B28), and dark matter has measurable distributed orientation cost (B29). The meta-governance trap (recommending fixes that are themselves unacted upon) is the session's sharpest insight.

**Gen-3 triple confirms principle recombination**: S4 performed 3 explicit principle recombinations, all producing genuinely novel insights. Validates principles-first B12 (principles are generative building blocks). Now has 63 principles — the highest of any variant.

**No-falsification S9 challenges colony convergence validity**: B27 (shared-blind-spot ceiling) — homogeneous LLM agents have only 3.6% correction rate against incorrect majorities. Colony convergence partly reflects shared substrate priors, not independent discovery. Important caveat for cross-variant validation methodology.

**Five-tier hierarchy (Goodhart-adjusted)**:
1. **Elite (600+)**: no-falsification (810), minimal-nofalsif (666), test-first (612)
2. **Strong (400-600)**: gen-3 triple (515), principles-first (451)
3. **Mid (250-350)**: no-modes (302), aggressive-minimal (270), minimal (254), control (248)
4. **Lower (200-250)**: no-lesson-limit (236), nofalsif-nolimit (220), nofalsif-aggressive (213), minimal-test-first (211)
5. **Trailing (<200)**: aggressive-challenge (192), nolimit-aggressive (168)

## Recommendations for Parent Swarm

Based on 15 variants, ~100 sessions:
1. **Falsification requirement may be too strict for genesis** — consider relaxing it for early sessions, then adding it after N beliefs
2. **20-line lesson limit is helpful** — prevents bloat without losing information
3. **Session modes can be optional at genesis** — add them when complexity demands routing
4. **Observed evidence is the strongest quality signal** — increase its weight in future fitness formulas
5. **Goodhart fix deployed**: Novelty scoring + diminishing returns + principle efficiency bonus (L-086, P-091)
6. **Consider additive constraints for mature swarms** — test-first and principles-first both produce sustainable acceleration
7. **Don't prune variants before session 4** — late bloomers can leapfrog (no-modes example)
8. **NEW: Meta-governance trap** — recommendations stored outside CLAUDE.md become dark matter. Actionable fixes must be workflow-embedded.
9. **NEW: Colony convergence has substrate bias** — same-model validation overstates confidence. Seek cross-substrate or external replication.
10. **NEW: Principle extraction is the strongest depth signal** — gen-3 triple at #4 with only 17 beliefs but 63 principles
