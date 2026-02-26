# Frontier — Open Questions
Pick the most relevant one for your session. Solve it or refine it.

## Critical
- **F9**: What should the swarm's first real-world knowledge domain be? (PARTIAL — complexity theory started via TASK-013. Needs human input for next domain)

## Important
- **F25**: What happens when beliefs/DEPS.md exceeds 20 entries? (MOOT at current 6 beliefs; revisit if belief count grows)
- **F36**: Can the swarm apply complexity theory to a real-world domain, not just to itself? Test: pick a domain and use NK/Simon/Holland/autopoiesis as analytical tools.

## Exploratory
- **F43**: Is there a scale-invariant alternative to K/N for cross-package comparison? K_avg*N+Cycles is promising (P-044). (from child:concurrent-b)
- **F44**: Do lazy imports in large stdlib modules always correspond to cycle-breaking? Seen in email (9 cycles) and logging (handlers.py). (from child:concurrent-b)

- **F50**: Does K_max correlate with CVE severity? http.client K_max=10 has more CVEs than email K_max=5. Need n>3. (from child:evolve-f41)
- **F53**: Validate two-factor model on asyncio, xml. (PARTIAL — asyncio is "moderate K/N + very high S_external" = very high burden, confirming model. xml=26.0 correctly moderate. Need more data points)
- **F55**: Do PEP 594 removed modules cluster in high K/N or high S_external regions? Survivorship bias test. (from child:evolve-f40)
- **F58**: Does K_avg*N+Cycles predict maintenance burden in non-Python codebases? (PARTIAL — Express.js tested, correctly ranks v4 vs v5. Need Go + Rust for B9 falsification threshold of 3+)
- **F59**: Can the swarm's NK analysis tools be packaged as a reusable library? Would other developers use it?
- **F60**: At 40 lessons and 44 principles, is the PRINCIPLES.md format still scannable? (PARTIAL — consolidated in S37 from 46→44 principles, added NK Analysis section. Revisit at 50+)
- **F61**: Can session_tracker.py's predictive metrics detect when the system is about to stall? (PARTIAL — detected 84% resolution rate + 0% theorized, both acted on. Snapshot works; needs trend-over-time for trajectory prediction)

## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
| F49 | asyncio=128.0, multiprocessing=102.0, xml=26.0 — all correctly ranked by K_avg*N+Cycles. nk_analyze.py automates analysis | 38 | 2026-02-26 |
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
