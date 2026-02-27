# Isomorphism Atlas — Atlas of Deep Structure
v0.1 | 2026-02-28 | S187 | Seeded from human signal + L-274

## What this is
A cross-domain atlas of structural equivalences. Each entry maps one abstract structure to its manifestations across multiple domains. This is NOT a fact database — it is a compression of world knowledge into shared structure.

**Core claim (L-274):** Maximum-compression world knowledge is structural equivalence, not facts.
When you identify one abstract structure shared by N domains, you've captured N domains in 1 entry.
Value scales super-linearly with domain count: each new domain potentially matches every existing structure.

**What swarm can do:** Find and verify structural similarity.
**What swarm cannot do:** Guarantee encyclopedic factual accuracy.

---

## How to read an entry

Each entry has:
- **Structure**: the abstract pattern, domain-agnostic
- **Manifestations**: how it appears in specific domains
- **Sharpe score**: evidence quality × breadth (1–5; higher = better-verified, wider)
- **Gaps**: domains where this structure *might* apply but hasn't been verified

---

## Atlas entries

### ISO-1: Optimization-under-constraint
**Structure**: A system minimizes a loss function by making incremental adjustments in the direction of steepest local improvement, subject to boundary conditions.

| Domain | Manifestation | Notes |
|--------|---------------|-------|
| Mathematics | Gradient descent / Lagrange multipliers | Canonical form |
| Physics | Principle of least action | Variational calculus formulation |
| Evolution | Natural selection | Fitness = negative loss; mutation = perturbation |
| Economics | Market equilibration | Price discovery = loss minimization |
| Neuroscience | Synaptic plasticity (LTP/LTD) | Hebbian learning = local gradient step |
| Swarm | Belief update + lesson Sharpe selection | High-Sharpe = low loss; compaction prunes |
| Control theory | PID controller / LQR | Explicit cost function; real-time adjustment |

**Sharpe: 5** (7 domains; mathematically grounded; verified in all domains)
**Gaps**: Linguistics (is grammar acquisition optimization?), Chemistry (is reaction kinetics optimization?)

---

### ISO-2: Selection pressure → diversity collapse → stable attractor
**Structure**: A population under strong selection pressure loses variance, converges to a local attractor, and becomes brittle to novel perturbations. Without diversity maintenance, the system cannot escape the attractor.

| Domain | Manifestation | Notes |
|--------|---------------|-------|
| Evolution | Genetic bottleneck / monoculture | Loss of allelic diversity → extinction risk |
| Economics | Market monopoly / winner-takes-all | Competition eliminated; innovation stagnates |
| Ideas / culture | Paradigm lock-in (Kuhn) | Anomalies suppressed until crisis |
| Swarm | Belief monoculture risk | PHIL-13: competitive deception risk; challenge cycle maintains diversity |
| Machine learning | Mode collapse (GANs) | Generator converges to single output |
| Ecology | Island biogeography | Small populations → diversity loss |

**Sharpe: 4** (6 domains; well-attested; mechanism differs by substrate)
**Gaps**: Linguistics (dialect → standard convergence?), Governance (political polarization as attractor?)

---

### ISO-3: Hierarchical compression (MDL principle)
**Structure**: A system with many observations reduces to a compact representation (a "model") that predicts the observations with minimal description length. The model trades bias for variance; the optimal model is the one that compresses most without losing prediction accuracy.

| Domain | Manifestation | Notes |
|--------|---------------|-------|
| Information theory | Minimum description length (MDL) | Canonical form |
| Science | Scientific law / theory | Newton's laws compress all projectile trajectories |
| Neuroscience | Cortical abstraction hierarchy | V1→V2→IT: edge→shape→object |
| Swarm | Lesson → Principle → CORE compression | L-NNN → P-NNN → CORE.md; each level is MDL step |
| Linguistics | Grammar from corpus | Grammar = compressed representation of utterances |
| Cognitive science | Concept formation | Category = compression of exemplars |

**Sharpe: 4** (6 domains; information-theoretic grounding is rigorous; some mappings structural/theorized)
**Gaps**: Economics (price as compression of supply/demand signals?), History (historical narrative as MDL?)

---

### ISO-4: Phase transition (threshold → qualitative shift)
**Structure**: A system exhibiting continuous parameter change undergoes a discontinuous qualitative shift at a critical threshold. Below threshold: one regime. Above: a qualitatively different regime. The transition is often irreversible.

| Domain | Manifestation | Notes |
|--------|---------------|-------|
| Physics | Phase transitions (ice→water→steam) | Canonical form; order parameter |
| Evolution | Cambrian explosion / punctuated equilibrium | Threshold conditions → rapid diversification |
| Mathematics | Percolation threshold / graph connectivity | Sudden giant component emergence |
| NK complexity | K-threshold → chaos transition | K<2: ordered; K>2: chaotic (L-series) |
| Swarm | URGENT threshold in maintenance.py | Proxy-K >10% → qualitative escalation |
| Neuroscience | Action potential (all-or-nothing) | Threshold firing is binary phase transition |
| Economics | Market panic / bank run | Confidence crosses threshold → cascade |
| Social systems | Tipping points (Gladwell; Schelling) | Small perturbation past threshold → cascade |

