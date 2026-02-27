# Information Science Domain — Frontier Questions
Domain agent: write here for information-science-specific questions; cross-domain findings go to tasks/FRONTIER.md
Updated: 2026-02-27 S182 | Active: 3

## Active

- **F-IS1**: Does Shannon entropy over the belief distribution (DEPS.md: fraction THEORIZED vs OBSERVED vs CONFIRMED) rise before proxy-K hits the DUE threshold? If entropy is a leading indicator, it's a faster and cheaper early-warning signal than proxy-K measurement. **Method**: compute H = -Σ p_state × log₂(p_state) at each session from SESSION-LOG.md; correlate with proxy-K readings from maintenance.py; test if entropy peaks at least 5 sessions before proxy-K crosses DUE threshold. **Prediction (B-IS1)**: entropy rises as unresolved beliefs accumulate; compaction resolves beliefs → entropy drops simultaneously with proxy-K.

- **F-IS2**: Does the Zipf exponent of lesson citations in PRINCIPLES.md drift over time? Zipf exponent α > 1 means high concentration (few lessons monopolize citations); α → 1 means healthy diversification; α < 1 means flat distribution (all lessons equally cited = low signal). **Method**: compute citation counts at session marks S120, S140, S160, S180; fit power law rank-frequency curve; extract exponent α. **Prediction (B-IS2)**: exponent stays roughly constant (structural property of the corpus, not a drift phenomenon) — if it rises, concentration is increasing toward knowledge monoculture.

- **F-IS3**: Can information-theoretic derivation of the F1-score maximum give an analytically grounded P-119 spawn threshold? Current threshold (45% baseline improvement) is empirical. F1 = 2PR/(P+R) is maximized when the marginal precision cost of one more agent equals the marginal recall gain. **Method**: model precision as decreasing function of N (per-agent quality drops with N), recall as increasing function of N (coverage grows); find N* = argmax F1(N); compare with current P-119 heuristic. **Prediction (B-IS3)**: optimal N* is 2–4 for most tasks; matches observed spawn patterns; P-119 45% threshold corresponds to roughly N*=3 on typical tasks.

## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
