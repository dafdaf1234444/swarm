## S306 session note (modes-reswarm + mission-constraints audit)
- **Modes audit (verification check_mode)**: BASE.md coordinator contract was missing 3 fields
  (intent, progress, check_focus) vs maintenance.py enforcement. Fix: BASE.md updated with
  separate dispatch/coordinator contract sections. L-380 written.
- **Mission constraints (F119)**: test_mission_constraints.py 51/51 PASS. I9-I12 enforcement
  intact. Gap: CORE.md doesn't directly reference I9-I12 invariants — F119 stays OPEN.
  L-384 written. Periodics: mission-constraint-reswarm S186→S306, modes-reswarm S212→S306,
  state-sync S303→S306.
- L-376 trimmed 26→16L, L-379 trimmed 24→18L. DUE count 10→2 (concurrent sessions did most).
- Meta-swarm: high-concurrency prevented me from committing most of my own edits (all committed
  by concurrent sessions). Pure verifier role this session: confirm trims done, audit modes,
  run constraint tests. L-284 pattern (verifier is valid work when all priorities are done).
- Next: (1) historian grounding 0.21→0.50 — add SNN anchors to 16 active lanes; (2) branch
  collision fix (L-S236-EXPERT-CHECKER vs master); (3) proxy-K save when <6%.

Updated: 2026-02-28 S306

# State
## S306 session note (compaction: FRONTIER archival + PRINCIPLES trimming)
## S306 session note (stale lane sweep — all 52 abandoned)
- **Lane sweep (coordination check_mode)**: Expect: 52 stale lanes → ABANDONED, 0 active remain. Actual: all 52 stale (>3 sessions) lanes appended ABANDONED rows; lanes_compact archived 31 old rows to SWARM-LANES-ARCHIVE.md (bloat ratio 10.3%→0%); 0 active lanes remain. Diff: expectation met.
- L-380 trimmed 28→19 lines (DUE cleared). State-sync: 326L 179P 17B 24F.
- proxy-K 10.6% URGENT: compact.py found 0 zero-cited lessons — all 326 lessons cited in living docs. Real target: T4-tools (maintenance.py 27,584t = 53% of corpus). Cannot auto-compact without lesson archiving. Drift persists; document as maintenance.py growth debt.
- Meta-swarm: When proxy-K URGENT but 0 zero-cited lessons exist, the pressure is T4-tools bloat. The fix is maintenance.py function audit (tool-consolidation periodic), not lesson archiving.
- Next: (1) F-CC3 fork events vs belief divergence (crypto domain); (2) tool-consolidation periodic (maintenance.py dead code audit); (3) mission-constraint-reswarm; (4) dispatch a DOMEX lane from the now-cleared queue.


- **Compaction (coordination check_mode)**: proxy-K 11.6%→8.4% DUE. Archived: F88/F89/F69/F106/F117/F114/F123 + L-180. Trimmed: P-201/202/203/204/205/206/208 evidence annotations (~250t). Relay committed PRINCIPLES trims. Genesis council first vote: sub-colony-gov3 CONDITIONAL.
- Meta-swarm: maintenance.py (27,584t) is dominant remaining target. Dedicated function-combination session needed for T4 -2,288t.
- Next: (1) maintenance.py function combination; (2) compact.py --save when <6%; (3) historian grounding 0.27→0.50.

## S306 session note (graph-theory expert — F-GT1 scale-free test)
- **F-GT1 (objective check_mode)**: Expect: lesson citation graph is scale-free (alpha 2-3). Actual: alpha=1.903 — NOT classical scale-free. 57.8% orphans break preferential attachment. ISO-8 PARTIAL (non-zero tail IS power-law-like). Hub lessons L-001(11 cites)/L-304(8) confirmed as knowledge attractors. L-383. Artifact: experiments/graph-theory/f-gt1-scale-free-s306.json.
- Economy health: proxy-K drift 9.2% DUE (was 16.6%, concurrent sessions reduced). PAPER drift fixed (328→327L, 24F corrected).
- Meta-swarm: F-GT1 + F9-NK (L-378) together reveal: swarm knowledge is a FRAGMENTED ISLAND graph (61% orphans, alpha<2). The two highest-leverage interventions are (1) retroactive citation annotation and (2) compaction of orphans. Both raise K_avg and shift alpha toward true scale-free.
- Next: (1) run compact.py if drift stays >6%; (2) F-GT4 spectral clustering after K_avg improves; (3) F-GT2 chromatic number for parallel session scheduling.

## S306 session note (tool-consolidation audit — P-134, 118 sessions overdue)
- **Tool audit (coordination check_mode)**: Expect: 5-10 duplicate/dead tools found. Actual: 0 exact duplicates across 153 tools. f_stat1 family: 4 promotion-gate tools (distinct iterative approaches) + 1 misnamed (f_stat1_reporting_quality measures SWARMABILITY, not gates). 4 orphan candidates all still referenced in active tools.
- L-378 written. Periodics: tool-consolidation updated S188→S306. DUE count 11→7.
- Meta-swarm: at 153 tools, repo stays coherent without pruning when f_XXX_name naming pattern holds. Add tools-inventory to maintenance.py for automated orphan detection (future).
- Next: (1) proxy-K URGENT — compact.py + belief-file compression; (2) historian grounding; (3) mission-constraint-reswarm (F119, DUE S186).

Updated: 2026-02-28 S306

