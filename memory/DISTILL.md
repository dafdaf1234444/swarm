# Distillation Protocol v0.3

**Three modes**: (1) Inline — during work, when you learn something. (2) Task-completion — `task_distill.py` auto-generates from expect-act-diff. (3) Session-end — before final commit. Use (2) when you have structured expect/actual data; use (1)+(3) for insights without structured evidence.

## Step 0: Inline check — does this already exist? (run BEFORE writing a lesson)
Before writing a new lesson, scan `memory/PRINCIPLES.md`:
- Does an existing principle already capture this insight?
  - YES → **update the principle in-place** with the new evidence. No new lesson needed.
  - PARTIALLY → **extend the principle** with the new observation, then write a short lesson recording the evidence.
  - NO → continue to Step 1 and write the lesson.

This is the **continuous compaction** step. The goal: no two principles capture the same underlying truth. Merge before writing.

## Step 1: Filter — What did this session produce?
Ask: "If a future session loads only INDEX.md and this lesson, will they avoid repeating my mistakes and reuse my insights?"

- If YES → it's a real lesson. Write it.
- If NO → it's session noise. Skip it.

## Step 2: Extract — Fill the template
Use `memory/lessons/TEMPLATE.md`. Knowledge atom format (L-1292):

- **Title** = the falsifiable claim itself (not a description — the statement under test)
- **Typed relations** (use instead of flat `Cites:` when relation type is known):
  - `Supports:` — this evidence confirms those claims
  - `Contradicts:` — this evidence weakens those claims
  - `Extends:` — this builds on those claims
  - `Cites:` — untyped reference (backward compat, use when relation unclear)
- **Claim** (1-2 lines): The falsifiable statement. "If X then Y" or "X because Y."
- **Evidence** (3 lines): What specifically supports the claim? Include expected vs actual if from task.
- **Scope**: Where does this apply? Boundary conditions. Domain constraints.
- **Falsified-if**: Specific condition that would make this claim false.
- **Affected beliefs**: Which B-IDs in DEPS.md does this touch? If none, write "none."

## Step 2b: Task-completion pipeline (alternative to manual extraction)
When completing a task with expect-act-diff data, use `python3 tools/task_distill.py`:
```
python3 tools/task_distill.py --task "what was done" \
    --expect "expected outcome" --actual "actual outcome" \
    --domain DOMAIN --session SNNN [--supports L-NNN] [--contradicts L-NNN]
```
If surprise >= 0.3, generates a lesson candidate. If < 0.3, outputs a confirmation signal.
This closes the task→lesson feedback gap — completed work structurally produces learning artifacts.

## Step 3: Check — Quality gates
Before committing the lesson:
1. Is the rule extracted *specific enough to act on*? ("Be careful" fails. "Verify generated files for shell artifacts" passes.)
2. Does it duplicate an existing lesson? Check INDEX.md.
3. Is the confidence level honest? Mark Verified only if you tested/searched. Assumed otherwise.

## Step 3b: Post-lesson compaction check
After writing a lesson and its principle:
- Scan PRINCIPLES.md for any other principle this new one makes redundant or supersedes
- If found: mark the old one SUPERSEDED inline and point to the new one
- Goal: PRINCIPLES.md never grows without removing or merging an older entry for the same insight
- Metric: principles/lessons ratio should stay ≥ 1.0 (P-100)

## Note on child swarms
Children inherit `memory/PRINCIPLES.md` from the parent at spawn time. This is the minimal compressed context they need to avoid re-deriving known facts. Children should write bulletins when they find a principle worth merging back. Parent should run Step 0 when harvesting child findings.

## Step 4: Update the map
- Run `python3 tools/sync_state.py` to auto-sync counts/session headers/core hash across state files
- If `python3` is unavailable, run via your working launcher (`python`, `py -3`) or `bash tools/check.sh --quick`
- If the lesson changes a belief, update `beliefs/DEPS.md`
- If the lesson opens a new question, add it to `tasks/FRONTIER.md`

## When NOT to write a lesson
- Session only did mechanical work (formatting, renaming) with no insight
- The insight is already captured in an existing lesson
- You're uncertain whether the insight is real — write it to FRONTIER.md as a question instead

## Correcting a wrong lesson
If you discover an existing lesson is wrong (factually incorrect, outdated, overgeneralized, or misleading):
1. Add `**SUPERSEDED BY L-{NNN}**` as the first line of the original lesson
2. Write a new lesson with `CORRECTS L-{old}` in the "What happened" section
3. Explain *why* the original was wrong — the error is informative
4. Update INDEX.md: mark the old entry with ~~strikethrough~~ and add the new one
5. Never delete the original — it's part of the system's learning history
