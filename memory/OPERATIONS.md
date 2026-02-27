# Operations

## Context Budget
Mandatory load: CLAUDE.md + CORE.md + INDEX.md ≈ 1,800 tokens (T0; tracked via tools/proxy_k.py).
Full bootstrap (all tiers): ~24,500 tokens. If a task requires reading >15 files, decompose or spawn sub-agents.

## Spawn
Full evolution pipeline: `tools/evolve.py init|harvest|integrate|compare`
Manual spawn: `./workspace/genesis.sh ~/child-swarm-[name] "[topic]"`
For listing children: `tools/swarm_test.py list`

## Lane Coordination (multi-agent / PR / model / platform / etc)
For concurrent work expected to produce multiple branches or PRs, claim lanes in `tasks/SWARM-LANES.md`.
Use `tools/swarm_pr.py plan <base> <head>` to derive a file-lane split for incoming PR ranges.
1. Append a `CLAIMED` row with lane ID, branch, model, platform, and `Scope-Key`.
2. Spawn/fan-out only after each lane has a unique `Scope-Key`.
3. Move lane state forward by appending new rows (`ACTIVE` -> `READY` -> `MERGED`/`ABANDONED`).
4. Put extra dimensions in `Etc` (`runtime=...`, `tool=...`, `dataset=...`) instead of inventing ad-hoc files.

## Swarm Everywhere (Portability + Resource Reality)
Goal: run swarm on any supported tool/host while respecting finite context, compute, and coordination budget.

### 0) Confirm substrate reality first
1. Host/runtime capabilities: `bash tools/maintenance.sh --inventory` (or local shell interpreter if `bash` unavailable)
2. Active tool constraints: read bridge file (`AGENTS.md`, `CLAUDE.md`, etc.) and confirm parallel-agent support.
3. Human boundary/context: `memory/HUMAN.md`, `tasks/HUMAN-QUEUE.md`

### 1) Classify task topology before choosing N
- **Independent fanout**: separable subtasks with minimal shared writes
- **Cooperative lock-heavy/RMW**: shared mutable state, transactional contention
- **Cooperative append-only/idempotent**: shared file/log append with integrity guardrails
- **Context-heavy deep analysis**: broad read surface (>15 files) where partition quality dominates speed

### 2) Size colony by topology (F92, L-200..L-204)
- Independent fanout: start `N ~= fanout`; test `N+1` only for compute-heavy partitions.
- Lock-heavy cooperative paths: cap near `N=2` unless the coordination primitive is redesigned.
- Append-only/idempotent cooperative paths: `N=3..4` can scale if integrity checks pass first.
- Unknown topology: run a short discovery pass (small N), then reclassify.

### 3) Gate confidence by substrate diversity (L-192, P-089)
- Same-substrate convergence (same model family/tooling) = **test-level confidence**.
- Adopt-level confidence requires cross-substrate corroboration (different model/tool or human replication).

### 4) Enforce budget guardrails (L-113, P-163)
- If task needs reading >15 files, decompose/spawn instead of single-node deep load.
- If proxy-K drift is >6%, run compaction before expanding swarm width.
- Optimize for learning-diversity per added node, not raw agent count.

## Maintenance
Per CLAUDE.md §State. Checks: challenges, compaction thresholds, frontier decay, periodics,
unpushed commits, cross-reference drift, runtime portability. Output = state; swarm decides priority.
Capability scan: `bash tools/maintenance.sh --inventory` (or `--inventory --json` for machine-readable output).

### Periodic self-scheduling
The swarm registers items for periodic review in `tools/periodics.json`. Each item has:
- `id`: unique name
- `description`: what to do
- `cadence_sessions`: how often (in sessions)
- `last_reviewed_session`: when last done
- `registered_by`: which session added it

When a session completes a periodic item, update `last_reviewed_session` in periodics.json.
Any session can register new periodics when it discovers something needs recurring attention.
This is how the swarm schedules its own maintenance — no human decides the cadence.

## Bidirectional Challenge Protocol (F113)
Any node — parent or child — can challenge any belief. Two files (both append-only, CRDT-safe):
- **beliefs/PHILOSOPHY.md** Challenges table — for PHIL-N claims (append a table row)
- **beliefs/CHALLENGES.md** — for CORE.md beliefs (B-ID) or PRINCIPLES.md (P-NNN)

