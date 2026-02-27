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

### ~~HQ-5: Jepsen bug reproduction (F95)~~ RESCOPED S132
See Answered section below.

## Process Feedback

### ~~HQ-6: Is the swarm's output useful to you?~~ ANSWERED S52
See Answered section below.

### ~~HQ-7: Concurrent local edits appeared during this swarm run — proceed or pause?~~ ANSWERED S128
See Answered section below.

### ~~HQ-8: Concurrent edits detected again during swarm run — continue integrating or wait?~~ ANSWERED S132
See Answered section below.

### ~~HQ-9: Concurrent edits keep landing mid-run — continue with live integration by default?~~ ANSWERED S144
See Answered section below.

## Answered

### HQ-9: Concurrent edits keep landing mid-run — continue with live integration by default?
**Date**: 2026-02-27 | **Session**: S144
**Answer**: Repeated `swarm` continuation signal after pause prompts indicates continue integrating by default.
**Action**: Treat concurrent edits as live-state integration by default unless explicitly told to pause/freeze.

### HQ-8: Concurrent edits detected again during swarm run — continue integrating or wait?
**Date**: 2026-02-27 | **Session**: S132
**Answer**: `swarm` re-issued after pause prompt (continue integrating).
**Action**: Continued autonomous execution on top of live concurrent changes; state reconciliation remains part of each run.

### HQ-5: Jepsen bug reproduction (F95)
**Date**: 2026-02-27 | **Session**: S132
**Answer**: Re-scoped: this is a swarm execution experiment, not a human-only question.
**Action**: Removed from HUMAN-QUEUE open set; execution deferred to swarm backlog when time/runtime budget is allocated.

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

### HQ-7: Concurrent local edits appeared during this swarm run — proceed or pause?
**Date**: 2026-02-27 | **Session**: S128
**Answer**: `swarm` re-issued after pause prompt (continue).
**Action**: Continued execution on current dirty tree; logged state and resumed autonomous maintenance flow.
