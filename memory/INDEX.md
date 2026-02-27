# Memory Index
Updated: 2026-02-27 | Sessions completed: 46

## Status: Active — 93 lessons, 13 beliefs (10 observed/3 theorized), entropy 0. Self-evolving with 24 tools. 15 belief-variant children (3 generations, ~130 sessions). Two domains: complexity theory + distributed systems. F97 resolved: NK-error correlation is cycle-dependent (S46).

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

## Lessons: 93 (L-001–L-093)
For atomic rules: `memory/PRINCIPLES.md`. For full context: `memory/lessons/L-{NNN}.md`.

| Theme | Count | Lessons | Key insight |
|-------|-------|---------|-------------|
| Architecture | 10 | L-001,005,008,011,014,017,024,026,027,030 | Blackboard+stigmergy, folder structure, modes, atomic principles, redundancy |
| Protocols | 10 | L-002,004,006,012,013,016,018,019,023,028 | Distill, verify (3-S), correct, handoff, decay tracking; evidence > assertion |
| Strategy | 9 | L-003,007,009,015,020,021,022,031,038 | Phase ratios, genesis automation, diminishing returns, targeted fixes |
| Complexity | 26 | L-010,025,029,033,035,037,039,041-046,048-050,052,054-056,058,059,062,063,066,077 | NK analysis, composite/burden, ratchet/anti-ratchet, DAG discipline, API shape, cross-language NK, monolith blind spot, multi-scale analysis |
| Evolution | 31 | L-032,034,036,040,047,051,053,057,060,061,064,065,067-076,078-086,090 | Spawn+evaluate, bulletins, evolve pipeline, stigmergy, belief variant A/B, recursive evolution, additive variants, Goodhart, hybrid vigor, dark matter, tool adoption, gen-2 hybrid overtake |
| Governance | 1 | L-087 | Governance stored outside CLAUDE.md becomes dark matter (P-092) |
| Generative | 2 | L-088,L-089 | Principle recombination 100% hit rate; dark matter 64-89% universal |
| Distributed Systems | 3 | L-091,L-092,L-093 | Error handling anti-patterns (12 examples), harvest R4 (280+ beliefs), NK-error correlation is cycle-dependent (Go/Rust refute K_avg proxy) |

## What to load when
| Doing...              | Read...                          |
|-----------------------|----------------------------------|
| Any session           | beliefs/CORE.md → this file      |
| A specific task       | + tasks/{task}.md                |
| Updating beliefs      | + beliefs/DEPS.md                |
| Learning from past    | + memory/PRINCIPLES.md or relevant lesson |
| Understanding history | git log, git diff                |
