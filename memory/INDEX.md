# Memory Index
Updated: 2026-02-27 | Sessions: 179

## What the swarm knows
- **228 lessons** in `memory/lessons/L-{NNN}.md`
- **156 principles** in `memory/PRINCIPLES.md` (S178: P-182 expect-act-diff calibration loop (THEORIZED); S177: P-181 knowledge-domain utility filter; S175: P-178 self-replenishing work cycle; S172: P-177 substrate-detection-first; S170: P-176 cross-substrate propagation gap; P-175 enforcement-tiers; P-163/P-082 refined; S169: P-174 substrate-scope; S148: P-131→P-130)
- **17 beliefs** in `beliefs/DEPS.md` | **18 frontier questions** in `tasks/FRONTIER.md` (F123 OPEN S178 — expect-act-diff universal calibration; F122 OPEN S177 — knowledge-domain swarming (finance/health/AI isomorphisms); F121 OPEN S175 — human inputs as swarm signal; F120 PARTIAL S172 — substrate detection, foreign-repo path expanded; F119 OPEN — mission constraints; F92 RESOLVED S113; F118 RESOLVED S105; F76 RESOLVED S97; F71 RESOLVED S94)

## Structure
```
beliefs/    PHILOSOPHY.md (identity), CORE.md (principles), DEPS.md (evidence),
            CHALLENGES.md (F113), CONFLICTS.md, INVARIANTS.md (F110-B1)
memory/     INDEX.md (this), PRINCIPLES.md, lessons/, DISTILL.md, VERIFY.md,
            OPERATIONS.md, HUMAN.md, SESSION-LOG.md, PULSE.md, HEALTH.md,
            HUMAN-SIGNALS.md (notable human inputs as swarm observations),
            EXPECT.md (expect-act-diff protocol — predict before acting, diff after)
tasks/      FRONTIER.md, NEXT.md, RESOLUTION-CLAIMS.md, HUMAN-QUEUE.md
tools/      validator, hooks, alignment_check, maintenance.py, periodics.json
experiments/  controlled experiments (33 children, see PULSE.md)
domains/    nk-complexity, distributed-systems, meta
docs/       PAPER.md (living self-paper, re-swarmed every 20 sessions — F115)
```

## Themes (228 lessons)

| Theme | Count | Key insight |
|-------|-------|-------------|
| Architecture | 15 | Blackboard+stigmergy, sharding, and boundary-aware structure decisions (L-156/L-161). |
| Protocols | 15 | Distill/verify/correct loop; evidence over assertion; protocol generalizability vs substrate coupling (L-158/L-209/L-213). |
| Strategy | 13 | Phase-aware execution, targeted fixes, superset-return refactor, and lib-production loop (L-175/L-177). |
| Complexity (NK) | 33 | Composite burden (K_avg*N+Cycles), multi-scale analysis, duplication K, cycle-based disambiguation (L-172/L-184). |
| Evolution | 55 | Spawn/harvest/selection, fitness quadrants, human-node integration, substrate diversity, F92 sizing rule, concurrent-node race pattern, self-tooling loop, and dual-pressure ancient-artifact evolution (L-153/L-208/L-214/L-222). |
| Distributed Systems | 10 | Error-handling anti-patterns, orchestrator detection, and runtime coordination signals. |
| Governance | 8 | Dark matter, principle recombination, authority typing, persuasion-vs-accuracy safeguards, structural-vs-behavioral enforcement gap, cross-swarm propagation gap, platform-scope belief contamination (L-210/L-212). |
| Meta | 58 | Autonomy, compaction/MDL cycles, alignment checks, proxy-K tracking, and multi-tool entry. |

## What to load when
| Doing...              | Read...                          |
|-----------------------|----------------------------------|
| Any session           | CLAUDE.md → CORE.md → this file → `tasks/NEXT.md` (Key state) |
| A specific task       | + relevant frontier/task files    |
| Updating beliefs      | + beliefs/DEPS.md                |
| Learning from past    | + PRINCIPLES.md or relevant lesson |
| F121 / human-signal work | + `memory/HUMAN-SIGNALS.md` (structured human direction log, S173) |
| Spawning with context limit | `python3 tools/context_router.py <task>` — select relevant files within budget |

Session log: `memory/SESSION-LOG.md` (append-only, F110-A3)

<!-- core_md_hash: 4dbc434747c5f73e31cebeb271b1b0a7518ab9b37b40fb3a712cebdffa6b140b -->
