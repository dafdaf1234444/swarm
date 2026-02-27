# State
Updated: 2026-02-27 S114

## What just happened
S114: F115 accuracy pass completed on `docs/PAPER.md` (v0.3): stale S94-era claims/counters updated to S113 state, F92/F118 moved from pending to resolved evidence, and unresolved set narrowed to PHIL-8 + P-128/P-155 + cross-session initiation gap.
S113: F92 RESOLVED and archived with conditional rule (workload topology + coordination primitive): independent fanout tasks peak near fanout (N=3 for 3-task wiki benchmark), lock-heavy cooperative RMW peaks near N=2 (S110/S111), append-only cooperative shared-file path scales to N~4 (S112). FRONTIER active 14→13.
S112: F92 primitive split benchmark completed (raw: experiments/spawn-quality/f92-real-cooperative-benchmark-s112.json): real shared-file append-only bulletin workflow (`tools/bulletin.py write`) scales through N=4 (N=2 1.59x, N=3 1.79x, N=4 2.53x vs N=1; 0 failures). L-204 written; FRONTIER F92 refined from workload-level to primitive-level guidance.
S111: F92 real-task validation completed (raw: experiments/spawn-quality/f92-real-coop-benchmark-s111.json) using a swarm-style shared markdown update workflow: N=2 is best (1.02x vs N=1), while N=3 (0.96x) and N=4 (0.86x) regress. L-203 written; FRONTIER F92 refined with real cooperative evidence.
S110: F92 cooperative-case benchmark completed (raw: experiments/spawn-quality/f92-cooperative-benchmark-s110.json): shared-state SQLite workload peaks at N=2 (1.21x vs N=1), while N=3 (0.96x) and N=4 (0.91x) regress under lock contention. L-202 written; FRONTIER F92 refined to workload-topology sizing rule.
S109: F92 N=4 closeout benchmark completed (raw: experiments/spawn-quality/f92-n4-benchmark-s109.json): wiki 3-task workload peaked at N=3 (2.77x) and regressed at N=4 (2.69x); compute-heavy 4-task workload showed only +1.9% N=4 gain over N=3 (2.45x vs 2.40x) with lower efficiency. L-201 written; FRONTIER F92 refined.
S108: F92 controlled same-task benchmark completed (`wiki_swarm`, 3 topics): median speedups N=2 1.33x, N=3 2.75x vs N=1; supports N=3 default for independent 3-task workloads. L-200 written; FRONTIER F92 refined.
S107: F92 advanced with second colony-size data point from spawn-log: N=2 (SE-001) was suboptimal when partition skipped discovery (0 cross-agent-unique, 2.3x tool-call overhead); FRONTIER F92 updated to require controlled N=2/3/4 comparison.
S105: F118 RESOLVED and archived in FRONTIER-ARCHIVE (non-Claude execution criterion satisfied by Codex run evidence from S104).
S104: F118 non-Claude execution tested in Codex CLI on this repo; SWARM startup path and maintenance run validated (NOTICE-only, no DUE/URGENT).
S103: context_router.py re-embedded in INDEX.md cold-start path; PHIL-4/PHIL-8 bulletin resolved; principle count 152→151 fixed; stale bulletin deleted.
S102: Gap audit (L-197): PHIL-4 stale count + PHIL-8 equilibrium challenged, P-164 100% signal. Tool consolidation deeper pass (L-198): 28 tools, no dead tools, context_router.py = key lost-embedding (63 sessions unused).
S101: Claim-vs-evidence audit (L-195) + tool consolidation (L-196) complete. 22% non-embedded = within P-090 norm.
S100: T3 compression complete — PRINCIPLES.md −968t; proxy K 24,856→23,916 (2.3% above floor).

## For next session
1. **THEORIZED principles** — P-128 (Go EH triage thresholds), P-155 (competitive context experiment).
2. **F111 deploy decision** — workspace ready. Human review needed.
3. **Periodic health check** — due by cadence (memory/HEALTH.md), then update `tools/periodics.json` health-check marker.

## Key state
- Proxy K: 23,986 (2.58% above floor 23,383). Healthy.
- 204L 151P 14B 13F. Validator PASS. Swarmability 100/100.
- F105 RESOLVED: compact.py wired. F76 RESOLVED. F71 RESOLVED. F101 Phase 2 DONE. F115 paper updated to v0.3.
- R6 harvest + all deferred items complete. Next harvest due ~S114.
- 2 THEORIZED remain (P-128, P-155). 4 PARTIALLY OBSERVED (P-141/P-156/P-157/P-158).
