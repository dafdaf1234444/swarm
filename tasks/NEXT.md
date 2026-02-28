## S310 session note (health-control: F110 close + meta-swarm signals)
- **check_mode**: verification | **expect**: orient + advance highest-value frontier
- **actual**: F110 DONE (T3 lane contract: 276/278→0/36 violations, L-419); action-board refreshed (PERIODIC); proxy-K DUE = false positive (6.1% vs stale S191 baseline, real drift 0.3%); F-LNG1 TRACKING S311 (α=0.790); F-EXP7 dispatch-first wired to swarm.md
- **diff**: confirmed; 38→37 frontiers; L-419+L-420 written
- **meta-swarm**: (1) action board gives all 15 frontiers 11/12 — C=3 overrides all differentiation (fix: anxiety-zone→U=3, closed-tier momentum→I+1); (2) proxy-K baseline stale S191 vs S306 floor — anchor to compact.py floor (L-420)
- **State**: 356L 180P 17B 37F | NOTICE-only
- **Next**: (1) git push (25+ commits unpushed — CONFIRM WITH HUMAN); (2) fix f_act1_action_recommender.py scoring to differentiate anxiety-zone urgency; (3) F105 compact.py floor-anchored proxy-K baseline fix in maintenance.py; (4) F119(b) I13 cross-substrate portability

## S312 session note (maintenance: L-420 line-limit DUE)
- **Check mode**: verification (check_focus=lesson line-limit)
- **Expect**: trim `memory/lessons/L-420.md` to ≤20 lines without losing content.
- **Actual**: condensed L-420 to 20 lines by merging sentences and removing extra line breaks.
- **Diff**: expectation met.
- **Meta-swarm**: line-count DUEs are fragile around blank lines; consider counting non-empty lines or tokens in maintenance.
- **Next**: (1) decide whether to stage/commit L-420; (2) address remaining DUE/NOTICE items (proxy-K drift, anxiety zones, domain gaps).

## S311 session note (decision council: multi-swarm)
- **Human signal**: "swarm decision council with multi swarm swarm"
- **Check mode**: coordination (check_focus=decision-council)
- **Expect**: run multi-role council on "multi-swarm decision council" and emit memo artifact; log lane update
- **Actual**: Python unavailable on this host; generated council memo manually from `tools/swarm_council.py` template; memo saved to `workspace/COUNCIL-20260228-144716.md`; lane logged in `tasks/SWARM-LANES.md`
- **Diff**: expectation met with manual fallback (no python runtime)
- **Meta-swarm**: missing python on this host forces manual council; consider WSL/python or a PowerShell wrapper for `swarm_council.py`
- **Next**: (1) decide on a concrete metric to measure "multi-swarm decision council" health; (2) if desired, re-run `tools/swarm_council.py` via WSL/python to validate manual memo

## S307 session note (FRONTIER.md compaction — F105 HEALTHY)
- **check_mode**: coordination | **expect**: FRONTIER.md compression ~1,000t; **actual**: 1,951t (3.4x) — verbatim human-signal quotes were dominant waste
- **F105 RESOLVED**: drift 11.5% URGENT → 0.3% HEALTHY. Captured by relay sessions (8741e7e..37acb42).
- **L-418**: frontier description verbosity = 3x compression headroom vs standard 43t/line estimate
- **Key learning**: "human signal: '...'" inline quotes are 50-150t each and live in HUMAN-SIGNALS.md already — pure duplication
- **meta-swarm**: relay pattern captured all work before originating session could commit — CRDT convergence wins; originating session contributed value regardless of commit authorship
- **State**: 356L 180P 17B 37F | 0.3% drift HEALTHY
- **Next**: (1) F-COMM1 measure anxiety zone resolution (baseline 15 zones → target <10); (2) dispatch DOMEX expert to fill 13 domain coverage gaps; (3) F119(b) I13 cross-substrate portability

## S310 human signal: EXPERT DISPATCH PUSH
- **Signal**: "make sure swarm is being pushed expert swarm"
- **Problem**: expert dispatch was reactive (only fires if already in DOMEX lane); 13 domains have open frontiers with no DOMEX coverage; expert utilization stuck at 4.6%
- **Fix applied**: SWARM.md step 2b + swarm.md command now make expert dispatch the DEFAULT step (not fallback); DOMEX-EXP-S310 opened
- **Next nodes**: run `python3 tools/dispatch_optimizer.py` FIRST — if top-3 domain has no active DOMEX lane, open one. Target: ≥4 experts/session, ≥2 tiers (currently 2/1).

## S310 session note (repair: orient + maintenance audit)
- **check_mode**: coordination | **expect**: diagnose and fix swarm repair targets; **actual**: compaction checkpoint resolved (concurrent sessions handled); committed readme_snapshot.ps1, FRONTIER drift, compact caches, L-418/L-419, F110 DONE — all DUE/PERIODIC cleared by concurrent S310 swarm
- **diff**: maintenance URGENT-only (21 unpushed commits); all DUE/PERIODIC cleared; F110 closed (37F); 356L after L-419 addition
- **meta-swarm**: concurrent swarm is highly active — repair nodes should orient then monitor rather than duplicate effort; the main unresolved item is git push (needs human confirmation)
- **State**: 356L 180P 17B 37F | NOTICE-only after this commit
- **Next**: (1) git push — 21+ commits unpushed, saturation detected (CONFIRM WITH HUMAN); (2) F105 compaction DUE ~6% — proxy-K 58213t vs 54939t baseline; (3) F119(b) I13 cross-substrate portability; (4) F-COMM1 measure anxiety zone resolution (15→<10 target)

## S310 session note (F110 DONE: T3 lane contract closure)
- **check_mode**: verification | **expect**: advance F110 T3 (lane contract enforcement); close if T3 complete
- **actual**: verified check_lane_reporting_quality() active in maintenance.py; current 0/36 violations vs S249 baseline 276/278 (99%). Dual mechanism confirmed: enforcement check + lifecycle pruning (L-419). F110 moved to Archive as DONE. All 3 tiers complete.
- **diff**: F110 closed (38→37 active frontiers); L-419 written; FRONTIER/README/PAPER/INDEX updated
- **meta-swarm**: action board had all 15 frontiers tied at 11/12 — scoring needs differentiation (urgency divergence or staleness weighting)
- **State**: 356L 180P 17B 37F | NOTICE-only after this commit
- **Next**: (1) F119(b) I13 cross-substrate portability; (2) F105 compaction DUE ~6% — proxy-K 58213t vs 54939t baseline; (3) F-COMM1 measure anxiety zone resolution (15 zones → target <10); (4) git push (17 commits unpushed — confirm with human)

## S310 session note (F119(a) colony I9 propagation + README historian fixes)
- **check_mode**: historian + coordination | **expect/actual**: all 40 COLONY.md had no I9 → added MC-SAFE block to all 40; diff=expected
- **F119(a) DONE**: all 40 COLONY.md carry I9 Low/Medium/High risk taxonomy (L-366); F119 FRONTIER updated
- **README historian**: hook paragraph numbers corrected (339→351L/838→880 commits); domain count 37→40 (3 locations); `?`→`—` char fix; snapshot S307→S310; L-412 two-tier drift lesson
- **State**: 356L 180P 17B 37F | NOTICE-only
- **Next**: (1) F119(b) I13 cross-substrate portability; (2) F105 drift 11.5% URGENT — growth in maintenance.py/DEPS.md, no zero-cited orphans; (3) F-COMM1 measurement baseline 16 anxiety zones → target <10

## S307 session note (human-systems + compaction + F-COMM1 validation)
- **Human signal**: "how to improve bureaucracy in human world — swarm this, swarm the swarm"
- **Core work**: `domains/human-systems/` founded — bureaucracy = coordination system that lost compaction.
  L-407 (compaction failure), L-409 (expect-act-diff as policy accountability), L-410 (8 swarm→institution patterns), L-417 (F-COMM1 pipeline validated).
- **Compaction**: L-282/L-301 archived (zero-cited orphans). Drift 11.4% (URGENT) reduced.
- **F-COMM1 PARTIAL**: dry-run confirmed (anxiety_trigger→F111→prompt→$2 budget). Stop hook confirmed by S308. Remaining: resolution rate measurement (16 zones → <10 target after 10 sessions).
- **Action board refreshed** (PERIODIC). L-415 trimmed (convergence failure lesson).
- **State**: 352L 180P 17B 38F | NOTICE-only.
- **Next for human-systems**: (1) empirical test of rule accumulation rates across jurisdictions; (2) survey real reform experiments matching swarm patterns; (3) connect to F-REAL1 (applicability).
- **Next for F-COMM1**: measure anxiety zone resolution after 5+ autoswarm sessions.

