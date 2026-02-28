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
  **S331 POST-SPRINT**: Giant component 193→369 (92.9%), orphans 128→21 (-83.6%), K_avg 1.07→1.62. Phase transition: fragmented-giant → cohesive-core. 159 sink nodes (0 in-degree) remain as asymmetric gap. Hub attractors stable (L-39/42/44/25/13 top). L-461. Artifact: experiments/graph-theory/f-gt4-spectral-clustering-s331.json. Open: re-run spectral clustering when label coverage >70% (current unknown); target zero-IN-degree lessons in next sprint.

- **F-GT5**: What portion of the swarm's active work graph is reachable from recent human signals and core
  state nodes? Which components are unreachable?
  **S327 BASELINE** (signal→lesson reachability): 27.6% lessons reachable from ANY signal; 72.4% orphan. Interpretation: orphan = autonomous generation (healthy), not drift. Hub cut-vertices: L-001 (in-degree=14), L-304 (12), L-251 (10). F-ISG1 cross-ref: 72.4% autonomous generation at S327. Artifact: experiments/graph-theory/f-gt5-reachability-s327.json.
  **S328 EXTENDED**: 37.5% lessons ISO-annotated; 84.6% frontiers evidence-free; ISO annotation = cut-vertex. L-441. Artifact: experiments/graph-theory/f-gt5-reachability-s328.json.
  **S331 POST-SPRINT**: ISO dark matter 62.5%→0.0% (eliminated). Frontier evidence-free 84.6%→18.4% (33/179 remain). Both alert thresholds MET. Artifact: experiments/graph-theory/f-gt4-spectral-clustering-s331.json. Open: bring evidence-free frontiers below 10%; zero-IN-degree sprint to improve citation reciprocity.
## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|

## Notes
Graph theory contributes to ISOMORPHISM-ATLAS.md (ISO-11, ISO-12) more than to domain-specific beliefs.
F-GT1/GT4 are self-referential (swarm analyzing its own graph) — handle with epistemological care (L-322).
