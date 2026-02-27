# Information Science Domain Index
Updated: 2026-02-27 | Sessions: 186

## What this domain knows
- **4 core lessons**: L-232 (citation power-law), L-235 (age-normalized Sharpe/decay), L-256 (domain seed), L-262 (F-IS1 refutation + F-IS3 model correction)
- **Key beliefs**: B-IS1 (entropy-compaction predictor, REFUTED S183), B-IS2 (citation concentration/power-law signal, OBSERVED), B-IS3 (spawn discipline as precision/recall tradeoff, THEORIZED but now operationalized via `spawn_math.py`)
- **Active frontiers**: 3 in `domains/information-science/tasks/FRONTIER.md` (F-IS3, F-IS4, F-IS5)

## Lesson themes

| Theme | Key lessons/artifacts | Core insight |
|-------|------------------------|-------------|
| Power-law / Zipf | L-232, L-235 | Citation mass concentrates in a small lesson subset; zero-citation clusters are structural, not random noise |
| MDL / compaction | P-152, L-242 | Proxy-K behaves as rising sawtooth; compaction resets floor but growth resumes |
| Spawn math | L-262, `f-is3-spawn-math-s185.json`, `f-is3-spawn-math-s186-calibrated.json` | Spawn-size decisions need correlation-aware variance benefit minus explicit coordination cost |
| Preset routing | `f-is3-sensitivity-s186.json`, `f-is3-spawn-presets-s186.json` | F-IS3 now has executable spawn regimes (P0 no-spawn, P1 duo, P2 broad) pending live cost calibration |
| arXiv intake swarming | `tools/f_is5_arxiv_swarmable.py`, `f-is5-arxiv-swarmable-s186-rerun.json` | Literature discovery can be lane-partitioned into repeatable distill tasks instead of ad-hoc paper drops, with explicit selected/backlog accounting |
| Lane distillation scoring | `tools/f_is5_lane_distill.py`, `f-is5-lane-distill-s186-selected-vs-backlog.json` | Owner-isolated selected-vs-backlog passes remove collisions but also remove transfer overlap signal (0.0 acceptance), motivating controlled-overlap scoring |

## Structural isomorphisms with swarm design

| Information Science finding | Swarm implication | Status |
|----------------------------|-------------------|--------|
| Entropy H(X) as uncertainty proxy | Belief-state entropy did not vary enough to predict compaction timing; proxy-K remains primary trigger | REFUTED for this substrate (B-IS1, L-262) |
| MDL minimizes description length | Compaction should preserve high-value signal, not just cut tokens | OBSERVED |
| Citation concentration (power-law tendency) | A small lesson subset carries most reusable value; ranking/retention should be quality-aware | OBSERVED |
| Precision/recall tradeoff | Spawn width is an operating point on coverage vs noise/cost curve (P-119 gate) | THEORIZED -> INSTRUMENTED (F-IS3) |

## Spawn presets (F-IS3, S186)
- **P0-no-spawn**: high coupling/overhead (`rho >= 0.3` and `coordination_cost >= 0.04`) -> `N=1`
- **P1-duo-spawn**: bounded-overhead default (`coordination_cost 0.02-0.05`) -> `N=2`
- **P2-broad-spawn**: low-coupling/low-overhead exploration (`rho <= 0.2`, `coordination_cost <= 0.02`) -> `N=3`

## What's open
- **F-IS3**: replace coordination-cost floor assumptions with measured per-agent overhead from live runs and auto-route trials to P0/P1/P2.
- **F-IS4**: rerun the scored protocol with independent domain-lane owners (not coordinator-synthesized) and compare collision/transfer stability.
- **F-IS5**: combine explicit transfer tags with a controlled overlap slice (plus owner-isolated backlog pass) so acceptance can be measured under realistic merge pressure.

## Information science links to core principles
P-152 (MDL compression) | P-119 (spawn discipline gate) | P-163 (rising-sawtooth compaction dynamics)
