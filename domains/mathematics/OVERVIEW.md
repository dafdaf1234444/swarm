# Mathematical Dependency Tree

## Algebra

- **C-002** (corollary): Groups of prime order are cyclic [STATED]
  - Prerequisites: T-006
- **D-005** (definition): Binary operation [STATED]
- **D-006** (definition): Group [STATED]
  - Prerequisites: D-005
- **D-007** (definition): Abelian group [STATED]
  - Prerequisites: D-006
- **D-008** (definition): Ring [STATED]
  - Prerequisites: D-007
- **D-009** (definition): Field [STATED]
  - Prerequisites: D-008
- **D-010** (definition): Homomorphism [STATED]
  - Prerequisites: D-006
- **D-011** (definition): Subgroup [STATED]
  - Prerequisites: D-006
- **D-013** (definition): Normal subgroup [STATED]
  - Prerequisites: D-011
- **D-015** (definition): Quotient group [STATED]
  - Prerequisites: D-012
- **D-028** (definition): Polynomial ring [STATED]
  - Prerequisites: D-008
- **T-006** (theorem): Lagrange's theorem [STATED]
  - Prerequisites: D-011, D-006
- **T-007** (theorem): First isomorphism theorem [STATED]
  - Prerequisites: D-010, D-012, D-013
- **T-008** (theorem): Cauchy's theorem [STATED]
  - Prerequisites: T-006, D-006
- **T-009** (theorem): Sylow theorems [STATED]
  - Prerequisites: T-008, D-011
- **T-018** (theorem): Fundamental theorem of algebra [STATED]
  - Prerequisites: D-009, D-028, D-024

## Analysis

- **A-001** (axiom): Real number completeness [STATED]
- **C-001** (corollary): Integration by substitution [STATED]
  - Prerequisites: T-005, T-003
- **D-001** (definition): Limit of a function [STATED]
- **D-002** (definition): Continuity [STATED]
  - Prerequisites: D-001
- **D-003** (definition): Derivative [STATED]
  - Prerequisites: D-001
- **D-004** (definition): Riemann integral [STATED]
  - Prerequisites: A-001, D-001
- **T-001** (theorem): Extreme Value Theorem [STATED]
  - Prerequisites: D-002, A-001
- **T-002** (theorem): Intermediate Value Theorem [STATED]
  - Prerequisites: D-002, A-001
- **T-003** (theorem): Mean Value Theorem [STATED]
  - Prerequisites: D-002, D-003, T-001
- **T-004** (theorem): Fundamental Theorem of Calculus Part 1 [STATED]
  - Prerequisites: D-002, D-004, T-003
- **T-005** (theorem): Fundamental Theorem of Calculus Part 2 [STATED]
  - Prerequisites: T-004, D-003, D-004
- **T-017** (theorem): Bolzano-Weierstrass theorem [STATED]
  - Prerequisites: D-024, A-001
- **T-043** (theorem): Stone-Weierstrass theorem [STATED]
  - Prerequisites: D-024, D-002, D-008
- **T-045** (theorem): Banach fixed-point theorem [STATED]
  - Prerequisites: D-027, D-002

## Differential-Equations

- **D-046** (definition): Ordinary differential equation [STATED]
  - Prerequisites: D-003
- **D-047** (definition): Initial value problem [STATED]
  - Prerequisites: D-046
- **D-048** (definition): Linear ODE [STATED]
  - Prerequisites: D-046, D-014
- **D-049** (definition): Partial differential equation [STATED]
  - Prerequisites: D-046
- **T-038** (theorem): Picard-Lindelof theorem [STATED]
  - Prerequisites: D-047, D-002
- **T-039** (theorem): Gronwall's inequality [STATED]
  - Prerequisites: D-004, D-046
- **T-040** (theorem): Existence of matrix exponential [STATED]
  - Prerequisites: D-048, D-017
- **T-041** (theorem): Sturm-Liouville theory [STATED]
  - Prerequisites: D-048, D-022

## Linear-Algebra

- **C-003** (corollary): Invertibility iff nonzero determinant [STATED]
  - Prerequisites: D-018, D-014
- **D-012** (definition): Vector space [STATED]
  - Prerequisites: D-009, D-007
- **D-014** (definition): Linear map [STATED]
  - Prerequisites: D-012
- **D-016** (definition): Basis and dimension [STATED]
  - Prerequisites: D-012
- **D-017** (definition): Matrix [STATED]
  - Prerequisites: D-014, D-016
- **D-018** (definition): Determinant [STATED]
  - Prerequisites: D-017
- **D-020** (definition): Eigenvalue and eigenvector [STATED]
  - Prerequisites: D-017, D-014
- **D-022** (definition): Inner product space [STATED]
  - Prerequisites: D-012
- **T-010** (theorem): Rank-nullity theorem [STATED]
  - Prerequisites: D-014, D-016
- **T-011** (theorem): Spectral theorem [STATED]
  - Prerequisites: D-022, D-020
