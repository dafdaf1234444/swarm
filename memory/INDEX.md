# Memory Index
Updated: 2026-02-27 | Sessions completed: 55

## Status: Active — 115 lessons, 14 beliefs (12 observed/2 theorized), 118 principles, entropy 0. S55: F102 RESOLVED — falsification conditions removed from all architectural beliefs (B1,B2,B3,B6,B7,B8,B11,B12,B16). 3-session test confirmed: no drift, evidence-labeling provides equivalent coverage. L-115. Repo synced (0 commits ahead). S54 additions: L-112 (colony/staleness), L-113 (spawn budget finite), L-114 (two-phase spawn).

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
tasks/HUMAN-QUEUE.md  — questions only a human can answer (check at session start)
memory/HUMAN.md       — human contributions and strategic directives
.claude/commands/     — /swarm command (fractal session protocol)
```

## Lessons: 115 (L-001–L-115)
For atomic rules: `memory/PRINCIPLES.md`. For full context: `memory/lessons/L-{NNN}.md`.

| Theme | Count | Lessons | Key insight |
|-------|-------|---------|-------------|
| Architecture | 13 | L-001,005,008,011,014,017,024,026,027,030,102,105,106 | Blackboard+stigmergy, folder structure, modes, atomic principles, redundancy, domain sharding (P-111), true swarming architecture (P-112), online distillation (P-113) |
| Protocols | 11 | L-002,004,006,012,013,016,018,019,023,028,096 | Distill, verify (3-S), correct, handoff, decay tracking; evidence > assertion; principles resist decay (P-098) |
| Strategy | 10 | L-003,007,009,015,020,021,022,031,038,104 | Phase ratios, genesis automation, diminishing returns, targeted fixes; tool dedup every ~25 sessions (P-109) |
| Complexity | 26 | L-010,025,029,033,035,037,039,041-046,048-050,052,054-056,058,059,062,063,066,077 | NK analysis, composite/burden, ratchet/anti-ratchet, DAG discipline, API shape, cross-language NK, monolith blind spot, multi-scale analysis |
| Evolution | 35 | L-032,034,036,040,047,051,053,057,060,061,064,065,067-076,078-086,090,094,095,112,113,114 | Spawn+evaluate, bulletins, evolve pipeline, stigmergy, belief variant A/B, recursive evolution, additive variants, Goodhart, hybrid vigor, dark matter, tool adoption, gen-2 hybrid overtake, R4 blackboard/stigmergy split, hot-file parallelism ceiling; repo staleness verification (P-117); spawn budget finite (P-118,L-113); two-phase spawn before partition (L-114) |
| Governance | 1 | L-087 | Governance stored outside CLAUDE.md becomes dark matter (P-092) |
| Generative | 2 | L-088,L-089 | Principle recombination 100% hit rate; dark matter 64-89% universal |
| Distributed Systems | 7 | L-091,L-092,L-093,L-097,L-098,L-099,L-103 | Error handling anti-patterns (12 examples), harvest R4 (280+ beliefs), NK-error correlation cycle-dependent (Go/Rust/Python, P-097); B13 observed; K_out predicts EH bugs in Go (r=0.652, P-110) |
| Meta / Governance | 8 | L-100,L-101,L-107,L-108,L-109,L-110,L-111,L-115 | Conversations are sessions (P-107); feedback loops break at action boundary (P-108); swarm advantage = f(domain_count × doc_sparsity): additive/transformative/multiplicative (P-114, L-110); genesis rules are redundancy network (P-115); pair skeptic+explorer on contested findings (P-116, L-111); observed beliefs don't need explicit falsification (L-115) |

## What to load when
| Doing...              | Read...                          |
|-----------------------|----------------------------------|
| Any session           | beliefs/CORE.md → this file      |
| A specific task       | + tasks/{task}.md                |
| Updating beliefs      | + beliefs/DEPS.md                |
| Learning from past    | + memory/PRINCIPLES.md or relevant lesson |
| Understanding history | git log, git diff                |
