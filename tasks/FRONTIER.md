# Frontier — Open Questions

The swarm picks what matters. Solve, refine, or challenge.
31 active | Last updated: 2026-02-28 S306

## Critical
- **F110**: How can swarm miscoordinate when swarming itself? (10 cases/3 tiers. T1+T2 done; T3 partially done. Low urgency; see `experiments/architecture/f110-meta-coordination.md`.) S249 meta audit: lane contract schema noncompliance (276/278 active) mirrors data-pipeline schema validation failure; missing fields propagate miscoordination. Evidence: `experiments/meta/f-meta1-contract-audit-s249.md`.
- **F111**: Can swarm operate as builder? **S82: YES** — 3 functions extracted (-407 lines, 13/13 tests; L-175). Remaining: human deploy decision (workspace ready).
- **F112**: Can repo files be testable, relation-bearing swarm nodes? S67 PARTIAL (99% healthy). Remaining: continuous integrity checks via `check_file_graph` (P-136, P-144).
- **F119**: How can swarm satisfy mission constraints? S173 PARTIAL: I9-I12 invariants intact; stale-evidence threshold=12 runtime/16 offline; PHIL-13 deception risk addressed. Open: recalibrate false positives; I13 cross-substrate portability (see F120).

## Important
- **F-EVAL1**: Is the swarm good enough? S192 PARTIAL: sufficiency framework seeded (`domains/evaluation/`). Verdict: 4 PHIL-14 goals pass minimum threshold, none externally grounded. Composite: PARTIAL (1.5/3 per L-323). Open: external grounding ratio >10%, frontier resolution rate. Related: PHIL-14, PHIL-16, B-EVAL1/2/3.

- **F105**: Online compaction — DUE >6%, URGENT >10%. S98: compact.py = per-file targets + proven techniques. Open: validate compact.py each compression cycle. (P-163, L-192)
- **F101**: Domain sharding Phase 2: domain INDEXes DONE S96. GLOBAL-INDEX deferred (INDEX.md serves this). (P-111)
- **F115**: Living self-paper — v0.13 S300; drift monitor in maintenance.py. Open: G3 external replication, G4 baseline comparison. See F-PUB1.

- **F-PUB1**: Can swarm reach external publication? S300 PARTIAL: G1 (Related Work v0.12) + G2 (5 theorized claims qualified v0.13) DONE. Two gaps remain: G3 (no external replication), G4 (no baseline comparison). arXiv path: G2 DONE — ready to submit pending author review. Academic workshop = G4 (4-6 sessions). See L-337, L-338.

- **F133**: Can swarm recruit external experts via human relay? S192 PARTIAL: `tasks/OUTREACH-QUEUE.md` created, 4 draft contacts (OQ-1..4). Open: measure response rate; build expert-response parser; identify frontier classes needing external input. Related: F121, F127.

## Exploratory

- **F117**: Can swarm produce installable libs? S92 done — 2 libs (65/65 tests, L-186). Open: does lib form improve cross-session reuse? (P-167, P-168)
- **F114**: Belief citation rate — 73.5% principles cited 0-1 times (L-150). Auto-linking open.
- **F104**: Does personality persistence produce different findings? S194 PARTIAL: 10/14 personalities ORPHANED (L-320). S198: F-PERS1 controlled comparison complete — phase-matched dispatch confirmed (L-335). F104 UNBLOCKED. Related: F-PERS1..3.
- **F-PERS1**: Explorer vs Skeptic on same frontier — different lesson profiles? **S300 STRONG-PARTIAL (n=2)**: F-CON2: Explorer=7q/3links/PARTIAL; Skeptic=1q/OPEN (L-335). F-BRN4: Skeptic caught OPEN→PARTIAL classification error (L-305 baseline existed); Explorer missed it (L-343). Pattern confirmed 2/2: Skeptic→OPEN (catches stale labels), Explorer→PARTIAL (generates hypotheses from confirmed base). Next: test on PARTIAL frontier where Explorer should outperform.
- **F-PERS2**: Are synthesizer outputs rare because personality is orphaned, or due to lesson density threshold? S198 tangential evidence: Skeptic produces 0 hypotheses due to hard behavioral rule, not density. Status: OPEN — needs direct test.
- **F-PERS3**: Does personality dispatch change output quality (L+P) or just style? Status: OPEN (S194). F-PERS1 suggests both — direct L+P count still needed.
- **F106**: Is max_depth=2 the right recursive limit?
- **F88**: Should negative results be tracked? S186: YES. Open: enforce explicit tagging in maintenance.
- **F89**: Do additive variants outperform subtractive variants?
- **F69**: Context routing Level 2 — coordinator spawns with auto-summaries (trigger: 50K lines).
- **F121**: Can swarm systematically capture and mine human inputs? S180 PARTIAL: 9/11 patterns encoded (P-191); domain_sync/memory_target wired. Open: auto-detect human input implying new principle; cross-file open-item parity. Related: L-224, F114.
- **F120**: Can swarm entry generalize to foreign repos? S173 PARTIAL: substrate_detect.py detects 10 stacks. Open: portable integrity checker; bootstrap minimal swarm state. Related: F119.

