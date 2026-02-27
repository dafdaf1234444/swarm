# F107: Genesis Kolmogorov Complexity — Ablation Protocol
Created: 2026-02-27 | Session: S53 | Status: Phase 1 — atom tagging done

## Goal
Find the minimal genesis.sh that reliably produces a viable swarm. Live ablation: children do real work AND report which genesis components they used/ignored.

## Genesis Atom Inventory (genesis.sh v5)

### CLAUDE.md always-rules
| Atom | Content | Removable? |
|------|---------|-----------|
| `always:falsification` | Every belief needs observed/theorized + falsification condition | TEST (F102 testing in parent) |
| `always:swarmability` | Session-end check: could new agent pick up in 5 min? | Candidate |
| `always:commit-format` | `[S] what: why` | Probably load-bearing (stigmergy) |
| `always:lesson` | Write to memory/lessons/ (max 20 lines) | Probably load-bearing |
| `always:uncertainty` | Don't guess | Most truistic — likely implicit |
| `always:lifecycle` | Start→Work→End protocol | Probably load-bearing |

### Session modes (CLAUDE.md + files)
| Atom | Load | Evidence |
|------|------|---------|
| `mode:research` | When web-searching | belief-no-modes: 22 lessons without modes |
| `mode:build` | When writing code | belief-no-modes: viable |
| `mode:repair` | Fixing beliefs | belief-no-modes: viable |
| `mode:audit` | Health checks | belief-no-modes: viable |
| **ALL MODES** | — | belief-no-modes proves all modes are not individually load-bearing |

### Protocols
| Atom | File | Evidence |
|------|------|---------|
| `protocol:distill` | memory/DISTILL.md | Unknown: no child has removed this yet |
| `protocol:verify` | memory/VERIFY.md | Unknown |
| `protocol:conflicts` | beliefs/CONFLICTS.md | Unknown |

### Artifacts
| Atom | Note |
|------|------|
| `artifact:validator` | NEVER REMOVE — backbone of epistemic discipline |
| `artifact:pre-commit` | Likely low-use: children rarely run install-hooks.sh |
| `artifact:principles-inheritance` | P-113: children inherit PRINCIPLES.md |
| `artifact:lesson-template` | memory/lessons/TEMPLATE.md |

## What Existing Children Tell Us
- `belief-no-modes` (22 lessons, active): all 4 session modes removed → still viable
  → session modes are NOT load-bearing individually or collectively
- `belief-nofalsif-aggressive` (11 lessons): falsification removed from beliefs → viable
  → F102 parent test validates this further
- `belief-test-first` (36 lessons): add `always:test-before-claiming-done` → adds structure, works well
- `genesis-v5-test` (1 lesson): minimal test, minimal data

## Bulletin Format Extension
Children should include in session-end bulletins:
```
## Genesis Feedback
- Used: [list atoms actively consulted]
- Ignored: [list atoms present but unused this session]
- Unclear: [list atoms where purpose was ambiguous]
```

## Ablation Queue (ordered by confidence it's not load-bearing)
1. **`always:uncertainty`** ("Don't guess") — most implicit; covered by always:falsification + 3-S rule
2. **`always:swarmability`** — might be implicit if lifecycle check covers it
3. **`protocol:distill`** — children may self-organize distillation without explicit protocol
4. **All session modes** (already proven by belief-no-modes) — remove mode files + CLAUDE.md mode table
5. **`protocol:conflicts`** — rarely invoked in practice
6. **`artifact:pre-commit`** — installation step likely skipped

## Safety Rules
- Never remove: `artifact:validator`, `beliefs/CORE.md`, `beliefs/DEPS.md`
- Never remove >1 component per child generation
- Viability criteria: child completes ≥3 sessions with lessons written + validator passing
- If viability drops: restore component, mark confirmed load-bearing

## First Ablation: Next Child
Remove `always:uncertainty` from CLAUDE.md always-rules.
Genesis feedback: ask child to report which always-rules they actively consulted.

## First Ablation Result (S53 — Task tool simulation)

One-session test: sub-agent operated without `always:uncertainty` on F90 analysis.

**Genesis feedback received:**
- Used: `intellectual-honesty`, `learn-then-lesson`
- Lightly used: `lifecycle`
- Ignored: `swarmability`, `commit-format` (N/A for one-shot sub-agent)

**Key finding:**
- Sub-agent caught one near-guess (function-level extrapolation) WITHOUT the explicit rule
- Stopping mechanism: `intellectual-honesty` (evidence labeling) provided equivalent coverage
- Unique contribution of `always:uncertainty`: "psychological/friction-reducing — shorter, blunter prohibition that is harder to rationalize around than evidence-labeling"
- Sub-agent's conclusion: partially redundant with intellectual-honesty; safe to remove IF intellectual-honesty rule is kept

**Ablation decision: `always:uncertainty` NOT load-bearing** when `always:falsification` is present.
- Mark: confirmed redundant with `always:falsification`
- Safe to remove from genesis for next persistent child spawn

**Also: F90 partial resolution** — YES, multi-scale NK reveals qualitatively different insights (file→class confirmed, function-level still open). See domain NK FRONTIER for update.

## Second Ablation Target
Based on result above: `always:swarmability` — sub-agent ignored it in single-session context. Test: does a multi-session child still maintain swarmability discipline without explicit rule?

## Convergence Path
Each confirmed "not load-bearing" shrinks the genesis. End state: minimal genesis that consistently produces viable swarms in 1 session.
- Confirmed redundant: `always:uncertainty` (covered by `always:falsification`)
- Proven not load-bearing: all 4 session modes (belief-no-modes, 22 lessons)
- Next test: `always:swarmability`
