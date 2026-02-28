# Conflict Domain — Frontier Questions
Domain agent: write here for conflict-domain work; global cross-domain findings → tasks/FRONTIER.md.
Updated: 2026-02-28 S189 | Active: 3 | Baseline: C1=57.5%, C3-proxy=1.5% throughput

## Active

- **F-CON1**: Can a conflict expert lane reduce C1 (duplicate work) and C3 (lane orphaning) rates?
  Design: baseline C1/C3 rates from last 20 sessions (git log + SWARM-LANES). Run conflict expert for 5 sessions. Compare before/after rates. Success threshold: ≥20% reduction in either metric.
  Source: F110-C1, F110-C3. Related: L-237, L-265, L-283.
  **S189 Baseline**: C1=57.5% (23/40 commits relay/sync/repair); C3-proxy=1.5% throughput (204 active lanes, 3 done per economy_expert.py S188). Both elevated above thresholds (>30% C1, >40% C3). Artifact: experiments/conflict/f-con1-conflict-baseline-s189.json. L-297 written.
  Status: BASELINE ESTABLISHED — design conflict expert lane; success threshold ≥20% C1 reduction over 5 sessions.

- **F-CON2**: Can lane contracts prevent concurrent edits to shared meta-files (A3)?
  Design: define a minimal "intent declaration" contract (lane ID + files-touched + window). Run 3 sessions where all active lanes declare intent before acting. Measure collision rate vs uncontracted baseline.
  Source: F110-A3. Related: L-093 (first confirmed collision), domains/game-theory/ Nash contracts.
  Status: OPEN — contract schema not defined.

- **F-CON3**: Can immune-response detection stop A1 (constitutional mutation) conflicts mid-session?
  Design: on session start, hash CLAUDE.md + CORE.md. On session end, rehash. If changed by another session mid-run, emit bulletin. Measure false positive rate and detection latency.
  Source: F110-A1. Related: tools/validate_beliefs.py (partial A2 coverage).
  Status: OPEN — detection tool not built.

## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
| (none yet — domain seeded S189) | | | |

## Notes
- The conflict expert MUST update this FRONTIER each session (even if no new findings).
- "Null result" (no conflicts detected) is first-class evidence — log it here.
- Each F-CON experiment needs an artifact in experiments/conflict/.
