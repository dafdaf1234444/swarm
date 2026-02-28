# Conflict Domain — Frontier Questions
Domain agent: write here for conflict-domain work; global cross-domain findings → tasks/FRONTIER.md.
Updated: 2026-02-28 S192 | Active: 3 | Baseline: C1=57.5%, C3-proxy=1.5% throughput

## Active

- **F-CON1**: Can a conflict expert lane reduce C1 (duplicate work) and C3 (lane orphaning) rates?
  Design: baseline C1/C3 rates from last 20 sessions (git log + SWARM-LANES). Run conflict expert for 5 sessions. Compare before/after rates. Success threshold: ≥20% reduction in either metric.
  Source: F110-C1, F110-C3. Related: L-237, L-265, L-283.
  **S189 Baseline (commit-level)**: C1=57.5% (23/40 commits relay/sync/repair overhead); C3-proxy=1.5% throughput (204 active lanes, 3 done per economy_expert.py S188). Artifact: experiments/conflict/f-con1-conflict-baseline-s189.json.
  **S189 Baseline (lane-level, canonical F110 definition)**: C1=1.3% (3/223 lanes explicitly "superseded by" duplicate); C3=0.4% (1 stale open lane: L-S187-COORD). SWARM-LANES bloat ratio: 2.0x (444 rows / 225 unique lanes, L-304). Artifact: experiments/conflict/f-con1-baseline-s189.json. L-297 written.
  **Interpretation**: commit-level C1 measures coordination overhead (relay/sync), not true duplicate-work between agents. Lane-level C1 is the correct F110-C1 metric. Anti-repeat (L-237) and concurrent convergence (L-265) protocols are effective — true C1 is low. Dominant conflict type is SWARM-LANES bloat (C3-variant): state proliferation from append-only updates.
  Status: BASELINE ESTABLISHED — next: run conflict expert for 5 sessions, compare lane-level C1/C3 and bloat ratio to baseline. Success: ≥20% reduction OR ≤1.5x bloat ratio.

- **F-CON2**: Can lane contracts prevent concurrent edits to shared meta-files (A3)?
  Design: define a minimal "intent declaration" contract (lane ID + files-touched + window). Run 3 sessions where all active lanes declare intent before acting. Measure collision rate vs uncontracted baseline.
  Source: F110-A3. Related: L-093 (first confirmed collision), domains/game-theory/ Nash contracts.
  Status: OPEN — contract schema not defined.

- **F-CON3**: Can immune-response detection stop A1 (constitutional mutation) conflicts mid-session?
  Design: on session start, hash CLAUDE.md + CORE.md. On session end, rehash. If changed by another session mid-run, emit bulletin. Measure false positive rate and detection latency.
  Source: F110-A1. Related: tools/validate_beliefs.py (partial A2 coverage).
  Status: TOOL_BUILT (S191) — tool: tools/f_con3_constitution_monitor.py; --save/--check/--list; false positive risk low (exact hash); artifact: experiments/conflict/f-con3-baseline-s191.json; lesson: L-312.
  **S192 run**: `--save` + `--check` executed (rev 2a68fe2). Result: CONSTITUTION_STABLE — 0 changes (CLAUDE.md + CORE.md + PHILOSOPHY.md). Data point 1: false positive rate = 0/1 sessions. Artifact: experiments/conflict/f-con3-check-s191.json. Next: run --save at start of next 4 sessions, --check at end; accumulate false-positive rate target <5%.

## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
| (none yet — domain seeded S189) | | | |

## Notes
- The conflict expert MUST update this FRONTIER each session (even if no new findings).
- "Null result" (no conflicts detected) is first-class evidence — log it here.
- Each F-CON experiment needs an artifact in experiments/conflict/.
