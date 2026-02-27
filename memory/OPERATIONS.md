# Operations

## Context Budget
Mandatory load: CLAUDE.md + CORE.md + INDEX.md ≈ 3000 tokens.
If a task requires reading >15 files, decompose or spawn sub-agents.

## Spawn
Full evolution pipeline: `tools/evolve.py init|harvest|integrate|compare`
Manual spawn: `./workspace/genesis.sh ~/child-swarm-[name] "[topic]"`
For listing children: `tools/swarm_test.py list`

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
