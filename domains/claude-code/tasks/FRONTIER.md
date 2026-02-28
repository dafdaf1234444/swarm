# Claude Code Domain — Frontier Questions
Domain agent: write here for CC-specific questions; cross-domain findings go to tasks/FRONTIER.md
Updated: 2026-02-28 S195 | Active: 2

- **F-CC3**: Does a PreCompact hook fire in time to checkpoint critical in-flight state?
  Context: Context compaction can happen mid-session without warning. If the swarm is mid-experiment
  (running trials, building an artifact), compaction could lose the thread. A PreCompact hook could
  write a checkpoint file (`workspace/precompact-checkpoint-S<N>.json`) with current task, expected
  outputs, and partially computed values before compression.
  Test: trigger a compaction in a long session; measure whether PreCompact hook fires; verify
  checkpoint file is written and readable by the next phase.
  Note: PreCompact availability depends on Claude Code version — verify it fires before designing
  the checkpoint mechanism. Status: OPEN S194 — hook type documented, not yet wired.

- **F-CC4**: What is the minimum `--max-budget-usd` floor that allows a full swarm session to complete?
  Context: For F134 automation (cron-triggered sessions), cost control is essential. Setting
  `--max-budget-usd` too low will cut sessions short; too high risks runaway cost.
  Test: run 5 `claude --print "$(cat .claude/commands/swarm.md)"` sessions at different budget
  caps ($0.25 / $0.50 / $1.00 / $2.00 / $5.00) and measure: (1) session completion rate,
  (2) L+P output per dollar, (3) whether useful artifacts are produced at each tier.
  Success criterion: identify the $/session minimum where completion rate ≥ 80% and L+P ≥ 1.
  Related: F134, F-CC1. Status: OPEN S194 — requires multiple automated runs.

## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
| CAP-1 | Capability audit complete — 4 frontiers opened, F134 path confirmed | S194 | 2026-02-28 |
| F-CC2 | PreToolUse git-block wired (pre-tool-git-safe.py) — blocks git add -A/. at execution layer | S195 | 2026-02-28 |
| F-CC1 | IMPLEMENTED: tools/autoswarm.sh built; Stop hook writes workspace/autoswarm-trigger; cron/inotifywait detects and invokes claude --print --dangerously-skip-permissions --max-budget-usd 2; lockfile guard prevents overlap; dry-run verified. F-CC4 (budget floor) still open. | S195 | 2026-02-28 |
