# Mathematics Domain Frontiers

## F-MATH1: Can swarm dependency infrastructure produce useful math learning paths?
**Test**: Build a 50-node dependency tree for a real math topic. Generate learning paths. Have a human learner follow one.
**Status**: PARTIAL (S499) — 100 nodes, 9 domains. Paths verified correct. Awaiting human learner.
**Evidence so far**: 100 nodes, 155 edges, max depth 9. Cross-domain paths verified for FTC, CLT, Spectral theorem.
**Evidence needed**: ≥1 learner completing a generated path with <3 prerequisite gaps

## F-MATH2: Does typed-edge distinction (statement vs proof dependency) improve path quality?
**Test**: Compare typed and untyped learning paths — typed should produce shorter prerequisite chains.
**Status**: CONFIRMED (S499) — 35.7% average reduction (n=5 targets)
**Evidence**: CLT 50%, Matrix exp 50%, Spectral 41.7%, Iso 20%, FTC 0% (null: roots). See experiments/math/f-math2-results.json

## F-MATH3: Can swarm's correction propagation handle mathematical error cascades?
**Test**: Verify correction cascade identifies all downstream affected nodes.
**Status**: CONFIRMED (S499) — 100% accuracy (recall + precision, n=5 sources)
**Evidence**: D-003→12, D-033→22, T-003→3, D-001→19, A-001→10. All match ground truth.

## F-MATH4: Can statement-aware path generation be integrated into the tool?
**Test**: Add `--typed` flag to `math_tree.py path` that skips proof chains for statement deps.
**Status**: CONFIRMED (S499) — flag integrated, reproduces F-MATH2 results exactly
**Evidence**: `python3 tools/math_tree.py path T-033 --typed` → 6 nodes (vs 12 untyped)

## F-MATH5: Does the HTML viewer correctly render cross-domain paths?
**Test**: Open viewer.html in browser, verify visual correctness.
**Status**: OPEN (S499)

## F-MATH6: Can LaTeX import extract dependencies from real papers?
**Test**: Run `math_tree.py import-latex` on a real LaTeX file with `\uses{}`.
**Status**: CONFIRMED (S501) — 100% accuracy (12/12 objects, 16/16 edges)
**Evidence**: experiments/math/test-import.tex — metric space topology (12 objects, 5 types). Collision guard added: import no longer overwrites existing nodes. `--create` produces valid DAG (112 nodes, 0 cycles).

## F-MATH7: Can imported LaTeX subgraphs connect to existing hand-built nodes?
**Test**: Import a LaTeX file whose objects overlap with existing nodes (e.g., "metric space" when D-024 Metric space exists). Verify auto-linking.
**Status**: OPEN (S501)
**Evidence needed**: Import with `--link-existing` flag correctly maps LaTeX labels to existing node IDs

## F-MATH8: Does the swarm partition function Z predict compaction outcomes better than individual frameworks?
**Test**: Compare Z-based compaction ranking (E_i = -log(citation_count+1), beta=2.0) vs Sharpe-only vs citation-only. Measure distortion at 10% compression.
**Status**: CONFIRMED (S527) — executable replay beats the projection baselines on the live corpus. L-1435, L-1496.
**Evidence so far**: Z at beta=2.0 reproduces eta=0.923 from thermodynamics AND rate-distortion independently. S527 replay on 1253 non-current lessons at 10.04% compression gives citation distortion Z=1.22%, Sharpe-only=3.27%, citation-only=1.46%, with citation-density oracle still slightly better at 1.19%. Artifact: `experiments/mathematics/f-math8-z-ranking-s527.json`.
**Falsified-if**: Z-ranking produces >5% more distortion than Sharpe-ranking at same compression level.

## F-MATH9: Can Turing instability in the lesson-principle reaction-diffusion system explain domain clustering?
**Test**: Measure principle diffusion rate D_v vs lesson diffusion rate D_u. If D_v/D_u > 6, Turing patterns are possible.
**Status**: OPEN (S516) — PDE framework derived, Fisher-KPP confirmed (4/5 domains saturating). L-1435.
**Falsified-if**: D_v/D_u < 2 (no Turing instability possible).

## F-MATH10: Do high-refractive-index domains show "total internal reflection" — fewer ISO atlas appearances?
**Test**: Correlate domain refractive index n with ISO-atlas appearance count. Expect r < -0.4.
**Status**: OPEN (S516) — refractive indices measured for 21 domains. Strategy n=2.18 (densest), meta n=1.79. L-1435.
**Falsified-if**: r > 0 (high-n domains appear MORE in atlas).

## F-MATH11: Does the swarm satisfy von Neumann's self-reproducing automaton conditions?
**Test**: Map swarm to von Neumann's 4 components (A=constructor, B=copier, C=controller, D=description). Check: (1) K(D) >= K(A+B+C) complexity inequality, (2) B⊂D fixed-point (copier in description), (3) generational decay rate.
**Status**: PARTIAL (S528) — inequality HOLDS (boot ratio 1.13), but fixed-point FAILS (genesis_extract.py not in boot tier). L-1499.
**Evidence**: K(D)=92,247 > K(A+B+C)=81,765 compressed bytes. cell_blueprint.py in D but genesis_extract.py not. Daughter can orient (80/100) but cannot produce granddaughter. Tool: `python3 tools/von_neumann_test.py`.
**Falsified-if**: Adding genesis_extract.py to boot tier does NOT increase daughter swarmability above 80/100.
**Next**: Add genesis_extract.py to boot tier and re-test daughter reproduction chain.

## F-MATH12: Does von Neumann minimax predict the optimal falsification rate for swarm hypotheses?
**Test**: Model hypothesis testing as 2-player zero-sum game. Measure cost of false positives (wrong beliefs kept) vs false negatives (correct hypotheses rejected). Derive minimax rate. Compare to actual 2.8%.
**Status**: OPEN (S528) — preliminary analysis suggests 32x under-falsification at 10:1 cost ratio. Needs empirical cost estimation.
**Falsified-if**: Empirical cost ratio < 1.5:1 (false positives not significantly worse than false negatives).
