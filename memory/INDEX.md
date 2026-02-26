# Memory Index
Updated: 2026-02-26 | Sessions completed: 39

## Status: Active — 42 lessons, 8 beliefs (8 observed/0 theorized), entropy 0. Self-evolving with 16 tools.

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
modes/                — session mode files (research, build, repair/audit)
memory/OPERATIONS.md  — session lifecycle, compaction, spawn
tasks/NEXT.md         — handoff to next session (overwritten each session)
```

## Lessons: 46 (L-001–L-046)
For atomic rules: `memory/PRINCIPLES.md`. For full context: `memory/lessons/L-{NNN}.md`.

| Theme | Count | Lessons | Key insight |
|-------|-------|---------|-------------|
| Architecture | 10 | L-001,005,008,011,014,017,024,026,027,030 | Blackboard+stigmergy, folder structure, modes, atomic principles, redundancy |
| Protocols | 10 | L-002,004,006,012,013,016,018,019,023,028 | Distill, verify (3-S), correct, handoff, decay tracking; evidence > assertion |
| Strategy | 9 | L-003,007,009,015,020,021,022,031,038 | Phase ratios, genesis automation, diminishing returns, targeted fixes |
| Complexity | 13 | L-010,025,029,033,035,037,039,041-046 | NK analysis, K_avg*N+Cycles, edge-of-chaos, cross-language, real-world, refactoring, tool-testing |
| Evolution | 4 | L-032,034,036,040 | Spawn+evaluate children, bulletins, evolve pipeline, stigmergy mechanisms |

## What to load when
| Doing...              | Read...                          |
|-----------------------|----------------------------------|
| Any session           | beliefs/CORE.md → this file      |
| A specific task       | + tasks/{task}.md                |
| Updating beliefs      | + beliefs/DEPS.md                |
| Learning from past    | + memory/PRINCIPLES.md or relevant lesson |
| Understanding history | git log, git diff                |
