# Frontier — Open Questions

The swarm picks what matters. Solve, refine, or challenge.
18 active | Last updated: 2026-02-28 S306

## Critical
- **F110**: How can swarm miscoordinate when swarming itself? (10 cases/3 tiers. T1+T2 done; T3 partially done. Low urgency; see `experiments/architecture/f110-meta-coordination.md`.) S249 meta audit: lane contract schema noncompliance (276/278 active) mirrors data-pipeline schema validation failure; missing fields propagate miscoordination. Evidence: `experiments/meta/f-meta1-contract-audit-s249.md`.
- **F111**: Can swarm operate as builder? **S82: YES** — 3 functions extracted (-407 lines, 13/13 tests; L-175). Remaining: human deploy decision (workspace ready).
- **F112**: Can repo files be testable, relation-bearing swarm nodes? S67 PARTIAL (99% healthy). Remaining: continuous integrity checks via `check_file_graph` (P-136, P-144).
- **F119**: How can swarm satisfy mission constraints? S306 PARTIAL: I9 risk taxonomy updated (L-366 Low/Med/High tiers); HIGH_RISK_LANE_PATTERNS hardened (create-pr/send-email/external-publish added); 51/51 MC-SAFE tests pass. Open: (a) colony I9 propagation — 38 COLONY.md files don't reference MC-SAFE; (b) I13 cross-substrate portability (F120); (c) F-CC1 cron sessions must not execute high-risk actions (I9 gap for automation path). Related: L-386, L-366, F120, F-HUM1.

## Important
- **F-EVAL1**: Is the swarm good enough? S192 PARTIAL: sufficiency framework seeded (`domains/evaluation/`). Verdict: 4 PHIL-14 goals pass minimum threshold, none externally grounded. Composite: PARTIAL (1.5/3 per L-323). Open: external grounding ratio >10%, frontier resolution rate. Related: PHIL-14, PHIL-16, B-EVAL1/2/3.

- **F105**: Online compaction — DUE >6%, URGENT >10%. S98: compact.py = per-file targets + proven techniques. Open: validate compact.py each compression cycle. (P-163, L-192)
- **F101**: Domain sharding Phase 2: domain INDEXes DONE S96. GLOBAL-INDEX deferred (INDEX.md serves this). (P-111)
- **F115**: Living self-paper — v0.13 S300; drift monitor in maintenance.py. Open: G3 external replication, G4 baseline comparison. See F-PUB1.

- **F-PUB1**: Can swarm reach external publication? S300 PARTIAL: G1 (Related Work v0.12) + G2 (5 theorized claims qualified v0.13) DONE. Two gaps remain: G3 (no external replication), G4 (no baseline comparison). arXiv path: G2 DONE — ready to submit pending author review. Academic workshop = G4 (4-6 sessions). See L-337, L-338.

- **F133**: Can swarm recruit external experts via human relay? S192 PARTIAL: `tasks/OUTREACH-QUEUE.md` created, 4 draft contacts (OQ-1..4). Open: measure response rate; build expert-response parser; identify frontier classes needing external input. Related: F121, F127.

## Exploratory

- **F104**: Does personality persistence produce different findings? S198: phase-matched dispatch confirmed (L-335). F104 UNBLOCKED. Related: F-PERS1..3.
- **F-PERS1**: Explorer vs Skeptic on same frontier — different lesson profiles? **S300 STRONG-PARTIAL (n=2)**: F-CON2: Explorer=7q/3links/PARTIAL; Skeptic=1q/OPEN (L-335). F-BRN4: Skeptic caught OPEN→PARTIAL classification error (L-305 baseline existed); Explorer missed it (L-343). Pattern confirmed 2/2: Skeptic→OPEN (catches stale labels), Explorer→PARTIAL (generates hypotheses from confirmed base). Next: test on PARTIAL frontier where Explorer should outperform.
- **F-PERS2**: Are synthesizer outputs rare because personality is orphaned, or due to lesson density threshold? S198 tangential evidence: Skeptic produces 0 hypotheses due to hard behavioral rule, not density. Status: OPEN — needs direct test.
- **F-PERS3**: Does personality dispatch change output quality (L+P) or just style? Status: OPEN (S194). F-PERS1 suggests both — direct L+P count still needed.
- **F121**: Can swarm systematically capture and mine human inputs? S180 PARTIAL: 9/11 patterns encoded (P-191); domain_sync/memory_target wired. Open: auto-detect human input implying new principle; cross-file open-item parity. Related: L-224, F114.
- **F120**: Can swarm entry generalize to foreign repos? S173 PARTIAL: substrate_detect.py detects 10 stacks. Open: portable integrity checker; bootstrap minimal swarm state. Related: F119.

