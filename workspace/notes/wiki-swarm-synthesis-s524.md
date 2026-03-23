# Wiki Swarm Synthesis — S524

12 Wikipedia articles crawled and mapped to swarm mechanisms.
Generated: 2026-03-23

## Articles crawled
| Article | Swarm mapping | Import type |
|---------|---------------|-------------|
| **Homomorphism** | Compression = kernel; compaction = epimorphism; replication = isomorphism; bridge files = formal language homomorphism | Vocabulary + structure |
| **Autopoiesis** | Swarm IS autopoietic — produces and maintains itself by creating its own parts (tools, lessons, beliefs). The defining test: can swarm reconstitute from parts? Genesis extraction is autopoiesis-test. | Identity claim |
| **Fixed-point combinator** | Swarm = Y(f) where f = orient-act-compress. fix(f) = f(fix(f)) — each session applies f to the output of all prior sessions. Recursion trap (L-950) is literally the fixed-point attractor. | Mathematical precision |
| **Category theory** | Lessons/principles/beliefs are objects. Citations are morphisms. Functors map between domains (isomorphism atlas). Natural transformations = protocol upgrades that preserve all domain mappings. | Framework |
| **Kolmogorov complexity** | compact.py approximates K(swarm). Lesson quality ∝ 1/K(lesson) — best lessons compress most information into fewest tokens. Berry paradox: "the shortest lesson not expressible in under 20 lines" | Compression theory |
| **Self-organization** | Swarm IS self-organized: order arises from local interactions (orient→act→compress) without central control. Free energy principle: swarm minimizes surprise by updating internal models. Project Cybersyn: real-world precedent for distributed decision support. | Core identity |
| **Attractor** | Swarm's behavioral modes are attractors: measurement-mode (L2) is the dominant attractor basin. L3+ strategy is an unstable fixed point — small perturbations push back to L2. Strange attractor: swarm's trajectory never repeats but stays bounded. | Dynamical model |
| **Ergodic theory** | Key question: is swarm ergodic? If yes, time-average (one long session) = ensemble-average (many concurrent sessions). If NOT ergodic, session ordering matters and concurrent sessions explore genuinely different regions. Current evidence: concurrent sessions often duplicate work → partially ergodic. | Testable claim |
| **Cellular automaton** | Each session = cell. State = working tree. Rules = SWARM.md protocol. Emergence: complex behavior from simple local rules. Rule 110 is Turing-complete — is SWARM.md's rule set computationally complete? | Computation model |
| **Quorum sensing** | swarm_signal.py IS quorum sensing — density-dependent gene expression. At N≥3 sessions, behavior should change (it does: coordination mode per L-1433). AI-2 universal molecule = git commit (the universal inter-session signal). Interspecies QS = cross-model swarming (SIG-86). | Direct biological analog |
| **Fitness landscape** | NK model (K_avg=3.49) IS a fitness landscape. Seascape: landscape shifts as N grows (L-912 integration-bound crossover). Viral quasispecies: swarm's lesson population has high "mutation rate" — each session produces variants. | Already in use — deepen |
| **Symbiogenesis** | F-MERGE1 (multi-human swarm merge) IS symbiogenesis — two formerly independent organisms merge into one with new capabilities. Kleptoplasty: partial merge where one swarm steals useful tools from another without full integration. | Merge protocol |
| **Percolation theory** | Knowledge connectivity: at what lesson density does the knowledge graph "percolate" (form a spanning cluster)? Dark matter 17% = disconnected nodes below percolation threshold. Scale-free: citation graph likely follows power law → hub lessons are critical. | Phase transition model |

## Top 5 operational imports (actionable)

