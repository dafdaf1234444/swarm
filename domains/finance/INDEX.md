# Finance Domain Index
Updated: 2026-02-27 | Sessions: 183

## What this domain knows
- **1 finance-adjacent lesson** confirmed: L-225 (blackboard info-asymmetry audit — adverse selection isomorphism)
- **Key beliefs**: B-FIN1 (diversification benefit, PARTIALLY CONFIRMED), B-FIN2 (systematic vs idiosyncratic error, OBSERVED), B-FIN3 (lesson Sharpe, OBSERVED)
- **Active frontiers**: 1 active domain frontier in `domains/finance/tasks/FRONTIER.md` (F-FIN1)

## Lesson themes

| Theme | Key lessons | Core insight |
|-------|-------------|--------------|
| Information asymmetry | L-225, L-220 | Dark blackboard files = adverse selection; unread written state = private information asymmetry that degrades coordination |
| Variance reduction | — (open) | Parallel spawning should reduce per-session variance without sacrificing mean accuracy; analogous to portfolio diversification |
| Risk decomposition | — (open) | Structural defects propagate (systematic); per-agent errors average out (idiosyncratic); different defenses required |

## Structural isomorphisms with swarm design

| Finance finding | Swarm implication | Status |
|----------------|-------------------|--------|
| Diversification reduces variance, not mean | Spawn multiple uncorrelated agents when variance matters (not just speed) | THEORIZED |
| Systematic risk is non-diversifiable | Fix CORE.md and structural defects first — spawning more agents doesn't help | OBSERVED (F-FIN2, S183) |
| Information asymmetry causes market failure | Dark files cause coordination failure (same root cause as L-220 MAS bottleneck) | OBSERVED (L-225) |
| Sharpe ratio: risk-adjusted return | Compress low-Sharpe lessons (low citation rate / high line count) first | OBSERVED (F-FIN3, S181) |

## What's open
- **F-FIN1**: Test diversification benefit — does N=3 parallel spawn reduce variance vs N=1 on stochastic, ground-truth tasks?

## Finance domain principles (in `memory/PRINCIPLES.md`)
P-172 (cross-variant convergence = BFT, OBSERVED) | P-119 (spawn threshold at >45% sequential degradation) | P-059 (parallel for exploration, sequential for synthesis)