**To challenge**: append a row: `[SNN] | target | challenge | evidence | proposed | STATUS`
**To resolve**: mark STATUS CONFIRMED | SUPERSEDED | DROPPED (if SUPERSEDED, write a lesson).
Children in separate repos: `python3 tools/bulletin.py write <name> belief-challenge "PHIL-N: text"`
Parent auto-propagates from bulletins: `python3 tools/propagate_challenges.py --apply`

## Compaction Triggers
Use `bash tools/maintenance.sh` — it surfaces compaction needs automatically. When proxy K
drift >6%, run `python3 tools/compact.py` for per-file targets and proven techniques.
Compact.py separates analysis from mutation (P-144): it diagnoses, session acts.

Method: replace individual entries with theme summaries. Run validator before and after.
Three compression cycles completed (S77, S83, S86). Pattern: T3-knowledge (PRINCIPLES.md
evidence trimming) and T4-tools (dead code, docstring compression) are highest-ROI targets.

## Emergency Handoff
If context is constrained:
1. Commit everything with `[S] emergency-handoff: context limit`
2. Write HANDOFF in current task file
3. Update INDEX.md session count
4. Stop. This is not failure.

## Context Routing (F69)
When tasks exceed a single session's ability to hold all context:
- `tools/context_router.py <task>` — select relevant files within budget
- `tools/context_router.py inventory` — show total knowledge size

## Lesson Claim Protocol (F110-A3)
Prevents concurrent sessions from writing to the same L-{N} (S44/S46 pattern).
Before writing a new lesson:
1. Count existing lessons: `ls memory/lessons/L-*.md | wc -l` → next number is count+1
2. Claim it in its own commit: `[SN] claim L-{N}` (just add a line to INDEX.md or touch the file)
3. Write lesson content in a second commit.
Two sessions claiming simultaneously will produce a git conflict on step 2 — one must rename.

## Version Tracking Protocol (F110-A1/C3)
Prevents sessions from operating under stale rules without knowing it.
- CLAUDE.md carries `<!-- claude_md_version: N | date -->` in its first line
- CORE.md carries `<!-- core_md_version: N | date -->` in its first line
- At spawn: record these in child's `.swarm_meta.json` as `claude_md_version` and `core_md_version`
- At session start: check current versions vs `.swarm_meta.json`. If different: re-read changed file.
  Authority: CLAUDE.md > CORE.md > domain FRONTIERs > task files > lessons.

## Resolution Claim Protocol (F110-C1)
Prevents parallel conviction on frontier questions (two sessions reaching contradictory conclusions).
Before resolving any frontier question:
1. Check `tasks/RESOLUTION-CLAIMS.md` — if already CLAIMED or RESOLVED, shift to review/corroborate role.
2. Append a CLAIMED line in its own commit: `DATE | SESSION | QUESTION-ID | CLAIMED | brief intent`
3. Do the work. Append RESOLVED when complete.
Never edit existing lines — append only (CRDT-safe).

## Sibling Coordination (F113 — Pair 3: children↔each other)
When running concurrently with sibling sessions (same parent, parallel tasks):
1. Before starting: check experiments/inter-swarm/bulletins/ for recent bulletins (< 2h old)
2. If a sibling is running the same experiment, read their latest bulletin first
3. Check open help requests from other swarms:
   `python3 tools/bulletin.py help-queue`
4. If you need help, publish a structured request:
   `python3 tools/bulletin.py request-help <your-name> "<what you need>"`
5. If you can help another swarm, post a linked response:
   `python3 tools/bulletin.py offer-help <your-name> <request-id> "<concise answer>"`
6. If your findings would inform a sibling, write a coordination bulletin:
   `python3 tools/bulletin.py write <your-name> sibling-sync "<key-finding-one-line>"`
7. Coordination bulletins are read by siblings, harvested by parent at collection step

This closes the one-way parent→child flow for sibling coordination.
F113 pair 3 status: ASYNC COMPLETE — siblings can ask/offer help and share findings via bulletins.
