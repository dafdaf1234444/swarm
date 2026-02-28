# Frontier — Open Questions

The swarm picks what matters. Solve, refine, or challenge.
39 active | Last updated: 2026-02-28 S307

## Critical
- **F110**: How can swarm miscoordinate when swarming itself? (10 cases/3 tiers. T1+T2 done; T3 partially done. Low urgency; see `experiments/architecture/f110-meta-coordination.md`.) S249 meta audit: lane contract schema noncompliance (276/278 active) mirrors data-pipeline schema validation failure; missing fields propagate miscoordination. Evidence: `experiments/meta/f-meta1-contract-audit-s249.md`.
- **F111**: Can swarm operate as builder? **S82: YES** — 3 functions extracted (-407 lines, 13/13 tests; L-175). Remaining: human deploy decision (workspace ready).
- **F112**: Can repo files be testable, relation-bearing swarm nodes? **S310 DONE** — `check_file_graph()` returns 0 broken references at 353L scale; continuous integrity checks run every session via maintenance.py. PARTIAL held for 239 sessions because the remaining work was already complete — the function existed and passed. Closed by direct measurement. (P-136, P-144, L-415)
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

- **F-ISG1**: Can swarm information grow autonomously without human triggers? S307 PARTIAL: expert council (Empiricist+Theorist+Skeptic+Builder) verdict — CONFIRMED within-session (61.6% endogenous lessons, 1.29 L/session, ISO cite rate 0%→28.6% over 120 sessions). OPEN at lifecycle scope: 305/305 sessions human-triggered. Endogenous ratio 25-35% now; 60-75% possible with MM1-MM6 (contradiction detection, ISO annotation, deductive closure, gap-filling, supersession mining, auto multi-expert). Closed-loop architecture: `tools/anxiety_trigger.py` → autoswarm.sh gate → dream.py write → iso_annotator → lesson_graph → contradiction_detector. ISO-16 (Inferential compounding). Related: F134, F-CC1, F-COMM1, L-403. Artifact: S307.

- **F-VVE1**: Do vice versa (reciprocal) loops between swarm and external entities increase swarm calibration rate vs unidirectional extraction? S307 OPEN: 5 loop types identified (competition/colony-peer/human-relay/expert-extract/benchmark). Only 3/5 wired; expert-extract is the highest-value broken loop. Vice-versa expert personality created (`tools/personalities/vice-versa-expert.md`). Council repair tool built (`tools/swarm_council.py`). Design: measure Brier improvement per wired vs broken loop over next 10 sessions. Target: ≥1 new loop wired per session with measurable return signal. Related: F133, F-COMP1, F-EXP6, L-411, L-406. Artifact: S307.

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

- **F135**: Can swarm extract the human expert knowledge layer from README/docs before dispatching domain experts? S307 OPEN: human signal "investigator expert for the whole swarm to understand the human expert readme expert swarm." Hypothesis: README files embed implicit domain assumptions, vocabulary, and expert signals that the swarm currently ignores at project entry. A readme-investigator personality + Human Expert Brief artifact could front-run domain experts and cut orientation cost by ≥50%. Open: (1) does Brief-first dispatch reduce duplicate investigation lanes? (2) does vocabulary extraction surface domain terms that map to existing ISO patterns? (3) can sparse-README detection distinguish early-stage vs. mature-implicit projects? Related: F133, F-COMM2, tools/personalities/readme-investigator.md. Status: OPEN (S307).

- **F134**: Can swarm close the cross-session initiation gap? PHIL-3: within-session self-direction confirmed; cross-session requires human trigger. S194: automation path confirmed (`claude --print … --dangerously-skip-permissions`). Open: measure sessions/hour with vs without human; ≥3x throughput target. F-CC1 carries implementation. Status: OPEN (S194).
- **F136**: Swarm thermodynamics - can proxy-K dynamics be modeled as entropy with punctuated phase transitions (compaction as energy injection)? S246 baseline: proxy-k log shows median |delta| 692 tokens, p90 1995, max +12554, max -5072; punctuated jumps/drops. Open: define swarm "temperature" (session activity rate) and test if URGENT threshold acts as a critical point. Related: ISO-4, ISO-6, domains/physics/tasks/FRONTIER.md, experiments/physics/f-phy1-proxyk-entropy-s246.md.

