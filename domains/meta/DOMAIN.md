# Domain: Meta / Swarm Self-Knowledge
Topic: The swarm as its own domain. Focus on self-model quality, coordination fidelity, and improvement loops that raise future swarm performance.
Beliefs: B1-B8, B11, B12, B16 (architecture, coordination, governance)
Lessons: L-214, L-215, L-216, L-222, L-223, L-224, L-237, L-246, L-250, L-257
Frontiers: F-META1, F-META2, F-META3
Experiments: experiments/self-analysis/, experiments/operations-research/, experiments/game-theory/, experiments/history/
Load order: AGENTS.md or CLAUDE.md -> SWARM.md -> beliefs/CORE.md -> this file -> INDEX.md -> memory/INDEX.md -> tasks/NEXT.md

## Domain filter
Only self-referential findings that directly change swarm execution quality qualify.
Each candidate must satisfy all three:
1. Same coordination mechanism exists in swarm operation.
2. Same failure mode is visible in current swarm artifacts.
3. The finding implies a concrete lane/tool/protocol change.

## Core isomorphisms

| Meta concept | Swarm parallel | Isomorphism type | Status |
|--------------|----------------|------------------|--------|
| Self-model drift | FRONTIER/NEXT/INDEX inconsistency | State estimation | OBSERVED |
| Check-quality variation | explicit check mode tags in lanes | Measurement discipline | OBSERVED |
| Expect-act-diff closure lag | correction latency in active work | Feedback control | OBSERVED |
| Human signal loss | ephemeral chat inputs vs persisted signals | Input observability | OBSERVED |
| Improvement ROI uncertainty | change volume vs outcome quality | Optimization | THEORIZED |
