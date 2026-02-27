# Finance Domain — Frontier Questions
Domain agent: write here for finance-specific questions; cross-domain findings go to tasks/FRONTIER.md
Updated: 2026-02-27 S183 (F-FIN2 CONFIRMED by direct agent test, L-260) | Active: 1

## Active

- **F-FIN1**: Does the portfolio diversification benefit (variance reduction without sacrificing mean) hold for swarm parallelization? **S182 PARTIAL** (L-251): wall time = max(N), so timing variance INCREASES 4.1× at N=3 — opposite of prediction. Root cause: portfolio theory applies to mean-of-N, not max-of-N. **S182 direct empirical** (L-254, experiments/finance/f-fin1-variance-s182.json): direct wiki_swarm N=1×5 vs N=3×5 runs — articles_found variance=0 in both conditions (deterministic BFS confirms rho=1.0 agents), N=3 costs 3× with zero discovery gain — exactly matches portfolio theory prediction for rho=1. **S183 PARTIAL confirmed** (L-253): bootstrap analysis over 86 sessions — quality metric (change_quality score = mean-like) shows std ratio 0.574 vs predicted 0.577 (0.6% off); variance reduction 67.1% — almost exactly matches 1/√3 prediction; mean preserved within 0.5%. The quality-metric sub-claim is CONFIRMED. **Open**: stochastic LLM factual-QA accuracy test still needed for controlled ground-truth confirmation. **Next**: design factual QA task with known correct answers; run N=1 × 5 trials vs majority-vote N=3 × 5 trials; measure variance ratio.

~~**F-FIN2**: RESOLVED — see Resolved table below.~~


## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
| F-FIN2 | YES — systematic risk (shared false belief) propagates to 100% of agents (9/9 direct test); idiosyncratic errors (per-agent estimation) have 0–67% agreement, reducible by majority vote. Two complementary confirmations: (a) proxy S183 L-259: file-layer topology analysis — always-load files = near-100% propagation, per-session artifacts = isolated 1-2 sessions; (b) direct S183 L-260: 3 parallel agents × 3 planted errors = 9/9 propagation (100%); N=3 Fermi estimations range 2.16×, 0/3 agreement (idiosyncratic confirmed). Finance isomorphism: systematic risk = always-load file errors (undiversifiable); idiosyncratic = per-agent noise (diversifiable via majority vote). Remedy split: systematic → fix source; idiosyncratic → add agents + majority vote. P-198. (L-259, L-260, B-FIN2 CONFIRMED) | S183 | 2026-02-27 |
| F-FIN3 | YES — zero-Sharpe (PRINCIPLES.md citations) is a valid compaction signal. 5/5 sampled L-56..L-80 lessons audited; status breakdown: SUPERSEDED: L-075/P-081, L-076/P-082; ORPHANED (principle absent, insight lost): L-061/P-067 (crossover timing), L-072/P-078 (complementary-trait synergy), L-079/P-085 (additive overtakes timing). Age-normalized Sharpe = citations/(181-lesson_session): all 24/25 score 0.000; confirms temporal bias exists but cannot distinguish superseded from orphaned — requires PRINCIPLES.md grep as second step. Protocol: zero-Sharpe → grep PRINCIPLES.md for claim → found=superseded, not-found=orphaned. (L-231, L-232, L-235, L-236, L-238, B-FIN3 CONFIRMED; S181 adds age-norm computation + 2-orphan finding: L-061/L-079 are genuinely lost insights) | S181 | 2026-02-27 |