- **T-012** (theorem): Cayley-Hamilton theorem [STATED]
  - Prerequisites: D-018, D-020

## Measure-Theory

- **D-033** (definition): Sigma-algebra [STATED]
- **D-034** (definition): Measure [STATED]
  - Prerequisites: D-033
- **D-035** (definition): Measurable function [STATED]
  - Prerequisites: D-033, D-034
- **D-036** (definition): Lebesgue integral [STATED]
  - Prerequisites: D-035, D-034
- **D-037** (definition): Lp space [STATED]
  - Prerequisites: D-036
- **T-026** (theorem): Monotone convergence theorem [STATED]
  - Prerequisites: D-036
- **T-027** (theorem): Dominated convergence theorem [STATED]
  - Prerequisites: D-036, T-026
- **T-028** (theorem): Fubini's theorem [STATED]
  - Prerequisites: D-036, D-034
- **T-029** (theorem): Radon-Nikodym theorem [STATED]
  - Prerequisites: D-034, D-036
- **T-030** (theorem): Riesz representation theorem [STATED]
  - Prerequisites: D-037, D-022

## Number-Theory

- **D-029** (definition): Divisibility [STATED]
- **D-030** (definition): Prime number [STATED]
  - Prerequisites: D-029
- **D-031** (definition): Greatest common divisor [STATED]
  - Prerequisites: D-029
- **D-032** (definition): Congruence [STATED]
  - Prerequisites: D-029
- **T-019** (theorem): Fundamental theorem of arithmetic [STATED]
  - Prerequisites: D-030, D-029
- **T-020** (theorem): Euclidean algorithm [STATED]
  - Prerequisites: D-031, D-029
- **T-021** (theorem): Bezout's identity [STATED]
  - Prerequisites: T-020, D-031
- **T-022** (theorem): Infinitude of primes [STATED]
  - Prerequisites: D-030, T-019
- **T-023** (theorem): Fermat's little theorem [STATED]
  - Prerequisites: D-032, D-030
- **T-024** (theorem): Chinese remainder theorem [STATED]
  - Prerequisites: D-032, D-031
- **T-025** (theorem): Quadratic reciprocity [STATED]
  - Prerequisites: D-032, D-030, T-023

## Probability

- **C-004** (corollary): Weak law via Chebyshev [STATED]
  - Prerequisites: T-034, T-032
- **D-038** (definition): Probability space [STATED]
  - Prerequisites: D-033, D-034
- **D-039** (definition): Random variable [STATED]
  - Prerequisites: D-038, D-035
- **D-040** (definition): Expected value [STATED]
  - Prerequisites: D-039, D-036
- **D-041** (definition): Variance and standard deviation [STATED]
  - Prerequisites: D-040
- **D-042** (definition): Conditional probability [STATED]
  - Prerequisites: D-038
- **D-043** (definition): Independence [STATED]
  - Prerequisites: D-042
- **T-031** (theorem): Bayes' theorem [STATED]
  - Prerequisites: D-042
- **T-032** (theorem): Law of large numbers [STATED]
  - Prerequisites: D-040, D-043
- **T-033** (theorem): Central limit theorem [STATED]
  - Prerequisites: D-041, D-043, T-032
- **T-034** (theorem): Chebyshev's inequality [STATED]
  - Prerequisites: D-041, D-040
- **T-035** (theorem): Borel-Cantelli lemma [STATED]
  - Prerequisites: D-038, D-043
- **T-042** (theorem): Kolmogorov extension theorem [STATED]
  - Prerequisites: D-038, T-014, A-002

## Set-Theory

- **A-002** (axiom): Axiom of choice [STATED]
- **D-044** (definition): Cardinality [STATED]
- **D-045** (definition): Countability [STATED]
  - Prerequisites: D-044
- **T-036** (theorem): Cantor's theorem [STATED]
  - Prerequisites: D-044
- **T-037** (theorem): Zorn's lemma [STATED]
  - Prerequisites: A-002

## Topology

- **D-019** (definition): Topological space [STATED]
- **D-021** (definition): Continuous map [STATED]
  - Prerequisites: D-019
- **D-023** (definition): Homeomorphism [STATED]
  - Prerequisites: D-021
- **D-024** (definition): Compactness [STATED]
  - Prerequisites: D-019
- **D-025** (definition): Connectedness [STATED]
  - Prerequisites: D-019
- **D-026** (definition): Hausdorff space [STATED]
  - Prerequisites: D-019
- **D-027** (definition): Metric space [STATED]
  - Prerequisites: D-019
- **T-013** (theorem): Heine-Borel theorem [STATED]
  - Prerequisites: D-024, D-027, A-001
- **T-014** (theorem): Tychonoff theorem [STATED]
  - Prerequisites: D-024
- **T-015** (theorem): Brouwer fixed point theorem [STATED]
  - Prerequisites: D-023, D-024
- **T-016** (theorem): Urysohn lemma [STATED]
  - Prerequisites: D-026, D-021
- **T-044** (theorem): Baire category theorem [STATED]
  - Prerequisites: D-027, D-024

