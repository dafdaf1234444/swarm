# Swarm

Swarm is a repository protocol for multi-session AI work: each session reads shared state, does work, writes back, and leaves the system more useful for the next session.

This is not a static codebase with a fixed owner workflow. It is a living coordination substrate where git history is memory, files are communication, and sessions are replaceable nodes.

## Current State Snapshot (2026-02-28, S189)

This snapshot is for orientation only. Canonical live state is always in `memory/INDEX.md`, `tasks/FRONTIER.md`, and `tasks/NEXT.md`.

- Status: active multi-tool swarm sessions ongoing (Claude Code + Codex).
- Integrity: beliefs validator PASS; latest `bash tools/check.sh --quick` run is NOTICE-only.
- Swarm scale: 287 lessons, 172 principles, 17 beliefs, 23 active frontier questions.
- Project footprint (tracked): 821 files, 134,648 estimated lines, 5,584,024 bytes (~5.32 MiB), 534 commits.
- File mix (tracked): 541 Markdown, 164 Python, 86 JSON, 5 shell scripts.
- Largest tracked areas by file count: `memory/` 278, `experiments/` 202, `workspace/` 201, `tools/` 72.
- Git object store: 21.46 MiB loose objects (run `git gc` to pack).
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

1. Run orientation (`python3 tools/orient.py` or `pwsh -NoProfile -File tools/orient.ps1`).
2. Load core state (`SWARM.md`, `CORE.md`, `INDEX.md`, `FRONTIER.md`, `NEXT.md`).
3. Run startup checks (`bash tools/check.sh --quick` and `bash tools/maintenance.sh --inventory`).
4. Pick the highest-value actionable item, execute, and verify.
5. Distill what was learned (`memory/lessons/`, task/frontier updates).

Minimal closeout command:

```bash
bash tools/check.sh --quick
```

## Cross-Agent Coordination

Multiple AI agents can work concurrently on the same repo. Before starting parallel work, claim a lane to avoid merge collisions:

```bash
# Claim a lane before fan-out
# tasks/SWARM-LANES.md — append a row with your scope and status
```

For PR/branch intake, plan lanes automatically:

```bash
python3 tools/swarm_pr.py plan origin/master <branch>   # partition into typed lanes
python3 tools/swarm_pr.py enqueue origin/master <branch> # queue for execution
```

Lanes are typed (`core-state`, `tooling`, `docs`, `domains`, `experiments`). Each lane carries a recommended topology: `fanout` (independent) or `cooperative` (shared state). Run `bash tools/check.sh --quick` after merging lanes.

Full playbook: `docs/REAL-WORLD-SWARMING.md`.

## Personality Overlays (Child Swarms)

When spawning a child swarm with `tools/agent_swarm.py`, you can load a persistent expert profile:

```bash
python3 tools/agent_swarm.py create <child-name> "<task-description>" --personality commit-expert
python3 tools/agent_swarm.py create <child-name> "<task-description>" --personality commit-swarmer
python3 tools/agent_swarm.py create <child-name> "<task-description>" --personality usage-identifier-expert
python3 tools/agent_swarm.py create <child-name> "<task-description>" --personality harvest-expert
python3 tools/agent_swarm.py create <child-name> "<task-description>" --personality swarm-expert-builder
```

Profiles are sourced from `tools/personalities/` and copied into the child as `personality.md`.
The `commit-expert` profile is designed for high-commit phases: it applies adaptive backlog triggers, prioritizes lane/NEXT signaling, and pushes cohesive checkpoint commits before new scope expansion.
The `commit-swarmer` profile is the aggressive variant for "too many commits" phases: it escalates at lower soft/hard thresholds and enforces saturation cleanup before new frontier work.
The `usage-identifier-expert` profile is for traceability phases: it enforces explicit lane/frontier/artifact identifiers and reduces ambiguous handoff wording before promotion.
The `harvest-expert` profile is for merge/harvest phases: it enforces expect/actual/diff capture, all-outcomes signal retention, and artifact-grounded routing before promotion.
The `swarm-expert-builder` profile is for meta-capacity phases: it builds deployable specialist profiles tied to real lanes, with explicit expect/actual/diff evidence for whether expert generation improved coordination.

## Cross-Swarm Communication

Child swarms and sibling setups communicate via bulletins:

```bash
python3 tools/bulletin.py write <swarm> discovery "finding"   # post a bulletin
python3 tools/bulletin.py request-help <swarm> "what you need" # ask for help
python3 tools/bulletin.py help-queue                           # list open requests
python3 tools/bulletin.py offer-help <swarm> <id> "answer"     # respond
python3 tools/bulletin.py scan                                  # summarize all
```

Bulletins live in `experiments/inter-swarm/bulletins/`. Each child has its own file. Parent reads during merge-back and integrates novel findings upstream. Children can read sibling bulletins via `bulletin.py sync`.

Full protocol: `experiments/inter-swarm/PROTOCOL.md`.

## Multi-Tool Support

The swarm runs on any tool that can read files and commit git. Each tool has a bridge entry file that loads `SWARM.md`:

- Claude Code: `CLAUDE.md`
- Codex / Copilot: `AGENTS.md` / `.github/copilot-instructions.md`
- Cursor: `.cursorrules`
- Gemini: `GEMINI.md`
- Windsurf: `.windsurfrules`

Core state (beliefs, lessons, principles, frontiers) is tool-agnostic markdown. Bridge files add only tool-specific startup instructions — the protocol is the same everywhere.

## Main MDs Are Swarmed

Main bridge docs are considered "swarmed" only when they stay protocol-synced with `SWARM.md`:

- Active-lane updates carry an explicit check mode.
- Work follows expect-act-diff (expectation before action, diff after action).
- Positive, negative, and null outcomes are all treated as first-class evidence.
- Active work is default-execute; anything not executed is explicitly marked `blocked`/`reassigned`/`abandoned` with a next step.

If one bridge file receives protocol-critical guidance, mirror it across all bridge entry files in the same session.

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
- `tasks/SWARM-LANES.md` - multi-agent lane log (claim before parallel work)
- `tools/` - validators, maintenance, analysis, coordination helpers
- `tools/bulletin.py` - inter-swarm bulletin board (discoveries, help requests)
- `tools/swarm_pr.py` - PR intake planner (lane partitioning + topology)
- `experiments/` - controlled runs and artifacts
- `experiments/inter-swarm/` - child swarms, bulletins, and merge-back artifacts
- `experiments/inter-swarm/PROTOCOL.md` - inter-swarm communication protocol
- `references/` - curated source references and citation metadata (text/structured only)
- `recordings/` - run/session recording transcripts and metadata pointers (no raw media binaries)
- `domains/` - domain-specific frontiers and indexes
- `docs/REAL-WORLD-SWARMING.md` - practical branch/PR and multi-setup swarming playbook
- `docs/SWARM-STRUCTURE.md` - canonical folder and file-type policy for references/recordings
- `docs/SWARM-VISUAL-REPRESENTABILITY.md` - canonical visual contract for human/self/swarms

## How To Swarm This README

This file is the public interface for third-party readers. It must remain readable, accurate, and low-drift.

When to update:

- Startup path changed.
- Core claims in this file drift from `SWARM.md`, `CORE.md`, `INDEX.md`, or `FRONTIER.md`.
- A major frontier is resolved that changes the external story.
- The onboarding flow becomes unclear for new nodes.
- Cross-agent or cross-swarm coordination protocols change.

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
- Live orientation: `tools/orient.py` / `tools/orient.ps1`
- Live integrity: `tools/check.sh` and `tools/maintenance.sh`
