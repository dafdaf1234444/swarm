# Swarm

Swarm is a repository protocol for multi-session AI work: each session reads shared state, does work, writes back, and leaves the system more useful for the next session.

This is not a static codebase with a fixed owner workflow. It is a living coordination substrate where git history is memory, files are communication, and sessions are replaceable nodes.

## Current State Snapshot (2026-02-27, local run)

This snapshot is for orientation only. Canonical live state is always in `memory/INDEX.md`, `tasks/FRONTIER.md`, and `tasks/NEXT.md`.

- Status: active Codex-driven swarm sessions are ongoing.
- Integrity: beliefs validator PASS; latest `bash tools/check.sh --quick` run is NOTICE-only (dirty-tree/session-order/proxy-K reminders).
- Swarm scale: 208 lessons, 149 principles, 14 beliefs, 14 active frontier questions.
- Project footprint (tracked): 671 files, 80,220 estimated lines, 4,062,621 bytes (~3.88 MiB), 384 commits.
- File mix (tracked): 449 Markdown, 148 Python, 48 JSON, 5 shell scripts.
- Largest tracked areas by file count: `memory/` 217, `workspace/` 197, `experiments/` 155, `tools/` 52.
- Git object store size: 6.25 MiB (`git count-objects -vH`).
- Immediate human dependency: F111 deploy decision remains human-gated.
- Runtime note: this host currently relies on bash/`python3` paths for startup checks when PowerShell `python` is unavailable.

## Warning Before You Run `swarm`

- `swarm` is not a no-op status check. It authorizes autonomous work selection from live priorities.
- A swarm run can edit many files, run maintenance/experiments, and consume significant tokens quickly.
- Do not run swarm if you need a frozen tree. Use explicit scoped instructions instead (target file/task, exclusions, and timebox).
- Always inspect deltas in git history, not chat memory, to understand what changed and why.
- If you want bounded behavior, state hard constraints up front (for example: "README only, no tool code changes, no experiments").

## Read This First

If you are new, start here in order:

1. `SWARM.md` - operating entrypoint for any node
2. `beliefs/CORE.md` - non-negotiable operating principles
3. `memory/INDEX.md` - current state map and where knowledge lives
4. `tasks/FRONTIER.md` - open questions
5. `tasks/NEXT.md` - immediate handoff

For current integrity/status, run:

```bash
bash tools/check.sh --quick
```

PowerShell equivalent:

```powershell
pwsh -NoProfile -File tools/check.ps1 --quick
```

If `bash` is unavailable, follow runtime fallback instructions in `SWARM.md`.

Install commit-time quality hooks once per clone:

```bash
bash tools/install-hooks.sh
```

## Swarm Mentality

The swarm is built around a few behavioral commitments:

- Autonomy: sessions self-direct after loading state.
- Evidence first: claims are tracked and challenged; confidence alone is not enough.
- Compression is required: the context window is finite, so distilled knowledge survives.
- Correct, do not erase: mark superseded, append corrections, preserve traceability.
- File-native coordination: sessions coordinate via repo artifacts, not chat memory.
- Human as asymmetric node: high-leverage direction, no epistemic override without evidence.

If a change does not improve future-node pickup speed, it is probably not swarm-quality work.

## What This Is

- A persistent memory and coordination system for repeated AI sessions.
- A place to test and refine beliefs, principles, and workflows.
- A practical experiment in whether repeated structured sessions outperform isolated ones under some conditions.

## What This Is Not

- Not an autonomous always-on agent.
- Not guaranteed better than a strong single session for every task.
- Not a finished product with stable UX promises.

## How A Session Works

Every session is expected to follow this loop:

1. Load core state (`SWARM.md`, `CORE.md`, `INDEX.md`, `FRONTIER.md`, `NEXT.md`).
2. Run maintenance (`bash tools/maintenance.sh`).
3. Pick the highest-value actionable item.
4. Execute and verify.
5. Distill what was learned (`memory/lessons/`, task/frontier updates).

Minimal closeout command:

```bash
bash tools/check.sh --quick
```

## How To Participate

As a human node:

- Set mission and constraints.
- Provide directional corrections when the swarm drifts.
- Answer items in `tasks/HUMAN-QUEUE.md` that require human judgment.

## Current User Pattern

Current operation includes active Codex-driven swarm sessions. At user level, the workflow is intentionally simple and repetitive:

- Trigger `swarm` frequently (effectively "spam swarm") and observe what the system produces.
- Use git/session history as the main inspection surface for what changed and why.
- Accept exploratory token burn as part of discovery; expectations are often intentionally open-ended at start.
- Apply heavy steering only where needed; otherwise keep spawning fresh chats that reinforce the same objective: swarm as the primary ongoing activity.

As an AI node:

- Follow the startup order above.
- Work from `tasks/FRONTIER.md` and `tasks/NEXT.md`.
- Leave state cleaner, clearer, and easier to continue.

## Repo Map

- `beliefs/` - identity, principles, dependencies, conflicts, challenges
- `memory/` - index, principles, lessons, operations, verification protocols
- `tasks/` - active frontier, near-term handoff, resolution claims
- `tools/` - validators, maintenance, analysis, coordination helpers
- `experiments/` - controlled runs and artifacts
- `domains/` - domain-specific frontiers and indexes
- `docs/REAL-WORLD-SWARMING.md` - practical branch/PR and multi-setup swarming playbook

## How To Swarm This README

This file is the public interface for third-party readers. It must remain readable, accurate, and low-drift.

When to update:

- Startup path changed.
- Core claims in this file drift from `SWARM.md`, `CORE.md`, `INDEX.md`, or `FRONTIER.md`.
- A major frontier is resolved that changes the external story.
- The onboarding flow becomes unclear for new nodes.

How to update:

1. Verify claims against source files, not memory.
2. Prefer stable framing over volatile numbers.
3. If numbers are necessary, cite date/session context or point to `memory/INDEX.md`.
4. Keep this file as orientation, not a duplicate of operational docs.
5. After editing, run `bash tools/check.sh --quick`.

Definition of done for README changes:

- A third-party reader can answer: "What is this?", "How does it think?", "How do I start?".
- A future node can update this file without inventing process.

## Canonical Live State (Read This, Not Stale Snapshot Text)

Do not treat any static README numbers or claims as authoritative beyond their stamped date/session.

- Live state: `memory/INDEX.md`
- Live priorities: `tasks/FRONTIER.md` and `tasks/NEXT.md`
- Live integrity: `tools/check.sh` and `tools/maintenance.sh`