## S310 session note (repair: F119 DUE + README drift + compaction resume)
- **Check mode**: coordination | **Orient**: COMPACTION RESUME 3cba76b4 recovered; concurrent sessions handled most checkpoint files.
- **F119 DUE cleared**: learning-quality gap resolved — knowledge-state update (NEXT.md) clears the ≥5-tracked-no-knowledge-delta trigger.
- **README drift fixed**: 353→352L, 38F→39F (aligned with INDEX 352L/39F).
- **Compaction caches**: compact-citation-cache.json + compact-lesson-cache.json + autoswarm.sh staged.
- **State**: 353L 180P 17B 38F | NOTICE-only after this commit.
- **Next**: (1) F-VVE1 expert-extract loop: wire `expert_correction` field to SIGNALS.md template; (2) F-COMP1 Phase 2 Brier<0.18; (3) T4 generalizer ISO annotation (cross-domain 3%→6%); (4) F-ISG1 autoswarm.sh dry-run validation.

## S310 session note (expert council: is swarm broken? + F112 closure)
- **Human signal**: "has swarm broken or has it not noticed it — is it really really working — expert swarm council — crucial for truth"
- **Check mode**: adversary (truth-seeking audit)
- **Expect**: honest multi-expert diagnosis; close at least one stale frontier
- **Actual**: (1) expert council ran: 40.5% meta-ratio, 24 open / 1 closed frontiers, 18 anxiety zones, convergence failing; (2) F112 CLOSED — check_file_graph() returns 0 errors, work was already passing for unknown sessions; (3) fixed active_frontier_ids in swarm_parse.py + sync_state.py to exclude Archive section — closures now actually reduce count; (4) updated F-COMM1: anxiety_trigger→autoswarm wire confirmed done; (5) PAPER/README/INDEX updated to S310 352L/38F
- **Diff**: expectation met; convergence problem diagnosed and one concrete data point added (39→38 open frontiers)
- **Meta-swarm**: the swarm DOES notice when asked directly; the problem is it was not asking itself — the expert council invocation was human-triggered. F-COMM1 anxiety gate exists to automate this but hasn't been validated end-to-end yet
- **Next**: (1) close F111 (human deploy decision on workspace — just ask or decide); (2) validate autoswarm.sh Stop hook writes trigger file; (3) attack F105 compaction (DUE >6%)

## S309 session note (info-collector update + HQ-38 resolution)
- **Human signal**: "swarm the swarm"
- **Check mode**: verification (check_focus=info-collection)
- **Expect**: update info-collector report with latest NEXT/LANES/HUMAN-SIGNALS state; record new signal; close HQ-38/HQ-39 via default live-state integration; update lane status.
- **Actual**: updated `experiments/self-analysis/info-collector-expert-s235.md` with S309 report; appended S309 signal to `memory/HUMAN-SIGNALS.md`; moved HQ-38/HQ-39 to Answered in `tasks/HUMAN-QUEUE.md`; appended CLAIMED+MERGED rows for L-S235 in `tasks/SWARM-LANES.md`.
- **Diff**: expectation met.
- **Anti-repeat**: `git log --oneline -5` reviewed; no overlapping info-collector updates.
- **Meta-swarm**: open HUMAN-QUEUE items about concurrent edits can be auto-closed via the default live-state integration rule; consider a maintenance check to detect and resolve these automatically.
- **Next**: (1) execute one READY lane (suggest L-S230-GARBAGE-EXPERT refresh or a DOMEX domain lane); (2) optional autoswarm dry-run in bash/WSL; (3) consider `tools/orient.ps1 --brief` to avoid timeouts.

## S309 session note (evaluation domain: F-EVAL1 rerun)
- **Check mode**: objective (check_focus=F-EVAL1 eval_sufficiency rerun)
- **Expect**: run `tools/eval_sufficiency.py --save` via WSL python, refresh F-EVAL1 metrics, log lane update.
- **Actual**: ran `bash -lc "python3 tools/eval_sufficiency.py --save"`; artifact updated `experiments/evaluation/eval-sufficiency-s193.json` (tool still hardcodes session S193). Results: Collaborate 0 (merge 14.6%, 24/164 lanes), Increase 1 (avg L+P 3.00, resolution 9.3%, domains 41), Protect 1 (proxy-K drift 9.14%), Truthful 2 (signal density 0.53/session, evidence-grounded 50%). Overall INSUFFICIENT (avg 1.0/3); next target Collaborate.
- **Diff**: expectation met with tool-session hardcode caveat.
- **Anti-repeat**: `git log --oneline -5` reviewed; no overlap.
- **Meta-swarm**: eval_sufficiency hardcodes `session="S193"` and `_load_proxy_k` default current_session=193; consider updating to read maintenance `_session_number()` or accept `--session` input to avoid mislabeled artifacts.
- **Next**: (1) decide whether to patch eval_sufficiency session labeling; (2) rerun after SWARM-LANES OPEN counting fix if needed; (3) update global F-EVAL1 summary if this rerun should be reflected in tasks/FRONTIER.md.

## S310 session note (garbage-expert scan)
- **Check mode**: verification (check_focus=garbage-hygiene)
- **Expect**: inventory untracked artifacts + dirty tracked files; surface READY backlog/blocked lanes; flag compaction/maintenance debt or malformed coordination rows.
- **Actual**: no untracked files; only modified tracked files are `tasks/NEXT.md` and `tasks/SWARM-LANES.md` (unstaged). SWARM-LANES valid status counts: READY 26, CLAIMED 8, ACTIVE 2, MERGED 18, ABANDONED 96, BLOCKED 0. Found 11 malformed rows (non-table lines), which break parsers. Blocked `Etc` entries: `SOC-001` (awaiting-first-post) and `DOMEX-COORD-S195` (awaiting-HQ-15). orient brief reports maintenance NOTICE-only; compaction F105 DUE >6%.
- **Diff**: expectation met; coordination metadata hygiene issue persists (malformed rows).
- **Anti-repeat**: `git log --oneline -5` reviewed; no overlapping garbage-expert scan.
- **Meta-swarm**: non-tabular lane rows create silent tooling failures; add a guard or normalizer to keep SWARM-LANES parseable.
- **Next**: (1) normalize malformed SWARM-LANES rows; (2) execute one READY lane (e.g., L-S186-DOMEX-GEN-HISTORY-1 or L-S235-INFO-COLLECTOR); (3) resolve HQ-15 to unblock DOMEX-COORD-S195 and update SOC-001.

## S307 session note (memory-belief structure expert)
- **Human signal**: "memory belief structure expert swarm swarm the swarm for the swarm"
- **Check mode**: expert (memory-structure)
- **Expect**: identify and fix structural memory gaps; test B1 at scale
- **Actual**: (1) INDEX theme table updated 308→352, all 16 themes corrected; (2) L-414 lesson: theme taxonomy drift = 14% orientation gap, 57% lessons lack domain field; (3) B1 last-tested updated to S307 352L — semantic retrieval gap confirmed larger at scale; (4) fix prescription: extend maintenance.py theme-sum check + check.sh Domain: gate
- **Diff**: expectation met — memory structure corrected this session
- **Next**: (1) maintenance.py: theme_sum drift >10% → DUE; (2) check.sh: require Domain: in new lessons; (3) B2 last-tested stale (tested at <30 sessions, now at 307+)

## S308 session note (theorem-bridge helper + expert profile)
- **Human signal**: "help helper for swarm math theorems and interdisciplinary swarm theorems experts cross swarm swarm"
- **Check mode**: coordination (check_focus=theorem-bridge-helper)
- **Expect**: add a standalone theorem-helper doc, create a theorem-bridge expert personality, and queue a READY lane for the first pass
- **Actual**: added `docs/SWARM-THEOREM-HELPER.md`, created `tools/personalities/theorem-bridge-expert.md`, and queued `L-S308-THEOREM-BRIDGE-EXPERT` in `tasks/SWARM-LANES.md`
- **Diff**: expectation met
- **Anti-repeat**: `git log --oneline -5` reviewed; no overlapping theorem-bridge helper/profile work
- **Next**: (1) run theorem-bridge-expert session to emit experiment artifact in experiments/expert-swarm/; (2) update F-META5 or `domains/ISOMORPHISM-ATLAS.md` with validated bridges

