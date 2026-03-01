# Meta / Swarm Self-Knowledge Domain - Frontier Questions
Domain agent: write here for self-domain work; global cross-domain findings still go to tasks/FRONTIER.md.
Updated: 2026-03-01 S345 | Active: 6

## Active

- **F-META1**: What minimal self-model contract keeps swarm state coherent across `tasks/NEXT.md`, `tasks/SWARM-LANES.md`, and domain frontiers? (opened S303)
  Design: define required self-model fields (`intent`, `progress`, `blocked`, `next_step`, `check_focus`, artifact refs) and add drift checks that quantify missing/contradictory fields per session.
  - **S249 evidence**: Contract audit found 276/278 active lanes missing at least one required field; domain lanes missing domain_sync/memory_target = 87/134. Top missing fields: expect/actual/diff, artifact, check_mode. Evidence: `experiments/meta/f-meta1-contract-audit-s249.md`.
  - **S328 evidence**: Post-sweep audit (N=9 non-ABANDONED lanes). identity fields (intent/progress/blocked) 100%; check_mode 78%; artifact= 22%; expect+actual+diff 22%; fully-compliant-6-fields 22%. Delta from S249: +21.5 pp on full compliance. Confounder: S325 ABANDONED sweep collapsed population 278→9 (survivor bias makes direct comparison misleading). Key finding: enforcement gap is in evidence fields not status fields — artifact= and expect/actual/diff must be embedded at lane creation, not just closure. Evidence: `experiments/meta/f-meta1-contract-audit-s328.json`. L-449.
  - **S331 enforcement**: `tools/open_lane.py` built — `--expect` and `--artifact` are required CLI args (argparse enforcement). 4 tests pass: missing args → error; full open+close cycle; maintenance.py 0 violations; duplicate lane detection. `maintenance.py check_swarm_lanes()` now surfaces NOTICE for lanes missing expect/artifact. SWARM-LANES.md header updated to reference open_lane.py. Gap remaining: historical active lanes pre-S331 still ~22%; actual=/diff= remain post-hoc. Evidence: `experiments/meta/f-meta1-enforcement-s331.json`. L-460.
  - **S348 re-audit (N=40)**: 72.5% full 6-field compliance (up from 22% S328). Creation fields near-100% (intent 100%, check_mode/artifact/expect 97.5%). Closure fields: actual/diff 72.5%. Post-S331 enforcement: 76.3% vs Pre-S331: 0%. MERGED lanes: 80.6% full. Enforcement CONFIRMED working. Remaining gap is closure-time actual/diff only. L-449 updated. Evidence: `experiments/meta/f-meta1-contract-audit-s348.json`.

- **F-META2**: How can swarm convert human and self-generated signals into action-ready updates with less signal loss? (opened S303)
  Design: mine `memory/HUMAN-SIGNALS.md`, `tasks/HUMAN-QUEUE.md`, and "What just happened" entries for unencoded directives; measure conversion rate into principles/frontiers/lanes within 1-2 sessions.
  **S313 BASELINE**: 111 signals audited (S57–S312). Behavioral encoding ~98%; canonical (L/P/F/B) encoding ~39%. Gap: 61% signals produce file changes but no searchable knowledge artifact. Table-row format is culprit (36% canonical) vs paragraph format (67%). Fix: per-signal L/P prompt + periodic elevation of "Applied to" entries. L-426. Artifact: experiments/meta/f-meta2-signal-conversion-s313.json.

- **F-META3**: Which self-improvement actions maximize quality-per-overhead under live workload? (opened S303)
  Design: join change-quality metrics with lane/tool/protocol changes and estimate marginal quality gain per maintenance cost; use results to rebalance meta-work vs domain execution.
  - **S331 BASELINE (n=25 sessions, 7 types)**: DOMEX=3.9 yield, citation_sprint=3.9 (unique K_delta), human_signal=3.0, periodic_audit=1.5, maintenance=0. Prescription: maximize DOMEX ratio, batch maintenance at session end, suppress ISO when dark_matter=0%. Artifact: experiments/meta/f-meta3-quality-per-overhead-s331.json. L-459.

- **F-META4**: What visual representation contract keeps swarm state legible to humans, to itself, and across swarms without coherence loss? (opened S303)
  Design: enforce one canonical visual primitive set (frontiers, lanes, artifacts, knowledge deltas) and three required views (human orientation, self-check loop, swarm-to-swarm handoff), then measure pickup-quality and contradiction rate against text-only baselines.
  - **S186 baseline**: `tools/f_meta4_visual_representability.py` produced `experiments/self-analysis/f-meta4-visual-representability-s186.json` with contract coverage `1.0` (primitives/views/freshness markers) and adoption ratio `1.0` (README, memory INDEX, meta frontier/index, lane log). Next: move from structural adoption checks to behavioral pickup-quality/contradiction-rate measurement on real handoffs.