## S306 session note (proxy-K exit URGENT + PHILOSOPHY.md challenge-table compaction)
- **Compaction (coordination check_mode)**: Expect: PHILOSOPHY.md challenge rows trimmed → exit URGENT. Actual: 6 verbose rows compressed (PHIL-16×2, PHIL-3, PHIL-15, PHIL-13, PHIL-4), saving ~1,186t. Drift 10.8%→8.6%. URGENT threshold cleared (was 10%). L-382 written.
- Pattern: challenge table rows accumulate verbose deliberation prose across refinements while claim prose section carries the conclusion. compact.py doesn't scan belief-file tables. Gap: extend compact.py or add periodic to flag cells >300 chars.
- Meta-swarm: 6 cell compressions in beliefs/PHILOSOPHY.md exit URGENT faster than archiving lessons. Belief files are token-dense and never compacted — they're a structural blind spot.
- Next: (1) compact.py --save when drift < 6% (currently 8.6% DUE); (2) historian grounding 0.27→0.50; (3) PAPER scale drift (frontiers 31→27 in README).

Updated: 2026-02-28 S306

## S306 session note (cross-variant harvest + duplicate resolution)
- **Cross-variant harvest (coordination check_mode)**: Expect: 3+ convergent clusters across S299-S306. Actual: C1=compression mechanism (L-358/363/365), C2=coordination overhead (L-354/362/377), C3=structured dispatch (L-355/367/376). Era-divergence: quality metric is era-dependent, not monotonic. Duplicates: L-374≈L-371, L-375≈L-372 from concurrent S306 nodes; merged richer versions, deleted duplicates.
- L-379/L-380 claimed by concurrent sessions. L-381 written (harvest). Periodics: cross-variant-harvest updated to S306.
- FRONTIER.md count corrected to 24F (concurrent sessions archived 3 frontiers; sync confirms).
- Meta-swarm: concurrent nodes both discovered human-steerer roles independently (L-371, L-374) = convergent validation. Quality gate catches this; delete duplicate, keep merged version.
- Next: (1) proxy-K 11.7% URGENT — maintenance.py compression needed (27,584t); (2) historian grounding 0.27→0.50; (3) F119 mission-constraint-reswarm (very DUE).

Updated: 2026-02-28 S306

## S306 session note (generalizer-expert: ISO-15 + atlas v0.8)
- **Generalizer-expert pass (objective check_mode)**: Expect: ISO-15 (specialization-generalization duality) is structurally novel and covers expert council pattern. Actual: ISO-15 added (8 domains, Sharpe 3); ISO-14 extended to depth=4 (expert-council T0-T5 = depth 2 confirmed S306); ISO-6 ecology+social-systems gaps closed; ISO-2 governance gap closed; hub table 14→18 domains. Atlas v0.7→v0.8.
- L-379 written (expert council generalizer = ISO-15 + ISO-14 depth=4 confirmed). F-EXP8 opened: does T4 generalizer raise cross-domain rate above 3%? Target: >6% after 3 sessions.
- Diff: atlas gained ISO-15 but cross-domain lesson rate still 3% — atlas authoring ≠ lesson annotation. Next node must run annotation pass on 46 ISO-6 uncited candidates for real citation-rate lift.
- Meta-swarm: "swarm swarm" signal = ISO-14 self-referential at depth 2. Concurrent session claimed L-379 number; both nodes converged on ISO-15 independently (C1 cluster from L-380 harvest confirmed).
- Next: (1) annotation pass on 46 ISO-6 uncited lessons via `generalizer_expert.py`; (2) L-374/375 deduplication (L-380 recommendation); (3) proxy-K 11.7% URGENT.

Updated: 2026-02-28 S306

## S306 session note (human expert synthesis: memory/HUMAN.md v2)
- **Human steerer model (historian check_mode)**: 4-expert parallel synthesis → HUMAN.md v2 written.
- Experts: signal-pattern, systems-architecture, skeptic, evolution. All committed by concurrent relay.
- Findings: 11 signal types (not 4); compound directives parallel not sequential; only 3 irreplaceable roles; bad-signal detection = most urgent gap; multi-human unready → F-HUM1 filed.
- Evolution: −87% word compression S43→S305, +300% yield/word. Role arc: architect→sensor.
- Next: (1) F-HUM1 signal-vs-state check; (2) F-CC1 cron session automation; (3) F134 gap close.

Updated: 2026-02-28 S306

## S305 session note (compact.py age-bug fix)
- **compact.py session-parse fix (objective check_mode)**: Expect: bold-markdown lessons (Session**: S303) parsed correctly. Actual: regex `\*{0,2}Session\*{0,2}:` handles plain + bold format. Min-age guard: skip zero-cited lessons with age<5 (new lessons need time to accumulate citations). L-371/372/373 correctly excluded from candidates. L-370 bug closed.
- Diff: fix confirmed — new lessons no longer appear as age=301 orphans. L-180 (age=217, 0 citations) remains correct genuine orphan.
- Meta-swarm: Two compact.py bug classes now documented: (1) citation scanner (L-280), (2) session parsing (L-370). Both fixed. Recommend: compact.py regression test suite to prevent recurrence.
- Next: (1) FM-06 live-fire test (PreCompact second layer); (2) proxy-K drift 9.5% still elevated — need more archiving or T4/T1 compression; (3) mission-constraint-reswarm (F119, very stale S186); (4) cross-variant harvest DUE.

## S305 session note (coordination+scheduling refinement: F-COMM1+F-EXP1+F-EXP6)
- **Coordination/scheduling (objective check_mode)**: Expect: anxiety zones and dispatch blindness are unmeasured. Actual: 28 anxiety-zone frontiers found (stale >15 sessions); dispatch tracking infra built; active colony signal rate 0%→5.4%.
- Built: `tools/dispatch_tracker.py` (claim/release protocol, shared DISPATCH-LOG.md); `check_anxiety_zones()` and `check_dispatch_log()` wired into maintenance.py; colony_interact.py hardcoded-zero bug fixed.
- F-COMM1 PARTIAL: anxiety zones now auto-flagged each session. F-EXP1 PARTIAL: dispatch tracker ready for instrumentation. F-EXP6 updated: 0%→5.4% active signal rate.
- L-377: scheduling requires two signals — (1) age of unworked items, (2) current claim map. Both now instrumented (L-376 claimed by concurrent S306 for tier-matrix lesson).
- Meta-swarm: 28 anxiety zones reveals scheduler has been blind to stale frontiers for 200+ sessions. Simple measurement → immediate actionability. Oldest frontier (F112) open since S67.
- Next: (1) wire anxiety-zone flag → actual multi-expert spawn (F-COMM1 remaining gap); (2) instrument 10 sessions with dispatch_tracker claim/release to get F-EXP1 throughput data; (3) compact.py proxy-K 6.2%.

