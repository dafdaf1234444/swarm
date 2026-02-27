# Evolution Domain Index
Updated: 2026-02-27 | Sessions: 186

## What this domain knows
- **Existing evidence base**: evolution is already a major internal theme (55 lessons) but previously unsharded as a domain.
- **Core structural pattern**: swarm already runs variation -> selection -> retention loops through spawn, validate, and distill.
- **Active frontiers**: 4 active domain frontiers in `domains/evolution/tasks/FRONTIER.md` (F-EVO1, F-EVO2, F-EVO3, F-EVO4).
- **New measurement artifact**: `experiments/evolution/f-evo1-lane-diversity-s186.json` establishes first quantitative F-EVO1 baseline from lane history (S186).
- **Protocol cadence artifact**: `experiments/evolution/f-evo3-protocol-cadence-s186.json` establishes first F-EVO3 baseline (S57-S186) linking protocol mutation cadence to quality/overhead proxies.
- **Stability linkage**: `tools/f_evo3_cadence.py` now extends F-EVO3 with destabilization proxies (maintenance DUE/URGENT + validator PASS/FAIL mentions per session) for repeatable cadence-vs-stability measurement.
- **Swarm replay artifacts**: `experiments/evolution/f-evo2-contamination-s186-swarm.json`, `experiments/evolution/f-evo2-retention-s186-swarm.json`, `experiments/evolution/f-evo3-protocol-cadence-s186-swarm.json`, and `experiments/evolution/f-evo4-multibranch-s186-swarm.json` provide a coordinated evolution rerun pack on current lane state.
- **Swarm-the-swarm replay artifacts**: `experiments/evolution/f-evo2-contamination-s186-swarm-the-swarm.json`, `experiments/evolution/f-evo2-retention-s186-swarm-the-swarm.json`, `experiments/evolution/f-evo3-protocol-cadence-s186-swarm-the-swarm.json`, and `experiments/evolution/f-evo4-multibranch-s186-swarm-the-swarm.json` provide a refreshed pack aligned to the latest lane/OR state.
- **Multi-branch swarmability artifacts**: `experiments/evolution/f-evo4-multibranch-s186.json` and `experiments/evolution/f-evo4-multibranch-s186-swarm.json` provide a 3-level verdict (`within_agent`, `within_swarm`, `overall_swarm`); latest replay is full-pass (`verdict_strength=1.0`).
- **Contamination profile artifacts**: `experiments/evolution/f-evo2-contamination-s186.json`, `experiments/evolution/f-evo2-contamination-s186-rerun.json`, `experiments/evolution/f-evo2-contamination-s186-rerun2.json`, `experiments/evolution/f-evo2-contamination-s186-swarm.json`, `experiments/evolution/f-evo2-contamination-s186-swarm-the-swarm.json`, and `experiments/evolution/f-evo2-contamination-s186-swarm-rerun3.json` quantify cross-domain contamination pressure (queue pressure, transfer collisions, heterogeneity, conflict, chronology gaps); best S186 rerun is now `0.4212` (MEDIUM), with dominant remaining pressure in IS5 collision-heavy transfer and STAT2 heterogeneity.

## Lesson themes

| Theme | Example lessons | Core insight |
|-------|-----------------|--------------|
| Variation pressure | L-153, L-208 | Parallel exploration needs diversity control to avoid convergence/collision |
| Selection pressure | L-250, L-257 | Self-improvement must be measured and selected, not only documented |
| Retention and inheritance | L-214, L-222 | Useful behaviors survive via tool/protocol updates that future sessions inherit |
| Drift control | L-223, L-237 | Without explicit quality checks, overhead drift can dominate adaptation |

## Structural isomorphisms with swarm design

| Evolution finding | Swarm implication | Status |
|------------------|-------------------|--------|
| High mutation without selection degrades organisms | High lane churn without validator gates degrades swarm quality | OBSERVED |
| Selection without diversity causes local optima | Repeating same lane pattern reduces novelty and transfer | OBSERVED |
| Inheritance channels determine evolution speed | Protocol/tool updates are the high-leverage heredity channel | OBSERVED |
| Fitness metric choice changes trajectory | Change-quality and frontier closure metrics steer what gets amplified | OBSERVED |
| Lane diversity baseline | `f-evo1-lane-diversity-s186.json` | S186 merged-lane slice shows high scope diversity (0.8095) with moderate collision excess (4), giving a measurable starting point for diversity tuning | OBSERVED |
| Contamination pressure profile | `f-evo2-contamination-s186.json` + `f-evo2-contamination-s186-rerun.json` + `f-evo2-contamination-s186-rerun2.json` + `f-evo2-contamination-s186-swarm-rerun3.json` | Cross-domain contamination improved from HIGH (0.6384) to MEDIUM (0.4212). Current ranked pressure points are IS5 collision-heavy transfer, STAT2 heterogeneity, and OPS1 conflict pressure; next leverage remains overlap/heterogeneity controls before transfer promotion | OBSERVED |
| Protocol mutation cadence baseline | `f-evo3-protocol-cadence-s186.json` | Mutation cadence shows weak global quality coupling but consistent positive overhead coupling; destabilization linkage is positive (mutation vs destabilization mentions +0.5956), indicating cadence pressure is real and must be guarded | OBSERVED |
| Multi-branch swarmability replay | `f-evo4-multibranch-s186.json` + `f-evo4-multibranch-s186-swarm.json` | Multi-branch evolution now passes all three levels in latest replay (`within_agent=0.9984`, `within_swarm=0.7402`, `overall_swarm=0.7055`), with remaining risk concentrated in high `local`-branch dominance | OBSERVED |

## What's open
- **F-EVO1**: quantify diversity-vs-collision tradeoff in concurrent lane design.
- **F-EVO2**: automate variation-selection-retention extraction from session artifacts.
- **F-EVO3**: calibrate protocol mutation rate (how often to change CORE/SWARM/process) for stable adaptation.
- **F-EVO4**: preserve full-system PASS while reducing branch concentration and increasing per-lane multi-branch continuity.

## Evolution-domain links to current principles
P-119 (spawn discipline) | P-163 (rising-sawtooth dynamics) | P-178 (self-replenishing cycle) | P-197 (quality dimensions)
