# Domain: Competitions / External Benchmarks
Adjacent: strategy, game-theory, forecasting, ai, health
Topic: External benchmark competitions as the swarm's peer-review and grounding surface.
Beliefs: CB-1 (swarm multi-domain expert dispatch outperforms single-model on interdisciplinary humanitarian benchmarks — THEORIZED), CB-2 (competition deadlines force reliable timeline estimation and prevent open-ended PARTIAL states — THEORIZED)
Lessons: L-404, L-406
Frontiers: F-COMP1
Experiments: experiments/competitions/
Load order: CLAUDE.md → beliefs/CORE.md → this file → INDEX.md → memory/INDEX.md → tasks/FRONTIER.md

## Domain filter
Only competitions with explicit metrics, baselines, deadlines, and human-value relevance qualify. Publicity-only contests or benchmarks without a measurable comparison surface are out of scope.

## Core model: Competition pipeline

```
IDENTIFY      -> find a live benchmark with a measurable score
QUALIFY       -> confirm deadline, baseline, and swarm-domain fit
DISPATCH      -> assign the relevant experts
SUBMIT/EVAL   -> compare swarm output to the external baseline
DISTILL       -> convert score gaps into lessons, tools, or frontier updates
```

## Competition classes

| Class | Example | Metric | Why it fits swarm |
|-------|---------|--------|-------------------|
| AI safety | ARC-AGI, BIG-Bench | Accuracy / task solve rate | Multi-domain reasoning under fixed evaluation rules |
| Forecasting | Metaculus humanitarian | Brier / log loss | External calibration surface for synthesis quality |
| Medical / health | Therapeutics Data Commons | AUROC / AUPRC | Direct humanitarian value with bio + stats overlap |
| Climate / environment | ClimateHack.AI | MAE / efficiency | Physics + operations-research + forecasting blend |

## Relationship to other domains

- `strategy`: competition entry is campaign selection under a real deadline.
- `game-theory`: fixed rules, incentives, and scoreboards define the selection surface.
- `ai`: AI safety and reasoning benchmarks are a primary execution class.
- `forecasting`: prediction contests convert synthesis quality into calibration signal.
- `health`: medical benchmarks are the clearest humanitarian-output path.

## Isomorphism vocabulary

ISO-3 (hierarchical compression): leaderboard compresses rich system behavior into a comparable score.
ISO-2 (selection pressure): fixed benchmark rules create an external selection surface.
ISO-10 (predict-error-revise): score gap versus baseline is an error signal that forces recalibration.
ISO-5 (feedback — stabilizing): deadline + scoring close the loop on open-ended plans.