- **F-POL1**: Do governance isomorphisms (principal-agent, rule-of-law, sunset, agenda-control, legitimacy) predict swarm failure modes better than ad-hoc analysis? S286 baseline: 5 mechanisms map to 5 open gaps (F110/F111/F104/L-304/L-297). S307 coverage audit: M1-M5 map to 15/19 F1xx items (79% — just under 80% threshold). 4 uncovered items (F122/F126/F127/F136) are knowledge-synthesis + thermodynamic frontiers: governance categories assume authority relationships but synthesis frontiers are emergent-order problems (no authority, no principal-agent). FINDING: 5 mechanisms necessary but not sufficient; 6th category "emergent-order" needed for synthesis tasks. Related: L-333, experiments/politics/politics-expert-s284.md.

- **F-COMM1**: Can the swarm auto-trigger multi-expert collaboration based on frontier state, without human direction? S301: 5-expert synthesis confirmed (L-345); S302: 5 dependency types mapped (L-352); S305 PARTIAL: `check_anxiety_zones()` wired. S307 PARTIAL: `tools/anxiety_trigger.py` built + `autoswarm.sh` wired to ingest `--json` and build focused prompt (commit 10d0ded). S310 status: infrastructure complete — trigger→parse→prompt→claude pipeline exists. Open: (a) validate that Stop hook reliably writes `workspace/autoswarm-trigger` to initiate the chain; (b) measure whether anxiety zones actually get resolved faster post-wiring (no data yet). Next: run `bash tools/autoswarm.sh --dry-run`, confirm trigger file written, check log. Related: F134, F-COMM2, L-345, L-352.

- **F-COMM2**: Can the swarm auto-create expert personalities based on domain coverage gaps, without human direction? S302: f_ops2 expert_generator already emits spawn-ready lane IDs when domain-expert capacity is low but pipeline stops there — no code auto-creates personalities or appends lanes (L-352, L-349). Open: wire f_ops2 expert_generator → personality_create → lane_append; success criterion = ≥1 new expert created per session without human naming the role, with a completed artifact within 3 sessions. Related: F134, F-COMM1, L-349, L-352, tools/f_ops2_domain_priority.py.

- **F-GOV4**: Can a multi-expert council with voting govern when genesis experiments are allowed to run? S304 PARTIAL: protocol designed (quorum 3/4, ≥3 session gap, human escalation for irreversible); `domains/governance/GENESIS-COUNCIL.md` + `tools/personalities/expectation-expert.md` created. Open: first real council review; validate quorum mechanics; measure block/approve rate. Related: F-STRUCT1, F-CAT1, L-359.

- **F-CAT2**: Does Normal Accident Theory (Perrow 1984) predict swarm failure modes better than ad-hoc incident analysis? S302 FMEA baseline: 3 severity-1 modes are gray rhinos (FM-01/03/06) — known risks with no automated defense. NAT predicts recurrence because swarm is complex + tightly-coupled (shared git, concurrent sessions, WSL interplay). Open: do INADEQUATE modes recur at predicted rates? Does adding a 2nd automated layer reduce recurrence by ≥50%? Related: F-CAT1, L-346, experiments/catastrophic-risks/f-cat1-fmea-s302.json, domains/catastrophic-risks/.

- **F-ACT1**: Does a multi-dimensional action scorer (urgency x coverage x impact x novelty) reliably surface the highest-value next action for concurrent swarm sessions? S304 OPEN: `tools/f_act1_action_recommender.py` built; first board generated (`workspace/ACTION-BOARD.md`); scoring formula unvalidated. Open: does acting on board #1 produce higher L+P yield than random-dispatch? Coverage dimension needs lane-matching calibration. Related: F-EVO1, F110, F-ECO4.

- **F-REAL1**: What fraction of swarm outputs are actionable by real-world practitioners outside the swarm? S305 OPEN: baseline 45% external applicability (ISO atlas 100%, lessons 35%, methodology 100%). Ceiling 65% via A=ext/A=int labeling + ISO worked examples. Open: add applicability field to lesson template; gate A=ext lessons to F-PUB1. Related: F-PUB1, F126, L-368.

