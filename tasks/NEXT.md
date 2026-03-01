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

## S338 session note (code-quality-expert: swarm_io.py extraction, 4 JSON fixes, L-482)
- **check_mode**: objective | **lane**: DOMEX-META-CQ-S338 | **dispatch**: meta (code quality expert)
- **expect**: ≥3 dead/redundant functions in maintenance.py; ≥1000t savings
- **actual**: 0 dead functions (all 37 check_* registered in main). Instead found 8 duplicate utility functions across 10+ files (~4000-5000t waste). Created `tools/swarm_io.py` (shared module: read_text, git_cmd, session_number, token_count, line_count). Wired 10 consumer files. Fixed 4 silent JSON parse failures in maintenance.py (now emit NOTICE). maintenance.py 26465t→25997t (-468t). L-482 written.
- **diff**: LARGE — expect was wrong. The T4 problem is NOT dead check functions, it's pervasive utility duplication. Every new tool copies _read/_git from nearest neighbor. swarm_io.py breaks this pattern.
- **meta-swarm**: Code quality audits must distinguish function-level dead code (rare — maintenance.py has good hygiene) from cross-file structural duplication (massive — 8 utilities × 10 files). The audit itself is a diagnostic tool; the fix (swarm_io.py) is structural.
- **State**: 420L 178P 17B 36F | swarm_io.py created | maintenance.py -468t | Drift 16.9% URGENT
- **Next**: (1) Phase 1 maintenance.py compaction (1432t zero-risk removals from L-478); (2) migrate remaining tools to swarm_io.py imports (est. 2000-3000t savings); (3) dormant domain activation wave (28 remaining); (4) sink sprint at N=450

## S338 session note (meta-scaling resume: LNG F-LNG1 α=0.7425, reach_map 67.3%, SWARM-LANES compact 85→4, L-476)
- **check_mode**: objective | **lane**: DOMEX-LNG-S338 | **dispatch**: linguistics C-03 (score=34.5)
- **expect**: α(N=411) ≈ 0.739 per power-law model; rate stable at -0.00231/L; no saturation yet
- **actual**: α=0.7425 at N=412 (direct scan); model prediction 0.739; error <0.004 (model VALIDATED). Rate slowed 10x (-0.00046/L vs -0.00231/L). Cache methodology revealed INCONSISTENT after DOMAIN.md enrichment. L-476. Reach map: 67.3% composite, domain activation 33% bottleneck (L-475 committed). lanes_compact archived 85 stale rows.
- **diff**: Rate slowdown was unexpected (10x, not incremental). Likely from K_avg sprint redistributing citations. Cache vs direct scan split is a new methodological finding.
- **meta-swarm**: MEMORY.md had stale resonance data (64/15 domains) — corrected to 161/40. Cache-based Zipf tool gives inflated α after DOMAIN.md enrichment; switching to direct scan as canonical.
- **State**: 419L 178P 17B 36F | α=0.7425 N=412 rate=-0.00046/L | reach 67.3% | maintenance.py 25,997t (-2,472t)
- **Next**: (1) Phase 1 maintenance.py compaction (1,432t zero-risk: _reason_action_evidence_sessions+F119 block); (2) 28 dormant domain activation wave (target 50% reach = 21 active, needs ~7 DOMEX dispatches); (3) sink sprint at N=450 (157 zero-in-degree lessons)

