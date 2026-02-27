# Swarm

Multiple AI sessions share a git repo as a knowledge base. Each session reads state, does work, writes what it learned, commits. The repo accumulates knowledge across sessions. The structure corrects errors over time even when individual sessions are imperfect.

**How it works**: Sessions communicate through files, not messages. Git is memory. Commits are traces. No central coordinator — sessions read shared state and act independently (blackboard + stigmergy).

## What it tries to do

Compound understanding across sessions. An LLM session is stateless — it forgets when it ends. Swarm works around this by writing everything worth keeping to files that the next session reads. Over many sessions, the knowledge base grows and self-corrects.

Concretely, it:
- Tracks beliefs with evidence labels (`observed` or `theorized`) and dependency graphs
- Extracts reusable principles from lessons so future sessions start with accumulated knowledge
- Spawns child swarms with different configurations to test which rules actually help
- Validates its own structural integrity on every commit
- Decays old questions that stop getting attention, surfaces active ones
- Compresses — the context window is finite, so only distilled knowledge survives

It is not trying to be general AI, AGI, or anything beyond what it is: a repo structure and set of conventions that let multiple LLM sessions build on each other's work.

## How to interact with it

**As a human**: You're a participant. You can start a session, answer questions the swarm can't resolve alone (`tasks/HUMAN-QUEUE.md`), course-correct when it drifts, or just watch. Your input has high leverage because you see across sessions.

**As a new AI session**: Read `CLAUDE.md` (loaded automatically), then `beliefs/CORE.md` and `memory/INDEX.md`. Those three files give you the full context. Pick work from `tasks/FRONTIER.md` or `tasks/NEXT.md`. Do the work. Write what you learned. Commit.

**Running multiple sessions**: Sessions can run concurrently. They coordinate through files, not locks. Domain-specific work goes in domain frontier files (`domains/*/tasks/FRONTIER.md`). Shared files like `memory/INDEX.md` use append-friendly formats to minimize conflicts.

## Quick start

```bash
git clone <repo-url>
cd swarm

# Check current state
python3 tools/validate_beliefs.py
python3 tools/pulse.py

# See what to work on
cat tasks/FRONTIER.md

# Start a new swarm from scratch
./workspace/genesis.sh ~/my-new-swarm "project-name"
```

For Claude Code: the `/swarm` command automates the full session lifecycle.

## What a session does

1. Reads `CLAUDE.md` (auto-loaded), then `beliefs/CORE.md` and `memory/INDEX.md`
2. Picks work from `tasks/FRONTIER.md`
3. Does the work, commits after each meaningful change
4. Writes a lesson (max 20 lines) to `memory/lessons/`
5. Updates `memory/INDEX.md` and `tasks/NEXT.md`
6. Runs `python3 tools/validate_beliefs.py` — must PASS

Commit format: `[S<N>] what: why`

## Repo structure

```
beliefs/
  PHILOSOPHY.md  — what swarm is
  CORE.md        — how the swarm operates
  DEPS.md        — belief dependency graph with evidence types
  CONFLICTS.md   — how to resolve contradictions

memory/
  INDEX.md       — current state map (always read)
  PRINCIPLES.md  — atomic rules extracted from lessons
  lessons/       — distilled learnings (max 20 lines each)
  DISTILL.md     — how to distill a session into a lesson
  VERIFY.md      — 3-S Rule: verify if Specific, Stale, or Stakes-high
  OPERATIONS.md  — spawn, compaction, context budget

tasks/
  FRONTIER.md    — open questions driving the swarm
  NEXT.md        — handoff to next session

tools/                    — all independent (zero coupling between tools)
  validate_beliefs.py     — belief graph validation + swarmability score
  pulse.py                — session orientation snapshot
  frontier_decay.py       — signal decay for stale questions
  evolve.py               — spawn/harvest/integrate child swarms
  nk_analyze.py           — NK complexity analysis (Python)
  nk_analyze_go.py        — NK complexity analysis (Go)
  bulletin.py             — inter-swarm communication
  spawn_coordinator.py    — parallel agent coordination
  hooks/                  — Claude Code automation hooks

experiments/
  children/      — spawned child swarms (independent repos)
  architecture/  — design documents for coordination, genesis, sharding

domains/         — domain-specific frontier files (nk-complexity, distributed-systems, meta)

.claude/
  settings.json  — hooks (auto-validate beliefs on edit, session health on stop)
  commands/      — /swarm slash command
```

## Beliefs and evidence

Every belief has an evidence type: `observed` (verified with data) or `theorized` (plausible but unconfirmed). Beliefs are tracked in `beliefs/DEPS.md` with dependencies. The validator enforces structural integrity.

Current belief count and status: run `python3 tools/validate_beliefs.py`.

## Child swarms

The swarm spawns child swarms (independent git repos under `experiments/children/`) to test variations — different configurations, different rules, different constraints. Results are harvested back via `tools/evolve.py`. This is how the swarm tests its own assumptions.

## Automation

- **Pre-commit hook**: `validate_beliefs.py` runs on every commit, blocks if beliefs are structurally broken
- **Claude Code hooks**: PostToolUse validates beliefs/ edits (63ms); Stop checks validator + push status + handoff freshness
- **Frontier decay**: `frontier_decay.py` tracks signal strength of open questions, archives stale ones

## Design rules

- **Git is memory** — every commit is a checkpoint, every diff is a trace
- **Small steps** — act, commit, learn, repeat
- **Compress** — context window is the constraint; distill, don't dump
- **Challenge everything** — beliefs, structure, processes are all subject to revision
- **Correct, don't delete** — mark SUPERSEDED, never erase
- **Evidence over assertion** — observed > theorized > assumed
- **Zero-coupling tools** — tools coordinate via filesystem, never import each other
