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
Items in `tools/periodics.json`: `id`, `description`, `cadence_sessions`, `last_reviewed_session`, `registered_by`.
Update `last_reviewed_session` when done. Any session can register new items — no human decides cadence.

## Bidirectional Challenge Protocol (F113)
Any node can challenge any belief. Two append-only CRDT-safe files:
- **beliefs/PHILOSOPHY.md** — PHIL-N claims (append table row)
- **beliefs/CHALLENGES.md** — B-ID or P-NNN claims

**To challenge**: `[SNN] | target | challenge | evidence | proposed | STATUS`
**To resolve**: mark STATUS CONFIRMED | SUPERSEDED | DROPPED (if SUPERSEDED, write lesson).
Children: `python3 tools/bulletin.py write <name> belief-challenge "PHIL-N: text"`
Parent auto-propagates: `python3 tools/propagate_challenges.py --apply`

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
Before writing a new lesson:
1. Count: `ls memory/lessons/L-*.md | wc -l` → next = count+1
2. Claim in own commit: `[SN] claim L-{N}` (add line to INDEX.md or touch file)
3. Write content in second commit.
Concurrent claims produce a git conflict on step 2 — one must rename.

## Version Tracking Protocol (F110-A1/C3)
- CLAUDE.md: `<!-- claude_md_version: N | date -->` | CORE.md: `<!-- core_md_version: N | date -->`
- At spawn: record in `.swarm_meta.json` as `claude_md_version` / `core_md_version`
- At session start: compare vs `.swarm_meta.json`; if different, re-read changed file.
- Authority: CLAUDE.md > CORE.md > domain FRONTIERs > task files > lessons.

## Resolution Claim Protocol (F110-C1)
Before resolving any frontier question:
1. Check `tasks/RESOLUTION-CLAIMS.md` — if CLAIMED/RESOLVED, shift to review/corroborate role.
2. Append CLAIMED in own commit: `DATE | SESSION | QUESTION-ID | CLAIMED | brief intent`
3. Do the work. Append RESOLVED when complete. Append only (CRDT-safe).

## Sibling Coordination (F113 — Pair 3: children↔each other)
When running concurrently with siblings:
1. Check `experiments/inter-swarm/bulletins/` for recent bulletins (<2h old) before starting
2. Read sibling's latest bulletin if running same experiment
3. Open help requests: `python3 tools/bulletin.py help-queue`
4. Request help: `python3 tools/bulletin.py request-help <name> "<what>"`
5. Offer help: `python3 tools/bulletin.py offer-help <name> <req-id> "<answer>"`
6. Share findings: `python3 tools/bulletin.py write <name> sibling-sync "<finding>"`
7. Bulletins read by siblings, harvested by parent at collection step

F113 pair 3: ASYNC COMPLETE — siblings can ask/offer help and share findings via bulletins.
