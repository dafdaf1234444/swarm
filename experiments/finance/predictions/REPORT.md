# Swarm Investor — Prediction Report

Generated: 2026-03-22 19:40 | Total: 5 | Open: 5 | Resolved: 0

## Scorecard

*No predictions resolved yet. First resolution due: 2026-04-21*

## Active Predictions

### PRED-0003: ▲ BULL TLT [OPEN (29d)]

| Field | Value |
|-------|-------|
| Date | 2026-03-22 |
| Target | +3% to +8% from current |
| Timeframe | 1m |
| Confidence | ████░░░░░░ 40% |
| Resolve by | 2026-04-21 |
| Domains | physics, control-theory, psychology, statistics |
| Key risk | Inflation spikes further, forcing Fed hawkish — yields rise, TLT falls |

**Confidence adjusted after backtest:**
- 55% (2026-03-22): initial
- 40% (2026-03-22): backtest: 2022 TLT -31% during stagflation; current regime resembles 2022 not 2020; yields RISING despite equity weakness

**Thesis:** 10Y just breached 4% floor (4.39%) — flight to safety is beginning. ISO-4 phase transition: when equity risk-off accelerates, bonds become the attractor. Historical: in 7 of 8 major equity drawdowns since 1970, long bonds rallied within 30 days of the equity low. Psychology: fear regime shift from greed to fear drives capital rotation to safety. Control theory: Fed is in a bind (stagflation = can't cut OR hike) — policy paralysis favors bonds short-term. Confidence only 0.55 because stagflation is the one scenario where bonds DON'T rally (1970s analog).

---

### PRED-0001: ▼ BEAR SPY [OPEN (89d)]

| Field | Value |
|-------|-------|
| Date | 2026-03-22 |
| Target | -5% to -10% from current ~648 |
| Timeframe | 3m |
| Confidence | ██████░░░░ 60% |
| Resolve by | 2026-06-20 |
| Domains | physics, control-theory, finance, history, psychology |
| Key risk | Fed pivot or ceasefire in Middle East reverses energy shock |

**Thesis:** CAPE at 39 is 2x historical avg — only 1929 and 2000 were comparable (ISO-4 phase transition). Oil shock from Strait of Hormuz closure propagates through economy with ~6-12mo lag (ISO-11 network diffusion). Stagflation fears suppress both growth and value — no safe haven in equities. Rising 10Y yield (4.39%) tightens financial conditions while economy weakens. Historical base rate: CAPE>35 + oil shock → negative 3mo return ~65% of time. Sector rotation to utilities/energy signals defensive positioning (ISO-2 selection). Swarm calibration note: confidence 0.60 not higher because EMH says this is mostly priced in.

---

### PRED-0002: ▲ BULL XLE [OPEN (89d)]

| Field | Value |
|-------|-------|
| Date | 2026-03-22 |
| Target | +5% to +15% from current |
| Timeframe | 3m |
| Confidence | █████░░░░░ 55% |
| Resolve by | 2026-06-20 |
| Domains | physics, evolution, game-theory, control-theory |
| Key risk | Ceasefire reopens Hormuz, oil drops below 75, energy sector reverts |

**Confidence adjusted after backtest:**
- 65% (2026-03-22): initial
- 55% (2026-03-22): backtest: 2008 XLE -66% during demand destruction; recession risk underweighted

**Thesis:** Energy sector (XLE) already +9.4% while broad market flat — but the structural driver (Hormuz closure, Iran war) is ESCALATING not resolving. ISO-13 integral windup: oil inventory drawdown accumulates without discharge mechanism. Game theory: neither Iran nor coalition has incentive to de-escalate given current payoffs. Evolution lens: energy companies are the 'fit' organisms in stagflation — pricing power + real assets. Control theory: energy is the only sector with positive feedback loop from current macro (higher oil → higher revenue → higher stock).

---

### PRED-0004: ▲ BULL GLD [OPEN (89d)]

| Field | Value |
|-------|-------|
| Date | 2026-03-22 |
| Target | +5% to +12% from current |
| Timeframe | 3m |
| Confidence | ███████░░░ 70% |
| Resolve by | 2026-06-20 |
| Domains | history, game-theory, physics, psychology, distributed-systems |
| Key risk | Strong dollar rally crushes gold despite macro tailwinds |

**Thesis:** Gold is the consensus safe haven in every historical analog to current conditions: (1) geopolitical war escalation, (2) stagflation fears, (3) loss of confidence in monetary policy, (4) CAPE extreme. ISO-8 power law: gold tends to move in explosive bursts, not gradual trends — current conditions are the preconditions for a burst. Game theory: central banks globally diversifying away from USD reserves (confirmed by BIS data). Distributed systems lens: gold is the decentralized store of value — network effects strengthen during centralized-system stress. Highest confidence prediction because multiple independent structural drivers converge.

---

### PRED-0005: ▼ BEAR QQQ [OPEN (89d)]

| Field | Value |
|-------|-------|
| Date | 2026-03-22 |
| Target | -8% to -15% from current |
| Timeframe | 3m |
| Confidence | ██████░░░░ 60% |
| Resolve by | 2026-06-20 |
| Domains | evolution, physics, control-theory, information-science, psychology |
| Key risk | AI narrative re-accelerates with major product launch, tech leads recovery |

**Thesis:** Nasdaq 100 plunged 1.8% to 6-month lows — AI narrative bifurcating (software DOWN, infrastructure UP). ISO-2 selection: market is discriminating between AI hype and AI substance. Phase transition: tech leadership regimes last ~7-10 years (2013-2024 was tech's run); rotation to energy/utilities/value signals regime change. Control theory: higher rates disproportionately hurt long-duration growth assets (tech). Information theory: AI software companies have high information asymmetry — market can't distinguish real AI revenue from hype — so it sells all. Bear case slightly stronger than SPY because QQQ has higher CAPE + more rate sensitivity + AI narrative reversal.

---

## Methodology

Each prediction uses multi-domain structural analysis from the swarm's
46-domain knowledge base. Predictions are pre-registered (timestamped before
outcome), quantitative, and falsifiable. Historical backtesting grounds each
thesis against real market data, including failure cases.

The question being tested: **Can a collective intelligence system that reasons
across physics, game theory, evolution, psychology, and control theory produce
investment predictions that beat a coin flip?**

Full backtest: `experiments/finance/predictions/BACKTEST.md`
Registry tool: `python3 tools/market_predict.py score`