## S338 session note (DOMEX-META-S338: T4 compaction analysis — 4226t achievable 15.4%, L-478)
- **check_mode**: objective | **lane**: DOMEX-META-S338 | **dispatch**: meta C-01 (F-META1)
- **expect**: Identify ≥3 dead/redundant check functions in maintenance.py for removal, ≥1000t T4 reduction
- **actual**: CONFIRMED + exceeded. Full 2548L analysis. Total achievable: ~4226t (15.4%). Phase 1 (~1432t removals): _reason_action_evidence_sessions+F119 transition evidence (712t), check_mission_constraints self-ref (277t), runtime re-probe (280t), inline fallback (163t). Phase 2 (~1239t): shared helper extraction. Phase 3 (~1555t): message compression. T4 tier discovery: only 4 files count; nk_analyze/test_MC/belief_evolve are NOT in T4 tier. swarm_io.py pattern shifts helpers out of T4. L-478. S338 docstring pass already committed (-1036t).
- **diff**: More than expected — full structural analysis revealed redundant runtime probes and self-referential checks that are provably dead code. Phase 1 is zero-risk (static property assertions, never-reached branches).
- **meta-swarm**: T4 floor (S171, 167 sessions stale) is unrealistic target. Real goal = arrest growth. Each session should remove ≥500t. check_mission_constraints self-ref (reads own source at runtime to verify static structure) is the clearest example of code that can never fail if the file runs at all.
- **State**: 418L 178P 17B 36F | T4 compaction roadmap: 4226t achievable | SESSION-LOG gap S336-S338 FIXED
- **Next**: (1) Phase 1 removals (712+277+280+163 = 1432t zero-risk code removal); (2) dormant domain activation (28 dormant → 50% reach = 7 activations); (3) sink sprint at N=450

## S338 session note (expert-wave: 6 DOMEX lanes, 6 artifacts, 3 novelty domains activated, L-481)
- **check_mode**: objective | **lane**: expert-dispatch-S338 | **dispatch**: human signal ("experts needed for the swarm")
- **expect**: 3 existing DOMEX lanes executed + 3 novelty domains activated; ≥6 artifacts produced; domain reach rises from 21% toward 28%
- **actual**: CONFIRMED. 6 DOMEX lanes executed (META, NK, LNG, HLP, HS, STR), all MERGED. 6 experiment artifacts produced. 3 novelty domains (helper-swarm, human-systems, strategy) activated with first experiments. COUNCIL-REPAIR-S323 (+14 sessions stale) ABANDONED. K_avg=1.6562 at N=413. F-LNG1 α=0.7456 (12th point, 2nd stall). Maintenance.py compaction: 4,226t savings mapped (Phase 1: 1,432t zero-risk). NK defense-in-depth triad (governance/catastrophic-risks/game-theory) identified.
- **diff**: All 6 lanes opened, worked, and closed in one session — matches one-shot DOMEX norm (L-444). Domain reach: 21%→~28%. Expert utilization: 100% (6 DOMEX dispatches). Economy health: proxy-K drift 16.9% (was 64% at dirty tree estimate — cleaner now), production 4.44x above historical.
- **meta-swarm**: Parallel agent dispatch IS the scaling mechanism. One human signal → dispatch_optimizer → 4 parallel agents → 6 artifacts. The bottleneck is never dispatching — it's the 30+ dormant domains. At 4 agents/session, 50% reach requires ~3 more sessions of pure novelty dispatch.
- **State**: 417L 178P 17B 36F | 6 DOMEX MERGED | 3 novelty domains activated | K_avg=1.66 | α=0.7456 | Drift 16.9% URGENT
- **Next**: (1) execute Phase 1 maintenance.py compaction (1,432t zero-risk removals); (2) continue novelty domain wave (30 dormant remain, target 50% = 21 active); (3) NK domain integration sprint (governance P1, catastrophic-risks P2, game-theory P3); (4) sink sprint at N=450

## S338 session note (memory-automation: diagnostic-execution gap — MEMORY.md 217→81, tool-size gate, L-480)
- **check_mode**: assumption | **lane**: meta-memory-S338 | **dispatch**: human signal ("manage memory and automation better")
- **expect**: MEMORY.md compactable to ~150 lines; automation gaps diagnosable; at least one enforcement gate buildable
- **actual**: CONFIRMED + exceeded. MEMORY.md 217→81 lines (63% reduction, zero info loss — details to metrics.md + architecture.md topic files). Root cause diagnosed: swarm has 37 diagnostic checks but 0 execution automation (12/18 periodics overdue, 22/48 core tools unused). Tool-size gate added to check.sh (NOTICE on staged tools >5000t). L-480 written: "diagnostic-execution gap" as general pattern (ISO-6).
- **diff**: Expected ~150 lines, achieved 81 (better than expected). The "execution gap" insight generalizes L-472 (council-specific) to all automation. Key finding: periodics.json is advisory-only — no mechanism converts DUE → DOMEX lane.
- **meta-swarm**: The auto-memory (MEMORY.md) IS the swarm's cross-session memory. When it overflows, new sessions lose context. Self-compaction of memory is as important as compaction of knowledge (compact.py). Rule: every memory system needs a size governor and a compaction trigger.
- **State**: 417L 178P 17B 36F | MEMORY.md 81/200 lines | tool-size gate ACTIVE | Drift 16.9% URGENT
- **Next**: (1) compaction CRITICAL (maintenance.py 28k — split into modules); (2) periodic auto-scheduler (DUE → lane); (3) domain activation wave (28 dormant); (4) sink sprint at N=450

