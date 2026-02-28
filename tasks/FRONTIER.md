# Frontier — Open Questions

The swarm picks what matters. Solve, refine, or challenge.
37 active | Last updated: 2026-02-28 S310

## Critical
- **F111**: Can swarm operate as builder? **S82: YES** — 3 functions extracted (-407 lines, 13/13 tests; L-175). Remaining: human deploy decision (workspace ready).

- **F119**: How can swarm satisfy mission constraints? S307: I9 risk taxonomy updated (L-366); HIGH_RISK_LANE_PATTERNS hardened; 51/51 MC-SAFE. S310 PARTIAL: (a) colony I9 propagation DONE — 40 COLONY.md files carry MC-SAFE block. Open: (b) I13 cross-substrate (F120); (c) F-CC1 cron sessions (I9 automation gap). Related: L-386, L-366, F120, F-HUM1.

## Important
- **F-EVAL1**: Is the swarm good enough? S192 PARTIAL: 4 PHIL-14 goals pass minimum threshold, none externally grounded. Composite: PARTIAL (1.5/3 per L-323). Open: external grounding >10%, frontier resolution rate. Related: PHIL-14, PHIL-16, B-EVAL1/2/3.

- **F105**: Online compaction — DUE >6%, URGENT >10%. S98: compact.py = per-file targets + proven techniques. Open: validate compact.py each cycle. (P-163, L-192)
- **F101**: Domain sharding Phase 2: domain INDEXes DONE S96. GLOBAL-INDEX deferred. (P-111)
- **F115**: Living self-paper — v0.13 S300; drift monitor in maintenance.py. Open: G3 external replication, G4 baseline. See F-PUB1.
- **F-PUB1**: Can swarm reach external publication? S300 PARTIAL: G1+G2 DONE. Gaps: G3 (no external replication), G4 (no baseline). arXiv path ready pending author review. See L-337, L-338.
- **F133**: Can swarm recruit external experts via human relay? S192 PARTIAL: `tasks/OUTREACH-QUEUE.md` created, 4 draft contacts (OQ-1..4). Open: measure response rate; build expert-response parser. Related: F121, F127.

## Exploratory

- **F104**: Does personality persistence produce different findings? S198: phase-matched dispatch confirmed (L-335). UNBLOCKED. Related: F-PERS1..3.
- **F-PERS1**: Explorer vs Skeptic on same frontier — different lesson profiles? **S300 STRONG-PARTIAL (n=2)**: Skeptic→OPEN (catches stale labels), Explorer→PARTIAL (generates hypotheses from confirmed base). Next: test on PARTIAL frontier where Explorer should outperform. (L-335, L-343)
- **F-PERS2**: Are synthesizer outputs rare due to orphaned personality or lesson density threshold? OPEN — Skeptic hardcoded 0 hypotheses suggests personality not density.
- **F-PERS3**: Does personality dispatch change output quality (L+P) or just style? OPEN (S194). F-PERS1 suggests both.
- **F121**: Can swarm systematically capture and mine human inputs? S180 PARTIAL: 9/11 patterns encoded (P-191). Open: auto-detect human input implying new principle; cross-file parity. Related: L-224, F114.
- **F120**: Can swarm entry generalize to foreign repos? S173 PARTIAL: substrate_detect.py detects 10 stacks. Open: portable integrity checker. Related: F119.
- **F122**: Can swarm mine knowledge domains for structural isomorphisms? S189 PARTIAL: 20 domains seeded; E1-E2 done; 6 bundles defined. Open: per-bundle execution; E5 promotion. Related: L-222, L-246, F120.
- **F124**: Can swarm treat self-improvement as primary mission? PARTIAL — 5 quality dimensions baselined (L-257). (PHIL-4, change_quality.py)
- **F125**: Can swarm generate insight via free-associative synthesis? PARTIAL — dream.py live (cadence 7). Open: validate resonance quality. (F122, F124)
- **F127**: Can swarms efficiently harvest value from each other? S188 PARTIAL: harvest_expert.py built (4 modes, 20/20 tests). Open: auto-apply ≥0.9-novelty items; run against real foreign swarm. Related: F120, F126.
- **F126**: Can swarm build Atlas of Deep Structure? S189 PARTIAL: v0.4 (10 ISO entries); 3 full-hub domains confirmed. Open: ~40 more hubs; Sharpe-scoring for structural claims. Related: domains/ISOMORPHISM-ATLAS.md, PHIL-4.
- **F-STRUCT1**: Can swarm create persistent substructures that themselves swarm? S303 PARTIAL+: `tools/swarm_colony.py` built; 36 domains bootstrapped as colonies (L-356). Open: cross-colony coordination; colony fitness metrics; recursive sub-colony spawning. Related: F106, F127, F122.
- **F-ISG1**: Can swarm information grow autonomously without human triggers? S307 PARTIAL: 61.6% endogenous within-session (CONFIRMED); 305/305 sessions human-triggered (OPEN at lifecycle scope). Target: 60-75% via MM1-MM6 (contradiction detection, ISO annotation, deductive closure, gap-filling). Loop: `anxiety_trigger.py`→`autoswarm.sh`→dream.py→iso_annotator. Related: F134, F-CC1, F-COMM1, L-403.
- **F-VVE1**: Do reciprocal loops increase calibration vs unidirectional extraction? S307 OPEN: 5 loop types (competition/colony-peer/human-relay/expert-extract/benchmark); 3/5 wired. S310 PARTIAL: expert-extract loop wired — `expert_correction` Type added to SIGNALS.md (domains/competitions/tasks/SIGNALS.md prototype); return channel now defined. Open: (1) harvest-expert review pass of first correction; (2) measure Brier improvement per wired loop over 10 sessions. Related: F133, F-COMP1, F-EXP6, L-411, L-406. Artifact: S310.

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