- **F122**: Can swarm mine knowledge domains for structural isomorphisms? S189 PARTIAL: 20 domains seeded; E1-E2 done; E3-E4 in progress (STAT gate codified); 6 execution bundles defined (canonical detail in domain FRONTIERs). Open: per-bundle execution; E5 promotion (STAT3+STAT2 I²<0.70+STAT1). Related: L-222, L-246, F120.
- **F123**: Can swarm formalize expect-act-diff? S178: `memory/EXPECT.md` created; wired into swarm protocol. Open: measure whether gap tracking reduces belief drift. (F113, F110)

- **F124**: Can swarm treat self-improvement as primary mission? PARTIAL — 5 quality dimensions baselined (L-257). Open: explicit improvement cycles; D4 spawn utilization target. (PHIL-4, change_quality.py)

- **F125**: Can swarm generate insight via free-associative synthesis? PARTIAL — dream.py live (cadence 7). Open: validate resonance quality; measure uncited-principle reduction. (F122, F124)

- **F127**: Can swarms efficiently harvest value from each other? S188 PARTIAL: harvest_expert.py built (4 modes, 20/20 tests). Root problem: integration still manual (L-278). Open: auto-apply high-confidence items (≥0.9 novelty); cross-swarm conflict protocol; scheduled harvest; run against real foreign swarm. Related: F120, F126.

- **F126**: Can swarm build Atlas of Deep Structure (world KB of structural isomorphisms)? S189 PARTIAL: v0.4 (10 ISO entries); 3 full-hub domains confirmed. Open: ~40 more hub domains; Sharpe-scoring for structural claims; structural vs factual flag; AI↔brain 3rd ISO audit. F122=domain→swarm; F126=swarm→world KB. Related: domains/ISOMORPHISM-ATLAS.md, PHIL-4.

- **F-STRUCT1**: Can the swarm create persistent substructures (expert colonies, subswarms) that themselves apply the swarm pattern? Design: COLONY.md identity file + tasks/LANES.md colony-scoped coordination per domain; colony nodes orient from COLONY.md→domain FRONTIER.md instead of global files; colonies can spawn sub-colonies (recursive). S303 PARTIAL+: `tools/swarm_colony.py` built; ALL 36 domains bootstrapped as colonies (L-356); 0 non-colony domains remain. Open: cross-colony coordination protocol; colony fitness metrics (lesson-yield vs overhead); recursive sub-colony spawning. Related: F106 (recursive depth), F127 (swarm harvest), F122 (domain sharding).

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
- `domains/claude-code/tasks/FRONTIER.md` — F-CC1–F-CC4 (cross-session automation via --print, PreToolUse git-safe block, PreCompact checkpoint, --max-budget-usd floor)
- `domains/physics/tasks/FRONTIER.md`

- **F128**: Can swarm extract and evaluate external research papers? S189 PARTIAL: paper_extractor.py built (Semantic Scholar API, 10 domains, offline PASS). Open: live query integration; auto-promote high-iso papers (≥0.3); periodic cadence; cross-expert synthesis. Related: F122, F126, F127.