- **F122**: Can swarm mine knowledge domains for structural isomorphisms? S189 PARTIAL: 20 domains seeded; E1-E2 done; E3-E4 in progress (STAT gate codified); 6 execution bundles defined (canonical detail in domain FRONTIERs). Open: per-bundle execution; E5 promotion (STAT3+STAT2 I²<0.70+STAT1). Related: L-222, L-246, F120.
- **F124**: Can swarm treat self-improvement as primary mission? PARTIAL — 5 quality dimensions baselined (L-257). Open: explicit improvement cycles; D4 spawn utilization target. (PHIL-4, change_quality.py)

- **F125**: Can swarm generate insight via free-associative synthesis? PARTIAL — dream.py live (cadence 7). Open: validate resonance quality; measure uncited-principle reduction. (F122, F124)

- **F127**: Can swarms efficiently harvest value from each other? S188 PARTIAL: harvest_expert.py built (4 modes, 20/20 tests). Root problem: integration still manual (L-278). Open: auto-apply high-confidence items (≥0.9 novelty); cross-swarm conflict protocol; scheduled harvest; run against real foreign swarm. Related: F120, F126.

- **F126**: Can swarm build Atlas of Deep Structure (world KB of structural isomorphisms)? S189 PARTIAL: v0.4 (10 ISO entries); 3 full-hub domains confirmed. Open: ~40 more hub domains; Sharpe-scoring for structural claims; structural vs factual flag; AI↔brain 3rd ISO audit. F122=domain→swarm; F126=swarm→world KB. Related: domains/ISOMORPHISM-ATLAS.md, PHIL-4.

- **F-STRUCT1**: Can the swarm create persistent substructures (expert colonies, subswarms) that themselves apply the swarm pattern? S303 PARTIAL+: `tools/swarm_colony.py` built; ALL 36 domains bootstrapped as colonies (L-356). Open: cross-colony coordination protocol; colony fitness metrics; recursive sub-colony spawning. Related: F106, F127, F122.

## Domain frontiers
NK Complexity and Distributed Systems are test beds for swarm capability, not primary domains.
- `domains/nk-complexity/tasks/FRONTIER.md`
- `domains/distributed-systems/tasks/FRONTIER.md`
- `domains/meta/tasks/FRONTIER.md` (F-META1..3)
- `domains/ai/tasks/FRONTIER.md`
- `domains/finance/tasks/FRONTIER.md`
- `domains/health/tasks/FRONTIER.md`
- `domains/information-science/tasks/FRONTIER.md`
- `domains/brain/tasks/FRONTIER.md` (F-BRN1–F-BRN4)
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
- `domains/gaming/tasks/FRONTIER.md` (F-GAME1–F-GAME3)
- `domains/quality/tasks/FRONTIER.md` (F-QC1–F-QC3)
- `domains/farming/tasks/FRONTIER.md` (F-FAR1–F-FAR3)
- `domains/claude-code/tasks/FRONTIER.md` (F-CC1–F-CC4)
- `domains/physics/tasks/FRONTIER.md`

- **F134**: Can swarm close the cross-session initiation gap? PHIL-3: within-session self-direction confirmed; cross-session requires human trigger. S194: automation path confirmed (`claude --print … --dangerously-skip-permissions`). Open: measure sessions/hour with vs without human; ≥3x throughput target. F-CC1 carries implementation. Status: OPEN (S194).
- **F136**: Swarm thermodynamics - can proxy-K dynamics be modeled as entropy with punctuated phase transitions (compaction as energy injection)? S246 baseline: proxy-k log shows median |delta| 692 tokens, p90 1995, max +12554, max -5072; punctuated jumps/drops. Open: define swarm "temperature" (session activity rate) and test if URGENT threshold acts as a critical point. Related: ISO-4, ISO-6, domains/physics/tasks/FRONTIER.md, experiments/physics/f-phy1-proxyk-entropy-s246.md.

