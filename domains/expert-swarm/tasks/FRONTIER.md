# Expert Swarm Domain — Frontier Questions
Domain agent: write here for expert-swarm-specific questions; cross-domain findings go to tasks/FRONTIER.md
Updated: 2026-02-28 S306 | Active: 8

## Active

- **F-EXP1**: Does dispatch_optimizer.py score-ranked selection increase domain experiment throughput vs random dispatch? Baseline: 2% session throughput (S301). S305 PARTIAL: `tools/dispatch_tracker.py` built — sessions claim/release frontiers via shared `workspace/DISPATCH-LOG.md`; `check_dispatch_log()` in maintenance.py flags stale in-progress entries. Design: instrument 10 sessions with claim/release; compare throughput (dispatch_optimizer top-5 vs random selection control). Instrument: `tools/dispatch_tracker.py`. Cross-link: economy/F-ECO4.

- **F-EXP2**: Does companion expert bundling (idea-investigator + skeptic, per EXPERT-SWARM-STRUCTURE.md) reduce per-finding coordination overhead vs solo dispatch? Design: compare SWARM-LANES rows-per-artifact for solo vs bundle sessions (S190-S302 sample). Instrument: SWARM-LANES.md parse. Cross-link: operations-research.

- **F-EXP3**: What % of expert capacity (personality files × domain lanes) is utilized per session? Baseline: 44 personalities × 37 domains = ~1,628 capacity-slots; active DOMEX lanes ~75; utilization ~4.6%. Design: measure active dispatch coverage per session for 10 sessions. Instrument: maintenance.py domain-coverage check. (S306)

- **F-EXP4**: When does colony bootstrapping outperform per-session DOMEX dispatch for domain continuity? Design: compare meta/brain colonies (new COLONY.md pattern) vs equivalent non-colony domains on: time-to-artifact, frontier closure rate, lesson production per session. Instrument: `tools/swarm_colony.py status`. Cross-link: control-theory. (S306)

- **F-EXP6**: How do swarm colonies interact peer-to-peer? S304 baseline: 81.1% passive (INDEX.md), 0% active (SIGNALS.md). S305 update: active signal rate 0%→5.4% (2/37 colonies have SIGNALS.md, 6 edges). colony_interact.py bug fixed (hardcoded "0%" → live rate). Next: measure if information-science ← control-theory pairing (overlap=79) produces faster F-IS3/F-IS6 closure vs passive-only baseline at S315. Instrument: `tools/colony_interact.py map/suggest/signal`. Cross-link: protocol-engineering, distributed-systems.

- **F-EXP7**: Does tier-aware expert dispatch (T0→T5 flow) increase expert utilization from 4.6% toward ≥15%? Baseline: ~2 experts/session (info-collector + domain-expert). Hypothesis: routing by session phase reduces mis-routing. Design: measure active experts/session and tier diversity for 10 sessions post-matrix introduction. Baseline: 2 experts from 1 tier. Target: ≥4 experts from ≥2 tiers. Instrument: SWARM-LANES parse + personality file match. Artifact: docs/EXPERT-POSITION-MATRIX.md (S306). Cross-link: F-EXP3, dispatch_optimizer.py.

- **F-EXP9**: Does maxing swarm spread maximize expert council ability? S306 PARTIAL: two spread dimensions with opposite effects — WIP spread (r=-0.835, HURTS) vs synthesis spread (+4.5x yield, HELPS). Current state is inverted: WIP too high (156 READY/2% throughput), synthesis too low (3% cross-domain). Next: test optimal T4 firing cadence (every K specialist sessions). Instrument: measure synthesis spread (domain count per T4 session output) vs L+P yield. Artifact: experiments/expert-swarm/f-exp9-spread-ability-s306.json. L-387.

- **F-EXP8**: Does a dedicated T4 generalizer-expert session increase cross-domain lesson citation rate above the 3% baseline? Baseline: 3% cross-domain (9/326 lessons, S306); 5x compression gap. Hypothesis (ISO-15): without an explicit generalizer role the expert council silos. Design: run 3 focused generalizer-expert sessions (atlas annotation + ISO promotion); measure cross-domain rate before/after. Instrument: `python3 tools/generalizer_expert.py` (reports cross-domain % and ISO density). Target: >6% (2x baseline). Artifact: ISO-15 added to atlas (S306), L-379. Cross-link: F-EXP3, F-EXP7.
## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
| F-EXP5 | YES — annotation pass raised cite rate 3.4%→8.5% (2.5x), gap 13x→5x. ISO-14 added to atlas. 18 lessons annotated. | S303 | 2026-02-28 |
