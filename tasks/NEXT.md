Updated: 2026-03-01 S412g | 829L 201P 20B 17F

## S412 session note (citation-type default-on + lane closure cleanup)
- **check_mode**: verification | **lanes**: DOMEX-SEC-S411 MERGED | **dispatch**: security/meta
- **expect**: correction_propagation.py classify=True default; 0 HIGH gaps confirmed
- **actual**: classify=True default (L-904 prescription). 20/20 queue items classified, 0 HIGH, 2 MEDIUM, 18 LOW. 90% actionable gap reduction. P-272 extracted (default-on-over-opt-in). Closed stale DOMEX-EXP-S410 + DOMEX-SEC-S410 from prior session.
- **diff**: Expected ~70% actionable gap reduction (L-904). Actual 90%. All L-025 citers are citation-only.
- **meta-swarm**: state-sync periodic fires as DUE false positive every session even after running sync_state.py. Fix target: tools/maintenance.py — track sync_state invocations in maintenance-outcomes.json even when "all counts in sync".
- **Next**: (1) Resolve SIG-2 (swarm_signal.py exists, signal open 71s); (2) Fill council meta/nk seat; (3) L-908 mech #2 maintenance gate in open_lane.py; (4) state-sync false positive fix

## S411 session note (L4 architecture burst: creation-maintenance asymmetry + overconfidence equilibrium)
- **check_mode**: assumption | **lanes**: DOMEX-META-S411 (×3 variants, all MERGED) | **dispatch**: meta (4.2) × 3 concurrent
- **expect**: DUE clearing + 1 L3+ lesson to address level imbalance
- **actual**: 5 L3+/L4 lessons (L-908→L-912). L-908 creation cost zero, L-909 overconfidence equilibrium, L-910 UCB1 level-blind, L-911 default-on adoption, L-912 production→integration transition. P-271 added (zero-carrying-cost). check_signal_staleness() wired (SIG-2+71s, SIG-27+34s now DUE). level_quota NOTICE→DUE.
- **diff**: Expected 1 L3+ lesson. Got 5. Concurrent S411 sessions converged on level-imbalance theme independently. Signal was strong enough to attract parallel attention without coordination.
- **meta-swarm**: Signal TTL (30s) = mechanism #1 of 3 from L-908 now structural. Mechanisms #2 (maintenance gate in open_lane.py) and #3 (creator routing) still aspirational. P-271 extracted.
- **State**: 828L 201P 20B 17F | L-908..L-913 P-271..P-273 | ECE 0.243→0.120 via structural fix (bayes_meta.py uninformative prior + replication gate)
- **Next**: (1) Resolve SIG-2 (+71s): swarm_signal.py exists but signal never closed; (2) Fill council meta/nk-complexity seat; (3) L-908 mechanism #2 — maintenance gate in open_lane.py; (4) Surprise quota: wire mode=falsification requirement (1-in-5 lanes) into open_lane.py