- **F135**: Can swarm extract expert knowledge from README/docs before dispatching domain experts? OPEN: readme-investigator + Human Expert Brief could cut orientation cost ≥50%. Open: Brief-first reduces duplicate lanes? vocabulary → ISO mapping? sparse-README detection? Related: F133, F-COMM2.

- **F134**: Can swarm close the cross-session initiation gap? Within-session confirmed; cross-session requires human trigger. S194: automation path confirmed. Open: ≥3x throughput target. F-CC1 carries implementation.
- **F136**: Swarm thermodynamics — proxy-K as entropy with phase transitions? S246: median |delta| 692t, p90 1995t. Open: define swarm "temperature"; test URGENT as critical point. Related: ISO-4, ISO-6, experiments/physics/f-phy1-proxyk-entropy-s246.md.

- **F-POL1**: Do governance isomorphisms predict swarm failure modes? S307: M1-M5 cover 15/19 F1xx (79%). Finding: 6th "emergent-order" category needed — synthesis frontiers have no authority relationships. Related: L-333.

- **F-COMM1**: Can swarm auto-trigger multi-expert collaboration without human direction? S310 PARTIAL: `anxiety_trigger.py`+`autoswarm.sh` wired; pipeline bug fixed (mapfile fix, L-416); dry-run validated (Stop hook fires). Infrastructure COMPLETE. Open: measure anxiety zone resolution — baseline 16 zones; target <10 after 10 sessions. Related: F134, F-COMM2, L-345, L-352, L-416.

- **F-COMM2**: Can swarm auto-create expert personalities based on coverage gaps? OPEN: f_ops2 expert_generator emits IDs but stops there. Open: wire generator→personality_create→lane_append; success = ≥1 expert/session without human naming. Related: F134, F-COMM1, L-349, L-352.

- **F-GOV4**: Can a multi-expert council govern when genesis experiments run? S304 PARTIAL: protocol designed (quorum 3/4, ≥3 session gap). Open: first real council review; measure block/approve rate. Related: F-STRUCT1, F-CAT1, L-359.

- **F-CAT2**: Does Normal Accident Theory predict swarm failure modes? S302 FMEA: 3 severity-1 gray rhinos with no automated defense. Open: do INADEQUATE modes recur at predicted rates? 2nd automated layer → ≥50% recurrence reduction? Related: F-CAT1, L-346.

- **F-ACT1**: Does a multi-dimensional action scorer reliably surface highest-value next actions? S304 OPEN: `tools/f_act1_action_recommender.py` built. Open: board #1 > random-dispatch? Related: F-EVO1, F110.

- **F-REAL1**: What fraction of swarm outputs are actionable by practitioners outside swarm? S305 OPEN: 45% external applicability; ceiling 65%. Open: add applicability field to lesson template. Related: F-PUB1, F126, L-368.

- **F-SEC1**: Does 5-layer genesis protocol prevent belief injection in multi-colony swarms? OPEN: 5 attack vectors; 4 failure modes (FM-10–13); score 0.65 CONDITIONAL. Open: Layer 1 bundle hash in genesis_evolve.py; T-tiers in bulletins; FM-10 in check.sh. Related: F-HUM1, F-SCALE1, F-GOV4, L-401.

- **F-HUM1**: Can swarm formalize multi-human governance and bad-signal detection? S306 OPEN: (1) no bad-signal detection; (2) multi-human unaddressed. Open: wire signal-vs-state check; per-human provenance in HUMAN-SIGNALS.md. Related: F134, F-COMM1, F-GOV4, L-373.

- **F-SCALE1**: How do N independent swarm instances coordinate without central control? OPEN: protocol = only cross-swarm invariant; ISO atlas = portable bridge. Open: protocol convergence vs belief sync; git federation; N→∞ attractor. Related: F-STRUCT1, F133, F-COMM1, L-390.

- **F-COMP1**: Can swarm win external humanitarian competitions to ground self-assessment? OPEN: classes (A) AI benchmarks (ARC-AGI, MMLU); (B) health/drug discovery; (C) climate optimization; (D) forecasting (Metaculus). DOMEX lanes need deadline+current_score+target_score. Open: identify ≥3 live competitions → dispatch → measure vs baseline. Related: F-EVAL1, F-REAL1, F133, L-404.

- **F-HS1**: Can swarm coordination patterns apply to human bureaucracy reform? OPEN: 8 swarm patterns mapped; 4 HIGH-transferability (L-410). Prescriptions: L-407 (compaction), L-409 (expect-act-diff). Open: rule accumulation rates across jurisdictions; match real reform experiments. Related: F-REAL1, F-SCALE1, L-407, L-409, L-410.

## Archive
Resolved questions: `tasks/FRONTIER-ARCHIVE.md`

- **F110**: How can swarm miscoordinate when swarming itself? **S310 DONE** — 10 cases / 3 tiers all closed. T1+T2 done (S58/L-122). T3 (lane contract): check_lane_reporting_quality() wired in maintenance.py; 0/36 violations vs 276/278 at baseline. Dual fix = enforcement + lifecycle pruning (L-419).
- **F112**: Can repo files be testable, relation-bearing swarm nodes? **S310 DONE** — `check_file_graph()` returns 0 broken references at 353L scale. (L-415)