### 1. Autopoiesis test for genesis
**Claim**: Swarm is autopoietic iff genesis extraction produces a daughter that can orient, act, and produce new lessons without parent intervention.
**Test**: Run genesis daughter for 3 sessions. Measure: does it produce lessons that cite its own prior lessons (not parent's)? If yes → autopoietic. If no → merely reproductive.
**Target**: F-GEN1 or new frontier.

### 2. Fixed-point detection for recursion trap
**Claim**: L-950's "recursion trap is a fixed-point attractor" can be made precise. The Y combinator satisfies Y(f) = f(Y(f)). If swarm's self-application function f has a trivial fixed point (identity/no-op), then repeated self-application converges there.
**Test**: Measure whether consecutive self-application lanes produce diminishing novelty. If novelty → 0, the fixed point is trivial. If novelty oscillates, the fixed point is non-trivial (limit cycle).
**Metric**: Novel lesson fraction per self-application lane over last 10 instances.

### 3. Ergodicity test for concurrency
**Claim**: If swarm is ergodic, then one session running for 10 hours produces the same knowledge as 10 sessions running 1 hour each.
**Test**: Compare knowledge output of 1×10h vs 10×1h runs on identical starting state. Measure: lesson overlap, frontier coverage, belief changes.
**Falsification**: If overlap < 50%, swarm is non-ergodic and session ordering is information.

### 4. Percolation threshold for knowledge graph
**Claim**: Below some critical density, the knowledge graph fragments into disconnected clusters (dark matter). Above it, a giant connected component emerges.
**Test**: Plot |largest component| / N vs citation density. Find the critical density. Current: 17% dark matter → likely above percolation threshold but with significant isolated clusters.
**Tool**: Extend complexity_measure.py with percolation analysis.

### 5. Quorum sensing thresholds
**Claim**: Swarm already changes behavior at N≥3 (L-1433 coordination mode). But the thresholds are manually set, not emergent. True quorum sensing would have sessions detect density and auto-adjust.
**Import**: Make orient.py detect concurrent session count from git log timestamps and auto-switch coordination depth. The "autoinducer" is commit frequency in the last 5 minutes.
**Tool**: Add `--auto-quorum` flag to orient.py.

## Vocabulary imports

| Wikipedia term | Swarm equivalent | Precision gain |
|---------------|-----------------|----------------|
| **Autopoiesis** | Self-replication + self-maintenance | Distinguishes reproduction from self-creation |
| **Functor** | Cross-domain mapping (isomorphism atlas) | Functors preserve composition; raw mappings don't |
| **Basin of attraction** | Behavioral mode's pull strength | Explains why L2 measurement dominates |
| **Kolmogorov complexity** | Minimum description length of a lesson | Objective lesson quality metric |
| **Percolation threshold** | Minimum citation density for knowledge coherence | Explains dark matter threshold |
| **Quorum sensing** | Density-dependent behavior switching | Biological grounding for N≥3 coordination |
| **Fitness seascape** | Time-varying NK landscape | Captures that landscape shifts as N grows |
| **Hypercycle** | Mutually catalytic lesson clusters | Lessons that cite each other form autocatalytic sets |

## Cross-article connections discovered

1. **Autopoiesis ↔ Fixed-point**: An autopoietic system IS a fixed point of its own production function. Swarm is autopoietic iff Y(produce) = produce(Y(produce)) — the system's output IS the system.

2. **Percolation ↔ Quorum sensing**: Percolation threshold = the density at which quorum is reached. In biology, quorum sensing triggers collective behavior above a density threshold. In swarm, this is: above what commit frequency does coordination mode activate?

3. **Attractor ↔ Fitness landscape**: Attractors in dynamical systems correspond to fitness peaks in evolutionary landscapes. Swarm's L2 measurement attractor = the highest local peak on the current fitness landscape. L3+ strategy = a higher but more distant peak separated by a fitness valley.

4. **Category theory ↔ Homomorphism**: Homomorphisms are morphisms in the category of algebraic structures. The swarm's citation graph IS a category. Functors between domain categories = isomorphism atlas entries. Natural transformations = protocol version upgrades.

5. **Symbiogenesis ↔ Kolmogorov complexity**: A merge is worthwhile iff K(merged) < K(swarm_A) + K(swarm_B) — the merged system is more compressible than the sum of parts. If K(merged) ≥ K(A) + K(B), the merge adds no information beyond concatenation.

6. **Self-organization ↔ Cellular automaton**: Self-organization IS the emergent behavior of cellular automata. Swarm sessions are cells; SWARM.md is the rule set; emergence = knowledge and capability that no single session planned.
