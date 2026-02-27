# NK Complexity Domain — Frontier Questions
Domain agent: write here, not to tasks/FRONTIER.md
Updated: 2026-02-27 | Active: 3

## Active

- **F75**: Does decompose-by-data outperform decompose-by-method for ALL task types? (L-051)
  Current evidence: confirmed for data-parallel analysis tasks. Untested: sequential reasoning, refactoring.

- **F-NK4**: Does copy-paste coupling (duplication K) predict different bugs than import-based K? L-143: `complexity_ising_idea` has K_avg=0 (imports) but 15-file duplication of `config_to_patch_states`. **S82 PARTIAL**: measured duplication K on investor (K_imp=123, K_dup=3) vs complexity_ising_idea (K_imp≈0, K_dup≈21+). Anti-correlation confirmed: explicit imports → low K_dup; K_dup siblings = missing abstractions. L-172. Remaining: test on larger B9 validation set, check bug correlation.

- **F9-NK**: What additional knowledge domains should follow complexity theory?
  PARTIAL — complexity + distributed systems active. NK domain has 26 lessons, working tool (nk_analyze.py), cross-language support.
  Open: apply NK to human's own codebases (see HUMAN-QUEUE HQ-2).

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
