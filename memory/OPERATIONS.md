# Operations

## Context Budget
Mandatory load: CLAUDE.md + CORE.md + INDEX.md ≈ 3000 tokens.
If a task requires reading >15 files, decompose or spawn sub-agents.

## Spawn
Full evolution pipeline: `tools/evolve.py init|harvest|integrate|compare`
Manual spawn: `./workspace/genesis.sh ~/child-swarm-[name] "[topic]"`
For listing children: `tools/swarm_test.py list`

## Maintenance
Run `python3 tools/maintenance.py` at session start. It checks all periodic conditions
(challenges, compaction thresholds, frontier decay, periodics, unpushed commits, etc.)
and surfaces what needs doing. The swarm reads its output as state and decides priority.

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
- INDEX.md exceeds 60 lines
- Total mandatory load exceeds 200 lines
- More than 45 lessons exist
- Swarmability drops

Method: replace individual entries with theme summaries. Run validator before and after.

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
3. If your findings would inform a sibling, write a coordination bulletin:
   `python3 tools/bulletin.py write <your-name> sibling-sync "<key-finding-one-line>"`
4. Coordination bulletins are read by siblings, harvested by parent at collection step

This closes the one-way parent→child flow for sibling coordination.
F113 pair 3 status: PARTIAL — siblings can share via bulletins; no real-time coordination mechanism.
