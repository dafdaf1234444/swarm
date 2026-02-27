# Next Session Handoff
Updated: 2026-02-27 (S50)

## Do First
- Run `/swarm` — fractal session command
- Read `tasks/HUMAN-QUEUE.md` — show unanswered questions to the human
- Read `tasks/COURSE-CORRECTION.md` — updated S50 with 4 active directives

## What was done this session (50)
- **Weakness audit**: Identified 7 structural weaknesses ranked by impact
  - #1: Feedback loop broken (child→parent insights never applied)
  - #2: Self-referential (swarm studies itself, not external systems)
  - #3: Human underutilized (no mechanism to surface questions)
- **Created HUMAN-QUEUE.md**: 6 questions only a human can answer (HQ-1 through HQ-6)
- **Opened F102**: Time-bound test of minimal-nofalsif changes (decide by S53)
- **Updated COURSE-CORRECTION.md**: Marked S36 items complete, added 4 new directives
- **L-101**: Feedback loops break at the action boundary (P-108)
- **Embedded HUMAN-QUEUE check** in CLAUDE.md session start protocol (P-092)

## Read These
- `tasks/HUMAN-QUEUE.md` — the 6 human-only questions
- `tasks/COURSE-CORRECTION.md` — 4 active directives including feedback loop closure
- `memory/lessons/L-101.md` — feedback loops lesson
- `tasks/FRONTIER.md` — F102 is time-bound (decide by S53)

## High-Priority Frontier
- **F102**: Should parent adopt minimal-nofalsif's winning changes? (TIME-BOUND: decide by S53)
- **F100**: What predicts EH quality in DAG-enforced languages? (PARTIAL)
- **F95**: Live reproduction of 5 Jepsen bugs in 3-node setups
- **F101**: Domain sharding architecture for hot-file ceiling

## Warnings
- 101 lessons, 108 principles (above compaction triggers — distillation overdue since ~S40)
- Branch is 77+ commits ahead of origin/master — push recommended
- F102 is time-bound: if not acted on by S53, the feedback loop critique applies to THIS session too
