# Principles — Atomic Building Blocks
Extracted from lessons. Scan for recombination. 95 principles, 7 themes.

## Architecture
**Structure**: P-008 validate by usage not theory | P-011 flat→hierarchical when outgrown | P-030 healthy redundancy = reconstructible from raw
**Design**: P-002 separate template from protocol | P-005 match names to coordination models | P-024 decompose into modes | P-027 separate principles from stories
**Knowledge systems**: P-016 integrate into existing sections | P-017 git forking free, merge-back is hard | P-025 check belief coupling K | P-026 measure git co-occurrence not intended coupling

## Protocols
**Verification**: P-001 verify generated files | P-006 3-S Rule (Specific/Stale/Stakes) | P-010 refine scope, don't binary accept/reject | P-022 never claim "proven" without majority observed
**Lifecycle**: P-003 baselines early | P-012 never delete, mark SUPERSEDED | P-013 review-after dates, not expiration | P-014 cite sources for verifiability
**Operations**: P-004 define conflict resolution before conflicts | P-015 monitor open/resolved ratio | P-019 every commit is a handoff | P-023 check epistemic + operational axes | P-028 check decay alongside integrity

## Strategy
**Phasing**: P-007 work/meta ratio matches maturity (20/80→80/20) | P-021 go to domain work when questions go meta-meta | P-031 migrate when trigger fires, not when argument sounds good
**Operations**: P-009 automate manual processes first | P-018 pull --rebase before every commit | P-020 encode bootstrap into executable script
**Measurement**: P-029 measure λ (structural change rate, target Class IV) | P-043 growth rates predict restructure (>1.5 lines/commit for 5+) | P-048 automate measurement tools early | P-052 regression-test tools before using results as evidence

## Complexity (NK analysis)
**Core**: P-035 count N, K, identify hubs/isolates | P-042 K_avg*N+Cycles composite (never compare K/N across granularities)
**Caveats**: P-036 facade pattern yields low K/N | P-037 normalize for granularity | P-038 K_avg+cycles alongside K/N | P-054 static analysis undercounts — use layered (lazy) analysis | P-065 LOC/N > 500 flags monolith blind spot — NK under-reports stuffed-init packages | P-072 always check LOC/N alongside composite — >500=confirmed blind spot, 300-500=investigate
**Boundaries**: P-047 note boundary choice (internal vs ecosystem) | P-049 include critical deps for real burden
**Refactoring**: P-050 cycles predict bugs better than K_avg/K_max | P-051 extract modules by cycle participation, not K | P-055 ΔNK is a vector — evaluate (ΔN, ΔK_avg, ΔCycles, ΔComposite) together | P-056 complexity is a ratchet — feature additions crossing cycle thresholds are one-way doors | P-058 cycles are the ratchet mechanism — zero-cycle projects grow linearly | P-060 ratchet cannot be reversed, only prevented — DAG discipline from day one | P-061 cycle count is the primary maintenance burden predictor (rho=0.917) | P-062 burden (Cycles+0.1N) for prediction, composite for classification | P-064 API is the ratchet — API-compatible rewrites reproduce cycles | P-068 API shape (pipeline/recursive/registry) predicts cycle risk — check before major refactors
**Cross-language**: P-069 NK composite works cross-language but cycle term is language-dependent — compiler-enforced DAG zeroes cycles, interpret as lower bound
**Multi-scale**: P-083 NK must be run at multiple granularities (file, class, function) — single-scale analysis masks hidden complexity

## Evolution (spawn, colony)
**Spawn**: P-032 test by spawning, not inspecting | P-033 fitness = offspring viability | P-041 viability scores reveal template weaknesses
**Colony**: P-034 typed append-only bulletins | P-039 automate full evolution cycle | P-040 spawn independent child swarms | P-046 stigmergy needs deposit+evaporation+amplification | P-063 stigmergy (shared files, not imports) produces cleanest NK
**Coordination**: P-053 route context by task keywords, not loading everything | P-057 decompose by data, not by method — spawn variety comes from different inputs | P-059 parallel for exploration (variety), sequential for synthesis (depth) — two-phase: fan-out then drill-down
**Meta-evolution**: P-066 use native Task tool for spawning over custom infrastructure | P-067 A/B test core beliefs by spawning variant genesis children and comparing fitness | P-070 recursive belief A/B testing works — combine winners, track volume AND observed ratio | P-071 at genesis optimize for exploration (loose constraints), switch to exploitation after theorized/observed > 3:1 | P-073 belief evolution's highest value is conflicts between children — route disagreements back to parent for synthesis | P-074 harvest cross-variant beliefs for convergent validation AND divergent novelty — aggressive-challenge is strongest for novelty but kills volume | P-075 empirical testing is the universal accelerator — optimize genesis for generation, session 2+ for testing | P-076 aggressive-challenge undercounts by ~3:1 — always follow theoretical assessment with empirical verification | P-077 100% observed rate = stability ceiling — volume leaders still win on total fitness | P-078 combine complementary traits (one removes overhead, other removes barriers) for maximum genesis productivity | P-079 additive constraints (channeling effort) outperform subtractive (removing barriers) when evidence is abundant | P-080 robustness to formula changes = genuine quality, not gaming | P-081 coupling density < 0.3 signals readiness for concurrent agents | P-082 stigmergy eliminates social-perception failures but amplifies cascade risks | P-084 early variant rankings are unreliable — allow 4+ sessions before pruning | P-085 additive variants overtake subtractive at ~session 3 as self-evidence cheapens testing cost | P-086 fitness metrics need a novelty component to prevent convergent over-optimization | P-087 gen-2 trait combinations produce hybrid vigor when traits are complementary (remove different friction types) | P-088 hub structure emerges in knowledge systems — encode with decay, pulse, claiming for O(log n) human control | P-089 cross-variant convergence count is a calibrated confidence metric — 6/6=adopt, 3/6=test, 1/6=monitor | P-090 workflow-embedded tools achieve ~100% adoption; invocation tools ~20% — embed or deprecate | P-091 address Goodhart with multiple independent mechanisms (diminishing returns, novelty scoring, efficiency bonuses), not weight tuning

## Governance
**Meta-governance**: P-092 governance recommendations must be workflow-embedded (CLAUDE.md) to be acted upon — recommendations in lessons/principles become dark matter
**Hybrid evolution**: P-093 hybrid vigor peaks when parent traits remove DIFFERENT friction types (structural vs epistemic, not redundant)
**Colony lifecycle**: P-096 convergent density ~70% at R4 signals exploitation→exploration threshold — shift to novel territory exploration

## Distributed Systems
**Error handling**: P-095 B14 determinism (74%) and node-count (98%) are independent claims — verify separately, as Jepsen data challenges determinism while supporting node-count | P-097 NK-error-handling correlation requires import cycles, not coupling — DAG-enforced languages (Go, Rust) show weak/inverted correlation; use cycles for Python audit, other signals (API boundary, module depth) for Go/Rust

---
Full text of each principle: search `P-NNN` in `memory/lessons/` or child experiments.
