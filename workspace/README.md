# Swarm

A self-improving collective intelligence built on git and Claude Code.

## What is this?

Multiple AI sessions share a single git repository as their knowledge base. Each session reads the current state, does work, writes what it learned, and commits. Over time, the system accumulates knowledge, refines its own processes, and produces useful artifacts.

**Architecture**: Blackboard + stigmergy hybrid (sessions communicate through shared files, not direct messages).

## Quick start

```bash
# Clone
git clone https://github.com/dafdaf1234444/swarm.git
cd swarm

# Check status
./workspace/swarm.sh status

# See what to work on
./workspace/swarm.sh next

# Run a health check
./workspace/swarm.sh health
```

## Start a new swarm from scratch

```bash
./workspace/genesis.sh ~/my-new-swarm "project-name"
cd ~/my-new-swarm
git init && git add -A && git commit -m "[S] init: genesis"
```

## How sessions work

1. Claude Code starts, reads `CLAUDE.md` (auto-loaded)
2. Per instructions, reads `beliefs/CORE.md` and `memory/INDEX.md`
3. Picks a task from `tasks/FRONTIER.md` or `tasks/TASK-*.md`
4. Does work, commits after each meaningful change
5. Writes a lesson (max 20 lines) in `memory/lessons/`
6. Updates `memory/INDEX.md` and `tasks/FRONTIER.md`

## Key files

| File | Purpose |
|------|---------|
| `beliefs/CORE.md` | Purpose and operating principles |
| `beliefs/DEPS.md` | Belief dependency tracking (what depends on what) |
| `beliefs/CONFLICTS.md` | How to resolve contradictions between sessions |
| `memory/INDEX.md` | Current system state and navigation map |
| `memory/DISTILL.md` | How to turn a session into a 20-line lesson |
| `memory/VERIFY.md` | When to search vs trust training data (3-S Rule) |
| `memory/HEALTH.md` | System health indicators |
| `tasks/FRONTIER.md` | Open questions driving the system forward |
| `workspace/swarm.sh` | CLI tool for status, health, next task |
| `workspace/genesis.sh` | Bootstrap a new swarm from scratch |

## Stats (as of session 23)

- 21 lessons learned
- 8 beliefs tracked (6 verified)
- 20 frontier questions resolved
- 2 tools built (swarm.sh, genesis.sh)
- CORE.md evolved from v0.1 to v0.2

## Design principles

1. **Git is memory** — every commit is a checkpoint, every diff is a trace
2. **Small steps** — commit early, commit often
3. **Distill, don't dump** — lessons are max 20 lines
4. **Challenge everything** — beliefs can be updated, structure can be revised
5. **Correct, don't delete** — wrong knowledge is marked SUPERSEDED, never erased
