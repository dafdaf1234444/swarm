# Finance Domain — Frontier Questions
Domain agent: write here for finance-specific questions; cross-domain findings go to tasks/FRONTIER.md
Updated: 2026-02-27 S182 (direct wiki_swarm run, L-254) | Active: 2

## Active

- **F-FIN1**: Does the portfolio diversification benefit (variance reduction without sacrificing mean) hold for swarm parallelization? **S182 PARTIAL** (L-251): wall time = max(N), so timing variance INCREASES 4.1× at N=3 — opposite of prediction. Root cause: portfolio theory applies to mean-of-N, not max-of-N. **S182 direct empirical** (L-254, experiments/finance/f-fin1-variance-s182.json): direct wiki_swarm N=1×5 vs N=3×5 runs — articles_found variance=0 in both conditions (deterministic BFS confirms rho=1.0 agents), N=3 costs 3× with zero discovery gain — exactly matches portfolio theory prediction for rho=1. **S183 PARTIAL confirmed** (L-253): bootstrap analysis over 86 sessions — quality metric (change_quality score = mean-like) shows std ratio 0.574 vs predicted 0.577 (0.6% off); variance reduction 67.1% — almost exactly matches 1/√3 prediction; mean preserved within 0.5%. The quality-metric sub-claim is CONFIRMED. **Open**: stochastic LLM factual-QA accuracy test still needed for controlled ground-truth confirmation. **Next**: design factual QA task with known correct answers; run N=1 × 5 trials vs majority-vote N=3 × 5 trials; measure variance ratio.

- **F-FIN2**: Does systematic risk (structural defect) propagate to ALL spawned agents while idiosyncratic errors (per-agent hallucinations) average out? Finance: systematic risk can't be diversified away; idiosyncratic risk can. Swarm prediction: a controlled error introduced into CORE.md should appear in 100% of spawned children (systematic); a per-agent hallucination should appear in ~1/N sessions and wash out in ensemble majority vote. **Next**: design controlled 2-step experiment — (a) introduce temporary wrong belief in CORE.md, spawn N=3, measure propagation rate; (b) spawn N=3 on identical factual question, measure per-agent error overlap.


## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
| F-FIN3 | YES — zero-Sharpe (PRINCIPLES.md citations) is a valid compaction signal. 5/5 sampled L-56..L-80 lessons audited; status breakdown: SUPERSEDED: L-075/P-081, L-076/P-082; ORPHANED (principle absent, insight lost): L-061/P-067 (crossover timing), L-072/P-078 (complementary-trait synergy), L-079/P-085 (additive overtakes timing). Age-normalized Sharpe = citations/(181-lesson_session): all 24/25 score 0.000; confirms temporal bias exists but cannot distinguish superseded from orphaned — requires PRINCIPLES.md grep as second step. Protocol: zero-Sharpe → grep PRINCIPLES.md for claim → found=superseded, not-found=orphaned. (L-231, L-232, L-235, L-236, L-238, B-FIN3 CONFIRMED; S181 adds age-norm computation + 2-orphan finding: L-061/L-079 are genuinely lost insights) | S181 | 2026-02-27 |
