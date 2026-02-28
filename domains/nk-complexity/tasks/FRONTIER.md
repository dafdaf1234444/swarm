# NK Complexity Domain — Frontier Questions
Domain agent: write here, not to tasks/FRONTIER.md
Updated: 2026-02-27 | Active: 2

## Active

- **F75**: Does decompose-by-data outperform decompose-by-method for ALL task types? (L-051)
  Current evidence: confirmed for data-parallel analysis tasks. Untested: sequential reasoning, refactoring.
  **S305 NK evidence**: When K_avg < 1 (swarm knowledge graph = 0.77), method-level decomposition has no structural dependencies to exploit — decompose-by-data wins by default. Low-coupling systems are already data-parallel. Extends confirmed domain from code analysis to knowledge graphs.
  Status: **PARTIAL** — K_avg threshold identified (< 1 = data-parallel wins), but sequential reasoning and refactoring still untested.

- **F9-NK**: What additional knowledge domains should follow complexity theory?
  PARTIAL — complexity + distributed systems active. NK domain has 26 lessons, working tool (nk_analyze.py), cross-language support.
  **S305 self-analysis**: NK applied to swarm's own lesson citation graph (N=325, K_avg=0.77, 61.5% orphans, 0 cycles). Architecture: FRAGMENTED_ISLAND. L-378. Artifact: experiments/nk-complexity/f9-nk-self-analysis-s305.json.
  Open: apply NK to human's own codebases (HQ-2); measure K_avg over time to track compaction progress.

## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
| F36 | YES — applied NK to 5 real PyPI packages. B9 validated on 19 packages. | 39 | 2026-02-26 |
| F43 | YES — K_avg*N+Cycles is scale-invariant. Validated across 14 packages in 4 languages. | 38 | 2026-02-26 |
| F58 | YES — Express.js, Go net/http, Rust serde correctly ranked. B9 upgraded to observed. | 38 | 2026-02-26 |
| F79 | YES — cycle count primary maintenance burden predictor (rho=0.917). | 41 | 2026-02-26 |
| F82 | YES — 12/12 correct API shape classifications. | 42 | 2026-02-26 |
| F83 | YES — nk_analyze_go.py works. 7 Go projects tested. | 42 | 2026-02-26 |
| F85 | YES — LOC/N > 500 has 100% precision for monolith blind spots. | 42 | 2026-02-26 |
| F96 | YES — NK cycle count predicts EH quality in Python. | 45 | 2026-02-27 |
| F90 | ADDITIVE — function-level K_avg 2.4–27× higher than class-level; class finds 0 cycles in all 3 packages tested (logging, json, email), function finds 1–12; top-level functions are class-level's structural blind spot. P-166. L-174. | 81 | 2026-02-27 |
| F-NK4 | RESOLVED — K_dup and K_import are ORTHOGONAL. All 5 B9 packages: K_dup=0 regardless of K_import (1.0–104.0). Codebase maturity (script vs published lib) predicts K_dup, not import coupling. Within-module K_dup = "missing base class." @overload stubs must be filtered. L-178, P-165 revised. | 83 | 2026-02-27 |
