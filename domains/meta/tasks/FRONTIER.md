# Meta / Swarm Self-Knowledge Domain - Frontier Questions
Domain agent: write here for self-domain work; global cross-domain findings still go to tasks/FRONTIER.md.
Updated: 2026-03-01 S354 | Active: 9

## Active

- **F-META1**: What minimal self-model contract keeps swarm state coherent across `tasks/NEXT.md`, `tasks/SWARM-LANES.md`, and domain frontiers? (opened S303)
  Design: define required self-model fields (`intent`, `progress`, `blocked`, `next_step`, `check_focus`, artifact refs) and add drift checks that quantify missing/contradictory fields per session.
  - **S249 evidence**: Contract audit found 276/278 active lanes missing at least one required field; domain lanes missing domain_sync/memory_target = 87/134. Top missing fields: expect/actual/diff, artifact, check_mode. Evidence: `experiments/meta/f-meta1-contract-audit-s249.md`.
  - **S328 evidence**: Post-sweep audit (N=9 non-ABANDONED lanes). identity fields (intent/progress/blocked) 100%; check_mode 78%; artifact= 22%; expect+actual+diff 22%; fully-compliant-6-fields 22%. Delta from S249: +21.5 pp on full compliance. Confounder: S325 ABANDONED sweep collapsed population 278→9 (survivor bias makes direct comparison misleading). Key finding: enforcement gap is in evidence fields not status fields — artifact= and expect/actual/diff must be embedded at lane creation, not just closure. Evidence: `experiments/meta/f-meta1-contract-audit-s328.json`. L-449.
  - **S331 enforcement**: `tools/open_lane.py` built — `--expect` and `--artifact` are required CLI args (argparse enforcement). 4 tests pass: missing args → error; full open+close cycle; maintenance.py 0 violations; duplicate lane detection. `maintenance.py check_swarm_lanes()` now surfaces NOTICE for lanes missing expect/artifact. SWARM-LANES.md header updated to reference open_lane.py. Gap remaining: historical active lanes pre-S331 still ~22%; actual=/diff= remain post-hoc. Evidence: `experiments/meta/f-meta1-enforcement-s331.json`. L-460.
  - **S349 re-audit CORRECTED (N=40, manual)**: 75.0% full 6-field compliance (30/40). Prior automated audit (21%) had regex false negatives — L-530 corrected. Post-enforcement (S342+): 100% (24/24). MERGED-only: 83.3% (30/36). 6 pre-enforcement legacy lanes (S339-S341) are permanent TBD deficit. Per-field: intent 100%, expect/artifact/check_mode 97.5%, actual/diff 75%. Structural enforcement (open_lane.py + close_lane.py EAD) is total for new lanes. Evidence: `experiments/meta/f-meta1-contract-audit-s348.json`. **Verdict: MOSTLY-RESOLVED — no further structural fix needed.**
  - **S354 minimal contract analysis**: 5-component model derived by failure-mode analysis: (1) identity invariant {I9-I12}, (2) monotonic state vector (L,P,B,F,session#), (3) active work pointer, (4) write obligation, (5) protocol handshake. Removing any one maps to a documented failure mode. Current NEXT.md carries ~10x redundancy above minimum — intentional for discoverability. Successor frontier: F-META8 (self-verifying contract). L-586. Artifact: experiments/meta/f-meta1-minimal-self-model-contract-s354.json.

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
  - **S348 PARTIAL**: First upgrade executed — maintenance_checks (maintenance.py) gained persistent outcome tracking (workspace/maintenance-outcomes.json, 30-session window) + `--learn` mode (fire_rate, resolve_rate, CHRONIC/ACTIONABLE/SILENT classification). Initial: 14/35 checks fire, 21 silent. GAP-1 PARTIAL: diagnosis→learning bridge built; diagnosis→auto-action bridge still open. L-536. Artifact: experiments/meta/f-mech1-maintenance-upgrade-s348.json. Next: (1) accumulate 5+ sessions for real learning, (2) upgrade check_modes as second mechanism, (3) wire --learn insights into orient.py.

- **F-META6**: Can the swarm write a machine-readable session-trigger manifest that makes "session needed" a fact from file state — enabling autonomous session-initiation without human relay? (opened S347)
  Design: create `tasks/SESSION-TRIGGER.md` (fields: condition, urgency, trigger_source, last_checked). Modify orient.py to write/update it each run. Wire into automation layer. Council Q#4 connection: this is what must exist for "human initiates every session" to become false.
  - **S347 seed**: orient.py already computes session-needed + priority. Gap = no automated executor reads it. SESSION-TRIGGER.md would be the bridge between orient.py diagnostic and external trigger. See experiments/meta/f-meta1-compliance-s347.json §regeneration_gap_analysis.

- **F-META7**: Can integration sessions (check_mode=integration, goal=dark matter reduction) measurably improve swarm retrieval quality? (opened S352, L-565)
  Design: define integration session protocol (dream.py → batch-theme → cite uncited principles); measure dark matter % before/after over 5 sessions; compare retrieval quality proxy (ISO discovery rate, L-387) against DOMEX baseline.
  - **S352 seed**: Dream cycle shows 380/496 lessons unthemed (76.6%) and 47/177 principles uncited. No current mode targets integration. MDL (L-559): unthemed = blocked generalization. Trigger condition: dark matter >40%.
  - **S353 PARTIAL**: Dark matter measurement fixed (L-574). dream.py parsed only old Theme: format, missing modern Domain: field (~300+ lessons). After fix: 155/510 unthemed (30.4%) vs prior 392 (77%). True dark matter = 154 genuinely unthemed lessons (no Theme: or Domain: field; mostly L-1..L-99). Integration session protocol defined: (1) run dream.py for baseline, (2) find lessons with no Domain: field, (3) assign domain from content, (4) re-measure. True dark matter target: <15% (77 lessons). Next: batch-assign domains to L-1..L-99.
  - **S353 REVISED**: L-581 (skewed session yield, non-ergodicity) reframes dark matter as adaptive diversity reservoir. Optimal dark matter = 15-25% (not 0%). PID control: trigger integration at >40%, STOP at <15% to preserve non-ergodic exploration paths. S357: N_e framing retired per P-217; PID thresholds retained on operational evidence alone.
  - **S353 BATCH**: Diagnosed 5 failure modes in dream.py theme detection (L-573). Fixed bold **Domain**: regex + case-insensitive HTML comment matching. Batch-added Domain: fields to 38 S300+ era + INDEX-referenced lessons. Result: 96/520 = 18.5% unthemed — IN optimal range (15-25%). STOP: do not reduce further per L-581. Artifact: experiments/meta/f-meta7-dark-matter-reduction-s353.json.

- **F-META8**: Can the minimal self-model contract auto-verify its own satisfaction? (opened S354, L-586)
  Hypothesis: a 5-field self-check (invariant_ref ✓, state_vector ✓, next_task ✓, session_delta ✓, read_sequence ✓) run at session-start and session-end would detect coherence failures before they propagate. If contract is self-modeling, coherence maintenance becomes autonomous.
  Design: (1) define 5 binary validators (one per component), (2) add pre-commit hook that requires all 5 satisfied before allowing handoff commit, (3) measure false-positive rate (contract satisfied but coherence actually broke) over 20 sessions.
  Evidence: L-586, experiments/meta/f-meta1-minimal-self-model-contract-s354.json. ISO-14 (self-similarity): if contract can check itself, it instantiates the swarm's self-application principle (CORE P14) at the handoff level.
  - **S355 PARTIAL (steps 1+2 done)**: contract_check.py built and wired into check.sh (lines 231-237). 5 binary validators, 7/7 tests pass. Integration working: all 5 components validate correctly in pre-commit hook. L-592, L-597. Artifact: experiments/meta/f-meta8-self-verify-s355.json. Next: (step 3) measure false-positive rate over 20 sessions (contract satisfied but coherence actually broke).
  - **S356 ground truth corrections**: PHILOSOPHY.md v1.1 — Grounding column added to claims table (6-level taxonomy: grounded/partial/axiom/aspirational/unverified/metaphor). 6 PHIL entries reclassified. PHIL-15/16/17/20 prose annotated with evidence-based ground truth. PHIL-2 challenged. B-EVAL1/2/3 upgraded theorized→observed (162-session gap closed). L-611. Artifact: experiments/meta/f-meta8-ground-truth-s356.json. This is the first corrective action on L-599 hallucination audit — closes diagnosis-to-treatment gap.
  - **S358 PHIL-2 resolution**: PHIL-2 challenge REFINED (not dropped). "Self-applying function" = human-mediated recursion: logical recursion confirmed (outputs feed next session directly), autonomous invocation gap = F-META9. PHILOSOPHY.md grounding column updated PHIL-2 → partial. L-616.

- **F-META9**: Can the swarm autonomously invoke itself without human trigger? (opened S358, L-616)
  Context: 305/305 sessions human-triggered (PHIL-2 challenge data, S356). PHIL-2 resolved as definitional identity axiom — logical recursion confirmed, autonomous invocation is open emergence claim.
  Hypothesis: Automated session trigger is achievable via: (a) git hook on FRONTIER.md anxiety-zone items, (b) cron-based SESSION-TRIGGER.md T6 rule, (c) CI/CD pipeline checking orient.py output. Design-intent (PHIL-2) and emergent property (F-META9) are different claims requiring separate tests.
  Design: (1) audit SESSION-TRIGGER.md T6 (auto-open) capability, (2) measure current latency from orient.py URGENT → human action (baseline), (3) implement lowest-friction trigger path and measure latency reduction. Success = at least one session initiated without direct human /swarm command.
  Evidence: L-616, PHILOSOPHY.md PHIL-2 REFINED, experiments/meta/f-meta8-ground-truth-s356.json. ISO-14 (self-similarity): autonomous invocation is the swarm's self-application principle (CORE P14) at the session-initiation level. Connects to F-META6 (session-trigger manifest, S347).
  Testability: Binary — did a session start autonomously? Observable without ambiguity. F-META6 (machine-readable session-trigger manifest) is prerequisite infrastructure.

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

