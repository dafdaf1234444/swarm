# Mathematical Dependency Trees

Build and navigate dependency graphs for mathematics — axioms through corollaries — with automatic learning paths, error cascade detection, and collaborative authoring.

## Quick start

```bash
# Add mathematical objects
python3 tools/math_tree.py add --type axiom --title "Completeness of reals" --domain analysis
python3 tools/math_tree.py add --type definition --title "Continuity" --domain analysis --prereqs A-001
python3 tools/math_tree.py add --type theorem --title "Extreme Value Theorem" --prereqs D-001,A-001

# Generate a learning path
python3 tools/math_tree.py path T-001

# Interactive visualization (open in browser)
python3 tools/math_tree.py export --format json > domains/mathematics/nodes_export.json
# Then open domains/mathematics/viewer.html in a browser

# Validate the DAG
python3 tools/math_tree.py validate

# Visualize
python3 tools/math_tree.py export --format dot > math.dot
dot -Tpng math.dot -o math.png    # requires Graphviz

# Export
python3 tools/math_tree.py export --format json
python3 tools/math_tree.py export --format markdown
```

## Node types

| Type | Prefix | DOT shape | Description |
|---|---|---|---|
| axiom | A | diamond | Accepted without proof |
| definition | D | box | Introduces a concept |
| lemma | L | ellipse | Helper result |
| proposition | P | ellipse | Moderate result |
| theorem | T | double octagon | Major result |
| corollary | C | octagon | Direct consequence |
| example | E | note | Illustrative instance |

## Edge types (statement vs proof dependencies)

Inspired by [Lean Blueprint](https://github.com/PatrickMassot/leanblueprint), edges are typed:

| Edge type | DOT style | Meaning |
|---|---|---|
| `uses_in_statement` | solid | Needed to even *state* the result |
| `uses_in_proof` | dashed | Needed only in the proof |
| `generalizes` | dotted | This result generalizes the target |
| `specializes` | bold | This result is a special case |

Specify with `--prereqs "D-001:uses_in_statement,T-002:uses_in_proof"`.

The distinction matters for learning paths: statement dependencies are hard prerequisites (you can't understand the theorem without them), while proof dependencies can be deferred.

## Status tracking

Nodes progress through: `stub → stated → proved → verified → formalized`

```bash
python3 tools/math_tree.py status T-001 proved
```

In DOT exports, status maps to fill colors:
- **white** = stub
- **light yellow** = stated
- **light blue** = proved
- **light green** = verified
- **green** = formalized

## Error cascade

When a lemma is found flawed, propagate the error:

```bash
# See what's affected
python3 tools/math_tree.py cascade L-003

# Mark all downstream nodes as needing re-verification
python3 tools/math_tree.py cascade L-003 --mark
```

## LaTeX import

Extract dependencies from LaTeX files using the Lean Blueprint `\uses{}` convention:

```latex
\begin{theorem}[Extreme Value Theorem]\label{thm:evt}
  \uses{def:continuity, ax:completeness}
  A continuous function on a closed bounded interval attains its extrema.
\end{theorem}
```

```bash
python3 tools/math_tree.py import-latex paper.tex           # preview
python3 tools/math_tree.py import-latex paper.tex --create   # create nodes
```

## Learning path generation

The `path` command performs a topological sort of all prerequisites needed to reach a target:

```bash
$ python3 tools/math_tree.py path T-005
Learning path to T-005 (Fundamental Theorem of Calculus Part 2):
  9 nodes, 8 prerequisite steps

  1. [S] D-001 (definition): Limit of a function
  2. [S] D-002 (definition): Continuity
  3. [S] A-001 (axiom): Real number completeness
  4. [S] D-004 (definition): Riemann integral
  5. [S] D-003 (definition): Derivative
  6. [S] T-001 (theorem): Extreme Value Theorem
  7. [S] T-003 (theorem): Mean Value Theorem
  8. [S] T-004 (theorem): FTC Part 1
  9. [S] T-005 (theorem): FTC Part 2 → TARGET
```

## How this uses swarm infrastructure

This tool is the first external application of the swarm's dependency tracking systems:

| Swarm mechanism | Math application |
|---|---|
| Citation graph (L→L edges) | Theorem→theorem prerequisite edges |
| Belief DAG validation (cycle detection) | Ensures no circular dependencies |
| Knowledge state (BLIND-SPOT→ACTIVE) | Maps to learner mastery tracking |
| Correction propagation | Error cascade when proofs are flawed |
| Concurrent authoring (claim.py) | Multiple contributors build the tree |
| Expert dispatch | Route work to domain specialists |

## Comparison with existing tools

| Feature | Lean Blueprint | KnowTeX | Math Knowledge Graph | **math_tree.py** |
|---|---|---|---|---|
| Input format | LaTeX | LaTeX | Web UI | CLI + LaTeX import |
| Statement/proof edge distinction | Yes | Partial | No | **Yes** |
| Status tracking | Yes (colors) | No | No | **Yes** |
| Error cascade | No | No | No | **Yes** |
| Learning path generation | No | No | Partial | **Yes** |
| Concurrent authoring | No | No | No | **Yes** (via claim.py) |
| Self-improving | No | No | No | **Yes** (swarm cycle) |
| Visualization | Web + PDF | DOT + TikZ | Canvas | **DOT + JSON + Markdown** |

## Data format

Nodes are stored as individual JSON files in `domains/mathematics/nodes/`:

```json
{
  "id": "T-004",
  "type": "theorem",
  "title": "Fundamental Theorem of Calculus Part 1",
  "statement": "If f continuous on [a,b], then F(x)=∫_a^x f(t)dt is differentiable and F'(x)=f(x)",
  "domain": "analysis",
  "prerequisites": [
    {"ref": "D-002", "edge_type": "uses_in_proof"},
    {"ref": "D-004", "edge_type": "uses_in_proof"},
    {"ref": "T-003", "edge_type": "uses_in_proof"}
  ],
  "status": "stated",
  "proof_sketch": "",
  "tags": [],
  "notes": ""
}
```

## Contributing

1. Add nodes with `python3 tools/math_tree.py add`
2. Run `python3 tools/math_tree.py validate` before committing
3. Use `python3 tools/claim.py claim domains/mathematics/manifest.json` for concurrent safety
4. Commit: `[S<N>] math: added <topic> dependency chain`