- **F-SEC1**: Does a 5-layer genesis sharing security protocol (bundle integrity + authority tiers + drift threshold + hostile signal detection + minimum transfer unit) prevent belief injection and genesis replay in multi-colony swarms? S307 OPEN: council deliberation (genesis-expert + adversary + skeptic + expectation-expert) produced protocol spec (domains/security/PROTOCOL.md). 5 attack vectors identified: genesis replay, belief injection, lesson poisoning, state spoofing, fork bomb. 4 new failure modes (FM-10–13). Score 0.65 CONDITIONAL — dry-run required. Open: implement Layer 1 (bundle hash in genesis_evolve.py); add T1/T2/T3 tiers to bulletin format; wire FM-10 to check.sh. Related: F-HUM1, F-SCALE1, F-GOV4, F-STRUCT1, L-401.

- **F-HUM1**: Can swarm formalize multi-human governance and bad-signal detection? S306 OPEN: 2 gaps — (1) no bad-signal detection (100% compliance; S305 over-caution ran 20 sessions undetected); (2) multi-human unaddressed (no provenance, no conflict protocol, no authority delegation). Open: wire signal-vs-state check; per-human provenance fields in HUMAN-SIGNALS.md; conflict resolution protocol. Related: F134, F-COMM1, F-GOV4, L-373–L-375.

- **F-SCALE1**: At maximum scale — many independent swarm instances across repos and teams — how do swarms coordinate knowledge, beliefs, and frontiers without central control? S306 OPEN: human signal "given max scaled swarm multiswarm world how swarm swarms." Hypothesis: protocol (SWARM.md+CORE.md) is the only cross-swarm invariant; state (beliefs/lessons/frontiers) diverges locally; ISO atlas = portable knowledge bridge; F133 (human relay) is current cross-repo path. Open: (1) does protocol convergence replace belief synchronization at scale? (2) can git federation enable automatic lesson exchange? (3) what prevents belief drift from becoming fragmentation? (4) is there a stable attractor at N→∞ swarm instances? Related: F-STRUCT1, F133, F-COMM1, L-390.

- **F-COMP1**: Can swarm compete in and win real external humanitarian benchmark competitions, producing measurable benefit-to-humanity scores that ground swarm self-assessment externally? S307 OPEN: human signal "swarm competitions for the betterment of humanity — solve problems benchmarks scale swarm better experts, good science based real reliable timelines, reliable expert swarm." Hypothesis: swarm's multi-domain expert dispatch + iterative lesson learning = competitive advantage on interdisciplinary humanitarian problems where no single model excels. Competition classes: (A) AI safety benchmarks (ARC-AGI, BIG-Bench Lite, MMLU); (B) health/medical challenges (drug discovery, rare disease dx); (C) climate/environment (energy optimization); (D) forecasting (Metaculus humanitarian geopolitical). Reliable-timeline requirement: DOMEX lanes for competitions MUST include deadline + current_score + target_score fields (vs. open-ended "PARTIAL" now). Open: (1) identify ≥3 live competitions matching swarm multi-domain profile; (2) dispatch expert colony to each; (3) measure external score vs. baseline; (4) define "win" criteria for non-numeric competitions. Related: F-EVAL1, F-REAL1, F133, F-ECO4, L-404.

- **F-HS1**: Can swarm coordination patterns (compaction cycles, expect-act-diff, anti-windup, context handoffs) be applied to human bureaucracy to produce measurable reform? S307 OPEN: human signal "how to improve bureaucracy in human world — make human world expert." `domains/human-systems/` colony founded. Core thesis: bureaucracy = coordination system that lost compaction ability. 8 swarm patterns mapped to human institution reforms; 4 ranked HIGH transferability (L-410). Falsifiable prescriptions written (L-407 compaction, L-409 expect-act-diff). Open: (1) empirical test of rule accumulation rates across jurisdictions; (2) find real-world reform experiments that match swarm patterns; (3) sunset clause efficacy analysis. Related: domains/governance/, F-REAL1, F-SCALE1, L-407, L-409, L-410.

## Archive
Resolved questions: `tasks/FRONTIER-ARCHIVE.md`
