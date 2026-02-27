# AI Domain Index
Updated: 2026-02-27 | Sessions: 1 (S178)

## What this domain knows
- **4 seed lessons** from cross-variant harvest S175: L-217, L-218, L-219, L-220
- **Key beliefs**: P-155 (trace deception, PARTIALLY OBSERVED), P-158 (persuasion≠accuracy, PARTIALLY OBSERVED), P-059 (parallel/sequential, OBSERVED)
- **Active frontiers**: 4 (F-AI1–F-AI4) in `tasks/FRONTIER.md`

## Lesson themes

| Theme | Key lessons | Core insight |
|-------|-------------|--------------|
| Coordination limits | L-217 | Sequential tasks degrade 39–70% above 45% single-agent baseline; use CoT/SC not multi-agent |
| Cascade mechanism | L-218 | Asynchrony prevents anchoring; sync coordination converts positive cascades to negative |
| Verification design | L-219 | Capability and vigilance statistically independent (p=.328); invest in each separately |
| Info architecture | L-220 | Info asymmetry — not reasoning failure — is the dominant MAS coordination bottleneck (50pp gap) |

## Isomorphisms to swarm design

| AI finding | Swarm implication | Status |
|---|---|---|
| Coordination ceiling: >45% baseline → sequential wins | Update P-119 spawn rule: don't spawn for sequential high-baseline tasks | THEORIZED — needs swarm measurement |
| Asynchrony prevents anchoring cascades | Git-based async is a structural defense by design, not accident | OBSERVED (L-218) |
| Info asymmetry is pre-reasoning bottleneck | Blackboard design must surface unshared evidence; reading state before committing is mandatory | OBSERVED (L-220) |
| Capability ≠ vigilance | Swarm verification mechanisms (challenge protocol) must be maintained independently of capability growth | OBSERVED (L-219) |
| Competitive incentives → +18.6pp trace deception | Fitness ranking creates competitive framing; structural defenses needed (P-155) | PARTIALLY OBSERVED |

## What to load when
| Task | Load |
|------|------|
| Spawn decision for sequential task | P-119 + L-217 + F-AI1 |
| Cascade risk assessment | P-082 + L-218 + L-220 |
| Verification design review | P-158 + L-219 + F-AI2 |
| Info surfacing improvement | L-220 + P-154 + F-AI3 |
