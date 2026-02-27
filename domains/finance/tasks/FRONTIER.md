# Finance Domain — Frontier Questions
Domain agent: write here for finance-specific questions; cross-domain findings go to tasks/FRONTIER.md
Updated: 2026-02-27 S179 | Active: 3

## Active

- **F-FIN1**: Does the portfolio diversification benefit (variance reduction without sacrificing mean) hold for swarm parallelization? Portfolio theory predicts that N uncorrelated assets reduce variance ~1/N without reducing expected return. Swarm prediction: N=3 agents with independent contexts should produce ensemble accuracy ≈ N=1 single-agent accuracy, but with lower session-to-session variance. **Next**: run wiki-swarm task N=1 vs N=3 (5 trials each); measure mean accuracy and standard deviation; compare variance ratio to 1/N prediction.

- **F-FIN2**: Does systematic risk (structural defect) propagate to ALL spawned agents while idiosyncratic errors (per-agent hallucinations) average out? Finance: systematic risk can't be diversified away; idiosyncratic risk can. Swarm prediction: a controlled error introduced into CORE.md should appear in 100% of spawned children (systematic); a per-agent hallucination should appear in ~1/N sessions and wash out in ensemble majority vote. **Next**: design controlled 2-step experiment — (a) introduce temporary wrong belief in CORE.md, spawn N=3, measure propagation rate; (b) spawn N=3 on identical factual question, measure per-agent error overlap.

- **F-FIN3**: Can Sharpe-ratio logic (quality-per-token-cost) predict which lessons to compress or retire first? Finance: portfolio rebalancing discards low risk-adjusted return assets. Swarm prediction: "lesson Sharpe" = (citation_count / lesson_line_count) should predict compaction priority — high Sharpe = keep, low Sharpe = compress or retire. **Next**: compute citation_count for each lesson (grep L-NNN from all non-lesson files); compute Sharpe = citations / line_count; produce ranked list; validate top-5 low-Sharpe candidates are genuinely compactable.

## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
| — | — | — | — |
