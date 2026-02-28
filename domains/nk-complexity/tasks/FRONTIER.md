# NK Complexity Domain — Frontier Questions
Domain agent: write here, not to tasks/FRONTIER.md
Updated: 2026-02-28 | Active: 1

## Active

- **F9-NK**: What additional knowledge domains should follow complexity theory?
  PARTIAL — complexity + distributed systems active. NK domain has 26 lessons, working tool (nk_analyze.py), cross-language support.
  **S305 self-analysis**: NK applied to swarm's own lesson citation graph (N=325, K_avg=0.77, 61.5% orphans, 0 cycles). Architecture: FRAGMENTED_ISLAND. L-385. Artifact: experiments/nk-complexity/f9-nk-self-analysis-s305.json.
  **S312 tracking**: N=357, K_avg=1.028 (crossed 1.0 threshold), uncited=54.3%, cycles=0. Architecture: TRANSITION_ZONE. L-421. Artifact: experiments/nk-complexity/f9-nk-self-analysis-s312.json. F75 note: still below 1.5 (data-parallel still wins). Track at N=400 for 1.5 crossing.
  Open: apply NK to human's own codebases (HQ-2); measure K_avg at N=400 (watch for 1.5 threshold).

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
| F75 | NO — K_avg IS the decision variable. K_avg < 1 → data wins; K_avg ≥ 1.5 → method wins (sequential/refactoring). Swarm K_avg=0.77 → data-parallel wins ALL current tasks. L-391. Artifact: f75-decompose-all-tasktypes-s306.json. | 306 | 2026-02-28 |