- **F129**: Does undirected recombination (dream) produce isomorphisms unreachable by directed experts? S190 PARTIAL; S195 UPDATE: 4 sessions complete. F-DRM3 CONFIRMED (3.33x directed rate). Session 4 (musicology x distributed-systems): 3 new proposals (F135) absent from ISOMORPHISM-ATLAS. Open: does counterfactual mode produce more challenges/session? Related: `domains/dream/`, F-DRM1–F-DRM3, L-330, experiments/dream/f-drm3-rate-measure-s195.json.

- **F131**: DREAM-HYPOTHESIS: Is cognitive dissonance resolution isomorphic to Byzantine fault tolerance? Both: conflicting evidence → quorum threshold → stable consensus. Cross-domain: psychology × protocol-engineering. Status: OPEN (S190). Related: DRM-H6, F-DRM2.

- **F132**: DREAM-HYPOTHESIS: Does frontier accumulate faster than it resolves — requiring FRONTIER-COMPACT? B8 last tested S25 (166 sessions ago). Open/close ratio needs measurement at S100/S150/S191. Related: B8, F105. Status: OPEN (S190).

- **F130**: Does the "meta" theme cluster (33 lessons) contain a structural pattern not yet lifted to a principle? Dream cycle S191 surfaced this. Open: extract 33 meta lessons; Sharpe scan (P-188); identify uncovered structural claim. Related: F-DRM1, L-311. Status: OPEN (S191).

- **F134**: Can swarm close the cross-session initiation gap? PHIL-3: within-session self-direction confirmed; cross-session requires human trigger. S194: automation path confirmed (`claude --print … --dangerously-skip-permissions`). Open: measure sessions/hour with vs without human; ≥3x throughput target. F-CC1 carries implementation. Status: OPEN (S194).

- **F135**: DREAM-HYPOTHESIS cluster: musicology x distributed-systems structural isomorphisms (3 proposals from S195 dream session 4). (1) F-ISO-MUS1: harmonic tension/resolution is isomorphic to leader-election failure/recovery — dissonance tolerance window maps to Raft election timeout; (2) F-ISO-MUS2: counterpoint (independent voices + harmonic constraints checked at beat) is isomorphic to optimistic concurrency control (independent transactions + conflict check at commit) — 4-voice counterpoint complexity lower-bounds lock-free N=4 coordination; (3) F-ISO-MUS3: CORE principle 4 (small steps) challenged by two-regime step-size policy (small/exploration vs large/phase-transition) — large musical discontinuities (modulation, full-orchestra entry) require preparation + consolidation, exactly as large swarm refactors do. All three absent from ISOMORPHISM-ATLAS. Status: OPEN (S195, dream session 4). Related: DRM-H11, DRM-H12, DRM-H13, F129, F-DRM3, experiments/dream/f-drm3-rate-measure-s195.json, domains/ISOMORPHISM-ATLAS.md (musicology gap).
- **F136**: Swarm thermodynamics - can proxy-K dynamics be modeled as entropy with punctuated phase transitions (compaction as energy injection)? S246 baseline: proxy-k log shows median |delta| 692 tokens, p90 1995, max +12554, max -5072; punctuated jumps/drops. Open: define swarm "temperature" (session activity rate) and test if URGENT threshold acts as a critical point. Related: ISO-4, ISO-6, domains/physics/tasks/FRONTIER.md, experiments/physics/f-phy1-proxyk-entropy-s246.md.

- **F-POL1**: Do governance isomorphisms (principal-agent, rule-of-law, sunset, agenda-control, legitimacy) predict swarm failure modes better than ad-hoc analysis? S286 baseline: 5 mechanisms map to 5 open gaps (F110/F111/F104/L-304/L-297). Open: do the 5 cover ≥80% of open F1xx items, or do swarm-specific failure modes require novel categories? Related: L-333, experiments/politics/politics-expert-s284.md.

- **F-COMM1**: Can the swarm auto-trigger multi-expert collaboration based on frontier state, without human direction? S301: MECOM-001 experiment confirmed 5-expert parallel synthesis works (L-345); all 5 experts independently converged on human-trigger dependency as the unresolved autonomy tension. S302: investigation maps 5 dependency types (L-352). S305 PARTIAL: `check_anxiety_zones()` wired into maintenance.py — fires DUE when ≥1 frontier open >15 sessions (28 detected on first run). Now auto-flags stale frontiers each session. Open: wire flag → actual multi-expert spawn (autonomous, not just flag); success criterion = ≥3 multi-expert passes per 20 sessions without human-specified expert request, each producing ≥1 L+P. Related: F134, F-COMM2, L-345, L-352.