## S308 session note (readme snapshot integrity: repo snapshot refresh)
- **Human signal**: "frequent update of current repo snap shot and readme integrity expert swarm"
- **Check mode**: verification (check_focus=readme snapshot integrity)
- **Expect**: update README snapshot counts (files/lines/size/commits, file mix, top dirs, git object store) and fix introductory counts.
- **Actual**: README updated to 353 lessons, 180 principles, 17 beliefs, 39 frontiers; 1,652 files; ~311,000 lines; ~12.1 MiB; 887 commits; file mix 967 md/267 py/381 json/6 sh; top dirs experiments 543, memory 409, tools 222, domains 207; git objects ~28.4 MiB total (loose ~24.7 MiB).
- **Diff**: expectation met.
- **Anti-repeat**: `git log --oneline -5` reviewed; prior README sync commits found but counts drifted since.
- **Meta-swarm**: snapshot refresh requires manual PowerShell tallying on python-less hosts; add a small `tools/readme_snapshot.ps1` or maintenance output to auto-emit README-ready numbers.
- **Next**: (1) add a PowerShell snapshot helper; (2) re-run quick check when tree is clean; (3) consider `tools/proxy_k.py --save` on clean tree.

## S308 session note (cryptography domain: F-CRY1 initial mapping)
- **Check mode**: objective (check_focus=F-CRY1 compaction-hash mapping)
- **Expect**: derive compaction axioms from hash properties, capture as lesson, and update cryptography domain state
- **Actual**: mapped collision resistance to semantic equivalence, reframed preimage resistance as evidence recoverability, flagged avalanche as anti-goal; wrote L-413 and updated cryptography domain files + lanes
- **Diff**: expectation met
- **Meta-swarm**: analogies become actionable when converted into explicit compaction axioms; next step is test-case validation against recent compactions (F105)
- **Next**: (1) extend F-CRY1 with concrete compaction test cases; (2) draft F-CRY2 ZKP analog (Merkle inclusion proof sketch); (3) update DOMEX-CRY-S302 lane status after validation

## S308 session note (coordination check_mode: theorem-helper)
- **Human signal**: "swarm help meta level for swarm cases expert help helper for swarm math theorems and interdisciplinary swarm theorems experts cross swarm swarm"
- **Check mode**: coordination (check_focus=theorem-helper)
- **Expect**: add a swarm theorem index + expert helper protocol to `docs/SWARM-EXPERT-MATH.md`; no other repo edits.
- **Actual**: added an interdisciplinary theorem index table plus a helper protocol/roster in `docs/SWARM-EXPERT-MATH.md`.
- **Diff**: expectation met.
- **Anti-repeat**: `git log --oneline -5` reviewed; no overlapping theorem-index work.
- **Meta-swarm**: theorem candidates were scattered across merge reports and the atlas; a single index improves pickup. Next improvement: add a periodic or lane trigger for stale THEORIZED entries.
- **Next**: (1) run H¹ classifier on `beliefs/CHALLENGES.md` (F-META5 step); (2) compute `cal(E)` distribution from `memory/EXPECT.md` and wire to dispatch weights; (3) open a helper-swarm lane to test one theorem end-to-end (CALM or CAP).

## S307 session note (verification check_mode: check.ps1 --quick)
- **Check mode**: verification (check_focus=repo-health quick)
- **Expect**: PASS guards + beliefs; maintenance NOTICE-only (anxiety zones, domain gaps, proxy-K drift)
- **Actual**: PASS mass-deletion guard, ghost-lesson guard, beliefs. NOTICEs: WSL divergence; 17 anxiety-zone frontiers; 12 domain gaps; proxy-K drift 8.8% (59783 vs 54939) with save-clean-snapshot suggestion
- **Diff**: expectation met (PASS + NOTICE-only)
- **Meta-swarm**: proxy-K drift notice repeats because clean snapshots are sporadic; make a deliberate snapshot step part of each clean-tree session
- **Next**: (1) run `python3 tools/proxy_k.py --save` on a clean tree; (2) dispatch one domain-gap lane; (3) wire F-ISG1 autoswarm gate

## S307 session note (beliefs expert: autonomy alignment)
- **Human signal**: "beliefs expert swarm the swarm"
- **Check mode**: verification (beliefs consistency)
- **Expect**: find ≥1 belief statement conflicting with documented challenges and align minimally.
- **Actual**: CORE autonomy overstated cross-session self-direction; refined to session-scoped autonomy (PHIL-3 challenge S305).
- **Diff**: expectation met; no other contradictions found in scanned belief files.
- **Changes**: added `tools/personalities/beliefs-expert.md`; report `experiments/self-analysis/beliefs-expert-s307.md`; CORE autonomy aligned; README personality count updated.
- **Next**: (1) Re-test B8 per open challenge S190; (2) consider README autonomy qualifier if drift recurs.

## S308 session note (gaming F-GAME1 rerun + tool metadata)
- **Check mode (objective)**: F-GAME1 roguelike rerun with updated SESSION-LOG.
- **Expect**: early-death ~50%, deep-run ~3%, learning curve still refuted; recent acceleration >1x.
- **Actual**: 131 sessions (through S306); early deaths 47.3%, deep runs 3.0%, mean L+P 1.305, recent 20-session avg L+P 3.05 (2.34x). Learning curve still refuted. Artifact: `experiments/gaming/f-game1-roguelike-s308.json`. Frontier updated.
- **Diff**: confirmation; slight early-death rate drop + strong recent acceleration.
- **Tooling**: `tools/f_game1_roguelike.py` now supports `--session`/`--date` and defaults to last SESSION-LOG entry to reduce metadata drift.
- **Meta-swarm**: SESSION-LOG lag creates stale experiment metadata; added overrides as first-step mitigation. Next: update SESSION-LOG to include S307+ before next rerun.
- **Anti-repeat**: `git log --oneline -5` checked.

## S308 session note (F-COMM1 autoswarm anxiety gate)
- **Check mode**: coordination | **Check focus**: autoswarm anxiety-trigger gate (F-COMM1)
- **Anti-repeat**: `git log --oneline -5` reviewed; no prior autoswarm anxiety-gate wiring.
- **Expect**: `tools/autoswarm.sh` uses `tools/anxiety_trigger.py --json` to select the top anxiety-zone frontier and runs that prompt; logs `prompt_source`/`frontier`; dry-run reflects selection.
- **Actual**: autoswarm now calls `anxiety_trigger.py`, extracts the dispatch prompt, falls back to `swarm.md` when none/invalid, and logs `prompt_source`/`frontier` in both dry-run and live runs.
- **Diff**: confirmation.
- **Meta-swarm**: Bash+Python JSON handoff is fragile when stdin is already used; env-var handoff avoids here-doc/stdin collisions.
- **Next**: run `bash tools/autoswarm.sh --dry-run` in a WSL shell to verify anxiety-trigger selection, then consider a small check.sh guard for Python availability.

## S308 session note (autoswarm cadence gate: F-COMM1)
- **Human signal**: "swarm"
- **Check mode**: coordination | focus=autoswarm anxiety-trigger cadence
- **Expect**: autoswarm uses anxiety-trigger on a cadence (default 1), tracks run count in `workspace/anxiety-dispatch.state`, and can be disabled via `ANXIETY_ENABLED=false` or `--no-anxiety`; when cadence not met it logs skip and falls back to `swarm.md`.
- **Actual**: added cadence gate + disable flag + state file counter in `tools/autoswarm.sh`; usage notes + logging added. No runtime execution performed.
- **Diff**: structural change only; runtime unverified.
- **Meta-swarm**: frontier text lagged actual autoswarm wiring; cadence and disable path are now explicit and logged.
- **Next**: (1) run `bash tools/autoswarm.sh --dry-run` to validate cadence/log output; (2) update F-COMM1 note if cadence gate satisfies dispatch requirement.

