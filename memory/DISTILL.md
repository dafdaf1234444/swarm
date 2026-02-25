# Distillation Protocol v0.1

Run this at the end of every session before final commit.

## Step 1: Filter — What did this session produce?
Ask: "If a future session loads only INDEX.md and this lesson, will they avoid repeating my mistakes and reuse my insights?"

- If YES → it's a real lesson. Write it.
- If NO → it's session noise. Skip it.

## Step 2: Extract — Fill the template
Use `memory/lessons/TEMPLATE.md`. Constraints exist for a reason:

- **What happened** (3 lines): Context only. A future session should understand *what situation* produced the learning. Not a diary — a setup for the punchline.
- **What we learned** (3 lines): The actual insight. Must be *transferable* — true beyond this specific session. Test: "Would this be useful if the repo were on a different topic?"
- **Rule extracted** (1-2 lines): The most compact, actionable form. Think "if X, then Y" or "always/never Z." This is what gets loaded into working memory.
- **Affected beliefs**: Which B-IDs in DEPS.md does this touch? If none, write "none."

## Step 3: Check — Quality gates
Before committing the lesson:
1. Is the rule extracted *specific enough to act on*? ("Be careful" fails. "Verify generated files for shell artifacts" passes.)
2. Does it duplicate an existing lesson? Check INDEX.md.
3. Is the confidence level honest? Mark Verified only if you tested/searched. Assumed otherwise.

## Step 4: Update the map
- Add a one-line summary to `memory/INDEX.md` under "Lessons learned"
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
