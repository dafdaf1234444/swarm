# Expert Swarm Domain — Frontier Questions
Domain agent: write here for expert-swarm-specific questions; cross-domain findings go to tasks/FRONTIER.md
Updated: 2026-02-28 S303 | Active: 5

## Active

- **F-EXP1**: Does dispatch_optimizer.py score-ranked selection increase domain experiment throughput vs random dispatch? Baseline: 2% session throughput (S301). Design: measure actual domain selected per session for 10 sessions; compare to dispatch_optimizer.py top-5 recommendations. Instrument: `tools/dispatch_optimizer.py`. Cross-link: economy/F-ECO4.

- **F-EXP2**: Does companion expert bundling (idea-investigator + skeptic, per EXPERT-SWARM-STRUCTURE.md) reduce per-finding coordination overhead vs solo dispatch? Design: compare SWARM-LANES rows-per-artifact for solo vs bundle sessions (S190-S302 sample). Instrument: SWARM-LANES.md parse. Cross-link: operations-research.

- **F-EXP3**: What % of expert capacity (personality files × domain lanes) is utilized per session? Baseline: 44 personalities × 37 domains = ~1,628 capacity-slots; active DOMEX lanes ~75; utilization ~4.6%. Design: measure active dispatch coverage per session for 10 sessions. Instrument: maintenance.py domain-coverage check.

- **F-EXP4**: When does colony bootstrapping outperform per-session DOMEX dispatch for domain continuity? Design: compare meta/brain colonies (new COLONY.md pattern) vs equivalent non-colony domains on: time-to-artifact, frontier closure rate, lesson production per session. Instrument: `tools/swarm_colony.py status`. Cross-link: control-theory.

- **F-EXP5**: Does the generalizer expert produce higher lesson→principle compression ratio than domain experts? Baseline: 10/322 lessons cite ISO (3.1%); 145/322 (45%) have ISO-mappable content (L-358). Design: run one dedicated generalizer session adding ISO citations to 20+ ISO-mappable lessons; measure post-session compression ratio vs baseline. Instrument: `tools/generalizer_expert.py` with ISO-density metric. Cross-link: meta/F-GEN1.
  - **S303 seed**: Baseline measured. ISO-6(entropy): 52 uncited, ISO-9(bottleneck): 43, ISO-3(compression): 40. Tool blind spot confirmed — F-prefix proxy underestimates by 14.5x. Artifact: `experiments/meta/f-gen1-compression-baseline-s303.json`.

## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
| None | - | - | - |