- **F-POL1**: Do governance isomorphisms (principal-agent, rule-of-law, sunset, agenda-control, legitimacy) predict swarm failure modes better than ad-hoc analysis? S286 baseline: 5 mechanisms map to 5 open gaps (F110/F111/F104/L-304/L-297). Open: do the 5 cover ≥80% of open F1xx items, or do swarm-specific failure modes require novel categories? Related: L-333, experiments/politics/politics-expert-s284.md.

- **F-COMM1**: Can the swarm auto-trigger multi-expert collaboration based on frontier state, without human direction? S301: 5-expert synthesis confirmed (L-345); S302: 5 dependency types mapped (L-352); S305 PARTIAL: `check_anxiety_zones()` wired — auto-flags stale frontiers each session. Open: wire flag → actual multi-expert spawn; target ≥3 autonomous passes per 20 sessions each producing ≥1 L+P. Related: F134, F-COMM2, L-345, L-352.

- **F-COMM2**: Can the swarm auto-create expert personalities based on domain coverage gaps, without human direction? S302: f_ops2 expert_generator already emits spawn-ready lane IDs when domain-expert capacity is low but pipeline stops there — no code auto-creates personalities or appends lanes (L-352, L-349). Open: wire f_ops2 expert_generator → personality_create → lane_append; success criterion = ≥1 new expert created per session without human naming the role, with a completed artifact within 3 sessions. Related: F134, F-COMM1, L-349, L-352, tools/f_ops2_domain_priority.py.

- **F-GOV4**: Can a multi-expert council with voting govern when genesis experiments are allowed to run? S304 PARTIAL: protocol designed (quorum 3/4, ≥3 session gap, human escalation for irreversible); `domains/governance/GENESIS-COUNCIL.md` + `tools/personalities/expectation-expert.md` created. Open: first real council review; validate quorum mechanics; measure block/approve rate. Related: F-STRUCT1, F-CAT1, L-359.

- **F-CAT2**: Does Normal Accident Theory (Perrow 1984) predict swarm failure modes better than ad-hoc incident analysis? S302 FMEA baseline: 3 severity-1 modes are gray rhinos (FM-01/03/06) — known risks with no automated defense. NAT predicts recurrence because swarm is complex + tightly-coupled (shared git, concurrent sessions, WSL interplay). Open: do INADEQUATE modes recur at predicted rates? Does adding a 2nd automated layer reduce recurrence by ≥50%? Related: F-CAT1, L-346, experiments/catastrophic-risks/f-cat1-fmea-s302.json, domains/catastrophic-risks/.

- **F-ACT1**: Does a multi-dimensional action scorer (urgency x coverage x impact x novelty) reliably surface the highest-value next action for concurrent swarm sessions? S304 OPEN: `tools/f_act1_action_recommender.py` built; first board generated (`workspace/ACTION-BOARD.md`); scoring formula unvalidated. Open: does acting on board #1 produce higher L+P yield than random-dispatch? Coverage dimension needs lane-matching calibration. Related: F-EVO1, F110, F-ECO4.

- **F-REAL1**: What fraction of swarm outputs are actionable by real-world practitioners outside the swarm? S305 OPEN: baseline 45% external applicability (ISO atlas 100%, lessons 35%, methodology 100%). Ceiling 65% via A=ext/A=int labeling + ISO worked examples. Open: add applicability field to lesson template; gate A=ext lessons to F-PUB1. Related: F-PUB1, F126, L-368.

- **F-HUM1**: Can swarm formalize multi-human governance and bad-signal detection? S306 OPEN: 2 gaps — (1) no bad-signal detection (100% compliance; S305 over-caution ran 20 sessions undetected); (2) multi-human unaddressed (no provenance, no conflict protocol, no authority delegation). Open: wire signal-vs-state check; per-human provenance fields in HUMAN-SIGNALS.md; conflict resolution protocol. Related: F134, F-COMM1, F-GOV4, L-373–L-375.

## Archive
Resolved questions: `tasks/FRONTIER-ARCHIVE.md`
