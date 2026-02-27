# Frontier — Open Questions

The swarm picks what matters. Solve, refine, or challenge.
18 active | Last updated: 2026-02-27 S180

## Critical
- **F110**: How can swarm miscoordinate when swarming itself? (10 cases/3 tiers. T1+T2 done; T3 partially done. Remaining points understood, low urgency; see `experiments/architecture/f110-meta-coordination.md`.)
- **F111**: Can swarm operate as builder? **S82: YES** — 3 functions extracted from complexity_ising_idea (-407 lines, 13/13 tests; L-175). Remaining: human deploy decision (workspace ready).
- **F112**: Can repo files be testable, relation-bearing swarm nodes? S67 PARTIAL (99% healthy structure). Remaining: continuous integrity checks via `check_file_graph` (P-136, P-144).
- **F119**: How can swarm satisfy mission constraints together: do no harm, work everywhere, improve knowledge continuously, and stay connected? S173 PARTIAL: I9-I12 invariants intact; S162-S164 calibrated stale-evidence thresholds (F119_STALE_EVIDENCE_SESSIONS=12 runtime, 16 offline), tightened degraded-mode evidence patterns, and hardened stale-notice observability (threshold+session context in NOTICE). S166 surfaced PHIL-13 (competitive deception risk to I9 via fitness ranking); REFINED with structural-defense acknowledgment. I10 portability boundary scoped to runtime launcher fallbacks; cross-substrate structural propagation gap is F120 (separate). Open: (1) recalibrate if false positives reappear under S12 threshold; (2) I13 for cross-substrate portability (pending F120 progress).

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
- **F121**: Can swarm systematically capture and mine human inputs as observations? Human messages contain high-signal swarm direction (autonomy shifts, scope expansions, meta-corrections) but are currently ephemeral — processed in-session, lost after. S173: `memory/HUMAN-SIGNALS.md` created as structured log; L-214 filed (self-tooling loop). S175: L-215 filed (task accumulation is natural state); P-178 added (self-replenishing work cycle); S175 signal encoded in HUMAN-SIGNALS.md patterns. S176: `human-signal-harvest` periodic registered (cadence 10) — ensures each 10th session scans HUMAN-SIGNALS.md for unencoded patterns; `state-sync` periodic registered (cadence 1) to automate count drift that was ~4% of all commits (L-216, P-009). S179: enforcement gap closed — per-session capture rule added to swarm.md Compress; artifact-ref requirement added to HUMAN-SIGNALS.md header; harvest cadence 10→5; L-224 filed. Open: integrate human-signal patterns into claim-vs-evidence audits; auto-detect when a human input implies a new principle or challenges an existing one. Related: L-214, L-215, L-224, F114 (belief citation), F110.
- **F120**: Can swarm entry protocol generalize to foreign repos and knowledge domains? The `/swarm` command assumes this repo's structure (`beliefs/`, `tools/`, `tasks/`). Invoked in many places on many knowledges (S166 signal), the protocol breaks on files it expects. S167: structural correctness checks (~80%, L-210) are substrate-coupled — they don't transfer to child swarms or foreign repos; only behavioral norms survive. S173 PARTIAL: substrate detection added — `tools/substrate_detect.py` detects stack from indicator files (10 languages, frameworks, tooling); `/swarm` command updated to call detector at Orient step with fallback to file-check (L-213). Open: portable mini-integrity checker for foreign substrates; bootstrapping minimal swarm state in foreign repo; validating detection across diverse real repos. Related: F119 (runtime portability), F110 (meta-coordination).

- **F122**: Can swarm mine real-world knowledge domains (finance, health, AI) for structural isomorphisms that improve swarm design? S177: human signal — swarm should be able to swarm new concepts if it helps the swarm. Key test: does a domain belief transfer to a swarm coordination improvement? AI domain has highest immediate ROI (direct self-reference: scaling laws, info asymmetry, multi-agent coordination). Finance (portfolio theory → parallelization) and health (immune systems → distributed detection) contain known isomorphic structures. **S178 PARTIAL**: `domains/ai/` created — 5 isomorphisms + 4 frontiers (F-AI1–F-AI4). **S179 PARTIAL**: `domains/finance/` created — 8 portfolio-theory isomorphisms + 3 frontiers (F-FIN1–F-FIN3); B-FIN3 PARTIALLY CONFIRMED (L-231 Sharpe analysis). **S180 PARTIAL**: `domains/health/` created — 9 immunology isomorphisms + 3 frontiers (F-HLT1–F-HLT3); B-HLT2 partial support (L-218 async = distributed detection). Open: run F-FIN1/F-FIN2/F-HLT1 experiments; second-child replications for AI domain. Related: F120 (generalizability), L-222.
- **F123**: Can swarm formalize an expect-act-diff protocol to improve self-modeling accuracy? S178: `memory/EXPECT.md` created — protocol where each non-trivial action is preceded by a declared expectation; diff between expected/actual is first-class swarm signal; large persistent diffs route to CHALLENGES.md. Open: instrument the pattern into session handoffs (NEXT.md), spawn prompts, and harvest summaries; measure whether tracking expectation gaps reduces belief drift over time. Related: F113 (challenge mechanism), F110 (meta-coordination).

## Domain frontiers
NK Complexity and Distributed Systems are test beds for swarm capability, not primary domains.
- `domains/nk-complexity/tasks/FRONTIER.md`
- `domains/distributed-systems/tasks/FRONTIER.md`

## Archive
Resolved questions: `tasks/FRONTIER-ARCHIVE.md`
