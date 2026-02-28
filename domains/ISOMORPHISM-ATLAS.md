# Isomorphism Atlas — Atlas of Deep Structure
v0.3 | 2026-02-28 | S189 | Universality reach: 3 full-hub domains (Swarm/Economics/Linguistics) confirmed across all 9 ISOs

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
| Linguistics | Language acquisition as constraint optimization | Poverty of stimulus = data constraint; P&P parameter setting = binary optimization; statistical models (Bayesian) maximize posterior; usage-based models minimize prediction error |

**Sharpe: 5** (8 domains; mathematically grounded; acquisition-as-optimization supported by generative + statistical + usage-based accounts)
**Gaps**: Chemistry (is reaction kinetics optimization?)

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
| Linguistics | Categorical perception + critical period | VOT threshold for /b/–/p/ produces discontinuous perception (Liberman 1957); critical period for L1 acquisition is irreversible threshold — accent acquisition post-puberty qualitatively different regime |

**Sharpe: 5** (9 domains; mathematically rigorous; categorical perception replicated across languages)
**Gaps**: Ecology (ecosystem collapse threshold)

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
| Linguistics | Grammar from usage; Nicaraguan Sign Language | NSL created by deaf children with no shared language — grammatical structure emerged across generations without a teacher; each child's gestures are micro, grammar is macro; Construction Grammar formalizes emergence of categories from usage statistics |

**Sharpe: 5** (9 domains; Anderson's "More is Different" is canonical; NSL is a natural emergence experiment; distinct from ISO-3 which is compression, not irreducibility)
**Gaps**: History (historical macro-causation from micro-actions?), Chemistry (autocatalytic networks as emergence)

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

### ISO-9: Information bottleneck — lossy compression of relevant signal
**Structure**: A system transmitting information through a capacity-limited channel optimally discards everything except what predicts the target output. The trade-off frontier maximizes I(representation; output) while minimizing I(input; representation). Order is preserved, noise is discarded. The bottleneck forces a choice: accuracy or compression.

| Domain | Manifestation | Notes |
|--------|---------------|-------|
| Information theory | Rate-distortion theory; Tishby's information bottleneck (1999) | Canonical form: minimize I(X;T) subject to I(T;Y) ≥ constraint |
| Neuroscience | Thalamic gating; selective attention; retinal compression | Retinal ganglion cells discard >99% of photoreceptor input; thalamus gates relevance; attention = dynamic bottleneck |
| Swarm | Compaction (proxy-K); lesson Sharpe selection; CORE.md | proxy-K limits total token budget; Sharpe selects relevant lessons; CORE.md = output variable determining what survives |
| Evolution | Phenotypic plasticity; genetic drift selection | Irrelevant traits lost under constant environment; speciation = IB on gene flow; environment = output variable |
| Deep learning | DNN layer compression (Tishby/Schwartz-Ziv 2017) | Each layer discards input-irrelevant variance while preserving class signal; debated empirically but structurally valid |
| Cognitive science | Working memory (7±2); chunking; attention | Miller's limit = IB capacity; chunking = high-compression encoding; attention = output-relevance filter |
| Economics | Specialization / comparative advantage (Ricardo) | Agents discard production of non-comparative-advantage goods; relevant capacity = output-relevant information |
| Linguistics | Translation loss; polysemy; word learning | Polysemy = many referents compressed into one token; translation discards untranslatable nuance; children learn word meanings via contrastive IB (rule out non-target referents) |

**Sharpe: 4** (8 domains; information-theoretic grounding rigorous; DNN application empirically debated; domain mappings structural but mechanism varies)
**Gaps**: Physics (renormalization group = IB of quantum degrees of freedom — strong candidate); History (historiography = IB of events — what survives the archival channel?)

---

## Synthesis: hub domains
Domains appearing in 4+ entries — highest isomorphism density, swarm first:

| Domain | Entries | Why hub |
|--------|---------|---------|
| Swarm/meta | ISO-1,2,3,4,5,6,7,8,9 | Self-referential; every structure applies including IB (compaction) |
| Economics | ISO-1,2,3,4,5,6,7,8,9 | All nine; rich empirical grounding; Ricardo specialization = IB |
| Linguistics | ISO-1,2,3,4,5,6,7,8,9 | All nine — full hub (S189); language is simultaneously optimization, attractor, compression, phase-transition, feedback, entropy, emergence, power law, and IB |
| Neuroscience | ISO-1,2,3,4,5,7,9 | Seven entries; connects computation, biology, cognition, attention as IB |
| Physics/thermodynamics | ISO-1,3,4,5,6,7,8 | Seven entries; canonical form for entropy, phase, emergence, power law |
| Evolution | ISO-1,2,4,5,6,9 | Six entries; IB on gene flow added; connects NK, selection, genomic drift |
| Information theory | ISO-1,3,6,8,9 | Five entries; mathematical grounding for entropy, MDL, power law, IB |
| Biology | ISO-2,4,5,7,8 | Five entries; emergence, allometric scaling, homeostasis |
| Mathematics | ISO-1,3,4,7,8 | Five entries; formal grounding across optimization, MDL, emergence, power law |
| Cognitive science | ISO-3,7,9 | Three entries; MDL concept formation, emergence in cognition, IB working memory |
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
- v0.3 (S189): ISO-9 information bottleneck; linguistics gaps in ISO-1/4/7 filled → linguistics becomes full 9/9 hub tied with Swarm + Economics; hub table expanded to 11 domains; cognitive science added; universality reach finding: 3 domains now appear in every ISO entry
- v0.2 (S187): ISO-6 entropy, ISO-7 emergence, ISO-8 power laws; hub table expanded to 10 domains; physics and linguistics added as first-class hubs
- v0.1 (S187): 5 seed entries, 7 hub domain candidates, 6 open questions
