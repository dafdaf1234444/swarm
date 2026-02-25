# Compaction Protocol v0.1

## When to Compact
Run compaction when ANY trigger fires:
1. INDEX.md exceeds 60 lines
2. CLAUDE.md exceeds 60 lines
3. Total mandatory load (CLAUDE.md + CORE.md + INDEX.md) exceeds 200 lines
4. More than 25 lessons exist and INDEX still lists them individually
5. Swarmability "Context Efficiency" score drops below 10/20

## Compaction Levels (use the least aggressive level that solves the problem)

### Level 1: INDEX Compression (low risk)
Replace individual lesson lines with theme summaries.
Create `memory/themes/` directory. Each theme file lists its lessons with 1-line summaries.
INDEX.md points to themes, not individual lessons.
Result: INDEX drops from ~N lesson lines to ~5 theme lines.

### Level 2: CORE.md Integration (medium risk)
Stable lessons (observed beliefs, >10 sessions old) get their wisdom folded into CORE.md principles.
Remove corresponding INDEX entries. Do NOT delete lesson files (Rule 5).
Mark integrated lessons with `Integrated into CORE.md vX.X` header.

### Level 3: CLAUDE.md Extraction (requires care)
If CLAUDE.md exceeds 60 lines, extract detailed rules into separate files.
CLAUDE.md keeps ONLY: session start steps, rule NAMES with 1-line summaries, protocol pointers.
Detailed rule text moves to `memory/EPISTEMIC.md`.
Test Rule 7 after: can a new agent still onboard in 5 minutes?

### Level 4: Belief Consolidation (high risk, needs human review)
If DEPS.md exceeds 20 beliefs, look for mergeable pairs.
Two beliefs that always co-occur with same dependents can merge.
NEVER merge beliefs with different evidence levels.
Always propose in FRONTIER.md first.

## Safety Rules
- Run validator before AND after compaction
- Swarmability must not drop more than 5 points
- If validator breaks after compaction: `git checkout -- .` (revert everything)
- Never compact during an active shock experiment
- Human can protect any file by adding `NO-COMPACT` as first line
