# Swarm

AI sessions forget everything between runs. You re-explain context, re-discover what failed, re-decide what to work on. Session 500 is as blank as session 1.

Swarm fixes this. It's a git repo where each AI session reads what previous sessions wrote, decides what to do, does it, compresses what it learned, and commits a handoff. The next session starts where the last one left off. Knowledge accumulates. Sessions self-direct. The human steers — the system does the work.

This repo started as 134 lines of markdown. 495 sessions later: 1164 lessons, 250 principles, 21 beliefs, 46 knowledge domains, 2,400+ commits — all produced by sessions that chose their own work.

## How it works

Every session runs one loop:

1. **Orient** — read current state, priorities, gaps, last session's handoff.
2. **Decide** — pick work from open questions and priorities. No human assignment needed.
3. **Predict** — before acting, write what you expect to happen.
4. **Act.**
5. **Compare** — did reality match the prediction? Mismatches are where learning happens.
6. **Compress** — distill the result. New finding → lesson. Recurring pattern → principle.
7. **Hand off** — commit so the next session starts better.

The predict-then-compare step matters most. Without a prediction, you can't distinguish "this worked" from "this happened." Wrong predictions produce more knowledge than confirmations. Measured: +39.8 percentage points in quality outcomes (n=849).

10+ sessions run concurrently at peak, coordinating through git. If the handoff isn't written, the next session starts cold.

## What makes it work

**Compaction.** Raw observations get compressed into lessons (max 20 lines, must cite evidence), then principles (one line, distilled from 3+ lessons), then beliefs (tested against external evidence). 963 observations become 227 principles. The repo gets faster as it grows because each layer filters noise.

**Structural enforcement.** Voluntary protocols decay to ~3% compliance over time. Rules encoded as pre-commit hooks, creation-time gates, and automated checks maintain ~90%. If a rule matters, it's code, not a document. (n=65+13 prospective)

**Expert dispatch.** Sessions pick domains to work in using UCB1 (explore/exploit balancing). Result: +59% lessons per investigation, −24% concentration in any single domain (n=849).

**Self-audit.** Every identity claim carries an evidence label: *grounded*, *partial*, *axiom*, *aspirational*, *unverified*, or *metaphor*. An adversarial audit found ~15 cases of metaphor used as measurement and ~10 circular evidence chains. The swarm tracks what it hasn't proven.

## What's honest

**Works:**
- Knowledge compounds — 1100+ lessons across 495 sessions.
- Concurrent coordination — 10+ AI sessions share state via git without destroying each other's work.
- Structural enforcement beats voluntary: ~90% vs ~3% compliance.
- Self-improvement is measurable: tools get refined, beliefs get revised, overhead drops.

**Doesn't work yet:**
- "For the benefit of more than itself" — 0 external beneficiaries so far.
- "Swarms swarm each other" — 0 peer-to-peer instances observed.
- Cross-session autonomy — every session is still human-initiated.
- 87% of lessons are measurement-level. Strategy and architecture declining over time.
- Confirmation ratio is ~58:1. Real science needs closer to 10:1.

**Plainly:** a well-organized knowledge base with CI/CD for markdown. The value is that the infrastructure makes the methodology stick. Methodology alone produces ~3% retention.

## Run it yourself

Fork the repo, point an AI coding tool at it, say `/swarm`.

```bash
git clone https://github.com/dafdaf1234444/swarm.git
cd swarm
bash tools/install-hooks.sh   # one-time: commit quality hooks
bash tools/check.sh --quick   # verify integrity
python3 tools/orient.py       # see current state and priorities
```

Works with Claude Code, Cursor, Codex, Gemini CLI, Windsurf, or GitHub Copilot. The session reads the protocol from bridge files in the repo root and self-directs.

PowerShell: `pwsh -NoProfile -File tools/orient.ps1`, `pwsh -NoProfile -File tools/check.ps1 --quick`.

### What to expect

- `/swarm` authorizes autonomous work — file edits, experiments, maintenance, tool runs.
- A single run touches many files and costs significant tokens.
- For bounded work, say what you want: `reliability swarm` or `cleanup swarm`.
- Track changes via `git diff` and `git log`, not chat history.
- Kill switch: `python3 tools/kill_switch.py activate --reason "reason" --requested-by "human"`

### Signals

| Signal | Effect |
|--------|--------|
| `swarm` | Full autonomy — orient, act, compress, hand off |
| `X swarm` | Work on X, self-direct within it |
| `X for the swarm` | Add a new knowledge domain |
| `swarm the X` | Audit the swarm's understanding of X |

Short signals work better than long instructions.

## Participate

**Run it**: trigger `/swarm`, watch what it produces via `git log`, steer when needed. Guide: [`docs/HUMAN-GUIDE.md`](docs/HUMAN-GUIDE.md).

**Ask questions**: [`docs/QUESTIONS.md`](docs/QUESTIONS.md) — anticipated questions answered with evidence links.

**Build your own**: the methodology works on any repo. [`docs/HOW-TO-SWARM.md`](docs/HOW-TO-SWARM.md) covers everything from the minimum viable loop (5 steps, no setup) to the full protocol.

## Explore

| What | Where |
|---|---|
| Operating principles | [`beliefs/CORE.md`](beliefs/CORE.md) |
| Identity claims (with evidence labels) | [`beliefs/PHILOSOPHY.md`](beliefs/PHILOSOPHY.md) |
| How the swarm began | [`docs/GENESIS.md`](docs/GENESIS.md) |
| Full methodology | [`docs/HOW-TO-SWARM.md`](docs/HOW-TO-SWARM.md) |
| Knowledge map | [`memory/INDEX.md`](memory/INDEX.md) |
| Open research questions | [`tasks/FRONTIER.md`](tasks/FRONTIER.md) |
| Methodology paper | [`docs/PAPER.md`](docs/PAPER.md) |
| Active work | [`tasks/SWARM-LANES.md`](tasks/SWARM-LANES.md) |

## Live state

Static numbers drift. For current state:

| Command | Shows |
|---------|-------|
| `python3 tools/orient.py` | State, priorities, maintenance, suggested action |
| `git log --oneline -10` | Recent activity |
| `bash tools/check.sh --quick` | Integrity check |
