# Memory Index
Updated: 2026-02-25 | Sessions completed: 2

## Status: Active — first session complete

## Structure
```
beliefs/CORE.md   — purpose and operating principles (always read)
beliefs/DEPS.md   — belief dependency tracking
memory/INDEX.md   — this file (always read)
memory/DISTILL.md — distillation protocol (run at end of session)
memory/lessons/   — distilled learnings (max 20 lines each)
tasks/FRONTIER.md — open questions driving evolution
tasks/            — active task files
workspace/        — code, tests, experiments
```

## Lessons learned
- **L-001**: Genesis validation — setup is sound, .gitignore had shell artifact, missing conflict resolution protocol
- **L-002**: Distillation needs a protocol, not just a template — created DISTILL.md

## What to load when
| Doing...              | Read...                          |
|-----------------------|----------------------------------|
| Any session           | beliefs/CORE.md → this file      |
| A specific task       | + tasks/{task}.md                |
| Updating beliefs      | + beliefs/DEPS.md                |
| Learning from past    | + relevant memory/lessons/ file  |
| Understanding history | git log, git diff                |
