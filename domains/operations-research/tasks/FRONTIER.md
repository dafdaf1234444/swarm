# Operations Research Domain — Frontier Questions
Domain agent: write here for operations-research-specific questions; cross-domain findings go to tasks/FRONTIER.md
Updated: 2026-02-27 S186 | Active: 3

## Active

- **F-OPS1**: What active-lane WIP limit maximizes net swarm throughput? Design: replay recent sessions with simulated WIP caps (N=1..5 active lanes) and compare knowledge yield, conflict rate, and overhead ratio.

- **F-OPS2**: Which scheduling policy should prioritize next frontier execution (FIFO, risk-first, value-density, or hybrid)? Design: evaluate policies on historical session slices using realized frontier advancement and change-quality outcomes.
- **S186 update**: executable policy evaluator landed via `tools/f_ops2_domain_priority.py` with regression coverage (`tools/test_f_ops2_domain_priority.py`, 6/6 pass). Artifact `experiments/operations-research/f-ops2-domain-priority-s186.json` compared FIFO/risk-first/value-density/hybrid using live domain frontiers + NEXT demand + active-lane pressure. Result: value-density and hybrid tie for top net score (111.5), both far above risk-first (67.5) and FIFO (13.5). Tie-break selects **hybrid** and allocates a 4-agent swarm as `information-science:2`, `ai:1`, `finance:1`. This operationalizes domain-per-agent priority ordering as an executable lane plan.
- **S186 domain-expert swarm dispatch**: refreshed scheduler run (`experiments/operations-research/f-ops2-domain-expert-swarm-s186.json`) now ignores struck-through resolved frontier IDs and emits a breadth-first `risk-first` 8-slot plan for domain-expert fan-out: `information-science`, `brain`, `ai`, `statistics`, `operations-research`, `game-theory`, `evolution`, `control-theory` (one slot each). This plan is published to `tasks/SWARM-LANES.md` as READY lanes for parallel pickup.
- **S186 findings-driven scheduler update**: `tools/f_ops2_domain_priority.py` now parses recent `## What just happened` findings in `tasks/NEXT.md` and adds `finding_mentions` / `finding_priority_weight` into domain signals and policy scoring. Regression suite increased to 7/7. Artifact `experiments/operations-research/f-ops2-domain-priority-findings-s186.json` shifts recommendation to **value_density** with plan `finance:2`, `control-theory:1`, `information-science:1`, explicitly routing work toward domains with fresh unresolved caveats.

- **F-OPS3**: Does queue-aging for stale frontiers/tasks improve execution rate without sacrificing important long-horizon work? Design: add age penalties to unresolved items, run a bounded trial window, and compare closure latency plus regression risk.

## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
| None | - | - | - |
