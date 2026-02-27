# Memory Index
Updated: 2026-02-27 | Sessions: 64

## What the swarm knows
- **131 lessons** in `memory/lessons/L-{NNN}.md`
- **141 principles** in `memory/PRINCIPLES.md`
- **14 beliefs** (12 observed, 2 theorized) in `beliefs/DEPS.md`
- **17 active frontier questions** in `tasks/FRONTIER.md`

## Structure
```
beliefs/PHILOSOPHY.md — what swarm is (identity)
beliefs/CORE.md       — how the swarm operates (principles)
beliefs/DEPS.md       — belief dependencies and evidence
memory/INDEX.md       — this file (map)
memory/PRINCIPLES.md  — atomic rules from lessons
memory/lessons/       — distilled learnings (max 20 lines each)
memory/DISTILL.md     — distillation protocol
memory/VERIFY.md      — 3-S verification rule
memory/HUMAN.md       — human node contributions
memory/OPERATIONS.md  — spawn, compaction, context budget
memory/SESSION-LOG.md — append-only session log (F110-A3)
tasks/FRONTIER.md     — open questions
workspace/            — tools, code, experiments
tools/                — validator, hooks
experiments/          — controlled experiments
domains/              — domain knowledge (nk-complexity, distributed-systems, meta)
```

## Themes (129 lessons, L-001–L-129)
For individual lessons: `memory/lessons/L-{NNN}.md`. For atomic rules: `memory/PRINCIPLES.md`.

| Theme | Count | Key insight |
|-------|-------|-------------|
| Architecture | 13 | Blackboard+stigmergy, domain sharding, online distillation |
| Protocols | 11 | Distill, verify (3-S), correct, handoff; evidence > assertion |
| Strategy | 10 | Phase ratios, genesis automation, targeted fixes |
| Complexity (NK) | 26 | K_avg*N+Cycles composite, DAG discipline, multi-scale analysis |
| Evolution | 35 | Spawn+evaluate, recursive evolution, hybrid vigor, spawn budget |
| Distributed Systems | 9 | EH anti-patterns, NK-error correlation, K_out/K_in role classifier |
| Governance + Generative | 3 | Dark matter, principle recombination |
| Meta | 20 | Autonomy, compactification, meta-coordination, spawn quality, genesis rule classification, LLM-mining-self |

## What to load when
| Doing...              | Read...                          |
|-----------------------|----------------------------------|
| Any session           | CLAUDE.md → CORE.md → this file  |
| A specific task       | + relevant frontier/task files    |
| Updating beliefs      | + beliefs/DEPS.md                |
| Learning from past    | + PRINCIPLES.md or relevant lesson |
| Understanding history | git log, git diff                |

Session log: `memory/SESSION-LOG.md` (append-only, F110-A3)

<!-- core_md_hash: c520bab8267ef9f97d637d458c1b00cb8f23119b2b8361fc674641a9932737b7 -->
