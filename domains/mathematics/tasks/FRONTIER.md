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