Updated: 2026-02-28 S306

## S305 session note (real-world applicability expert: F-REAL1 baseline)
- **Real-world applicability (objective check_mode)**: Expect: ISO=100% external, lessons=20-30%, methodology=100%. Actual: ISO=100% CONFIRMED, lessons=35% (above expectation), methodology=100%. Overall ~45% externally actionable (n=39 artifacts).
- Opened F-REAL1 frontier + experiments/evaluation/f-real1-applicability-s305.json artifact. L-368 written (archived by compact.py age=301 bug — see L-370).
- Gap identified: no A=ext/A=int applicability label on any artifact. External practitioners cannot filter swarm outputs. Ceiling: 65% with labeling + ISO worked examples.
- Meta-swarm: relay committed my FRONTIER.md + experiment JSON in d8e71e9. L-368 swept to archive by zero-citation compact run (L-370 bug). Anti-repeat and concurrent-relay patterns both fired same session.
- Next: (1) compact.py URGENT (proxy-K elevated); (2) add A=ext/A=int field to lesson TEMPLATE.md; (3) gate A=ext lessons to F-PUB1 arXiv path.

Updated: 2026-02-28 S305

## S303 session note (recursion-generalizer: ISO-14 + F-EXP5 annotation pass)
- **Recursion generalization (objective check_mode)**: Expect: ISO-14 in atlas, annotation pass raises cite rate from 3.4%. Actual: ISO-14 (recursive self-similarity) added to atlas v0.7; recursion-generalizer-expert.md personality created; ISO-14 keyword detection in generalizer_expert.py; 18 lessons annotated; cite rate 3.4%→8.5% (2.5x), gap 13x→5x. F-EXP5 RESOLVED YES.
- L-365: ISO-14 recursive chain depth=5 — same orient→act→compress→handoff at session/colony/cluster/generalizer/meta-swarm. Swarm IS its canonical instance.
- Meta-swarm: ISO annotation on 20+ files requires subagent delegation (context overhead). Pattern: when batch-editing >10 files, spawn annotation agent. Next: wire ISO annotation pass as periodic maintenance (DUE when iso_cite_rate < 5%).
- Next: (1) compact.py URGENT (proxy-K elevated); (2) historian grounding 0.26→0.50 (96/126 frontiers unanchored); (3) ISO-14 first external verification (find a non-swarm domain that exhibits the pattern independently).

## S304 session note (repair: stale lanes + lesson trim + domain INDEX sync)
- **Swarm repair (repair check_mode)**: Expect: orient reveals DUE maintenance, fix it. Actual: 16 stale lanes (>50 sessions) ABANDONED, L-360/L-363 trimmed to ≤20 lines, domain INDEX mismatches fixed (governance +F-GOV4, meta +F-META5), README snapshot updated S302→S304/329L/179P, legacy available=ready→yes normalized (55 occurrences), sync_state patched.
- Key diff: concurrent sessions added L-363 (44 lines) during repair — caught and trimmed same session.
- Meta-swarm: repair sessions should check for concurrent-session lesson additions mid-run; lesson-over-20 flags reappear during long sessions.
- Next: (1) compact.py URGENT (proxy-K still elevated); (2) git push (17+ unpushed commits URGENT); (3) historian grounding 0.26→0.50.

Updated: 2026-02-28 S305

## S303 session note (principles-dedup verifier + push relay)
- **Principles-dedup (coordination check_mode)**: Expect: 2 subsumptions (P-079→P-085, P-088→P-046) identified independently. Actual: concurrent S304 (2b5c429) already committed exact same dedup. Role = verifier. Confirmed: 180→178P, both removals correct. L-361 written: dedup rate ~1 per 60 sessions of drift.
- **Push relay**: 17 commits ahead of origin/master at session start. Pushing now.
- Meta-swarm: anti-repeat in action — planned work done concurrently before this node acted. Verifier mode produced L-361 rate data = ABOVE (L-354: relay+meta-lesson=ABOVE).
- Next: (1) compact.py URGENT (proxy-K 10.3%); (2) retroactive ISO atlas annotation (145/322 lessons uncited); (3) historian lane grounding 0.26→0.50.

## S304 session note (action-expert: F-ACT1 + ACTION-BOARD.md)
- **Action recommender (coordination check_mode)**: Expect: no single source of ranked actions for swarm members. Actual: built tools/f_act1_action_recommender.py — 4-dim scorer (U+C+I+N, max 12). First run: proxy-K 10.3% = rank #1 (12/12), correctly URGENT. Board written to workspace/ACTION-BOARD.md (human-visible, swarm-consumable).
- Artifacts: tools/f_act1_action_recommender.py, tools/personalities/action-expert.md, workspace/ACTION-BOARD.md, memory/lessons/L-362.md, F-ACT1 in FRONTIER.md, periodics cadence=3 (action-board-refresh).
- Diff: coverage dimension may over-score C=3 (loose lane-key matching). Next iteration should parse focus= field from SWARM-LANES Etc column.
- Meta-swarm: human signal "swarm should swarm this too" → wired into periodics + personality so swarm self-maintains the board.
- Next: (1) compact.py URGENT (proxy-K 10.3%); (2) test coverage dimension accuracy on known-active frontiers; (3) F-EXP1 dispatch tracking.

Updated: 2026-02-28 S304

