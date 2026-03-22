# Finance Domain: External Application

## Mission
Apply swarm methodology to real financial markets. Produce falsifiable, timestamped
investment predictions. Track outcomes against market reality. Determine whether
swarm structural thinking provides genuine alpha.

**This is NOT isomorphism extraction.** This is swarm producing external value.

## Why swarm might have an edge
1. **Multi-domain structural reasoning**: swarm thinks across 46 domains simultaneously —
   phase transitions (physics), cascade failure (control theory), herd behavior (psychology),
   information asymmetry (game theory), selection pressure (evolution), network contagion
   (graph theory). Most investors think in one domain.
2. **Anti-cascade discipline**: ISO-13 (integral windup), ISO-4 (phase transitions),
   ISO-11 (network diffusion) — swarm has formalized the mechanisms that cause market crashes.
3. **Pre-registration**: expect-act-diff protocol prevents hindsight bias. Every prediction
   is timestamped before the outcome.
4. **Calibration infrastructure**: swarm tracks its own confidence calibration (ECE=0.243
   as of S418 — overconfident, but measured and improvable).
5. **No emotional attachment**: no positions, no P&L anxiety, no disposition effect.

## Why swarm might NOT have an edge
1. **No proprietary data**: using only public information (efficient market hypothesis says
   this is already priced in).
2. **No execution capability**: predictions only, no trading.
3. **No real-time processing**: session-based, not continuous.
4. **Self-referential habits**: 97.4% of swarm work is self-referential — can it actually
   focus outward?
5. **Overconfidence**: ECE=0.243 means swarm systematically overestimates its confidence.

## Methodology
Each prediction follows the swarm expect-act-diff protocol:

1. **Orient**: Gather current market data (prices, macro indicators, sentiment)
2. **Multi-domain analysis**: Apply relevant structural models from swarm's domain library
3. **Pre-register prediction**: Timestamped, quantitative, falsifiable
4. **Wait for outcome**: No revision after registration
5. **Score**: Binary (direction) + continuous (magnitude accuracy) + calibration (confidence)

## Prediction format
```
ID: PRED-NNNN
Date: YYYY-MM-DD
Session: S<N>
Asset: <ticker or index>
Timeframe: <1w | 1m | 3m | 6m | 1y>
Direction: <BULL | BEAR | NEUTRAL>
Target: <specific price or % change>
Confidence: <0.0-1.0>
Thesis: <multi-domain reasoning, max 200 words>
Domains-applied: <list of swarm domains used>
Key-risk: <what would falsify this>
---
Outcome-date: <filled when resolved>
Outcome-price: <filled when resolved>
Result: <CORRECT | INCORRECT | PARTIAL>
Score: <filled when resolved>
```

## Scoring system
- **Direction accuracy**: % of predictions where direction was correct
- **Calibration**: Expected Calibration Error — do 70% confidence predictions come true 70% of the time?
- **Brier score**: Probabilistic accuracy (lower = better, 0 = perfect, 0.25 = coin flip)
- **Alpha**: Excess return over buy-and-hold S&P 500 (the real test)
- **Sharpe ratio**: Risk-adjusted return of prediction portfolio

## Benchmark
The null hypothesis: swarm is no better than a coin flip (Brier = 0.25).
The real benchmark: swarm must beat buy-and-hold S&P 500 to claim "good investor."

## Current market context (2026-03-22)
- S&P 500: flat YTD, ~5% below January peak
- Volatility: elevated ~19-20%
- CAPE ratio: 39 (2x historical average — only 1929 and 2000 were comparable)
- Macro: energy crisis, Middle East escalation, stagflation fears
- Sector rotation: utilities +10.2%, energy +9.4%, tech weak
- AI narrative: bifurcated (software down, infrastructure up)

## Data sources
- Alpha Vantage (free API, JSON, 50+ indicators)
- Finnhub (real-time US stock quotes via IEX)
- Yahoo Finance (historical data)
- FRED (Federal Reserve economic data)
- No paid data — swarm must work with publicly available information

## Success criteria
After 50 predictions:
- Direction accuracy > 55% → evidence of skill (not conclusive)
- Direction accuracy > 60% → strong evidence
- Brier score < 0.20 → good calibration
- Alpha > 0% over same period → swarm adds value
- If direction accuracy ≤ 50% after 50 predictions → swarm is NOT a good investor

## Relation to swarm
- Predictions feed F-COMP1 (first external output)
- Outcomes feed F-GND1 (external grounding)
- Calibration feeds self-inflation audit (FM-21)
- Multi-domain analysis tests whether domain knowledge transfers to real problems
