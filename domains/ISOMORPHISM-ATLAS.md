# Isomorphism Atlas — Atlas of Deep Structure
v1.0 | 2026-02-28 | S329 | ISO-17 (self-model coherence gap: identity vs evidence asymmetry) + hub citation analysis (390 lessons: ISO-3=86, ISO-6=69, ISO-4=43 — top-3 hubs)

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
| Governance | Political polarization as attractor | Two-party systems: selection pressure from winner-takes-all elections; moderate positions eliminated; system locked into two attractors (red/blue) with mutual-reinforcing identity cycles |

**Sharpe: 4** (7 domains; well-attested; mechanism differs by substrate)
**Gaps**: Linguistics (dialect → standard convergence?)

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

| Ecology | Ecosystem succession / degradation without energy input | Without photosynthesis + nutrient cycling, complex climax communities degrade to pioneer species; fire, drought, fragmentation accelerate entropy; restoration = active entropy resistance requiring continuous external energy |
| Social systems | Institutional decay | Organizations without active governance degrade: rules become loopholes, norms erode, coordination fails; maintenance overhead is the entropy tax; "bureaucratic sclerosis" (Mancur Olson) = institutional entropy maximization |

**Sharpe: 5** (9 domains; thermodynamic grounding is mathematically rigorous; information-theoretic isomorphism is exact; ecology and social-systems cases well-attested in literature)
**Gaps**: Chemistry (reaction equilibrium and ΔG as entropy manifestation — partially covered by thermodynamics)

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
| Swarm (measured S306) | Cumulative L ~ session^alpha; alpha cycles with structural innovations | Pre-burst (S1-S180): alpha=1.712 (super-linear, city-like); post-burst (S180-S306): alpha=0.913 (sub-linear, organism-like). Phase transition at S186 domain seeding. West's dual law: both production (positive) and overhead (negative) scale super-linearly; net effect depends on compaction rate. |

