# Graph Theory Domain — Frontier Questions
Domain agent: write here, not to tasks/FRONTIER.md
Seeded: S196 | 2026-02-28

## Active

- **F-GT1**: Does the swarm's lesson-citation graph exhibit scale-free structure (power-law degree
  distribution from preferential attachment)? What is the exponent α?
  **S306 Result**: alpha=1.903 — NOT classical scale-free (threshold [2.0,3.0]). 57.8% orphans break
  preferential attachment. ISO-8 PARTIAL: non-zero tail is power-law-like; bulk is not. Hub lessons
  (L-001, L-304) confirmed as knowledge attractors — compaction must protect them. L-383.
  Artifact: experiments/graph-theory/f-gt1-scale-free-s306.json. Status: **RESOLVED PARTIAL**.

- **F-GT2**: What is the effective chromatic number of the SWARM-LANES concurrent-execution conflict (S196)
  graph? Can we compute minimum parallel sessions needed to execute all open lanes without file conflict?
  **Stakes**: Practical scheduling bound — tells the coordinator how many simultaneous safe sessions exist.
  **Method**: Build conflict graph (lanes sharing modified files = adjacent); compute χ via greedy coloring.

- **F-GT3**: Are there cut-vertex sessions in swarm history — sessions whose commits, if removed, (S196)
  would have disconnected the knowledge-evolution DAG (broken the chain of lesson evolution)?
  **Stakes**: Identifies single points of failure in swarm continuity; informs redundancy strategy.
  **Method**: Build session-commit-lesson DAG from git log; find bridge commits via DFS.

- **F-GT4**: Can spectral clustering reveal domain boundaries differing from declared labels?
  **S314 PARTIAL**: 17 connected components (giant n=193 + 16 micro + 128 orphans). All spectral clusters = "meta"-dominated. Declared taxonomy NOT confirmed by citation structure — topology-blind. L-423.
  Artifact: experiments/graph-theory/f-gt4-spectral-clustering-s314.json.
  Open: (1) improve label coverage (currently 40.6%); (2) re-run spectral on giant component only with k=10.

- **F-GT5**: What portion of the swarm's active work graph is reachable from recent human signals and core
  state nodes? Which components are unreachable?
  **Stakes**: Reachability measures coordination diffusion; unreachable components indicate drift and
  wasted work with no signal source.
  **Method**: Build a directed graph from HUMAN-SIGNALS → lanes → artifacts → lessons → frontiers. Compute
  reachability from signal nodes, identify disconnected components, and list cut vertices (bridge nodes).
## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|

## Notes
Graph theory contributes to ISOMORPHISM-ATLAS.md (ISO-11, ISO-12) more than to domain-specific beliefs.
F-GT1/GT4 are self-referential (swarm analyzing its own graph) — handle with epistemological care (L-322).