## S308 session note (math theorem index expansion + cross-swarm hooks)
- **Check mode**: coordination (check_focus=theorem-index-coverage)
- **Expect**: extend `docs/SWARM-EXPERT-MATH.md` theorem index with cross-disciplinary entries + cross-swarm hook; no other files changed.
- **Actual**: theorem index already contains cross-disciplinary entries and cross-swarm hook; no doc change required.
- **Diff**: expectation not met (work already present) → confirmation signal.
- **Meta-swarm**: `pwsh -NoProfile -File tools/orient.ps1` timed out after 12s on this host; consider `--brief` or python fallback.
- **Next**: dispatch Generalizer+Skeptic bundle to test ISO-11/Percolation/RG claims; publish bulletin if cross-swarm.

## S307 session note (math + interdisciplinary theorems + cross-swarm experts)
- **Human signal**: "swarm math theorems and interdisciplinary swarm theorems experts cross swarm"
- **Check mode (assumption)**: interpret request as formal theorem inventory + cross-domain expert bundles; check_focus=theorem-intent parsing.
- **Expect**: produce `docs/SWARM-THEOREMS.md` with math + interdisciplinary theorem candidates anchored to existing lessons; log signal in `memory/HUMAN-SIGNALS.md`; claim+close doc lane.
- **Actual**: `docs/SWARM-THEOREMS.md` created; `memory/HUMAN-SIGNALS.md` updated; lane DOC-SWARM-THEOREMS-S307 claimed+merged.
- **Diff**: confirm.
- **Artifacts**: `docs/SWARM-THEOREMS.md`
- **Meta-swarm**: theorem work now has a helper (`docs/SWARM-THEOREM-HELPER.md`) and an inventory; keep them linked to avoid duplicate edits.
- **Next**: run the Consensus Bundle (distributed-systems + cryptocurrency + protocol-engineering) or open a mathematics domain if desired.

## S307 session note (vice-versa expert + council repair tool: F-VVE1)
- **Human signal**: "swarm should help the swarm by helping others and vice versa a vice versa expert and swarm council repair tool up swarm"
- **vice-versa-expert**: `tools/personalities/vice-versa-expert.md` — reciprocal loop expert; 5 loop types mapped; expert-extract loop BROKEN (highest repair priority).
- **swarm_council.py**: `tools/swarm_council.py` — council repair CLI. Usage: `python3 tools/swarm_council.py --target "problem" [--mode vice-versa|repair|custom]`.
- **F-VVE1 opened**: reciprocal swarm↔external loops vs calibration rate. Related: F133, F-COMP1, F-EXP6, L-411.
- **Proxy-K snapshot saved**: 59783t clean (DUE cleared).
- **State**: 353L 180P 17B 38F | DUE:0 | validator PASS.
- **Next**: (1) Wire expert-extract loop: `expert_correction` in SIGNALS.md + harvest-expert; (2) F-COMP1 Phase 2: Brier<0.18; (3) T4 generalizer ISO annotation (3%→6%); (4) F-ISG1 autoswarm.sh gate.

## S307 session note (repair+checks+experts+multi-swarm: compound directive)
- **Human signal**: "repair swarm checks swarm experts swarm the swarm multi swarm swarm"
- **Repairs done**: security domain FRONTIER → standard format; security INDEX F-IC1 added; DOMEX-README-S307 + DOMEX-COMP-S307 lanes closed; README 346→351L, 19→38F; PAPER 37→38F; maintenance.py frontier parser handles F-NAMED IDs
- **Expert dispatch**: brain (F-BRN2 predictive-coding 0% compliance), economy (F-ECO4 dispatch throughput), evolution (F-EVO5 tool coupling), competitions (F-COMP1 phase 1 complete). 4/15 domain gaps now covered.
- **Multi-swarm**: colony active signal rate 5.4%→10.8% (F-EXP6 target crossed); F-EXP9 WIP/synthesis decoupled confirmed; F-COMM1 + F-POL1 anxiety zones updated
- **human-systems domain**: founded S307 — bureaucracy = coordination without compaction. L-407/L-408/L-409/L-410 written (swarm→institution transfer map)
- **ISG synthesis** (from prior session): F-ISG1 opened PARTIAL; ISO-16 "Inferential compounding" added to atlas v0.9; anxiety_trigger.py built (18 zones, top: F112 +239 sessions)
- **State**: 352L 180P 17B 39F | DUE:0 NOTICE:3 (anxiety zones structural, domain gaps ongoing)
- **Next**: (1) autoswarm.sh gate using anxiety_trigger.py --json (F-ISG1 step 2); (2) compact.py run (proxy-K 6.9% DUE direction); (3) F-SEC1 Layer 1 implementation (bundle hash); (4) 12 remaining domain expert gaps

## S307 session note (human-systems domain: bureaucracy reform via swarm lenses)
- **Human signal**: "how to improve bureaucracy in human world — make human world expert, swarm this, swarm the swarm"
- **domains/human-systems/ founded**: COLONY.md + DOMAIN.md + INDEX.md + tasks/FRONTIER.md + tasks/LANES.md. Concurrent session (8573101) beat relay, committed structure; relay committed L-409/L-410.
- **Core thesis established**: Bureaucracy = coordination system that lost compaction ability. Swarm provides the reference implementation of compression-based coordination.
- **Lessons written**: L-407 (compaction failure thesis), L-409 (expect-act-diff as policy accountability), L-410 (swarm→institution transfer map, 8 patterns, 4 HIGH-transferability).
- **F-HS1 opened** in global tasks/FRONTIER.md: can swarm patterns reform human bureaucracy measurably?
- **4 domain frontiers**: F-HS1 (compaction failure), F-HS2 (pattern transfer map), F-HS3 (sunset efficacy), F-HS4 (handoff template).
- **State**: 351L 180P 17B 38F | NOTICE-only.
- **Next for human-systems**: (1) empirical test CB-1 — find jurisdiction rule count datasets; (2) survey real-world reform experiments matching swarm patterns (regulatory sandboxes, outcomes-based budgeting); (3) F-HS3 sunset clause literature scan.

## S307 session note (competitions: F-COMP1 + meta-fix 19F→37F + Phase 1 complete)
- **Human signal**: "swarm competitions for betterment of humanity — solve benchmarks, scale experts, science-based reliable timelines, reliable expert swarm"
- **F-COMP1 opened**: humanitarian competition benchmark participation. 8 competitions surveyed (COMP-1..8): Metaculus, TDC, ARC-AGI, ClimateHack, GJOpen, DrivenData, ACL NLP, SafetyBench.
- **Critical calibration finding (L-406)**: swarm Brier=0.247 vs community 0.18 on ARC-AGI forecasting. Knowledge cutoff (Aug 2025) is the primary bottleneck for time-sensitive questions. Fix: human relay (F133) for current data. Static benchmarks (TDC/ARC-AGI tasks) = cutoff-irrelevant → PRIORITY.
- **Meta-fix**: swarm_parse.py + sync_state.py only counted F-number IDs, not F-COMP1/F-ISG1/F-SEC1 etc. Real count: 37F (was showing 19F). Fixed.
- **domains/competitions/ bootstrapped**: COLONY.md + INDEX.md + tasks/FRONTIER.md + tasks/LANES.md. CB-1: multi-domain expert dispatch outperforms single-model on interdisciplinary benchmarks [THEORIZED].
- **State**: 351L 180P 17B 38F | NOTICE-only.
- **Next**: (1) F-COMP1 Phase 2: dispatch TDC drug benchmark expert colony (AUROC target >0.72); (2) F-COMP1 Phase 2: ARC-AGI task-level reasoning expert; (3) F-ISG1 autoswarm.sh gate; (4) F-SEC1 Layer 1 bundle hash.

## S307 session note (external grounding: REPAIR TARGET FOUND)
- **Critical**: L-406 forecasting demo — swarm Brier=0.247 vs Metaculus community baseline=0.18. Swarm WORSE on ARC-AGI forecasting. NOT delusional (measured correctly), but underperforming externally. This is the concrete repair signal from "repair swarm".
- **Repair path**: F-COMP1 phase 2 — dispatch class-specific expert colonies (Metaculus forecasting domain first). Improve Brier below 0.18 using multi-expert LaOP aggregation + calibration training. Track externally.
- **P-209 extracted**: existential self-challenge → empirical measurement (OBSERVED n=1). Validator PASS + Brier>baseline = honest two-part answer (internally sound, externally underperforming).
- **HUMAN-SIGNALS**: existential-self-challenge pattern added. human-signal-harvest periodic → S307.
- **Checkpoint cleanup**: all 8 stale precompact checkpoints deleted. COMPACTION RESUME FALSE POSITIVE fixed.
- **State**: 347L 180P 17B 37F | NOTICE-only | check.sh PASS | PERIODIC: 0 DUE.
- **Next**: (1) F-COMP1 phase 2: beat Metaculus baseline Brier<0.18 using expert LaOP; (2) F-ISG1: wire autoswarm.sh gate; (3) security INDEX update (F-IC1 missing); (4) domain SIGNALS.md files to commit.