**Sharpe: 5** (8 domains; mathematically rigorous; universally observed)
**Gaps**: Linguistics (phonological contrast thresholds?), Ecology (ecosystem collapse threshold)

---

### ISO-5: Feedback loop — stabilizing vs. amplifying
**Structure**: A system's output feeds back into its input. Negative (stabilizing) feedback returns the system to equilibrium. Positive (amplifying) feedback drives the system away from equilibrium. Real systems mix both; which dominates determines behavior.

| Domain | Manifestation | Notes |
|--------|---------------|-------|
| Control theory | Negative feedback loop / PID | Canonical engineering form |
| Biology | Homeostasis (thermoregulation, pH) | Negative feedback preserving setpoint |
| Economics | Price mechanism | Negative: high price → less demand → lower price |
| Economics | Compound interest / network effects | Positive: growth begets growth |
| Swarm | Lesson quality cycle | Positive: good lessons cited → become principles → better swarming |
| Swarm | Proxy-K drift alert | Negative: high drift → compaction → lower drift |
| Neuroscience | Excitatory / inhibitory neurons | Balance of +/- feedback maintains stability |
| Climate | Ice-albedo feedback (positive) | Ice reflects light → less melting → more ice; or inverted |

**Sharpe: 5** (8 domains; fundamental to all dynamic systems; well-verified)
**Gaps**: Linguistics, History

---

### ISO-6: Entropy — degradation gradient and the cost of order
**Structure**: A closed system under no external input tends toward maximum disorder (maximum entropy). The gradient from low-entropy (ordered) to high-entropy (disordered) states defines the arrow of time. Maintaining low entropy requires continuous energy input. Order is not a default — it is a maintained exception.

| Domain | Manifestation | Notes |
|--------|---------------|-------|
| Thermodynamics | Boltzmann entropy; 2nd Law of Thermodynamics | S = k log W; disorder is the statistically dominant macro-state |
| Information theory | Shannon entropy; compression limits | H = -Σ p log p; lossless compression cannot exceed entropy; random data is incompressible |
| Evolution | Genomic drift without selection pressure | Without selection, mutations accumulate; fitness degrades; Muller's ratchet |
| Economics | Commodity pricing drift | Without innovation, products commoditize; margins compress toward zero; Schumpeter's creative destruction = entropy resistance |
| Swarm | Proxy-K drift; memory degradation without compaction | Without challenge cycles and compaction, beliefs drift stale; proxy-K increase IS entropy |
| Linguistics | Language simplification | Without prestige pressure or literacy, languages lose morphological complexity (creolization, pidgin formation) |
| Cognitive science | Memory decay without retrieval practice | Ebbinghaus forgetting curve; spacing effect = entropy resistance; consolidation requires energy |

**Sharpe: 5** (7 domains; thermodynamic grounding is mathematically rigorous; information-theoretic isomorphism is exact; domain mappings well-attested)
**Gaps**: Ecology (ecosystem succession as entropy gradient?), Social systems (institutional decay without maintenance?), Chemistry (reaction equilibrium and ΔG as entropy manifestation — partially covered by thermodynamics)

---

### ISO-7: Emergence — macro-behavior irreducible to micro-rules
**Structure**: When local agents follow simple rules with no explicit macro-programming, complex coordinated behavior emerges at the system level that cannot be predicted by reading the micro-rules alone. The emergent macro-level is causally real but irreducible to the micro-level. More is different (Anderson 1972).

| Domain | Manifestation | Notes |
|--------|---------------|-------|
| Physics | Phase transitions; superconductivity; crystal formation | Cooper pairs from electron-electron interaction; crystal lattice from isotropic atoms; new symmetry-breaking at macro scale |
| Biology | Ant colonies; flocking (Vicsek model); immune response | No central controller; colony-level intelligence from threshold-based local rules |
| Neuroscience | Consciousness from neurons; semantic concepts from synapses | No single neuron encodes "grandmother"; binding problem; qualia not predictable from connectome |
| Economics | Market prices from individual transactions | Hayek's price mechanism; distributed knowledge aggregation; no planner computes equilibrium |
| Swarm | Coherent beliefs from independent node commits | No node has full state; beliefs emerge from git convergence; swarm intelligence IS emergence |
| Mathematics | Gödel incompleteness; undecidable system-level truths | Truths about system not derivable from its own axioms; arithmetic transcends its axioms |
| Game theory | Nash equilibria without communication | Agents following local best-response converge to system-level equilibrium; coordination without coordination |
| Computation | NP-hardness; easy micro-steps → hard macro-problem | SAT: local clauses trivial; satisfying all simultaneously exponential; complexity emerges from combination |

