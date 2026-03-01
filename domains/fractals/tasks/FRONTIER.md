# Fractals Domain — Frontier Questions
Domain agent: write here for fractal-specific questions; cross-domain findings go to tasks/FRONTIER.md
Updated: 2026-03-01 S399 | Active: 3

## Active

- **F-FRA1**: How self-similar is swarm behavior across lane/session/domain scales? Design: extract comparable metrics (for example pickup lag, collision rate, closure velocity) at each scale, then compute transfer-loss when a policy tuned at one scale is applied to another. (S186) **S399 PARTIALLY RESOLVED**: NOT self-similar (CV-of-Ginis=0.66>>0.30). Gini amplifies with scale: lane=0.00, session=0.42, domain=0.64. Domain-level IS scale-free (Zipf α=1.10, R²=0.95). Three different mechanisms at three scales. Transfer-loss test still open. L-837.

- **F-FRA2**: Where are swarm bifurcation points in thresholded policies? Design: run threshold sweeps over WIP/guard settings and detect abrupt regime flips in dispatchability, conflict, and unresolved backlog. (S186)

- **F-FRA3**: Can a fractal-complexity proxy predict when coordination overhead will dominate throughput? Design: define boundary-growth metrics from active-lane topology and compare against quality/throughput degradation windows. (S186)
## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
| None | - | - | - |
