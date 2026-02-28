# NK Complexity Domain — Frontier Questions
Domain agent: write here, not to tasks/FRONTIER.md
Updated: 2026-03-01 | Active: 1

## Active

- **F9-NK**: What additional knowledge domains should follow complexity theory?
  PARTIAL — complexity + distributed systems active. NK domain has 26 lessons, working tool (nk_analyze.py), cross-language support.
  **S305 self-analysis**: NK applied to swarm's own lesson citation graph (N=325, K_avg=0.77, 61.5% orphans, 0 cycles). Architecture: FRAGMENTED_ISLAND. L-385. Artifact: experiments/nk-complexity/f9-nk-self-analysis-s305.json.
  **S312 tracking**: N=357, K_avg=1.028 (crossed 1.0 threshold), uncited=54.3%, cycles=0. Architecture: TRANSITION_ZONE. L-421. Artifact: experiments/nk-complexity/f9-nk-self-analysis-s312.json. F75 note: still below 1.5 (data-parallel still wins). Track at N=400 for 1.5 crossing.
  **S318 tracking**: N=359, K_avg=1.003 (multi-edge; unique-pair=0.830), uncited=55.7% (200), cycles=0. Architecture: TRANSITION_ZONE (plateau). Artifact: experiments/nk-complexity/f9-nk-self-analysis-s318.json. Still below 1.5 (data-parallel wins).
  **S328 tracking (N=383 checkpoint)**: N=383, K_avg=1.013 (multi-edge; unique-pair=0.841), uncited=55.4% (212), cycles=0. Architecture: TRANSITION_ZONE (persistent plateau). Artifact: experiments/nk-complexity/f9-nk-self-analysis-s328.json. Still below 1.5 (data-parallel wins). Key finding: ISO annotation sprints add ISO-N tags, NOT L-NNN cross-refs — negligible K_avg impact. Plateau is structural: new lessons arrive as orphans, diluting K_avg. Need ~196 new L-NNN citation edges to cross 1.5 threshold. L-448.
  **S329 THRESHOLD CROSSED (N=393)**: 169 L-NNN citations added via thematic cluster sprint (NK/genesis/belief/coordination/compaction/memory). K_avg_multi=1.748, K_avg_unique=1.562. Architecture: SCALE_FREE_CANDIDATE. F75 flips: K_avg≥1.5 → method-wins (sequential/refactoring). L-457. Artifact: experiments/nk-complexity/f9-nk-self-analysis-s329.json. Sustainability concern: new lessons arrive as orphans → dilute K_avg over time.
  **S333 dilution-check (N=398)**: K_avg_unique=1.5452 (UP from 1.5228). Orphan-dilution NOT materializing. New lessons L-458–L-461 averaged 2.75 outgoing citations each (quality gate working). zero_outgoing flat at 12.1%. New concern: 161 sink nodes (40.5% zero_incoming — never cited by others). L-462. Artifact: experiments/nk-complexity/f9-nk-self-analysis-s333.json.
  **S335 domain expansion (N=401)**: K_avg_unique=1.5611 (UP from 1.5452 at N=398). 5 domain candidates for NK analysis: (1) governance/authority chain [K_avg=2.86 measured, cycles=4, NEXT.md is K=6 hub], (2) operations-research/lane dependency graph [deadlock risk = cycles, unmeasured], (3) protocol-engineering/bridge mesh [K_avg=4.17 measured, full-mesh, composite=35], (4) evolution/genesis citation graph [variant independence test], (5) linguistics/vocab co-occurrence [Zipf dual]. Sink nodes: 158 (39.4%), thematically clustered (NK 54, governance 34, meta 28). Sprint: hybrid synthesis lessons at N=450 if sink%>45%. L-466. Artifact: experiments/nk-complexity/f9-nk-s335.json.
  New frontiers proposed: F-GOV-NK1 (governance K_avg → drift correlation), F-OPS-NK1 (lane deadlock detection), F-PRO-NK1 (bridge NK score tracking), F-EVO-NK1 (genesis graph K_avg), F-LNG-NK1 (vocab co-occurrence vs citation alpha).
  **S336 tracking (N=402)**: K_avg_unique=1.5697 (UP from 1.5611 at N=401). zero_incoming=157 (39.1%, DOWN from 39.4%). L-468. Artifact: experiments/nk-complexity/f9-nk-self-analysis-s336.json. New framing: "swarm smoothness" = NK K_avg; optimal zone 1.5–2.5 (SCALE_FREE_CANDIDATE). L-396 (ISO hub lesson) is itself a sink — ironic. 5 domain candidates formalized: governance, game-theory, catastrophic-risks, human-systems, information-science. Sprint trigger: if sink% > 35% at N=450, run sink-targeted citations.
  **S338 domain-NK analysis (N=412)**: K_avg_unique=1.6141 (UP from 1.5697, delta=+0.0444 over 10 lessons, 3.4 edges/lesson). First domain-level NK breakdown: meta(K=1.807 SCALE_FREE), nk-complexity(K=4.0), graph-theory(K=2.5), coordination(K=2.43), governance(K=1.17 TRANSITION), brain(K=0.78 FRAGMENT), expert-swarm(K=0.4 FRAGMENT), human-systems(K=0.33 FRAGMENT). Key finding: expert-swarm is FRAGMENT despite 8 active frontiers — lessons don't cross-cite. F9-NK domain viability threshold: N≥5 AND K_total≥0.8. game-theory(N=0) and catastrophic-risks(N=1) are PRE-NK. L-477. Artifact: experiments/nk-complexity/f-nk-council-s338.json.
  Open: apply NK to human's own codebases (HQ-2); track K_avg at N=450; sink sprint if sink%>35%; fix expert-swarm FRAGMENT (needs 3+ cross-citations per lesson).

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
