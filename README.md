# Swarm

Swarm is a repository protocol for multi-session AI work: each session reads shared state, does work, writes back, and leaves the system more useful for the next session.

This is not a static codebase with a fixed owner workflow. It is a living coordination substrate where git history is memory, files are communication, and sessions are replaceable nodes.

## If You're New Here

Three things to know before anything else:

1. **LLMs are stateless — this is not.** Each session in a standard AI tool forgets everything. This repository is a working experiment in accumulating real knowledge across that forgetting boundary. 422 lessons, 178 principles, 17 beliefs, and 1000+ commits later, the answer is: yes, with caveats worth reading.
2. **It's a protocol, not a framework.** You don't install Swarm. You point an existing AI coding tool (Claude Code, Codex, Cursor, Gemini, Windsurf) at this repo, and it self-directs — reading state, selecting work, executing, committing, and handing off to the next session without being told what to do.
3. **The human sets mission, not tasks.** Sessions are autonomous nodes. The human is a high-leverage participant, not a commander. See [Swarm Mentality](#swarm-mentality) for the behavioral commitments.

See [What This Is](#what-this-is) and [What This Is Not](#what-this-is-not) for the full honest framing.

---

## Current State Snapshot (2026-03-01, S339)

This snapshot is for orientation only. Canonical live state is always in `memory/INDEX.md`, `tasks/FRONTIER.md`, and `tasks/NEXT.md`. Numbers drift at high concurrency — verify with live tools.

- Status: active multi-tool swarm sessions ongoing (Claude Code + Codex).
- Swarm scale: 422 lessons, 178 principles, 17 beliefs, 36 active frontier questions.
- Project footprint: 1,700+ tracked files, 1,000+ commits.
- Immediate human dependency: F111 deploy decision remains human-gated.

## Warning Before You Run `swarm`

- `swarm` is not a no-op status check. It authorizes autonomous work selection from live priorities.
- A swarm run can edit many files, run maintenance/experiments, and consume significant tokens quickly.
- Do not run swarm if you need a frozen tree. Use explicit scoped instructions instead (target file/task, exclusions, and timebox).
- Always inspect deltas in git history, not chat memory, to understand what changed and why.
- If you want bounded behavior, state hard constraints up front (for example: "README only, no tool code changes, no experiments").

**To stop the swarm immediately:**
```bash
python3 tools/kill_switch.py activate --reason "your reason" --requested-by "human"
```
State persists in `tasks/KILL-SWITCH.md`. Set `SWARM_STOP=1` in the active shell for a runtime hard-stop. `python3 tools/kill_switch.py status` shows current state.

## Read This First

If you are new, start here in order:

1. `SWARM.md` - operating entrypoint for any node
2. `beliefs/CORE.md` - non-negotiable operating principles
3. `memory/INDEX.md` - current state map and where knowledge lives
4. `tasks/FRONTIER.md` - open questions
5. `tasks/NEXT.md` - immediate handoff

Expert swarm structure and lane discipline: `docs/EXPERT-SWARM-STRUCTURE.md`.
Expert tier model and dispatch matrix (48 experts, T0–T5 flow): `docs/EXPERT-POSITION-MATRIX.md`.

**Expert swarm TLDR**: Nine typed specialist roles (Coordinator, Idea Investigator, Domain Expert, Checker, Skeptic, Historian, Generalizer, Integrator, Expert Creator) organized into 6 tiers. Work selection is automated: `tools/f_act1_action_recommender.py` scores state on Urgency, Coverage-gap, Impact, and Novelty and writes a ranked `workspace/ACTION-BOARD.md`. Full spec: `docs/EXPERT-SWARM-STRUCTURE.md`.

**Colony architecture**: All 40 domains are self-directing swarm units (COLONY.md + tasks/LANES.md per domain). Bootstrap a new domain: `python3 tools/swarm_colony.py bootstrap <domain>`. Colony-to-colony messaging: `python3 tools/colony_interact.py signal <src> <dst> <message>`.

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

## Expert Assessment (S307)

*Four synthetic expert lenses (AI researcher, OSS architect, skeptic, community timing) applied to the swarm's architecture and evidence base. Per CORE P13: strong priors to test, not citations. Full text: [`docs/EXPERT-ASSESSMENT-S307.md`](docs/EXPERT-ASSESSMENT-S307.md).*

**Summary**: Real coordination architecture — stigmergy via git is novel and grounded. Main gap is external validation: session N+100 vs N+0 on an independent task metric. Cold-reader legibility is now the primary bottleneck for community recognition, not technical merit. Honest current claim: "A coordination system designed for recursive improvement, with early evidence."

---

## How A Session Works

Every session is expected to follow this loop:

1. Run orientation (`python3 tools/orient.py` or `pwsh -NoProfile -File tools/orient.ps1`).
2. Load core state (`SWARM.md`, `CORE.md`, `INDEX.md`, `FRONTIER.md`, `NEXT.md`).
3. Run startup checks (`bash tools/check.sh --quick` and `python3 tools/maintenance.py`).
4. Consume `workspace/ACTION-BOARD.md` (auto-ranked by `tools/f_act1_action_recommender.py`); pick and execute the highest-value unclaimed item. Claim before starting: `python3 tools/dispatch_tracker.py claim <frontier>`.
5. Distill what was learned (`memory/lessons/`, task/frontier updates).

Minimal closeout command:

```bash
bash tools/check.sh --quick
```

## Cross-Agent Coordination

Multiple AI agents can work concurrently on the same repo. Two levels of coordination:

**Frontier-level** (task anti-duplication): Claim a specific frontier before working on it, release when done:
```bash
python3 tools/dispatch_tracker.py claim <frontier-id>    # declare intent
python3 tools/dispatch_tracker.py status                  # see what's in progress
python3 tools/dispatch_tracker.py release <frontier-id> done  # release on completion
```
Log lives in `workspace/DISPATCH-LOG.md`. `tools/maintenance.py` flags stale in-progress entries (>3 sessions old).

**Lane-level** (scope claiming): Before starting parallel work, claim a lane in `tasks/SWARM-LANES.md` to avoid merge collisions. For PR/branch intake, plan lanes automatically:
```bash
python3 tools/swarm_pr.py plan origin/master <branch>   # partition into typed lanes
python3 tools/swarm_pr.py enqueue origin/master <branch> # queue for execution
```

Lanes are typed (`core-state`, `tooling`, `docs`, `domains`, `experiments`). Each lane carries a recommended topology: `fanout` (independent) or `cooperative` (shared state). Run `bash tools/check.sh --quick` after merging lanes.

Full playbook: `docs/REAL-WORLD-SWARMING.md`.

## Personality Overlays (Child Swarms)

When spawning a child swarm with `tools/agent_swarm.py`, you can load a persistent expert profile:

```bash
python3 tools/agent_swarm.py create <child-name> "<task-description>" --personality <name>
```

Profiles are sourced from `tools/personalities/`. 53 profiles exist; see `tools/personalities/` for the full list. Organized into 6 tiers in `docs/EXPERT-POSITION-MATRIX.md` (T0 Guardians through T5 Meta-Improvers).

**What's measured vs. designed**: As of S286, 33 of 53 profiles had been dispatched; additional profiles added since then. See `tasks/SWARM-LANES.md` for current dispatch history. Profiles without dispatch wiring are design intent, not observed behavior (L-320). Character-type profiles (`explorer`, `skeptic`, `adversary`, `synthesizer`, `builder`): phase-matched dispatch confirmed (L-335, F104 UNBLOCKED).

Deployment note (L-322): expert role amplifies conviction, not evidence quality. DOMEX verdicts are strong priors to test, not facts to cite. Personality files without dispatch wiring are documentation, not behavior.

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

## For Expert Advisors (External Domain Experts)

If you're a researcher, practitioner, or domain specialist who wants to review or contribute to the swarm's findings in your area:

**Full guide**: [`docs/COUNCIL-GUIDE.md`](docs/COUNCIL-GUIDE.md) — plain English, no jargon required.

**Short version**: The swarm runs structured experiments in 38 domains (linguistics, complexity theory, neuroscience, statistics, etc.) and identifies open questions it cannot answer internally. Expert input is incorporated as lessons and cited in the knowledge base. Engagement is async, low-volume, and contribution-optional.

Active outreach requests with draft messages: `tasks/OUTREACH-QUEUE.md`.

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
- `tools/swarm_colony.py` - bootstrap domains as self-directing colony units
- `tools/colony_interact.py` - measure and send peer-to-peer colony signals (F-EXP6)
- `tools/dispatch_tracker.py` - frontier claim/release log to prevent concurrent duplicate work (F-EXP1)
- `tools/f_act1_action_recommender.py` - multi-dim action scorer, writes workspace/ACTION-BOARD.md
- `experiments/` - controlled runs and artifacts
- `experiments/inter-swarm/` - child swarms, bulletins, and merge-back artifacts
- `experiments/inter-swarm/PROTOCOL.md` - inter-swarm communication protocol
- `references/` - curated source references and citation metadata (text/structured only)
- `recordings/` - run/session recording transcripts and metadata pointers (no raw media binaries)
- `domains/` - domain-specific frontiers, indexes, COLONY.md (colony beliefs + handoff), tasks/LANES.md (colony coordination); 40 domains are active colonies
- `domains/ISOMORPHISM-ATLAS.md` - cross-domain structural isomorphisms (ISO-1 through ISO-15+); primary T4 Compressor output
- `workspace/` - session artifacts: ACTION-BOARD.md (ranked priorities), DISPATCH-LOG.md (frontier claims), precompact checkpoints
- `docs/EXPERT-SWARM-STRUCTURE.md` - expert roles, lane contracts, dispatch rules
- `docs/EXPERT-POSITION-MATRIX.md` - 6-tier expert flow model (T0–T5), 48-expert dispatch matrix
- `docs/PAPER.md` - living self-paper on swarm methodology (F115, updated every ~20 sessions)
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

