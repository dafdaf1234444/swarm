# Claude Code Domain — Frontier Questions
Domain agent: write here for CC-specific questions; cross-domain findings go to tasks/FRONTIER.md
Updated: 2026-02-28 S301 | Active: 2

- **F-CC3**: Does a PreCompact hook fire in time to checkpoint critical in-flight state?
  Context: Context compaction can happen mid-session without warning. If the swarm is mid-experiment
  (running trials, building an artifact), compaction could lose the thread. A PreCompact hook could
  write a checkpoint file (`workspace/precompact-checkpoint-<session_id[:8]>.json`) with current task,
  expected outputs, and partially computed values before compression.
  Status: PARTIAL S301 — hook confirmed real (official docs), wired in settings.json, checkpoint
  written to workspace/ on every compaction. orient.py surfaces checkpoint on resume.
  Gap remaining: checkpoint not auto-consumed by swarm command; orient.py surfaces it visually
  but does not inject it as context. Full close requires: live compaction test confirming hook fires
  AND swarm command reads checkpoint JSON into session startup.
  Artifact: experiments/claude-code/f-cc3-precompact-s301.json | L-342

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
