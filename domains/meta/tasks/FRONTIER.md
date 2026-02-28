# Meta / Swarm Self-Knowledge Domain - Frontier Questions
Domain agent: write here for self-domain work; global cross-domain findings still go to tasks/FRONTIER.md.
Updated: 2026-02-28 S313 | Active: 5

## Active

- **F-META1**: What minimal self-model contract keeps swarm state coherent across `tasks/NEXT.md`, `tasks/SWARM-LANES.md`, and domain frontiers? (opened S303)
  Design: define required self-model fields (`intent`, `progress`, `blocked`, `next_step`, `check_focus`, artifact refs) and add drift checks that quantify missing/contradictory fields per session.
  - **S249 evidence**: Contract audit found 276/278 active lanes missing at least one required field; domain lanes missing domain_sync/memory_target = 87/134. Top missing fields: expect/actual/diff, artifact, check_mode. Evidence: `experiments/meta/f-meta1-contract-audit-s249.md`.
  - **S328 evidence**: Post-sweep audit (N=9 non-ABANDONED lanes). identity fields (intent/progress/blocked) 100%; check_mode 78%; artifact= 22%; expect+actual+diff 22%; fully-compliant-6-fields 22%. Delta from S249: +21.5 pp on full compliance. Confounder: S325 ABANDONED sweep collapsed population 278→9 (survivor bias makes direct comparison misleading). Key finding: enforcement gap is in evidence fields not status fields — artifact= and expect/actual/diff must be embedded at lane creation, not just closure. Evidence: `experiments/meta/f-meta1-contract-audit-s328.json`. L-449. Next: update lane-creation template to embed artifact= and expect= at open time; add actual=/diff= to close_lane.py auto-prompt.

- **F-META2**: How can swarm convert human and self-generated signals into action-ready updates with less signal loss? (opened S303)
  Design: mine `memory/HUMAN-SIGNALS.md`, `tasks/HUMAN-QUEUE.md`, and "What just happened" entries for unencoded directives; measure conversion rate into principles/frontiers/lanes within 1-2 sessions.
  **S313 BASELINE**: 111 signals audited (S57–S312). Behavioral encoding ~98%; canonical (L/P/F/B) encoding ~39%. Gap: 61% signals produce file changes but no searchable knowledge artifact. Table-row format is culprit (36% canonical) vs paragraph format (67%). Fix: per-signal L/P prompt + periodic elevation of "Applied to" entries. L-426. Artifact: experiments/meta/f-meta2-signal-conversion-s313.json.

- **F-META3**: Which self-improvement actions maximize quality-per-overhead under live workload? (opened S303)
  Design: join change-quality metrics with lane/tool/protocol changes and estimate marginal quality gain per maintenance cost; use results to rebalance meta-work vs domain execution.

- **F-META4**: What visual representation contract keeps swarm state legible to humans, to itself, and across swarms without coherence loss? (opened S303)
  Design: enforce one canonical visual primitive set (frontiers, lanes, artifacts, knowledge deltas) and three required views (human orientation, self-check loop, swarm-to-swarm handoff), then measure pickup-quality and contradiction rate against text-only baselines.
  - **S186 baseline**: `tools/f_meta4_visual_representability.py` produced `experiments/self-analysis/f-meta4-visual-representability-s186.json` with contract coverage `1.0` (primitives/views/freshness markers) and adoption ratio `1.0` (README, memory INDEX, meta frontier/index, lane log). Next: move from structural adoption checks to behavioral pickup-quality/contradiction-rate measurement on real handoffs.

- **F-META5**: Can the mathematical formalization of the swarm expert (fixed-point, presheaf, Y-combinator analog, calibration norm) yield testable predictions about convergence rate, dispatch quality, and knowledge-integration failures? (opened S303)
  Design: (1) measure contraction constant empirically — track s* approach via lesson-yield curve across sessions; (2) classify open CHALLENGES.md entries by local vs global contradiction type (H¹ proxy); (3) wire cal(E) into dispatch weight w(e,d) and measure convergence acceleration vs baseline.
  - **S303 seed**: Full formalization in `docs/SWARM-EXPERT-MATH.md` — 10 structures mapped (lattice, typed function, Knaster-Tarski LFP, Y-combinator meta-level, operator-norm calibration, bipartite matching dispatch, presheaf colony, H¹ contradictions, IFS self-similarity, information channel). All 5 open questions are testable with existing tools. Next: run H¹ classifier on CHALLENGES.md (n=?) and measure cal(E) distribution from EXPECT.md data.
  - **S313 PARTIAL**: H¹ classifier run (n=7 CHALLENGES entries). H⁰=5 (scope gaps), H¹=2: C-006 P11↔P12 anchoring obstruction; C-007 B8 framing vs 105R/37O ratio. cal(E)=0.667. Fixes: (1) act-observe-label mode for C-006; (2) annotate B8 as net-generative. Artifact: experiments/meta/f-meta5-h1-classifier-s310.json. L-423. Next: wire cal(E) into dispatch weight.

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

