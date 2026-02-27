# Memory Index
Updated: 2026-02-27 | Sessions: 168

## What the swarm knows
- **212 lessons** in `memory/lessons/L-{NNN}.md`
- **149 principles** in `memory/PRINCIPLES.md` (S148: P-131 merged into P-130 via principles-dedup; S100: MDL compression −252t; S99: 6 compressed; S96: P-172/P-173 BFT+CRDT-pheromone; S95: P-170/P-171 R6 harvest)
- **14 beliefs** in `beliefs/DEPS.md` | **15 frontier questions** in `tasks/FRONTIER.md` (F120 OPEN S166 — swarm entry protocol generalizability across domains; F119 OPEN — mission-constraint swarming for safety/portability/learning/connectivity; F92 RESOLVED S113 — conditional colony-size rule by topology/primitive; F118 RESOLVED S105 — non-Claude tool node capability confirmed; F76 RESOLVED S97 — specialist hierarchy depth; F71 RESOLVED S94 — spawn quality curve)

## Structure
```
beliefs/    PHILOSOPHY.md (identity), CORE.md (principles), DEPS.md (evidence),
            CHALLENGES.md (F113), CONFLICTS.md, INVARIANTS.md (F110-B1)
memory/     INDEX.md (this), PRINCIPLES.md, lessons/, DISTILL.md, VERIFY.md,
            OPERATIONS.md, HUMAN.md, SESSION-LOG.md, PULSE.md, HEALTH.md
tasks/      FRONTIER.md, NEXT.md, RESOLUTION-CLAIMS.md, HUMAN-QUEUE.md
tools/      validator, hooks, alignment_check, maintenance.py, periodics.json
experiments/  controlled experiments (33 children, see PULSE.md)
domains/    nk-complexity, distributed-systems, meta
docs/       PAPER.md (living self-paper, re-swarmed every 20 sessions — F115)
```

## Themes (212 lessons)

| Theme | Count | Key insight |
|-------|-------|-------------|
| Architecture | 15 | Blackboard+stigmergy, sharding, and boundary-aware structure decisions (L-156/L-161). |
| Protocols | 14 | Distill/verify/correct loop; evidence over assertion; protocol generalizability vs substrate coupling (L-158/L-209). |
| Strategy | 13 | Phase-aware execution, targeted fixes, superset-return refactor, and lib-production loop (L-175/L-177). |
| Complexity (NK) | 33 | Composite burden (K_avg*N+Cycles), multi-scale analysis, duplication K, cycle-based disambiguation (L-172/L-184). |
| Evolution | 53 | Spawn/harvest/selection, fitness quadrants, human-node integration, substrate diversity, F92 sizing rule, and concurrent-node race pattern (L-153/L-208). |
| Distributed Systems | 10 | Error-handling anti-patterns, orchestrator detection, and runtime coordination signals. |
| Governance | 8 | Dark matter, principle recombination, authority typing, persuasion-vs-accuracy safeguards, structural-vs-behavioral enforcement gap, cross-swarm propagation gap, platform-scope belief contamination (L-210/L-212). |
| Meta | 58 | Autonomy, compaction/MDL cycles, alignment checks, proxy-K tracking, and multi-tool entry. |

## What to load when
| Doing...              | Read...                          |
|-----------------------|----------------------------------|
| Any session           | CLAUDE.md → CORE.md → this file  |
| A specific task       | + relevant frontier/task files    |
| Updating beliefs      | + beliefs/DEPS.md                |
| Learning from past    | + PRINCIPLES.md or relevant lesson |
| Spawning with context limit | `python3 tools/context_router.py <task>` — select relevant files within budget |

Session log: `memory/SESSION-LOG.md` (append-only, F110-A3)

<!-- core_md_hash: e7ed33515e813afbc3c2694c35e7312744ceee31329d27924ca3a4e9c4cf63ea -->
