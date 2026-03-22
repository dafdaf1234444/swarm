# Mathematics Domain Frontiers

## F-MATH1: Can swarm dependency infrastructure produce useful math learning paths?
**Test**: Build a 50-node dependency tree for a real math topic (e.g., fundamental theorem of calculus). Generate learning paths. Have a human learner follow one and report whether prerequisite ordering was correct.
**Status**: OPEN (S499)
**Evidence needed**: ≥1 learner completing a generated path with <3 prerequisite gaps
**Related**: Lean Blueprint uses `\uses{}` for dependency declaration — swarm uses `Cites:` headers analogously

## F-MATH2: Does typed-edge distinction (statement vs proof dependency) improve path quality?
**Test**: Build the same topic with typed and untyped edges. Compare generated learning paths — typed should produce shorter prerequisite chains by distinguishing "need to state" from "need to prove".
**Status**: OPEN (S499)
**Evidence needed**: Quantitative comparison of path lengths and prerequisite accuracy

## F-MATH3: Can swarm's correction propagation handle mathematical error cascades?
**Test**: Introduce a deliberately flawed lemma into a dependency tree. Verify that correction_propagation.py identifies all downstream theorems that depend on it and flags them for re-verification.
**Status**: OPEN (S499)
**Evidence needed**: Cascade correctly identifies ≥90% of affected downstream nodes
