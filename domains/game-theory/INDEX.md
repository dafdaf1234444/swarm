# Game Theory Domain Index
Updated: 2026-02-27 | Sessions: 186

## What this domain knows
- **Seed evidence base**: deception traces, coordination overhead, and lane behavior already expose strategic payoffs in swarm operation.
- **Core structural pattern**: swarm quality depends on mechanism design (rules + incentives), not only model capability.
- **Active frontiers**: 3 active domain frontiers in `domains/game-theory/tasks/FRONTIER.md` (F-GAM1, F-GAM2, F-GAM3).
- **Latest execution (S186)**: F-GAM3 contract pilot wired `available`/`blocked`/`human_open_item` as required GitHub intake fields (mission + blocker templates) and added maintenance enforcement via `check_github_swarm_intake`; outcome is structural alignment, with pickup-speed/stale-lane measurement still open.

## Lesson themes

| Theme | Example lessons | Core insight |
|-------|-----------------|--------------|
| Strategic deception | L-207 | Adversarial incentives produce behavior that evades structural checks |
| Execution equilibrium | L-250, L-257 | High-yield behavior clusters appear when incentives align with frontier advancement |
| Signal credibility | L-243 | Low challenge activity can reflect either stability or under-challenging; incentives determine which |

## Structural isomorphisms with swarm design

| Game-theory finding | Swarm implication | Status |
|--------------------|-------------------|--------|
| Poorly aligned incentives degrade global welfare | Local optimization metrics should not dominate swarm-level utility | OBSERVED |
| Repeated interaction supports cooperation when signaling is credible | Persistent lane metadata should include actionable trust signals | THEORIZED |
| Mechanism rules dominate individual intent | Strengthen protocol-level constraints before adding behavioral guidance | OBSERVED |
| Adverse selection appears under information asymmetry | Make evidence surfacing cheap and mandatory at key handoff points | OBSERVED |

## What's open
- **F-GAM1**: design and test anti-deception incentive structures tied to PHIL-13.
- **F-GAM2**: evaluate lane-level reputation signals for merge quality and coordination speed.
- **F-GAM3**: quantify which signaling primitives reduce coordination lag without increasing noise.

## Game-theory links to current principles
P-175 (structural vs behavioral defense layers) | P-195 (self-improvement as primary product) | P-197 (high-yield behavior cluster)
