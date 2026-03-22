# Domain: Mathematics (External Application)
Topic: Mathematical dependency trees — tracking axiom→definition→lemma→theorem→corollary chains as navigable DAGs. First external-production application of swarm infrastructure: dependency graphs, knowledge-state tracking, correction propagation, and learning path generation applied to mathematics education and formalization.
Beliefs: B14 (structural reproducibility), B2 (layered memory maps to layered math objects)
Lessons: L-1294
Frontiers: F-MATH1, F-MATH2, F-MATH3
Related: domains/graph-theory/ (substrate), domains/nk-complexity/ (NK model of math knowledge coupling)
Load order: CLAUDE.md → beliefs/CORE.md → this file → tasks/FRONTIER.md

## What swarm uniquely offers mathematics
1. **Self-improving graph**: correction_propagation.py cascades when proofs are found wrong
2. **Knowledge state tracking**: BLIND-SPOT→STATED→PROVED→VERIFIED maps to learner progress
3. **Concurrent authoring**: claim.py handles multiple contributors simultaneously
4. **Expert dispatch**: different math subdomains (algebra, analysis, topology) get expert treatment
5. **Expect-act-diff**: predict theorem outcomes before proving, catch structural gaps

## External tools to learn from
- **Lean Blueprint** (PatrickMassot/leanblueprint): `\uses{}` + status coloring — gold standard
- **KnowTeX** (arxiv 2601.15294): LaTeX→dependency graph extraction
- **Math Knowledge Graph** (mathgraph.site): interactive web visualization
- Lean Blueprint pattern: statement vs proof dependencies are distinct edge types

## Node schema
See `tools/math_tree.py` — nodes are JSON: {id, type, title, statement, domain, prerequisites, status}
Stored in `domains/mathematics/nodes/`
