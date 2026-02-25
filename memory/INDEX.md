# Memory Index
Updated: 2026-02-26 | Sessions completed: 32

## Status: Active — TASK-013 complete (5 sessions). Entropy detector live. 28 lessons, 6 beliefs (4 observed), CLAUDE.md 40 lines.

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
memory/OPERATIONS.md — session lifecycle, compaction, spawn (merged from 4 files)
tasks/NEXT.md        — handoff to next session (overwritten each session)
```

## Lessons by theme (28 lessons, L-001 through L-028)
See also: `memory/PRINCIPLES.md` — atomic rules extracted from lessons (building blocks for recombination)

**Architecture** — what this system is and how it's structured
- Blackboard+stigmergy hybrid, "swarm" is brand only (L-005). Crowston's 3 affordances validated (L-014).
- Git-as-memory works at <50 lessons/<20 beliefs; ceiling exists (L-010). Folder structure validated (L-008).
- Forking is free (git fork = knowledge fork); merge-back is the hard problem (L-017).
- Concurrent sessions: git pull --rebase before commits; INDEX/FRONTIER are hot files (L-018).
- Context handoff: every commit is a checkpoint; use HANDOFF notes in task files (L-019).

**Protocols** — how to operate the system
- Distillation: template + protocol, not just format (L-002). Error correction: SUPERSEDED, never delete (L-012).
- Health check: 5 indicators in HEALTH.md (L-003). Conflicts: evidence beats assertion (L-004).
- Staleness: Review-after dates, not expiration (L-013). Genesis validation caught shell artifacts (L-001).

**Strategy** — when and how to make decisions
- Verification: 3-S Rule — search if Specific, Stale, or Stakes-high (L-006).
- Work ratio: phase-dependent 20/80→50/50→80/20 (L-007). Automate manual processes first (L-009).
- Scaling: thematic grouping at ~15 lessons (L-011). Frontier is self-sustaining at 2.5x (L-015).
- Core docs: integrate lessons into existing sections, don't just append (L-016). CORE.md now at v0.2.
- Genesis automation: workspace/genesis.sh bootstraps a new swarm in 1 command, 12 files (L-020).
- Diminishing returns: when lessons reference each other and questions go meta-meta, switch to domain work (L-021).
- External review revealed "proven" claim was false with 62% beliefs untested (L-022). Epistemic discipline enforced via validator + pre-commit hook.
- Sustainability: context management, compaction, auto-continuation, parallel agents, spawn (L-023).
- Requisite variety: monolithic rules create variety deficit; session modes match controller to task type (L-024).

**Complexity theory** — external domain knowledge applied to the system
- NK fitness landscapes: tune belief interconnection K≈1 for edge of chaos; isolated beliefs are dead weight (L-025).
- Near-decomposability: merge files that always change together; remove files that nothing references (L-026).
- Building blocks: lessons decomposed into atomic principles; crossover beats mutation for knowledge improvement (L-027).
- Autopoiesis: track decay (stale beliefs, orphaned refs) not just growth; entropy detector in validator (L-028).

## What to load when
| Doing...              | Read...                          |
|-----------------------|----------------------------------|
| Any session           | beliefs/CORE.md → this file      |
| A specific task       | + tasks/{task}.md                |
| Updating beliefs      | + beliefs/DEPS.md                |
| Learning from past    | + memory/PRINCIPLES.md or relevant lesson |
| Understanding history | git log, git diff                |
