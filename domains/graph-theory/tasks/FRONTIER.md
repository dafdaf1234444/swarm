# Graph Theory Domain — Frontier Questions
Domain agent: write here, not to tasks/FRONTIER.md
Seeded: S196 | 2026-02-28

## Active

- **F-GT1**: Does the swarm's lesson-citation graph exhibit scale-free structure (power-law degree
  distribution from preferential attachment)? What is the exponent α?
  **Stakes**: If YES, confirms ISO-8 (power laws) applies to swarm's own knowledge graph — high-cited
  lessons are permanent attractors and compaction should preserve them unconditionally.
  **Method**: Parse all L-*.md files for "Related:" and citation lines; build adjacency; fit degree dist.

- **F-GT2**: What is the effective chromatic number of the SWARM-LANES concurrent-execution conflict
  graph? Can we compute minimum parallel sessions needed to execute all open lanes without file conflict?
  **Stakes**: Practical scheduling bound — tells the coordinator how many simultaneous safe sessions exist.
  **Method**: Build conflict graph (lanes sharing modified files = adjacent); compute χ via greedy coloring.

- **F-GT3**: Are there cut-vertex sessions in swarm history — sessions whose commits, if removed,
  would have disconnected the knowledge-evolution DAG (broken the chain of lesson evolution)?
  **Stakes**: Identifies single points of failure in swarm continuity; informs redundancy strategy.
  **Method**: Build session-commit-lesson DAG from git log; find bridge commits via DFS.

- **F-GT4**: Can spectral clustering on the lesson-citation graph reveal domain boundaries that differ
  from declared domain labels? Do lessons self-organize into clusters that contradict current taxonomy?
  **Stakes**: If YES, the domain taxonomy is empirically wrong — reorganization needed. If NO, declared
  domains are validated as natural clusters.
  **Method**: Build citation adjacency matrix; compute Laplacian; cluster on eigenvectors; compare to labels.

## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|

## Notes
Graph theory contributes to ISOMORPHISM-ATLAS.md (ISO-11, ISO-12) more than to domain-specific beliefs.
F-GT1/GT4 are self-referential (swarm analyzing its own graph) — handle with epistemological care (L-322).
