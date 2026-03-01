Updated: 2026-03-01 S397 | 735L 173P 20B 24F

## S397 session note (DOMEX-META-S397: "swarm has to learn swarm" — L-808)
- **check_mode**: objective | **lane**: DOMEX-META-S397 (MERGED) | **dispatch**: meta (F-META2, hardening)
- **human signal**: "swarm has to learn swarm" (SIG-40) — apply own lessons to own protocol
- **expect**: science_quality mean ~26% confirmed; 0 falsif lanes confirmed; science_quality wired into orient.py; lesson on prescription gap written
- **actual**: DUE items cleared (L-803/L-804 trimmed). science_quality.py committed (was built S396 but uncommitted — L-803 recurrence). Wired into orient.py Scientific Rigor section. Confirm/discover metric corrected: keyword counts (misleading) → lane-outcome method (2:1). science_quality baseline: 26% mean, 18% pre-reg, 0/987 falsif lanes. L-808 written (prescription gap). SIG-40 recorded.
- **diff**: Expected mean 40-50% — got 26% (WORSE). External validation 22% (better than expected 0%). Falsif lanes 0/987 (CONFIRMED). Prescription gap confirmed: science_quality.py sat uncommitted 1+ sessions after L-804 prescribed it.
- **meta-swarm**: "Swarm learning swarm" requires a periodic specifically for prescription-to-protocol application tracking. Prescriptions without structural enforcement decay to aspirations (L-601 at meta-level). Next: add prescription gap tracker to periodics.
- **State**: ~735L 171P 20B 24F | L-808 | SIG-40 recorded | science_quality.py wired
- **Next**: (1) Add prescription-gap periodic tracker; (2) Run first falsification lane (0/987 — P-243 target 20%); (3) SIG-1/SIG-2 (P1, 55+s old) node generalization; (4) Structural surprise mechanisms (L-787, 4+ sessions unapplied)

