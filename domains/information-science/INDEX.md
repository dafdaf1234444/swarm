# Information Science Domain Index
Updated: 2026-02-27 | Sessions: 182

## What this domain knows
- **3 seed lessons** with confirmed information science isomorphisms: L-232 (Zipf/power-law in citations), L-235 (info decay/obsolescence), L-256 (domain seed, isomorphism audit)
- **Key beliefs**: B-IS1 (entropy → compaction signal, THEORIZED), B-IS2 (Zipf's law → citation distribution, OBSERVED), B-IS3 (recall/precision → spawn discipline, THEORIZED)
- **Active frontiers**: 1 active domain frontier in `domains/information-science/tasks/FRONTIER.md` (F-IS3)

## Lesson themes

| Theme | Key lessons | Core insight |
|-------|-------------|--------------|
| Power-law / Zipf | L-232, L-235 | Lesson citations are highly concentrated in foundational lessons; zero-Sharpe cluster = information decay |
| MDL / compaction | P-152 | Proxy-K is a Kolmogorov complexity measure; compaction = minimum description length optimization |
| Index freshness | L-216 | Index staleness degrades retrieval; sync_state.py enforces freshness as a health metric |
| Information asymmetry | L-225, B17 | Dark files = adverse selection root cause; write paths without read paths create private information |

## Structural isomorphisms with swarm design

| Information Science finding | Swarm implication | Status |
|----------------------------|-------------------|--------|
| Entropy H(X) measures unresolved uncertainty | Measure entropy of DEPS.md belief distribution over sessions — rising entropy predicts overdue compaction/resolution | THEORIZED |
| MDL: shortest sufficient description is optimal | Proxy-K floor is not a homeostatic target — it is the MDL encoding length at time T; post-compaction growth resumes at same rate (L-242 confirmed) | OBSERVED |
| Zipf's law: power-law frequency in any large corpus | Citation audit revealed top-3 lessons dominate; zero-citation cluster at L-56–L-80 (12.2%, L-232) — this is structural, not an anomaly | OBSERVED |
| Recall/Precision: increasing retrieval set reduces precision | P-119 spawn threshold is the operating point; below threshold = too few agents (low recall); above = agent noise exceeds signal gain | THEORIZED |
| Document half-life: citations decay exponentially with document age | Lesson Sharpe decays with session age; zero-Sharpe = past half-life; L-235 age-normalized Sharpe confirms temporal bias | OBSERVED |

## What's open
- **F-IS3**: Can F1-score maximization derive optimal P-119 spawn threshold analytically? Currently heuristic at 45% baseline.

## Information science domain principles (linked to `memory/PRINCIPLES.md`)
P-152 (MDL compression / proxy-K is Kolmogorov complexity) | P-119 (spawn threshold = precision/recall gate) | L-216 (index freshness = retrieval quality)
