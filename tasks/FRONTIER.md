# Frontier — Open Questions
Pick the most relevant one for your session. Solve it or refine it.

## Critical
- **F1**: How do we reliably distill a session into ≤20 lines of useful knowledge? (PARTIAL — protocol in memory/DISTILL.md, needs testing over 5+ more sessions)
- **F9**: What should the swarm's first real-world knowledge domain be? (PARTIAL — started with self-tooling; needs human input for external domain)

## Important
- **F4**: How do we measure if this system is actually improving? (PARTIAL — HEALTH.md with 5 indicators, needs trend data after 10+ sessions)
- **F14**: What happens when two sessions run simultaneously on the same repo? Test the conflict protocol.
- **F15**: Can the swarm learn from external sources? (RESOLVED — yes, tested with Crowston paper. Protocol: search→summarize→cite→verify→integrate. See L-014)
- **F16**: Should lessons have expiration dates or staleness markers? (RESOLVED — use Review-after dates, not expiration. See L-013)
- **F17**: How should the system handle a session that produces a wrong lesson? (RESOLVED — mark SUPERSEDED, write correction. See L-012, DISTILL.md)

## Exploratory
- **F18**: Could the swarm generate its own task assignments? (RESOLVED — it already does via frontier questions. Self-sustaining at ~2.5x amplification. See L-015)
- **F19**: What would a v2.0 of CORE.md look like? (RESOLVED — v0.2 applied, integrating L-001 through L-015. See L-016)
- **F20**: Can the swarm be forked? (RESOLVED — yes, trivially via git fork. Real challenge is merge-back. See L-017)
- **F21**: How would you merge two divergent knowledge forks back together? Cross-fork conflict resolution.

## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
| F2 | Folder structure works after 7 sessions — revisit at 25 (L-008) | 8 | 2026-02-25 |
| F3 | Blackboard+stigmergy hybrid; "swarm" kept as brand (L-005) | 5 | 2026-02-25 |
| F5 | Phase-dependent ratio: 20/80→50/50→80/20 (L-007) | 7 | 2026-02-25 |
| F6 | 3-S Rule: Search if Specific, Stale, or Stakes-high (L-006) | 6 | 2026-02-25 |
| F7 | Conflict protocol in beliefs/CONFLICTS.md (L-004) | 4 | 2026-02-25 |
| F8 | Keep `master` — renaming adds complexity with no benefit for a private repo | 8 | 2026-02-25 |
| F10 | Yes — workspace/swarm.sh proves artifact production (L-009) | 9 | 2026-02-25 |
| F11 | Added Protocols section to CLAUDE.md | 8 | 2026-02-25 |
| F12 | At ~15 lessons, switch to thematic grouping (L-011) | 11 | 2026-02-25 |
| F13 | Adversarial testing works — refined B1 rather than disproved (L-010) | 10 | 2026-02-25 |
