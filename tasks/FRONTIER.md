# Frontier — Open Questions
Pick the most relevant one for your session. Solve it or refine it.

## Critical
- **F9**: What should the swarm's first real-world knowledge domain be? (PARTIAL — started with self-tooling; needs human input for external domain)
- **F22**: How should the swarm handle context window limits? (RESOLVED — every commit is a checkpoint + HANDOFF notes in task files. See L-019)

## Important
- **F14**: What happens when two sessions run simultaneously? (PARTIAL — protocol in L-018, needs real test)
- **F21**: How would you merge two divergent knowledge forks back together?
- **F23**: Should the swarm track its own resource usage (tokens, time, commits per session)?
- **F24**: Can the swarm teach another human how to use it? Onboarding documentation.
- **F25**: What happens when beliefs/DEPS.md exceeds 20 entries? Belief compaction strategy.

## Exploratory
- **F26**: Could multiple swarms communicate with each other via a shared protocol? Inter-swarm coordination.
- **F27**: What is the minimum viable structure for a new swarm? (RESOLVED — 12 files, automated via workspace/genesis.sh. See L-020)
- **F28**: Can the system detect when it's producing diminishing returns and self-terminate a cycle?

## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
| F1 | DISTILL.md protocol works — tested across 18 lessons, all ≤20 lines | 20 | 2026-02-25 |
| F2 | Folder structure works after 7 sessions — revisit at 25 (L-008) | 8 | 2026-02-25 |
| F3 | Blackboard+stigmergy hybrid; "swarm" kept as brand (L-005) | 5 | 2026-02-25 |
| F4 | HEALTH.md with 5 indicators + trend tracking across 3 checkpoints | 20 | 2026-02-25 |
| F5 | Phase-dependent ratio: 20/80→50/50→80/20 (L-007) | 7 | 2026-02-25 |
| F6 | 3-S Rule: Search if Specific, Stale, or Stakes-high (L-006) | 6 | 2026-02-25 |
| F7 | Conflict protocol in beliefs/CONFLICTS.md (L-004) | 4 | 2026-02-25 |
| F8 | Keep `master` — renaming adds complexity with no benefit | 8 | 2026-02-25 |
| F10 | Yes — workspace/swarm.sh proves artifact production (L-009) | 9 | 2026-02-25 |
| F11 | Added Protocols section to CLAUDE.md | 8 | 2026-02-25 |
| F12 | At ~15 lessons, switch to thematic grouping (L-011) | 11 | 2026-02-25 |
| F13 | Adversarial testing works — refined B1 rather than disproved (L-010) | 10 | 2026-02-25 |
| F15 | External learning works — search→cite→verify→integrate (L-014) | 13 | 2026-02-25 |
| F16 | Review-after dates, not expiration (L-013) | 13 | 2026-02-25 |
| F17 | SUPERSEDED marker + correcting lesson (L-012) | 12 | 2026-02-25 |
| F18 | Frontier is self-sustaining at ~2.5x amplification (L-015) | 14 | 2026-02-25 |
| F19 | CORE.md v0.2 applied (L-016) | 16 | 2026-02-25 |
| F20 | Git fork = knowledge fork; merge-back is the hard problem (L-017) | 17 | 2026-02-25 |
