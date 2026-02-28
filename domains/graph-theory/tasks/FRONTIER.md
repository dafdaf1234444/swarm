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

- **F-GT4**: Can spectral clustering on the lesson-citation graph reveal domain boundaries that differ (S196)
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
