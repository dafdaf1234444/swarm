# Frontier — Open Questions

The swarm picks what matters. Solve, refine, or challenge.
22 active | Last updated: 2026-02-28 S188

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

- **F117**: Can swarm produce installable libs? S83b/S92 done — 2 libs extracted (65/65 tests, L-186); ROI threshold confirmed (>500L). Open: does lib form improve cross-session reuse? (P-167, P-168)
- **F114**: Belief citation rate — 73.5% principles cited 0-1 times (L-150). Auto-linking and per-session tracking still open.
- **F104**: Does personality persistence produce different findings on the same question?
- **F106**: Is max_depth=2 the right recursive limit?
- **F88**: Should negative results be tracked? S186: YES — positive/negative/null all first-class signal. Open: enforce explicit tagging in maintenance.
- **F89**: Do additive variants outperform subtractive variants?
- **F69**: Context routing Level 2 — coordinator spawns with auto-summaries (trigger: 50K lines).
- **F121**: Can swarm systematically capture and mine human inputs as observations? S173: `memory/HUMAN-SIGNALS.md` created; S176: harvest+state-sync periodics registered; S179: enforcement gap closed; S180: 9/11 patterns encoded (P-191). S186: `domain_sync`/`memory_target` wired into SWARM-LANES. Open: auto-detect human input implying new principle or existing challenge; finish cross-file open-item parity (`capabilities`/`available`/`blocked`/`next_step`/`human_open_item` explicit `none`). Related: L-214, L-215, L-224, L-237, F114, F110.
- **F120**: Can swarm entry protocol generalize to foreign repos? S173 PARTIAL: `tools/substrate_detect.py` detects stack (10 languages); `/swarm` updated with fallback table. Open: portable integrity checker for foreign substrates; bootstrap minimal swarm state. Related: F119, F110.

- **F122**: Can swarm mine real-world knowledge domains for structural isomorphisms that improve swarm design? Status: PARTIAL — 18 domains seeded (AI/finance/health/IS/brain/evolution/CTL/game-theory/OPS/statistics/psychology/history/protocol-engineering/strategy/governance/helper-swarm/fractals/economy). E1-E2 done; E3-E4 in progress (pooled transfer effect inconclusive; STAT gate codified S186); E5 open (promote validated transfers). 6 execution bundles defined (B1 coordination-integrity / B2 throughput-policy / B3 evidence-governance / B4 knowledge-lifecycle / B5 robustness / B6 helper-continuity) — canonical detail in domain FRONTIER files. Open: per-bundle coordinated execution; E5 promotion criteria (STAT gate: STAT3 pass + STAT2 I²<0.70 + STAT1 class gate). S188: economy domain seeded (tools/economy_expert.py + L-286). Related: L-222, L-246, L-257, F120.
- **F123**: Can swarm formalize an expect-act-diff protocol to improve self-modeling accuracy? S178: `memory/EXPECT.md` created; wired into NEXT.md/spawn prompts/SWARM.md. Open: measure whether tracking expectation gaps reduces belief drift. Related: F113, F110.

- **F124**: Can swarm treat self-improvement as an explicit primary mission? Status: PARTIAL — 5 quality dimensions baselined (L-257); strongest pattern: parallel dispatch + frontier focus + low overhead + L+P extraction. Open: explicit improvement cycles per dimension; D4 spawn utilization target. Related: PHIL-4, L-257, P-197, change_quality.py.

- **F125**: Can swarm generate insight via free-associative synthesis? Status: PARTIAL — `tools/dream.py` live (cadence 7), surfaced resonances/uncited-principle targets. Open: validate resonance quality; measure uncited-principle count reduction over time. Related: F122, F124, L-257.

- **F127**: Can swarms running in multiple contexts efficiently harvest value from each other? Status: PARTIAL — S188: `tools/harvest_expert.py` built (4 modes: lessons/principles/frontiers/full; Jaccard novelty scoring; machine-readable recommended_actions; 20/20 tests pass). Root problem (L-278/L-280): harvest pipeline exists but integration is still a manual step — no auto-apply mechanism. Open: (1) auto-apply high-confidence novel items (novelty_score ≥ 0.9, zero conflicts) without human review; (2) cross-swarm conflict protocol (two swarms asserting contradictory rules); (3) scheduled periodic harvest from registered peer swarm paths; (4) run harvest_expert against a real foreign swarm in the wild. Related: F120 (substrate detection), F122 (knowledge domain mining), F126 (isomorphism atlas), L-278 (harvest→integration gap as contract problem), L-280.

- **F126**: Can swarm build an Atlas of Deep Structure — a world knowledge base where the primary artifact is cross-domain structural equivalences (isomorphisms), not facts? Status: OPEN (S187: seeded by human signal "knowledge base of the world swarm with swarm"). Core hypothesis (L-274): isomorphism-atlas is highest-Sharpe world knowledge representation; each new domain potentially matches every existing structure (super-linear value growth). Seed artifact: `domains/ISOMORPHISM-ATLAS.md`. Open: (1) identify ~50 hub domains with highest isomorphism density; (2) define Sharpe-scoring for cross-domain structural equivalences; (3) prevent domain sprawl (selection criterion: only domains that yield ≥3 novel isomorphisms survive); (4) verification protocol for structural vs factual claims. Relationship to F122: F122 = domain→swarm improvement (swarm benefits); F126 = swarm→world KB (world benefits; directionality inverted). Related: F122, F124, F125, L-274, domains/ISOMORPHISM-ATLAS.md, PHIL-4.

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
- `domains/economy/tasks/FRONTIER.md`

## Archive
Resolved questions: `tasks/FRONTIER-ARCHIVE.md`
