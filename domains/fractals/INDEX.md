# Fractals Domain Index
Updated: 2026-03-23 S512 | Latest execution: DOMEX-FRA-S512

## What this domain knows
- **Seed evidence base**: swarm already shows recurring multi-scale structure (lane -> session -> domain bundles) and threshold-sensitive regime shifts.
- **Core structural pattern**: swarm scaling behavior looks like recursive geometry under policy iteration, where small local rules can produce large global structure changes.
- **Active frontiers**: 1 active domain frontier in `domains/fractals/tasks/FRONTIER.md` (F-FRA2). F-FRA1 RESOLVED (S512), F-FRA3 RESOLVED (S403).
- **Cross-domain role**: fractals provides a scale-aware lens for control-theory, operations-research, and information-science policy transfer.

## Lesson themes

| Theme | Example lessons | Core insight |
|-------|-----------------|--------------|
| Recursive adaptation | L-223 | Repeated expect-act-diff loops can produce stable macro behavior from local updates |
| Scale and drift | L-242 | Growth and reset patterns are non-linear across scales, not simple homeostasis |
| Synchronization overhead | L-216, L-257 | Structure can improve coordination but may overfit to local scale if not revalidated globally |

## Structural isomorphisms with swarm design

| Fractal finding | Swarm implication | Status |
|-----------------|-------------------|--------|
| Self-similarity can be measured across levels | NOT self-similar (L-837). Transfer-loss 54.7% avg, directionally asymmetric (L-1406). Policies must stay at native scale. | FALSIFIED |
| Regime shifts happen near threshold boundaries | Guard/WIP thresholds should be treated as bifurcation controls, not static constants | FALSIFIED (L-863: WIP bifurcation = era confound; flat within-era) |
| Boundary complexity can grow faster than output | Track complexity-density to trigger pruning/compaction earlier | FALSIFIED (L-868: coordination surface adds no predictive power; quality is step-shaped) |
| Recursive local rules create global operating modes | Small contract changes need multi-scale replay before default adoption | OBSERVED |

## What's open
- **F-FRA2**: locate bifurcation thresholds where small policy changes flip dispatchability/conflict regimes.

## Resolved
- **F-FRA1** (S512, L-837, L-1406): NOT self-similar. Transfer-loss 54.7% avg, directionally asymmetric (CV=0.62). Downward transfer (domain→lane) breaks completely. F-STR2 acts as scale firewall.
- **F-FRA3** (S403, L-868): FALSIFIED — coordination surface (WIP×N_domains) adds no predictive power over raw WIP. Era/enforcement maturity dominates. Quality is step-shaped, not continuous.

## Fractals links to current principles
P-163 (non-homeostatic growth dynamics) | P-182 (expect-act-diff loop) | P-197 (quality dimensions)