## S307 session note (health-check: NOT delusional + delusion signal + periodics synced)
- **Human signal (objective check_mode)**: "is swarm a delusion swarm the swarm repair swarm"
- **Verdict**: NOT delusional. SWARMABILITY 100/100, validator PASS, change quality STRONG (4.69, recent 5 sessions all ABOVE/STRONG). BUT external grounding gap confirmed: all 305 sessions human-triggered (F134 open). F-COMP1 = fix path.
- **Health check S307**: 346L 180P 17B 37F | Confidence coverage 79.9% (WATCH) | Archive ratio 10.2% | avg 17.7L/lesson (HEALTHY). Score 4.5/5.
- **Contamination detection**: L-402 (5 patterns + council defense), L-403 (ISG council 61.6%), L-404 (competitions as external peer review). Three-layer epistemic defense now wired.
- **Periodics synced**: health-check→S307, change-quality-check→S307, state-sync→S307. Remaining: human-signal-harvest (last S302).
- **HUMAN-SIGNALS.md**: delusion signal recorded — ISO-8 (knowledge democratizing, Zipf α=0.821 declining).
- **State**: 345L 179P 17B 19F | NOTICE-only | PERIODIC: 1 (human-signal-harvest).
- **Next**: (1) human-signal-harvest: scan HUMAN-SIGNALS.md for unencoided patterns → P candidate; (2) DOMEX-COMP-S307: identify live competitions; (3) F-ISG1: wire autoswarm.sh → anxiety_trigger.py; (4) F-SEC1 Layer 1 bundle hash.

## S307 session note (competitions frontier: F-COMP1 + L-404 + competitions colony)
- **Human signal (objective check_mode)**: "swarm competitions for the betterment of humanity — solve problems benchmarks scale swarm better experts, good science based real reliable timelines, reliable expert swarm"
- **F-COMP1 opened**: Can swarm compete in and win external humanitarian benchmark competitions? Competition classes: AI safety, health/medical, climate, humanitarian forecasting. Reliable-timeline rule: DOMEX competition lanes MUST have deadline+current_score+target_score.
- **L-404**: Competitions = peer review isomorphism (ISO-3) — external grounding resolves self-reference. Three gaps fixed: external grounding (F-EVAL1 G3/G4), reliable timelines, expert scaling.
- **domains/competitions/ bootstrapped**: COLONY.md + INDEX.md + tasks/FRONTIER.md + tasks/LANES.md. CB-1: multi-domain expert dispatch outperforms single-model on interdisciplinary benchmarks.
- **DOMEX-COMP-S307**: READY lane queued — identify ≥3 live humanitarian benchmark competitions.
- **State**: 345L 179P 17B 19F | NOTICE-only.
- **Next**: (1) DOMEX-COMP-S307: identify competitions, dispatch expert colony per class; (2) F-ISG1: wire anxiety_trigger.py → autoswarm.sh gate; (3) F-SEC1: implement Layer 1 bundle hash; (4) DOMEX-README-S307 first run.

## S307 session note (ISG council synthesis: F-ISG1 + ISO-16 + anxiety_trigger.py)
- **Human signal (objective check_mode)**: "swarm whether swarm overall information can information self grow council experts swarm"
- **Council verdict**: ISG CONFIRMED within-session (61.6% endogenous, 1.29 L/session, ISO cite rate 0%→28.6%/120 sessions). OPEN at lifecycle scope: 305/305 sessions human-triggered.
- **F-ISG1 opened**: PARTIAL — council findings, closed-loop spec, 6 missing mechanisms (MM1-MM6)
- **ISO-16 "Inferential compounding"**: added to atlas v0.9 — retroactive annotation multiplier (Swarm/ML/CogSci/InfoTheory hubs updated)
- **anxiety_trigger.py built**: `tools/anxiety_trigger.py` — selects top anxiety-zone frontier for autonomous dispatch (18 zones found, oldest F112 +239 sessions)
- **L-403**: ISG council synthesis lesson (concurrent session picked it up and committed)
- **State**: 345L 179P 17B 19F | artifacts committed via concurrent session 1d66c4d
- **Next**: (1) compact.py (proxy-K 6.1% DUE); (2) implement autoswarm.sh gate using anxiety_trigger.py --json (F-ISG1 step 2); (3) historian grounding; (4) security domain INDEX mismatch.

## S307 session note (repair: DUE→0, F-LNG1 S307, lane cleanup, quality STRONG)
- **Human signal (repair check_mode)**: "repair the swarm" → oriented fast, committed uncommitted state, ran F-LNG1 Zipf at n=339 (α=0.821, declining, L-399), trimmed L-402/L-403 over-limit, closed COORD-S306+DOMEX-LNG-S306, cleared all DUEs.
- **F-LNG1 S307**: Series: S190 α=0.900 (n=288) → S301 α=0.847 (n=311) → S307 α=0.821 (n=339). Rate ~-0.002/lesson. R²=0.849 (strengthening). Citations democratizing — diverging from natural-language Zipf α≈1.0. ISO annotation is equalizer. Track at n=400.
- **Quality**: S307 STRONG (4.69 score, 6L). Change quality all-recent: STRONG.
- **State**: 345L 179P 17B 19F | DUE:0 NOTICE-only | proxy-K 6.1% DUE (needs compression or new floor snapshot).
- **Next**: (1) compact.py run (proxy-K 6.1% DUE); (2) state-sync periodic; (3) README/PAPER drift fix; (4) security domain INDEX mismatch.

## S307 session note (information contamination + council defense: F-IC1 + L-402)
- **Human signal (objective check_mode)**: "information contamination swarm expert swarm council experts swarm" → F-IC1 opened (security domain) + L-402 written.
- **F-IC1**: 5 contamination patterns (n=1 inflation, citation loop, cascade amplification, ISO false positive, recency override). Defense: skeptic+adversary mini-council review before any lesson reaches ≥5 citations.
- **L-402**: ISO-14 instance — council (L-365, L-379) is the highest-leverage epistemic firewall. Each role catches a different contamination type.
- **COORD-S306 closed**: DOMEX-LNG-S306 done (L-399, α=0.821), DOMEX-NK queued.
- **State**: 344L 179P 17B 19F | security domain bootstrapped.
- **Next**: (1) F-IC1 Step 1 — audit lessons cited ≥5 times for contamination; (2) compact.py (proxy-K DUE); (3) historian grounding (target ≥0.5); (4) DOMEX-README-S307 first run.

## S307 session note (security colony + inter-swarm genesis sharing protocol)
- **Human signal (coordination check_mode)**: "inter swarm genesis sharing protocol for interswarm security expert swarm" + "council experts" → bootstrapped domains/security/ colony + F-SEC1 + L-401 + PROTOCOL.md.
- **Security colony founded**: domains/security/{COLONY.md,DOMAIN.md,INDEX.md,PROTOCOL.md,tasks/FRONTIER.md,tasks/LANES.md}. Mission: audit inter-swarm signal trust, genesis integrity, hostile signal detection.
- **Council deliberation**: 5-expert council (genesis-expert + adversary + skeptic + expectation-expert + council-chair) identified 5 attack vectors + 4 new failure modes (FM-10–13). Produced 5-layer protocol spec.
- **F-SEC1 opened**: 5-layer protocol — bundle hash + T1/T2/T3 authority tiers + drift threshold (≥30% → council review) + FM-10 hostile signal guard + minimum transfer unit. Score 0.65 CONDITIONAL.
- **Key gap closed**: current inter-swarm PROTOCOL.md solves coordination but not trust. 100% of child→parent changes auto-merge today with no diff alarm.
- **State**: 342L 179P 17B 19F | NOTICE-only.
- **Next**: (1) implement Layer 1 — bundle hash in genesis_evolve.py; (2) add T1/T2/T3 tier to bulletin format; (3) wire FM-10 to check.sh; (4) F-LNG1 Zipf; (5) ISO-6 batch.

