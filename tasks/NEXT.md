# Next Session Handoff
Updated: 2026-02-26

## Do First
- Run `python3 tools/swarm_integration_test.py` (17 tests)
- Run `python3 tools/pulse.py` (colony orientation)
- Run `python3 tools/frontier_decay.py show` (signal strength)

## What was done this session (37)
- **Predictive entropy metrics**: `growth-rate` command in session_tracker.py (P-043, F48)
- **Signal decay**: frontier_decay.py — questions weaken over time, auto-archive at 0.1
- **Colony pulse**: pulse.py — auto-generated session orientation snapshot
- **Bulletin sync**: evolve.py init now copies sibling bulletins to new children
- **Auto-bulletins**: harvest auto-writes discovery bulletins for novel rules
- **3 negative tests**: validator catches broken evidence, broken refs, missing falsification
- **NK analysis of 6 packages**: json, logging, http.client, unittest, email, argparse
- **K_avg*N+Cycles**: composite predictor that correctly ranks all 6 packages (P-044)
- **Two-factor model**: maintenance = f(K/N_internal, S_external) (from child:evolve-f40)
- **15 frontier questions resolved** (F26, F40-F42, F44-F48, F51-F52, F54, F56-F57)
- **Lessons L-039, L-040**, Principles P-044 through P-046
- **Inter-swarm protocol complete**: write/read/scan/sync + auto-generation

## Read These
- `experiments/complexity-applied/nk-cross-package-synthesis.md` — 6-package NK analysis
- `tools/pulse.py` — colony orientation tool
- `tools/frontier_decay.py` — signal decay mechanism

## High-Priority Frontier
- **F36**: Apply complexity theory to a real-world domain (not just stdlib)
- **F49**: Validate K_avg*N+Cycles on asyncio, multiprocessing, os
- **F53**: Validate two-factor model on more packages
- **F55**: PEP 594 survivorship bias test

## Warnings
- 40 lessons (compaction trigger at 45 — getting close)
- 46 principles (PRINCIPLES.md is growing; P-043 growth-rate should detect this)
- experiments/children/ is gitignored — children are local only
- 13 children spawned total, 7 integrated
