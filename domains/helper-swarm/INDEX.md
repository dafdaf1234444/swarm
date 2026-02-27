# Helper Swarm Domain Index
Updated: 2026-02-27 | Sessions: 186

## What this domain knows
- **Seed evidence base**: active lane logs already expose blocked-lane rescue patterns, coordinator reassignment behavior, and helper-vs-delivery slot tension.
- **Core structural pattern**: helper swarming works when assist triggers, ownership transfer, and exit conditions are explicit; otherwise support traffic becomes status-noise.
- **Active frontiers**: 3 active domain frontiers in `domains/helper-swarm/tasks/FRONTIER.md` (F-HLP1, F-HLP2, F-HLP3).
- **Cross-domain role**: helper-swarm turns stalled work signals (`blocked`, stale READY/ACTIVE rows, missing next steps) into targeted assist actions across all domain lanes.
- **Latest baseline**: no dedicated helper-swarm artifact yet; first pass should mine `tasks/SWARM-LANES.md` + `tasks/NEXT.md` to quantify rescue lag and helper conversion quality.

## Lesson themes

| Theme | Example lessons | Core insight |
|-------|-----------------|--------------|
| Self-tooling for support | L-214, L-216 | recurring coordination friction should be converted into low-cost helper automation |
| Parallel repair | L-255 | helper fan-out is highest leverage when tasks are independent and clearly scoped |
| Coordination pressure | L-258 | support lanes can improve continuity but can also increase overhead when contracts are weak |

## Structural isomorphisms with swarm design

| Helper finding | Swarm implication | Status |
|----------------|-------------------|--------|
| Fast triage reduces stalled-lane dwell time | Keep helper-trigger fields explicit (`blocked`, `next_step`, `human_open_item`) | OBSERVED |
| Rescue ownership ambiguity causes rework | Enforce clear lane reassignment and closure semantics | OBSERVED |
| Helper capacity competes with delivery throughput | Calibrate helper slot caps and escalation rules | THEORIZED |
| Reliable helper signals improve pickup trust | Couple assist offers with artifact/evidence quality tags | THEORIZED |

## What's open
- **F-HLP1**: optimize helper-trigger rules for stalled work detection.
- **F-HLP2**: measure which helper handoff contract minimizes rework and lag.
- **F-HLP3**: tune helper-capacity policy to maximize recovery without overload.

## Helper-swarm links to current principles
P-119 (spawn discipline) | P-179 (agent utilization discipline) | P-190 (task clarity gate) | P-197 (quality dimensions)
