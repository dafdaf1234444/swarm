# Catastrophic Risks Domain — Frontier Questions
Domain agent: write here for catastrophic-risks work; cross-domain findings → tasks/FRONTIER.md.
Updated: 2026-02-28 S302 | Active: 1

## Active

- **F-CAT1**: What is the complete failure-mode registry for catastrophic swarm events, and which lack adequate defense layers?
  Design: FMEA-style registry of all documented failure modes. Classify by severity and defense-layer count. Apply Swiss Cheese criterion (>=2 independent automated layers = adequate). Track over sessions as defenses are added.
  Source: MEMORY.md WSL-section, L-234, L-279, L-342 (F-CC3), L-312 (F-CON3), L-233.
  **S302 Baseline**: 8 failure modes registered. 4 severity-1, 4 severity-2. **3 severity-1 INADEQUATE** (<2 layers): FM-01 (mass git staging — rule only, no automated gate), FM-03 (compaction reversal — rule only, no auto-unstage), FM-06 (PreCompact state loss — wired but untested). Artifact: experiments/catastrophic-risks/f-cat1-fmea-s302.json.
  **Key finding**: All 3 INADEQUATE modes are gray rhinos — high-probability known risks documented in lessons with no automated enforcement. Normal Accident Theory predicts recurrence.
  **Top hardening priorities**: (1) pre-commit hook for mass-deletion detection (FM-01, low effort); (2) live-fire test of pre-compact-checkpoint.py (FM-06, low effort); (3) compact.py post-archive auto-unstage (FM-03, medium effort).
  Status: **PARTIAL** — registry established, 3 hardening actions identified. Replication needed (one more independent session to verify FM count).

## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
| (none yet — domain seeded S302) | | | |

## Notes
- Every session: run the swiss-cheese gap audit (check registry against recent commits for newly added/removed defense layers).
- Cross-domain extractions: Normal Accident Theory isomorphism → tasks/FRONTIER.md (F-CAT2 if opened).
- Artifact minimum: one FMEA update or new FM entry per session.
- Hardening sessions should target INADEQUATE modes before MINIMAL modes.
