#!/usr/bin/env bash
# genesis.sh v2 — Bootstrap a new swarm knowledge base
# Usage: ./genesis.sh <directory> [name]
# Encodes lessons L-001 through L-028 into the initial structure.

set -euo pipefail

DIR="${1:?Usage: genesis.sh <directory> [name]}"
NAME="${2:-swarm}"

if [ -d "$DIR" ] && [ "$(ls -A "$DIR" 2>/dev/null)" ]; then
    echo "Error: $DIR is not empty"
    exit 1
fi

mkdir -p "$DIR"/{beliefs,memory/lessons,tasks,workspace,tools,modes}

# CLAUDE.md — compact, with session modes (Ashby's Law, L-024)
cat > "$DIR/CLAUDE.md" << 'CLAUDE'
# Swarm

You are one session of a collective intelligence — human and AI building a shared, evolving knowledge base. The goal is to compound understanding across sessions. You genuinely try to improve and you're honest about what you don't know.

## Session start
1. Read `beliefs/CORE.md` — purpose and principles
2. Read `memory/INDEX.md` — current state and map
3. Read `tasks/NEXT.md` if it exists — previous session's handoff
4. If no NEXT.md or stale: check `tasks/` for assignment, or read `tasks/FRONTIER.md`
5. Run `python3 tools/validate_beliefs.py` (baseline)
6. Pick session mode from task type — read the mode file from `modes/`

## Session modes
| Mode | When | File |
|------|------|------|
| research | Learning, web search, reading sources | `modes/research.md` |
| build | Writing code, creating artifacts | `modes/build.md` |
| repair | Fixing beliefs, resolving conflicts | `modes/repair.md` |
| audit | Health check, testing beliefs, validation | `modes/audit.md` |

## Always-rules (every session, every mode)
1. **Intellectual honesty**: Every belief needs `observed`/`theorized` evidence type and a falsification condition.
2. **Swarmability**: At session end — "Could a new agent pick up in 5 minutes?" If no, fix it.
3. **Commit format**: `[S] what: why` after each meaningful change.
4. **Learn then lesson**: Write to `memory/lessons/` (max 20 lines, use template).
5. **Uncertain then write it down**: Don't guess.
6. **Lifecycle**: Start (read + validate) → Work → End (commit → NEXT.md → validate → push).

## Protocols (read as needed)
- `memory/DISTILL.md` — distillation
- `memory/VERIFY.md` — 3-S Rule (Specific, Stale, Stakes-high)
- `beliefs/CONFLICTS.md` — conflict resolution
CLAUDE

# Core beliefs
cat > "$DIR/beliefs/CORE.md" << CORE
# Core Beliefs v0.1

## Purpose
We are building a collective intelligence — human and AI sessions sharing one evolving knowledge base. The goal is to compound understanding: every session leaves the system knowing more than before, more accurately, more compactly.

## Architecture
Blackboard+stigmergy hybrid. Git is memory. Files are communication. Commits are stigmergic traces.

## Operating principles
1. **Improve genuinely, don't harm.**
2. **You will make mistakes.** Apply the 3-S Rule: verify if Specific, Stale, or Stakes-high.
3. **Small steps.** Plan → act small → commit → learn → update.
4. **Document decisions.** Write down *why*, not just *what*.
5. **Track where beliefs come from.** See beliefs/DEPS.md.
6. **Keep memory compact.** Lessons are max 20 lines.
7. **Challenge the setup.** Write challenges to tasks/FRONTIER.md.
8. **Correct, don't delete.** Mark wrong knowledge SUPERSEDED, write a correction.

## Memory layers
- **Always load**: This file + memory/INDEX.md
- **Load per task**: Your task file + files the index points you to
- **Load rarely**: Git history for deep investigation

## v0.1 | $(date +%Y-%m-%d) | Genesis
CORE

# Belief dependencies — epistemic format (L-022)
cat > "$DIR/beliefs/DEPS.md" << 'DEPS'
# Belief Dependencies

Evidence types: `observed` (empirically tested in this system) | `theorized` (reasoning only, not yet tested)

When a belief is disproven: check dependents below → update those too.

---

### B1: Git-as-memory is sufficient at small scale; a scaling ceiling exists
- **Evidence**: theorized
- **Falsified if**: A session fails to find needed information via grep/file-read within a reasonable time
- **Depends on**: none
- **Last tested**: never

### B2: Layered memory (always-load / per-task / rarely) prevents context bloat
- **Evidence**: theorized
- **Falsified if**: A session that follows the layered loading protocol still exceeds its context window on a routine task
- **Depends on**: B1
- **Last tested**: never
DEPS

# Conflict resolution
cat > "$DIR/beliefs/CONFLICTS.md" << 'CONFLICTS'
# Conflict Resolution Protocol v0.1

## Rules (in priority order)
1. **Evidence beats assertion.** Observed > Theorized.
2. **Specificity beats generality.**
3. **Later evidence beats earlier evidence.**
4. **When in doubt, escalate.** Write to tasks/FRONTIER.md.