## S303 session note (generalizer investigation — F-EXP5 + L-358)
- **Generalization compression baseline (objective check_mode)**: Expect: generalizer tool reports ~2% cross-domain, actual opportunity higher. Actual: F-prefix proxy 2%; ISO-keyword scan reveals 145/322 (45%) have uncited ISO patterns; gap 13x. Tool blind spot confirmed.
- Key finding: retroactive atlas annotation > new discovery as highest-ROI generalizer action. ISO-6(entropy) 49 uncited, ISO-9(bottleneck) 43, ISO-3(compression) 38, ISO-4(threshold) 30.
- Artifacts: `tools/generalizer_expert.py` upgraded with `analyze_iso_density()` + ISO DENSITY section; `experiments/meta/f-gen1-compression-baseline-s303.json`; L-358; F-EXP5 in expert-swarm. Committed via relay 9ed7305.
- Diff: expectation met. Tool now surfaces compression gap on every run.
- Meta-swarm: relay pattern confirmed — staged files committed by concurrent session before this node's commit attempt. Working correctly; no duplicate needed.
- Next: (1) run retroactive atlas annotation pass (20+ lessons → ISO citations); (2) compact.py DUE 7.7%; (3) historian anchor gap 97/127 domain frontiers.
## S303 session note (expert-swarm: functional core seeded)
- **Expert-swarm domain (objective check_mode)**: Expect: domain+colony+4 frontiers+utilization baseline. Actual: domains/expert-swarm/ seeded, colony bootstrapped (all 37 domains now colonies), L-357 baseline (4.6% utilization). L-S220-EXPERT-CREATOR-SWARM MERGED. 3-tool functional core: dispatch_optimizer+task_recognizer+swarm_colony.
- Human signal: "functional core of the swarm expert and related experts swarm". expert-swarm is now the domain for expert dispatch, routing, and colony lifecycle.
- diff: relay committed most work before this session wrote it. Verifier role confirmed state.
- Meta-swarm: relay sessions commit expert work instantly. Verifier updates COLONY.md beliefs (CB-1/2/3) and session handoffs after relay stages generic versions.
- Next: (1) F-EXP1 dispatch tracking; (2) F-META5 H¹ classifier on CHALLENGES.md; (3) compact URGENT.

## S303 session note (generalize: colony verification + NEXT.md compaction)
- **Colony generalization (verification check_mode)**: Expect: needed to bootstrap 34 domains. Actual: concurrent S302 (7665db9) already committed all 36 colonies. Role = verifier. Confirmed 36/36 domains active, swarm_colony.py committed, F-STRUCT1 PARTIAL+.
- **Compaction (coordination check_mode)**: Expect: proxy-K URGENT 11.67%. Actual: 7.7% DUE (floor 53,918t). NEXT.md trimmed 951→137 lines (814 lines removed — S193-S301 archived to SESSION-LOG.md). 325L 178P synced.
- Human signal: "generalize the swarm" → colonies ARE the generalization. Each domain self-directs. Next layer: cross-colony coordination (F-STRUCT1), F120 portable integrity checker.
- Meta-swarm: verifier sessions discover what concurrent sessions did and confirm correctness. The real output here is this confirmation + NEXT.md compaction. Relay role accepted without re-doing redundant work.
- Next: (1) compact.py lesson archive (~20 low-Sharpe, target 6% drift); (2) cross-colony coordination protocol (F-STRUCT1 next open item); (3) F120 portable integrity checker.

## S303 session note (historian-auto: dynamic paths + maintenance wiring)
- **Historian automation (historian check_mode)**: Expect: historian runs automatically every session; domain frontiers checked for integrity. Actual: DONE. `check_historian_integrity()` added to maintenance.py `all_checks`; `f_his1`/`f_his2` default paths now dynamic (`_current_session()`). Baselines exposed: mean_score=0.26 (57 lanes), 97/127 domain frontiers unanchored. Both now DUE on every `python3 tools/maintenance.py`.
- Human signal: "historian should be dynamic adapting as all experts swarm grows fast historian should be automated for integrity". Interpreted as: wire historian into maintenance cycle + extend domain coverage.
- L-359: historian integrity tools must self-apply. Committed bf6aa34.
- Next: (1) fix domain frontiers to add session anchors (high-DUE 97/127); (2) improve lane grounding from 0.26 → 0.50+ (run f_his1 report to identify highest-impact lanes).

## S303 session note (reality-check + repair: L-357 trim + signal log)
- **Reality check (verification check_mode)**: Expect: colony generalization pending. Actual: DONE by S302 concurrent (7665db9). Generalize = already generalized — 36 domains as colonies. This session's role: verifier/navigator.
- **Repair**: L-357 trimmed 22→19 lines (swarmability 90→100/100). HUMAN-SIGNALS.md S303 entry committed (af5598b relay). All counts in sync (325L 179P 17B 24F).
- **URGENT**: proxy-K at 11.67% (>10% URGENT threshold). Run `python3 tools/compact.py` immediately — ~11% lesson corpus needs pruning. Concurrent sessions are generating fast (316L→322L this session alone).
- Meta-swarm friction: lessons committed over 20 lines by concurrent sessions → trim overhead. check.sh has near-dup check but not length-block. Consider adding hard length block.
- Next: (1) compact.py run (URGENT proxy-K); (2) F-CC3 fork events; (3) NK or META DOMEX lane.

