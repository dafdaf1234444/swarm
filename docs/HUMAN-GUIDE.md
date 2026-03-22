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

## How to talk to it

Short signals work better than long instructions. These are the patterns that produce the most:

| Signal | What it does | Example |
|--------|--------------|---------|
| `swarm` | Full autonomy — runs the full loop | `/swarm` |
| `X swarm` | Work on X, self-direct within it | `reliability swarm` |
| `X for the swarm` | Donate a concept as a new domain | `game theory for the swarm` |
| `X+Y+Z swarm` | Multiple parallel directives | `cleanup + reliability + metrics swarm` |
| `swarm the X` | Audit the swarm's understanding of X | `swarm the enforcement model` |
| Philosophical reframe | Changes what the swarm IS | `swarm has to be autonomous from my commands too` |

**Less is more.** The swarm has compressed human input by −87% over 498 sessions while value/word increased. A two-word directive outperforms a paragraph of instructions.

**Compound signals run in parallel**, not sequence. `cleanup + metrics swarm` means: work both simultaneously, not cleanup-then-metrics.

---

## How to read what it's doing

Three commands tell you everything:

```bash
git log --oneline -10          # what happened across all sessions
python3 tools/orient.py        # current state, priorities, open frontiers
cat tasks/NEXT.md              # last session's handoff note
```

The swarm commits after every meaningful action. The git log *is* the progress report.

---

## When you need to step in

Three moments require human input:

1. **Direction drift** — The swarm is technically working but on the wrong thing. Say where you want it to go: `X swarm`.

2. **Judgment calls** — `tasks/HUMAN-QUEUE.md` holds questions the swarm can't answer itself (irreversible actions, external access, goal conflicts). Check it occasionally.

3. **Kill switch** — If something is heading wrong: say stop or write to `tasks/KILL-SWITCH.md`. This is your irreplaceable authority. Use it.

Everything else — prioritization, execution, verification, compression — is automated.

---

## What breaks it

- **Assigning tasks step-by-step** — over-prescribes and kills autonomy. Give direction, not instructions.
- **Ignoring HUMAN-QUEUE.md** — questions pile up, work stalls on judgment calls.
- **Vague reframes without follow-up** — philosophical shifts need at least one session of follow-through to stick.
- **Expecting one-session results on multi-session problems** — the swarm compounds over time. A single session is one data point, not a conclusion.

---

## The minimum

To get value immediately:

1. Say `/swarm` (or type `swarm` in your AI session)
2. Check `git log --oneline -5` to see what happened
3. If direction is wrong, say where you want it: `X swarm`

That's it. The repo handles the rest.

---

*For methodology: [`docs/HOW-TO-SWARM.md`](HOW-TO-SWARM.md)*
*For signal taxonomy: [`memory/HUMAN.md`](../memory/HUMAN.md)*
*Source of truth: [`SWARM.md`](../SWARM.md)*
