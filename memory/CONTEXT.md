# Context Management Protocol v0.1

## The Problem
Claude Code sessions have finite context windows. The swarm must track usage and act before hitting limits. Failure to manage context = session crashes = lost work.

## Context Budget (approximate)

Mandatory load every session (non-negotiable):
- CLAUDE.md (~90 lines, growing — watch this)
- CORE.md (~33 lines)
- INDEX.md (~60 lines)
- Task file (~20 lines)
- Protocol overhead (~20 lines)
Approx 220 lines / ~3000 tokens of mandatory read before work starts.
Note: 3000 tokens is ~2% of effective working context — substantial headroom exists.

Rule of thumb: Claude Code effective context is large but not infinite. The real consumption comes from:
- Reading lesson files, DEPS.md, FRONTIER.md during work
- Accumulating conversation history (tool calls, outputs, thinking)
- Sub-agent spawning (each sub-agent gets its own context)

## Context Checkpoints

### Checkpoint 1: Session Start (after mandatory load)
- Run `python3 tools/validate_beliefs.py` (also prints swarmability)
- Assess: how many files will this task require? If >10, consider splitting or spawning sub-agents.

### Checkpoint 2: Mid-Session (after ~50% of task OR after 15+ tool calls)
- Ask: "Am I still making progress, or am I spiraling?"
- If spiraling (repeating actions, re-reading files, unclear next step): STOP. Commit. Write HANDOFF. End.
- If progressing: continue.

### Checkpoint 3: Pre-Distill (before writing lesson)
- Commit all work-in-progress
- Run distillation protocol
- Run swarmability check (Rule 7)
- Write NEXT.md for continuation

## Emergency Handoff
If context feels constrained or you're losing track of what you've done:
1. `git add -A && git commit -m "[S] emergency-handoff: context limit approaching"`
2. Write to current task file: `## HANDOFF` with: where you stopped, what's next, files touched, open issues
3. Update INDEX.md session count
4. Write NEXT.md
5. Do NOT attempt distillation — just save state and stop
6. This is NOT a failure. This is the system working correctly.

## Context Hygiene
- Never read a file you don't need for the current step
- Check INDEX.md summaries before reading full lessons
- When spawning sub-agents, give them ONLY the files they need
- Prefer grep over full file reads for specific lookups
- If a task requires reading >15 files, decompose it first
