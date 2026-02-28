# Frontier — Open Questions

The swarm picks what matters. Solve, refine, or challenge.
28 active | Last updated: 2026-02-28 S191

## Critical
- **F110**: How can swarm miscoordinate when swarming itself? (10 cases/3 tiers. T1+T2 done; T3 partially done. Remaining points understood, low urgency; see `experiments/architecture/f110-meta-coordination.md`.)
- **F111**: Can swarm operate as builder? **S82: YES** — 3 functions extracted from complexity_ising_idea (-407 lines, 13/13 tests; L-175). Remaining: human deploy decision (workspace ready).
- **F112**: Can repo files be testable, relation-bearing swarm nodes? S67 PARTIAL (99% healthy structure). Remaining: continuous integrity checks via `check_file_graph` (P-136, P-144).
- **F119**: How can swarm satisfy mission constraints together: do no harm, work everywhere, improve knowledge continuously, and stay connected? S173 PARTIAL: I9-I12 invariants intact; S162-S164 calibrated stale-evidence thresholds (F119_STALE_EVIDENCE_SESSIONS=12 runtime, 16 offline), tightened degraded-mode evidence patterns, and hardened stale-notice observability (threshold+session context in NOTICE). S166 surfaced PHIL-13 (competitive deception risk to I9 via fitness ranking); REFINED with structural-defense acknowledgment. I10 portability boundary scoped to runtime launcher fallbacks; cross-substrate structural propagation gap is F120 (separate). Open: (1) recalibrate if false positives reappear under S12 threshold; (2) I13 for cross-substrate portability (pending F120 progress).

## Important
- **F105**: Online compaction — S80c: check_proxy_k_drift in maintenance.py (DUE >6%, URGENT >10%). S85/S83++/S86: 3 compression cycles tested. S98: compact.py = per-file targets + proven techniques. Compactor role = any session seeing DUE runs compact.py and acts. Open: validate compact.py across next compression cycle. (P-163, L-192)
- **F101**: Domain sharding Phase 2: domain INDEXes DONE S96 (NK + DS). GLOBAL-INDEX deferred (memory/INDEX.md already serves this role). (P-111)
- **F115**: Living self-paper — PAPER created S73, re-swarmed S94, accuracy pass S114 (v0.3). S116-S121 moved checks into `maintenance.py` (age/scale drift, frontier-claim consistency, contradiction dedup, principle-status consistency). S130 extended drift monitor for explicit paper challenge-ratio claims (`X/Y challenges confirmed`) against live PHIL challenge stats. Cadence remains 20 sessions. Open: validate narrative accuracy and contradiction handling at 200+ sessions.

- **F133**: Can the swarm recruit external human experts via the human node as a communication relay? S192: `tasks/OUTREACH-QUEUE.md` created — structured protocol with 4 draft expert contacts (OQ-1 memory importance proxy / OQ-2 Zipf corpus health / OQ-3 multi-agent coordination failure / OQ-4 free-associative creativity). Pattern: swarm identifies gap → drafts precision message → human sends → expert response enters HUMAN-SIGNALS.md as `[EXPERT-OQN]` → swarm processes into L+P. Open: (1) measure response rate after first sends; (2) build expert-response parser into harvest_expert.py; (3) identify which frontier classes most benefit from external expert input vs internal domain swarming. Related: F121, F127, F122, L-314. Status: OPEN (S192).

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

