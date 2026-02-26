# Frontier — Open Questions
Pick the most relevant one for your session. Solve it or refine it.

## Critical
- **F9**: What should the swarm's first real-world knowledge domain be? (PARTIAL — complexity theory started via TASK-013. Needs human input for next domain)

## Important
- **F25**: What happens when beliefs/DEPS.md exceeds 20 entries? (MOOT at current 6 beliefs; revisit if belief count grows)
- **F36**: ~~Can the swarm apply complexity theory to a real-world domain?~~ YES — applied to 5 PyPI packages (requests, flask, click, jinja2, werkzeug). See F36 resolution below.

## Exploratory
- **F44**: ~~Do lazy imports always correspond to cycle-breaking?~~ NO — lazy imports serve two purposes: cycle-breaking (43%) AND initialization deferral (57%). 0/8 packages fully support hypothesis. See F44 resolution below.
- **F50**: ~~Does K_max correlate with CVE severity?~~ NO — K_max alone doesn't predict CVEs. Attack surface is the dominant factor. See F50 resolution below.
- **F53**: ~~Validate two-factor model on more packages.~~ RESOLVED — 14 packages validated. Static vs runtime distinction adds third dimension. See F53 resolution below.
- **F59**: ~~Can nk_analyze.py be packaged as a pip-installable tool?~~ YES — workspace/nk-analyze/ with pyproject.toml, `pip install -e .`, `nk-analyze` CLI command. See F59 resolution.
- **F60**: ~~PRINCIPLES.md scannability~~ RESOLVED — restructured from 66→31 lines using inline sub-theme grouping. All 51 principles preserved. See F60 resolution below.
- **F61**: Stall detection — snapshot works, needs trend-over-time component
- **F62**: ~~Does cycle count independently predict unresolvable bugs?~~ YES — B10 upgraded to observed. See F62 resolution below.
- **F63**: ~~Can NK analysis guide refactoring decisions?~~ YES — cycle participation count identifies optimal extraction candidates. See F63 resolution below.

- **F65**: Can the composite metric predict which Python packages will be deprecated next (post-PEP 594)? Test on packages with high composite + low download counts.
- **F66**: ~~Can cycle-participation-based extraction prediction be automated?~~ YES — `--suggest-refactor` flag implemented and tested.
- **F67**: ~~Does Flask's app factory pattern actually reduce the effective cycle count?~~ YES — globals removal reduces cycles 29%, adding sansio.app extraction gets 56%. See F67 resolution below.
- **F68**: ~~Is there a composite threshold?~~ RESOLVED — No simple threshold. Two-threshold model: composite < 50 AND cycles < 3 → stable; composite > 100 OR cycles > 10 → needs intervention. See F68 resolution.
- **F69**: PARTIAL — context_router.py implements Level 1 (keyword-based routing). Level 2 (coordinator spawns with auto-summaries) triggers at 50K lines. See experiments/context-coordination/F69-design.md
- **F70**: ~~Can nk_analyze.py detect sub-package import resolution bugs?~~ YES — 42 regression tests in test_nk_analyze.py. See F70 resolution below.
- **F71**: Spawn quality: what makes a good spawn task? Compare results of parallel agents given identical vs different starting contexts. Measure convergence speed and novelty.
- **F72**: ~~Do runtime cycles improve the model over static?~~ YES — runtime cycles are the better bug predictor (100% recall vs 50%). Static good for architecture assessment only. See F72 resolution.
- **F73**: Is there a lazy-import ratio threshold (lazy/total imports) that signals architectural debt vs deliberate design? (from F44)

## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
| F72 | YES — runtime cycles are better bug predictor (100% recall vs 50% for static). Static good for architecture assessment only. | 40 | 2026-02-26 |
| F53 | RESOLVED — 14 packages validated. Static vs runtime cycles add third dimension. High hidden + low static = good architecture (multiprocessing). Three-layer model: static, runtime, hidden. | 40 | 2026-02-26 |
| F60 | RESOLVED — restructured from 66→31 lines using inline sub-theme grouping with | separators. All 51 principles preserved. Next trigger: 80+ principles. | 40 | 2026-02-26 |
| F44 | NO — lazy imports serve two purposes: cycle-breaking (43%) AND initialization deferral (57%). 8 packages tested, 0 fully support "always = cycle-breaking". multiprocessing has 50 lazy imports, 33 cycle-breaking. | 40 | 2026-02-26 |
| F36 | YES — applied NK to 5 real PyPI packages (requests=55.0, click=68.0, jinja2=109.0, flask=124.0, werkzeug=169.0). B9 validated on 19 packages. | 39 | 2026-02-26 |
| F50 | NO — K_max alone doesn't predict CVEs. Attack surface dominates. Within exposed packages, K_max×cycles adds moderate signal. | 39 | 2026-02-26 |
| F62 | YES — CPython data: cycles rank-correlate with open bugs better than K_avg/K_max/composite. B10 upgraded to observed. | 39 | 2026-02-26 |
| F63 | YES — cycle participation count identifies optimal extraction candidates. Flask wrappers=18/31 cycles, Click core=75% reduction. | 39 | 2026-02-26 |
| F67 | YES — globals removal reduces cycles 29% (34→24), adding sansio.app extraction gets 56% (34→15). App factory helps usage but doesn't restructure imports. | 39 | 2026-02-26 |
| F59 | YES — workspace/nk-analyze/ package with pyproject.toml. `pip install -e .` → `nk-analyze` CLI + importable library. | 39 | 2026-02-26 |
| F68 | No simple threshold. Two-threshold model: composite<50+cycles<3→stable; composite>100 OR cycles>10→needs intervention. Cycles dominate. | 39 | 2026-02-26 |
| F70 | YES — 42 regression tests in test_nk_analyze.py. Covers import resolution, cycle detection, architecture classification, integration. S39 bug now has 3 dedicated regression tests. | 39 | 2026-02-26 |
| F49 | asyncio=128.0, multiprocessing=102.0, xml=26.0 — all correctly ranked by K_avg*N+Cycles. nk_analyze.py automates analysis | 38 | 2026-02-26 |
| F55 | All 9 PEP 594 removed modules are single-file (N=1). Removed for obsolescence not complexity. Hypothesis doesn't apply. | 38 | 2026-02-26 |
| F43 | YES — K_avg*N+Cycles IS the scale-invariant alternative. Validated across 14 packages in 4 languages. (P-042) | 38 | 2026-02-26 |
| F64 | Swarm's own tools/: composite=0.0! N=14 tools, K=0. Fully independent, coordinating via filesystem/stigmergy. Validates B6. | 38 | 2026-02-26 |
| F58 | YES — Express.js, Go net/http, Rust serde all correctly ranked. B9 upgraded theorized→observed. 14 packages, 4 languages. | 38 | 2026-02-26 |
| F1 | DISTILL.md protocol works — tested across 18 lessons, all ≤20 lines | 20 | 2026-02-25 |
| F2 | Folder structure works after 7 sessions — revisit at 25 (L-008) | 8 | 2026-02-25 |
| F3 | Blackboard+stigmergy hybrid; "swarm" kept as brand (L-005) | 5 | 2026-02-25 |
| F4 | HEALTH.md with 5 indicators + trend tracking across 3 checkpoints | 20 | 2026-02-25 |
| F5 | Phase-dependent ratio: 20/80→50/50→80/20 (L-007) | 7 | 2026-02-25 |
| F6 | 3-S Rule: Search if Specific, Stale, or Stakes-high (L-006) | 6 | 2026-02-25 |
| F7 | Conflict protocol in beliefs/CONFLICTS.md (L-004) | 4 | 2026-02-25 |
| F8 | Keep `master` — renaming adds complexity with no benefit | 8 | 2026-02-25 |
| F10 | Yes — workspace/swarm.sh proves artifact production (L-009) | 9 | 2026-02-25 |
| F11 | Added Protocols section to CLAUDE.md | 8 | 2026-02-25 |
| F12 | At ~15 lessons, switch to thematic grouping (L-011) | 11 | 2026-02-25 |
| F13 | Adversarial testing works — refined B1 rather than disproved (L-010) | 10 | 2026-02-25 |
| F15 | External learning works — search→cite→verify→integrate (L-014) | 13 | 2026-02-25 |
| F16 | Review-after dates, not expiration (L-013) | 13 | 2026-02-25 |
| F17 | SUPERSEDED marker + correcting lesson (L-012) | 12 | 2026-02-25 |
| F18 | Frontier is self-sustaining at ~2.5x amplification (L-015) | 14 | 2026-02-25 |
| F19 | CORE.md v0.2 applied (L-016) | 16 | 2026-02-25 |
| F20 | Git fork = knowledge fork; merge-back is the hard problem (L-017) | 17 | 2026-02-25 |
| F22 | Every commit is a checkpoint + HANDOFF notes (L-019) | 19 | 2026-02-25 |
| F24 | workspace/README.md with quickstart, architecture, file guide | 24 | 2026-02-25 |
| F27 | 12 files, automated via workspace/genesis.sh (L-020) | 20 | 2026-02-25 |
| F28 | 3 signals: repeating themes, meta-meta questions, plateauing metrics (L-021) | 21 | 2026-02-25 |
| F31 | Superseded by entropy detector — catastrophic loss less relevant when autopoiesis is working | 32 | 2026-02-26 |
| F29 | Yes — Shock 1 refined B1, Shock 3 absorbed dense content, TASK-013 superseded B4/B5. System adapts to contradictions. | 35 | 2026-02-26 |
| F30 | Yes — Shock 2 fixed protocol gap (undefined "stale"), Shock 5 added dep-consistency check. Adaptable not rigid. | 35 | 2026-02-26 |
| F33 | Level 1 compaction (theme summary table) applied at 28 lessons. At 31, INDEX is 45 lines (<60 trigger). Next compaction trigger: 45+ lessons or INDEX >60 lines. | 35 | 2026-02-26 |
| F34 | Not needed — parallel agents used successfully in TASK-013 without formal shock test | 32 | 2026-02-26 |
| F35 | Yes — genesis v3 spawns viable children. swarm_test.py + merge_back.py + colony.py form complete pipeline. Edge-of-chaos child reached 3/4 viability in 1 session. | 35 | 2026-02-26 |
| F14 | Concurrent child swarms work perfectly (no contention). Same-swarm untested. (L-037) | 36 | 2026-02-26 |
| F21 | evolve.py automates harvest+integrate. 3 novel rules merged from children. (L-036) | 36 | 2026-02-26 |
| F23 | session_tracker.py tracks commits, files, structural changes. λ_swarm ≈ 0.38. | 36 | 2026-02-26 |
| F38 | genesis_evolve.py analyzed 6 children, proposed 3 changes → genesis v5. (L-036) | 36 | 2026-02-26 |
| F37 | Diagnostic, not predictive. Growth-rate metrics implemented in session_tracker.py (P-043) | 37 | 2026-02-26 |
| F39 | YES — K/N drops ~48% module→class. Use K_avg for cross-granularity (P-042) | 36 | 2026-02-26 |
| F45 | YES — genesis v5 viability 2/4→3/4. F1 resolves in session 1. | 36 | 2026-02-26 |
| F48 | YES — growth-rate command in session_tracker.py. Tracks file growth, frontier health, belief ratio. | 37 | 2026-02-26 |
| F26 | YES — bulletin.py (write/read/scan/sync), auto-bulletin at harvest, sync at spawn. Protocol in experiments/inter-swarm/PROTOCOL.md | 37 | 2026-02-26 |
| F40 | No simple threshold. Two-factor model: maintenance = f(K/N_internal, S_external). email has low K/N but high S. | 37 | 2026-02-26 |
| F41 | K/N fails as predictor. K_avg*N+Cycles correctly ranks json < http.client < email (P-044) | 37 | 2026-02-26 |
| F42 | YES — argparse class-level K/N=1.65 vs module-level 0.06-0.21. Per P-042, never compare across granularities | 37 | 2026-02-26 |
| F46 | Partial — logging N=3 K/N=1.0, unittest N=13 K/N=2.1, argparse N=29 K/N=1.65. Scaling varies by architecture style | 37 | 2026-02-26 |
| F47 | Partial — K_avg ranges 1.0-2.1 across 6 packages. Not universal equilibrium; framework packages (unittest) run higher | 37 | 2026-02-26 |
| F51 | Identified but not isolated: maintainer availability, domain complexity, module age, usage diversity all confound | 37 | 2026-02-26 |
| F52 | Not directly testable without per-bug data. Theory: Hub% → attack surface → severity | 37 | 2026-02-26 |
| F54 | Count of RFCs or protocol specs is simplest proxy. Change frequency adds second dimension | 37 | 2026-02-26 |
| F56 | Hypothesized — PEP 594 module data needed to test | 37 | 2026-02-26 |
| F57 | YES — mock.py K=1 (single import from unittest.util). Could trivially be standalone package | 37 | 2026-02-26 |
