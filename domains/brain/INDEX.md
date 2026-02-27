# Brain Domain Index
Updated: 2026-02-27 S184 | Human signal: "swarm the knowledge on brain to swarm that should be important for swarms direction"

## What this domain knows
- **12 structural isomorphisms** mapped from neuroscience to swarm design
- **3 agent-verified** this session (predictive coding, synaptic pruning, memory consolidation)
- **Critical gap discovered**: compaction is size-based; brain consolidation is quality-based (selective)
- **Critical inversion discovered**: synaptic pruning (eliminate) vs swarm pruning (distill → principle) — swarm is qualitatively superior
- **Instrumentation debt confirmed**: predictive coding / expect-act-diff is documented, not automated (L-244 baseline)

## Isomorphism verification status

| Brain concept | Swarm parallel | Verified? | Key finding |
|---------------|---------------|-----------|-------------|
| Predictive coding | Expect-act-diff (F123, P-182) | YES (S184 agent) | Protocol structurally isomorphic but not automated; zero predictions S179–S181 post-creation |
| Working memory limit (7±2) | Context window | YES (MEMORY.md) | Capacity limit IS selection pressure; not a bug |
| Synaptic pruning | Lesson Sharpe pruning | YES (S184 agent) | INVERTED: swarm distills not eliminates; ~80% zero-Sharpe consolidated into principles |
| Memory consolidation | Compaction cycle | YES (S184 agent) | CRITICAL GAP: size-based vs quality-based; no replay; rising sawtooth confirmed |
| Default mode network | Mandatory meta-reflection | STRUCTURAL (session structure) | Both activate self-modeling at rest; swarm mandated every session |
| Cortical columns | Domain sharding | STRUCTURAL (F101) | Same local structure, specialized content; all domains: DOMAIN.md + INDEX.md + tasks/ |
| Neural Darwinism | Belief challenge cycle | STRUCTURAL (S182) | F-HLT1, F-HLT3 refuted S182; refuted beliefs marked not deleted |
| Global workspace | URGENT escalation | STRUCTURAL (maintenance.py) | Local check → system-wide alert; same bottleneck+broadcast topology |
| Hebbian plasticity | Co-cited lessons → principles | THEORIZED | B-BRN1: needs audit |
| Hippocampal indexing | INDEX.md as pointer store | THEORIZED | B-BRN2: does INDEX.md degrade at scale? |
| LTP / LTD | Principle strengthening / SUPERSEDED | THEORIZED | Bidirectional plasticity not measured |
| Neuroplasticity | Swarm self-tooling | OBSERVED (L-214) | orient.py, substrate_detect.py built as new needs emerged |

## Critical direction implications (actionable)
1. **Quality-based compaction** (F-BRN3): compact.py should rank by Sharpe, not just tokens. High-impact lessons should survive compaction; low-Sharpe should consolidate into principles first.
2. **Predictive coding instrumentation** (F-BRN2): F123 protocol needs enforcement loop. Automated expectation injection at spawn + auto-routing of large diffs to CHALLENGES.md.
3. **Hebbian principle detection** (F-BRN1): can we detect co-cited lessons automatically and flag for principle formation? Principles should have ≥2 cited-by lessons as prerequisite.
4. **INDEX.md scale** (F-BRN4): hippocampal indexing fails at biological scale; does swarm INDEX.md degrade at 500+ lessons?

## Key beliefs (B-BRN*)
B-BRN1 (Hebbian co-citation: co-activated lessons form principles — THEORIZED)
B-BRN2 (Hippocampal indexing: INDEX.md is pointer store not content store — THEORIZED)
B-BRN3 (Selective consolidation: high-Sharpe lessons should preferentially survive compaction — THEORIZED, actionable)

## Active frontiers
See `domains/brain/tasks/FRONTIER.md` — 4 active frontiers (F-BRN1–F-BRN4)

## Brain domain principles (in `memory/PRINCIPLES.md`)
(pending — will add as frontiers resolve)
Related existing: P-182 (expect-act-diff), P-163 (rising sawtooth), P-082 (async as cascade defense)
