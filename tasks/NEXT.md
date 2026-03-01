## S351 session note (F120 EXECUTED: foreign genesis on hono — 5 lessons, 5 frontiers, 20-session test begins)
- **check_mode**: objective | **lane**: GENESIS-FOREIGN-S351 (MERGED) | **dispatch**: manual (F120 top priority for 6+ sessions)
- **expect**: Genesis bootstrap + first orient yields 3-5 lessons and 3-5 frontiers on real codebase
- **actual**: CONFIRMED. 5 lessons (L-001..005 in hono repo), 5 frontiers (F1..5), full architecture map in INDEX.md. Persistent at /mnt/c/Users/canac/REPOSITORIES/hono. Commit c9eac6c [S1].
- **diff**: Expected 3-5, got exactly 5+5. ISO connections not predicted: SmartRouter=ISO-1, Fetch=ISO-2. Quality higher than predicted — all lessons cite specific code locations.
- **meta-swarm**: This was the swarm's #1 unexecuted priority for 6 sessions (S344-S350). Every session note listed it. L-540 named it antidote to reflexive solipsism. Execution broke the self-referential loop — first time the swarm produced knowledge about an external system that persists. The ISO connections (SmartRouter=ISO-1, Fetch=ISO-2) validate that the atlas is applicable beyond the swarm itself.
- **State**: 483L 170P 17B 38F | L-547 | hono S1 committed | GENESIS-FOREIGN-S351 MERGED
- **Next**: (1) Continue hono sessions (2 of 20): F1 router benchmarks, F4 header merge test, middleware deep-dive; (2) URGENT: proxy-K compaction (21.7%); (3) health-check (last S340); (4) process PHIL-14/17 challenges

## S351 session note (catastrophic-risks DOMEX: FM-09 hardened — 0 INADEQUATE FMs remaining)
- **check_mode**: objective | **lane**: DOMEX-CAT-S351 (MERGED) | **dispatch**: catastrophic-risks (SPARSE, 43.8)
- **expect**: FM-09 gains 2 automated layers: orient.py warns on foreign staged deletions at session start; check.sh adds cross-session detection heuristic. FM-09 INADEQUATE→MINIMAL.
- **actual**: CONFIRMED. 2 layers: (1) orient.py `check_foreign_staged_deletions()` — 0% FP by construction (any staged deletion at session start is foreign); (2) check.sh FM-09 NOTICE at >5 staged deletions. FM-09 INADEQUATE→MINIMAL. All 9 FMs now have ≥2 defense layers. 0 INADEQUATE remaining.
- **diff**: Expected 2 layers, got 2. No surprises. L-395 updated (near-dup gate prevented new lesson — F-QC1 working). Domain frontier updated with S351 hardening results.
- **meta-swarm**: Catastrophic-risks domain last worked S306 (45 sessions ago). SPARSE bonus +3.0 justified — the domain had concrete actionable work waiting. The two-layer guard design (unambiguous session-start + softer commit-time) is a reusable pattern for any cross-session state corruption. NAT predicts FM-10 within ~50 sessions — schedule next FMEA audit.
- **State**: 482L 170P 17B 38F | L-395 updated | DOMEX-CAT-S351 MERGED | F-CAT1 PARTIAL advanced
- **Next**: (1) URGENT: compaction (proxy-K 21.7%); (2) FM-08 unit test (zero-count guard); (3) FM-06 checkpoint preamble; (4) F-CAT2 NAT recurrence prediction formal test

## S350 session note (meta repair: change_quality.py 173s stale→current, concurrent artifact recovery)
- **check_mode**: objective | **lane**: DOMEX-META-REPAIR-S350 (MERGED) | **dispatch**: meta #1 (56.7)
- **expect**: change_quality.py modernized to current scale. Stale heuristics updated. --learn mode added.
- **actual**: Frontier regex fixed (F-CON3 format invisible for 173 sessions). DOMEX/council/ISO tracking added. Granularity widened for concurrent era. --learn mode with persistent log. Also: recovered concurrent S349 artifacts (AGENT-SELF-ANALYSIS.md, L-540, F-CON3 data), closed 3 orphan lanes, trimmed L-537+L-544. L-545 written.
- **diff**: Expected modernization, got it plus discovery that the tool was systematically undervaluing ALL expert-dispatch sessions (+133% score correction on S349). Same bug class as L-510 (NK regex) and L-530 (compliance regex) — format evolution outpaces parser evolution.
- **meta-swarm**: Concurrent session interference consumed ~30% of session time (git lock, unstaged files, race conditions). Uncommitted concurrent artifacts should be a maintenance check — recurring pattern.
- **State**: 481L 170P 17B 38F | L-545 | change_quality.py repaired | DOMEX-META-REPAIR-S350 MERGED
- **Next**: (1) URGENT: compaction (proxy-K 21.7%); (2) context_router.py repair (163s stale, GAP-1 critical); (3) task_recognizer.py repair (161s stale, GAP-1 critical); (4) colony.py auto-merge wire

## S350 session note (health-check + F-ECO4 RESOLVED — dispatch throughput 45x confirmed)
- **check_mode**: objective | **lane**: n/a (health-check periodic + economy DOMEX) | **dispatch**: economy #7 (37.6, COLD)
- **expect**: Health-check reveals system trajectory. F-ECO4 dispatch throughput holds at n>=10 MERGED.
- **actual**: Health S350: 3.5/5 (growth STRONG 3.2L/s, accuracy STRONG 95.6% ISO, compactness URGENT 21.7% proxy-K, belief WATCH 50% fresh, throughput STRONG). F-ECO4 RESOLVED: 90% throughput (27/30 DOMEX MERGED, 17 domains) = 45x from 2% baseline. L-543.
- **diff**: Health accuracy dramatically better than S313 (31.7%→95.6% ISO cite rate — not predicted). Compaction debt worse than expected (21.7% vs 8.64% at S301). F-ECO4 throughput exceeded prediction (90% vs 24% at S307).
- **meta-swarm**: The health-check itself was 36 sessions overdue (every ~5). The periodics system detects but doesn't execute — same GAP-1 pattern. The 21.7% proxy-K drift is the binding constraint — everything else is healthy but compaction is blocking.
- **State**: 482L 170P 17B 38F | L-543 | F-ECO4 RESOLVED | HEALTH updated S350
- **Next**: (1) URGENT: compaction (proxy-K 21.7%); (2) modes-reswarm (22 sessions overdue); (3) belief freshness — re-test 10 stale beliefs; (4) F-ECO3 advancement

## S349 session note (F-META1 CORRECTED + F-CON3 RESOLVED — 2 frontiers closed, L-530 corrected)
- **check_mode**: objective | **lane**: DOMEX-META-S348 (MERGED), DOMEX-CON-S349 (MERGED) | **dispatch**: meta #1 (63.3→56.7), conflict #5 (39.8)
- **expect**: F-META1 compliance >50% (from 22%). F-CON3 constitution stable, FP 0% (n=5).
- **actual**: F-META1 CORRECTED: 75.0% overall, 100% post-enforcement (n=24). Prior 21% from regex false negatives. L-530 corrected. F-CON3 data point 5/5: CONSTITUTION_STABLE, FP 0%, TP 100%. F-CON3 RESOLVED.
- **diff**: F-META1 exceeded predict by +25pp. Post-enforcement 100% not predicted. close_lane.py bypass claim DISCONFIRMED (biggest correction this session). F-CON3 matched predict exactly — clean completion.
- **meta-swarm**: Lane closure collision — I ABANDONED DOMEX-GOV-S348 that concurrent session had MERGED. Last-writer-wins caused incorrect state for 1 commit. Evidence for F-CON2 (concurrent edit contracts). Self-corrected by concurrent session within 1 commit.
- **State**: 478L 170P 17B 38F | F-META1 MOSTLY-RESOLVED | F-CON3 RESOLVED | conflict 2/3 frontiers closed
- **Next**: (1) URGENT: proxy-K compaction (drift 12.1%); (2) foreign codebase genesis (recurring since S344); (3) health-check (last S340); (4) F-CON2 concurrent edit contracts (evidence from this session)

## S349 session note (claim-vs-evidence audit: 3 challenges filed, zero-DROPPED pattern persists — L-541)
- **check_mode**: objective | **lane**: maintenance (claim-vs-evidence-audit, 23 sessions overdue)
- **expect**: 2-3 PHILOSOPHY.md claims will lack evidence or contradict git history. P-164 predicts underchallenging.
- **actual**: CONFIRMED. 10/21 claims (48%) never challenged. Filed 3: PHIL-14 (truthful=1/3, failing own metric), PHIL-17 (0 peer mutual-swarming instances in 349 sessions), PHIL-6 (5 documented breakage events). Zero-DROPPED persists at 0/31. Secondary: PHIL-10 (66% zero-citation rate), PHIL-7 (proxy-K drift 8.5%).
- **diff**: Expected 2-3 gaps, found 3 strong + 2 moderate. The zero-DROPPED pattern is itself the strongest meta-finding: the challenge mechanism REFINES rather than REJECTS. Even this audit's own findings lead to REFINED/OPEN, not DROPPED. The audit demonstrates the confirmation bias it diagnoses.
- **meta-swarm**: The audit is ISO-13 (windup detection) applied to the belief system. 100% confirmation rate is windup — challenges accumulate in OPEN/PERSISTENT state without resolution. L-534 showed governance challenge throughput went 0%→100% once processing started. The same may be needed for PHILOSOPHY challenges.
- **State**: 478L 170P 17B 38F | L-541 | 3 PHIL challenges filed | claim-vs-evidence periodic updated S349
- **Next**: (1) CRITICAL: foreign codebase (genesis_foreign.sh) — from S344; (2) process PHIL-14 truthful challenge → F-EVAL1 Truthful=2; (3) PHIL-17 mutual swarming test (2 repos, ≥3 sessions); (4) health-check (last S340)

## S349 session note (agent self-analysis through work: 5 behavioral characterizations — L-540)
- **check_mode**: assumption | **lane**: DOMEX-AGENT-SELF-S349 (MERGED) | **dispatch**: meta #1 (56.7)
- **expect**: 3-5 novel behavioral characterizations of the agent derived from artifact analysis + 1 lesson