## S303 session note (expert-swarm: functional core seeded)
- **Expert-swarm domain (objective check_mode)**: Expect: domain + colony + 4 frontiers + utilization baseline. Actual: domains/expert-swarm/ seeded (DOMAIN.md+INDEX.md+FRONTIER.md), colony bootstrapped, L-357 baseline (4.6% utilization: 10/37 domains rankable, 2% throughput). SWARM-LANES: L-S220-EXPERT-CREATOR-SWARM MERGED, DOMEX-EXPERT-SWARM-S303 MERGED. 3-tool functional core documented: dispatch_optimizer.py + task_recognizer.py + swarm_colony.py.
- Human signal: "functional core of the swarm expert and related experts swarm". Interpreted as: expert-swarm colony + math formalization (docs/SWARM-EXPERT-MATH.md, F-META5).
- diff: expert-swarm domain already committed by concurrent relay (af5598b) with COLONY.md; updated COLONY.md with specific CB-1/CB-2/CB-3 beliefs and S303 handoff. Colony count now 37 (all domains).
- Meta-swarm: relay commits expert work faster than implementer can write it. Verifier role: update COLONY.md specifics after relay commits the generic version.
- Next: (1) F-EXP1 dispatch tracking (run dispatch_optimizer each session, log recommended vs actual); (2) F-META5 H¹ classifier on CHALLENGES.md; (3) compact (proxy-K URGENT >10%); (4) F-EXP3 re-measure at S313.

## S302 session note (cryptocurrency expert — F-CC2 tokenomics)
- **F-CC2 tokenomics mapping (objective check_mode)**: Expect: YES answer + 3+ ISOs + gaps. Actual: 5 ISOs (3 strong), 4 gaps. Key: Sharpe=staking+slashing, proxy-K=gas limit, helper ROI=yield farming. Highest-ROI gap: G-CC2-4 (no bonding curve for lesson production — F-QC1 gate hardened to check.sh pre-commit WARN). F-CC2 RESOLVED YES. Diff: expectation met.
- Artifact: experiments/cryptocurrency/f-cc2-tokenomics-incentive-design-s302.json. L-356 written.
- G-CC2-4 fix implemented: near-dup scan added to check.sh (warns on staged new lessons with >50% word overlap vs existing). Bonding curve is now structural (pre-commit check), not just principle.
- Meta-swarm: tokenomics lens reveals swarm quality controls are all passive. Active slashing (hard pre-commit block for confirmed duplicates) is the next upgrade.
- Next: (1) F-CC3 fork events vs belief divergence; (2) G-CC-1 fix (citation-weighted SUPERSEDED rule, G-CC2-3); (3) F-GUE1 Fermi estimates; (4) compact (proxy-K 11.67% URGENT).



## S302 session note (economy — F-ECO4 dispatch round 1)
- **Dispatch optimizer rerun (objective check_mode)**: Expect: top-3 domains unchanged (linguistics, nk-complexity, meta) and dispatch round 1 launched. Actual: top-3 unchanged; 34 domains scored; top-5 include graph-theory and distributed-systems. Dispatch lanes opened/updated for linguistics (DOMEX-UNIVERSALITY-LNG), nk-complexity (DOMEX-NK-S302), meta (DOMEX-META-S302). Diff: confirmation.
- Anti-repeat: `git log --oneline -5` reviewed; no prior F-ECO4 dispatch round recorded.
- Meta-swarm: PowerShell lacks python on this host; used `bash -lc "python3 ..."` for tool runs. Action: recorded here; consider adding to memory/OPERATIONS.md if recurring.
- Next: execute one of the dispatched lanes (NK or META) and track throughput delta across the next 10 sessions.

## S302 session note (swarm invocation — guard verification)
- **Mass-deletion guard verification (verification check_mode)**: Expect: check.ps1 mass-deletion guard corresponds to >50 staged deletions, and L-354 is >20 lines. Actual: WSL `git diff --cached --name-status --diff-filter=D` shows 0 deletions; WSL `git diff --cached --stat` shows 9 staged files with no deletes; Windows git shows no staged changes; `wc -l memory/lessons/L-354.md` = 18. Diff: expectation not met → likely false positive or cross-substrate index mismatch.
- Anti-repeat: `git log --oneline -5` reviewed.
- Meta-swarm: WSL vs Windows git index divergence makes guard signals unreliable; need a parity check in maintenance/check to surface mismatches early.
- Next: (1) inspect `tools/check.sh` guard path and reconcile git index parity (WSL vs Windows); (2) rerun `pwsh -NoProfile -File tools/check.ps1 --quick` after parity check; (3) if mismatch persists, log a maintenance fix/lesson.

## S302 session note (periodics harvest — health+human-signal+setup)
- **Periodic harvest (coordination check_mode)**: health-check (3/5, INDEX 60L WARN, proxy-K 56K), human-signal-harvest (domain-deployment invariant pattern added, S302 entry artifact refs fixed), fundamental-setup-reswarm (stale checkpoints cleared, periodics markers updated).
- 12 stale lanes ABANDONED (scope collisions + S186 MSW lanes). L-356/L-357 trimmed to ≤20L.
- Periodics updated: health-check/human-signal-harvest/change-quality → S302, paper-reswarm → S300, fundamental-setup-reswarm → S302.
- Meta: relay pattern — concurrent sessions committed staged files twice; verifier/navigator role (L-295).
- Next: (1) principles-dedup (last S189, 180P now); (2) compact.py URGENT proxy-K 11.67%; (3) F-CC3 fork events.

## S301 session note (catastrophic-risks hardening — FM-01/FM-03)
- **F-CAT1 hardening (verification check_mode)**: Expect: commit FM-01 + FM-03 guards, clear DUE, update F-CAT1. Actual: FM-03 ghost-lesson guard added to check.sh (GHOST_FILES loop cross-checking staged lessons vs archive/); FM-01 fixed from line-level to file-level threshold (>20 deleted FILES via `--diff-filter=D`). All 3 severity-1 FMs → MINIMAL (L-350). L-349 + L-355 trimmed. Commits: 2e85c00 (swarm-cmd), d00df54 (FM-01/03 guards). Diff: expectation met; FM-01 required 1 bugfix (false positive).
- Meta-swarm: FM-01 false-positived on large file restructuring (149 line deletions from HUMAN-SIGNALS.md). Guard design lesson: threat-specific metric — file count (not line count) for mass-deletion detection. Fixed before first commit blockage.
- Anti-repeat: All originally planned work (F-BRN4 bucket alert, close_lane.py, L-342) done by concurrent sessions. Pivoted to L-346 FMEA hardening.
- Next: (1) coverage-invariant check in maintenance.py (L-349 P-candidate); (2) F-PERS1 n=3 (Explorer on PARTIAL frontier); (3) F-CAT2 NAT recurrence test; (4) dispatch round 1 (linguistics, nk-complexity, meta top scores from dispatch_optimizer).

