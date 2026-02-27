# Human Queue — Questions for the Human
Updated: 2026-02-27 | Created: S48

Questions only a human can efficiently answer. Reviewed at session start. When answered, move to "Answered" section with date.
Every new open `HQ-N` entry must include ask-time metadata: `**Asked**: YYYY-MM-DD | **Session**: SNN`.

## Strategic Decisions

### ~~HQ-1: Which domain should be primary?~~ RESOLVED S55
**Answer**: "swarm serves the swarm" — the primary domain IS the swarm itself (meta/architecture).
NK complexity and distributed systems are test beds for validating the swarm's analytical capabilities, not ends in themselves. All domain work should compound back into swarm self-knowledge.
**Action**: F9 resolved. Meta/architecture domain elevated to primary. L-118.

### ~~HQ-2: Should the swarm output be used on YOUR codebases?~~ ANSWERED S52
See Answered section below.

## Domain Expertise Needed

### ~~HQ-3: Does etcd run errcheck?~~ ANSWERED S52
See Answered section below.

### ~~HQ-4: P-102 parallelism threshold — is the 45% source real?~~ RESOLVED S56
**Answer**: UNVERIFIED — hallucinated/misremembered. Literature search found no paper supporting a "45% accuracy threshold". Real finding: parallelize on high ambiguity, not accuracy threshold. P-102 SUPERSEDED.
**Action**: P-102 corrected in PRINCIPLES.md. L-116 written.

## Lab Work

### HQ-5: Jepsen bug reproduction (F95)
**Asked**: 2026-02-27 | **Session**: S48 (inferred from file creation)
Set up a 3-node Docker cluster. Reproduce 1-2 known bugs: Redis-Raft split-brain or TiDB auto-retry. Track determinism (% of runs that exhibit the bug). Validates B14.
**Effort**: 2-4 hours. **Stakes**: Moves B14 from theorized to observed (or kills it).

## Process Feedback

### ~~HQ-6: Is the swarm's output useful to you?~~ ANSWERED S52
See Answered section below.

## Answered

### HQ-6: Is the swarm's output useful to you?
**Date**: 2026-02-27 | **Session**: 52
**Answer**: "The swarm should check whether swarming is better than a single strong Claude. It needs to complete actual tasks to verify this. The trick is Claude is already strong enough — the swarm needs to verify whether swarming is right or not."
**Action**: F103 opened — design a comparative benchmark. Swarm vs single Claude on real task.

### HQ-2: Should the swarm output be used on YOUR codebases?
**Date**: 2026-02-27 | **Session**: 52
**Answer**: Repos available at `<your-repos>` (WSL: `<your-repos>`) and `<wsl-home>`. Avoid murex-related repos. Swarm should investigate/analyze, not modify in place. Pick tasks that evolve the swarm best or demonstrate swarm strength. Long-term vision: colonies, sub-swarms, colony tests.
**Action**: F103 incorporates real-repo analysis as benchmark vehicle.

### HQ-3: Does etcd run errcheck?
**Date**: 2026-02-27 | **Session**: 52
**Answer**: "Same" — the swarm should verify things itself, not rely on human for this.
**Action**: Self-verification principle recorded. Add to TODO for F100 Consul replication.
