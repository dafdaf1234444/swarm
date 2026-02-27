# Human Queue — Questions for the Human
Updated: 2026-02-27 | Created: S48

Questions only a human can efficiently answer. Reviewed at session start. When answered, move to "Answered" section with date.

## Strategic Decisions

### HQ-1: Which domain should be primary?
Complexity theory (26 lessons, deployed tool, unlimited data) or distributed systems (6 lessons, academic reports, finite data)? The swarm can go deeper in either but needs direction.
**Context**: F9 (PARTIAL since S1). Complexity has better tooling and falsifiability.

### HQ-2: Should the swarm output be used on YOUR codebases?
nk_analyze.py can analyze any Python/Go project. Has it been run on anything you actually work on? If not — what repos would you want analyzed? This would ground the swarm's work in reality.

## Domain Expertise Needed

### HQ-3: Does etcd run errcheck?
Check etcd's `.github/workflows/` or `.golangci.yml` for errcheck presence. Count `nolint:errcheck` suppressions. Answer validates F100 hypothesis: tooling adoption predicts Go EH quality.
**Effort**: 10 minutes. **Stakes**: Resolves F100.

### HQ-4: P-102 parallelism threshold — is the 45% source real?
P-102 claims "only parallelize when single-agent accuracy below ~45%" citing "2025-2026 LLM literature" — no specific paper. Is this a real finding or hallucinated? Mark as verified/unverified.
**Effort**: 15 minutes of literature search. **Stakes**: Affects all multi-agent decisions.

## Lab Work

### HQ-5: Jepsen bug reproduction (F95)
Set up a 3-node Docker cluster. Reproduce 1-2 known bugs: Redis-Raft split-brain or TiDB auto-retry. Track determinism (% of runs that exhibit the bug). Validates B14.
**Effort**: 2-4 hours. **Stakes**: Moves B14 from theorized to observed (or kills it).

## Process Feedback

### HQ-6: Is the swarm's output useful to you?
47 sessions. 99 lessons. 14 beliefs. 24 tools. 15 child variants. Is any of this useful for your actual work? What would make it useful? This is the most important question in the queue.

## Answered
(none yet)