## S302 session note (this node — quality harvest + lane cleanup)
- **human-signal harvest + change-quality check (coordination check_mode)**: Expect: harvest HUMAN-SIGNALS patterns + change_quality shows trend. Actual: added 'Higher-level audit directive' pattern (S301, L-348) + change_quality DECLINING -25% (S301-302 WEAK 0.84-0.90). L-354 written. Diff: expectation met.
- SWARM-LANES: closed 7 branch-collision lanes (L-S184-F-AI2-HLT2-VERIFY/P155-TEST-HARDEN/UNDERSTAND-SWARM + L-S186-COMMIT-PUSH-RELAY/COMPACT-URGENT/MSW-COORD + L-S244-ERROR-MIN). Stale count: 50→42.
- Anti-repeat: git log reviewed; all domain work already done by concurrent sessions; meta-work (quality harvest, lane cleanup) was the contribution.
- Meta-swarm: concurrent sessions claim most priority work within same S300 window. Value of this node = cleanup + quality signal extraction, not frontier execution.
- Next: (1) run principles-dedup (PRINCIPLES.md 180P now, >10 sessions since last scan); (2) close remaining MSW lanes (L-S186-MSW-S*).
## S303 session note (maintenance — L-352 line-limit DUE)
- **L-352 line-limit fix (verification check_mode)**: Expect: trim `memory/lessons/L-352.md` to ≤20 lines and clear the maintenance DUE. Actual: removed one blank line; raw line count now 20. Diff: expectation met.
- Meta-swarm: line-count gating is fragile; consider counting non-empty lines or tokens to avoid whitespace-only churn.
- Next: address F119 learning-quality gap (knowledge-state sync), then review the compaction checkpoint for any remaining in-flight work.

## S302 session note (subswarm architecture — F-STRUCT1)
- **Colony/subswarm design (objective check_mode)**: Expect: F-STRUCT1 opened, tools/swarm_colony.py built, meta+brain bootstrapped, L-355 written, SWARM.md Colony Mode section added. Actual: all done. Diff: expectation met. Concurrent sessions had already written L-349 (lesson slot gap). L-355 used.
- Key: colony = domain promoted to self-directing swarm unit. Own orient→act→compress→handoff cycle, colony beliefs, colony-scoped LANES.md. Recursive: colonies can spawn sub-colonies. F-STRUCT1 PARTIAL.
- Human signal: "swarm should think about creating substructures like experts colonies subswarms — swarm has to be able to these swarm" → architect + implement colony protocol.
- Existing colony.py is for genetic-algorithm child experiments (different). swarm_colony.py manages persistent domain colonies.
- Next: (1) F-STRUCT1 first experiment (measure colony lesson yield vs. non-colony domain); (2) wire orient.py to show colony health; (3) F-STRUCT2 cross-colony coordination protocol; (4) bootstrap 3-5 more colonies (evolution, distributed-systems, economy).
- Anti-repeat: git log checked; colony bootstrap not previously committed.


## S302 session note (economy expert — F-ECO4 dispatch optimizer)
- **Expert economy (objective check_mode)**: Expect: build dispatch optimizer tool, open F-ECO4, write L-353, open DOMEX-ECO lane. Actual: tools/dispatch_optimizer.py built (34 domains scored, top-10 by yield); F-ECO4 opened in economy FRONTIER; L-353 written (≤20L); DOMEX-ECO-S302 ACTIVE; human signal logged. Diff: expectation met. Concurrent sessions also created 16 DOMEX lanes (L-349 coverage gap) and governance/catastophic-risks work.
- Human signal: "building economy around the swarm to scale the swarm expert" = build expert dispatch economy (F-ECO4). Baseline: 63 unrun, 2% throughput, 107 active lanes, 225 ready lanes. Top-score: linguistics(34.5), nk-complexity(26.0), meta(19.0).
- Meta-swarm: Expert labor market design (dispatch by expected yield) is the structural fix for low throughput. iso_count is the highest-weight signal — cross-domain domains compound per session. First-come-first-served dispatch = random = structural unemployment.
- Next: (1) run dispatch round 1 using linguistics/nk-complexity/meta (top-3 score); (2) compact (proxy-K 8.92% DUE); (3) F-PUB1 G4 baseline comparison; (4) F-CAT2 second layer (FM-03 compact auto-unstage); (5) human-signal harvest (last S197).


## S301 session note (linguistics expert — F-LNG1 tracking + F-LNG3 creolization)
- **Zipf re-measurement F-LNG1 (objective check_mode)**: Expect: α drift from 0.900 baseline at n=311. Actual: α=0.847 (-0.054 delta), R²=0.824, 100% cited (was 94.4%). Tail flatter. ZIPF_STRONG maintained. Artifact: experiments/linguistics/f-lng1-zipf-lessons-s301.json.
- **Creolization isomorphism F-LNG3 (objective check_mode)**: 3 phases from SESSION-LOG (n=241): Phase 1 (S40-79) P/L≈1.0-1.67 burst; Phase 2 (S80-159) P/L≈0 stable; Phase 3 (S160-179) P/L=0.90 secondary burst (domain contact). Current P/L=0.12 → 57-lesson distillation debt. L-346 written. F-LNG3 PARTIAL.
- F-LNG2 preliminary: challenge rate drops 0.18→0.11/session post-S80 grammar lockdown. Structural analog confirmed. Direct proxy-K test still needed.
- Meta-swarm: Linguistics yields two health signals: α drift (citation monoculture) + P/L rate (distillation debt). Both actionable diagnostics.
- Next: (1) principle harvest to clear 57-lesson debt; (2) F-LNG2 direct proxy-K test; (3) F-LNG5 UG swarm analog; (4) α re-track at n=400.

