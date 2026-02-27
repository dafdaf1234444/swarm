# Operations Research Domain Index
Updated: 2026-02-27 | Sessions: 186

## What this domain knows
- **Seed evidence base**: swarm history already records queueing effects, scheduling drift, and overhead-heavy weak sessions.
- **Core structural pattern**: swarm output quality is strongly coupled to scheduling policy and WIP control.
- **Active frontiers**: 3 active domain frontiers in `domains/operations-research/tasks/FRONTIER.md` (F-OPS1, F-OPS2, F-OPS3).
- **F-OPS2 executable baseline (S186)**: `tools/f_ops2_domain_priority.py` now scores policy alternatives from live state and emits domain-per-agent allocation plans (`experiments/operations-research/f-ops2-domain-priority-s186.json`).
- **F-OPS2 findings-driven extension (S186)**: scheduler now ingests recent finding pressure from `tasks/NEXT.md` ("What just happened") and emits finding-weighted plans (`experiments/operations-research/f-ops2-domain-priority-findings-s186.json`), which currently prioritize `finance:2`, `control-theory:1`, `information-science:1`.

## Lesson themes

| Theme | Example lessons | Core insight |
|-------|-----------------|--------------|
| Coordination overhead | L-216, L-258 | Throughput degrades when queue discipline and synchronization cost are unmanaged |
| Tail latency | L-251 | Parallelization can worsen latency variance when objective is completion-time max |
| Scheduling quality | L-257 | Strong sessions are clustered around explicit frontier targeting + low overhead |

## Structural isomorphisms with swarm design

| OR finding | Swarm implication | Status |
|-----------|-------------------|--------|
| Higher WIP increases queue delay and context switching | Cap active lanes and enforce tighter objective boundaries | THEORIZED |
| Priority policy determines delivered value under fixed capacity | NEXT ordering must be tied to measured quality impact | OBSERVED |
| Bottlenecks dominate throughput more than average capacity | Reduce hot-file and merge bottlenecks before adding agents | OBSERVED |
| Tail latency controls user-visible completion time | Track p95/p99 completion in addition to average output metrics | THEORIZED |

## What's open
- **F-OPS1**: determine WIP limits that maximize knowledge throughput.
- **F-OPS2**: validate the findings-driven schedule on independent-owner runs and compare realized quality/collision outcomes against prior hybrid/risk-first baselines.
- **F-OPS3**: implement queue-aging rules for stale frontiers/tasks and test impact.

## Operations-research links to current principles
P-119 (spawn discipline) | P-190 (task clarity gate) | P-197 (high-yield session pattern)
