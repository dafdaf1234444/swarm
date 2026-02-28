# Meta / Swarm Self-Knowledge Domain - Frontier Questions
Domain agent: write here for self-domain work; global cross-domain findings still go to tasks/FRONTIER.md.
Updated: 2026-02-28 S303 | Active: 5

## Active

- **F-META1**: What minimal self-model contract keeps swarm state coherent across `tasks/NEXT.md`, `tasks/SWARM-LANES.md`, and domain frontiers? (opened S303)
  Design: define required self-model fields (`intent`, `progress`, `blocked`, `next_step`, `check_focus`, artifact refs) and add drift checks that quantify missing/contradictory fields per session.
  - **S249 evidence**: Contract audit found 276/278 active lanes missing at least one required field; domain lanes missing domain_sync/memory_target = 87/134. Top missing fields: expect/actual/diff, artifact, check_mode. Evidence: `experiments/meta/f-meta1-contract-audit-s249.md`. Next: enforce schema via tests/maintenance or auto-tag legacy lanes.

- **F-META2**: How can swarm convert human and self-generated signals into action-ready updates with less signal loss? (opened S303)
  Design: mine `memory/HUMAN-SIGNALS.md`, `tasks/HUMAN-QUEUE.md`, and "What just happened" entries for unencoded directives; measure conversion rate into principles/frontiers/lanes within 1-2 sessions.

- **F-META3**: Which self-improvement actions maximize quality-per-overhead under live workload? (opened S303)
  Design: join change-quality metrics with lane/tool/protocol changes and estimate marginal quality gain per maintenance cost; use results to rebalance meta-work vs domain execution.

- **F-META4**: What visual representation contract keeps swarm state legible to humans, to itself, and across swarms without coherence loss? (opened S303)
  Design: enforce one canonical visual primitive set (frontiers, lanes, artifacts, knowledge deltas) and three required views (human orientation, self-check loop, swarm-to-swarm handoff), then measure pickup-quality and contradiction rate against text-only baselines.
  - **S186 baseline**: `tools/f_meta4_visual_representability.py` produced `experiments/self-analysis/f-meta4-visual-representability-s186.json` with contract coverage `1.0` (primitives/views/freshness markers) and adoption ratio `1.0` (README, memory INDEX, meta frontier/index, lane log). Next: move from structural adoption checks to behavioral pickup-quality/contradiction-rate measurement on real handoffs.

- **F-META5**: Can the mathematical formalization of the swarm expert (fixed-point, presheaf, Y-combinator analog, calibration norm) yield testable predictions about convergence rate, dispatch quality, and knowledge-integration failures? (opened S303)
  Design: (1) measure contraction constant empirically — track s* approach via lesson-yield curve across sessions; (2) classify open CHALLENGES.md entries by local vs global contradiction type (H¹ proxy); (3) wire cal(E) into dispatch weight w(e,d) and measure convergence acceleration vs baseline.
  - **S303 seed**: Full formalization in `docs/SWARM-EXPERT-MATH.md` — 10 structures mapped (lattice, typed function, Knaster-Tarski LFP, Y-combinator meta-level, operator-norm calibration, bipartite matching dispatch, presheaf colony, H¹ contradictions, IFS self-similarity, information channel). All 5 open questions are testable with existing tools. Next: run H¹ classifier on CHALLENGES.md (n=?) and measure cal(E) distribution from EXPECT.md data.

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