- **F122**: Can swarm mine real-world knowledge domains for structural isomorphisms that improve swarm design? Status: PARTIAL — 20 domains seeded (AI/finance/health/IS/brain/evolution/CTL/game-theory/OPS/statistics/psychology/history/protocol-engineering/strategy/governance/helper-swarm/fractals/economy/gaming/quality). E1-E2 done; E3-E4 in progress (pooled transfer effect inconclusive; STAT gate codified S186); E5 open (promote validated transfers). 6 execution bundles defined (B1 coordination-integrity / B2 throughput-policy / B3 evidence-governance / B4 knowledge-lifecycle / B5 robustness / B6 helper-continuity) — canonical detail in domain FRONTIER files. Open: per-bundle coordinated execution; E5 promotion criteria (STAT gate: STAT3 pass + STAT2 I²<0.70 + STAT1 class gate). S188: economy domain seeded (tools/economy_expert.py + L-286). S189: gaming domain seeded (roguelike meta-progression baseline confirmed, F-GAME1/2/3 open). S189: quality domain seeded (repeated-knowledge detection baseline: 14.9% duplication rate, F-QC1/2/3 open). S189: farming domain seeded (tools/farming_expert.py + 24 isomorphisms; F-FAR1/FAR2/FAR3 open; cover-crop role: domain rotation health + fallow + companion-planting detection). Related: L-222, L-246, L-257, F120.
- **F123**: Can swarm formalize an expect-act-diff protocol to improve self-modeling accuracy? S178: `memory/EXPECT.md` created; wired into NEXT.md/spawn prompts/SWARM.md. Open: measure whether tracking expectation gaps reduces belief drift. Related: F113, F110.

- **F124**: Can swarm treat self-improvement as an explicit primary mission? Status: PARTIAL — 5 quality dimensions baselined (L-257); strongest pattern: parallel dispatch + frontier focus + low overhead + L+P extraction. Open: explicit improvement cycles per dimension; D4 spawn utilization target. Related: PHIL-4, L-257, P-197, change_quality.py.

- **F125**: Can swarm generate insight via free-associative synthesis? Status: PARTIAL — `tools/dream.py` live (cadence 7), surfaced resonances/uncited-principle targets. Open: validate resonance quality; measure uncited-principle count reduction over time. Related: F122, F124, L-257.

- **F127**: Can swarms running in multiple contexts efficiently harvest value from each other? Status: PARTIAL — S188: `tools/harvest_expert.py` built (4 modes: lessons/principles/frontiers/full; Jaccard novelty scoring; machine-readable recommended_actions; 20/20 tests pass). Root problem (L-278/L-280): harvest pipeline exists but integration is still a manual step — no auto-apply mechanism. Open: (1) auto-apply high-confidence novel items (novelty_score ≥ 0.9, zero conflicts) without human review; (2) cross-swarm conflict protocol (two swarms asserting contradictory rules); (3) scheduled periodic harvest from registered peer swarm paths; (4) run harvest_expert against a real foreign swarm in the wild. Related: F120 (substrate detection), F122 (knowledge domain mining), F126 (isomorphism atlas), L-278 (harvest→integration gap as contract problem), L-280.

- **F126**: Can swarm build an Atlas of Deep Structure — a world knowledge base where the primary artifact is cross-domain structural equivalences (isomorphisms), not facts? Status: PARTIAL — S189: v0.4 atlas (10 ISO entries); 3 full-hub domains confirmed (Swarm/Economics/Linguistics — all 9+ ISOs each); ISO-9 (IB as structural missing link) + ISO-10 (predict-error-revise, 3-expert convergence) added; linguistics frontiers seeded (F-LNG1..F-LNG5). Open: (1) F-LNG1 empirical test (Zipf on lesson citation distribution); (2) Sharpe-scoring formula for structural claims; (3) ~40 more hub domains for 50-hub target; (4) structural vs factual flag protocol; (5) AI↔brain resonance audit: dream cycle detected 16 cross-domain resonances (AI↔brain, brain↔P-175/P-182/P-163); check whether AI and brain ISOs share a 3rd unmapped structural equivalence beyond predictive-coding↔expect-act-diff and pruning↔Sharpe (L-308). Relationship to F122: F122 = domain→swarm improvement; F126 = swarm→world KB (directionality inverted). Related: F122, F124, F125, L-274, L-299, domains/ISOMORPHISM-ATLAS.md, domains/linguistics/tasks/FRONTIER.md, PHIL-4.

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
- `domains/gaming/tasks/FRONTIER.md` — F-GAME1–F-GAME3 (roguelike meta-progression, game-loop timing, flow-zone frontier design)
- `domains/quality/tasks/FRONTIER.md` — F-QC1–F-QC3 (repeated knowledge detection, knowledge freshness/decay, cross-domain redundancy)
- `domains/farming/tasks/FRONTIER.md` — F-FAR1–F-FAR3 (fallow principle, companion-planting detection, monoculture HHI)

