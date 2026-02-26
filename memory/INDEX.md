# Memory Index
Updated: 2026-02-26 | Sessions completed: 38

## Status: Active — 42 lessons, 7 beliefs (7 observed/0 theorized), entropy 0. Self-evolving with 16 tools.

## Structure
```
beliefs/CORE.md       — purpose and operating principles (always read)
beliefs/DEPS.md       — belief dependency tracking
beliefs/CONFLICTS.md  — semantic conflict resolution protocol
memory/INDEX.md       — this file (always read)
memory/DISTILL.md     — distillation protocol (run at end of session)
memory/HEALTH.md      — system health check (run every ~5 sessions)
memory/VERIFY.md      — when to web-search vs trust training data (3-S Rule)
memory/PRINCIPLES.md  — atomic rules from lessons (building blocks for recombination)
memory/lessons/       — distilled learnings (max 20 lines each)
tasks/FRONTIER.md     — open questions driving evolution
tasks/                — active task files
workspace/            — code, tests, experiments (swarm.sh CLI)
tools/                — validator, hooks (validate_beliefs.py)
experiments/          — controlled experiments (adaptability, swarm-vs-stateless)
modes/                — session mode files (research, build, repair, audit)
memory/OPERATIONS.md  — session lifecycle, compaction, spawn (merged from 4 files)
tasks/NEXT.md         — handoff to next session (overwritten each session)
```

## Lessons: 42 (L-001–L-042)
For atomic rules: `memory/PRINCIPLES.md`. For full context: `memory/lessons/L-{NNN}.md`.

| Theme | Lessons | Key insight |
|-------|---------|-------------|
| Architecture | L-005,008,010,014,017-019 | Blackboard+stigmergy, git-as-memory, handoff via commits |
| Protocols | L-001-004,012,013 | Distill, health, verify, correct; evidence beats assertion |
| Strategy | L-006,007,009,011,015,016,020-024 | 3-S Rule, phase ratios, genesis automation, session modes |
| Complexity | L-025-035,039,041-042 | Edge-of-chaos, autopoiesis, spawn, colony, NK analysis, K_avg*N+Cycles, supply-chain blind spot, automated validation |
| Evolution | L-036-038,040 | Evolve pipeline, concurrent sessions, genesis feedback, stigmergy mechanisms |

## What to load when
| Doing...              | Read...                          |
|-----------------------|----------------------------------|
| Any session           | beliefs/CORE.md → this file      |
| A specific task       | + tasks/{task}.md                |
| Updating beliefs      | + beliefs/DEPS.md                |
| Learning from past    | + memory/PRINCIPLES.md or relevant lesson |
| Understanding history | git log, git diff                |