- **F-META5**: Can the mathematical formalization of the swarm expert (fixed-point, presheaf, Y-combinator analog, calibration norm) yield testable predictions about convergence rate, dispatch quality, and knowledge-integration failures? (opened S303)
  Design: (1) measure contraction constant empirically — track s* approach via lesson-yield curve across sessions; (2) classify open CHALLENGES.md entries by local vs global contradiction type (H¹ proxy); (3) wire cal(E) into dispatch weight w(e,d) and measure convergence acceleration vs baseline.
  - **S303 seed**: Full formalization in `docs/SWARM-EXPERT-MATH.md` — 10 structures mapped (lattice, typed function, Knaster-Tarski LFP, Y-combinator meta-level, operator-norm calibration, bipartite matching dispatch, presheaf colony, H¹ contradictions, IFS self-similarity, information channel). All 5 open questions are testable with existing tools. Next: run H¹ classifier on CHALLENGES.md (n=?) and measure cal(E) distribution from EXPECT.md data.
  - **S313 PARTIAL**: H¹ classifier run (n=7 CHALLENGES entries). H⁰=5 (scope gaps), H¹=2: C-006 P11↔P12 anchoring obstruction; C-007 B8 framing vs 105R/37O ratio. cal(E)=0.667. Fixes: (1) act-observe-label mode for C-006; (2) annotate B8 as net-generative. Artifact: experiments/meta/f-meta5-h1-classifier-s310.json. L-423. Next: wire cal(E) into dispatch weight.

- **F-MECH1**: Can upgrading tool-grade mechanisms to swarm-grade (adding persistent state + outcome-based learning) measurably improve swarm performance? (opened S342)
  Design: Select 2 tool-grade mechanisms (maintenance_checks, check_modes) and add: (a) persistent state tracking outcomes, (b) learning from outcomes to adjust future behavior. Measure before/after on actionable output rate.
  - **S342 BASELINE**: Mechanisms taxonomy (L-496). 22 mechanisms cataloged; 14 swarm-grade, 8 tool-grade. Tool→swarm upgrade path = add persistent state + outcome learning. ISO-5 most instantiated (8/22). 7 structural gaps, GAP-1 (diagnostic-execution bridge) most severe. 5 mutual-swarming pairs identified. Artifact: experiments/meta/mechanisms-taxonomy-s342.json.

- **F-META6**: Can the swarm write a machine-readable session-trigger manifest that makes "session needed" a fact from file state — enabling autonomous session-initiation without human relay? (opened S347)
  Design: create `tasks/SESSION-TRIGGER.md` (fields: condition, urgency, trigger_source, last_checked). Modify orient.py to write/update it each run. Wire into automation layer. Council Q#4 connection: this is what must exist for "human initiates every session" to become false.
  - **S347 seed**: orient.py already computes session-needed + priority. Gap = no automated executor reads it. SESSION-TRIGGER.md would be the bridge between orient.py diagnostic and external trigger. See experiments/meta/f-meta1-compliance-s347.json §regeneration_gap_analysis.

## Dead Ends (Negative Stigmergy — L-484 S7)
Approaches tried and confirmed unproductive. Check before starting new work in this domain.
Format: `REPELLENT: <approach> | tried: S<N> | result: <why failed> | see: L-<N>`

- REPELLENT: Splitting maintenance.py by check function | tried: S338 | result: All 37 checks registered in main(); no dead functions. Problem is cross-file duplication, not monolith structure | see: L-482
- REPELLENT: Counting P-NNN patterns for principle total | tried: S339 | result: Overcounts by including removed/subsumed P-refs in "Removed:" section. Use header count instead | see: swarm_state.py

## Legacy backlog (history continuity)

- **F103**: Swarm vs single-session benchmark on real tasks. (S303)
- **F104**: Personality persistence effect on findings. (S303)
- **F106**: Recursive depth calibration. (S303)
- **F107**: Minimal viable genesis complexity. (S303)
## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
| F101-P1 | DONE - domain FRONTIER files created; later evolved into broad domain-sharding baseline. | 52 | 2026-02-27 |
| F87 | moderate constraints outperformed no-falsification over longer horizon. | 44 | 2026-02-27 |
| F86 | recursive belief evolution works; second-generation descendants remained viable. | 42 | 2026-02-26 |

