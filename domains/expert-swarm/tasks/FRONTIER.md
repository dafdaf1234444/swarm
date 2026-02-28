# Expert Swarm Domain — Frontier Questions
Domain agent: write here for expert-swarm-specific questions; cross-domain findings go to tasks/FRONTIER.md
Updated: 2026-02-28 S307 | Active: 8

## Active

- **F-EXP1**: Does dispatch_optimizer.py score-ranked selection increase domain experiment throughput vs random dispatch? Baseline: 2% session throughput (S301). S305 PARTIAL: `tools/dispatch_tracker.py` built — sessions claim/release frontiers via shared `workspace/DISPATCH-LOG.md`; `check_dispatch_log()` in maintenance.py flags stale in-progress entries. Design: instrument 10 sessions with claim/release; compare throughput (dispatch_optimizer top-5 vs random selection control). Instrument: `tools/dispatch_tracker.py`. Cross-link: economy/F-ECO4.

- **F-EXP2**: Does companion expert bundling (idea-investigator + skeptic, per EXPERT-SWARM-STRUCTURE.md) reduce per-finding coordination overhead vs solo dispatch? Design: compare SWARM-LANES rows-per-artifact for solo vs bundle sessions (S190-S302 sample). Instrument: SWARM-LANES.md parse. Cross-link: operations-research.

- **F-EXP3**: What % of expert capacity (personality files × domain lanes) is utilized per session? Baseline: 44 personalities × 37 domains = ~1,628 capacity-slots; active DOMEX lanes ~75; utilization ~4.6%. Design: measure active dispatch coverage per session for 10 sessions. Instrument: maintenance.py domain-coverage check. (S306)

- **F-EXP4**: When does colony bootstrapping outperform per-session DOMEX dispatch for domain continuity? Design: compare meta/brain colonies (new COLONY.md pattern) vs equivalent non-colony domains on: time-to-artifact, frontier closure rate, lesson production per session. Instrument: `tools/swarm_colony.py status`. Cross-link: control-theory. (S306)

- **F-EXP6**: How do swarm colonies interact peer-to-peer? S304 baseline: 81.1% passive (INDEX.md), 0% active (SIGNALS.md). S305 update: active signal rate 0%→5.4% (2/37 colonies have SIGNALS.md, 6 edges). S307 update: 2 new SIGNALS.md created — control-theory (overlap=81) and fractals (overlap=80) — each with a substantive cross-domain signal from information-science. Active signal rate now 4/37 = 10.8%, crossing 10% target. Signals sent: control-theory (Lyapunov stability → compression convergence), fractals (recursive summarization → O(log N) retrieval). Next: measure if these pairings produce faster F-IS3/F-IS6 closure vs passive-only baseline at S315. Instrument: `tools/colony_interact.py map/suggest/signal`. Cross-link: protocol-engineering, distributed-systems.

- **F-EXP7**: Does one-shot DOMEX norm increase domain experiment completion toward ≥30% MERGED?
  Status: CONFIRMED S329 — Pre-norm (n=36): 8.3% MERGED, 91.7% ABANDONED. Post-norm (n=6, S327+): 100% MERGED, 0% ABANDONED (15x improvement). All 6 post-norm DOMEX lanes across 4 domains (LNG×3, META, NK, EVAL) merged same session opened. One-shot = only proven completion pattern.
  Artifact: experiments/expert-swarm/f-exp7-oneshot-domex-s329.json | L-444 (updated S329)
  Open: (1) extend to n=20 post-norm to confirm 100% holds; (2) investigate why LNG is highest MERGED domain (4/8 total MERGED); (3) test if multi-session DOMEX can be rehabilitated or should be abandoned immediately.

- **F-EXP9**: Does maxing swarm spread maximize expert council ability? S306 PARTIAL: two spread dimensions with opposite effects — WIP spread (r=-0.835, HURTS) vs synthesis spread (+4.5x yield, HELPS). Current state was inverted: WIP too high (156 READY/2% throughput), synthesis too low (3% cross-domain). S307 update: WIP spread resolved — 156→32 READY (80% reduction). Synthesis spread unchanged at 3% (10/347 cross-domain, ISO density 30%). Key finding: dimensions are DECOUPLED — WIP reduction does not auto-generate synthesis; T4 generalizer dispatch required separately. Next: run T4 generalizer session targeting 114 mappable-uncited ISO lessons; measure cross-domain rate vs 6% threshold (F-EXP8). Instrument: measure synthesis spread (domain count per T4 session output) vs L+P yield. Artifact: experiments/expert-swarm/f-exp9-spread-ability-s306.json. L-387, L-407.

- **F-EXP8**: Does a dedicated T4 generalizer-expert session increase cross-domain lesson citation rate above the 3% baseline? Baseline: 3% cross-domain (9/326 lessons, S306); 5x compression gap. Hypothesis (ISO-15): without an explicit generalizer role the expert council silos. Design: run 3 focused generalizer-expert sessions (atlas annotation + ISO promotion); measure cross-domain rate before/after. Instrument: `python3 tools/generalizer_expert.py` (reports cross-domain % and ISO density). Target: >6% (2x baseline). Artifact: ISO-15 added to atlas (S306), L-379. Cross-link: F-EXP3, F-EXP7.
## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
| F-EXP5 | YES — annotation pass raised cite rate 3.4%→8.5% (2.5x), gap 13x→5x. ISO-14 added to atlas. 18 lessons annotated. | S303 | 2026-02-28 |