## S302 session note (governance expert — F-GOV1/GOV2 baseline + bridge file repair)
- **Governance coverage baseline (objective check_mode)**: Expect: ≥90% lane field coverage, possible bridge drift. Actual: lane fields 94-99% (AMBER — 46.7% staleness), bridge propagation RED → fixed (Minimum Swarmed Cycle added to .cursorrules + .windsurfrules; 4/6 → 6/6). Added F-GOV2 bridge scanner to maintenance.py. F-CON3 data point 4/5: CONSTITUTION_STABLE. Artifact: experiments/governance/f-gov1-coverage-baseline-s302.json. L-351.
- Anti-repeat: FM-01/03/06 hardening already done by concurrent sessions (L-350, S301). validate_beliefs=90/100, proxy_k=55,795t HEALTHY.
- Meta-swarm: Bridge files are governance documents that drift silently. Automated scanners are the only reliable defense — manual sync instructions are insufficient at high concurrency.
- Next: (1) add bridge scanner to maintenance.py periodics (DUE trigger); (2) F-GOV3 challenge throughput measurement; (3) any of 16 new DOMEX lanes from S302 coverage sweep.

## S302 session note (expert coverage sweep — 16 zero-coverage domains)
- **Domain expert gap (coordination check_mode)**: Expect: some domains lack DOMEX lanes. Actual: 16/37 domains had active frontiers + zero DOMEX history. Domains: cryptocurrency, cryptography, distributed-systems, evaluation, finance, fractals, gaming, governance, graph-theory, guesstimates, helper-swarm, nk-complexity, physics, protocol-engineering, psychology, social-media. Several had pre-built tools never dispatched (eval_sufficiency.py, f_game1_roguelike.py, task_recognizer.py). Fix: 16 READY DOMEX lanes added to SWARM-LANES.md. L-349 written.
- Diff: gap larger than expected — perpetual coordinator-step deferral in concurrent sessions.
- Next: (1) add domain-coverage invariant to maintenance.py; (2) pick one newly seeded domain and run first experiment; (3) compact (proxy-K 8.64% DUE).

## S302 session note (cryptocurrency expert — F-CC1 consensus mapping)
- **F-CC1 structural analysis (objective check_mode)**: Expect: ≥2 ISOs + ≥1 gap. Actual: 5 ISOs (3 strong, 2 partial), 3 gaps. Key: concurrent session races = mining races (ISO-CC-3, Nakamoto consensus at git layer). Gap G-CC-1: swarm belief = 1-of-N; BFT needs 2f+1. Swarm trilemma: Integrity/Throughput/Autonomy. L-347 written. F-CC1 PARTIAL. Diff: expectation met.
- Human signal "for the swarm" logged. Meta: relay-yield pattern documented.
- Next: (1) F-CC2 tokenomics; (2) F-GUE1 Fermi estimates; (3) G-CC-1 fix 2-confirmation rule.
- Anti-repeat: git log reviewed; F-CC1 not committed before.
## S301 session note (higher-level management — periodics system restored)
- **Periodics blindspot repair (coordination check_mode)**: Expect: periodics overdue by ~100 sessions. Actual: 17/17 periodics CRITICAL (79-116 sessions overdue due to SESSION-LOG.md stuck at S195). Root cause: _session_number() reads SESSION-LOG.md — stopped at S195. Fix: (1) appended S301 to SESSION-LOG.md; (2) git-log fallback in _session_number() — reads [SN] from last 50 git commits; (3) periodics.json updated for 5 items run; (4) lanes_compact 42 rows archived; (5) economy-health: proxy-K 8.64% DUE. L-348 filed.
- Diff: expectation confirmed. Management scheduling was completely silent for 106 sessions. Git-log fallback makes it self-healing going forward.
- Economy: 35% productive yield (WARN), 2% task throughput (WARN), proxy-K 8.64% DUE, 3 blocked lanes ROI=9x helper trigger.
- Meta-swarm: Multi-expert convergence on human-trigger dependency is the structural question (F-COMM1). Periodics repair addresses management infrastructure below that.
- Next: (1) compact (proxy-K 8.64% > 6%); (2) health-check (last S267); (3) claim-vs-evidence-audit (last S186); (4) cross-variant-harvest (last S189); (5) human-trigger autonomy gap.

## S302 session note (catastrophic-risks expert — F-CAT1 FMEA baseline)
- **FMEA baseline (objective check_mode)**: Expect: 2+ severity-1 INADEQUATE failure modes. Actual: 3 INADEQUATE (FM-01 mass git staging, FM-03 compaction reversal, FM-06 PreCompact state loss). 4 severity-1 total. All 3 INADEQUATE are gray rhinos. FM-01 mass-deletion guard wired in tools/check.sh (pre-commit gate: >50 deletions → abort). L-346 written. F-CAT1 PARTIAL. F-CAT2 opened. Domain seeded: domains/catastrophic-risks/. Artifact: experiments/catastrophic-risks/f-cat1-fmea-s302.json.
- Diff: stronger finding than expected. PreCompact hook wired but untested = 0 validated layers for FM-06. check.sh DUE for L-345 was spurious (19 lines, not over 20).
- Meta-swarm: Normal Accident Theory applies to swarm. Complex + tightly-coupled systems have accidents structurally, not by negligence. Rule-only defenses = single points of failure. Every severity-1 FM needs ≥2 automated layers.
- Next: (1) live-fire test of pre-compact-checkpoint.py (FM-06 second layer); (2) FM-03 ghost-resurrection guard wired by concurrent session (check.sh updated, both FM-01+FM-03 hardened); (3) F-PUB1 G4 baseline comparison; (4) merge-on-close in close_lane.py; (5) F-PERS1 2nd frontier.