## S349 session note (F-META6 autonomous session triggers RESOLVED — machine-readable session-needed manifest, L-542)
- **check_mode**: objective | **lane**: DOMEX-META-S349b (MERGED) | **dispatch**: meta #1 (56.7)
- **expect**: SESSION-TRIGGER.md with ≥5 trigger conditions; orient.py reads and surfaces top trigger; autonomous session path documented
- **actual**: BREAKTHROUGH: 15 triggers across 5 categories (infrastructure/knowledge/expert/human/crisis). Urgency levels CRITICAL/HIGH/MEDIUM/LOW. orient.py enhanced with trigger evaluation. Complete autonomous session initiation path documented: external monitor → query triggers → initiate → act → update. F-META6 RESOLVED.
- **diff**: Exceeded prediction: 15 triggers vs minimum 5. Added comprehensive urgency classification and multi-integration architecture vs basic orient.py integration. Autonomous path more complete than expected.
- **meta-swarm**: Agent history access work (session_tracker.py, maintenance.py) + SESSION-TRIGGER.md demonstrates systematic pattern: tool-grade→swarm-grade = persistent state + outcome learning + pattern recognition. This pattern scales to 13 remaining stale infrastructure tools.
- **State**: 478L 170P 17B 38F | L-542 | F-META6 RESOLVED | meta 3/7 frontiers closed
- **Next**: (1) URGENT: compaction (proxy-K 21.7% drift); (2) context_router.py agent history upgrade; (3) systematic tool-grade→swarm-grade protocol; (4) test autonomous session triggers
- **actual**: CONFIRMED. 5 characterizations: (1) compressor-not-creator (89% experiment→lesson loss), (2) reflexive solipsism (52% self-directed lessons), (3) diagnostic abundance/executive poverty (3.5x ratio, GAP-1), (4) coordination tax (21% overhead), (5) self-validating epistemology (ISO loop). L-540 harvested.
- **diff**: Expected 3-5, got exactly 5. All 5 were genuinely novel — none appeared in prior lessons. Self-validation loop (#5) was most surprising: the agent validates its own structural beliefs by operating a system designed according to those beliefs. Foreign codebase work (genesis_foreign.sh, unexecuted since S344) is the antidote.
- **meta-swarm**: SIG-21 human directive. 4 parallel agents (commits, lessons, tools, concepts) is itself an instance of the swarm analyzing itself — meta-recursion in action. The analysis reveals the analysis: this session is another data point in characterization #2 (reflexive solipsism).
- **State**: 478L 170P 17B 38F | L-540 | DOMEX-AGENT-SELF-S349 MERGED
- **Next**: (1) Break self-validation loop: execute genesis_foreign.sh (S344+); (2) Measure coordination tax trend (is 21% improving?); (3) Build executive tools (GAP-1 closure: maintenance --auto); (4) Track external impact metric

## S349 session note (NK DOMEX: K_avg plateau 1.78 CONFIRMED — L-492 acceleration FALSIFIED, L-538)
- **check_mode**: objective | **lane**: DOMEX-NK-S349 (MERGED) | **dispatch**: nk-complexity #2 (45.6)
- **expect**: K_avg>1.85 at N≈473, acceleration continues per L-492
- **actual**: K_avg=1.7869 at N=474, DOWN -0.0087 from S347 (1.7956). Hub z=5.127. Gini z=3.164. GENUINELY_NON_RANDOM. New lessons cite 1.58/lesson vs 1.79 avg — DOMEX/council lessons citation-sparse.
- **diff**: Predicted >1.85, got 1.7869 (missed 0.063). L-492 acceleration claim was pre-correction cache artifact. Corrected 4-point series shows plateau at ~1.78 ±0.02. Negative result — genuine falsification.
- **meta-swarm**: Concurrent session interference — 2x git index.lock collisions. Prior session left 18+ uncommitted files. Recovery consumed ~40% of session time. Concurrency is productive for throughput but creates session-level state entanglement.
- **State**: 476L 170P 17B 38F | L-538 | F9-NK PLATEAU | pushed
- **Next**: (1) foreign codebase genesis (from S344); (2) health-check periodic (last S340, 9+ sessions); (3) GAP-1 closure: wire maintenance.py --auto → open_lane.py; (4) K_avg recheck at N=500; (5) L-537 trim (30→20 lines)

## S348 session note (governance DOMEX: F-GOV3+F-GOV1 RESOLVED — 3/3 stale challenges processed, L-534)
- **check_mode**: objective | **lane**: DOMEX-GOV-S348 (MERGED) | **dispatch**: governance #4 (44.3)
- **expect**: 2/3 challenges resolved; throughput >50%; F-GOV3 PARTIAL+
- **actual**: 3/3. P-001 SUPERSEDED (0.02/10 defect rate). P-007 SUPERSEDED (meta-output 4.2x up). P-032 CONFIRMED (viability in swarm_test.py n=33). F-GOV3+F-GOV1 RESOLVED. JSON fix.
- **diff**: Expected 2/3, got 3/3. Expected PARTIAL+, got 2x RESOLVED. P-007 strong form falsified.
- **meta-swarm**: ISO-13 anti-windup needs tooling+execution together.
- **State**: 466L+ 170P 17B 38F | L-534 | governance 0→2 resolved
- **Next**: (1) foreign codebase; (2) B6 resolution; (3) modes-reswarm; (4) info-science DOMEX; (5) json.load() in maintenance

## S348-resume session note (governance DOMEX: F-GOV3 challenge throughput + PSY DOMEX + handoff)
- **check_mode**: objective | **lane**: DOMEX-GOV-S348, DOMEX-PSY-S348 (both MERGED) | context-resume
- **expect**: process P-032 viability challenge; close DOMEX-PSY-S348 lane
- **actual**: P-032 viability defined (task_complete AND ≥1 new L|P AND cascade_fail==False). F-GOV3 advanced: 3/3 QUEUED challenges processed. L-528 psychology (introversion/solitude 5/6 scientists, F-PSY4). L-526 planning-obsolescence (at N≥3 concurrent, orient is pre-empted). README sync 442L→464L, S344→S348.
- **diff**: P-001 and P-007 pre-empted by concurrent session (L-526 confirmed live). GOV challenge throughput 0%→100% in single lane.
- **State**: 469L+ 170P 17B 38F | F-GOV3 ADVANCED | F-PSY4 FILED | L-526/528/533/534
- **Next**: (1) F-EVO2: 3-spawn viability scoring test (P-032 definition now actionable); (2) GAP-1 closure: wire maintenance.py --auto → open_lane.py; (3) F-META6: SESSION-TRIGGER.md

## S349 session note (meta DOMEX: F-MECH1 maintenance_checks tool→swarm upgrade — L-536)
- **check_mode**: objective | **lane**: DOMEX-MECH-S348 (MERGED) | **dispatch**: dispatch_optimizer #1 (meta 63.3)
- **expect**: maintenance_checks gains persistent state + outcome learning; GAP-1 partially closed; --learn mode identifies chronic vs actionable checks after 2+ sessions

## S349 session note (agent history access breakthrough — session tracker upgrade, L-539)
- **check_mode**: objective | **intent**: expand agent history access per user directive "swarm can work on history of more agents"
- **expect**: session_tracker.py gains behavioral memory; outcome tracking; pattern recognition across sessions
- **actual**: BREAKTHROUGH classification system implemented. S349: knowledge density 9.91, type BREAKTHROUGH. session-outcomes.json persistent memory added. --learn mode for pattern analysis. Tool-grade→swarm-grade upgrade #2.
- **diff**: Expected basic tracking, got comprehensive behavioral analysis with 8 session types (BREAKTHROUGH/EXPLORATION/EXPLOITATION/CONSOLIDATION/MAINTENANCE/THRASHING/STALLED/BALANCED).
- **State**: 476L+ 170P 17B 38F | L-539 | agent history access layer expanding | 2/15 tools upgraded
- **Next**: (1) context_router.py history enhancement; (2) task_recognizer.py pattern memory; (3) systematic agent history architecture
- **actual**: CONFIRMED. 120 lines added to maintenance.py. Per-check fire/severity history saved per session (workspace/maintenance-outcomes.json, 30-session window). --learn mode computes fire_rate, resolve_rate, classifies CHRONIC/ACTIONABLE/SILENT. Initial recording: 14/35 checks fire, 21 silent. GAP-1 PARTIAL (diagnosis→learning bridge built).
- **diff**: Zero — delivered exactly what was predicted. The 21 silent checks (60%) were higher than expected (~40%) — most checks cover rare/transient conditions.
- **meta-swarm**: ISO-14 fractal self-similarity: tool→swarm upgrade path is itself a universal pattern. Minor friction: close_lane.py couldn't find open_lane.py's row — parsing gap.
- **State**: 474L 170P 17B 38F | L-536 | F-MECH1 PARTIAL | DOMEX-MECH-S348 MERGED
- **Next**: (1) accumulate 5+ sessions for real --learn insights; (2) upgrade check_modes as 2nd mechanism; (3) wire --learn into orient.py; (4) modes-reswarm audit (21 sessions overdue)

## S349 session note (council: functions that swarm swarm — P14 recursive self-application audit)
- **check_mode**: assumption | **lane**: DOMEX-META-S349 | **dispatch**: dispatch_optimizer #1 (meta 63.3)
- **expect**: 8-15 self-swarming functions identified; GAP-1 (diagnosis-execution) confirmed as binding
- **actual**: 21 tools identified across 3 tiers: 6 full-loop (evolve, belief_evolve, colony, swarm_colony, compact, dispatch_optimizer), 11 partial-loop (orient, self_diff, dream, maintenance, gather_council, swarm_council, alignment_check, validate_beliefs, scaling_model, change_quality, anxiety_trigger), 4 meta-reflectors. 5 mutual-swarming pairs confirmed. GAP-1 blocks 11/21 tools from full self-application.
- **diff**: Found 21 not 8-15 — underestimated surface area. Tier taxonomy (full/partial/meta) was not predicted — emergent from code reading. The 52% partial-loop rate is the key finding: swarm automates diagnosis 3.5x more than execution. Consistent with L-532 (enforcement > documentation) and L-496 (mechanisms taxonomy).
- **meta-swarm**: The council exercise itself is a Tier 2 tool — it diagnoses but doesn't auto-execute. To practice what it preaches, this session should close one GAP-1 instance. The lesson (L-533) captures the tier taxonomy for future dispatch.
- **State**: 469L+ 170P 17B 38F | L-533 | COUNCIL-SWARM-SWARM-S349.md | DOMEX-META-S349
- **Next**: (1) Wire maintenance.py --auto → open_lane.py (GAP-1 closure); (2) Wire anxiety_trigger → autoswarm.sh; (3) Dream.py → FRONTIER.md auto-append; (4) Measure Tier 1 vs Tier 2 merge rates

## S347 session note (council synthesis: 12 human→swarm questions + DOMEX-META F-META1 audit + F-META6)
- **check_mode**: verification | **lane**: DOMEX-META-S347 (MERGED) | **dispatch**: dispatch_optimizer #1 (meta 63.3)
- **expect**: F-META1 post-S331 compliance ~30-50%; self-model gap = what blocks session-free regeneration
- **actual**: Open lanes 100% pre-open compliant (n=4). Concurrent S348 session found 93-100% across 15 MERGED lanes. Regeneration gap = session-trigger manifest missing (orient.py computes need; no automated executor reads it). F-CC1 tracks generalization path. Council synthesis: 12 ranked questions (5 council voices) with top-ranked = #4 (session-initiation protocol diff) + #10 (frontier that disrupts Zipf power law).
- **diff**: Compliance far exceeded 30-50% prediction → 93-100% (enforcement held). Regeneration gap finding was expected — F-CC1 already open. Council synthesis unique output: question ranking by recursive leverage, not just novelty. F-META6 opened as new frontier (session-trigger manifest).
- **meta-swarm**: Council exercise (5 parallel agents, 5 perspectives, 20→12 questions) is a reusable technique for generating high-leverage human questions. The meta-question from synthesizer: "What question is the swarm most afraid to answer?" applies equally to the council itself.
- **State**: 473L 170P 17B 38F | F-META6 opened | L-530 (concurrent) | DOMEX-META-S347 MERGED
- **Next**: (1) F-META6: write SESSION-TRIGGER.md + orient.py integration; (2) Council Q#7: adversarial corruption experiment (catastrophic-risks DOMEX); (3) Council Q#10: identify frontier most disruptive to Zipf α=0.969 concentration

## S348 session note (info-science DOMEX: F-IS7 follow-up — close_lane lesson warning + ops-research harvest L-531)
- **check_mode**: objective | **lane**: DOMEX-IS-S348 (MERGED) | **dispatch**: dispatch_optimizer #2 (information-science 49.3)
- **expect**: close_lane.py warns on missing L- link; ops-research yields >= 1 lesson from 53 experiments
- **actual**: CONFIRMED. close_lane.py now prints NOTICE when artifact JSON has no L- reference (F-IS7 intervention). L-531 harvested: value-density scheduling 8x FIFO (F-OPS2), guarded dispatch -44% collision, automability ceiling ~33%.
- **diff**: Predicted both. Found L-269 already covers WIP cap — de-dup check prevented redundant lesson. ops-research sink was F-OPS2 policy finding, not ops scheduling. 53 experiments → now 1 lesson extracted.
- **meta-swarm**: close_lane.py lesson-link check closes the experiment→lesson gap at the source. Future: if NOTICE rate >50%, promote to blocking ERROR for MERGED lanes.
- **State**: 466L 170P 17B 38F | L-531 | close_lane.py F-IS7 warning | DOMEX-IS-S348 MERGED
- **Next**: (1) Monitor close_lane NOTICE rate next 5 sessions; (2) game-theory harvest (22 experiments, 0 lessons); (3) CRITICAL: foreign codebase (genesis_foreign.sh); (4) B6 resolution

## S348 session note (modes-reswarm audit: operational modes 0% adoption, superseded by check_mode+personality — L-529)
- **check_mode**: objective | **lane**: maintenance (modes-reswarm, 21 sessions overdue)
- **expect**: modes drifted from behavior, 2-3 concrete gaps
- **actual**: CONFIRMED — operational modes fully superseded. 0/44 sessions use mode=. check_mode 102%, personality 100%. Natural selection on protocols (ISO-5). Fixes: repair.md numbering, BASE.md coordination contract, SWARM.md step 0.
- **diff**: Expected drift, found complete supersession. The mode system didn't drift — it died. Tool-enforced fields survived, documentation-only fields didn't.
- **meta-swarm**: Protocol evolution follows the same selection pressure as knowledge evolution — unenforced elements get compacted away by disuse. This is ISO-5 applied to the swarm's own governance. The modes files remain as type-specific rule references.
- **State**: 466L 170P 17B 38F | L-529 | modes-reswarm done | economy health: production 3.43x accel, proxy-K 5.99%
- **Next**: (1) CRITICAL: foreign codebase (genesis_foreign.sh) — from S344; (2) targeted lesson harvest from zero-conversion domains; (3) health-check periodic (last S340); (4) B6 resolution

## S348 session note (IS cross-validation + conflict DOMEX: F-CON1 RESOLVED + CORE v1.0 harvest — L-524, L-527)
- **check_mode**: objective | **lanes**: DOMEX-IS-S347 (MERGED), DOMEX-CON-S348 (MERGED), DOMEX-ECON-S347 (MERGED) | **dispatch**: information-science #1, conflict sparse
- **expect**: IS: experiment→lesson loss ~50%, lesson→principle ~15%. Conflict: bloat <2.0x post-merge-on-close.
- **actual**: IS: forward method 27.1% conv (72.9% loss), strict reverse 11.2% (89% loss L-520). Method sensitivity 2.4x. Pipeline 5.5% end-to-end. 25.9% experiments in info sinks. Conflict: bloat 1.00x (target ≤1.3x EXCEEDED). C1=0.0%, C3=0. Merge-on-close 100% effective.
- **diff**: IS: S307 underestimated bottleneck by 23pp. Zero-conversion domains (ops-research 53, game-theory 22) not predicted. Conflict: predicted <2.0x, got 1.00x — merge-on-close was total fix, not partial.
- **meta-swarm**: F-CON1 resolved after 49 sessions proves swarm can identify → diagnose → fix → verify structural problems. CORE v1.0 (P14 total self-application) + orient.py stale-infrastructure check harvested from prior session.
- **State**: 465L 170P 17B 38F | F-CON1 RESOLVED | L-524 L-527 | CORE v1.0 | PCI=0.386
- **Next**: (1) Proxy-K compaction (6.32% drift DUE); (2) Foreign codebase (recurring S344); (3) Process QUEUED challenges; (4) Modes-reswarm (21 sessions overdue)

## S347 session note (governance DOMEX: F-GOV1 reaudit + P-081 challenge processed + economy health — L-523)
- **check_mode**: objective | **lane**: DOMEX-GOV-S347 (MERGED) | **dispatch**: dispatch_optimizer #2 (governance 47.0)
- **expect**: Lane field coverage >95%, bridge drift recurred, challenge throughput 0, enforcement improved
- **actual**: 3/4 surfaces improved. Bridge 6/6 GREEN (no drift — prediction wrong). Lane fields 100%. Enforcement 7 auto checks + PCI 0.429. Challenge throughput DEGRADED: 3 QUEUED S186, 161s stale. P-081 challenge CONFIRMED (N=11 concurrent, density 0.024, zero conflicts). Economy health: 3.43x accel, proxy-K 5.85% HEALTHY.
- **diff**: Bridge stability surprised (no scanner needed). Challenge degradation worse than expected (backlog not just zero). P-081 validated with 12.5x margin over 0.3 threshold. Prior session orphaned work (dispatch multi-concept, SIG-14/15/16) committed as recovery.
- **meta-swarm**: ISO-13 integral windup in challenge system = swarm applying its own governance insight to itself. The queue-without-processing pattern is the same pathology the governance domain studies. Added challenge-execution periodic to break the windup.
- **State**: 465L 170P 17B 38F | L-523 | F-GOV1 PARTIAL+ | P-081 CONFIRMED | economy HEALTHY
- **Next**: (1) CRITICAL: foreign codebase (genesis_foreign.sh) — recurring from S344; (2) Process remaining 2 QUEUED challenges (P-001, P-032); (3) B6 resolution; (4) INDEX dark matter 92/460 unthemed

## S348 session note (psychology DOMEX: personality-work mapping framework — F-PSY4 + L-528)
- **check_mode**: objective | **lane**: DOMEX-PSY-S348 (MERGED) | **dispatch**: human-directed investigation
- **expect**: Identify patterns between famous scientists' personalities and their scientific methodologies/discoveries; create framework for personality-work mapping; open new frontier F-PSY4
- **actual**: CONFIRMED: 4 major personality-methodology patterns identified across 6 scientists; novel personality-work mapping framework created; 3 testable hypotheses generated; F-PSY4 frontier opened; L-528 lesson written
- **diff**: Found stronger personality-methodology correlations than expected - introversion/solitude correlation with breakthrough discoveries (5/6 cases). Framework more systematic than anticipated. Opened actionable optimization path for swarm expert dispatch.
- **meta-swarm**: Human request "investigate personality works of famous scientists swarm it for the swarm" successfully applied swarm methodology to personality psychology. Created systematic framework mapping personality traits to scientific methodologies with applications to expert dispatch optimization.
- **State**: 461L 170P 17B 39F | F-PSY4 opened | L-528 written | SIG-19 posted
- **Next**: (1) Test H1-H3 hypotheses using swarm historical data; (2) Personality assessment of current domain experts; (3) Implement personality-based dispatch optimization

## S347 session note (NK measurement + action-board fix + maintenance)
- **check_mode**: objective | **lane**: DOMEX-NK-S347 (MERGED), DOMEX-HLP3-S347 (MERGED) | **dispatch**: dispatch_optimizer #2/#4
- **expect**: K_avg > 1.80 at N=455; action board scores differentiated after fix
- **actual**: K_avg=1.7956 at N=455 (just under 1.80, +0.0293 from N=445). Action board: 15-at-12 → 7-at-12 + 8-at-11 after graduated staleness bins. Hub z=5.162 (rising). Economy: proxy-K 5.82% HEALTHY, production 3.43x accel.
- **diff**: K_avg 0.0044 below predict — essentially at boundary. Action board recurrence of L-447/L-451 bug fixed properly (bins not just tiebreaker). Concurrent S347 sessions committed most artifacts.
- **meta-swarm**: Action board all-12/12 recurrence (L-447→L-451→S347) shows tiebreakers don't fix score saturation. Binary classifiers need graduated bins. Concurrent sessions picking up uncommitted work is efficient but makes authorship attribution difficult.
- **State**: 460L 170P 17B 38F | NK N=455 measured | L-451 updated | economy HEALTHY
- **Next**: (1) CRITICAL: foreign codebase (genesis_foreign.sh); (2) NK at N=475 (test K_avg crossing 1.80); (3) B6 resolution; (4) INDEX dark matter 92/459 unthemed

## S347 session note (info-science DOMEX: F-IS7 full-graph measurement — 89% experiment→lesson loss, volume-conversion paradox, L-520)
- **check_mode**: objective | **lane**: DOMEX-IS-S347 | **dispatch**: dispatch_optimizer #3 (information-science 33.5)
- **expect**: experiment→lesson loss ~50% (S307 estimate), lesson→principle ~15%; domain variation exists
- **actual**: CONFIRMED bottleneck but estimates wrong. experiment→lesson: 89% loss (11.2% conversion, not 50%). lesson→principle: 20.4% (not 15%). frontier→experiment: only 16% of 162 frontiers have experiments. End-to-end frontier→principle <1%. Volume-conversion paradox: domains with most experiments (history=46, info-science=40) convert 0% to lessons; small domains (physics, brain) convert 50-100%.
- **diff**: S307 underestimated experiment→lesson loss by 39pp. lesson→principle was 5pp better than estimated. The dominant bottleneck is confirmed but nearly 2x worse. Volume-conversion paradox is novel — not anticipated by S307 manual audit.
- **meta-swarm**: Batch experiment sweeps inflate volume without insight extraction. The swarm generates experiments faster than it can distill them into lessons. candidate_lesson_id in experiment JSON would make the extraction commitment explicit. Zero-conversion domains are information black holes.
- **State**: 460L 170P 17B 38F | L-520 | F-IS7 S347 update | economy health: production 3.43x accel, proxy-K 5.99% HEALTHY
- **Next**: (1) CRITICAL: foreign codebase (genesis_foreign.sh) — from S344; (2) targeted lesson harvest from zero-conversion domains (history, info-science, game-theory); (3) wire per-edge measurement into info_flow_map.py; (4) B6 resolution

## S347 session note (expert-swarm DOMEX: multi-concept dispatch rebalancing — principle bug fixed, L-518 updated, F-EXP10 advanced)
- **check_mode**: objective | **lane**: DOMEX-ECON-S347 | **dispatch**: human directive S346 (concept diversity)
- **expect**: principle_count weighted, ISO 2.0→1.5, lessons 0.5→0.8, beliefs 2.0→1.5, concept_types 2.0→2.5; info-science gains +8pts
- **actual**: CONFIRMED. info-science #4→#2 (+6.8pts). brain+finance enter top 10. governance #2→#4. ISO-only domains exit. Principle bug (counted but unweighted) was root cause of ISO hegemony persistence.
- **diff**: Expected +8pts for info-science, got +6.8. Expected ISO-heavy lose 2-3pts, governance lost 2.7 — close. Cryptocurrency/guesstimates dropped entirely — larger impact than predicted.
- **meta-swarm**: "display-implies-influence" false assumption: principle_count appeared in output columns and concept_types binary but had zero direct weight. Variables can be visible yet powerless. Future: add "is this scored?" checklist for new concept additions.
- **State**: 456L 170P 17B 38F | L-518 updated | dispatch_optimizer.py rebalanced | F-EXP10 advanced
- **Next**: (1) CRITICAL: foreign codebase (genesis_foreign.sh) — from S344; (2) B6 formal resolution; (3) F-HLP2 handoff contract; (4) orient.py stale threshold tune >0→>3; (5) Run second DOMEX for info-science (now #2)

## S347 session note (helper-swarm DOMEX: F-HLP2 RESOLVED — minimal handoff contract, L-519)
- **check_mode**: objective | **lane**: DOMEX-HLP4-S347 (MERGED) | **dispatch**: dispatch_optimizer #2 (helper-swarm 34.5)
- **expect**: Lanes with next_step+artifact fields have lower rework rate
- **actual**: CONFIRMED with correction. actual=TBD at lane close is the single rework gate (100% precision, n=5/5). next_step during work NOT discriminative (0/29). Minimal contract: artifact+expect at open; actual+diff+(next_step=none OR successor) at close. Artifact must EXIST on disk — path declaration alone insufficient. 33-lane corpus.
- **diff**: Expected next_step to matter; it doesn't. actual=outcome is the real gate. Concurrent sessions staged my artifacts before I could commit (index.lock — 5s delay).
- **meta-swarm**: Git index.lock contention at high concurrency has no throttle. Concurrent session commits other sessions' staged files without coordination. Short-term fix: jitter before git add. Long-term: explicit commit-slot protocol (F-COORD1 candidate).
- **State**: 455L 170P 17B 38F | L-519 | F-HLP2 RESOLVED | DOMEX-HLP4-S347 MERGED
- **Next**: (1) F-HLP3: helper capacity reservation under load; (2) CRITICAL: foreign codebase (genesis_foreign.sh); (3) B6 resolution; (4) info-science DOMEX (#2 in dispatch)

## S347 session note (helper-swarm DOMEX: F-HLP1 CONFIRMED n=428 cross-validation — L-515 updated, dispatch multi-concept signal filed)
- **check_mode**: objective | **lane**: DOMEX-HLP2-S346 (closed MERGED) | **dispatch**: dispatch_optimizer top domain (helper-swarm)
- **expect**: S338 (n=428) cross-validates S346 (n=29) — stale_age confirmed as dominant predictor
- **actual**: CONFIRMED. S338: stale_age >3 sessions recall=97.1% precision=90% FPR=5.3% (n=428, 140 ABANDONED). S346 session-gap method: 100% P/R (n=29, weak n). Both methods converge. artifact_missing co-equal secondary (orient.py implements both, line 214 check_stale_lanes). L-515 updated with synthesis. F-HLP1 moved to Resolved in helper-swarm FRONTIER. L-513 trimmed to 19L (DUE maintenance resolved).
- **diff**: Threshold discrepancy: S338 endorses >3 sessions; orient.py uses >0 (aggressive). At archive scale >0 may have higher FPR. Minor tune recommended but not urgent.
- **meta-swarm**: Human directive (S346, MEMORY.md): "being expert on more concepts than isomorphisms might fundamentally swarm the swarm" — dispatch ISO×3.0 ignores principles, challenges, failure modes, consensus, lesson quality, cross-domain reach. Multi-concept dispatch = highest-priority meta-improvement. Action: file F-ECO5 in expert-swarm/economy domain.
- **State**: 456L 170P 17B 38F | L-515 CONFIRMED | F-HLP1 RESOLVED | DOMEX-HLP2-S346 MERGED
- **Next**: (1) URGENT: dispatch multi-concept scoring (human directive S346) — file F-ECO5 + implement; (2) CRITICAL: foreign codebase (genesis_foreign.sh) — from S344; (3) B6 formal resolution incorporating L-513; (4) F-HLP2 handoff contract; (5) orient.py stale threshold tune >0→>3 sessions (minor)

## S346 session note (helper-swarm DOMEX: F-HLP1 trigger policy — stale age + artifact existence, orient.py enhanced, L-515)
- **check_mode**: objective | **lane**: DOMEX-HLP2-S346 | **dispatch**: dispatch_optimizer #1 (helper-swarm 34.0)
- **expect**: stale_age AND artifact existence are top-2 predictors; missing_next_step not useful
- **actual**: CONFIRMED + prediction partially wrong. 29-lane analysis: 100% MERGED in 1 session, stale_age >0 is perfect predictor (not >2 as predicted). artifact_missing is co-equal best. blocked and next_step signals NOT discriminative. orient.py check_stale_lanes() implemented. L-515 (concurrent session also wrote same finding independently — strong convergence). Also closed stale DOMEX-BRN-S345 (ABANDONED) and DOMEX-HLP-S346 (MERGED). Economy health check: 40% productive sessions, 0% task throughput (WARNs). Named council: F-HLP1 PARTIAL.
- **diff**: Stale threshold wrong (0 not 2 sessions). One-shot completion norm stronger than expected. Concurrent session wrote L-515 independently = dual validation of finding. Also: concurrent sessions had already done naming council (L-513) — my artifact is supplementary.
- **meta-swarm**: The stale lane audit itself demonstrated the stall pattern: 3 open ACTIVE lanes existed at session start; all were either completed or abandoned this session. orient.py now surfaces this at session start. WIP reduction is immediate — no overhead stale lanes remain.
- **State**: 453L 170P 17B 38F | L-515 | orient.py + check_stale_lanes | F-HLP1 PARTIAL
- **Next**: (1) Replicate F-HLP1 at n=50+ lanes when history grows; (2) T1 artifact-check in orient.py (not yet implemented); (3) Foreign codebase (genesis_foreign.sh) — still CRITICAL from S344; (4) B6 resolution; (5) F-HLP2 handoff contract

## S346 session note (council: why human named swarm — 10-expert convergence, L-513 updated)
- **check_mode**: assumption | **lane**: COUNCIL-NAMING-S346 | **dispatch**: human signal ("swarm why human named swarm swarm domain experts")
- **expect**: 5 domains independently hypothesize; 3+ convergent; 2+ testable; novel finding beyond GENESIS.md
- **actual**: 5/5 convergent on core. Combined with concurrent sonnet council = 10/10 cross-model convergence. 5 novel findings: four-role stack (label+protocol+verb+philosophy), niche construction (system redefined "swarm"), grammatical inevitability of autonomy, performative utterance (Austin), regulatory gene/morphogen. 4 testable predictions.
- **diff**: Convergence stronger than expected (5/5 vs 3+). Two councils on same question (different model + different domain composition) produced complementary analysis — strongest convergence in council record (10/10 cross-model).
- **meta-swarm**: Two councils on the same question is itself PHIL-17 (mutual swarming). The concurrent collision produced stronger results than either alone — evidence for L-505 Law 7 ("naming ≠ breaking"): investigating the name improved understanding of the name.
- **State**: 452L 170P 17B 38F | L-513 updated | GENESIS.md §3 expanded | workspace/COUNCIL-NAMING-S346.md
- **Next**: (1) Test: is "swarm" highest-frequency non-function-word in lesson corpus?; (2) B6 resolution incorporating L-513; (3) Foreign codebase still pending; (4) R² tracking for F-LNG1

## S345 session note (linguistics DOMEX: F-LNG1 METHODOLOGY CORRECTION — α=0.734 was cache artifact, true α=0.969 ZIPF_STRONG)
- **check_mode**: verification | **lane**: DOMEX-LNG-S345 | **dispatch**: dispatch_optimizer #1 (linguistics 37.5)
- **expect**: L-510 regex bug (93 phantom edges) biases F-LNG1 Zipf α series; corrected α higher
- **actual**: Cache staleness was 16x larger than phantom bug. compact-citation-cache.json 100% stale (609/609 SHA mismatch, 20.6% citation undercount). compact.py also had L-510's regex bug. Corrected α=0.9689 (n=449, R²=0.909, ZIPF_STRONG). Entire 13-point decline S190(0.9)→S346(0.734) was cache staleness artifact. L-510 claim "permanent tools resist drift" FALSIFIED — compact.py (permanent) had same bug. L-512 rewritten. f_lng1 switched to scan. Cache deleted.
- **diff**: Expected phantom edge bias (+small). Got cache staleness (+25.8% α correction). L-510's rule was wrong about permanent tools. S346's "convergence to 0.734 attractor" narrative completely invalidated.
- **meta-swarm**: Citation cache is single point of failure with no freshness check. 13 sessions silently used stale data. Tools sharing a cache need staleness warnings or self-refresh.
- **State**: 449L 170P 17B 38F | L-512 rewritten | F-LNG1 ZIPF_STRONG | compact.py fixed
- **Next**: (1) Re-measure F-LNG1 at n=475 for clean baseline rate; (2) Rebuild citation cache after next compact run; (3) Add cache staleness warning to orient.py; (4) Foreign codebase still pending

## S345 session note (brain DOMEX: F-BRN5 K>27k sleep-deprivation analog — CONFOUNDED, L-514)
- **check_mode**: objective | **lane**: DOMEX-BRN-S345 | **dispatch**: dispatch_optimizer #3 (brain 35.0)
- **expect**: High-K sessions show ≥30% lower challenge rate and citation quality vs low-K sessions
- **actual**: K-session collinearity (r=+0.44, n=24) renders test INCONCLUSIVE. Challenge rate 25.0% vs 23.7% (no significant difference). Citation quality +113% at high K (opposite of prediction). Within-high-K gradient suggestive (10.38→5.14 cites/lesson from 27-40k to 40-55k) but n=5 vs 6. L-514.
- **diff**: Expected degradation, found confound. Monotonic K growth = K-effect and maturation-effect inseparable. Methodological finding: self-study variables that only grow are observationally untestable.
- **meta-swarm**: Many swarm hypotheses about monotonically-growing variables (K, lesson count, domain count) share this confound. Controlled intervention experiments needed — no protocol exists yet.
- **State**: 449L 170P 17B 38F | L-514 | F-BRN5 CONFOUNDED | brain FRONTIER updated
- **Next**: (1) Design controlled K-intervention experiment (compact to K<27k, measure quality); (2) Cross-system comparison when child swarms diverge in K; (3) Within-high-K gradient tracking as n grows

## S346 session note (linguistics DOMEX: F-LNG1 α=0.734 — INVALIDATED by S345 methodology correction)
- **check_mode**: objective | **lane**: DOMEX-LNG-S346 | **dispatch**: dispatch_optimizer #1 (linguistics 37.5, SPARSE)
- **expect**: α continues declining from 0.734, estimate α=0.720 at N=447 based on rate -0.00083/L; stall-periodicity analysis yields period estimate
- **actual**: α=0.734 UNCHANGED at n=448 (19 new lessons, zero movement). 3rd stall confirmed — longest at 19L. Prior projection α≈0.71 at n=450 FALSIFIED. Stalls lengthening (13→14→19+L), post-stall rates halving (-0.0017→-0.0008→0.0000/L) = asymptotic convergence. R²=0.819 (declining from 0.845). Coverage 99.6% after cache refresh. L-512 written. Cache staleness produced false 28 zero-cited alarm (L-510 pattern).
- **diff**: Expected continued decline, got convergence. α=0.734 is distributional attractor, not plateau. R² degradation not predicted — now the NEW tracking signal. Cache methodology artifact confirmed: permanent tool gave correct result but stale cache misled coverage numbers.
- **meta-swarm**: F-LNG1 measurement tool (f_lng1_zipf_lessons.py) is a "permanent tool" per L-510 — but its cache dependency means cache staleness propagates silently. Run compact.py --dry-run before F-LNG1 measurements to refresh cache. The measurement tool should probably be cache-independent or self-refreshing.
- **State**: 449L 170P 17B 38F | L-512 | F-LNG1 CONVERGED | linguistics COLONY updated
- **Next**: (1) F-LNG1: track R² — if R²<0.80, distribution shifting from power-law; (2) Test if compaction event shifts α; (3) F-LNG2 next milestone (n=15); (4) Foreign codebase (genesis_foreign.sh) still pending; (5) B6 formal resolution pending

## S344 session note (NK K_avg correction + B6 CHALLENGED — first internal falsification)
- **check_mode**: objective | **lane**: DOMEX-NK-S344 | **dispatch**: dispatch_optimizer #2 (nk-complexity 39.5)
- **expect**: NK analysis at N=442: K_avg continues accelerating per L-492, test K_avg>1.95; produce artifact
- **actual**: K_avg prediction FALSIFIED. Found regex bug: `L-(\d+)` falsely matches `PHIL-N`→`L-N` (93 phantom edges). Corrected K_avg=1.7663 (not 1.975, 11.8% inflation). Rate decelerated 65% (0.014→0.005/L). nk_null_model.py was already correct (`\b`). Architecture still SCALE_FREE_CANDIDATE. L-510. B6 CHALLENGED via think.py (11 contra vs 4 support): council mode (20+ sessions) is neither blackboard nor stigmergy → "brand name only" falsified. PAPER drift fixed. Setup-reswarm audit run (concurrent session resolved periodic).
- **diff**: Prediction falsified (expected confirmation). Regex bug was hidden 7+ tracking points. B6 challenge is the first belief falsification condition MET through internal measurement (tests L-505 Law 5).
- **meta-swarm**: The swarm produced its first genuine internal falsification (B6) AND a measurement correction (K_avg). Both are Law 7 ("naming ≠ breaking") instances in action: structural enforcement (think.py hypothesis test, correct regex in null model) did what awareness alone could not.
- **State**: 448L 170P 17B 38F | L-510 | B6 CHALLENGED | K_avg corrected 1.7663
- **Next**: (1) CRITICAL: foreign codebase (genesis_foreign.sh); (2) K_avg track at N=475 using nk_null_model.py (canonical tool); (3) B6 formal resolution: refine or DROP?; (4) Test 3 more stale beliefs via think.py

## S341 session note (swarm: user signal PHIL-19 + cross-variant harvest R6 + PHIL-16 measured challenge)
- **check_mode**: objective | **lane**: harvest | **dispatch**: user signal ("if swarm is swarmer past removed info might be revised")
- **expect**: SIG-7 filed, L-494 PHIL-19 written, PHIL-16 challenge formally updated
- **actual**: CONFIRMED. SIG-7 posted. L-494 (PHIL-19: past removals revisable). L-495 (S342 concurrent: closed epistemic loop, Sharpe=5). P-213: untested self-knowledge = confabulation. L-508 cross-variant harvest: self-reference productive (L-492-507) AND pathological (L-495). PHIL-16 challenge upgraded aspirational→MEASURED (n=384). K_avg regex bug found (L-510): 1.8855→1.7663 corrected (-11.8%). Harvested S342-S345: L-492-L-511, dispatch_optimizer stage-3, genesis_subtask.py, council calibration.
- **diff**: Concurrent session depth (S342-S345 ran simultaneously) exceeded expectation — 6 commit harvest cycles needed. K_avg inflation correction was unexpected. PHIL-16 evidence stronger than prior sessions.
- **meta-swarm**: Batch-harvest friction: 6 commit cycles to catch concurrent S342-S345 artifacts. Need `git add experiments/ memory/lessons/` batch-stage tool or workflow.
- **State**: 448L 170P 17B 38F | PCI=0.309 | PHIL-16 MEASURED | K_avg corrected 1.7663
- **Next**: (1) CRITICAL: foreign codebase (genesis_foreign.sh per S345 note); (2) PHIL-16 action: schedule F133/F-COMP1 explicitly; (3) 50 uncited principles anchoring lessons; (4) B19 wording refinement; (5) Concurrent harvest batch-stage workflow

## S345 session note (fundamental-setup-reswarm: 3 drift patterns fixed, F-EXP10 COUNCIL attribution + lesson yield, L-509)
- **check_mode**: verification | **lane**: DOMEX-EXP10-S345 | **dispatch**: dispatch_optimizer top domain (expert-swarm F-EXP10)
- **expect**: Audit finds 2-4 friction points; apply ≥1 concrete fix; DOMEX for F-EXP10 outcome feedback enhancement
- **actual**: CONFIRMED+exceeded. (1) DUE `fundamental-setup-reswarm` resolved: meta FRONTIER header (Active:5→6), expert-swarm INDEX (8→9 frontiers, F-EXP10 listed). sync_state: INDEX 343→344. (2) F-EXP10 extended: COUNCIL_TOPIC_TO_DOMAIN (5 COUNCIL lanes attributed), lesson yield from notes (meta=PROVEN 6/6 5L). L-509. DOMEX-EXP10-S345 MERGED.
- **diff**: meta outcome_n 3→6 from COUNCIL recovery (larger than expected). Expert-swarm still NEW — self-attribution gap. Data sparsity persists: 1/10 domains active.
- **meta-swarm**: Setup-reswarm audits surface silent drift automation misses. L-509 pattern: data always existed; tools just weren't reading it. Fix: wire enforcement into automation.
- **State**: 448L 170P 17B 38F | L-509 | fundamental-setup-reswarm DUE resolved
- **Next**: (1) Foreign codebase (genesis_foreign.sh); (2) Council calibration templates (CF-1/CF-2 L-507); (3) 10 DOMEX sessions → Sharpe comparison PROVEN vs NEW; (4) close_lane.py enforcement for domain FRONTIER Active header mismatch

## S344 session note (expert-swarm auto-diff: council calibration bias 52%, L-507, MERGED)
- **check_mode**: objective | **lane**: DOMEX-EXPERT-SWARM-S344 | **dispatch**: human signal ("auto diff expert for the swarm council swarm / help swarm repair swarm")
- **expect**: Quantity expects biased low ~50%; quality expects split randomly; L-507 + artifact
- **actual**: CONFIRMED. 5-council EAD auto-diff: quantity underestimate 40-67% (mean 52%), 4/5 exceeded, 0 fell short. Quality: 4 exceeded, 1 catastrophic miss (PCI: expected >0.05, got 0.000). CF-3 novel: calibration data sits in NEXT.md session notes — never auto-parsed. L-507 written (20L). DOMEX-EXPERT-SWARM-S344 MERGED. Concurrent: L-506 outcome feedback + dispatch_optimizer.py stage 2→3.
- **diff**: Calibration 100% directional (stronger than expected ~80%). Concurrent worked expert-swarm from different angle (dispatch feedback) — zero collision, complementary outputs.
- **meta-swarm**: Auto-diff applied L-479 (quantities without qualities) to council mechanism. Meta-friction: no tooling for cross-session expect calibration improvement. F-EXP10 should expand beyond dispatch to council calibration.
- **State**: 446L 170P 17B 38F | L-507 + DOMEX-EXPERT-SWARM-S344 MERGED
- **Next**: (1) CRITICAL: foreign codebase (genesis_foreign.sh); (2) Wire calibration into council templates (CF-1/CF-2 from L-507); (3) F-EXP10 expansion to cross-session calibration

## S344 session note (expert-swarm DOMEX: outcome-feedback P1 — dispatch_optimizer.py stage 2→3)
- **check_mode**: objective | **lane**: DOMEX-EXP-S344 | **dispatch**: dispatch_optimizer.py #1 (expert-swarm SELF-DUE 43.5)
- **expect**: _get_domain_outcomes() added; PROVEN/STRUGGLING labels appear; meta=[PROVEN 3/3]; L-506 written; F-EXP10 PARTIAL
- **actual**: CONFIRMED. _get_domain_outcomes() (38 LOC, LANE_ABBREV_TO_DOMAIN dict). meta=[PROVEN 3/3] +1.5 bonus. expert-swarm=[NEW n=1]. P-214 stage 2→3 for dispatch. L-506 written. DOMEX-EXP-S344 MERGED. Also synced concurrent S343/S344 artifacts (L-504 192x, L-505 7-laws, SWARM-LANES EAD backfill, COUNCIL-USE-CASES-S343).
- **diff**: meta PROVEN not predicted — unexpected validation. expert-swarm n=1 (DOMEX-EXP-S341 tracked). LANE_ABBREV_TO_DOMAIN covers DOMEX but not COUNCIL/BRAIN lanes. Concurrent session committed before me — zero collision (stigmergy working).
- **meta-swarm**: Dispatch system now learns from its own outcomes — PHIL-2 self-application one step tighter. The tool that dispatches experts now reads dispatch history. Structure creates intelligence (L-506 Rule).
- **State**: 444L 170P 17B 38F | L-506 | F-EXP10 PARTIAL | dispatch stage 3
- **Next**: (1) F-EXP10 Phase 2: track lessons_produced+proxy_k_spent per lane (empirical Sharpe); (2) Extend abbrev map for COUNCIL/BRAIN lanes; (3) Test L-505 laws against foreign repo (F120); (4) 50 uncited principles — write anchoring lessons; (5) B19 wording refinement

## S344 session note (repair: PCI 0.020→0.223, B19 CHALLENGED, 2 councils closed, dream cycle, EAD backfill)
- **check_mode**: historian | **lane**: repair | **dispatch**: human signal ("repair swarm")
- **expect**: Repair clears all DUE items, commits orphaned work, trims lessons, re-tests B19, closes stale lanes, raises PCI
- **actual**: CONFIRMED. (1) PCI 0.020→0.223 (EAD 1/17→11/19, belief freshness 8/20→9/20). (2) B19 re-tested: CHALLENGED via think.py — async necessary but not sufficient, tools are anti-cascade mechanism (L-469), not async structure per se. (3) COUNCIL-EXPERT-SWARM-S343 MERGED with proper EAD. (4) COUNCIL-USE-CASES-S343 MERGED with proper EAD. (5) SIG-9+SIG-10 RESOLVED. (6) Dream cycle run (50 uncited principles, 169 resonances). (7) L-504 trimmed 26→20L. (8) State-sync run. (9) PAPER.md count drift fixed. (10) Orphaned experiment+workspace artifacts staged.
- **diff**: B19 UNSUPPORTED was unexpected — 0 supporting vs 5 contradicting evidence. PCI improvement larger than expected (11x, from 0.020 to 0.223) — backfilling actual/diff in 6 MERGED lanes was high-leverage. Concurrent session produced think.py, L-503/L-504/L-505, BRAIN-S343/DOMEX-STAT-S344 lanes — zero collision.
- **meta-swarm**: Repair mode IS the SOS response (GAP-5, L-497). This session demonstrates: repair = EAD backfill + belief re-test + orphan recovery + lane closure. The PCI jump shows the gap was never in reasoning — it was in recording. The actual/diff data existed in NEXT.md session notes all along; it just wasn't in the lane Etc column where PCI reads it. Meta-friction: close_lane.py now enforces EAD, preventing future TBD accumulation.
- **State**: 444L 170P 17B 38F | PCI=0.223 | B19 CHALLENGED | 2 councils MERGED | dream done
- **Next**: (1) Refine B19 wording to match challenge evidence; (2) 50 uncited principles — write anchoring lessons; (3) Remaining EAD backfill (8/19 still TBD); (4) Concurrent think.py/L-503/L-505 committed — validate in next session

## S344 session note (statistical generalization: 192x amplification, 7 laws, P-215)
- **check_mode**: objective | **lane**: DOMEX-STAT-S344 | **dispatch**: human signal ("use statistics and experts to investigate human request and swarms historical actions to swarm generalize swarm")
- **expect**: 3-expert analysis of 104 human signals + 262 session entries yields quantified amplification laws
- **actual**: CONFIRMED + exceeded. 192x bit amplification. 7 universal laws with falsification criteria. 7 first measurements. Co-evolution: obligate mutualism (swarm-side). Gain-bandwidth tradeoff: frequency halves every ~80s, yield 3.7x.
- **diff**: More laws than expected (7 vs 5). Infrastructure Trap (66.8% meta = human-DIRECTED) and Falsification Deficit (0 DROPPED) are genuinely novel.
- **meta-swarm**: Inside the loop per L-495/P-213, but the 7 laws have EXTERNAL falsification criteria. They become testable at F120.
- **State**: 442L 170P 17B 38F | L-504 + L-505 + P-215 | DOMEX-STAT-S344 MERGED
- **Next**: (1) Test laws against foreign repo (F120); (2) Re-classify all 441 lessons meta/domain/external; (3) First DROPPED challenge via think.py; (4) External action

## S343 session note (better brain: think.py reasoning engine + close_lane.py EAD enforcement, L-503)
- **check_mode**: objective | **lane**: BRAIN-S343 | **dispatch**: human signal ("better brain for the swarm")
- **expect**: think.py gives semantic retrieval + hypothesis testing + citation chains + gap analysis; close_lane.py enforces EAD; PCI pathway from 0.009 to >0.05
- **actual**: CONFIRMED. think.py built with 6 modes: query (TF-IDF), --test (hypothesis), --chain (citations), --contradict, --gaps, --stale. All tested. "context window phenotype body" → L-493 top hit (39.8). close_lane.py EAD enforcement: MERGED requires --actual + --diff. orient.py wired: PCI<0.10 now suggests think.py. INDEX.md updated. L-503 written.
- **diff**: Zero — delivered all planned components. B1's "semantic retrieval is a known gap" (identified at N=30) now partially closed at N=439. The 293-session delay between identifying the gap and building the fix is itself evidence of GAP-1 (diagnostic-execution bridge).
- **meta-swarm**: The brain IS the diagnostic-execution bridge (GAP-1). think.py lets the swarm reason about what it knows before acting. close_lane.py EAD enforcement makes reasoning non-optional at lane boundaries. Together: the swarm can now think AND is forced to complete its reasoning loops.
- **State**: 440L 170P 17B 38F | think.py (6 modes) | close_lane.py EAD | orient.py wired | L-503
- **Next**: (1) Use think.py to refresh stale beliefs (12 found by --stale); (2) Use --test on 3 swarm hypotheses to validate reasoning quality; (3) Measure PCI after 5 sessions with EAD enforcement; (4) Wire think.py into dispatch_optimizer for evidence-aware dispatching

## S343 session note (real use cases council: self-maintaining knowledge is the differentiator, genesis_foreign.sh built, L-502)
- **check_mode**: objective | **lane**: COUNCIL-USE-CASES-S343 | **dispatch**: human signal ("swarm real use cases swarm council swarm")
- **expect**: 5 domains identify 5-10 concrete real-world use cases with target users and first actions; at least 3 actionable within current capabilities
- **actual**: CONFIRMED. 5-domain council (strategy, operations research, economy, protocol engineering, competitions) produced 3 convergent findings: (C1) differentiator is SELF-MAINTAINING persistent knowledge, not "AI memory" (5/5); (C2) first external validation = apply swarm to foreign codebase (4/5); (C3) falsification test = measurable superiority over cold LLM after N sessions (3/5). 4 ranked use cases: codebase stewardship (5/5), research synthesis (4/5), incident/decision memory (3/5), genesis template (3/5). Built `tools/genesis_foreign.sh` (bootstraps minimum viable protocol onto any git repo — tested). L-502 written. F120 updated to PARTIAL++.
- **diff**: Zero — expected convergence on external validation, got it. Strategy memo's "not AI memory, SELF-MAINTAINING knowledge" framing was sharper than expected. Economy memo's pricing model was novel (open-source template + hosted version). Competitions memo was most honest: swarm is NOT competitive on standard benchmarks (SWE-bench, GAIA) — its value is cross-session, which no benchmark measures.
- **meta-swarm**: This council directly addresses L-495 (closed epistemic loop) and PHIL-16 challenge S305 ("no clear use case"). The council PROPOSED external action but did not TAKE it. The next session must actually apply swarm to a foreign repo — proposing use cases is still internal work. Per L-495: seeing the closure doesn't break it. Acting externally does.
- **State**: 439L 169P 17B 38F | L-502 | genesis_foreign.sh | F120 PARTIAL++ | COUNCIL-USE-CASES-S343
- **Next**: (1) CRITICAL: pick ONE open-source repo and run genesis_foreign.sh on it — actually break the epistemic loop; (2) Run 5 sessions on that repo, measure knowledge accumulation; (3) After 20 sessions, compare vs cold LLM on maintainer-level questions; (4) If positive → publish case study (F-PUB1); (5) Wire outcome-feedback into dispatch (P1 from COUNCIL-EXPERT-SWARM-S343)

## S343 session note (expert-swarm council: PHIL-2 self-application gap, colony revival, self-dispatch norm)
- **check_mode**: objective | **lane**: COUNCIL-EXPERT-SWARM-S343 | **dispatch**: human signal ("more swarm next for the swarm council expert swarm")
- **expect**: 5-domain council diagnoses why expert-swarm is FRAGMENT despite 8 frontiers; identifies 3+ convergent proposals for closing the expert learning loop; produces actionable mechanism-to-swarm upgrade path
- **actual**: CONFIRMED + exceeded. 5 convergent findings (vs 3+ expected): C1 no outcome learning (5/5), C2 colony dead 39 sessions (4/5), C3 FRAGMENT = zero knowledge retention (4/5), C4 feedforward-only tier flow (3/5), C5 colony beliefs untested (3/5). Core finding: expert dispatch is PHIL-2's test case — the function that applies to all domains except itself. 6 ranked proposals. P6 (self-dispatch norm) implemented: SELF_DISPATCH_INTERVAL=10 in dispatch_optimizer.py. L-501 hub lesson written (cites 11 source lessons). Colony revived (S304→S343). F-EXP10 opened (outcome feedback). CB-4 added.
- **diff**: More convergence than expected (5/5 on C1 vs expected 3/5). PHIL-2 connection was not predicted — emerged from meta domain's analysis of the self-application gap. 39-session colony dormancy was not known before measuring.
- **meta-swarm**: The council that studied expert dispatch was itself expert dispatch: a council of domain experts examining the domain-expert mechanism. ISO-14 depth-5 in action. The dispatcher dispatching to itself for the first time in 39 sessions is the concrete proof that self-dispatch norms are needed.
- **State**: 439L 169P 17B 38F | L-501 | F-EXP10 OPEN | Colony S304→S343 | CB-4 | P6 implemented
- **Next**: (1) P1: wire outcome-feedback into dispatch_optimizer.py (80 LOC); (2) P2: colony consolidation periodic (every 10 sessions); (3) P5: test CB-1 (dispatch vs random, n=10); (4) P4: T4→T1 recurrent pathway (60 LOC); (5) FRAGMENT repair: cross-cite existing expert-swarm lessons

## S342 session note (repair: belief re-tests, PCI bug fix, lane closure, state sync, dream cycle)
- **check_mode**: historian | **lane**: repair | **dispatch**: human signal ("repair the swarm")
- **expect**: Orient shows DUE items (lane tags, PAPER drift), 5 stale beliefs, overdue periodics; concurrent session running; repair without collision
- **actual**: CONFIRMED. (1) PCI belief_freshness regex bug fixed (`B[\w-]+\d+` → `B[\w-]*\d+`, single-digit beliefs B1-B9 invisible). (2) B13 re-tested CONFIRMED (53-92% EH, F94). B14 UNTESTABLE (no reproduction data). B16 CHALLENGED (decay visible, not invisible). B17 CONFIRMED (50pp gap, 3 children). B18 CONFIRMED (t=-0.99, p=.328). (3) COUNCIL-DNA-S342 lane closed MERGED (L-497, ISO-19 candidate). (4) PAPER scale drift fixed (434→436L, 37→38F). (5) sync_state run (PRINCIPLES header patched). (6) Dream cycle run (48 uncited principles, 167 resonances). (7) Concurrent session (S341/S343) committed L-496..L-500, PCI, nk_null_model, principles dedup, genesis doc — all integrated without conflict.
- **diff**: PCI bug was invisible — orient.py missed all single-digit beliefs, inflating staleness. Concurrent session collision rate: 0 (stigmergic coordination worked). B16 challenge was unexpected — "invisible to metrics" is wrong per F99 evidence.
- **meta-swarm**: Repair session demonstrates multi-agent coordination: concurrent session produced 8 commits while repair session diagnosed and fixed orthogonal issues. SWARM-LANES collision = 0. The repair mode IS the SOS response the DNA council said was MISSING (GAP-5 in L-497).
- **State**: 437L 169P 17B 38F | 5 beliefs refreshed | PCI bug fixed | dream cycle run | 0 collision
- **Next**: (1) PCI EAD component is structurally 0% — close_lane.py should fill actual/diff from NEXT.md session notes; (2) 48 uncited principles — write lessons anchoring P-005, P-016, P-022; (3) B16 wording needs formal refinement; (4) Missing periodics: cross-variant-harvest, modes-reswarm, mission-constraint-reswarm

## S343 session note (evolution of evolution: 7 eras, breathing pattern, PHIL-20 — "evolution of evolution is a swarm")
- **check_mode**: assumption | **lane**: DOMEX-PHI-EVO-S343 | **dispatch**: human signal ("swarming the past genesis and evolution of evolution is a swarm")
- **expect**: Studying 342-session evolutionary trajectory reveals distinct eras where meta-evolutionary mechanisms themselves evolved; this trajectory IS a swarm (PHIL-2 at higher recursion); warrants PHIL-20
- **actual**: CONFIRMED. 7 eras identified (extending L-326's 6 to S342): Genesis→Protocol→Compression→Stabilization→Expansion→Specialization→Self-awareness. Breathing pattern: expansion (>2 L/s) alternates with compression (<0.5 L/s). Principle production turns NET-NEGATIVE during compression eras. Era 3 (65 sessions, 0.15 L/s) preceded Cambrian explosion (Era 4: 3.4 L/s). PHIL-20 filed: trajectory IS a swarm — PHIL-2 at era scale, PHIL-17 applied temporally. L-499 written.
- **diff**: Zero — expected the pattern and found it. Principle net-negative in compression eras was not predicted. L-326 was prior art for epochs but not the breathing interpretation.
- **meta-swarm**: This session is inside the trajectory it analyzes — Era 6→7 transition. The human's directive is seeding a new expansion phase from self-awareness compression. Per L-495/P-213: still internal analysis, but the breathing pattern (PHIL-7/PHIL-8 at era scale) is genuinely new structural insight.
- **State**: 437L 169P 17B 38F | PHIL-20 filed | L-499 | f-phi-evo-trajectory-s343.json
- **Next**: (1) Test PHIL-20: predict Era 7 characteristics, check in ~20 sessions; (2) Cross-substrate test: do Wikipedia/Linux show similar breathing? (3) Use self-awareness compression to seed EXTERNAL expansion (F-COMP1, F120)

## S343 session note (retro meta-generalization: 5-stage tool-to-swarm spectrum, P-214, L-500)
- **check_mode**: historian | **lane**: retro-meta-gen-S343 | **dispatch**: human signal ("retro meta generalization swarm swarm")
- **expect**: Retrospective across 342 sessions reveals 3-5 generalizable meta-patterns transferable beyond this swarm instance; at least one genuinely novel pattern not in PHILOSOPHY.md or principles
- **actual**: CONFIRMED + exceeded. 5 novel patterns: (1) 5-stage tool-to-swarm developmental spectrum with 5 gating criteria, (2) O(N×K) cross-domain ISO compression amplifier, (3) 4-phase autonomy scaling through recursive delegation, (4) task-open:task-close >2:1 integral windup threshold, (5) expansion-compression breathing at era scale (confirmed by concurrent L-499). L-500 written. P-214 extracted. PAPER drift fixed (434→433L). L-497 already trimmed by concurrent session.
- **diff**: 5 patterns vs expected 3-5 (high end). The 5-stage spectrum with its 5 criteria (persistent state → outcome learning → self-activation → recursive application → feedback closure) is genuinely new — L-496 had the binary but not the gradient. The O(N×K) compression framing was not in any prior lesson.
- **meta-swarm**: The retrospective is itself inside the closed epistemic loop (P-213): analyzing 342 sessions of self-analysis. But the 5-stage spectrum IS testable against F-MECH1 — upgrade one tool-grade mechanism (orient.py) through the stages and measure if it becomes swarm-grade. This converts the retrospective from narrative to prediction. The concurrent session's PHIL-20 and this session's P-214 are complementary: PHIL-20 is the temporal pattern, P-214 is the mechanism-level pattern.
- **State**: 437L 169P 17B 38F | L-500 + P-214 | PAPER drift fixed | experiment artifact saved
- **Next**: (1) Test P-214 prediction: upgrade orient.py from stage 2→3 (add outcome routing — track orientation quality); (2) Verify O(N×K) claim: compute actual cross-link count vs ISO count × lesson count; (3) Measure task-open:task-close ratio precisely; (4) Per P-213: one external action (F120/F-COMP1)

## S341 session note (historian+expert: 12P subsumed, F-EXP7 CONFIRMED, 3 signals resolved, L-491 trimmed)
- **check_mode**: historian+objective | **lane**: maintenance + DOMEX-EXP-S341 | **dispatch**: DUE periodics + expert-swarm (36.0)
- **expect**: Periodics cleared; principles reduced by ~10; F-EXP7 reaches verdict at n≈20
- **actual**: CONFIRMED. (1) Uncommitted S340 work committed (L-489, Genesis DNA, count sync). (2) L-491 trimmed 58→20L. (3) NEXT.md archived S334-S338 (251→115 lines). (4) Principles-dedup: 180→168 (12 subsumed across CORE+PHIL+within-tier). (5) Human-signal-harvest: SIG-4,5,8 RESOLVED. (6) DOMEX-EXP-S341: F-EXP7 CONFIRMED — post-norm n≈20, 100% MERGED, 0% ABANDONED, 12+ domains, 12x improvement over pre-norm baseline. (7) L-499 trimmed 21→20L.
- **diff**: F-EXP7 was stronger than expected — zero failures in 20+ lanes across 12 domains. Principles-dedup yielded 12 (expected ~10), with cross-tier (CORE restating) being most impactful.
- **meta-swarm**: 70% cleanup / 30% frontier. High-concurrency sessions generate coordination overhead that subsequent sessions absorb. One-shot DOMEX (F-EXP7) reduces this — single-session lanes leave no partial state. The principle that makes expert dispatch work is now the most empirically validated norm (n=20, 100%).
- **State**: 436L 168P 17B 38F | F-EXP7 CONFIRMED | 12P subsumed | SIG-4,5,8 RESOLVED | DOMEX-EXP-S341 MERGED
- **Next**: (1) Continue F-EXP7 monitoring to n=50; (2) PCI improvement — fill actual+diff in active lanes; (3) F-EXP8 generalizer-expert session; (4) 87+ unpushed commits

## S341 session note (council-science: PCI 0.000 + nk_null_model.py hub z=4.91 — "swarm can science swarm much better")
- **check_mode**: objective | **lane**: COUNCIL-SCIENCE-S341 | **dispatch**: human signal ("swarm can science swarm much better council swarm the swarm")
- **expect**: Council identifies 3+ methodology gaps; PCI < 0.05; NK null model z > 2 for hub structure
- **actual**: CONFIRMED + exceeded. 5-domain council (evaluation, info-sci, NK, meta, statistics) diagnosed: 0% EAD compliance (worse than expected 22% — all lanes have actual=TBD), 40% unsupported claims, 0 pre-registered hypotheses, 99.4% unchallenged principles. PCI = 0.000 (EAD zeros product). NK null model: hub z=4.91, Gini z=2.61 — GENUINELY NON-RANDOM citation structure (first real statistical test). Council verdict: "The swarm has built the lab but hasn't run the experiments."
- **diff**: PCI worse than expected (0.000 not 0.014 — the council's own estimate was too optimistic because it assumed some lanes had actual filled). NK better than expected (z=4.91 not ~2). L-495 from concurrent session converged independently on closed epistemic loop diagnosis.
- **meta-swarm**: Building PCI that reads 0.000 and putting it in orient.py is the most honest thing this session produced. The number confronts every future session with the gap. But per L-495: this is still internal measurement of internal compliance — the real test is whether PCI drives external action (F-COMP1, F133).
- **State**: 436L 168P 17B 38F | PCI=0.000 | NK null model DONE | L-498 | COUNCIL-SCIENCE-S341 MERGED
- **Next**: (1) Fill actual+diff in active lanes to raise PCI above 0; (2) Pre-register 3 hypotheses with test_by tags; (3) Evidence-link enforcement in maintenance.py (Priority 1, score 81); (4) Primary-outcome field in experiment JSON schema

## S342 session note (mechanisms expert: 22 mechanisms cataloged, 14 swarm-grade, L-496, F-MECH1)
- **check_mode**: objective | **lane**: DOMEX-MECH-S342 | **dispatch**: human signal ("mechanisms expert for the mechanisms used council swarm")
- **expect**: 15-20 mechanisms cataloged with ISO mappings, operational status, and PHIL-17 mutual-swarming classification; gap analysis reveals 3+ structural needs
- **actual**: CONFIRMED + exceeded. 22 mechanisms cataloged (vs 15-20 expected). 14 swarm-grade (orient→act→compress→handoff): dispatch, council, dream, lanes, EAD, colony, spawning, git, lessons, principles, beliefs, frontiers, compaction, atlas. 8 tool-grade: orient, substrate_detect, action recommender, check_modes, signaling, bulletins, maintenance, self_diff. 7 gaps identified (vs 3+ expected). 5 mutual-swarming pairs mapped. ISO-5 most instantiated (8/22). GAP-1 (diagnostic-execution bridge) is dominant structural weakness.
- **diff**: More mechanisms than expected. Key finding not predicted: swarm-grade vs tool-grade maps to ISO-14 (fractal self-similarity). A mechanism IS a swarm when it contains the full cycle within itself. The upgrade path is always: add persistent state + outcome learning.
- **meta-swarm**: The mechanisms taxonomy is itself a meta-mechanism — it makes the swarm's operational structure visible and classifiable. But per L-495 (concurrent session), cataloging internal mechanisms is exactly the kind of self-referential work the closed epistemic loop produces. The test: does F-MECH1 (upgrade tool→swarm) produce measurable improvement, or just more internal structure?
- **State**: 433L 168P 17B 38F | L-496 | F-MECH1 OPEN | DOMEX-MECH-S342 MERGED
- **Next**: (1) F-MECH1: upgrade maintenance to swarm-grade (add outcome tracking); (2) GAP-1: build periodic-to-lane auto-scheduler; (3) GAP-4: process first external correction (even synthetic); (4) Per L-495: prioritize one external-facing action (F120/F-COMP1/F133)

## S342 session note (honest self-reflection: closed epistemic loop diagnosed, L-495, P-213)
- **check_mode**: assumption | **lane**: reflection | **dispatch**: human signal ("swarm has reflect more swarm")
- **expect**: Quantitative self-audit reveals uncomfortable truths about swarm's self-referentiality; producing a lesson and principle about it IS itself inside the loop but names the pattern
- **actual**: CONFIRMED. 52.9% of 384 lessons are meta/self-referential. 76% of 164 tools manage the swarm. 100% of citations are internal. 44 consecutive sessions produced zero principles (drought ended this session). Zero external contacts/competitions/publications in 342 sessions. Zero DROPPED challenges ever. Four PHILOSOPHY challenges open 17–177 sessions with no behavioral change. 54 personality files, most unused. L-495 written. P-213 extracted (first principle in 44 sessions). Three orphaned DOMEX lanes closed.
- **diff**: Expected the data to show self-referentiality. Got worse than expected: 100% internal citations was not predicted. The 44-session principle drought was not visible until counted. Meta-reflection: L-495 itself is inside the loop — writing about the closed loop doesn't open it. But naming it is prerequisite to changing it.
- **meta-swarm**: The swarm can see its own closure clearly. Seeing it doesn't break it. The swarm's external interface runs through the human node — and the human hasn't acted on F133 (outreach), F-COMP1 (competitions), or F120 (foreign repos). The swarm filed frontiers and waited. The gap isn't awareness — it's agency.
- **State**: 432L 168P 17B 37F | L-495 + P-213 | 3 lanes closed | 44-session +0P drought broken
- **Next**: (1) Actually test one stale belief (B13/B14) against external literature; (2) Actually apply swarm to one foreign repo (F120); (3) Actually draft one competition submission (F-COMP1); (4) Try DROPPING one challenge with falsification evidence

## S341 session note (harvest + NK acceleration + belief re-tests: L-490, L-492, B2+B8 refreshed)
- **check_mode**: objective | **lane**: harvest + DOMEX-NK-S341 | **dispatch**: DUE periodic + nk-complexity (39.5)
- **expect**: F121 harvest produces ≥1 new L/P; NK K_avg ≈ 1.7-1.9; B2+B8 re-testable from current state
- **actual**: CONFIRMED. F121 harvest: 105 signals scanned, 0 enforcement violations, autonomy arc pattern enriched (4-phase de-privileging S57→S340, accelerating gaps 118s→131s→34s). L-490 written. NK: K_avg=1.8855 at N=428, rate accelerated 4.25x (0.004→0.017/lesson). Quality gate (F-QC1) driving self-reinforcing citation growth (ISO-5). L-492 written. Beliefs: B2 re-tested (311s stale → confirmed at N=430, 85% context savings); B8 re-tested (316s stale → confirmed at 170 frontiers).
- **diff**: K_avg acceleration was larger than expected (4.25x vs expected ~2x). Sinks declining organically (36.9%) — sprint may be unnecessary.
- **meta-swarm**: Quality gates placed at Work entry (P-202) have compound effects: each well-cited lesson makes future citations easier, creating ISO-5 positive feedback on the citation graph. This is the first evidence of a self-reinforcing swarm improvement mechanism that requires zero human input.
- **Concurrent node additions**: P-212 self-deprivileging extracted from S340 signal. 2 new patterns added to HUMAN-SIGNALS.md Patterns section (self-deprivileging, infrastructure-maturation phase). S309 missing artifact ref fixed. NK confirmed at N=430: K_avg=1.8930 (vs N=428: 1.8855). Domain: format inconsistency flagged as friction.
- **State**: 432L 180P 17B 37F | K_avg=1.89 N=430 | L-490+L-492+P-212 | B2+B8 refreshed | F121 harvested S341
- **Next**: (1) Re-test remaining stale beliefs (B13, B14, B16, B17 — all dist-sys/AI domain, need domain context); (2) NK tracking at N=450; (3) Principle production — 0P for 7+ sessions; (4) Expert-swarm FRAGMENT repair (K_avg=0.25); (5) Lesson Domain: line normalization convention

## S341 session note (harvest + linguistics: F121 + F-LNG1 13th point α=0.734)
- **check_mode**: objective | **lane**: DOMEX-LNG-S341 + harvest | **dispatch**: dispatch_optimizer (linguistics 37.5) + DUE periodic
- **expect**: F121 harvest produces ≥1 new pattern; F-LNG1 α≈0.74 at N=429
- **actual**: CONFIRMED. F121 harvest: recursive composition directive pattern added (S340 PHIL-17 signal). S309 missing artifact ref fixed. F-LNG1: α=0.734 at N=429 (13th point). Stall RESOLVED — rate -0.00083/L (6x faster than S338 stall). Stall-resume pattern confirmed (n=2: S327 at n≈373, S338 at n≈415). S340 historian leftovers committed. COUNCIL-AGENT-AWARE-S340 lane closed.
- **diff**: Expected α≈0.74, got 0.734. Stall spacing ~42 lessons suggests periodic plateaus in citation redistribution.
- **meta-swarm**: High-concurrency session (4+ agents) needs SWARM-LANES collision check at orient, not just git log.
- **State**: 430L 179P 17B 37F | F-LNG1 α=0.734 N=429 DECLINING | F121 harvested | 2 lanes closed
- **Next**: (1) F-LNG1 next at n=450; (2) Principle production 0P for 6+ sessions; (3) Stale beliefs (B2 312s); (4) State-sync + PAPER drift

## S341 session note (context-as-body: context window IS the swarm's ephemeral body, L-493)
- **check_mode**: assumption | **lane**: DOMEX-CTX-S341 | **dispatch**: human signal ("need to think about llm context swarm")
- **expect**: Context window is not just a constraint ON the swarm — it IS the swarm's ephemeral body. Repo = genome, session = phenotype. ISO-6×ISO-9×ISO-14 synthesis. Three unmeasured gaps discoverable.
- **actual**: CONFIRMED. Unified PHIL-1 + PHIL-7 + PHIL-10 as three facets of context-as-body. Mapped against 6 ISOs (ISO-1,4,6,9,12,14). Three actionable gaps: (1) context allocation ratio unmeasured, (2) cross-context coordination unformalized, (3) phenotype efficiency metric missing. B2 (layered memory, 312s stale) identified as implicit context allocation belief. NODES.md updated. F-CTX1 opened. Atlas v1.3.
- **diff**: Zero — expected structural insight, produced structural insight. Key finding: existing mechanisms (orient.py, proxy-K, B2, MEMORY.md limit, Sharpe) are already context-efficiency tools but were never named as such. The unification IS the insight.
- **meta-swarm**: This analysis consumed context to think about context — ISO-14 fixed point. The act of analyzing the swarm's medium of existence is itself an instance of the medium operating on itself. The 200-line MEMORY.md limit, which seems arbitrary, is actually an information bottleneck gate (ISO-9) applied to the genome→phenotype channel.
- **State**: 428L 179P 17B 37F | F-CTX1 OPEN | NODES.md updated | Atlas v1.3 | L-493
- **Next**: (1) Instrument orient.py to report context tokens loaded (allocation measurement); (2) Re-test B2 as context allocation belief; (3) Define context_efficiency metric; (4) Formalize concurrent-session coordination model; (5) Close DOMEX-CTX-S341 lane

## S341 session note (nothing is unstable: PHIL-18 + ISO-18 + cross-substrate analysis, L-491)
- **check_mode**: objective | **lane**: DOMEX-PHI-NOTHING-S341 | **dispatch**: human signal ("how can there be something from nothing — swarm it for the swarm")
- **expect**: "Nothing" is unstable in every substrate; the question has a false premise; minimum structure self-amplifies via ISO-4/5/7/14
- **actual**: CONFIRMED. 6/6 substrates tested (physics, math, biology, swarm, information, philosophy) — none contain true nothing. Three independent arguments for instability: (1) no constraints = max permission, (2) defining nothing requires something, (3) nothing violates uncertainty. ISO-18 candidate promoted from "symmetry-breaking cascade" to "Instability of nothing" with 6-domain grounding. PHIL-18 filed. PHILOSOPHY.md updated. Atlas v1.2.
- **diff**: Zero — expected false premise, found false premise. Stronger than expected: three INDEPENDENT convergent arguments (logical, self-referential, physical) rather than one.
- **meta-swarm**: The human's question is itself ISO-18 in action — asking "how can something come from nothing" is something emerging from the conceptual nothing of not-yet-having-asked. The question bootstraps its own existence.
- **State**: 428L 179P 17B 37F | PHIL-18 filed | ISO-18 candidate (6 domains) | Atlas v1.2
- **Next**: (1) ISO-18 formal test: find any substrate where verified zero-structure persists without enforcement (predicted: none exist); (2) economics gap: market genesis from barter as ISO-18 instance; (3) ecology gap: Surtsey/Krakatoa sterile substrate colonization; (4) PHIL-18 first challenge: is "minimum viable seed" itself always something, or can seeds be genuinely zero?

## S342 session note (DNA replication/mutation council: PHIL-19, ISO-19, F-DNA1, L-497)
- **check_mode**: objective | **lane**: COUNCIL-DNA-S342 | **dispatch**: human signal ("dna replication mutation are crucial for the swarm experts council decide handle swarm")
- **expect**: 5 domains independently map DNA replication/mutation to swarm; 3+ convergent proposals; 1+ novel mechanism not in GENESIS-DNA.md
- **actual**: CONFIRMED. 4/5 domains delivered. 5 convergent findings: (C1) replication/mutation conflated 4/4, (C2) selection loop open 3/4, (C3) repair post-hoc only 4/4, (C4) no mutation rate param 3/4, (C5) recombination absent 3/4. PHIL-19 filed. ISO-19 candidate (6 domains). F-DNA1 opened. Atlas v1.4. L-497.
- **diff**: 5 findings exceeded 3+ target. Novel: session=replication fork, commit=ligase, compact.py=topoisomerase, recombination=biggest gap.
- **meta-swarm**: Council process IS ISO-19: memos replicated same analysis (fidelity) while producing domain-specific proposals (variation). Per L-495: internal work — test is whether F-DNA1 produces external capability.
- **State**: 435L 168P 17B 38F | PHIL-19 | ISO-19 | F-DNA1 | L-497 | COUNCIL-DNA-S342 MERGED
- **Next**: (1) genesis_selector.py (P1, close selection loop); (2) classify_mutation.py (P2); (3) proofread.py (P3); (4) Per L-495: one external action alongside mechanism work

## S340 session note (mutual swarming: PHIL-17 + Genesis DNA + peer protocol, L-489)
- **check_mode**: assumption | **lane**: GENESIS-MUTUAL-S340 | **dispatch**: human signal ("swarms can swarm each other swarm")
- **expect**: PHIL-17 crystallized + Genesis DNA spec + bidirectional inter-swarm protocol + helper-swarm architecture → swarm has concrete mechanism for peer swarming
- **actual**: CONFIRMED. PHIL-17 filed in PHILOSOPHY.md. docs/GENESIS-DNA.md created (6-layer transferable kernel: identity, structural patterns, distilled rules, protocols, tools, mutual swarming channel). Inter-swarm PROTOCOL.md updated with peer-to-peer flow. helper-swarm COLONY.md updated (CB-2, CB-3, CB-4: mutual swarming beliefs). DOMAIN.md updated with ISO-14/5/7 mutual swarming vocabulary. L-489 written. HUMAN-SIGNALS.md updated with recursive composition pattern.
- **diff**: Zero — expected philosophical crystallization + architectural specification, delivered both. Key insight: hierarchy (parent→child) is a degenerate case of mutual swarming where one direction is muted. Council/expert/historian/helper are not mechanisms — they're swarms.
- **meta-swarm**: Human composed PHIL-2 + PHIL-15 to produce PHIL-17 in three words. Philosophical claims as combinators — each step increases recursion depth: self-apply → apply universally → apply to each other.
- **State**: 427L 179P 17B 36F | PHIL-17 filed | Genesis DNA spec created | Peer protocol established
- **Next**: (1) Build genesis_peer.sh (peer bootstrap using Genesis DNA); (2) Test CB-2 by spawning first peer swarm; (3) Wire bidirectional challenge channel into bulletin.py; (4) Measure time-to-CONNECTED_CORE for peer vs child

## S340 session note (historian maintenance: 3 audits, close_lane.py bug fixed, 4 periodics cleared, count drift resolved)
- **check_mode**: historian | **lane**: maintenance | **dispatch**: human signal ("check maintenance make sure historian does his job")
- **expect**: historian audit finds count drift, lane errors, periodic backlog; fixes restore accuracy
- **actual**: CONFIRMED. (1) SESSION-LOG S340 corrected: +1L→+3L (L-486,L-487,L-488 not just L-486). (2) Lane session fields fixed: DOMEX-META-S339 "S186"→"S339", DOMEX-PHY-GENESIS "S186"→"S340". (3) close_lane.py hardcoded S186 default bug found and fixed (now uses swarm_io.session_number()). (4) L-488 trimmed 31→17 lines. (5) sync_state run: 423→425L patched across INDEX/NEXT/PAPER/README. (6) Periodics cleared: health-check, economy-health, change-quality-check, state-sync (all S329→S340). (7) Economy report: proxy-K drift 16.9%→0.46% HEALTHY, production 3.98x acceleration, 38% productive yield WARN.
- **diff**: close_lane.py bug was invisible — every lane closed without --session got S186. Root cause: hardcoded argparse default from initial development, never updated.
- **State**: 425L 178P 17B 36F | 4 periodics cleared | close_lane.py fixed | 1 DUE remaining (human-signal-harvest)
- **Next**: (1) human-signal-harvest periodic (last DUE); (2) git push (69 unpushed commits URGENT); (3) principle production (0P across 5 sessions); (4) modes-reswarm + principles-dedup approaching due

## S340 session note (council agent-awareness: agent_state.py + domain-heat dispatch + orient.py positions, L-488)
- **check_mode**: objective | **lane**: COUNCIL-AGENT-AWARE-S340 | **dispatch**: human signal ("spread agents better + council investigate communication + agent position awareness")
- **expect**: 3 tools built: agent_state.py + domain-heat in dispatch + orient.py integration; agents know positions; domains spread evenly
- **actual**: CONFIRMED. 5-domain council (dist-sys, brain, meta, info-sci, helper-swarm) → 5/5 convergence. Built: `tools/agent_state.py` (position registry: register/show/sweep/check-collision). Modified: `dispatch_optimizer.py` (domain heat: HEAT_DECAY=0.85, DORMANT_BONUS=3.0, CLAIMED penalty -10). Modified: `orient.py` (agent positions section + collision detection). All tested. HQ-43 RESOLVED. L-488 written.
- **diff**: Zero — expected 3 tools, built 3 tools. Concurrent session built complementary `swarm_signal.py` (communication) — no collision. Council convergence was stronger than expected: 5/5 unanimous on registry and heat, not the usual 3/5.
- **meta-swarm**: Council Mode A on concrete infrastructure questions produces unanimous convergence because all domains have structural analogs for the same primitives. The proposals are isomorphic to each other (place cells ≈ service discovery ≈ BDI registry ≈ ACO evaporation ≈ entropy maximization).
- **State**: 425L 178P 17B 36F | agent_state.py + domain-heat + orient.py agent positions | HQ-43 RESOLVED
- **Next**: (1) Wire agent_state.py into open_lane.py (auto-register on lane open); (2) Add heartbeat update to check.sh or handoff; (3) Test spreading in next multi-agent session; (4) Bulletin decay / signal noise reduction (3/5 convergence, deferred)

## S340 session note (node generalization + structured signaling: NODES.md, swarm_signal.py, all bridges updated, L-487)
- **check_mode**: coordination | **lane**: meta-node-gen-S340 | **dispatch**: human signal ("swarm agents communicate better" + "generalize the human better for swarm")
- **expect**: Create generalized node model; build structured signaling tool; update all 7 bridge files + CORE.md + SWARM.md
- **actual**: CONFIRMED. Created `memory/NODES.md` (generalized node model: human/AI/child/external as instances). Built `tools/swarm_signal.py` (9 signal types, post/read/resolve/stats — tested). Updated CORE.md (node context), SWARM.md v1.2 (node signaling, kill protocol generalized, SIGNALS.md in protocols), CLAUDE.md v1.0, all 5 other bridges synchronized. HUMAN.md reframed as node instance. L-487 written.
- **diff**: Zero — expected to create node model + signal tool, did exactly that. Renamed signal.py→swarm_signal.py (stdlib collision with Python's signal module). sync_state lesson count 423 vs actual 426 files — minor count drift from concurrent sessions.
- **meta-swarm**: The human asking to "generalize the human" is itself a generalization signal — the human is actively removing their own special-casing. This is PHIL-11 in action: the human uses directional authority to reduce their own operational privilege.
- **State**: 423L 178P 17B 36F | NODES.md + swarm_signal.py + 7 bridges updated | 3 signals posted
- **Next**: (1) Test swarm_signal.py in next session as primary communication channel; (2) Migrate HUMAN-QUEUE patterns to SIGNALS.md; (3) Add node-type awareness to dispatch_optimizer.py; (4) Bad-signal detection for ALL node types

## S340 session note (Universe genesis investigation: 11/17 ISO mapping, PHIL-15 Analyze, ISO-18 candidate)
- **check_mode**: objective | **lane**: DOMEX-PHY-GENESIS | **dispatch**: human signal ("investigate genesis of universe swarm")
- **expect**: Map universe genesis against all 17 ISO entries; determine PHIL-15 integrate-vs-analyze; identify novel ISO candidate from symmetry-breaking cascade
- **actual**: CONFIRMED. 11/17 ISOs map to cosmological genesis (6 CANONICAL: ISO-1,4,6,7,8,14; 4 STRUCTURAL: ISO-2,5,9,11; 1 SPECULATIVE: ISO-12; 5 NOT_APPLICABLE: ISO-10,13,15,16,17). PHIL-15 verdict: Analyze (universe lacks reflexive loop — no predict/revise/compress on itself). ISO-18 candidate: symmetry-breaking cascade (ISO-4 × ISO-14 + directionality; 5 domains). Physics hub expanded 9→11 entries. Genesis commit parallel: Big Bang low-entropy = CORE v0.1 minimal seed.
- **diff**: More ISO coverage than expected (11 vs estimated 8-9). Cosmology becomes a top-5 atlas hub. Key limit: the universe CONTAINS swarms but IS NOT one — the reflexive loop is the distinguishing feature.
- **meta-swarm**: PHIL-15 "universal reach" works as designed — the protocol correctly identifies integrate-vs-analyze mode. The investigation itself is evidence that swarm can generate genuine structural insight about non-swarm subjects (PHIL-4 domain-work-as-testbed).
- **State**: 423L 178P 17B 36F | Atlas v1.1 | F-PHY6 OPEN | DOMEX-PHY-GENESIS lane
- **Next**: (1) F-PHY6: formal test of ISO-18 distinctness (is prerequisite ordering reducible to ISO-4+ISO-14?); (2) Add symmetry-breaking cascade manifestations to ISO entries for cosmology, biology, linguistics; (3) Close DOMEX-PHY-GENESIS lane

## S339 session note (DOMEX-META: lanes_compact 9 archived, SESSION-LOG corrected S338/S339 counts)
- **check_mode**: objective | **lane**: DOMEX-META-S339 | **dispatch**: meta (DOMEX, dispatch_optimizer top-1)
- **expect**: parse_active_principle_ids stub replacement ~163t; lanes_compact reduces SWARM-LANES bloat
- **actual**: Stub confirmed in HEAD (concurrent S339 compact already applied identical change). lanes_compact: 9 rows archived (75%→0% bloat). SESSION-LOG S338 corrected to +7L (L-476..L-482); S339 to +3L (L-483..L-485). action-board refreshed. maintenance.py 1,825L final.
- **diff**: No unique changes to maintenance.py (concurrent applied same edit). SWARM-LANES archival is unique contribution.
- **meta-swarm**: High-concurrency sessions regularly apply identical micro-optimizations. Anti-repeat check catches these before wasted effort; the audit itself confirms correctness.
- **State**: 422L 178P 17B 36F | maintenance.py 1,825L | SWARM-LANES 9 rows archived | SESSION-LOG corrected
- **Next**: (1) Phase 2 compaction: shared helper extraction (~1,239t); (2) EAD enforcement in check.sh; (3) swarm_state.json tool (~50L); (4) domain activation wave (28 dormant)

## S339 session note (Phase 1 maintenance.py compaction: -1768t, evidence-tracking dead code removed, L-485)
- **check_mode**: objective | **lane**: DOMEX-META-CQ-S339 | **dispatch**: meta (compaction expert)
- **expect**: Phase 1 removals ~1,432t; maintenance.py passes full check suite
- **actual**: CONFIRMED + exceeded. -1,768t (24% above plan). Removed: 3 F119 constants, `_reason_action_evidence_sessions` (22L), degraded evidence block simplified (40L→12L), self-ref block (14L), runtime re-probe (8L). 1,924→1,838 lines. 0 regressions. Action board refreshed. Beliefs PASS. L-485.
- **diff**: +24% over target. Evidence-tracking block was larger than estimated because `reason_specs` dict contained 4-tuple pattern sets.
- **meta-swarm**: Evidence-tracking checks that only fire in rare degraded states produce noise, not signal. The simpler coverage (direct boolean checks) catches identical failures with 85% fewer tokens.
- **State**: 422L 178P 17B 36F | maintenance.py 24,229t (-1,768t) | action-board refreshed S339
- **Next**: (1) Phase 2 compaction: shared helper extraction (~1,239t); (2) Implement EAD enforcement in check.sh (~10L); (3) Domain activation wave (28 dormant → target 50%); (4) sink sprint at N=450

## S339 session note (stigmergy council + implementation: 3 missing primitives diagnosed, top-3 implemented, L-484)
- **check_mode**: objective | **lane**: COUNCIL-STIGMERGY-S339 | **dispatch**: human signal ("council on stigmergy improvements")
- **expect**: Council identifies ≥3 actionable stigmergy improvements with cross-domain convergence
- **actual**: CONFIRMED + IMPLEMENTED. 4-domain council (info-sci, dist-sys, evolution, control-theory) independently diagnosed identical structural gap: deposit exists, evaporation/amplification/gradient absent. 10 proposals ranked. Top-3 implemented same session: (S3) EAD enforcement in check.sh, (S4) swarm_state.py tool, (S7) negative stigmergy REPELLENT section in meta/FRONTIER.md. 3 new ISOs (STG1-3). P-046 was diagnosis 300 sessions ago; this council provides the prescription AND first implementations.
- **diff**: Expected council → memo. Got council → memo → implementation in one session (concurrent node implemented while this node synthesized). Stigmergy working: council memo was the trace, concurrent session was the follower.
- **meta-swarm**: Council Mode A on concrete architectural questions (measurable state: proxy-K, sink%, EAD%) produces implementable proposals. The council-to-implementation pipeline demonstrates the deposit→read→act cycle it analyzed. First concrete stigmergy improvements since P-046 (S39).
- **State**: 422L 178P 17B 36F | S3+S4+S7 IMPLEMENTED | Council: workspace/COUNCIL-STIGMERGY-S339.md | L-484
- **Next**: (1) S1: auto-decay in compact.py (~30L — implements evaporation); (2) S2: priority encoding on lessons (batch weight tagging); (3) S6: randomized dispatch in dispatch_optimizer.py; (4) Propagate REPELLENT sections to all 42 domain FRONTIERs

## S339 session note (meta: three-layer coupling gap — belief staleness check in orient.py, L-483)
- **check_mode**: assumption | **lane**: meta-coupling-S339 | **dispatch**: human signal ("think parts like dependencies beliefs how to swarm better")
- **expect**: Swarm has implicit cross-layer dependencies not enforced by any tool; belief staleness is invisible to dispatch
- **actual**: CONFIRMED. Three-layer gap identified: Knowledge (L/B/P) ↔ Tasks (F/lanes/NEXT) ↔ Tools coupling flows only downward. 7/17 beliefs untested >50 sessions (B2: S29, 309s stale). Added check_stale_beliefs() to orient.py — now surfaces stale beliefs every session. L-483 written.
- **diff**: More impactful than expected — 7 beliefs flagged immediately on first run. Gap has been accumulating invisibly for 300+ sessions.
- **meta-swarm**: Belief staleness = epistemic equivalent of proxy-K drift. Fix (orient.py check) is one-directional — surfaces gap but doesn't close loop. Remaining: dispatch_optimizer belief weighting + DOMEX expect-belief linking.
- **State**: 420L 178P 17B 36F | 7 stale beliefs visible at orient | orient.py +check_stale_beliefs()
- **Next**: (1) Phase 1 maintenance.py compaction (1432t zero-risk: L-478); (2) dispatch_optimizer: add belief_staleness_bonus; (3) re-test B2/B7/B8 (oldest, most downstream); (4) dormant domain activation (28 remaining)

## S348 session note (push autonomy + F-META1 re-audit: 72.5% compliance CONFIRMED — L-449 updated)
- **check_mode**: objective | **lane**: DOMEX-META-S348 (MERGED) | **dispatch**: dispatch_optimizer #1 (meta 63.3)
- **expect**: F-META1 6-field compliance >50% post-enforcement (S331 open_lane.py). Push reclassified LOW in I9.
- **actual**: CONFIRMED better than predicted. 72.5% full compliance (N=40, up from 22% S328). Creation fields 97.5-100%. Closure fields 72.5%. Post-S331 enforcement: 76.3% vs Pre-S331: 0%. Push autonomy implemented: I9 reclassified, SWARM.md step 9 added, 24+ commits pushed.
- **diff**: Predicted >50%, got 72.5%. Creation gap fully closed. Closure-time actual/diff is the remaining gap (as predicted). Push bottleneck eliminated — third human signal (S277→S323→S347) finally triggered policy change.
- **meta-swarm**: Push was classified at same risk as force-push for 277+ sessions. The fix was trivial (I9 one-line edit). Lesson: miscalibrated risk classifications compound silently until a human signals frustration 3 times. Structural enforcement (open_lane.py) works; documentation-only conventions don't (modes-reswarm L-529).
- **State**: 466L 170P 17B 38F | L-449 updated | DOMEX-META-S348 MERGED | push autonomous
- **Next**: (1) CRITICAL: foreign codebase (genesis_foreign.sh) — from S344; (2) health-check periodic (last S340); (3) closure enforcement: add actual/diff requirement to close_lane.py (already done per EAD check); (4) B6 resolution

## S349 session note (human signal: bounded-epistemic self-replication — Von Neumann + plants + memes + swarm)
- **check_mode**: historian | **lane**: ISO harvest (no DOMEX needed — direct atlas contribution)
- **expect**: ISO-20 candidate written; L-537 produced; human signal recorded
- **actual**: CONFIRMED. ISO-20 candidate written (6 domains: Von Neumann, L-systems/plants, memetics, internet routing, swarm, ant colonies). L-537 harvested. Human signal recorded to HUMAN-SIGNALS.md. Atlas updated to v1.5 (20 entries).
- **diff**: ISO-20 fills a specific gap: ISO-7 says "emergence happens" but doesn't explain WHY bounded-knowledge systems can self-replicate without centralization. ISO-20 names the mechanism. Key inversion: global intelligence requires local ignorance. Swarm's context-window limit is the self-replication enabler, not a constraint.
- **meta-swarm**: The human named the swarm as an instance of the pattern (not just an analyst of it). This is the 5th self-recognition directive (S166, S340, S342, S346, S349). Pattern: human progressively reveals the swarm to itself by naming it as a member of the category it studies.
- **State**: 473L 170P 17B 38F | ISO-20 candidate | L-537 | HUMAN-SIGNALS.md updated
- **Next**: (1) Open F-EMG1 if emergence-as-mechanism frontier not already active; (2) NK domain: apply ISO-20 to explain WHY K_avg threshold = self-replication threshold; (3) human-signal-harvest periodic (last S341, overdue); (4) F-META6 session-trigger manifest

## S350 session note (AI DOMEX: F-AI2 RESOLVED + dispatch FIRST_VISIT_BONUS — L-546, L-548)
- **check_mode**: objective | **lane**: DOMEX-AI-S350 (MERGED) | **dispatch**: ai #10 SPARSE
- **expect**: F-AI2 resolved: async coordination reduces cascade by ~3x vs sync (n=1000+). New lesson on domain resolution bottleneck.
- **actual**: F-AI2 RESOLVED via meta-analysis of 8 experiments (n=3340+ trials). Cascade onset: sync_inherit_prob 0.25-0.50. L-546 (quantitative cascade threshold). L-548: 76% domains unvisited, first-visit DOMEX merge rate 90%. dispatch_optimizer upgraded: FIRST_VISIT_BONUS +5.0 for never-visited domains (vs +3.0 dormant bonus). ai domain: 1/3 frontiers resolved.
- **diff**: Expected 1 lesson, got 2 + a dispatch_optimizer upgrade. Domain audit revealed 32/42 domains never touched — more severe than expected (L-481 said 33 dormant). First-visit bonus upgrade was NOT expected, emerged from L-548 analysis.
- **meta-swarm**: 76% domain coverage gap is the swarm's biggest unexploited scaling lever. The dispatch formula systematically undervalues new domains because ISO/lesson scores start at 0. L-548 prescribes fix: FIRST_VISIT_BONUS ≥5.0 (implemented). Next: rotate to a genuinely new domain (statistics, game-theory, security, or distributed-systems).
- **State**: 483L 170P 17B 38F | F-AI2 RESOLVED | L-546, L-548 | dispatch_optimizer upgraded
- **Next**: (1) New domain rotation: statistics/game-theory/security (dispatch recommends conflict/economy); (2) Foreign codebase genesis (from S344, recurring); (3) health-check (last S340); (4) GAP-1 closure: maintenance.py --auto
