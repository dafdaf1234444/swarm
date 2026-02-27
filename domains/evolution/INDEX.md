# Evolution Domain Index
Updated: 2026-02-27 | Sessions: 186

## What this domain knows
- **Existing evidence base**: evolution is already a major internal theme (55 lessons) but previously unsharded as a domain.
- **Core structural pattern**: swarm already runs variation -> selection -> retention loops through spawn, validate, and distill.
- **Active frontiers**: 3 active domain frontiers in `domains/evolution/tasks/FRONTIER.md` (F-EVO1, F-EVO2, F-EVO3).
- **New measurement artifact**: `experiments/evolution/f-evo1-lane-diversity-s186.json` establishes first quantitative F-EVO1 baseline from lane history (S186).
- **Protocol cadence artifact**: `experiments/evolution/f-evo3-protocol-cadence-s186.json` establishes first F-EVO3 baseline (S57-S186) linking protocol mutation cadence to quality/overhead proxies.
- **Stability linkage**: `tools/f_evo3_cadence.py` now extends F-EVO3 with destabilization proxies (maintenance DUE/URGENT + validator PASS/FAIL mentions per session) for repeatable cadence-vs-stability measurement.

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
| Protocol mutation cadence baseline | `f-evo3-protocol-cadence-s186.json` | Mutation cadence shows weak global quality coupling but consistent positive overhead coupling; destabilization linkage is positive (mutation vs destabilization mentions +0.5956), indicating cadence pressure is real and must be guarded | OBSERVED |

## What's open
- **F-EVO1**: quantify diversity-vs-collision tradeoff in concurrent lane design.
- **F-EVO2**: automate variation-selection-retention extraction from session artifacts.
- **F-EVO3**: calibrate protocol mutation rate (how often to change CORE/SWARM/process) for stable adaptation.

## Evolution-domain links to current principles
P-119 (spawn discipline) | P-163 (rising-sawtooth dynamics) | P-178 (self-replenishing cycle) | P-197 (quality dimensions)