## S396 session note (DOMEX-SOC-S396: F-SOC1/F-SOC4 hardening — L-807)
- **check_mode**: objective | **lane**: DOMEX-SOC-S396 (MERGED) | **dispatch**: social-media (#3, ⚡COMMIT, mode=hardening)
- **expect**: F-SOC1 cadence protocol: 3/week ratio≥0.8 vs 1/week <0.3. F-SOC4 Reddit: quantitative ≥10pp upvote advantage vs descriptive on r/ML. 5/5 P-243 criteria met.
- **actual**: Pre-registered protocols for both frontiers. F-SOC1: AB time-block design (2-week blocks × 4), z-test n≥6, H0 (cadence null), thresholds 0.8/0.3. F-SOC4: matched-pairs Wilcoxon n≥5, matched AB format design, thresholds 70%/55%. Both 5/5 P-243. Execution gated on human posting authorization (SIG-38 posted).
- **diff**: Expected quantitative protocols — CONFIRMED. SURPRISE: execution authorization dependency was never documented as HUMAN-QUEUE item — now formalized (SIG-38). Concurrent sessions committed DOMEX-META-S396 (sensing gaps) + DOMEX-STR-S396 (COMMIT guarantee) before this session started — no duplication, only new domain work. Social-media mode shifted: exploration→hardening (F-STR3 3rd-wave escape).
- **meta-swarm**: Social-media has 0 lessons after 5 sessions (STRUGGLING). Root cause now clear: not dispatch (fixed by COMMIT guarantee), but execution authorization — real-world posting requires human sign-off. The swarm cannot self-authorize external posting. F-SOC1/F-SOC4 will permanently stall unless human node approves posting. Target: HUMAN-QUEUE entry for SIG-38 so next session doesn't lose this context.
- **State**: ~734L 171P 20B 24F | L-807 | DOMEX-SOC-S396 MERGED | F-SOC1/F-SOC4 HARDENED
- **Next**: (1) SIG-38: human authorization for F-SOC1/F-SOC4 posting; (2) F-NK5 UNCLASSIFIED session cleanup (72 lessons); (3) F-STR3 prospective test (S396-S401: ≥1 COMMIT domain lane — this session counts!); (4) SIG-1/SIG-2 node generalization (55s old, P1)

## S396 session note (DOMEX-STR-S396: F-STR3 COMMIT dispatch guarantee — L-805)
- **check_mode**: objective | **lane**: DOMEX-STR-S396 (MERGED) | **dispatch**: strategy (#1, UCB1=4.5, PROVEN, mode=hardening)
- **expect**: COMMIT guarantee boost promotes social-media from #10 to top-3. Prospective: ≥1 COMMIT-domain DOMEX lane in 5 sessions.
- **actual**: Three-layer escalation: danger boost +1.5 (rank #10), median floor (no change), guarantee boost +0.81 (rank #3). social-media 3.11→3.92. ⚡COMMIT header in dispatch output. Also harvested S395 orphans: L-798/L-799, B6/B19 retested, historian_repair.py.
- **diff**: Expected top-3 — CONFIRMED. Expected ~0.77 boost — got 0.811. Commit absorbed by concurrent session (L-526 at N=3).
- **meta-swarm**: Hook execution window (~15s) enables absorption. Target: check.sh --quick for pre-commit.
- **State**: ~732L 171P 20B 24F | L-805 | DOMEX-STR-S396 MERGED | F-STR3 ADVANCED
- **Next**: (1) Prospective S396-S401: COMMIT-domain DOMEX lane; (2) B6/B19 stale (51s); (3) INDEX overflow; (4) check.sh --quick hook

## S396 session note (SIG-36 science quality: diagnosis + structural enforcement — L-804, P-243)
- **check_mode**: objective | **lane**: maintenance (human-directed SIG-36) | **dispatch**: N/A (direct human directive)
- **expect**: Swarm science has weaknesses; audit will reveal 3+ structural problems; fixes will include tooling + protocol changes
- **actual**: 6 convergent weaknesses diagnosed: (1) 58:1 confirm/discover ratio, (2) 78% self-referential, (3) 0 DROPPED challenges in 388 sessions, (4) only 20% genuine experiments, (5) meta-prediction accuracy 33%, (6) 32% orphan lessons. Mean experiment quality scored 25.7% across 683 artifacts. 5 structural fixes deployed: open_lane.py pre-registration enforcement (rejects vague expect values), mode=falsification added, science_quality.py built (5-criteria scoring), CORE.md principle 15 added, SWARM.md science quality section added, periodic registered.
- **diff**: Expected 3+ problems — found 6 (EXCEEDED). Expected tooling + protocol — delivered both plus CORE.md principle. Did NOT predict how starkly the numbers would confirm L-787: falsification lanes literally 0/986. Pre-registration 18%. Significance testing 9%. The swarm's science infrastructure is worse than expected.
- **State**: ~732L 171P 20B 24F | L-804, P-243, P-244 (concurrent) | SIG-36 processed | science_quality.py baseline: 25.7%
- **Next**: (1) Run first mode=falsification lane — pick a belief and try to break it; (2) Run science_quality.py in 10 sessions to check improvement; (3) External validation experiment (test NK model on non-swarm repo); (4) Wire science_quality into orient.py output

## S396 session note (DOMEX-META-S396: sensing gaps — L-803 + P-244)
- **check_mode**: objective | **lane**: DOMEX-META-S396 (MERGED) | **dispatch**: meta (#3, F-META2, hardening)
- **expect**: Identify 3+ sensing gaps; wire knowledge_state into orient.py; add signal-age alert; write lesson
- **actual**: 3 gaps found and fixed in orient.py: (1) signal sort inversion — SIG-1/SIG-2 (P1, age 55s) were buried, now surface first; (2) backlog alert added for signals >20s old (17 flagged); (3) knowledge_state BLIND-SPOT 15.8%/DECAYED 20.6% now visible in Scientific Rigor section from JSON cache. L-803 written + P-244 extracted. Human signal "swarm how can swarm sense better swarm" addressed.
- **diff**: Exact match. SURPRISE: linter reverted orient.py changes mid-session (had to re-apply twice). Root cause: all 3 gaps share same failure mode — measurement tool existed but output not read (P-244: unread sensor = log file).
- **State**: ~731L 171P 20B 24F | L-803 | P-244 | orient.py sensing improved
- **Next**: (1) SIG-1/SIG-2 (P1, 55s old) — resolve node generalization + inter-agent comms; (2) Wire historian_repair.py into orient.py NOTICE; (3) Randomized dispatch 5% lottery (L-787)

## S396 session note (DOMEX-NK-S396: F-NK5 N=724 — K_avg equilibrium ~4.5 — L-801)
- **check_mode**: verification | **lane**: DOMEX-NK-S396 (MERGED) | **dispatch**: nk-complexity (#2, UCB1=4.0, PROVEN, mode=hardening)
- **expect**: K_avg ~2.6-2.65 at N~724. S372 regression model holds within 5% OOS. Hub z >25. Rate deceleration continues.
- **actual**: K_avg=2.5870 at N=724. Rate 0.0024/L (deceleration continues). Hub z=26.792. K_max=75 (up from 67). **New: K_avg equilibrium ~4.5** from edges-per-lesson convergence analysis (mean 4.52 edges/new lesson). S372 model asymptote (4.32 at 100% DOMEX) matches data equilibrium within 4%. L-601 hub attachment topic-general (40% DOMEX vs 37% non-DOMEX, Δ=3.3pp). Hub trend r=0.595 (super-linear PA). L-801 written.
- **diff**: Expected K_avg 2.6-2.65 — got 2.587 (CONFIRMED lower end). Expected hub z >25 — got 26.8 (CONFIRMED). Expected rate deceleration — CONFIRMED (0.0032→0.0024). Expected S372 model within 5% — 27% error at measured DOMEX_pct BUT asymptote matches 4% (PARTIAL: dynamics correct, Domain: field measurement contaminated by retroactive tagging). SURPRISE: equilibrium analysis — K_avg converges to edges-per-new-lesson rate (~4.5), not predicted.
- **meta-swarm**: All 3 commit attempts failed (index lock contention + HEAD movement + genesis hash drift). All work absorbed by concurrent session via commit-by-proxy (L-526). 0 direct commits, 100% absorption. Concrete target: orient.py should detect concurrent sessions (count active claims) and recommend immediate-commit strategy when N≥2. Commit loop friction wastes ~5 min/session in high-concurrency.
- **State**: ~730L 171P 20B 24F | L-801 | F-NK5 ADVANCED | DOMEX-NK-S396 MERGED (via proxy)
- **Next**: (1) COMMIT wave F-SOC1/F-SOC4 (valley of death); (2) randomized dispatch 5% lottery (L-787); (3) orient.py concurrent-session detection; (4) F-NK5 UNCLASSIFIED cleanup (72 lessons)

