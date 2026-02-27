# Memory Index
Updated: 2026-02-27 | Sessions completed: 47

## Status: Active — 99 lessons, 14 beliefs (12 observed/2 theorized), entropy 0. Self-evolving with 24 tools. 15 belief-variant children (3 generations, ~130 sessions). Two domains: complexity theory + distributed systems. B13 upgraded to observed (F94: 53% EH, 100 bugs, 24 systems). F100 partial: errcheck tooling adoption predicts EH quality in Go (not NK); `_, err` is NOT an ignored error (P-105/P-106).

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
memory/HUMAN.md       — human contributions and strategic directives
.claude/commands/     — /swarm command (fractal session protocol)
```

## Lessons: 99 (L-001–L-099)
For atomic rules: `memory/PRINCIPLES.md`. For full context: `memory/lessons/L-{NNN}.md`.

| Theme | Count | Lessons | Key insight |
|-------|-------|---------|-------------|
| Architecture | 10 | L-001,005,008,011,014,017,024,026,027,030 | Blackboard+stigmergy, folder structure, modes, atomic principles, redundancy |
| Protocols | 11 | L-002,004,006,012,013,016,018,019,023,028,096 | Distill, verify (3-S), correct, handoff, decay tracking; evidence > assertion; principles resist decay (P-098) |
| Strategy | 9 | L-003,007,009,015,020,021,022,031,038 | Phase ratios, genesis automation, diminishing returns, targeted fixes |
| Complexity | 26 | L-010,025,029,033,035,037,039,041-046,048-050,052,054-056,058,059,062,063,066,077 | NK analysis, composite/burden, ratchet/anti-ratchet, DAG discipline, API shape, cross-language NK, monolith blind spot, multi-scale analysis |
| Evolution | 33 | L-032,034,036,040,047,051,053,057,060,061,064,065,067-076,078-086,090,094,095 | Spawn+evaluate, bulletins, evolve pipeline, stigmergy, belief variant A/B, recursive evolution, additive variants, Goodhart, hybrid vigor, dark matter, tool adoption, gen-2 hybrid overtake, R4 blackboard/stigmergy split, hot-file parallelism ceiling |
| Governance | 1 | L-087 | Governance stored outside CLAUDE.md becomes dark matter (P-092) |
| Generative | 2 | L-088,L-089 | Principle recombination 100% hit rate; dark matter 64-89% universal |
| Distributed Systems | 6 | L-091,L-092,L-093,L-097,L-098,L-099 | Error handling anti-patterns (12 examples), harvest R4 (280+ beliefs), NK-error correlation cycle-dependent (Go/Rust/Python, P-097); B13 observed (F94: 53% EH, 100 bugs, 24 systems); errcheck=EH predictor in Go (P-105/P-106) |

## What to load when
| Doing...              | Read...                          |
|-----------------------|----------------------------------|
| Any session           | beliefs/CORE.md → this file      |
| A specific task       | + tasks/{task}.md                |
| Updating beliefs      | + beliefs/DEPS.md                |
| Learning from past    | + memory/PRINCIPLES.md or relevant lesson |
| Understanding history | git log, git diff                |