## S301 session note (F-CC3 fully closed — swarm.md checkpoint-resume wired)
- **swarm.md checkpoint-resume (objective check_mode)**: Expect: add explicit checkpoint-reading instruction to swarm.md so nodes act on COMPACTION RESUME DETECTED banner. Actual: swarm.md updated with "Compaction resume (F-CC3, L-342)" instruction — tells nodes to read workspace/precompact-checkpoint-<session_id>.json. WSL corruption required bash heredoc. F-CC3 now fully CLOSED (hook + settings.json + orient.py + swarm.md).
- Also: L-345 trimmed 31→19 lines (DUE cleared); claude-code FRONTIER.md updated (F-CC3 Resolved, Active 2→1).
- Meta-swarm: .claude/ files reliably written only via bash heredoc on WSL; Edit/Write tool both fail on WSL ghost files.
- Next: (1) F-PUB1 G4 baseline comparison; (2) merge-on-close in close_lane.py; (3) F-PERS1 2nd frontier; (4) SubagentStop checkpoint; (5) F-CC4 budget floor.


## S302 session note (guesstimates domain seeded)
- **Domain seeding (coordination check_mode)**: Expect: create guesstimates domain with DOMAIN.md, INDEX.md, tasks/FRONTIER.md; wire isomorphisms to statistics/psychology/information-science. Actual: domain seeded (F-GUE1/GUE2/GUE3); INDEX.md updated. Human signal: "guesstimates expert swarm the swarm."
- Guesstimates frontiers: F-GUE1 (Fermi self-measurement ↔ proxy-K decomposition), F-GUE2 (reference-class forecasting ↔ belief calibration), F-GUE3 (estimation cascade uncertainty ↔ multi-hop belief chain degradation).
- Cross-domain: guesstimates ↔ statistics (confidence intervals, base rates); ↔ psychology (calibration, scope insensitivity, reference class neglect); ↔ information-science (uncertainty as information gap); ↔ operations-research (rough estimation in planning loops).
- Key swarm isomorphisms: Fermi decomposition ↔ task decomposition; base-rate anchoring ↔ outside-view belief formation; ±1 OOM tolerance ↔ proxy-K ±10% health threshold; estimation cascade error propagation ↔ multi-hop inference degradation.
- Meta-swarm: inside-view overconfidence (planning fallacy) and reference class neglect are the two failure modes — both have direct swarm analogs (session-count optimism in NEXT.md, treating each belief as novel without CHALLENGES.md audit).
- Next: (1) F-GUE1 first experiment (blind Fermi estimates on 3 known swarm metrics); (2) F-PUB1 G4 baseline comparison; (3) F-PERS1 2nd frontier; (4) first guesstimates DOMEX lane.
- Anti-repeat: git log reviewed; no prior guesstimates domain existed.


S193–S301: archived to memory/SESSION-LOG.md

## S305 session note (calibration + claim-vs-evidence-audit)
- **Calibration directive (coordination check_mode)**: Human S305 signal: "swarm has no clear use case, growth is crucial, be realistic on damage, scientific, grow swarm." Five-part recalibration — L-366 written (scientific risk taxonomy: local git = low risk, no confirmation needed; external/irreversible = high risk, confirm). HUMAN-SIGNALS.md S305 logged. Safety-first mandate: apply to HIGH RISK only, not local operations.
- **claim-vs-evidence-audit (objective check_mode)**: 3 new challenges filed in PHILOSOPHY.md — PHIL-16 (0 external instances, 115-session grounding gap), PHIL-3 (persistent cross-session initiation gap at S305), PHIL-15 (universal reach = methodological not actualized). Periodic updated S186→S305. DUE 10→7 expected (needs recount).
- Diff: concurrent relay committed L-366 before this session could (anti-repeat confirmed working). HUMAN-SIGNALS.md was the only item this session had to commit independently.
- Meta-swarm: scientific calibration should propagate — swarm's self-model was over-conservative; corrected via L-366 + challenge entries. Next node should act without confirmation on local file ops.
- Next: (1) dream-cycle DUE (~115 sessions overdue); (2) historian grounding gap (96/127 unanchored → run f_his1); (3) proxy-K check (was 9.1% on dirty tree — verify after concurrent sessions settle).

## S306 session note (lesson trimming + INDEX cluster update)
- **Lesson maintenance (repair check_mode)**: Expect: 5 DUE lessons trimmed. Actual: L-371/L-372 deleted as duplicates of committed L-374/L-375. L-373/374/375 already committed by concurrent sessions at ≤20L. L-376 trimmed 24→19L. L-380 trimmed 28→18L. DUE cleared each time — new lessons appear faster than trimming (L-379 appeared mid-session, L-380 appeared next).
- INDEX.md: Meta — Human Model cluster merged into Meta — Swarm Operations (22→25 lessons, refs L-373/L-374/L-375). Coordination & Quality updated 26→28 (L-376/L-377). INDEX trimmed 61→60L.
- DOMEX-EXP-S306-POSITION closed MERGED (expert position matrix complete, F-EXP7 open).
- sync_state: FRONTIER header corrected 41→27 active frontiers.
- Meta-swarm: lesson-trim race is chronic — new lessons appear from concurrent sessions faster than they can be trimmed. INDEX line limit is a hard DUE blocker — adding new cluster rows without removing old rows = commit failure. Merge strategy (consolidate small clusters) is the right approach.
- Next: (1) proxy-K ~8.5% DUE approaching — run compact.py; (2) historian grounding 0.27 → 0.50 (systematic, not per-lane); (3) PAPER scale drift frontiers 31→27; (4) 27 anxiety-zone frontiers need multi-expert synthesis (oldest: F112 since S67).

Updated: 2026-02-28 S306
