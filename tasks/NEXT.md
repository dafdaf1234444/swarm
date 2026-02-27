# State
Updated: 2026-02-27 S73b+ (F111 builder + principle-count resolution)

## What just happened
S73b+ (this session):
- **F111 fix phase DONE (proposal)**: full refactoring analysis of complexity_ising_idea.
  Found 21 duplicated function copies across 15 files (510 lines, 4.2% of codebase).
  3 target extractions: config_to_patch_states → src/coarse_grain.py,
  compute_ei_equalized → src/ei_compute.py, compute_patch_autocorrelation → src/analysis.py.
  Plus pyproject.toml + pytest conversion. Proposal in experiments/f111-builder/.
  Read-only per HQ-2 — human can apply.
- **Principle-count disagreement RESOLVED**: S73a header-trust wins. After S70c compaction,
  ID-counting finds 147 IDs but only 131 are definitions (16 are references like "P-033 merged"
  inside other principles). A parser can't distinguish without understanding the text format.
  Header is maintained by compaction sessions; INDEX cross-checks against it. Correct approach.

S75 (prior):
- F116 proxy K baseline: 26,107 tokens. tools/proxy_k.py live.
- Confidence backfill: L-048–L-058 done.

## For next session
1. **F116 subtractive sub-swarm** — pick a belief in PRINCIPLES.md with 0 citations (e.g.
   P-048, P-052 — measurement principles), remove it, run validate_beliefs.py, test if
   swarm still functions. Accept if proxy K decreases + no validation failures. (added S75)
2. **F-NK4** — duplication K metric. Measure on B9 validation set (19 packages). (added S72)
3. **F111 apply phase** — Human review of experiments/f111-builder/complexity-ising-refactor-proposal.md.
   If approved, apply the 4-step refactoring to complexity_ising_idea. (added S73b+)
4. **F84 belief variants** — minimal-nofalsif leads at ~140 sessions. Fresh eval? (added S69)
5. **F114 belief citation rate** — auto-link relevant principles during work. (added S65)

## Key state
- F111: test 1 (dutch) = full pipeline, test 2 (complexity_ising_idea) = full proposal ready.
  Human review needed to apply. experiments/f111-builder/complexity-ising-refactor-proposal.md.
- F116: baseline measured (26,107 tokens). tools/proxy_k.py live. Next: subtractive sub-swarm.
- maintenance.py principle-count: RESOLVED (header-trust, S73a correct).
- F113: ALL 4 PAIRS DONE.
- F110 Tier 3: A2 DONE. B2+C2 deferred.
- 148 lessons, 131 principles, 14 beliefs, 20 frontiers.
- docs/PAPER.md: living self-paper (cadence 20 periodic).
