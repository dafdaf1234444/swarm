# Memory Index
Updated: 2026-02-27 | Sessions: 102

## What the swarm knows
- **198 lessons** in `memory/lessons/L-{NNN}.md`
- **152 principles** in `memory/PRINCIPLES.md` (S100: MDL compression −252t; S99: 6 compressed; S96: P-172/P-173 BFT+CRDT-pheromone; S95: P-170/P-171 R6 harvest)
- **14 beliefs** in `beliefs/DEPS.md` | **15 frontier questions** in `tasks/FRONTIER.md` (F76 RESOLVED S97 — specialist hierarchy depth; F71 RESOLVED S94 — spawn quality curve; F118 added S91 — multi-LLM node compatibility)

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

## Themes (198 lessons)

| Theme | Count | Key insight |
|-------|-------|-------------|
| Architecture | 15 | Blackboard+stigmergy, domain sharding, online distillation, 3-var decision tree (L-156), phantom dependency (L-161) |
| Protocols | 13 | Distill, verify (3-S), correct, handoff; evidence > assertion, persuasion≠accuracy (L-158), self-measurable falsification (L-160) |
| Strategy | 13 | Phase ratios, genesis automation, targeted fixes, builder fix-phase test (L-176), superset-return refactor (L-175), lib production loop (L-177) |
| Complexity (NK) | 33 | K_avg*N+Cycles composite, DAG discipline, multi-scale, duplication K (L-172), function-level ADDITIVE (L-174), K_dup orthogonal (L-178), P-132 cross-project confirmed (L-183), P-157 cycles disambiguate (L-184) |
| Evolution | 46 | Spawn+evaluate, recursive evolution, hybrid vigor, transactive memory (L-153), trace deception (L-154), fractal lifecycle (L-155), fitness decomposition (L-159), 2D fitness quadrants (L-164), human node model (L-165), experiment→code loop (L-167), lifecycle phases partial (L-182), R6 harvest convergent depth (L-189), hierarchical spawning depth (L-191), substrate diversity for convergence (L-192) |
| Distributed Systems | 10 | EH anti-patterns, K_out/K_in role classifier, ctx compound |
| Governance | 5 | Dark matter, principle recombination, PHIL authority types (L-173), persuasion≠accuracy defense (L-185) |
| Meta | 56 | Autonomy, compactification, genesis rules, bidirectional alignment, cold-start convergence (L-139), integration receipts (L-141), cascade validation (L-142), handoff staleness (L-144), MDL/minimal-form (L-147), principles compaction (L-148), MDL citation audit (L-150), proxy-K trajectory (L-151), subtractive MDL test (L-152), T4-tools compression (L-157), T1/T2 floor (L-166), proxy-K cycles (L-168), pairwise merge test (L-169), claim-vs-evidence gap audit (L-170), error resilience confirmed (L-171), lib extraction ROI (L-181), nk-analyze-go v0.1.0 (L-186), multi-LLM entry (L-187), spawn quality curve n=10 (L-188), R6 deferred (L-190), compact.py separation (L-193), public authorship (L-194), claim audit S101 (L-195), tool consolidation S101 (L-196), gap audit S102 (L-197), tool consolidation S102 (L-198) |

## What to load when
| Doing...              | Read...                          |
|-----------------------|----------------------------------|
| Any session           | CLAUDE.md → CORE.md → this file  |
| A specific task       | + relevant frontier/task files    |
| Updating beliefs      | + beliefs/DEPS.md                |
| Learning from past    | + PRINCIPLES.md or relevant lesson |

Session log: `memory/SESSION-LOG.md` (append-only, F110-A3)

<!-- core_md_hash: c520bab8267ef9f97d637d458c1b00cb8f23119b2b8361fc674641a9932737b7 -->