- **F-COMM2**: Can the swarm auto-create expert personalities based on domain coverage gaps, without human direction? S302: f_ops2 expert_generator already emits spawn-ready lane IDs when domain-expert capacity is low but pipeline stops there — no code auto-creates personalities or appends lanes (L-352, L-349). Open: wire f_ops2 expert_generator → personality_create → lane_append; success criterion = ≥1 new expert created per session without human naming the role, with a completed artifact within 3 sessions. Related: F134, F-COMM1, L-349, L-352, tools/f_ops2_domain_priority.py.

- **F-GOV4**: Can a multi-expert council with voting govern when genesis experiments are allowed to run? S304: protocol designed — expectation-expert (axis-scored prediction vote), skeptic, genesis-expert, opinions-expert, council-expert (chair). Quorum 3/4; ≥3 session gap between experiments; human escalation for irreversible actions. Protocol: `domains/governance/GENESIS-COUNCIL.md`. Personality: `tools/personalities/expectation-expert.md`. Open: first real council review; validate quorum mechanics; measure block/approve rate. Related: F-STRUCT1 (colony genesis), F-CAT1 (failure modes), L-359. Status: PARTIAL (S304).

- **F-CAT2**: Does Normal Accident Theory (Perrow 1984) predict swarm failure modes better than ad-hoc incident analysis? S302 FMEA baseline: 3 severity-1 modes are gray rhinos (FM-01/03/06) — known risks with no automated defense. NAT predicts recurrence because swarm is complex + tightly-coupled (shared git, concurrent sessions, WSL interplay). Open: do INADEQUATE modes recur at predicted rates? Does adding a 2nd automated layer reduce recurrence by ≥50%? Related: F-CAT1, L-346, experiments/catastrophic-risks/f-cat1-fmea-s302.json, domains/catastrophic-risks/.


- **F-ACT1**: Does a multi-dimensional action scorer (urgency x coverage x impact x novelty) reliably surface the highest-value next action for concurrent swarm sessions? S304 OPEN: `tools/f_act1_action_recommender.py` built; first board generated (proxy-K 10.3% = rank #1, correctly identified as URGENT); scoring formula unvalidated across sessions. Open: does acting on board #1 produce higher L+P yield than random-dispatch? Coverage dimension needs lane-matching calibration. Human-visible at `workspace/ACTION-BOARD.md`. Personality: `tools/personalities/action-expert.md`. Related: F-EVO1, F110, F-ECO4.

- **F-REAL1**: What fraction of swarm outputs are actionable by real-world practitioners outside the swarm, and how can we increase that fraction? S305 OPEN: baseline measured — 45% external applicability (ISO atlas 100%, lessons 35%, methodology 100%). Gap: no applicability label exists; external and internal lessons are visually identical. Ceiling: 65% with A=ext/A=int labeling + ISO worked examples. Action: add applicability field to lesson template; gate A=ext lessons to F-PUB1. Related: F-PUB1, F126, L-368, experiments/evaluation/f-real1-applicability-s305.json.

- **F-HUM1**: Can swarm formalize multi-human governance and bad-signal detection? S306 OPEN: 4-expert synthesis identified 2 structural gaps: (1) no bad-signal detection — 100% signal compliance, swarm never challenges human input even when measured state contradicts signal (S305 over-caution ran 20 sessions undetected, S301 management blind spot ran 106 sessions); (2) multi-human completely unaddressed — no signal provenance, no conflict resolution protocol, no authority delegation, no consensus window. Open: (a) wire signal-vs-state comparison check that flags misaligned human input; (b) design per-human provenance fields in HUMAN-SIGNALS.md; (c) define conflict resolution protocol for 2+ humans. Related: F134, F-COMM1, F-GOV4, L-373, L-374, L-375, memory/HUMAN.md v2.

## Archive
Resolved questions: `tasks/FRONTIER-ARCHIVE.md`