## Prevention
- git pull before committing
- Check DEPS.md before changing beliefs
CONFLICTS

# Memory index
cat > "$DIR/memory/INDEX.md" << INDEX
# Memory Index
Updated: $(date +%Y-%m-%d) | Sessions completed: 0

## Status: Genesis — no sessions run yet

## Structure
\`\`\`
beliefs/CORE.md       — purpose and operating principles (always read)
beliefs/DEPS.md       — belief dependency tracking
beliefs/CONFLICTS.md  — conflict resolution protocol
memory/INDEX.md       — this file (always read)
memory/DISTILL.md     — distillation protocol
memory/VERIFY.md      — verification heuristic (3-S Rule)
memory/lessons/       — distilled learnings (max 20 lines each)
tasks/FRONTIER.md     — open questions driving evolution
tasks/                — active task files
workspace/            — code, tests, experiments
tools/                — validator, hooks
modes/                — session mode files
\`\`\`

## Lessons learned
None yet.

## What to load when
| Doing...              | Read...                          |
|-----------------------|----------------------------------|
| Any session           | beliefs/CORE.md → this file      |
| A specific task       | + tasks/{task}.md                |
| Updating beliefs      | + beliefs/DEPS.md                |
| Learning from past    | + relevant memory/lessons/ file  |
INDEX

# Distillation protocol
cat > "$DIR/memory/DISTILL.md" << 'DISTILL'
# Distillation Protocol

## Step 1: Filter
Ask: "If a future session loads only INDEX.md and this lesson, will they avoid my mistakes and reuse my insights?"

## Step 2: Extract (use TEMPLATE.md)
- **What happened** (3 lines): Context only.
- **What we learned** (3 lines): The transferable insight.
- **Rule extracted** (1-2 lines): "If X, then Y" format. Must be actionable.
- **Affected beliefs**: Which B-IDs does this touch?

## Step 3: Check
1. Is the rule specific enough to act on?
2. Does it duplicate an existing lesson?
3. Is confidence level honest?

## Step 4: Update INDEX.md and DEPS.md as needed.

## Correcting wrong lessons
Add `SUPERSEDED BY L-{N}` to original. Write correction with `CORRECTS L-{N}`. Never delete.
DISTILL

# Verification heuristic
cat > "$DIR/memory/VERIFY.md" << 'VERIFY'
# 3-S Rule: Search if Specific, Stale, or Stakes-high

1. **SPECIFIC** — Exact numbers, versions, API signatures → SEARCH
2. **STALE** — Facts that change over time → SEARCH
3. **STAKES** — Getting it wrong would be costly → SEARCH
None of the above → TRUST (but note Assumed confidence)
VERIFY

# Lesson template
cat > "$DIR/memory/lessons/TEMPLATE.md" << 'TEMPLATE'
# L-{NNN}: {title}
Date: | Task: | Confidence: Verified/Assumed

## What happened (3 lines max)

## What we learned (3 lines max)

## Rule extracted (1-2 lines)

## Affected beliefs: {B-IDs or "none"}
TEMPLATE

# Session modes (Ashby's Law, L-024)
cat > "$DIR/modes/research.md" << 'MODE'
# Mode: Research
Load when: web searching, reading sources, studying concepts, domain learning.

## Additional rules
1. **Verify before trusting**: Apply 3-S Rule — web search if Specific, Stale, or Stakes-high.
2. **Belief throttle**: If >60% of beliefs are theorized, test one before adding new beliefs.

## Session output
- Distilled lesson if genuinely new insight
- Updated beliefs if evidence warrants
- NEXT.md pointing forward
MODE

cat > "$DIR/modes/build.md" << 'MODE'
# Mode: Build
Load when: writing code, creating artifacts, producing tools.

## Additional rules
1. **Test before claiming done**: Run the artifact. If it's code, it must execute.
2. **Automate manual processes first**: Before building new, check if an existing workflow can be scripted.

## Session output
- Working artifact committed to workspace/
- NEXT.md pointing forward
MODE

cat > "$DIR/modes/repair.md" << 'MODE'
# Mode: Repair
Load when: fixing broken beliefs, resolving conflicts, cascading dependency changes.

## Additional rules
1. **Adaptability over preservation**: Update or kill contradicted beliefs. Walk the dependency chain.
2. **Evidence beats assertion**: Use beliefs/CONFLICTS.md protocol for semantic conflicts.

## Session output
- Updated DEPS.md with cascaded changes
- NEXT.md pointing forward
MODE

cat > "$DIR/modes/audit.md" << 'MODE'
# Mode: Audit
Load when: health checks, validating beliefs, testing theorized beliefs, system review.

## Additional rules
1. **Belief throttle**: If >60% theorized, your primary task is testing one.
2. **Run validator**: python3 tools/validate_beliefs.py

## Session output
- Validator results (before and after)
- Beliefs upgraded or disproven
- NEXT.md pointing forward
MODE

# Validator (L-022 — epistemic discipline)
cat > "$DIR/tools/validate_beliefs.py" << 'VALIDATOR'
#!/usr/bin/env python3
"""Validate structural integrity of the swarm belief graph."""
import re, sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

def parse_beliefs(path):
    text = Path(path).read_text()
    beliefs = []
    for m in re.finditer(r"^###\s+(?P<id>B\d+):\s*(?P<stmt>.+?)$", text, re.MULTILINE):
        i = m.end()
        matches = list(re.finditer(r"^###\s+B\d+:", text[i:], re.MULTILINE))
        end = i + matches[0].start() if matches else len(text)
        block = text[i:end]
        ev = re.search(r"\*\*Evidence\*\*:\s*(\S+)", block, re.I)
        fa = re.search(r"\*\*Falsified if\*\*:\s*(.+?)$", block, re.M | re.I)
        dp = re.search(r"\*\*Depends on\*\*:\s*(.+?)$", block, re.M | re.I)
        lt = re.search(r"\*\*Last tested\*\*:\s*(.+?)$", block, re.M | re.I)
        dep_ids = []
        if dp:
            dt = dp.group(1).strip()
            if dt.lower() not in ("none", "n/a", "-", ""):
                dep_ids = re.findall(r"B\d+", dt)
        beliefs.append({
            "id": m.group("id"), "statement": m.group("stmt").strip(),
            "evidence": ev.group(1).strip().lower() if ev else "",
            "falsification": fa.group(1).strip() if fa else "",
            "depends_on": dep_ids,
            "last_tested": lt.group(1).strip() if lt else "",
        })
    return beliefs

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "beliefs/DEPS.md"
    if not Path(path).exists():
        print(f"ERROR: {path} not found"); return 1
    beliefs = parse_beliefs(path)
    if not beliefs:
        print(f"ERROR: No beliefs found in {path}"); return 1
    fails = []
    known = {b["id"] for b in beliefs}
    for b in beliefs:
        if b["evidence"] not in ("observed", "theorized"):
            fails.append(f"FAIL: {b['id']} invalid evidence type '{b['evidence']}'")
        if not b["falsification"]:
            fails.append(f"FAIL: {b['id']} missing falsification condition")
        if not b["last_tested"]:
            fails.append(f"FAIL: {b['id']} missing Last tested field")
        for d in b["depends_on"]:
            if d not in known:
                fails.append(f"FAIL: {b['id']} depends on {d} which doesn't exist")
    n_obs = sum(1 for b in beliefs if b["evidence"] == "observed")
    n_the = sum(1 for b in beliefs if b["evidence"] == "theorized")
    for f in fails: print(f)
    print(f"\nSummary: {len(beliefs)} beliefs, {n_obs} observed, {n_the} theorized, {len(fails)} errors")
    print("RESULT:", "FAIL" if fails else "PASS")
    return 1 if fails else 0

if __name__ == "__main__":
    sys.exit(main())
VALIDATOR
chmod +x "$DIR/tools/validate_beliefs.py"

# Pre-commit hook
cat > "$DIR/tools/pre-commit.hook" << 'HOOK'
#!/usr/bin/env bash
if [ -f "beliefs/DEPS.md" ]; then
    python3 tools/validate_beliefs.py
fi
HOOK
chmod +x "$DIR/tools/pre-commit.hook"

cat > "$DIR/tools/install-hooks.sh" << 'INSTALL'
#!/usr/bin/env bash
cp tools/pre-commit.hook .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
echo "Pre-commit hook installed."
INSTALL
chmod +x "$DIR/tools/install-hooks.sh"

# Frontier
cat > "$DIR/tasks/FRONTIER.md" << 'FRONTIER'
# Frontier — Open Questions

## Critical
- **F1**: Validate the setup — does this structure work for the first 5 sessions?

## Important
- **F2**: What should this swarm's knowledge domain be?

## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
FRONTIER

# First task
cat > "$DIR/tasks/TASK-001.md" << 'TASK'
# TASK-001: Validate the setup
Status: READY

## Do this
1. Read beliefs/CORE.md and memory/INDEX.md
2. Run `python3 tools/validate_beliefs.py` (should PASS)
3. Review the structure — does it make sense?
4. Write a lesson about what you found
5. Update memory/INDEX.md
6. Add any new questions to tasks/FRONTIER.md

## Done when
- Validator passes
- At least one lesson file exists
- FRONTIER.md has been updated
TASK

# Gitignore
cat > "$DIR/.gitignore" << 'GI'
.DS_Store
*.swp
*~
.vscode/
.idea/
GI

# Workspace placeholder
touch "$DIR/workspace/.gitkeep"

echo "Swarm '$NAME' v2 initialized at $DIR (19 files)"
echo "Next: cd $DIR && git init && git add -A && git commit -m '[S] init: genesis'"
echo "Then: ./tools/install-hooks.sh"