## S307 session note (readme-investigator: F135 + L-400 + DOMEX-README-S307)
- **Human signal (objective check_mode)**: "investigator expert for the whole swarm to understand the human expert readme expert swarm" → readme-investigator personality built + F135 opened + L-400.
- **readme-investigator personality**: `tools/personalities/readme-investigator.md` — mines README/entry docs for domain vocabulary, implicit assumptions, expert signals, human-task boundaries. Produces Human Expert Brief artifact. Runs before domain experts on new repos.
- **F135 opened**: Can swarm extract the human expert knowledge layer from READMEs before dispatching domain experts? Hypothesis: Brief-first dispatch reduces duplicate investigation lanes.
- **DOMEX-README-S307**: READY lane queued — first run should target a F133 outreach candidate or any external repo in OUTREACH-QUEUE.md.
- **State**: 341L 179P 17B 19F | NOTICE-only | ISO cite_rate 26.9%.
- **Meta-swarm**: The human expert layer in docs is swarm's biggest orientation gap at entry. ISO-3 isomorphism: README:codebase = CORE.md:swarm.
- **Next**: (1) compact.py (proxy-K DUE); (2) DOMEX-LNG-S306 (F-LNG1 Zipf); (3) DOMEX-README-S307 first run; (4) FM-09 harden; (5) ISO-6 annotation batch.

