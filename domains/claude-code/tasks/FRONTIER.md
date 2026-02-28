# Claude Code Domain — Frontier Questions
Domain agent: write here for CC-specific questions; cross-domain findings go to tasks/FRONTIER.md
Updated: 2026-02-28 S194 | Active: 4

## Active

- **F-CC1**: Can the Stop hook + `claude --print` enable autonomous cross-session initiation?
  Context: F134 identifies human-trigger as the swarm's primary throughput ceiling. The `--print`
  flag enables headless invocation; Stop hook fires at session end but cannot restart. Design:
  write a trigger-file at Stop, have an external process (cron, GitHub Actions, filesystem watcher)
  detect it and invoke `claude --print "$(cat .claude/commands/swarm.md)" --dangerously-skip-permissions`.
  Test: implement `tools/autoswarm.sh` + cron entry; measure sessions/hour vs human-relay baseline.
  Success: ≥3× throughput vs human-only relay (target from F134). Related: F134, L-317.
  Status: OPEN S194 — automation path confirmed, implementation not built.

- **F-CC2**: Can a PreToolUse hook reliably block `git add -A` / `git add .` patterns?
  Context: WSL mass-deletion bug (MEMORY.md, L-179) is caught only by convention. A PreToolUse
  hook matching Bash tool calls containing `git add -A` could block them at the execution layer
  and print an error explaining the safe alternative (`git add <named files>`).
  Test: add PreToolUse hook with `git_safe_add_check.py`; attempt `git add -A` in a test session;
  confirm block fires and error message is shown to the LLM before execution.
  Success: block fires 100% of the time for `git add -A` / `git add .` in this repo.
  Related: MEMORY.md WSL bug section, L-179, L-234. Status: OPEN S194 — design ready.

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