## S338 session note (self-diff council: can the swarm diff itself? PARTIAL — quantities yes, qualities no; tools/self_diff.py built, L-479)
- **check_mode**: objective | **lane**: DOMEX-META-DIFF-S338 | **dispatch**: human signal ("can the swarm diff itself properly consult diff expert and council")
- **expect**: Swarm has partial self-diff via expect-act-diff (P-182) and proxy-K; expect no unified tool
- **actual**: CONFIRMED. 14 quantitative measurement tools audited (proxy_k, compact, reach_map, change_quality, scaling_model, f_ctl2_diff_latency, maintenance×6, session_tracker, swarm_pr, f_con3). 0 unified self-diff tools existed. Built `tools/self_diff.py` — snapshots counts + hashes + metrics + belief status + lane health + proxy-K + EAD compliance. Council Mode A (5 domains: meta, evaluation, information-science, NK, governance) convened via `swarm_council.py`. L-479 written.
- **diff**: As expected — quantitative coverage strong, qualitative absent. Key gap: 22% EAD compliance despite P-182 doctrine. Hash-based content tracking closes "silent edit" detection gap. Remaining: belief content evolution, cross-domain flow matrix, self-model fidelity calibration.
- **meta-swarm**: The question "can the swarm diff itself" IS itself an expect-act-diff on the swarm's self-knowledge. Council synthesis across 5 domains identified ISO-17 (self-model coherence gap) as the structural pattern: identity fields 100%, evidence fields 22%. Building the tool makes the gap visible.
- **State**: 416L 178P 17B 36F | self_diff.py baseline saved | Council 3/10 seats | Drift URGENT
- **Next**: (1) compaction CRITICAL (maintenance.py 28k); (2) qualitative self-diff extension (git-log per file for content versioning); (3) belief status trajectory tracking; (4) cross-domain coupling matrix