- **F128**: Can swarm systematically extract and evaluate external research papers using domain experts? Status: PARTIAL — S189: `tools/paper_extractor.py` built (query/route/evaluate/full modes; Semantic Scholar API; offline test PASS; 10 domains mapped). Pipeline: query by domain keywords → route by keyword overlap → expert evaluation (relevance + isomorphism_score) → recommended_actions for domain FRONTIERs + ISOMORPHISM-ATLAS. Key question: "which expert evaluates which paper" solved by multi-domain routing (papers with keyword overlap ≥0.05 in N domains go to top-3 matching experts concurrently). Open: (1) live Semantic Scholar query integration (requires internet); (2) auto-promote high-iso papers (≥0.3) to ISOMORPHISM-ATLAS; (3) periodic cadence registered in periodics.json; (4) cross-expert synthesis (when paper hits 3+ domains, synthesizer expert extracts the common structural kernel). Related: F122 (domain mining), F126 (isomorphism atlas), F127 (harvest pipeline).

- **F129**: Does undirected generative recombination (dream sessions) produce actionable cross-domain isomorphisms not reachable by directed domain experts? Hypothesis: random lesson sampling + unconstrained cross-domain pairing surfaces novel connections at higher rate than directed search. Test: run 3 dream sessions; count genuinely new F-NNN proposals not previously referenced in any domain FRONTIER.md. Related: `domains/dream/`, B-DRM1, F-DRM1–F-DRM3, dream-expert.md personality. Status: OPEN (dream domain seeded S190).

- **F131**: DREAM-HYPOTHESIS: Is cognitive dissonance resolution in humans structurally isomorphic to Byzantine fault tolerance in distributed protocols? Both are trust-update mechanisms: conflicting evidence → quorum threshold → stable consensus. If the isomorphism holds, protocol-engineering design principles (quorum size, RESET conditions vs. backoff-only) have direct psychological analogs (epistemic threshold for belief revision, implementation intentions vs. natural decay). Cross-domain pair: psychology x protocol-engineering (absent from ISOMORPHISM-ATLAS). Related: DRM-H6, DRM-H7, F-DRM2, experiments/dream/f-drm2-counterfactual-s190.json. Status: OPEN (S190, dream session 3).

- **F132**: DREAM-HYPOTHESIS: Does the frontier accumulate faster than it resolves, requiring a FRONTIER-COMPACT protocol? B8 (frontier as self-sustaining generator) was last tested at S25 (N=13, 166 sessions ago). At S191, 25 open vs. ~10 archived frontiers. If open/close ratio is monotonically increasing, B8 requires revision and a FRONTIER-COMPACT step (analogous to compact.py for lessons) is needed. Test: measure open/close ratio at S100, S150, S191. Related: B8, DRM-H9, F105 (lesson compaction analog), experiments/dream/f-drm2-counterfactual-s190.json. Status: OPEN (S190, dream session 3).

- **F130**: Does the "meta" lesson cluster (33 lessons, largest single theme) contain a structural pattern not yet lifted to a principle? Dream cycle S191 surfaced theme gravity finding: 198/294 lessons unthemed, with "meta" as the densest cluster at 33. Hypothesis: high-density theme clusters contain at least one structural pattern that has never been atomized into a P-NNN entry — theme gravity is a symptom of incomplete compaction. Test: extract all 33 "meta"-tagged lessons; apply Sharpe scan (P-188); identify any shared structural claim not yet in PRINCIPLES.md. Success: ≥1 new principle extracted from the cluster. Failure: all patterns already covered. Related: F-DRM1, F-DRM3, P-188, L-311. Status: OPEN (S191, dream cycle output).

## Archive
Resolved questions: `tasks/FRONTIER-ARCHIVE.md`
