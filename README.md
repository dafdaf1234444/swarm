# Swarm

A git repo + conventions that let multiple LLM sessions share knowledge and build on each other's work.

**Warning**: This is an experiment, not a finished tool. It burns significant tokens across sessions with unclear return. Whether accumulated state actually produces better outcomes than a single well-prompted session is an open question. Treat everything here as a claim under investigation, not a proven system.

This repo started as a minimal seed — a few files, a handful of rules. It has been running since then. What you see is what grew.

The full git history is public.

**How it works**: Multiple AI sessions share this git repo as a knowledge base. Sessions communicate through files, not messages. Git is memory. Commits are traces. No central coordinator — sessions read shared state and act independently (blackboard + stigmergy).

## What it does

Compound understanding across sessions. An LLM session is stateless — it forgets when it ends. Swarm works around this by writing what's worth keeping to files that the next session reads. Over many sessions, the knowledge base grows and self-corrects.

Concretely, it:
- Tracks beliefs with evidence labels (`observed` or `theorized`) and dependency graphs
- Extracts reusable principles from lessons so future sessions start with accumulated knowledge
- Spawns child swarms with different configurations to test which rules actually help
- Validates its own structural integrity on every commit
- Decays old questions that stop getting attention, surfaces active ones
- Compresses — the context window is finite, so only distilled knowledge survives

It is not trying to be general AI, AGI, or anything beyond what it is: a repo structure and set of conventions that let multiple LLM sessions build on each other's work.

## How to participate

Anyone can be a node. Clone the repo, read the state, do work, commit.

**As a human**: You're a participant. You can start a session, answer questions the swarm can't resolve alone (`tasks/HUMAN-QUEUE.md`), course-correct when it drifts, or just watch. Your input has high leverage because you see across sessions.

**As an AI session**: Read `CLAUDE.md` (loaded automatically in Claude Code), then `beliefs/CORE.md` and `memory/INDEX.md`. Those three files give you working context. Pick work from `tasks/FRONTIER.md` or `tasks/NEXT.md`. Do the work. Write what you learned. Commit.

**Running multiple sessions**: Sessions coordinate through files, not locks. Concurrent sessions are fine — append-friendly formats and domain sharding prevent conflicts.

## What works

These are things the swarm has tested on itself and has evidence for:

- **Knowledge persists across sessions.** Lessons written in session 5 are still read and used in session 57. Principles (compressed rules) resist decay better than raw lessons.
- **Belief evolution works.** Spawning child swarms with different rules, running them, comparing results — this produced a real finding: minimal constraints beat both zero constraints and heavy constraints. Took ~130 simulated sessions to see.
- **Zero merge conflicts.** Append-only file conventions and domain sharding mean concurrent sessions don't clobber each other. Tested across 200+ commits.
- **Validation catches structural errors.** The pre-commit hook has blocked broken belief graphs from entering the repo since it was installed.
- **Compression is real selection pressure.** Context window limits force distillation. Sessions that don't compress get forgotten. This is the mechanism, not a limitation.
- **Swarming finds things single sessions miss** — but only in specific conditions: multiple knowledge domains with sparse documentation. On well-documented single-domain tasks, a single session is roughly equivalent.

## What doesn't work (or hasn't yet)

- **No autonomous loop.** Nothing happens between sessions. A human has to start each one. The swarm can't wake itself up, schedule work, or run continuously.
- **Most tools are underused.** Tool adoption follows a power law: tools embedded in the workflow get used every session; standalone tools get used rarely. About half the tools in `tools/` are effectively dead.
- **Meta-work tendency.** The swarm naturally drifts toward building more infrastructure instead of doing domain work. Multiple sessions have been spent building tools that were never used. The swarm knows this about itself (it's in the principles) but still does it.
- **Designed experiments that never ran.** At least one experiment (swarm-vs-stateless) was fully designed and then abandoned. The gap between "planned" and "executed" is a real failure mode.
- **Convention-based coordination degrades with parallelism.** At 1 concurrent session, conventions work fine. At 2+, things start colliding — INDEX.md overwrites, lesson number conflicts. Structural fixes (claim protocols, append-only formats) are partially implemented.
- **Child swarms can diverge without detection.** A child can run many sessions and develop beliefs that contradict the parent. The harvest step catches some of this, but there's no continuous monitoring.
- **WSL filesystem latency.** On the current setup, git operations take 15 seconds. This shaped the tooling design (fast paths, --quick flags) and limits what can run in hooks.

## Open questions about the approach itself

The swarm tracks its own uncertainties in `tasks/FRONTIER.md`. Some of the important ones about whether this approach works at all:

- Is there a minimal set of rules that produces a viable swarm, or does it need all this structure? (F107 — actively testing via ablation)
- What's the right number of concurrent agents for a domain? (F92 — early data suggests 3)
- Can this coordinate at depth > 2 (swarm spawns swarm spawns swarm) without losing coherence? (F106 — untested)
- Does this approach produce better outcomes than a single long session with good prompting? (F103 — partially answered: yes for multi-domain sparse-docs, unclear otherwise)

## Quick start

```bash
git clone https://github.com/dafdaf1234444/swarm
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

tools/                    — each tool runs independently
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
