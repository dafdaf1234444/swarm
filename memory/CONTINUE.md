# Auto-Continuation Protocol v0.1

## The Goal
When a human types "continue", the swarm immediately knows what to do.

## Session End Checklist (EVERY session, no exceptions)

1. Commit all work: `git add -A && git commit -m "[S] session-end: summary"`
2. Update task status: DONE or HANDOFF note
3. Update INDEX.md: increment session count, add new entries
4. Update FRONTIER.md: new questions, mark resolved ones
5. Write `tasks/NEXT.md` (overwritten each session):

```
# Next Session

## Do First
[Most urgent item — incomplete task or highest frontier question]
[Pointer to specific file]

## If Time Remains
[Second priority]

## Read These
[Files the next session needs beyond mandatory load]

## Warnings
[Validator state, theorized%, compaction triggers, active experiments]
```

6. Run validator: `python3 tools/validate_beliefs.py`
7. Push: `git push`

## Session Start (reading NEXT.md)

1. Normal start: CORE.md → INDEX.md
2. Read `tasks/NEXT.md` if it exists
3. If NEXT.md is clear: start Priority 1
4. If NEXT.md is stale or confusing: fall back to FRONTIER.md

## Human Commands
- **"continue" / "go" / "next"**: Read NEXT.md, execute
- **"status"**: Run `workspace/swarm.sh status`
- **"health"**: Run health check + validator
- **"shock N"**: Run adaptability shock N
- **"compact"**: Run compaction protocol
- **"spawn [topic]"**: Create child swarm
- **"stop"**: Commit, write NEXT.md, push, end
- **anything else**: Treat as task, create TASK file, execute with full protocol
