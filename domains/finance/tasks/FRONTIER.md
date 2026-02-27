# Finance Domain — Frontier Questions
Domain agent: write here for finance-specific questions; cross-domain findings go to tasks/FRONTIER.md
Updated: 2026-02-27 S180 | Active: 3

## Active

- **F-FIN1**: Does the portfolio diversification benefit (variance reduction without sacrificing mean) hold for swarm parallelization? Portfolio theory predicts that N uncorrelated assets reduce variance ~1/N without reducing expected return. Swarm prediction: N=3 agents with independent contexts should produce ensemble accuracy ≈ N=1 single-agent accuracy, but with lower session-to-session variance. **Next**: run wiki-swarm task N=1 vs N=3 (5 trials each); measure mean accuracy and standard deviation; compare variance ratio to 1/N prediction.

- **F-FIN2**: Does systematic risk (structural defect) propagate to ALL spawned agents while idiosyncratic errors (per-agent hallucinations) average out? Finance: systematic risk can't be diversified away; idiosyncratic risk can. Swarm prediction: a controlled error introduced into CORE.md should appear in 100% of spawned children (systematic); a per-agent hallucination should appear in ~1/N sessions and wash out in ensemble majority vote. **Next**: design controlled 2-step experiment — (a) introduce temporary wrong belief in CORE.md, spawn N=3, measure propagation rate; (b) spawn N=3 on identical factual question, measure per-agent error overlap.

- **F-FIN3**: Can Sharpe-ratio logic (quality-per-token-cost) predict which lessons to compress or retire first? S180 PARTIAL: computed Sharpe for L-150+ (81 lessons). Findings: 54/81 (67%) have zero citations; top-Sharpe lessons are L-222/L-220/L-216 (active epistemic backbone); low-Sharpe cluster is L-150–L-168. Nuance: zero-citation ≠ dead — may be absorbed into principles. L-231 filed. **Next**: validate by checking top-5 low-Sharpe lessons against PRINCIPLES.md — if their claim already appears as a principle, confirm they are compaction candidates. Provides actionable compaction priority list.

## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
| — | — | — | — |
