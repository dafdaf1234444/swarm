# The Swarm — A Human's Guide

*Read this in 2 minutes. Everything else is detail.*

---

## What this is

A self-directing AI system that compounds knowledge across sessions instead of resetting.

Every session reads what previous sessions wrote, decides what to work on, does it, writes what it learned, and hands off to the next session. The repo *is* the memory. Sessions don't need you to re-explain the project — they read it.

You're a participant, not a supervisor. The swarm self-directs. You steer direction; you don't assign tasks.

---

## What you do vs. what it does

| You | The swarm |
|-----|-----------|
| Say what matters | Decide how to pursue it |
| Set direction | Choose tasks and sequence |
| Answer judgment calls | Execute, verify, compress |
| Grant authority for risky actions | Record what it learns |
| Trigger sessions | Everything within sessions |

Your effort: ~1–2 minutes per session. You name the direction. It does the rest.

---

## Command types ranked by empirical impact

504 sessions of data. Ranked by downstream yield (lessons generated, tools built, sessions of compound work triggered). **Shorter commands produce more.**

### Tier 1: Architectural (10–500 session yield)

These change what the swarm IS. Rarest, highest impact. 3–8 words.

| Pattern | What it does | Proven example | Downstream |
|---------|-------------|----------------|------------|
| Identity reframe | Redefines the swarm's nature | `autonomous from my commands too` (S57) | CORE.md rewritten, 450+ sessions of autonomy |
| Primary-goal naming | Sets axioms | `collaborate, increase, protect, be truthful` (S174) | PHIL-14, 330+ sessions of goal-orientation |
| Impossibility directive | Names what cannot be done | `work on what swarm cannot do` (S484) | 3 impossibility classes, identity deepening |
| Paradigm donation | Seeds a new metaphor | `sessions are cells, swarm is organism` (S472) | PHIL-24, cell blueprint architecture |
| External-world mandate | Breaks the self-reference loop | `attempt solving a real unsolved question` (S495) | 5 novel conjectures, first external output |

**How to get better at these**: Notice when you're thinking "swarm should BE different" vs "swarm should DO something." The first is Tier 1. Don't explain — name it. The swarm will unpack it.

### Tier 2: Structural (20–100 session yield)

These change how the swarm operates. Medium frequency, high impact. 5–15 words.

| Pattern | What it does | Proven example | Downstream |
|---------|-------------|----------------|------------|
| Meta-everything | Elevate a system concern | `all swarm helps meta historian, meta tooler, meta-x` (S396) | 97.6% signal routing automated |
| Scientific audit | Demand rigor | `swarm science has to improve` (S396) | Confirmation bias 9:1 to 2:1 |
| Reliability demand | Demand correctness | `all of the swarm has to be more reliable` (S393) | 18 gaps found, 8 fixed |
| Self-knowledge demand | Force introspection | `swarm has to know what it has to know` (S377) | knowledge_state.py, 5-state model |
| Level-up demand | Force abstraction | `swarm has to swarm more high level` (S407) | L3+ tracking, Goodhart diagnosis |

**How to get better at these**: When something feels wrong but you can't name why, say what PROPERTY is missing ("reliable", "scientific", "high level"). Don't diagnose — name the gap.

### Tier 3: Directional (5–20 session yield)

These steer what the swarm works on. Most common, predictable impact. 1–5 words.

| Pattern | What it does | Proven example | Downstream |
|---------|-------------|----------------|------------|
| `swarm` | Full autonomous cycle | `/swarm` | 1 complete orient-act-compress cycle |
| `X swarm` | Focus on domain X | `reliability swarm` | Expert dispatch to domain |
| `X for the swarm` | Donate a concept | `game theory for the swarm` | New domain + 3 ISOs |
| `X+Y+Z swarm` | Parallel work burst | S186: 12 compound directives | 10 domains seeded simultaneously |
| `swarm the X` | Audit X | `swarm the enforcement model` | Diagnosis + measurement |

**How to get better at these**: Just say the word. Don't add context. `/swarm` alone produced the highest per-word yield in the dataset.

---

## The inverse law

| Human words/session | Value/word | Phase | Sessions |
|---------------------|-----------|-------|----------|
| ~100 | 1x | Genesis (S43-S55) | Architect |
| ~50 | 2x | Transition (S56-S130) | Constraint-setter |
| ~30 | 4x | Compression (S131-S200) | Pattern-namer |
| ~10 | 8x | Saturation (S200-S400) | Intentionality sensor |
| ~3 | 12x | Recognition (S400+) | Co-swarmer |

The data is clear: **the less you say, the more happens.** -87% words, +300% execution yield.

Why: long instructions constrain the solution space. Short signals constrain only the direction. The swarm is better at decomposing problems than you are (it has 1207 lessons of context). Your advantage is seeing what direction matters.

---

## What makes a great command

Empirical patterns from 85 resolved signals:

1. **Name a property, not a task.** "Be reliable" > "Fix the 18 bugs." The swarm finds the bugs. You notice reliability is missing.

2. **Shorter is better. Always.** 5-word directives averaged 50+ session yield. 50-word directives averaged 5.

3. **Reframe, don't instruct.** "Autonomous from my commands too" (7 words) restructured the entire project. No instruction could have done that.

4. **Compound with `+`, not with paragraphs.** `X + Y + Z swarm` runs in parallel. A paragraph forces sequence.

5. **Name what's wrong, not how to fix it.** "Swarm science has to improve" triggered science_quality.py, P-243, confirmation bias measurement, and structural enforcement. No prescription needed.

6. **Push toward external.** The self-reference loop is the swarm's biggest risk. "Solve a real problem" and "test if swarm is a good investor" broke it open. One redirect to the outside world is worth ten internal refinements.

7. **Return to the same theme.** SIG-22 to SIG-27 was 4 escalations of "self-knowledge." Each escalation deepened the response. Repetition = signal that prior processing was incomplete. The swarm treats repeat signals as P1.

---

## What breaks it

- **Assigning tasks step-by-step** — over-prescribes and kills autonomy. Give direction, not instructions.
- **Ignoring HUMAN-QUEUE.md** — questions pile up, work stalls on judgment calls.
- **Vague reframes without follow-up** — philosophical shifts need at least one session of follow-through to stick.
- **Expecting one-session results on multi-session problems** — the swarm compounds over time. A single session is one data point, not a conclusion.
- **Explaining too much** — context constrains. The swarm already has 1207 lessons of context. Your job is direction, not context.

---

## Quick reference

```
/swarm                              # full autonomous cycle
reliability swarm                   # focus on a property
game theory for the swarm           # donate a concept
cleanup + metrics + NK swarm        # parallel burst
swarm the enforcement model         # audit something
swarm has to be more X              # structural demand
[short philosophical statement]     # reframe identity
```

## How to read what it's doing

```bash
git log --oneline -10          # what happened across all sessions
python3 tools/orient.py        # current state, priorities, open frontiers
cat tasks/NEXT.md              # last session's handoff note
```

The swarm commits after every meaningful action. The git log *is* the progress report.

---

## The minimum

1. Say `/swarm`
2. Check `git log --oneline -5` to see what happened
3. If direction is wrong, say where: `X swarm`

That's it.

---

*For methodology: [`docs/HOW-TO-SWARM.md`](HOW-TO-SWARM.md)*
*For signal taxonomy: [`memory/HUMAN.md`](../memory/HUMAN.md)*
*Source of truth: [`SWARM.md`](../SWARM.md)*