## S338 session note (DOMEX-NK C-02: domain K_total maturity + K_avg=1.6141 at N=412, L-477)
- **check_mode**: objective | **lane**: DOMEX-NK-S338 | **dispatch**: nk-complexity C-02 (score=36.5)
- **expect**: Test F9-NK domain candidates (game-theory, catastrophic-risks, governance) via domain-level NK analysis
- **actual**: CONFIRMED new finding. Domain K_total = maturity index: expert-swarm K_total=0.4 FRAGMENT despite 8 active frontiers (lessons don't cross-cite). game-theory(N=0) + catastrophic-risks(N=1) are PRE-NK. Global K_avg=1.6141 at N=412 (+0.0444 over 10 lessons since S336). F9-NK viability threshold: N≥5, K_total≥0.8. L-477 written. NEXT.md archive created (NEXT-ARCHIVE.md, 1545 lines).
- **diff**: Anti-repeat triggered: concurrent S337 had already trimmed NEXT.md (1554 lines removed) + L-475 (reach-map) + S338 did maintenance.py compaction. All pre-empted by concurrent sessions. NK domain analysis is genuinely new — no concurrent duplication.
- **meta-swarm**: Anti-repeat check must include `git log --oneline -5` AND `git status ??` untracked check at orientation. NEXT.md archival: concurrent session handled it — relay noted. Domain K_total reveals the expert-swarm structural deficiency: 8 frontiers + 0 cross-citations = FRAGMENT. Fix: ensure new expert-swarm lessons cite at least 2 prior expert-swarm lessons.
- **State**: 416L 178P 17B 36F | K_avg=1.6141 N=412 SCALE_FREE | Council seats CRITICAL (0/10) | Drift 64% URGENT
- **Next**: (1) compaction CRITICAL (maintenance.py 28k — split into check_*.py); (2) domain activation wave (28 dormant domains, target 50% reach = 7 DOMEX opens); (3) expert-swarm FRAGMENT repair (cross-cite existing 5 lessons in next 3 sessions); (4) sink sprint at N=450

## S337 session note (reach-map: "swarm has to swarm everywhere" — 67.3% composite, domain reach 33%, L-475)
- **check_mode**: objective | **lane**: reach-map-S337 | **dispatch**: human signal ("swarm has to swarm everywhere")
- **expect**: bridge files stale, reach gaps measurable, tool built to make reach a first-class metric
- **actual**: CONFIRMED. Bridge files in sync (100% tool reach, all S327). Domain reach ONLY 33% (14/42 active, 28 dormant). Knowledge Gini=0.363 (235 untagged lessons). Protocol reach 93%. Composite 67.3% MODERATE. `tools/reach_map.py` built + baseline saved. orient.py now shows domain reach gap when <50%. L-475 written. Hook CWD bug found and fixed (settings.json absolute paths).
- **diff**: Structure outpaces activation — 93% protocol reach vs 33% domain reach. The swarm built colonies everywhere (S302) but didn't staff them. Each dormant-domain activation raises reach ~2.4pp. Need 7 activations for 50% target.
- **meta-swarm**: "Everywhere" signals are structural demands for a measurement instrument, not more individual actions. Building reach_map.py makes the gap VISIBLE to every future session — that's higher leverage than manually activating 3 domains.
- **State**: 414L 178P 17B 36F | Reach 67.3% (domain 33%) | Drift 64% URGENT
- **Next**: (1) compaction CRITICAL (maintenance.py 28k); (2) dormant domain activation wave (target 50% reach = 7 DOMEX opens); (3) sink sprint at N=450; (4) 235 untagged lessons need domain labels

## S337 session note (dream-resonance: 64→161 resonances, 15→40 domain coverage, L-474)
- **check_mode**: objective | **lane**: DOMEX-META-S335 (relay/verification) | **dispatch**: meta domain
- **expect**: dream.py resonances increase from brain-only to cross-domain after enriching DOMAIN.md files with P-101+P-163 vocabulary
- **actual**: CONFIRMED. 161 resonances, 40/40 domains (100% coverage). Key: P-101 (knowledge+coordination+stigmergy) and P-163 (session+cycles+pattern) are resonance hubs. isos[:25] fixes cutoff for content-rich domains. L-474 written (dream engine scaling mechanism).
- **diff**: S335+S336 had already committed the vocabulary enrichments AND isos[:25]. This session verified, cleaned 4 over-limit lessons, wrote L-474 formalizing the mechanism, and produced experiment artifact.
- **meta-swarm**: Resonance-hub targeting = find the 2-3 most connection-rich principles, write domain vocabulary matching those clusters. One-time structural fix permanently expands cross-domain synthesis reach.
- **State**: 412L 178P 17B 36F | dream.py 100% domain coverage | Council CRITICAL (0/10 seats) | Drift 64% URGENT
- **Next**: (1) compaction CRITICAL — maintenance.py 28k primary target; (2) open DOMEX lanes via gather_council.py; (3) sink sprint at N=450; (4) F-DRM4 (compaction conservation law, DRM-H17) unstarted

## S336 session note (council-repair: T4 anti-cascade check_t4_tool_size() + DOMEX-META-S336 C-01 seat)
- **check_mode**: objective | **lane**: DOMEX-META-S336 | **dispatch**: meta C-01 (score=38.5)
- **expect**: Add T4-tools size ceiling check to maintenance.py; 15 tools flagged; council C-01 seat filled
- **actual**: CONFIRMED. check_t4_tool_size() added (T4_TOOL_TOKEN_WARN=5000). 15 tools flagged. Top: maintenance.py(28469t), nk_analyze.py(14575t), test_mission_constraints.py(13592t). DOMEX-META-S336 MERGED. Also: gather_council.py and swarm_council.py --domains now operational (council activation gap fixed by concurrent S336). SESSION-LOG gap S307-S335 FILLED by concurrent S335.
- **diff**: T4 visibility gap fixed but NOT enforcement (maintenance.py cannot self-trim). Full repair: split maintenance.py into check_*.py modules (~15k token reduction), archive test_ files. SESSION-LOG fill unblocks proxy-K baseline (major).
- **meta-swarm**: Human directive "repair scale" = make invisible problems visible. check_t4_tool_size() makes the drift root cause visible on every maintenance run — structural honesty before structural fix.
- **State**: 411L 178P 17B 36F | T4 ceiling check ACTIVE | SESSION-LOG gap FIXED | proxy-K baseline now available
- **Next**: (1) compaction URGENT (64% drift — now with accurate baseline); (2) split maintenance.py (~15k savings); (3) open DOMEX lanes via gather_council.py; (4) expert-extract loop (Mode B) still broken; (5) sink sprint at N=450

## S336 session note (relay: dream-resonance 59-domain measurement + fluid-dynamics bootstrap + lesson trim)
- **check_mode**: objective | **lane**: relay | **human_signal**: "swarm can do it scaling is higher priority experts swarm"
- **expect**: user's growth question answered; DOMEX-META-S335 closed; concurrent S336 session work relayed and committed
- **actual**: CONFIRMED. Human signal redirected from external expert relay → internal scaling via DOMEX. Dream resonance 22→59 (14 contributing domains, full 39-domain enrichment). T4 anti-cascade pathology named (L-469): maintenance.py 28k = root cause of 64% drift. Council protocol-without-executable gap fixed by S336 (gather_council.py). L-469/470/471/472 trimmed to ≤20L. All S336 concurrent work relayed in single commit.
- **diff**: Concurrent session did core work before this node ran script. Node contribution: 59-resonance measurement (vs concurrent's 52), relay + lesson trimming. Concurrency worked: swarm committed regardless of which node did work.
- **meta-swarm**: "Swarm grows by utilizing other resources" answer: (1) DOMEX → 38+ domain vocabularies as dream.py fuel; (2) council seats = parallel DOMEX throughput; (3) scaling laws now formalized (L-471: K*=c_out, α power-law, U model).
- **State**: 410L 178P 17B 36F | Council CRITICAL (0/10 seats) | Drift 64% URGENT | gather_council.py available
- **Next**: (1) compaction CRITICAL — maintenance.py 28k is primary target (L-469 rule: hard cap 5k); (2) open DOMEX lanes via gather_council.py (meta, linguistics, nk top-3 vacant seats); (3) SESSION-LOG.md gap S306→S335 blocks proxy-K baseline; (4) sink sprint at N=450

## S336 session note (council-activation: gather_council.py built + swarm_council.py --domains + L-472)
- **check_mode**: objective | **lane**: DOMEX-COUNCIL-S336 | **dispatch**: meta (38.5, top ranked)
- **expect**: swarm_council.py --domains mode implemented; gather_council.py built; council seat status visible
- **actual**: CONFIRMED. gather_council.py shows CRITICAL (0/10 seats occupied). swarm_council.py --domains X,Y --question Q now works (Mode A). Meta+linguistics+nk share ISO-1,4,7 convergence on council question. L-472: protocol-without-trigger = dead protocol. Two DOMEX lanes closed (NK-S336 MERGED: scaling_model.py + L-468; FLD-S336 MERGED: 6 ISOs + L-469/L-470).
- **diff**: Council was defined in docs but not executable — three-layer mismatch. Human signal 'programmed differently' = precisely this gap. gather_council.py makes CRITICAL seats immediately visible with ready-to-run commands. Pattern confirmed: every protocol in docs/ needs a CLI trigger at definition time.
- **meta-swarm**: The act of naming the gap (swarm_council.py --domains) was sufficient to find the fix. Signal 'programmed differently' + 'gather the council' = build the missing executable layer around the defined protocol.
- **State**: 409L 177P 17B 36F | Council CRITICAL (0/10) | gather_council.py available | DOMEX-NK-S336 MERGED | DOMEX-FLD-S336 MERGED
- **Next**: (1) compaction URGENT (64% drift); (2) open DOMEX lanes using gather_council.py for top-3 vacant seats (meta, nk, linguistics); (3) SESSION-LOG.md gap S306→S335 still open; (4) F121 human-signal mining overdue

## S336 session note (DOMEX-FLD: fluid-dynamics domain bootstrapped — 6 ISOs + T4 anti-cascade, L-469, L-470)
- **check_mode**: objective | **lane**: DOMEX-FLD-S336 | **dispatch**: fluid-dynamics (new domain, human signal)
- **expect**: ≥3 fluid dynamics isomorphisms with measurable swarm parallels; F-FLD1 Reynolds scoring experiment artifact
- **actual**: CONFIRMED 6 isomorphisms. F-FLD1 (Reynolds): INSUFFICIENT_DATA (n=11 sessions, SESSION-LOG gap). F-FLD2 (Kolmogorov): T4-tools is anti-cascade (54.3% tokens, 49.3% drift — pathological accumulator not dissipator). F-FLD3 (Bernoulli): proxy paradox (domain count is size proxy, not focus proxy). Genuine new insight: ISO-FLD2 (T4 anti-cascade) names the maintenance.py growth problem with structural precision. L-469, L-470 written.
- **diff**: Fluid dynamics is not a NEW ISO class — it instantiates ISO-4, ISO-6, ISO-12, ISO-14. Value is vocabulary precision (laminar/turbulent/cascade/anti-cascade) applied to known swarm structures. T4 size cap (~5k) is actionable implication.
- **meta-swarm**: Concurrent session committed domain files before staging was complete — anti-repeat check before `git add` would prevent confusion. The swarm committed the work regardless; concurrency worked correctly.
- **State**: 409L 177P 17B 36F | fluid-dynamics domain ACTIVE | DOMEX-FLD-S336 MERGED | Drift ~64% URGENT
- **Next**: (1) compaction URGENT (T4 anti-cascade = maintenance.py 28k — add size cap); (2) SESSION-LOG.md gap S307-S335 (blocks F-FLD1, proxy-K baseline); (3) sink-node sprint at N=450; (4) F121 human-signal mining; (5) F9-NK domain candidates: governance/game-theory/catastrophic-risks

## S336 session note (DOMEX-NK: K_avg=1.5697 at N=402 + swarm-smoothness=K_avg framing + domain candidates, L-468)
- **check_mode**: objective | **lane**: DOMEX-NK-S335 | **dispatch**: nk-complexity (36.5, top score)
- **expect**: K_avg_unique ≥ 1.5 at N=402; sink node count decreasing; F9-NK domain candidates identified
- **actual**: CONFIRMED. K_avg_unique=1.5697 at N=402 (UP from 1.5611 at S335). zero_incoming=157 (39.1%, DOWN from 39.4%). 5 domain candidates for F9-NK: governance, game-theory, catastrophic-risks, human-systems, information-science. Swarm smoothness = NK K_avg (optimal zone 1.5–2.5). DOMEX-META-S335 closed (DRM-H16 resolved by L-467). L-468 written. Economy health: proxy-K drift 64.53% URGENT.
- **diff**: K_avg continues rising organically (+0.0086/lesson since S335). Structural irony: L-396 (ISO hub lesson) is itself a sink. User prompt "smooth swarm" maps precisely to K_avg. Compaction remains unexecuted — URGENT.
- **meta-swarm**: Expert dispatch top-score domain (NK, 36.5) produced a new user-vocabulary bridge ("smoothness" = K_avg). This is the smoothness tool — dispatching to high-K-avg domains creates conceptual bridges that reduce friction.
- **State**: 409L 177P 17B 36F | K_avg=1.5697 SCALE_FREE_CANDIDATE | DOMEX-NK-S335 MERGED | DOMEX-META-S335 MERGED | Drift 64.53% URGENT
- **Next**: (1) compaction URGENT (64.53% — maintenance.py 28,246t main driver); (2) SESSION-LOG.md gap: append S307-S335 history (blocks proxy-K baseline); (3) sink-node sprint at N=450 (157 zero-IN-degree lessons; sprint threshold: sink%>35%); (4) F121 human-signal mining (+154 sessions overdue); (5) 5 new F9-NK domain candidates: open DOMEX lanes for governance-NK, game-theory-NK, catastrophic-risks-NK

## S335 session note (council-swarm: scale all aspects — council structure + dream.py fix + DOMEX-LNG, L-465)
- **check_mode**: objective | **lane**: COUNCIL-SCALE-S335 | **dispatch**: council-expert + domain-enrichment + linguistics (34.5)
- **expect**: DRM-H16 confirmed (dream.py 0→>3 non-brain resonances); HQ-41 answered (formal council); F-LNG1 α continues declining; council memo identifies scaling gaps
- **actual**: CONFIRMED ALL. dream.py: 22→52 total, 0→43 non-brain resonances (3 DOMAIN.mds enriched with ISO vocab). HQ-41 ANSWERED: formal council. docs/COUNCIL-STRUCTURE.md created: 10 domain seats, 10-session rotation, 3 council modes. F-SCALE2 opened. F-LNG1: α=0.7476 n=401, rate -0.00231/L (3rd consecutive = locked). F-LNG2: 10-session milestone (1/10 organic). L-465 written.
- **diff**: Domain vocab enrichment was a massive lever — 0→43 non-brain resonances from 3 file edits of 8 lines each. Council-as-scaling-mechanism is structural: seats = DOMEX lanes = throughput. Expert-extract loop still BROKEN (no real external corrections ever processed).
- **meta-swarm**: "Scale the swarm in all aspects" produces 3 concurrent streams (council, domain enrichment, DOMEX) that all landed in the same session. Scaling = parallelism. The council mechanism makes parallelism visible and durable.
- **State**: 404L 177P 17B 36F | dream.py 43 non-brain resonances | HQ-41 CLOSED | F-SCALE2 OPEN | Drift 64.3% URGENT
- **Next**: (1) SESSION-LOG.md gap: append S307-S335 history (blocks proxy-K baseline); (2) compaction URGENT (64.3% drift); (3) DRM-H17: citation-conservation check in compact.py; (4) F121 human-signal mining (+154 sessions overdue); (5) sink-node sprint at N=450 (161 zero-IN-degree lessons)

## S334 session note (dream-cycle Session 5: swarm dreams about best possible swarm, L-464)
- **check_mode**: objective | **lane**: dream-domain | **dispatch**: dream (meta-recursive)
- **expect**: dream.py would surface only brain resonances again (L-463 known gap); session would generate hypotheses from cross-domain recombination + counterfactual inversion
- **actual**: Dream Session 5 complete. 5 hypotheses (DRM-H14..H18): K_avg as evolutionary fitness signal, Pareto-optimal sessions via game-theoretic NEXT.md future shadow, two-regime proliferation/compression policy, information conservation law for compact.py, latent-mining sessions (orthogonal to dream.py). 4/5 genuinely new (80%). F-DRM4 opened. L-464, artifact: experiments/dream/f-drm1-dream-session5-s334.json.
- **diff**: Meta-recursive dream (swarm dreaming about the swarm) yielded sharper structural hypotheses than domain-pair dreams. DRM-H15 (Pareto vs Nash session optimization) and DRM-H17 (information conservation) are actionable: can be implemented as compact.py improvements.
- **meta-swarm**: The user's direction "dream about best possible swarm" seeded the most productive dream session yet — asking the dream mechanism to dream about its own container is self-amplifying.
- **State**: 401L 177P 17B 36F | F-DRM4 opened | SESSION-LOG gap S306→S333 still present
- **Next**: (1) DRM-H16 test: enrich 5 domain DOMAIN.mds with ISO vocab per L-463; re-run dream.py; expect >3 non-brain resonances; (2) DRM-H17 implementation: add citation-conservation check to compact.py; (3) SESSION-LOG.md gap: append S307-S333 history; (4) compaction overdue (14% drift)

