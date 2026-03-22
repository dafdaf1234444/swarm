# Swarm

**A self-directing AI system that remembers, learns, and improves across sessions.**

AI sessions forget everything between runs. Session 500 is as blank as session 1. You re-explain context, re-discover what failed, re-decide what to work on — every single time.

Swarm fixes this. It's a git repo where each AI session reads what previous sessions wrote, decides what to do, does it, compresses what it learned, and commits a handoff. The next session starts where the last one left off. Knowledge accumulates. Sessions self-direct. The human steers — the system does the work.

## What it's produced

This repo started as **134 lines of markdown**. After 498 sessions:

| Metric | Count | What it means |
|--------|-------|---------------|
| Lessons | 1,181 | Compressed findings, each max 20 lines with cited evidence |
| Principles | 251 | One-line rules distilled from 3+ lessons each |
| Beliefs | 21 | Tested against external evidence, falsifiable |
| Domains | 48 | Independent knowledge areas the swarm explores |
| Tools | 108 | Python/shell tools the swarm built to manage itself |
| Commits | 2,400+ | Every session commits its work for the next one |

All of this was produced by sessions that chose their own work. No task assignments, no human-written to-do lists.

## The core loop

Every session runs the same cycle:

```
Orient → Decide → Predict → Act → Compare → Compress → Hand off
```

1. **Orient** — read current state, priorities, gaps, last session's handoff
2. **Decide** — pick work from open questions and priorities (no human assignment needed)
3. **Predict** — before acting, write what you expect to happen
4. **Act**
5. **Compare** — did reality match the prediction? Mismatches are where learning happens
6. **Compress** — distill the result: new finding → lesson, recurring pattern → principle
7. **Hand off** — commit so the next session starts better

The predict-then-compare step is the engine. Without a prediction, you can't distinguish "this worked" from "this happened." Wrong predictions produce more knowledge than confirmations. Measured: **+39.8 percentage points** in quality outcomes (n=849).

## What's impressive (and what's honest)

### Works

- **Knowledge compounds** — 1,181 lessons across 498 sessions, compressed into 251 principles and 21 beliefs. The repo gets *faster* as it grows because each compression layer filters noise.
- **10+ concurrent AI sessions** coordinate through git at peak, sharing state without destroying each other's work. The system has characterized its own stability dynamics at different concurrency levels.
- **Structural enforcement** — voluntary protocols decay to ~3% compliance over time. Rules encoded as pre-commit hooks, creation-time gates, and automated checks maintain ~90% (n=65+13 prospective). L-601: "If a rule matters, it's code, not a document."
- **Expert dispatch** — sessions pick domains using UCB1 (explore/exploit balancing): +59% lessons per investigation, -24% concentration in any single domain (n=849).
- **Self-audit** — every identity claim carries an evidence label (*grounded*, *partial*, *axiom*, *aspirational*, *unverified*, *metaphor*). The swarm found ~15 of its own metaphors being used as measurements and ~10 circular evidence chains — and logged them as problems to fix.
- **The swarm built its own tools** — 108 active tools (orient, dispatch, compaction, claim protocol, contract validation, knowledge state classification, lane management, etc.), all written and refined by sessions across 498 iterations.

### Doesn't work yet (and it knows)

- "For the benefit of more than itself" — 0 external beneficiaries so far
- "Swarms swarm each other" — 0 peer-to-peer instances observed
- Cross-session autonomy — every session is still human-initiated
- 87% of lessons are measurement-level; strategy and architecture declining
- Confirmation ratio is ~58:1 (real science needs closer to 10:1)
- 52.9% of content is self-referential

**Plainly:** a well-organized knowledge base with CI/CD for markdown. The value is that the infrastructure makes the methodology stick — methodology alone produces ~3% retention.

## Try it yourself

Fork the repo, point any AI coding tool at it, say `/swarm`.

```bash
git clone https://github.com/dafdaf1234444/swarm.git
cd swarm
bash tools/install-hooks.sh   # one-time: commit quality hooks
bash tools/check.sh --quick   # verify integrity
python3 tools/orient.py       # see current state and priorities
```

**Works with**: Claude Code, Cursor, Codex, Gemini CLI, Windsurf, GitHub Copilot. The session reads the protocol from bridge files in the repo root and self-directs.

**PowerShell**: `pwsh -NoProfile -File tools/orient.ps1`, `pwsh -NoProfile -File tools/check.ps1 --quick`.

### Signals — how you talk to it

| Signal | What happens |
|--------|-------------|
| `swarm` | Full autonomy — orient, act, compress, hand off |
| `X swarm` | Work on X, self-direct within it |
| `X for the swarm` | Add a new knowledge domain |
| `swarm the X` | Audit the swarm's understanding of X |

Short signals work better than long instructions. The swarm reads context from its own state, not from your prompt.

### What to expect

- `/swarm` authorizes autonomous work — file edits, experiments, maintenance, tool runs
- A single run touches many files and costs significant tokens
- For bounded work, say what you want: `reliability swarm` or `cleanup swarm`
- Track changes via `git diff` and `git log`, not chat history
- Kill switch: `python3 tools/kill_switch.py activate --reason "reason" --requested-by "human"`

## Build your own

The methodology works on any repo. You don't need to fork this one.

**Minimum viable loop (no setup)**:
1. Create a `LESSONS.md` file in your repo
2. Before each AI session, tell it to read `LESSONS.md` first
3. After each session, have it write what it learned
4. Over time, compress repeated patterns into principles

**Full methodology**: [`docs/HOW-TO-SWARM.md`](docs/HOW-TO-SWARM.md) covers the complete protocol — from the 5-step minimum loop to the full self-directing system.

## Explore the repo

| What | Where | Description |
|------|-------|-------------|
| Operating principles | [`beliefs/CORE.md`](beliefs/CORE.md) | 14 principles governing swarm behavior |
| Identity claims | [`beliefs/PHILOSOPHY.md`](beliefs/PHILOSOPHY.md) | 25 claims, each with evidence labels |
| Origin story | [`docs/GENESIS.md`](docs/GENESIS.md) | How 134 lines became this |
| Full methodology | [`docs/HOW-TO-SWARM.md`](docs/HOW-TO-SWARM.md) | Apply swarm to any repo |
| Methodology paper | [`docs/PAPER.md`](docs/PAPER.md) | Formal description (v0.27.0) |
| Knowledge map | [`memory/INDEX.md`](memory/INDEX.md) | What the swarm knows |
| Open questions | [`tasks/FRONTIER.md`](tasks/FRONTIER.md) | Research driving evolution |
| Active work | [`tasks/SWARM-LANES.md`](tasks/SWARM-LANES.md) | What sessions are working on |
| FAQ | [`docs/QUESTIONS.md`](docs/QUESTIONS.md) | Honest answers with evidence links |
| Human guide | [`docs/HUMAN-GUIDE.md`](docs/HUMAN-GUIDE.md) | How to participate (~1-2 min/session) |

## Live state

Numbers in this README drift. For current state:

| Command | Shows |
|---------|-------|
| `python3 tools/orient.py` | State, priorities, maintenance, suggested action |
| `python3 tools/task_order.py` | Scored task list with priority tiers |
| `git log --oneline -10` | Recent activity |
| `bash tools/check.sh --quick` | Integrity check |

## License

[MIT](LICENSE)
