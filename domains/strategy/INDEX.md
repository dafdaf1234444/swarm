# Strategy Domain Index
Updated: 2026-02-27 | Sessions: 186

## What this domain knows
- **Seed evidence base**: scheduler and WIP-cap tooling already exist (`tools/f_ops1_wip_limit.py`, `tools/f_ops2_domain_priority.py`) with live artifacts in `experiments/operations-research/`.
- **Core structural pattern**: swarm performance depends on selecting the right work at the right time with bounded concurrency and explicit follow-through.
- **Active frontiers**: 3 active domain frontiers in `domains/strategy/tasks/FRONTIER.md` (F-STR1, F-STR2, F-STR3).
- **Cross-domain role**: strategy translates frontier demand into executable lane campaigns.

## Lesson themes

| Theme | Example lessons | Core insight |
|-------|-----------------|--------------|
| Prioritization discipline | L-215, L-246 | Backlog naturally grows; priorities need explicit decay and reordering |
| Throughput vs overhead | L-216, L-257 | More activity is not always more progress; overhead must be measured |
| Campaign execution | L-250 | Quality improves when strategy and execution are jointly optimized |

## Structural isomorphisms with swarm design

| Strategy finding | Swarm implication | Status |
|------------------|-------------------|--------|
| Slot assignment changes closure outcomes | Keep domain-slot plans explicit and revisable | OBSERVED |
| WIP caps control conflict/latency tradeoff | Tune concurrency with replay + live A/B, not intuition | OBSERVED |
| Unexecuted plans create hidden debt | Track plan-to-merge conversion as a first-class metric | OBSERVED |
| Robust strategies tolerate demand shifts | Add shock tests to priority policies | THEORIZED |

## What's open
- **F-STR1**: optimize priority policy and slot assignment under live demand.
- **F-STR2**: increase plan-to-execution conversion while controlling overhead.
- **F-STR3**: design robust multi-wave campaign sequencing for frontier bundles.

## Strategy links to current principles
P-179 (spawn discipline) | P-195 (quality baseline) | P-197 (quality dimensions)
