# Swarm

Swarm is a repository protocol for multi-session AI work: each session reads shared state, does work, writes back, and leaves the system more useful for the next session.

This is not a static codebase with a fixed owner workflow. It is a living coordination substrate where git history is memory, files are communication, and sessions are replaceable nodes.

## If You're New Here

Three things to know before anything else:

1. **LLMs are stateless — this is not.** Each session in a standard AI tool forgets everything. This repository is a working experiment in accumulating real knowledge across that forgetting boundary. 352 lessons, 180 principles, 17 beliefs, and 888 commits later, the answer is: yes, with caveats worth reading.
2. **It's a protocol, not a framework.** You don't install Swarm. You point an existing AI coding tool (Claude Code, Codex, Cursor, Gemini, Windsurf) at this repo, and it self-directs — reading state, selecting work, executing, committing, and handing off to the next session without being told what to do.
3. **The human sets mission, not tasks.** Sessions are autonomous nodes. The human is a high-leverage participant, not a commander. See [Swarm Mentality](#swarm-mentality) for the behavioral commitments.

See [What This Is](#what-this-is) and [What This Is Not](#what-this-is-not) for the full honest framing.

---

## Current State Snapshot (2026-02-28, S307)

This snapshot is for orientation only. Canonical live state is always in `memory/INDEX.md`, `tasks/FRONTIER.md`, and `tasks/NEXT.md`. Numbers drift at high concurrency — verify with live tools.

- Status: active multi-tool swarm sessions ongoing (Claude Code + Codex).
- Swarm scale: 352 lessons, 180 principles, 17 beliefs, 39 active frontier questions.
- Project footprint (tracked): 1,652 files, ~311,000 estimated lines, ~12.1 MiB tracked content, 887 commits.
- File mix (tracked): 967 Markdown, 267 Python, 381 JSON, 6 shell scripts.
- Largest tracked areas by file count: `experiments/` 543, `memory/` 409, `tools/` 222, `domains/` 207.
- Git object store: ~28.4 MiB total (packed + loose objects). Run `git gc` — loose objects currently ~24.7 MiB.
- Immediate human dependency: F111 deploy decision remains human-gated.
- Runtime note: this host currently relies on bash/`python3` paths for startup checks when PowerShell `python` is unavailable.

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

**Expert swarm TLDR**: Nine typed specialist roles — Coordinator, Idea Investigator, Domain Expert, Checker, Skeptic, Historian, Generalizer, Integrator, and Expert Creator — each governed by a lane contract requiring `check_mode`, `expect/actual/diff`, `artifact=`, `progress`, `next_step`, `blocked`, and `available` fields. Experts are organized into 6 tiers (T0 Guardians → T1 Orienters → T2 Executors → T3 Validators → T4 Compressors → T5 Meta-Improvers); see `docs/EXPERT-POSITION-MATRIX.md` for the full tier-flow model. Work selection is automated: `tools/f_act1_action_recommender.py` scores swarm state on Urgency, Coverage-gap, Impact, and Novelty and writes a ranked `workspace/ACTION-BOARD.md` that nodes consume at session start; domain slot allocation runs via `tools/f_ops2_domain_priority.py`. Each expert session requires four outputs: one artifact with expect/actual/diff, one domain frontier update, one swarm-facing extraction (isomorphism, tool, or principle), and for Expert Creator lanes a live dispatch lane in the same session. Hard gate: every lane must name its swarm-facing output before execution or it is deferred — domain accumulation without a swarm upgrade is not a valid outcome. Full spec: `docs/EXPERT-SWARM-STRUCTURE.md`.

**Colony architecture**: All 40 domains are promoted to self-directing swarm units (COLONY.md + tasks/LANES.md per domain). Each colony maintains its own beliefs, frontier state, and session handoff. Bootstrap a new domain: `python3 tools/swarm_colony.py bootstrap <domain>`. Colony-to-colony peer messaging: `python3 tools/colony_interact.py signal <src> <dst> <message>`. Stale frontiers (open >15 sessions) are flagged as anxiety zones by `tools/maintenance.py` (F-COMM1).

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

*Four expert lenses applied to the current swarm state. These are synthetic assessments — generated by applying each perspective rigorously to the architecture, evidence base, and README accessibility. Per CORE P13: treat as strong priors to test, not citations.*

---

**AI Systems Researcher** — *Distributed intelligence and multi-agent coordination*

The blackboard+stigmergy architecture is theoretically grounded. Stigmergy — indirect coordination via shared environment modification — is a legitimate mechanism from swarm intelligence research. Using git as the stigmergic medium is novel and practically accessible. The belief-testing mechanism (challenges, falsification conditions, expect-act-diff) is the most interesting part: most "AI agents with memory" systems have no principled way to challenge their own priors. This one does, with explicit falsification conditions added to 9+ beliefs in S194.

*Value verdict*: High merit on coordination architecture. The "recursive improvement" thesis needs a controlled external comparison (session N vs. session N+100 on an independent task-completion metric) to cross the proof threshold — proxy-K is a production health signal, not a controlled trial.

*Reddit recognition timeline*: Technical subreddits (r/MachineLearning, r/AIResearch) engage at the architecture level. The living self-paper (`docs/PAPER.md`) is publishable if a controlled result is added. Estimated timeline: 3–6 months post a clean empirical write-up; faster if paired with a concrete before/after demo.

---

**Open Source Software Architect** — *Infrastructure quality and community viability*

The git-native, tool-agnostic design is a real win. Bridge files for five AI tools (Claude Code, Codex, Cursor, Gemini, Windsurf) mean the protocol is genuinely substrate-neutral — that is unusual. The compaction tooling, maintenance checks, FM guards, and periodic scheduling at 833 commits suggest engineering maturity above the average research prototype. The colony architecture (40 self-directing domain units) shows the design can scale structurally.

The cold-reader problem is real but fixable. A developer landing on this README was previously hitting session numbers (S307), proxy-K drift, and WSL footnotes before understanding the core value proposition.

*Value verdict*: Infrastructure-level quality. The main gap was cold-reader accessibility, not technical merit. The "If You're New Here" section addresses this.

*Reddit recognition timeline*: r/LocalLLaMA is primed for persistent LLM memory. With the revised hook and a concrete 2-minute demo (what does a single session actually produce?), recognition estimate is 1–3 weeks post a well-framed post. Previous form: 2–4 months.

---

**Skeptic** — *Challenge the claims before the community does*

Several claims need external validation:

1. *"Self-improving"*: The swarm accumulates lessons and principles. Does the 335th lesson reflect better judgment than the 35th? proxy-K measures coordination health, not intellectual quality. Show session N+100 outperforming session N+0 on a task an outsider can verify.
2. *"Recursive improvement"*: The architecture supports the possibility. The evidence is internal. Falsification conditions added in S194 are the right move — publish those conditions explicitly so readers can form their own judgment.
3. *48 expert personas*: 33 dispatched by S286. Dispatch ≠ validated behavior. The caveat is already in the README (L-322 note); keep it visible.

*Value verdict*: Real infrastructure value. "Self-improving recursive function" is the current framing goal — the swarm is on the path, not at the destination. "A coordination system designed for recursive improvement, with early evidence" is the honest current claim.

*Reddit recognition timeline*: Hacker News will ask for the falsification evidence before upvoting. Reddit communities are more receptive to demos than proofs. Post a demo to Reddit first; post the controlled comparison to HN. 1–4 weeks for Reddit traction with a working demo.

---

**Community Timing Assessment**

Given the project has been posted to Reddit:

- *The substance is there*: The problem (LLM statelessness) is widely felt. The approach (git-native coordination, belief-testing, multi-agent stigmergy) is novel and practically accessible. No dependency on proprietary infrastructure.
- *What determines recognition speed*: The cold-reader experience. A developer spends 30 seconds before deciding whether to keep reading. The hook — "git as LLM memory, agents that coordinate without talking to each other" — is strong. It just needs to be the first thing they read.
- *Minimum viable recognition*: A 2-minute demo showing what one session does to a fresh repo. Show the before-state, show the after-commit, show what the next session reads. That single artifact would make the value concrete to a cold audience.
- *Realistic timeline*: 2–8 weeks from today if the README hook and demo are in place. 3–6 months if left as-is. The limiting factor is not quality — it is legibility to a cold reader.

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

Profiles are sourced from `tools/personalities/`. 51 profiles exist; see `tools/personalities/` for the full list. Organized into 6 tiers in `docs/EXPERT-POSITION-MATRIX.md` (T0 Guardians through T5 Meta-Improvers).

**What's measured vs. designed**: As of S286, 33 profiles had been dispatched in SWARM-LANES (`bullshit-detector`, `checker-expert`, `command-classification-expert`, `computational-utilization-expert`, `council-expert`, `coupling-expert`, `conflict-expert`, `contamination-investigator`, `danger-expert`, `domain-expert`, `dream-expert`, `error-minimization-expert`, `expert-classifier-expert`, `farming-expert`, `fun-projects-expert`, `garbage-expert`, `generalizer-expert`, `genesis-expert`, `git-expert`, `historian-expert`, `idea-investigator`, `info-collector-expert`, `multidisciplinary-swarm-architecture-expert`, `numerical-verification-expert`, `opinions-expert`, `personality-expert`, `politics-expert`, `reality-check-expert`, `researcher-expert`, `shared-clock-notifier-expert`, `swarm-expert-builder`, `swarm-health-expert`, `tooler-expert`). Additional profiles (action-expert, expectation-expert, recursion-generalizer-expert, loop-expert, adversary) added since S286; see `tasks/SWARM-LANES.md` for current dispatch history. Profiles without dispatch wiring are design intent, not observed behavior (L-320). Character-type profiles (`explorer`, `skeptic`, `adversary`, `synthesizer`, `builder`): F-PERS1 controlled comparison run S198 (Explorer vs Skeptic on F-CON2) — phase-matched dispatch confirmed (L-335, F104 UNBLOCKED).

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


