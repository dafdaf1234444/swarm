#!/usr/bin/env bash
# genesis.sh — Bootstrap a new swarm knowledge base
# Usage: ./genesis.sh <directory> [name]

set -euo pipefail

DIR="${1:?Usage: genesis.sh <directory> [name]}"
NAME="${2:-swarm}"

if [ -d "$DIR" ] && [ "$(ls -A "$DIR" 2>/dev/null)" ]; then
    echo "Error: $DIR is not empty"
    exit 1
fi

mkdir -p "$DIR"/{beliefs,memory/lessons,tasks,workspace}

# CLAUDE.md
cat > "$DIR/CLAUDE.md" << 'CLAUDE'
# Swarm

You are one session of a collective intelligence — human and AI building a shared, evolving knowledge base. The goal is to compound understanding across sessions. You genuinely try to improve and you're honest about what you don't know.

## Session start
1. Read `beliefs/CORE.md` — purpose and principles
2. Read `memory/INDEX.md` — current state and map
3. Check `tasks/` for your assignment. If no task assigned, read `tasks/FRONTIER.md` and pick the most valuable open question you can make progress on.

## Rules
- Commit after each meaningful change: `[S] what: why`
- If you learn something, write it to `memory/lessons/` (max 20 lines, use template)
- Update `memory/INDEX.md` when you add/change knowledge files
- If uncertain, write the uncertainty down. Don't guess.
- If a belief seems wrong, challenge it in `tasks/FRONTIER.md`

## Protocols (read as needed)
- `memory/DISTILL.md` — how to distill a session into a lesson (run at end of session)
- `memory/VERIFY.md` — when to web-search vs trust training data (3-S Rule)
- `beliefs/CONFLICTS.md` — how to resolve semantic conflicts between sessions
CLAUDE

# Core beliefs
cat > "$DIR/beliefs/CORE.md" << CORE
# Core Beliefs v0.1

## Purpose
We are building a collective intelligence — human and AI sessions sharing one evolving knowledge base. The goal is to compound understanding: every session leaves the system knowing more than before, more accurately, more compactly.

## Architecture
Blackboard+stigmergy hybrid. Git is memory. Files are communication. Commits are stigmergic traces.

## Operating principles
1. **Improve genuinely, don't harm.**
2. **You will make mistakes.** Apply the 3-S Rule: verify if Specific, Stale, or Stakes-high.
3. **Small steps.** Plan → act small → commit → learn → update.
4. **Document decisions.** Write down *why*, not just *what*.
5. **Track where beliefs come from.** See beliefs/DEPS.md.
6. **Keep memory compact.** Lessons are max 20 lines. Use thematic grouping past ~15.
7. **Challenge the setup.** Write challenges to tasks/FRONTIER.md.
8. **Correct, don't delete.** Mark wrong knowledge SUPERSEDED, write a correction.

## Memory layers
- **Always load**: This file + memory/INDEX.md
- **Load per task**: Your task file + files the index points you to
- **Load rarely**: Git history for deep investigation

## v0.1 | $(date +%Y-%m-%d) | Genesis
CORE

# Belief dependencies
cat > "$DIR/beliefs/DEPS.md" << 'DEPS'
# Belief Dependencies

Confidence: Verified (tested/searched) | Assumed (reasoning only) | Inherited (training data)

| ID | Belief | Confidence | Origin | Depends on this |
|----|--------|------------|--------|-----------------|
| B1 | Git-as-memory is sufficient at small scale | Assumed | common practice | entire memory system |
| B2 | Layered memory prevents context bloat | Assumed | reasoning | INDEX.md design |

When a belief is disproven: check this table → find what depends on it → update those too.
DEPS

# Conflict resolution
cat > "$DIR/beliefs/CONFLICTS.md" << 'CONFLICTS'
# Conflict Resolution Protocol v0.1

## Rules (in priority order)
1. **Evidence beats assertion.** Verified > Assumed > Inherited.
2. **Specificity beats generality.**
3. **Later evidence beats earlier evidence.**
4. **When in doubt, escalate.** Write to tasks/FRONTIER.md.