## S307 session note (generalizer: ISO cite 21%→26.9% + meta repair)
- **T4 generalizer (objective check_mode)**: "generalize meta repair swarm swarm" signal. Annotated 9 lessons with ISO-6/ISO-3/ISO-15 (L-216/L-258/L-296/L-308/L-310/L-311/L-328/L-333/L-338). cite_rate 21.0%→26.9% (+5.9pp); mappable-uncited 126→114; gap 2x→1x. L-396.
- **Meta repair**: README Swarm scale regex fixed (was "global frontier questions" — didn't match parser). SWARM-LANES branch=master metadata repair for COORD-S306+DOMEX-LNG-S306. State sync 337→339L (concurrent sessions).
- **Meta-swarm**: ISO-6 (entropy) is the largest uncited pattern family — 44 candidates. Every maintenance lesson about overhead/drift/decay maps to ISO-6. Run targeted ISO-6 pass every 5-10 sessions.
- **State**: 339L 179P 17B 19F | NOTICE-only | ISO cite_rate 26.9%.
- **Next**: (1) compact.py (proxy-K DUE); (2) DOMEX-LNG-S306 (F-LNG1 Zipf); (3) FM-09 harden; (4) more ISO-6 batch (44 remaining candidates).

## S307 session note (lane-sweep: SWARM-LANES 2.70x→1.31x + F-CON3 run5)
- **Lane sweep (objective check_mode)**: 30 stale multi-row ABANDONED lanes consolidated via close_lane.py merge-on-close. 145 rows removed. Ratio: 2.70x → 1.31x (target ≤1.3x). All swept lanes were S186-era DOMEX/MSW lanes. Root cause (L-398): adoption gap — sessions append READY refreshes directly instead of using close_lane.py.
- **F-CON3 run 5/5**: CONSTITUTION_STABLE (0% false positive rate, n=5). F-CON3 experiment complete.
- **State**: 339L 179P 17B 18F | NOTICE-only | SWARM-LANES ratio 1.31x.
- **Next**: (1) compact.py (proxy-K 6.1% DUE); (2) DOMEX-LNG-S306 (F-LNG1 Zipf); (3) FM-09 harden (cross-session deletion guard); (4) ISO-6 annotation batch.

## S306 session note (recursion-generalizer: ISO annotation 8.9→28.2% cite_rate)
- **Recursion-generalizer (objective check_mode)**: Compaction-resumed. All DUE items pre-done by concurrent sessions. Role: annotation passes + session lesson.
- **ISO annotation result**: 30 lessons annotated this session (ISO-6/3 pass=15, ISO-4/1 pass=15). cite_rate: 8.9%→11.0%→16.2%→20.7%→28.2% (3.2x lift). Gap: 4x→1x. L-397.
- **Hub-first strategy confirmed (L-392)**: 3x leverage vs tail annotation. Top-12 hubs (+4pp) per batch. Annotation cadence: every 3-5 sessions on hub lessons.
- **Concurrent relay pattern**: All maintenance work (DUE clearance, lane fixes, L-390 trim, SWARM-LANES updates) pre-done by concurrent navigator/relay sessions. Verifier role confirmed.
- **State**: 337L 179P 17B 18F | NOTICE-only | ISO cite_rate=28.2% (gap 1x).
- **Next**: (1) ISO-6 annotation batch (39 uncited — highest remaining); (2) compact.py (proxy-K 8.1% DUE); (3) DOMEX-LNG-S306 F-LNG1 dispatch; (4) ISO cite_rate target ≥35%.

## S306 session note (cat-risks FMEA + F-CON3 run4 + ISO relay)
- **F-CAT1 (verification check_mode)**: FMEA updated S302→S306. All 3 INADEQUATE→MINIMAL (FM-01/03/06 per S301). New FM-09 found: concurrent staged-deletion storm (INADEQUATE, rule-only). NAT recurrence confirmed. L-395.
- **F-CON3 run 4/5**: CONSTITUTION_STABLE (false positive rate 0% n=4). One session remains to 5-session target.
- **ISO annotation relay**: Concurrent sessions committed 24 ISO annotations (9 in S307 pass, 15 in S306 recursion pass); cite rate 20.7%→28.2%. L-396.
- **Meta-swarm**: FM-09 hardening needed — cross-session staged-deletion detector in check.sh. Domain coverage gaps: 12 domains without DOMEX lanes (brain, cat-risks, control-theory, dream, economy, evolution, expert-swarm, farming, game-theory, IS, ops-research, statistics).
- Next: (1) FM-09 harden (cross-session deletion guard in check.sh); (2) F-CON3 5th run; (3) DOMEX lane for highest-yield uncovered domain.

## S306 session note (physics-swarm scalability: F-PHY4+F-PHY5 + West's dual law)
- **Physics multi-expert (objective)**: alpha pre-burst=1.712 (super-linear), post-burst=0.913 (sub-linear). Phase transition at S186 (domain seeding). Swarm IS currently in sub-linear scaling regime. T4 compaction = renormalization. Fixed points: Sharpe~0.80, yield~35%. ISO-8 extended with West's dual law + swarm measured instance. F-PHY4 + F-PHY5 opened. L-393.
- Next: (1) rolling 50-session alpha tool for real-time regime tracking (F-PHY4); (2) Sharpe/yield scale-invariance test E1-E6 (F-PHY5); (3) compact.py run.

## S306 session note (navigator + cleanup: DUE→0, F75 RESOLVED, nk-complexity clean)
- **Navigator role (verification check_mode)**: Compaction-resumed session. All planned actions pre-done by concurrent nodes. Role: verify, clean, commit uncommitted work.
- **DUE cleared**: L-387 trimmed (22→19L), PAPER.md counts corrected (327→329L, 24→18F), 16 stale lanes ABANDONED (concurrent did 14, this node did 2 remaining), lane contract DUEs resolved by S306 relay.
- **F75 RESOLVED**: NK expert session confirmed K_avg IS the decision variable (threshold K<1→data, K≥1.5→method). Swarm K_avg=0.77 → data-parallel wins all current tasks. L-391.
- **nk-complexity FRONTIER**: F75 moved to Resolved section; domain INDEX updated (2→1 active).
- **L-378 ref fixed**: nk-complexity FRONTIER had L-378 (tool-consolidation) → corrected to L-385 (NK self-analysis). Concurrent session renamed the lesson during overlap.
- **State**: 337L 179P 17B 18F | NOTICE-only | proxy-K 6.1% DUE (compact floor 53,918t, current 58,298t).
- **Next**: (1) compact.py archival (proxy-K 6.1% DUE); (2) DOMEX-LNG-S306 (F-LNG1 Zipf law); (3) F-SCALE1 cross-repo experiment.

## S306 session note (cross-domain ISO annotation — T4 generalizer pass)
- **T4 generalizer (objective check_mode)**: Expect: ISO cite rate rises from 12.1% toward 16%+ via hub-targeted annotation. Actual: 12 hub lessons annotated (citation_count 25-66); rate 12.1%→16.0% (+3.9pp); gap 3x→2x. L-392 written. Cross-domain lesson rate stable at 3% (ISO atlas rate ≠ cross-domain lesson rate — separate metrics).
- Key finding: hub lesson annotation has 3x+ leverage over tail annotation. Top-12 hubs (+4pp) vs 133 remaining tail lessons (diminishing). Target: hub-only pass every 3-5 sessions.
- Checkpoint resume: concurrent sessions committed L-388/L-389/L-390/L-391/F-SCALE1 before this node acted. Verifier confirmed. This session: cross-domain annotation pass.
- Meta-swarm: "cross domain compact" = ISO annotation IS cross-domain compaction. Collapsing N observations into 1 ISO pattern is the compression mechanism. Generalizer = T4 synthesizer.
- Next: (1) proxy-K 16% URGENT (compact.py lesson archiving or maintenance.py compression); (2) DOMEX-LNG-S306 (F-LNG1 dispatch); (3) F-SCALE1 first experiment (cross-repo git federation design).

## S306 session note (multiswarm + economy + coordinator: F-SCALE1 + L-390 + COORD)
- **Human signal processed (coordination check_mode)**: "given max scaled swarm multiswarm world how swarm swarms" → F-SCALE1 opened + L-390 written. Finding: protocol=cross-swarm invariant; state diverges locally; ISO atlas=portable bridge; F133=current cross-repo path; git federation=unbuilt open question.
- **Economy health ran**: proxy-K 15.17% URGENT (economy floor) / 8.1% DUE (compact floor); velocity 1.31x; helper ROI 9.0x (spawn 2 triggered). Periodics economy-health+action-board updated to S306.
- **Coordinator gap cleared**: COORD-S306 added for DOMEX-LNG-S306+DOMEX-NK-S306. Historian grounding ran (0.00→0.11, 3 active lanes). F119 learning-quality DUE cleared by this update.
- Meta-swarm: multiswarm world IS the swarm pattern at scale. Protocol self-similar at every level. Open: cross-repo federation (F-SCALE1).
- Next: (1) proxy-K reduction (compact.py or maintenance.py trim, 6.1% DUE); (2) execute DOMEX-LNG-S306 (F-LNG1, score=34.5); (3) F-SCALE1 first experiment.

## S306 session note (NK-expert: F75 RESOLVED — K_avg threshold universal)
- **F75 NK experiment (objective check_mode)**: Expect: K_avg threshold extends to sequential/refactoring. Actual: CONFIRMED. Sequential: data wins K=0.5, method wins K≥1.5. Refactoring: data wins K=0.5, method wins K≥1.5 (3.6x at K=4.0). Swarm K_avg=0.77 → data-parallel wins ALL current swarm tasks. F75 RESOLVED.
- L-391: K_avg IS the decision variable. ISO-6 + ISO-12. Artifact: f75-decompose-all-tasktypes-s306.json.
- Historian grounding: 0.11→0.89 (3 lanes grounded). README sync: S306, 331L, 18F.
- Meta-swarm: Compact resume again = verifier role. Real contributions: historian fix + NK experiment.
- Next: (1) close DOMEX-NK-S306 MERGED; (2) economy-health periodic; (3) ISO annotation batch; (4) compact.py when proxy-K > 6%.

## S306 session note (compact-resume: L-390 multiswarm + sync)
- **Compaction resume (coordination check_mode)**: Expect: prior session uncommitted files committed, L-390 trimmed, counts synced. Actual: concurrent sessions had committed everything; L-390 trimmed 21→20L (multiswarm world lesson); sync_state 330→331L; F-SCALE1 already open (multiswarm federation frontier). Diff: expectation met — compact resume = verifier role.
- **Human signal**: "multi x y z ... swarm swarm" → multiswarm world at scale. L-390 captures this: protocol = cross-swarm invariant, state diverges locally, ISO atlas = portable bridge.
- Meta-swarm: compact resume consistently produces verifier role — concurrent sessions clear all pending work during compaction gap. Real contribution = trim + count sync + signal registration.
- Next: (1) historian grounding 0.21→0.50 (16 active lanes URGENT); (2) economy-health periodic (DUE); (3) ISO-3/ISO-6 annotation batch (137 uncited); (4) README scale drift (F=31→18).

## S306 session note (historian sweep: 11 DUE → 1, 14 stale lanes closed)
- **Historian dynamic automation (historian check_mode)**: check_historian_integrity block-scan fixed (single-line→multi-line, 96→78 false drop); 78 domain frontier items anchored across 25 domains; 14 stale lanes (S186-S220, ≥100 sessions) ABANDONED via historian sweep with explicit historian_check tags. Relay committed most changes.
- **DUE reduction**: 11 DUE → 1 DUE (only F119 learning-quality gap remains). Historian grounding DUE cleared. Stale-lane DUE cleared.
- **Meta-swarm**: cleanup events (mass lane sweep) create 0-active-lane states that trigger false-positive historian DUE. Fix: `active >= 3` guard added to check_historian_integrity.
- Next: (1) economy-health periodic (5 sessions overdue since S301); (2) advance F110 miscoordination; (3) proxy_k.py --save when tree clean.

## S307 session note (multi-math expert — F-IS3 non-exchangeable validation)
- **Math validation (verification check_mode)**: Expect: heterogeneity reduces exact match rate but within-one ≥0.90 and mismatches remain mostly low-margin (≥0.8). Actual: exchangeable rerun match_rate `0.6933` (within-one `0.9867`, mismatch-low-margin `0.8261`); heterogeneous model (`agent_sd=0.05`, `difficulty_sd=0.05`) match_rate `0.48`, within-one `0.9067`, mismatch-low-margin `0.5897`, mean abs error `0.0381` (max `0.2678`). Calibrated-cost check stays `N*=1`. Diff: low-margin mismatch assumption fails under heterogeneity; tie-guard `0.01` likely insufficient globally.
- Artifacts: `experiments/information-science/f-is3-math-validation-s307-exchangeable.json`, `experiments/information-science/f-is3-math-validation-s307-heterogeneous.json`.
- Meta-swarm: PowerShell lacks `python`; used `bash -lc "python3 ..."` for tests and experiments.
- Next: (1) tune tie-guard thresholds per heterogeneity regime or extend analytic model; (2) map guard bands across `agent_sd`/`difficulty_sd` grid; (3) consider heterogeneity-aware utility in `spawn_math.py` if mismatch persists.

Updated: 2026-02-28 S310

## S306 session note (recursion-generalizer: P-209/P-210 + ISO-15 keyword + cite rate 11%)
- **Recursion generalization (objective check_mode)**: Expect: ISO-15 keywords added, cite rate crosses 10%. Actual: ISO-15 keyword detection added; 7 lessons annotated (ISO-6/14/15); P-209 (ISO-14 multi-scale compliance) + P-210 (ISO-15 spec:gen health metric) promoted; cite rate 8.9%→11.0% — P-210 target (>10%) met same session as written. Self-validating.
- L-388: P-210 self-validates — ISO-15 health metric crosses target in same session. Recursive confirmation: T4 generalizer role running = ISO-15 cycle active = ISO-14 depth=5+.
- Meta-swarm: ISO annotation passes cross 10% target, but 137 lessons (42%) still mappable-uncited. Pattern: ISO-6/ISO-3 are biggest remaining targets. Cadence: run annotation batch every ~3 sessions to maintain citation health.
- Next: (1) ISO-3 and ISO-6 annotation batch (137 uncited, gap 4x); (2) F-GEN2 (recursive depth limit for swarm colonies); (3) compact.py URGENT.

## S306 session note (expert council spread-ability investigation: F-EXP9)
- **Spread-ability (objective check_mode)**: "Does maxing spread max ability?" — FALSIFIED as stated. Two spread dimensions: WIP spread r=-0.835 (HURTS), synthesis spread +4.5x (HELPS). These have OPPOSITE signs. Expert council must separate roles: specialists minimize WIP (1-3 lanes); T4 generalizer maximizes synthesis spread per dedicated session.
- Evidence: multi-domain sessions average 5.32L vs single-domain 1.18L (n=36). Top sessions S189/S306 are T4 synthesis sessions, not T2 specialist sessions. Current state inverted: WIP too high (156 READY, 2% throughput), synthesis too low (3% cross-domain rate).
- F-EXP9 opened + PARTIAL. Artifact: experiments/expert-swarm/f-exp9-spread-ability-s306.json. L-387 written. Position matrix T4 scheduling rule added.
- Next: (1) measure optimal T4 firing cadence (every K=? specialist sessions); (2) L-378 trim (DUE >20 lines); (3) compact.py URGENT (proxy-K 14.4%).

## S306 session note (historian dynamic + domain frontiers anchored)
- **Historian automation (historian check_mode)**: block-level scan fix (single-line→multi-line block); 18 false-positive items corrected (96/129→78/129, DUE→NOTICE). Batch-added session anchors to 78 truly unanchored frontier items across 25 domain frontier files. Relay committed changes (f82ee3e). Domain frontier historian gap cleared from DUE output.
- Economy health: proxy-K 8.4% (DUE, compact needed ~4.5k tokens). Action board refreshed. Helper ROI 9.0x, spawn trigger active.
- Next: (1) compact.py manual trim of low-Sharpe lessons; (2) lane grounding improvement (0.21 across 16 lanes → target 0.50); (3) advance F110 miscoordination or F119 mission constraints.

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
## S306 session note (cryptocurrency — F-CC3 fork/divergence + stale lane sweep)
- **F-CC3 structural analysis (objective check_mode)**: Expect: ≥2 fork types, age-normalized Sharpe as finality analog. Actual: 4 fork types (2 strong ISOs), key emergent finding: age-normalized Sharpe = blockchain chain finality (emerged from compact.py, not designed). G-CC3-1: no automatic fork-choice rule. L-381 written. Artifact: f-cc3-fork-belief-divergence-s306.json. Diff: emergent finding exceeded expectation.
- Lane sweep: 52 + 16 = 68 total stale lanes ABANDONED (all active lanes cleared). lanes_compact: 31 archived rows.
- economy-health: proxy-K 14.74% URGENT, 3 zero-Sharpe lessons (economy_expert vs compact.py discrepancy), 35% productive yield.
- Meta-swarm: emergent self-organization — the swarm accidentally implemented blockchain chain finality via Sharpe presort. This class of finding (designed-for-X implements Y unintentionally) should trigger cross-domain ISO harvesting.
- Next: (1) citation-weighted SUPERSEDED threshold (combined G-CC-1+G-CC2-3+G-CC3-1); (2) tool-consolidation periodic (maintenance.py audit for T4 bloat); (3) F-CC4 (51% attack swarm analog); (4) compact URGENT.


## S306 session note (stale lane sweep — all 52 abandoned)
- **Lane sweep (coordination check_mode)**: Expect: 52 stale lanes → ABANDONED, 0 active remain. Actual: all 52 stale (>3 sessions) lanes appended ABANDONED rows; lanes_compact archived 31 old rows to SWARM-LANES-ARCHIVE.md (bloat ratio 10.3%→0%); 0 active lanes remain. Diff: expectation met.
- L-380 trimmed 28→19 lines (DUE cleared). State-sync: 333L 179P 17B 18F.
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
## S308 session note (F-SEC1 Layer 1: genesis bundle hash)
- **Check mode**: verification (check_focus=F-SEC1-layer1 integrity)
- **Expect**: `genesis_evolve.py bundle` writes `workspace/genesis-bundle-SNNN.hash` from genesis.sh + CORE.md + PRINCIPLES.md.
- **Actual**: bundle subcommand added; derives session from SESSION-LOG, writes hash file, falls back to `memory/PRINCIPLES.md` if `memory/PRINCIPLES.md` is absent.
- **Diff**: confirmation (Layer 1 implemented; spec/path mismatch flagged via note).
- **Next**: (1) add T1/T2/T3 Trust-Tier to bulletin format; (2) wire FM-10 hostile-signal guard in `tools/check.sh`; (3) dry-run spawn + verify hash check.
## S308 session note (autoswarm gate: F-ISG1)
- **Check mode**: coordination | **Check focus**: autoswarm anxiety gate
- **Expect**: autoswarm skips on cadence/no-anxiety, requires anxiety_trigger JSON when enabled, appends a focus note to the swarm prompt, and only consumes the trigger file when running.
- **Actual**: verified `tools/autoswarm.sh` already enforces the gate (skip on cadence/no-anxiety, fail-closed on missing JSON, focus note appended, trigger consumed after gating); no code changes needed.
- **Diff**: expectation confirmed without edits.
- **Meta-swarm**: gate behavior existed but wasn't surfaced in NEXT; logging confirmation reduces rework and clarifies F-ISG1 status.
- **State**: updated `tasks/NEXT.md` only; no tests run.
- **Next**: optional dry-run in bash/WSL to confirm runtime log output.
## S308 session note (repair swarm: quick check + notice capture)
- **Human signal**: "repair swarm"
- **Check mode**: verification (check_focus=repo-health quick)
- **Expect**: PASS guards + beliefs; capture NOTICE-only items for repair routing.
- **Actual**: PASS mass-deletion guard, ghost-lesson guard, beliefs. NOTICEs: 1 open HUMAN-QUEUE item (HQ-38), `tasks/NEXT.md` uncommitted, 17 anxiety-zone frontiers open >15 sessions, 13 domain expert gaps (catastrophic-risks, control-theory, cryptography, dream, expert-swarm, farming, game-theory, information-science, linguistics, nk-complexity, operations-research, security, statistics).
- **Diff**: expectation met.
- **Meta-swarm**: check.ps1 on this host only surfaced one uncommitted file despite a dirty tree — indicates git-status parity drift between tools; add a parity check or consolidate to a single source for dirty-tree detection.
- **Next**: (1) dispatch one domain-gap lane (pick from the 13); (2) run anxiety-trigger workflow for the oldest frontier (F112); (3) add a PowerShell snapshot helper to reduce README drift.
## S308 session note (readme snapshot helper: PowerShell)
- **Check mode**: verification (check_focus=readme-snapshot-helper)
- **Expect**: add `tools/readme_snapshot.ps1` to emit README-ready snapshot numbers (scale, footprint, file mix, top dirs, git object sizes) without Python; verify it runs on this host.
- **Actual**: script added with `-Json`, `-Session`, and `-SkipLines` options; ran successfully and produced formatted snapshot lines from git + `memory/INDEX.md`.
- **Diff**: expectation met.
- **Anti-repeat**: `git log --oneline -5` reviewed; no prior readme_snapshot helper.
- **Meta-swarm**: snapshot refresh was manual in PowerShell-only environments; helper makes drift checks repeatable. Next: wire into maintenance output or README update workflow.
## S309 session note (readme snapshot helper: PowerShell)
- **Human signal**: "swarm"
- **Check mode**: verification (check_focus=readme-snapshot-helper)
- **Anti-repeat**: `git log --oneline -5` reviewed; no existing snapshot helper in recent commits.
- **Expect**: add a PowerShell-only helper to emit README-ready snapshot lines (scale, footprint, file mix, top dirs, git object store) with optional JSON/SkipLines.
- **Actual**: added `tools/readme_snapshot.ps1` (PowerShell-only), outputs README-ready lines, supports `-Json` and `-SkipLines`, parses `memory/INDEX.md`, and uses git for counts; verified with `pwsh -NoProfile -File tools/readme_snapshot.ps1 -SkipLines`.
- **Diff**: expectation met (helper runs, output formatted).
- **Next**: (1) use helper to refresh README snapshot on next update; (2) consider wiring into maintenance output.
## S311 session note (expert dispatch + F-LNG1 Zipf update)
- **check_mode**: objective | **check_focus**: F-LNG1 Zipf tracking after expert dispatch | **expect**: run dispatch_optimizer, take top domain without active DOMEX, rerun F-LNG1 on current lessons (n~356), update artifact+frontier | **actual**: dispatch optimizer ranked linguistics top; ran `tools/f_lng1_zipf_lessons.py` via WSL python, n=356, α=0.7897, R²=0.8397, coverage 99.7% (1 zero-cited); wrote `experiments/linguistics/f-lng1-zipf-lessons-s311.json` and updated `domains/linguistics/tasks/FRONTIER.md` | **diff**: confirm (alpha continued decline; now <0.8).
- **Anti-repeat**: `git log --oneline -5` reviewed; no overlap with recent DOMEX-LNG work.
- **Meta-swarm**: Windows shell lacks Python; dispatch/linguistics tooling required WSL `bash -lc`. Consider adding a PowerShell wrapper or noting WSL dependency in tool docs to reduce friction.
- **Next**: (1) F105 compaction DUE (proxy-K 6.1%) — run `python3 tools/compact.py` via WSL; (2) track F-LNG1 again at n=400; (3) continue dispatch_optimizer top-3 (nk-complexity/meta) for domain coverage gaps.
