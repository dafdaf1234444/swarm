# Operations — Session Lifecycle & Sustainability
Merged from: CONTEXT.md, COMPACT.md, CONTINUE.md, SPAWN.md (L-026)

## Context Budget
Mandatory load: CLAUDE.md + CORE.md + INDEX.md ≈ 3000 tokens (~2% of working context).
Real consumption comes from conversation history accumulation, not mandatory files.
If a task requires reading >15 files, decompose it or spawn sub-agents.

## Session End Checklist
1. Commit all work
2. Update task status (DONE or HANDOFF note in task file)
3. Update INDEX.md (session count, new lessons/themes)
4. Update FRONTIER.md (new questions, resolved ones)
5. Write `tasks/NEXT.md`:
   - Do First: most urgent item + file pointer
   - Read These: files beyond mandatory load
   - Warnings: validator state, theorized%, active experiments
6. Run validator
7. Push

## Emergency Handoff
If context feels constrained or you're losing track:
1. Commit everything with `[S] emergency-handoff: context limit approaching`
2. Write HANDOFF section in current task file (where stopped, what's next, files touched)
3. Update INDEX.md session count, write NEXT.md
4. Do NOT attempt distillation — just save state and stop. This is not failure.

## Compaction Triggers
Run compaction when ANY fires:
- INDEX.md exceeds 60 lines
- Total mandatory load exceeds 200 lines
- More than 45 lessons exist (next trigger after 31)
- Swarmability "Context Efficiency" drops below 10/20

Compaction method: replace individual lesson lines in INDEX.md with theme summaries.
Create `memory/themes/` if needed. Run validator before and after.

## Spawn (tested — genesis v3)
To create a child swarm: `./workspace/genesis.sh ~/child-swarm-[name] "[topic]"`
Scope it to <5 sessions. Child develops own beliefs. Merge back via parent session reading compressed findings.
For sub-swarm testing: use `tools/swarm_test.py` to spawn, run, and evaluate child swarms.
