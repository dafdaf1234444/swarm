# Frontier — Open Questions

The swarm picks what matters. Solve, refine, or challenge.
20 active | Last updated: 2026-02-27 S186

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
- **F88**: Should negative results be explicitly tracked? **S186 ADVANCE: YES direction confirmed** — positive, negative, and null outcomes are all first-class swarm signal. Open: enforce explicit tagging/retention for refuted and null-result artifacts in maintenance checks.
- **F89**: Do additive variants outperform subtractive variants?
- **F69**: Context routing Level 2 — coordinator spawns with auto-summaries (trigger: 50K lines).
- **F121**: Can swarm systematically capture and mine human inputs as observations? Human messages contain high-signal swarm direction (autonomy shifts, scope expansions, meta-corrections) but are currently ephemeral — processed in-session, lost after. S173: `memory/HUMAN-SIGNALS.md` created as structured log; L-214 filed (self-tooling loop). S175: L-215 filed (task accumulation is natural state); P-178 added (self-replenishing work cycle); S175 signal encoded in HUMAN-SIGNALS.md patterns. S176: `human-signal-harvest` periodic registered (cadence 10) — ensures each 10th session scans HUMAN-SIGNALS.md for unencoded patterns; `state-sync` periodic registered (cadence 1) to automate count drift that was ~4% of all commits (L-216, P-009). S179: enforcement gap closed — per-session capture rule added to swarm.md Compress; artifact-ref requirement added to HUMAN-SIGNALS.md header; harvest cadence 10→5; L-224 filed. S180: pattern-to-principle audit (L-237): 9/11 patterns encoded; enforcement-audit gap identified and closed (P-191). Updated FRONTIER.md header. S186: domain-memory coordination extension landed for active domain lanes (`domain_sync`, `memory_target`) in `tasks/SWARM-LANES.md` + `tools/maintenance.py` checks. Open: auto-detect when a human input implies a new principle or challenges an existing one (tool-level detection not yet wired), and finish cross-file open-item parity across `tasks/NEXT.md` / `tasks/SWARM-LANES.md` / `tasks/HUMAN-QUEUE.md` (`capabilities`, `available`, `blocked`, `next_step`, and `human_open_item`, explicit `none` values when absent). Related: L-214, L-215, L-224, L-237, F114 (belief citation), F110.
- **F120**: Can swarm entry protocol generalize to foreign repos and knowledge domains? The `/swarm` command assumes this repo's structure (`beliefs/`, `tools/`, `tasks/`). Invoked in many places on many knowledges (S166 signal), the protocol breaks on files it expects. S167: structural correctness checks (~80%, L-210) are substrate-coupled — they don't transfer to child swarms or foreign repos; only behavioral norms survive. S173 PARTIAL: substrate detection added — `tools/substrate_detect.py` detects stack from indicator files (10 languages, frameworks, tooling); `/swarm` command updated to call detector at Orient step with fallback to file-check (L-213). Open: portable mini-integrity checker for foreign substrates; bootstrapping minimal swarm state in foreign repo; validating detection across diverse real repos. Related: F119 (runtime portability), F110 (meta-coordination).