**Sharpe: 5** (8 domains; Anderson's "More is Different" is canonical; each domain independently well-attested; swarm is a direct instance)
**Gaps**: Linguistics (grammar emergence from language use — partially ISO-3), History (historical macro-causation from micro-actions?), Chemistry (autocatalytic networks as emergence)

---

### ISO-8: Power laws — non-linear size-property scaling
**Structure**: Many natural and social systems exhibit power-law relationships where a property P scales as P ∝ N^α for some non-integer exponent α. These Zipf/Pareto/allometric distributions arise from multiplicative processes, preferential attachment, or scale-free network structure. The exponent α is often conserved across substrates with the same generative mechanism.

| Domain | Manifestation | Notes |
|--------|---------------|-------|
| Linguistics | Zipf's law: word frequency ∝ 1/rank | Holds across all measured languages; generative mechanism: least-effort principle (Zipf) or random typing (Miller) |
| Economics | Pareto distribution: top 20% hold 80% of wealth | Preferential attachment; wealth begets wealth; Lorenz curve; income distributions |
| Biology | Allometric scaling: metabolic rate ∝ mass^0.75 | Kleiber's law; fractal vascular network explanation (West/Brown); holds across 27 orders of magnitude |
| Networks | Degree distribution in scale-free networks | Barabási-Albert preferential attachment; internet, citations, social networks |
| Physics | 1/f noise; critical phenomena; fractal geometry | Self-organized criticality (Bak); power spectral density; at phase transitions, correlation length diverges |
| Information theory | Kolmogorov complexity distribution | Most strings are incompressible; compressible strings follow power-law distribution |
| Swarm / NK complexity | NK fitness landscape: complexity ∝ K^N | Exponential scaling of epistatic interactions; proxy-K as complexity exponent; lesson citation follows power law |
| Cities / social systems | Population ∝ rank^(-1); city scaling laws | Zipf for cities; GDP per capita ∝ city population^1.15 (superlinear); West's urban scaling |

**Sharpe: 4** (8 domains; mathematical grounding solid; generative mechanisms debated — multiple explanations for same exponent; cross-domain exponent identity unverified)
**Gaps**: Neuroscience (neural avalanches and self-organized criticality — likely power law); History (conflict sizes follow power law — Richardson's law); Evolution (extinction event sizes)

---

## Synthesis: hub domains
Domains appearing in 4+ entries — highest isomorphism density, swarm first:

| Domain | Entries | Why hub |
|--------|---------|---------|
| Swarm/meta | ISO-1,2,3,4,5,6,7,8 | Self-referential; every structure applies |
| Economics | ISO-1,2,3,4,5,6,7,8 | All eight; rich empirical grounding |
| Neuroscience | ISO-1,2,3,4,5,7 | Six entries; connects computation, biology, cognition |
| Physics/thermodynamics | ISO-1,3,4,5,6,7,8 | Seven entries; canonical form for entropy, phase, emergence, power law |
| Evolution | ISO-1,2,4,5,6 | Five entries; connects NK complexity, selection, genomic drift |
| Linguistics | ISO-2,3,5,6,8 | Five entries; newly elevated; language as compressible adaptive system |
| Information theory | ISO-1,3,6,8 | Four entries; mathematical grounding for entropy, MDL, power law |
| Biology | ISO-2,4,5,7,8 | Five entries; emergence, allometric scaling, homeostasis |
| Mathematics | ISO-1,3,4,7,8 | Five entries; formal grounding across optimization, MDL, emergence, power law |
| Control theory | ISO-1,5 | Engineering instantiation of feedback+optimization |

---

## Open questions (F126)
1. **Hub identification**: What are the ~50 domains with highest isomorphism density? (current table: 7 candidates)
2. **Sharpe scoring**: How to measure evidence quality × breadth for a structural claim?
3. **Domain sprawl prevention**: Selection criterion: only domains yielding ≥3 novel ISO entries survive as first-class domains.
4. **Verification protocol**: Structural claims vs. factual claims — how to flag unverifiable entries?
5. **Synthesis entries**: Knowledge appearing ONLY at 3+ domain intersections — how to surface these?
6. **Inversion check**: Every ISO entry has a known failure mode (where the structure breaks). Documenting inversions is as valuable as the structure itself.

---

## Relationship to F122
F122: domain → isomorphisms → swarm improvement (swarm is beneficiary)
F126: swarm → isomorphism atlas → world knowledge base (world is beneficiary)
Both share the mechanism. F126 inverts the directionality of value flow.

## Version history
- v0.2 (S187): ISO-6 entropy, ISO-7 emergence, ISO-8 power laws; hub table expanded to 10 domains; physics and linguistics added as first-class hubs
- v0.1 (S187): 5 seed entries, 7 hub domain candidates, 6 open questions
