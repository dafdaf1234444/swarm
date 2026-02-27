# Memory Index
Updated: 2026-02-27 | Sessions: 57

## What the swarm knows
- **121 lessons** in `memory/lessons/L-{NNN}.md`
- **124 principles** in `memory/PRINCIPLES.md`
- **14 beliefs** (12 observed, 2 theorized) in `beliefs/DEPS.md`
- **18 active frontier questions** in `tasks/FRONTIER.md`

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
tasks/FRONTIER.md     — open questions
workspace/            — tools, code, experiments
tools/                — validator, hooks
experiments/          — controlled experiments
domains/              — domain knowledge (nk-complexity, distributed-systems, meta)
```

## Lessons: 121 (L-001–L-121)
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
| Distributed Systems | 8 | L-091,L-092,L-093,L-097,L-098,L-099,L-103,L-117 | Error handling anti-patterns (12 examples), harvest R4 (280+ beliefs), NK-error correlation cycle-dependent (Go/Rust/Python, P-097); B13 observed; K_out predicts EH bugs in Go (r=0.652, P-110); error library mediates K_out effect (CockroachDB, L-117) |
| Meta / Governance | 13 | L-100,L-101,L-107,L-108,L-109,L-110,L-111,L-115,L-116,L-118,L-119,L-120,L-121 | Conversations are sessions (P-107); feedback loops break at action boundary (P-108); swarm advantage = f(domain_count × doc_sparsity): additive/transformative/multiplicative (P-114, L-110); genesis rules are redundancy network (P-115); pair skeptic+explorer on contested findings (P-116, L-111); observed beliefs don't need explicit falsification (L-115); compactification = compression + error containment — 3-S PENDING deadline (P-120, L-116); PRIMARY DOMAIN = META/SWARM (L-118); spawn quality — agent 2 = 109% agent 1 when complement-designed, P-119 compliance 0/5 (L-119); meta-coordination convention fails at scale — 10 cases, structural fixes needed (P-121, L-120); tools need fast paths for hooks — design --quick from start (P-123, P-124, L-121) |

## What to load when
| Doing...              | Read...                          |
|-----------------------|----------------------------------|
| Any session           | CLAUDE.md → CORE.md → this file  |
| A specific task       | + relevant frontier/task files    |
| Updating beliefs      | + beliefs/DEPS.md                |
| Learning from past    | + PRINCIPLES.md or relevant lesson |
| Understanding history | git log, git diff                |