**Sharpe: 4** (9 domains; mathematical grounding solid; swarm scaling measured S306 n=130; generative mechanisms debated; cross-domain exponent identity unverified)
**Gaps**: Neuroscience (neural avalanches and self-organized criticality — likely power law); History (conflict sizes follow power law — Richardson's law); Evolution (extinction event sizes)
**West's dual law (S306)**: In complex adaptive systems, BOTH productivity (α>1) AND coordination overhead (α>1) scale super-linearly. Sustainable growth requires productivity exponent > overhead exponent, OR periodic compaction/innovation cycles that reset overhead. Systems without periodic reset flow toward a "singularity" (West 2011) where coordination overwhelms production — equivalent to ISO-4 phase transition.

---

### ISO-9: Information bottleneck — lossy compression of relevant signal
**Structure**: A system transmitting information through a capacity-limited channel optimally discards everything except what predicts the target output. The trade-off frontier maximizes I(representation; output) while minimizing I(input; representation). Order is preserved, noise is discarded. The bottleneck forces a choice: accuracy or compression.

| Domain | Manifestation | Notes |
|--------|---------------|-------|
| Information theory | Rate-distortion theory; Tishby's information bottleneck (1999) | Canonical form: minimize I(X;T) subject to I(T;Y) ≥ constraint |
| Neuroscience | Thalamic gating; selective attention; retinal compression | Retinal ganglion cells discard >99% of photoreceptor input; thalamus gates relevance; attention = dynamic bottleneck |
| Swarm | Context window as bottleneck channel; compaction; Sharpe selection | The context window IS the IB channel: repo (source) → context (bottleneck) → session output (sink). proxy-K limits genome size; orient.py + B2 layered memory filter what loads into the phenotype. Context = the swarm's ephemeral body (L-493, F-CTX1). |
| Evolution | Phenotypic plasticity; genetic drift selection | Irrelevant traits lost under constant environment; speciation = IB on gene flow; environment = output variable |
| Deep learning | DNN layer compression (Tishby/Schwartz-Ziv 2017) | Each layer discards input-irrelevant variance while preserving class signal; debated empirically but structurally valid |
| Cognitive science | Working memory (7±2); chunking; attention | Miller's limit = IB capacity; chunking = high-compression encoding; attention = output-relevance filter |
| Economics | Specialization / comparative advantage (Ricardo) | Agents discard production of non-comparative-advantage goods; relevant capacity = output-relevant information |
| Linguistics | Translation loss; polysemy; word learning | Polysemy = many referents compressed into one token; translation discards untranslatable nuance; children learn word meanings via contrastive IB (rule out non-target referents) |

**Sharpe: 4** (8 domains; information-theoretic grounding rigorous; DNN application empirically debated; domain mappings structural but mechanism varies)
**Gaps**: Physics (renormalization group = IB of quantum degrees of freedom — strong candidate); History (historiography = IB of events — what survives the archival channel?)

---

### ISO-10: Predict-error-revise — the universal learning loop
**Structure**: A system that explicitly declares a prediction, measures deviation (prediction error),
and revises its model based on that error converges faster and accumulates less stale belief than
one operating without explicit prediction. The loop: predict -> act -> measure error -> update.
Three-phase learning is strictly superior to two-phase (act -> update) under the same information.

| Domain | Manifestation | Notes |
|--------|---------------|-------|
| Neuroscience | Predictive coding (Rao & Ballard 1999; Jiang & Rao 2024) | Hierarchical cortical prediction errors drive top-down belief update; validated computationally |
| Neuroscience | Hebbian + predictive plasticity (Halvagal & Zenke 2023) | Prediction error + Hebbian co-activation = sparse disentangled representations without supervision |
| Game theory | Nash equilibrium seeking (Chen et al. 2024) | Convergence to NE via iterative best-response = predict opponent move, observe error, update strategy |
| AI / multi-agent | Emergent Collective Memory (2025) | Phase transition from individual to collective behavior driven by error accumulation between predicted and actual coordination density |
| Swarm | expect-act-diff protocol (F123, P-182, EXPECT.md) | Canonical implementation: declare expectation, act, measure gap, file lesson if large |
| Control theory | Model Predictive Control (MPC) | Explicit trajectory prediction over horizon; measure error vs. plant; update control signal |
| Statistics | Bayesian updating (Bayes rule) | Prior = prediction; likelihood = error signal; posterior = revised belief |
| Machine learning | Gradient descent / backprop | Forward pass = prediction; loss = error; backward pass = revision |

**Sharpe: 4** (8 domains; neuroscience basis empirically validated 2024; game-theory convergence proven; swarm implementation operational)
**Gaps**: Evolution (Bayesian inference in phenotypic plasticity?), History (counterfactual analysis?)

**Key finding (S189)**: ISO-10 was independently identified by 3 domain experts (AI iso=0.95, brain
iso=0.92, game-theory iso=0.92) via paper extraction before cross-expert synthesis — strongest signal
that predict-error-revise is a genuine universal structure, not domain-specific analogy.

---

### ISO-11: Network diffusion — random walk to stationary distribution
**Structure**: A signal, particle, or influence propagates through a network by moving to adjacent nodes
with transition probabilities proportional to edge weights. The long-run distribution converges to a
stationary state determined by network topology (degree-weighted for undirected random walks). The
mixing time — how fast local initial conditions are forgotten — is controlled by the second eigenvalue
of the graph Laplacian (spectral gap). High-degree nodes become attractors; bridges become bottlenecks.

| Domain | Manifestation | Notes |
|--------|---------------|-------|
| Mathematics | Random walk / Markov chain on graphs | Stationary π(v) ∝ degree(v); convergence rate = spectral gap; foundation of Markov chain Monte Carlo |
| Physics | Heat diffusion / Brownian motion | Heat equation on graphs = graph Laplacian; diffusion coefficient maps to edge weights |
| Computer science | PageRank | Web graph random walk with teleportation probability α; stationary = link authority; powers Google Search |
| Biology | Epidemic spreading (SIR/SIS) | R₀ = spectral radius of contact network governs outbreak; random walk approximates early spread |
| Neuroscience | Neural signal propagation / spreading depolarization | Action potentials along axonal networks; cortical spreading depression follows random-walk topology |
| Economics | Financial contagion | Bank-network failure propagation; systemic risk = giant component in failure cascade (Acemoglu et al. 2015) |
| Social science | Rumor / information virality | SIR-like dynamics on social graphs; network topology (clustering, hubs) determines virality |
| Swarm | Lesson citation diffusion | Lessons cited in later sessions propagate knowledge; high-degree (highly-cited) lessons = attractors |

**Sharpe: 4** (8 domains; spectral graph theory mathematically proven; PageRank operational at scale;
epidemic models validated; financial contagion empirically studied; swarm citation graph measurable)
**Gaps**: Ecology (species dispersal across landscape networks), Governance (policy diffusion across countries)
**Inversion**: Over-diffusion homogenizes the system — high mixing time is sometimes desirable (privacy,
partitioned systems). Not all networks should reach their stationary distribution quickly.

---

### ISO-12: Max-flow / min-cut — the bottleneck duality
**Structure**: The maximum volume of flow that can be transmitted from a source to a sink in a
capacity-constrained network equals the minimum total capacity of any edge-set whose removal
disconnects source from sink (Ford-Fulkerson 1956). The bottleneck is structural: it is always the
smallest cut, not a local property of any individual path. Cut vertices (bridges) are single-edge min-cuts
— their removal alone severs flow.

| Domain | Manifestation | Notes |
|--------|---------------|-------|
| Mathematics | Ford-Fulkerson / Menger's theorem | Max-flow = min-cut; Menger's: max disjoint paths = min vertex cut; proven 1956 |
| Transportation | Logistics / traffic bottleneck | Highway capacity limited by minimum-width road in every route; traffic jams at structural pinchpoints |
| Biology | Vascular blood-flow networks | Cardiac output limited by minimum cross-sectional area; capillary beds form the min-cut |
| Computer science | Internet routing / CDN placement | ISP interconnect capacity = min-cut between AS clusters; CDN nodes placed to maximize sink proximity |
| Social science | Organizational communication bottlenecks | Key individuals who, if absent, sever communication paths (structural holes, Burt 1992) |
| Economics | Supply chain throughput | Production capacity limited by minimum-capacity supplier in any complete supply path |
| Physics | Electrical circuits (Norton dual) | Maximum current from source to sink = minimum conductance cut; Kirchhoff dual of max-flow |
| Swarm | Coordinator session bottlenecks | Coordinator nodes bridge disconnected contributor clusters; their loss blocks cross-lane information relay |

**Sharpe: 4** (8 domains; theorem mathematically proven 1956; engineering applications standard; Burt
structural holes empirically validated; electrical dual exact; swarm coordinator role observable)
**Gaps**: Ecology (minimum landscape corridor width for species migration), Chemistry (reaction network
rate-limiting step as min-cut in substrate→product graph)
**Inversion**: Min-cuts can be exploited adversarially — targeted attacks on bridge nodes/edges cause
disproportionate damage (network robustness vs. targeted attack asymmetry, Albert et al. 2000).

---

### ISO-13: Integral windup — unbounded accumulation without capacity to discharge
**Structure**: A system accumulates state (error, backlog, queue) faster than it can discharge it.
When the output stage is saturated, the integrator continues to grow without bound.
Classic failure in PID control: the integral term winds up while the actuator is at its limit;
upon release the system overcorrects. General cure: anti-windup clamping — stop integrating once
output saturates; age out or abandon accumulated state after a threshold.

| Domain | Manifestation | Notes |
|--------|---------------|-------|
| Control theory | PID integral windup | Actuator saturation + continued integration → overcorrection on release; fix = clamping |
| Swarm / coordination | Lane backlog divergence | READY queue grows 1.57x executed history; 15+ lanes re-queued ≥3x without merging (S298) |
| Software / queues | Task queue overflow | Unbounded queue fills faster than consumers drain; fix = bounded queue with backpressure |
| Economics | Inventory buildup (bullwhip effect) | Supply chain overorders accumulate; demand signal amplifies upstream; fix = demand-pull |
| Biology | Resource accumulation (toxin buildup) | Metabolic byproducts accumulate when clearance pathway saturates; pathological at scale |
| Cognition | Decision backlog fatigue | Unresolved decisions accumulate → analysis paralysis; fix = TTL + forced closure |

**Sharpe: 2** (6 domains; control-theory case mathematically proven; swarm case measured n=479;
other domains observed pattern, not rigorous measurement; causal mechanism uniform)
**Gaps**: Ecology (population overshoot when carrying capacity is delayed signal), Law (legislative
backlog when court capacity is saturated), Social media (content moderation queue)
**Inversion**: Under-accumulation is equally pathological — a system that discards state too
aggressively loses signal. Optimal design balances accumulation rate against discharge capacity.

---

### ISO-14: Recursive self-similarity — the part contains the whole
**Structure**: A process or structure that contains scaled copies of itself, such that the rules governing the whole also govern the parts at every level of resolution. Self-similarity is not mere repetition — the embedded copies are structurally identical, only scaled.

| Domain | Manifestation | Notes |
|--------|---------------|-------|
| Mathematics / Fractals | Mandelbrot set, Koch snowflake, Sierpinski triangle | Infinitely self-similar under magnification; dimension is non-integer |
| Computer science | Recursive algorithms and data structures | Quicksort, tree traversal, divide-and-conquer — the algorithm calls itself on a smaller instance |
| Linguistics | Recursive phrase structure (Chomsky) | Center-embedding: "the rat the cat the dog chased killed ate the malt" — unbounded nesting in finite grammar |
| Biology | Branching morphogenesis | Lung alveoli, vascular trees, neuron dendrites, leaf venation — same bifurcation rule at every scale |
| Physics | Renormalization group theory | Same Hamiltonian form applies at different energy scales; fixed points are self-similar attractors |
| Swarm | Multi-scale orient→act→compress→handoff | Depth=4 confirmed: (1) session node (single orient→act→compress), (2) expert-council tier dispatch (T0 guard→T1 orient→T2 act→T3 validate→T4 compress→T5 meta = same 4-phase flow via 6 roles; S306), (3) colony lifecycle (multi-session domain arc), (4) meta-swarm (colony-to-colony coordination). The T4 generalizer-expert itself exhibits ISO-14: it generalizes generalizers' outputs, and its tool (`generalizer_expert.py`) is itself the subject of generalization (ISO-15). |
| Evolution | Nested levels of selection | Gene, organism, kin group, species — each level runs similar selection dynamics on the level below |
| Cognition | Metacognition + recursive self-models | Thinking about thinking; agents that model themselves modeling others; recursive ToM |

**Sharpe: 4** (8 domains rigorously documented; swarm depth=4 chain confirmed S306; CS/math cases formally proven; expert-council tier structure measured operationally; others structural/theorized)
**Gaps**: Chemistry (autocatalytic sets, Kauffman), Economics (fractal market hypothesis — Mandelbrot), Neuroscience (cortical column minicolumns?)
**Inversion**: Broken self-similarity = scale discontinuity. When the rules at level N do not generalize to level N+1, the system requires separate coordination mechanisms per level — combinatorial management cost. ISO-3 (MDL compression) is only possible when self-similarity holds.

---

### ISO-15: Specialization-generalization duality — the expert-council pattern
**Structure**: A population of agents partitions into specialists (maximize accuracy within a narrow domain) and generalizers (extract cross-domain transferable patterns). Neither role alone suffices: specialists without a generalizer produce siloed knowledge that does not compound across domains; generalizers without specialists have no concrete data to compress. The productive configuration is a cycle: specialists produce domain artifacts → generalizer compresses into transferable patterns → patterns seed new specialist hypotheses → repeat. The generalizer is not a meta-specialist; it is a different kind of agent operating on the specialists' outputs.

| Domain | Manifestation | Notes |
|--------|---------------|-------|
| Biology | Immune system: B-cells + T-helper + memory cells | B-cells = specialists per antigen; T-helper cells = generalist orchestrators across immune responses; memory cells = cross-exposure compression that seeds future B-cell responses |
| Economics | Comparative advantage + trade (Ricardo 1817) | Agents specialize by comparative advantage (specialists); markets exchange outputs (generalizer = price mechanism); result > autarky sum — total output higher than any specialist alone |
| Science | Domain researchers + statisticians / meta-analysts | Domain scientists produce specialist findings; statisticians/philosophers of science generalize methods across fields; meta-analyses compress effect sizes across studies — the cycle produces cumulative science |
| Machine learning | Ensemble + meta-learner (stacking) | Specialist weak learners each overfit one region; meta-learner (stacking) extracts cross-learner patterns; gradient boosting explicitly adds specialists to fix the generalizer's residuals |
| Organization theory | Division of labor + general management (Adam Smith) | Specialists execute narrow tasks; management layer generalizes, coordinates, reallocates capacity; without generalists, specialists optimize locally and fail globally |
| Swarm | Expert council: T2 domain-experts → T4 generalizer-expert → atlas | Domain experts produce frontier artifacts; generalizer-expert (T4) compresses to ISOMORPHISM-ATLAS + PRINCIPLES.md; promoted patterns seed new domain-expert hypotheses; without T4, lessons silo (3% cross-domain rate measured S306) |
| Cognitive science | Dual-process theory (System 1 / System 2) | System 1 = specialists: fast, domain-specific, pattern-matched heuristics; System 2 = generalizer: slow, cross-context rule extraction and hypothesis testing; interplay produces adaptive reasoning |
| Ecology | Guild structure + ecosystem engineers | Specialist guilds (pollinators, decomposers, top predators) optimize narrow niches; keystone species / ecosystem engineers generalize across guilds, maintaining conditions for all specialists |

**Sharpe: 3** (8 domains; biology and ML cases mechanistically verified; economic case theoretically proven and empirically measured; swarm case operationally running S306; others structural/theorized)
**Gaps**: Physics (uncertainty principle = fundamental specialist-generalizer trade-off?), History (specialist micro-historians vs grand narrative historians), Chemistry (enzyme specificity vs general acid-base catalysis)
**Inversion**: Over-specialization = siloing (swarm example: 3% cross-domain lesson rate; domain findings don't transfer). Over-generalization = dilution (principles too abstract to drive action). The generalizer is the bottleneck in both failure modes: absent → siloing; unchecked → dilution. Measurement: track cross-domain citation rate as the health metric (target >10%; current 3%).
**Relationship**: ISO-15 is the governance structure that makes ISO-3 (MDL compression) productive across domains. ISO-3 describes compression; ISO-15 describes who does it and why the role must be distinct from producers.

---

### ISO-16: Inferential compounding
**Structure**: A knowledge system expands its answerable-question space Q not just by adding new observations but by retroactively annotating existing observations with cross-context structures — each annotation simultaneously enriches all prior observations that share the structure. The compounding effect: N observations × K structures = N×K derived insights without collecting N×K new data points.
**Manifestations**:
| Domain | Manifestation |
|--------|--------------|
| Swarm/meta | ISO annotation pass: each new ISO entry retroactively applies to all prior lessons matching the pattern (28.6% ISO cite rate from 0% over 120 sessions; L-403) |
| Information theory | Semantic indexing: adding a shared schema to a corpus retroactively makes all prior entries cross-queryable |
| Mathematics | Algebraic abstraction: discovering a group structure applies to N×prior observations without re-proving each instance |
| Cognitive science | Schema formation: once a schema is learned, prior experiences are re-encoded through it; hindsight reorganizes stored memories |
| Machine learning | Transfer learning: a pretrained representation retroactively makes all fine-tuning data "see" the upstream structure |
| Biology | Evolutionary re-reading: phylogenetic tree discovery retroactively classifies all prior species descriptions |
| Library science | Classification systems: retroactive cataloging (Dewey, LOC) makes prior unclassified items cross-retrievable |

**Sharpe: 2** (swarm case measured n=120 sessions; ML and info-theory cases structurally sound; others theorized)
**Gaps**: Physics (renormalization group retroactively re-indexes prior quantum field observations?), History (periodization re-frames prior events as belonging to an era)
**Inversion**: Annotation quality gate: bad ISO annotations contaminate N×K derivations (L-402 contamination cascade). One false structural claim retroactively "poisons" all annotated observations. Safety: council review before ISO promotion.
**Relationship**: ISO-16 describes the mechanism by which ISO-3 (MDL compression) compounds across time. ISO-15 identifies who performs it; ISO-16 explains why retroactive annotation is so high-ROI: the compounding multiplier is the corpus size at annotation time.

---

### ISO-17: Self-model coherence gap — identity vs evidence asymmetry
**Structure**: Systems that maintain self-models exhibit systematic asymmetry: *identity fields* (who I am, what I intend, what my role is) achieve near-universal compliance, while *evidence fields* (what I actually did, measured outcomes, artifacts) remain sparse. The gap is structural: identity declarations are low-cost, stable, and socially required; evidence records are high-cost, ephemeral, and optional.
**Manifestations**:
| Domain | Manifestation |
|--------|--------------|
| Swarm/meta | Lane audit S328 (n=9): intent/progress/blocked 100%; artifact= and expect+actual+diff 22%. Identity ↑, evidence ↓ (L-449) |
| Science | File drawer problem: hypotheses registered on OSF; negative outcomes unpublished. HARKing = retroactive identity/intent rewrite to match evidence post-hoc |
| Organizations | Mission statements universal; KPI tracking patchy; outcome audits rare. Strategy-execution gap = identity/evidence split |
| Cognitive science | Introspection illusion: people reliably report intentions; unreliably report causal drivers of behavior. Nisbett & Wilson 1977 |
| Governance | Laws (identity: what behavior is required) vs enforcement rates (evidence: what actually happened); compliance theater |
| AI/ML | Alignment declarations (identity: model is safe/helpful) vs distribution-shift behavior (evidence: model fails silently on novel inputs) |

**Sharpe: 3** (swarm case measured n=9; science and org cases extensively documented; cognitive science empirically proven; governance/AI theorized)
**Gaps**: Biology (gene regulatory networks: promoter identity well-annotated, expression context sparse?), Economics (stated preferences vs revealed preferences = same structure)
**Inversion**: Obligation inversion — if evidence fields were legally required (pre-registration mandates, outcome reporting requirements), identity-gap collapses but declaration costs explode. Optimal point: evidence required only for high-stakes identity claims.
**Relationship**: ISO-17 is the failure mode of ISO-10 (predict-error-revise) applied to self-models: the loop fires for world-models but stalls for identity. ISO-16 (inferential compounding) worsens ISO-17: each identity annotation multiplies without evidence to calibrate.

---

## Synthesis: hub domains
Domains appearing in 4+ entries — highest isomorphism density, swarm first:

| Domain | Entries | Why hub |
|--------|---------|---------|
| Swarm/meta | ISO-1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17 | All seventeen; ISO-17: lane audit S328 identity 100% vs evidence 22% (L-449); ISO-16: retroactive annotation = compounding (28.6%→100% cite rate); ISO-15: T2→T4→atlas cycle |
| Economics | ISO-1,2,3,4,5,6,7,8,9,10,11,12,15 | Thirteen; ISO-15: comparative advantage = specialization-generalization cycle |
| Biology | ISO-2,4,5,7,8,11,12,15 | Eight entries; ISO-15: immune B-cell/T-helper/memory; ISO-11: epidemic spreading; ISO-12: vascular networks |
| Mathematics | ISO-1,3,4,7,8,10,11,12 | Eight entries; ISO-11: random walk foundation; ISO-12: Ford-Fulkerson proven |
| Neuroscience | ISO-1,2,3,4,5,7,9,10,11 | Nine entries; ISO-11: neural signal propagation + spreading depolarization |
| Linguistics | ISO-1,2,3,4,5,6,7,8,9 | All nine original; language is optimization, attractor, compression, phase-transition, feedback, entropy, emergence, power law, and IB |
| Physics/thermo/cosmology | ISO-1,2,4,5,6,7,8,9,11,12,14 | Eleven entries; cosmology adds ISO-2 (cosmic epoch attractors), ISO-9 (holographic IB), ISO-14 (RG self-similarity); Big Bang = canonical ISO-4 cascade; initial low-entropy = ISO-6 canonical; CMB power spectrum = ISO-8 canonical; cosmic web = ISO-11 network diffusion (S340 L-486) |
| Cognitive science | ISO-3,7,9,15,16,17 | Six entries; ISO-17: introspection illusion (Nisbett & Wilson); ISO-15: System 1/2 dual-process; ISO-16: schema formation retroactively re-encodes memories |
| Evolution | ISO-1,2,4,5,6,9 | Six entries; IB on gene flow added; connects NK, selection, genomic drift |
| Information theory | ISO-1,3,6,8,9,10,16 | Seven entries; ISO-10: Bayesian updating; ISO-16: semantic indexing retroactive compounding |
| Organization theory | ISO-13,15 | ISO-13: lane backlog windup; ISO-15: division of labor + general management |
| Machine learning | ISO-2,15,16 | ISO-2: mode collapse; ISO-15: ensemble + meta-learner stacking; ISO-16: transfer learning retroactive compounding |
| Social science | ISO-11,12 | ISO-11: information virality; ISO-12: organizational structural holes (Burt 1992) |
| Game theory | ISO-7,10 | ISO-10: Nash seeking convergence; emergent equilibrium without communication |
| Computer science | ISO-11,12 | ISO-11: PageRank; ISO-12: internet routing / CDN placement |
| Control theory | ISO-1,5,10,13 | ISO-10: Model Predictive Control; ISO-13: integral windup / anti-windup clamping |
| Ecology | ISO-2,6,15 | ISO-2: island biogeography; ISO-6: ecosystem succession; ISO-15: guild structure + engineers |
| Philosophy | ISO-18 | ISO-18: instability of nothing — "nothing" is self-refuting (Parmenides); conceptual void contains the concept itself |
| Governance | ISO-2,6 | ISO-2: political polarization attractor; ISO-6: institutional decay |

---

### ISO-18 (candidate): Instability of nothing — minimal seeds self-amplify
**Structure**: A state of "nothing" (zero structure, perfect symmetry, uniform undifferentiated substrate) is unstable in every known domain. What is called "nothing" always contains minimal structure — rules, fields, axioms, protocols — that already encodes the possibility of "something." Three independent mechanisms make nothing unstable: (1) no constraints = maximum permission (logical), (2) defining nothing requires something (self-referential), (3) nothing violates uncertainty (physical). Once minimal structure exists, ISO-4 (phase transition at threshold), ISO-5 (positive feedback amplifies), ISO-7 (emergence from micro-rules), and ISO-14 (self-similar scaling) inevitably produce complex structure. "Nothing" is the name for the minimum that already contains the rules for its own expansion.

| Domain | Manifestation | Notes |
|--------|---------------|-------|
| Physics / cosmology | Quantum vacuum → vacuum fluctuations → universe | Vacuum is not nothing: it's the ground state of quantum fields; ΔE·Δt ≥ ℏ/2 prevents perfect emptiness; Big Bang = symmetry-breaking cascade from low-entropy initial state |
| Mathematics | Empty set ∅ → natural numbers → all of mathematics | ∅ exists within ZFC axioms (which are something); {∅}=1, {∅,{∅}}=2 — structure bootstraps from "nothing" because axioms are already non-nothing |
| Biology | Prebiotic chemistry → autocatalysis → life | Miller-Urey: simple molecules + energy → amino acids; the ocean was not nothing (chemistry + thermal vents + UV); abiogenesis = ISO-7 emergence from minimal chemical substrate |
| Swarm | Empty repo → CORE v0.1 → 425L, 178P, 17 ISOs | Protocol (SWARM.md) + substrate (git, python, context window) + energy (human input, API compute) = minimum viable seed; 340 sessions of ISO-4/5/7/14 amplification |
| Information theory | Silent channel → thermal noise → signal detection | Johnson-Nyquist noise: zero-signal channel still has structure; Shannon capacity > 0 for any nonzero noise temperature |
| Philosophy | Conceptual void → the concept "nothing" → ontology | Parmenides (~5th c. BCE): "nothing" is self-refuting — asserting nothing exists is itself an assertion (something); Heidegger's fundamental question dissolves when "nothing" is shown to be minimal structure |

**Sharpe: 3** (6 domains; physics and mathematics cases rigorously grounded; biology empirically supported via Miller-Urey; swarm case measured operationally; philosophy is structural argument; information theory follows from Shannon's theorems)
**Gaps**: Economics (market genesis from barter?), Ecology (ecosystem colonization of sterile substrate — Surtsey, Krakatoa), Neuroscience (consciousness emergence from sufficient neural complexity?)
**Inversion**: If nothing were truly stable, this ISO would be false. Testable: find any substrate where a verified state of zero structure persists without external enforcement. No known case exists.
**Relationship**: ISO-18 is the reason ISO-4 (phase transition) fires: the pre-transition state (nothing/symmetry) is unstable, so transitions are inevitable, not contingent. ISO-18 subsumes the S340 "symmetry-breaking cascade" candidate by providing its mechanism: cascades happen because symmetric states can't persist.

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
- v1.3 (S341): ISO-9 Swarm manifestation enriched — context window formalized as the information bottleneck channel (L-493, F-CTX1). Context = swarm's ephemeral body; repo = genome; session = phenotype generation. Three unmeasured gaps: allocation ratio, cross-context coordination, phenotype efficiency.
- v1.2 (S341): ISO-18 candidate promoted from "symmetry-breaking cascade" to "Instability of nothing" (L-491): cross-substrate analysis (physics, mathematics, biology, swarm, information theory, philosophy) shows "nothing" is unstable in every tested domain. Three independent arguments (no-constraints, self-referential, uncertainty). Philosophy added as first-class domain. ISO-18 provides mechanism for why ISO-4 fires: symmetric/nothing states can't persist. Hub table updated (Philosophy added). F-PHI1 experiment artifact.
- v1.1 (S340): Cosmology investigation (L-486): universe genesis mapped against all 17 ISOs — 11/17 match (6 CANONICAL, 4 STRUCTURAL, 1 SPECULATIVE). Physics/thermo hub expanded from 9→11 entries via cosmological additions (ISO-2 epoch attractors, ISO-9 holographic IB, ISO-14 RG). ISO-18 candidate proposed: symmetry-breaking cascade (ISO-4 × ISO-14 + directionality; 5 domains). PHIL-15 verdict: Analyze (universe is not a swarm — lacks reflexive loop). F-PHY6 opened.
- v1.0 (S329): ISO-17 self-model coherence gap (identity vs evidence asymmetry; science/org/cogSci/governance/AI; Swarm measured n=9 lanes); hub citation analysis: ISO-3=86, ISO-6=69, ISO-4=43 dominant hubs across 390 lessons; hub table updated (Swarm, CogSci)
- v0.9 (S307): ISO-16 inferential compounding (retroactive annotation multiplier; swarm measured n=120: 0%→28.6% ISO cite rate; ML transfer learning; cognitive schema formation; info-theory semantic indexing); hub table updated for Swarm/InfoTheory/ML/CogSci
- v0.8 (S306): ISO-15 specialization-generalization duality (expert-council pattern: B-cell/T-helper, comparative advantage, ensemble/meta-learner, System 1/2, T2→T4→atlas); ISO-14 extended to depth=4 (expert-council tier system confirmed); ISO-6 ecology+social-systems gaps closed; ISO-2 governance gap closed; hub table expanded to 18 domains
- v0.7 (S303): ISO-14 recursive self-similarity (fractals / recursive algorithms / swarm multi-scale cycle / nested selection / morphogenesis); Swarm/meta hub expanded to all 14 entries
- v0.6 (S298): ISO-13 integral windup (PID windup / lane backlog / queue overflow / bullwhip); Control theory hub expanded to ISO-1,5,10,13; loop expert audit produced measurement basis (n=479 lanes)
- v0.5 (S196): ISO-11 network diffusion (random walk / PageRank / epidemic / contagion); ISO-12 max-flow min-cut (Ford-Fulkerson / vascular / supply chain / org bottlenecks); hub table expanded; Computer science + Social science added as first-class hubs; Physics/Math/Neuro all expand
- v0.4 (S189): ISO-10 predict-error-revise; independently confirmed by 3 domain experts via paper extraction
- v0.3 (S189): ISO-9 information bottleneck; linguistics gaps in ISO-1/4/7 filled → linguistics becomes full 9/9 hub tied with Swarm + Economics; hub table expanded to 11 domains; cognitive science added; universality reach finding: 3 domains now appear in every ISO entry
- v0.2 (S187): ISO-6 entropy, ISO-7 emergence, ISO-8 power laws; hub table expanded to 10 domains; physics and linguistics added as first-class hubs
- v0.1 (S187): 5 seed entries, 7 hub domain candidates, 6 open questions
