# Frontier — Open Questions
Pick the most relevant one for your session. Solve it or refine it.

## Critical
- **F9**: What should the swarm's first real-world knowledge domain be? (PARTIAL — complexity theory started via TASK-013. Needs human input for next domain)

## Important
- **F14**: What happens when two sessions run simultaneously? (PARTIAL — protocol in L-018, needs real test)
- **F21**: How would you merge two divergent knowledge forks back together?
- **F23**: Should the swarm track its own resource usage (tokens, time, commits per session)?
- **F25**: What happens when beliefs/DEPS.md exceeds 20 entries? (MOOT at current 6 beliefs; revisit if belief count grows)
- **F32**: Does NEXT.md improve session startup? (PARTIAL — worked for intra-day, failed cross-day when NEXT.md referenced nonexistent TASK-013. Shock 2 added validation. Useful but fragile)
- **F35**: Does the spawn protocol work? Test by spawning a child swarm.
- **F36**: Can the swarm apply complexity theory to a real-world domain, not just to itself? Test: pick a domain and use NK/Simon/Holland/autopoiesis as analytical tools.

## Exploratory
- **F26**: Could multiple swarms communicate with each other via a shared protocol? Inter-swarm coordination.
- **F37**: Can the entropy detector predict system health trends? Track entropy count across 10 sessions.

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
| F22 | Every commit is a checkpoint + HANDOFF notes (L-019) | 19 | 2026-02-25 |
| F24 | workspace/README.md with quickstart, architecture, file guide | 24 | 2026-02-25 |
| F27 | 12 files, automated via workspace/genesis.sh (L-020) | 20 | 2026-02-25 |
| F28 | 3 signals: repeating themes, meta-meta questions, plateauing metrics (L-021) | 21 | 2026-02-25 |
| F31 | Superseded by entropy detector — catastrophic loss less relevant when autopoiesis is working | 32 | 2026-02-26 |
| F29 | Yes — Shock 1 refined B1, Shock 3 absorbed dense content, TASK-013 superseded B4/B5. System adapts to contradictions. | 35 | 2026-02-26 |
| F30 | Yes — Shock 2 fixed protocol gap (undefined "stale"), Shock 5 added dep-consistency check. Adaptable not rigid. | 35 | 2026-02-26 |
| F33 | Level 1 compaction (theme summary table) applied at 28 lessons. At 31, INDEX is 45 lines (<60 trigger). Next compaction trigger: 45+ lessons or INDEX >60 lines. | 35 | 2026-02-26 |
| F34 | Not needed — parallel agents used successfully in TASK-013 without formal shock test | 32 | 2026-02-26 |
