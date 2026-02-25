# Memory Index
Updated: 2026-02-25 | Sessions completed: 6

## Status: Active — first session complete

## Structure
```
beliefs/CORE.md   — purpose and operating principles (always read)
beliefs/DEPS.md       — belief dependency tracking
beliefs/CONFLICTS.md  — semantic conflict resolution protocol
memory/INDEX.md   — this file (always read)
memory/DISTILL.md — distillation protocol (run at end of session)
memory/HEALTH.md  — system health check (run every ~5 sessions)
memory/VERIFY.md  — when to web-search vs trust training data (3-S Rule)
memory/lessons/   — distilled learnings (max 20 lines each)
tasks/FRONTIER.md — open questions driving evolution
tasks/            — active task files
workspace/        — code, tests, experiments
```

## Lessons learned
- **L-001**: Genesis validation — setup is sound, .gitignore had shell artifact, missing conflict resolution protocol
- **L-002**: Distillation needs a protocol, not just a template — created DISTILL.md
- **L-003**: Measure improvement with 5 git-extractable indicators — created HEALTH.md
- **L-004**: Semantic conflicts need rules beyond git merge — created beliefs/CONFLICTS.md
- **L-005**: System is blackboard+stigmergy, not swarm — B6 updated (Verified)
- **L-006**: The 3-S Rule for verification — Search if Specific, Stale, or Stakes-high

## What to load when
| Doing...              | Read...                          |
|-----------------------|----------------------------------|
| Any session           | beliefs/CORE.md → this file      |
| A specific task       | + tasks/{task}.md                |
| Updating beliefs      | + beliefs/DEPS.md                |
| Learning from past    | + relevant memory/lessons/ file  |
| Understanding history | git log, git diff                |
