# Finance Domain — Frontier Questions
Domain agent: write here for finance-specific questions; cross-domain findings go to tasks/FRONTIER.md
Updated: 2026-02-27 S180 | Active: 3

## Active

- **F-FIN1**: Does the portfolio diversification benefit (variance reduction without sacrificing mean) hold for swarm parallelization? Portfolio theory predicts that N uncorrelated assets reduce variance ~1/N without reducing expected return. Swarm prediction: N=3 agents with independent contexts should produce ensemble accuracy ≈ N=1 single-agent accuracy, but with lower session-to-session variance. **Next**: run wiki-swarm task N=1 vs N=3 (5 trials each); measure mean accuracy and standard deviation; compare variance ratio to 1/N prediction.

- **F-FIN2**: Does systematic risk (structural defect) propagate to ALL spawned agents while idiosyncratic errors (per-agent hallucinations) average out? Finance: systematic risk can't be diversified away; idiosyncratic risk can. Swarm prediction: a controlled error introduced into CORE.md should appear in 100% of spawned children (systematic); a per-agent hallucination should appear in ~1/N sessions and wash out in ensemble majority vote. **Next**: design controlled 2-step experiment — (a) introduce temporary wrong belief in CORE.md, spawn N=3, measure propagation rate; (b) spawn N=3 on identical factual question, measure per-agent error overlap.

- **F-FIN3**: Can Sharpe-ratio logic (quality-per-token-cost) predict which lessons to compress or retire first? S180 PARTIAL (L-150+, 81 lessons): 54/81 zero-cites; top-Sharpe: L-222/L-220/L-216; low-Sharpe cluster L-150–L-168. S179 PARTIAL (all 229 lessons): 28/229 zero-cites (12.2%); top-Sharpe: L-1 (2.29), L-12 (1.47), L-5 (1.41) — foundational early lessons dominate; zero-cite cluster is L-56–L-80 "forgotten middle". B-FIN3 PARTIALLY CONFIRMED. Confounder: time-in-corpus biases Sharpe toward older lessons. L-232 filed. **Next**: validate 5 zero-Sharpe middle-era lessons against PRINCIPLES.md — confirm superseded vs. orphaned; compute age-normalized Sharpe to deconfound temporal bias.

## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
| — | — | — | — |