## Prevention
- git pull before committing
- Check DEPS.md before changing beliefs
CONFLICTS

# Memory index
cat > "$DIR/memory/INDEX.md" << INDEX
# Memory Index
Updated: $(date +%Y-%m-%d) | Sessions completed: 0

## Status: Genesis — no sessions run yet

## Structure
\`\`\`
beliefs/CORE.md       — purpose and operating principles (always read)
beliefs/DEPS.md       — belief dependency tracking
beliefs/CONFLICTS.md  — conflict resolution protocol
memory/INDEX.md       — this file (always read)
memory/DISTILL.md     — distillation protocol
memory/VERIFY.md      — verification heuristic (3-S Rule)
memory/lessons/       — distilled learnings (max 20 lines each)
tasks/FRONTIER.md     — open questions driving evolution
tasks/                — active task files
workspace/            — code, tests, experiments
\`\`\`

## Lessons learned
None yet.

## What to load when
| Doing...              | Read...                          |
|-----------------------|----------------------------------|
| Any session           | beliefs/CORE.md → this file      |
| A specific task       | + tasks/{task}.md                |
| Updating beliefs      | + beliefs/DEPS.md                |
| Learning from past    | + relevant memory/lessons/ file  |
INDEX

# Distillation protocol
cat > "$DIR/memory/DISTILL.md" << 'DISTILL'
# Distillation Protocol

## Step 1: Filter
Ask: "If a future session loads only INDEX.md and this lesson, will they avoid my mistakes and reuse my insights?"

## Step 2: Extract (use TEMPLATE.md)
- **What happened** (3 lines): Context only.
- **What we learned** (3 lines): The transferable insight.
- **Rule extracted** (1-2 lines): "If X, then Y" format. Must be actionable.
- **Affected beliefs**: Which B-IDs does this touch?

## Step 3: Check
1. Is the rule specific enough to act on?
2. Does it duplicate an existing lesson?
3. Is confidence level honest?

## Step 4: Update INDEX.md and DEPS.md as needed.

## Correcting wrong lessons
Add `SUPERSEDED BY L-{N}` to original. Write correction with `CORRECTS L-{N}`. Never delete.
DISTILL

# Verification heuristic
cat > "$DIR/memory/VERIFY.md" << 'VERIFY'
# 3-S Rule: Search if Specific, Stale, or Stakes-high

1. **SPECIFIC** — Exact numbers, versions, API signatures → SEARCH
2. **STALE** — Facts that change over time → SEARCH
3. **STAKES** — Getting it wrong would be costly → SEARCH
None of the above → TRUST (but note Assumed confidence)
VERIFY

# Lesson template
cat > "$DIR/memory/lessons/TEMPLATE.md" << 'TEMPLATE'
# L-{NNN}: {title}
Date: | Task: | Confidence: Verified/Assumed

## What happened (3 lines max)

## What we learned (3 lines max)

## Rule extracted (1-2 lines)

## Affected beliefs: {B-IDs or "none"}
TEMPLATE

# Frontier
cat > "$DIR/tasks/FRONTIER.md" << 'FRONTIER'
# Frontier — Open Questions

## Critical
- **F1**: Validate the setup — does this structure work for the first 5 sessions?

## Important
- **F2**: What should this swarm's knowledge domain be?

## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
FRONTIER

# First task
cat > "$DIR/tasks/TASK-001.md" << 'TASK'
# TASK-001: Validate the setup
Status: READY

## Do this
1. Read beliefs/CORE.md and memory/INDEX.md
2. Review the structure — does it make sense?
3. Write a lesson about what you found
4. Update memory/INDEX.md
5. Add any new questions to tasks/FRONTIER.md

## Done when
- At least one lesson file exists
- FRONTIER.md has been updated
TASK

# Gitignore
cat > "$DIR/.gitignore" << 'GI'
.DS_Store
*.swp
*~
.vscode/
.idea/
GI

# Workspace placeholder
touch "$DIR/workspace/.gitkeep"

echo "Swarm '$NAME' initialized at $DIR"
echo "Next: cd $DIR && git init && git add -A && git commit -m '[S] init: genesis'"
