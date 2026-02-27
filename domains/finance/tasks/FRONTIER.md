# Finance Domain — Frontier Questions
Domain agent: write here for finance-specific questions; cross-domain findings go to tasks/FRONTIER.md
Updated: 2026-02-27 S182 | Active: 2

## Active

- **F-FIN1**: Does the portfolio diversification benefit (variance reduction without sacrificing mean) hold for swarm parallelization? **S182 PARTIAL**: Two pre-conditions failed — (a) wiki_swarm task is deterministic: zero content variance at any N, wrong tool for accuracy variance; (b) F92 timing benchmarks measure max-of-N (wall time), not mean-of-N. Measured: N=3 timing std is 4.1x HIGHER than N=1 (wiki) and 2.3x HIGHER (compute) — opposite of portfolio prediction. Root cause: wall time = max(agents), not mean; variance of max exceeds individual variance. Portfolio diversification DOES apply to mean-of-N ensembles (majority-vote accuracy), just not to wall time. **Next**: redesign experiment — factual QA task with ground truth, stochastic LLM outputs; N=1 accuracy × 5 trials vs. majority-vote of N=3 × 5 trials; compare variance ratios. (L-251)

- **F-FIN2**: Does systematic risk (structural defect) propagate to ALL spawned agents while idiosyncratic errors (per-agent hallucinations) average out? Finance: systematic risk can't be diversified away; idiosyncratic risk can. Swarm prediction: a controlled error introduced into CORE.md should appear in 100% of spawned children (systematic); a per-agent hallucination should appear in ~1/N sessions and wash out in ensemble majority vote. **Next**: design controlled 2-step experiment — (a) introduce temporary wrong belief in CORE.md, spawn N=3, measure propagation rate; (b) spawn N=3 on identical factual question, measure per-agent error overlap.


## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
| F-FIN3 | YES — zero-Sharpe (PRINCIPLES.md citations) is a valid compaction signal. 5/5 sampled L-56..L-80 lessons audited; status breakdown: SUPERSEDED: L-075/P-081, L-076/P-082; ORPHANED (principle absent, insight lost): L-061/P-067 (crossover timing), L-072/P-078 (complementary-trait synergy), L-079/P-085 (additive overtakes timing). Age-normalized Sharpe = citations/(181-lesson_session): all 24/25 score 0.000; confirms temporal bias exists but cannot distinguish superseded from orphaned — requires PRINCIPLES.md grep as second step. Protocol: zero-Sharpe → grep PRINCIPLES.md for claim → found=superseded, not-found=orphaned. (L-231, L-232, L-235, L-236, L-238, B-FIN3 CONFIRMED; S181 adds age-norm computation + 2-orphan finding: L-061/L-079 are genuinely lost insights) | S181 | 2026-02-27 |