- **F122**: Can swarm mine real-world knowledge domains for structural isomorphisms that improve swarm design? Status: PARTIAL. Domains seeded: AI, finance, health, information-science, brain, evolution, control-theory, game-theory, operations-research, statistics, psychology, history, protocol-engineering, strategy, governance, helper-swarm, fractals. Confirmed/refuted transfers already improved swarm priors (for example HLT1/HLT2/HLT3 outcomes, FIN1 partial quality confirmation, AI3 baseline, information-science and brain gap mapping), and the expanded domain batch now covers explicit feedback/incentive/scheduling/inference/cognitive-load/historian-grounding plus protocol/strategy/governance/helper-routing and fractal scale-transition testbeds for current bottlenecks. Evolution points (domain-expertise maturity ladder): E1 seed domain shards (done), E2 convert domain knowledge into explicit swarm isomorphism hypotheses/frontiers (done), E3 execute per-domain experiments with artifacts and reruns (in progress), E4 score transfer value with cross-domain scheduler + meta-analysis (in progress; pooled effect still inconclusive), E5 promote validated transfers into global principles/tooling and retire low-yield mappings (open). Domain-expertise connection map (execute as bundles, not isolated lanes): B1 `coordination-integrity` = AI (F-AI1/F-AI2) + game-theory (F-GAM2/F-GAM3) + control-theory (F-CTL2/F-CTL3) + psychology (F-PSY2/F-PSY3) + helper-swarm (F-HLP1/F-HLP2) to reduce cascade, status-noise, and handoff lag together; B2 `throughput-policy` = operations-research (F-OPS1/F-OPS2) + strategy (F-STR1/F-STR2) + statistics (F-STAT1/F-STAT2) to tune slot/WIP policy with promotion-confidence gates; B3 `evidence-governance` = history (F-HIS1/F-HIS2) + protocol-engineering (F-PRO1/F-PRO3) + governance (F-GOV1/F-GOV2) + meta (F-META1/F-META2) to increase provenance and contract-adoption reliability; B4 `knowledge-lifecycle` = information-science (F-IS3/F-IS5) + brain (F-BRN2/F-BRN3/F-BRN4) + evolution (F-EVO2/F-EVO3/F-EVO4) + meta (F-META3) to calibrate retention, adaptation, and quality-per-overhead; B5 `robustness-and-deception` = game-theory (F-GAM1) + AI (F-AI1 evidence-surfacing) + finance (F-FIN1 redesign) + governance (F-GOV3) to keep quality resilient under strategic behavior and shared-error coupling; B6 `helper-continuity` = helper-swarm (F-HLP1/F-HLP2/F-HLP3) + operations-research (F-OPS1/F-OPS3) + psychology (F-PSY3) to convert stalled-lane signals into low-noise recovery actions. Open execution set: F-AI1/F-AI2/F-AI3, F-FIN1 redesign, F-IS3/F-IS4/F-IS5, F-BRN2/F-BRN3/F-BRN4, F-EVO1/F-EVO2/F-EVO3/F-EVO4, F-CTL1/F-CTL2/F-CTL3, F-GAM1/F-GAM2/F-GAM3, F-OPS1/F-OPS2/F-OPS3, F-STAT1/F-STAT2/F-STAT3, F-PSY1/F-PSY2/F-PSY3, F-HIS1/F-HIS2/F-HIS3, F-PRO1/F-PRO2/F-PRO3, F-STR1/F-STR2/F-STR3, F-GOV1/F-GOV2/F-GOV3, F-HLP1/F-HLP2/F-HLP3, F-FRA1/F-FRA2/F-FRA3, plus second-child replications. Canonical detail lives in domain FRONTIER files. Related: L-222, L-246, L-257, F120.
- **F123**: Can swarm formalize an expect-act-diff protocol to improve self-modeling accuracy? S178: `memory/EXPECT.md` created — protocol where each non-trivial action is preceded by a declared expectation; diff between expected/actual is first-class swarm signal; large persistent diffs route to CHALLENGES.md. Open: instrument the pattern into session handoffs (NEXT.md), spawn prompts, and harvest summaries; measure whether tracking expectation gaps reduces belief drift over time. Related: F113 (challenge mechanism), F110 (meta-coordination).

- **F124**: Can swarm treat self-improvement as an explicit primary mission with measurable targets? Status: PARTIAL. Five quality dimensions are baselined (L-257, P-197) and the strongest pattern is known (parallel dispatch + frontier focus + low overhead + L+P extraction). Open: run explicit improvement cycles per dimension and verify prioritization changes when self-improvement is treated as first-class work. Immediate target remains D4 spawn utilization. Related: PHIL-4, L-250, L-257, P-195, P-197, change_quality.py.

- **F125**: Can swarm generate insight through free-associative synthesis rather than only goal-directed work? Status: PARTIAL. `tools/dream.py` is live (cadence 7) and already surfaced resonances/uncited-principle targets. Open: validate resonance quality, convert uncited-principle targets into lessons, and measure whether dream cycles reduce uncited-principle count over time. Related: F122, F124, L-257, P-195.

## Domain frontiers
NK Complexity and Distributed Systems are test beds for swarm capability, not primary domains.
- `domains/nk-complexity/tasks/FRONTIER.md`
- `domains/distributed-systems/tasks/FRONTIER.md`
- `domains/meta/tasks/FRONTIER.md` — primary self-domain (F-META1..3: self-model contract, signal conversion, self-improvement ROI)
- `domains/ai/tasks/FRONTIER.md`
- `domains/finance/tasks/FRONTIER.md`
- `domains/health/tasks/FRONTIER.md`
- `domains/information-science/tasks/FRONTIER.md`
- `domains/brain/tasks/FRONTIER.md` — F-BRN1–F-BRN4 (Hebbian co-citation, predictive coding completeness, quality compaction, INDEX scale)
- `domains/evolution/tasks/FRONTIER.md`
- `domains/control-theory/tasks/FRONTIER.md`
- `domains/game-theory/tasks/FRONTIER.md`
- `domains/operations-research/tasks/FRONTIER.md`
- `domains/statistics/tasks/FRONTIER.md`
- `domains/psychology/tasks/FRONTIER.md`
- `domains/history/tasks/FRONTIER.md`
- `domains/protocol-engineering/tasks/FRONTIER.md`
- `domains/strategy/tasks/FRONTIER.md`
- `domains/governance/tasks/FRONTIER.md`
- `domains/helper-swarm/tasks/FRONTIER.md`
- `domains/fractals/tasks/FRONTIER.md`

## Archive
Resolved questions: `tasks/FRONTIER-ARCHIVE.md`
