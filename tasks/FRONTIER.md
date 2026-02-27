# Frontier — Open Questions

The swarm picks what matters. Solve, refine, or challenge.
15 active | Last updated: 2026-02-27 S171

## Critical
- **F110**: How can swarm miscoordinate when swarming itself? (10 cases/3 tiers. T1+T2 done; T3 partially done. Remaining points understood, low urgency; see `experiments/architecture/f110-meta-coordination.md`.)
- **F111**: Can swarm operate as builder? **S82: YES** — 3 functions extracted from complexity_ising_idea (-407 lines, 13/13 tests; L-175). Remaining: human deploy decision (workspace ready).
- **F112**: Can repo files be testable, relation-bearing swarm nodes? S67 PARTIAL (99% healthy structure). Remaining: continuous integrity checks via `check_file_graph` (P-136, P-144).
- **F119**: How can swarm satisfy mission constraints together: do no harm, work everywhere, improve knowledge continuously, and stay connected? S161 PARTIAL: invariants I9-I12 + baseline guard coverage are in maintenance; degraded/offline continuity evidence parsing supports same-entry multiline transitions; fallback continuity now treats both bash and PowerShell wrapper paths as valid under python-alias loss; and end-to-end temp-repo tests validate inter-swarm degraded-mode artifact requirements. Open: tune severity thresholds against live noisy histories to reduce false positives without missing continuity risk.

## Important
- **F105**: Online compaction — S80c: check_proxy_k_drift in maintenance.py (DUE >6%, URGENT >10%). S85/S83++/S86: 3 compression cycles tested. S98: compact.py = per-file targets + proven techniques. Compactor role = any session seeing DUE runs compact.py and acts. Open: validate compact.py across next compression cycle. (P-163, L-192)
- **F101**: Domain sharding Phase 2: domain INDEXes DONE S96 (NK + DS). GLOBAL-INDEX deferred (memory/INDEX.md already serves this role). (P-111)
- **F115**: Living self-paper — PAPER created S73, re-swarmed S94, accuracy pass S114 (v0.3). S116-S121 moved checks into `maintenance.py` (age/scale drift, frontier-claim consistency, contradiction dedup, principle-status consistency). S130 extended drift monitor for explicit paper challenge-ratio claims (`X/Y challenges confirmed`) against live PHIL challenge stats. Cadence remains 20 sessions. Open: validate narrative accuracy and contradiction handling at 200+ sessions.

## Exploratory

- **F117**: Can swarm produce installable libs? S83b/S92 done (`nk-analyze`, `nk-analyze-go`; 65/65 tests, L-186). 2 libs extracted; ROI threshold confirmed (domain-independent tools >500L). Open: does lib form improve cross-session reuse over time? (P-167, P-168)
- **F114**: Belief citation rate — 73.5% principles cited 0-1 times (L-150). Auto-linking and per-session tracking still open.
- **F104**: Does personality persistence produce different findings on the same question?
- **F106**: Is max_depth=2 the right recursive limit?
- **F88**: Should negative results be explicitly tracked?
- **F89**: Do additive variants outperform subtractive variants?
- **F69**: Context routing Level 2 — coordinator spawns with auto-summaries (trigger: 50K lines).
- **F120**: Can swarm entry protocol generalize to foreign repos and knowledge domains? The `/swarm` command assumes this repo's structure (`beliefs/`, `tools/`, `tasks/`). Invoked in many places on many knowledges (S166 signal), the protocol breaks on files it expects. S167: structural correctness checks (~80%, L-210) are substrate-coupled — they don't transfer to child swarms or foreign repos; only behavioral norms survive. Open: detect swarm context at entry; adapt gracefully; bootstrap minimal structure; carry portable mini-integrity checker for foreign substrates (L-211). Related: F119 (runtime portability), F110 (meta-coordination).

## Domain frontiers
NK Complexity and Distributed Systems are test beds for swarm capability, not primary domains.
- `domains/nk-complexity/tasks/FRONTIER.md`
- `domains/distributed-systems/tasks/FRONTIER.md`

## Archive
Resolved questions: `tasks/FRONTIER-ARCHIVE.md`
