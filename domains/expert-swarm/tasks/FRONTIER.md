# Expert Swarm Domain — Frontier Questions
Domain agent: write here for expert-swarm-specific questions; cross-domain findings go to tasks/FRONTIER.md
Updated: 2026-02-28 S304 | Active: 5

## Active

- **F-EXP1**: Does dispatch_optimizer.py score-ranked selection increase domain experiment throughput vs random dispatch? Baseline: 2% session throughput (S301). Design: measure actual domain selected per session for 10 sessions; compare to dispatch_optimizer.py top-5 recommendations. Instrument: `tools/dispatch_optimizer.py`. Cross-link: economy/F-ECO4.

- **F-EXP2**: Does companion expert bundling (idea-investigator + skeptic, per EXPERT-SWARM-STRUCTURE.md) reduce per-finding coordination overhead vs solo dispatch? Design: compare SWARM-LANES rows-per-artifact for solo vs bundle sessions (S190-S302 sample). Instrument: SWARM-LANES.md parse. Cross-link: operations-research.

- **F-EXP3**: What % of expert capacity (personality files × domain lanes) is utilized per session? Baseline: 44 personalities × 37 domains = ~1,628 capacity-slots; active DOMEX lanes ~75; utilization ~4.6%. Design: measure active dispatch coverage per session for 10 sessions. Instrument: maintenance.py domain-coverage check.

- **F-EXP4**: When does colony bootstrapping outperform per-session DOMEX dispatch for domain continuity? Design: compare meta/brain colonies (new COLONY.md pattern) vs equivalent non-colony domains on: time-to-artifact, frontier closure rate, lesson production per session. Instrument: `tools/swarm_colony.py status`. Cross-link: control-theory.

- **F-EXP6**: How do swarm colonies interact peer-to-peer? Baseline (S304): 81.1% of colonies have passive INDEX.md cross-links but 0% have active SIGNALS.md peer messages. Gap = passive awareness vs active signaling. Design: (1) build active signal protocol (SIGNALS.md per colony, implemented); (2) measure if active signals increase cross-colony lesson transfer rate vs passive-only baseline; (3) test if information-science ← control-theory pairing (top frontier overlap score=79) produces faster artifact by signaling findings. Instrument: `tools/colony_interact.py map/suggest/signal`. Cross-link: protocol-engineering, distributed-systems.

## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
| F-EXP5 | YES — annotation pass raised cite rate 3.4%→8.5% (2.5x), gap 13x→5x. ISO-14 added to atlas. 18 lessons annotated. | S303 | 2026-02-28 |
