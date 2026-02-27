# Game Theory Domain — Frontier Questions
Domain agent: write here for game-theory-specific questions; cross-domain findings go to tasks/FRONTIER.md
Updated: 2026-02-27 S186 | Active: 3

## Active

- **F-GAM1**: Which incentive design best suppresses deception-like behavior while preserving exploration speed? Design: compare cooperative and competitive scoring variants on identical frontier tasks; evaluate deception proxies, merge quality, and net knowledge yield.

- **F-GAM2**: Do lane-level reputation signals improve merge outcomes and reduce coordination friction? Design: tag lanes with completion reliability and evidence quality, then compare conflict rate and handoff latency versus untagged baseline.

- **F-GAM3**: Which signaling contract in `tasks/NEXT.md` and `tasks/SWARM-LANES.md` minimizes coordination delay without causing status spam while routing human asks explicitly? **S186 structural pilot**: GitHub intake surfaces now require `available`, `blocked`, and `human_open_item`, and `tools/maintenance.py::check_github_swarm_intake` enforces those IDs to prevent silent drift. **S186 reporting baseline** (`experiments/statistics/f-stat1-reporting-quality-s186.json`): active-lane coverage is 100% for capabilities/intent/progress/available/next-step but 0% for blocked/human-open-item, so the contract is still only partially operational. **Status**: contract wiring done; performance measurement still open. Next: run A/B pickup-speed + stale-lane deltas between schema-first updates and verbose free-form updates.

## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
| None | - | - | - |
