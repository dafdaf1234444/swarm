# System Health Check v0.1

Run periodically (every ~5 sessions) to assess whether the swarm is improving.

## Quick metrics (run via git/bash)

### 1. Knowledge growth
```bash
# Lessons count
ls memory/lessons/L-*.md | wc -l

# Frontier questions resolved vs open
grep -c '^\- \*\*F' tasks/FRONTIER.md
grep -c '|' tasks/FRONTIER.md  # resolved table rows (minus header)
```
**Healthy**: Lessons grow steadily. Resolved frontier questions increase.
**Unhealthy**: Many sessions but few lessons. Frontier only grows, never resolves.

### 2. Knowledge accuracy
```bash
# Confidence ratio
grep -c 'Confidence: Verified' memory/lessons/L-*.md
grep -c 'Confidence: Assumed' memory/lessons/L-*.md
```
**Healthy**: Verified ratio increases over time.
**Unhealthy**: Everything stays Assumed forever.

### 3. Compactness
```bash
# Lesson length (should be ≤20 lines each)
wc -l memory/lessons/L-*.md

# INDEX.md length (should stay navigable)
wc -l memory/INDEX.md
```
**Healthy**: Lessons stay ≤20 lines. INDEX stays under ~50 lines.
**Unhealthy**: Lessons bloat. INDEX becomes a wall of text.

### 4. Belief evolution
```bash
# Beliefs updated vs original count
wc -l beliefs/DEPS.md
git log --oneline beliefs/DEPS.md | wc -l
```
**Healthy**: DEPS.md gets edited, not just appended. Beliefs are challenged.
**Unhealthy**: DEPS.md never changes after genesis.

### 5. Task throughput
```bash
# Done vs total tasks
grep -rl 'Status: DONE' tasks/ | wc -l
ls tasks/TASK-*.md | wc -l
```
**Healthy**: Most tasks reach DONE. New tasks emerge from completed work.
**Unhealthy**: Tasks pile up. Many IN PROGRESS, few DONE.

## Overall health signal
Count how many of the 5 indicators are "healthy."
- 4-5: System is compounding well
- 3: Adequate but watch the weak areas
- 1-2: Something is structurally wrong — create a task to diagnose
- 0: Stop and rethink the approach

---

## Latest check: S162 (2026-02-27)

| Indicator | Status | Detail |
|-----------|--------|--------|
| Knowledge growth | HEALTHY | 207 lessons, 149 principles, 14 beliefs, 14 active frontiers; core state counts remain stable. |
| Knowledge accuracy | HEALTHY | `validate_beliefs.py --quick` remains PASS (14 beliefs, 0 errors, warnings-only). |
| Compactness | WATCH | Proxy-K drift remains NOTICE-level in this dirty tree; capture a clean snapshot (`python3 tools/proxy_k.py --save`) when stable. |
| Belief evolution | HEALTHY | Mission-constraint guardrails (F119) remain wired, with no challenge debt surfaced by maintenance. |
| Task throughput | HEALTHY | Runtime/inventory/quick-check pass completed in this session with Beliefs PASS and no DUE/PERIODIC blockers. |

**Score: 4.5/5** (compactness remains WATCH due to dirty-tree measurement volatility, not structural regression)

**Notes**: This refresh keeps health cadence current while preserving startup reliability across wrapper-first runtime paths.

## Latest check: S160 (2026-02-27)

| Indicator | Status | Detail |
|-----------|--------|--------|
| Knowledge growth | HEALTHY | 207 lessons, 149 principles, 14 beliefs, 14 active frontiers; no regression in core state counts. |
| Knowledge accuracy | HEALTHY | `validate_beliefs.py --quick` remains PASS (14 beliefs, 0 errors, warnings-only). |
| Compactness | WATCH | Proxy-K drift stays NOTICE-level in a dirty tree; keep clean-snapshot follow-through (`python3 tools/proxy_k.py --save`) when stable. |
| Belief evolution | HEALTHY | Mission-constraint guardrails (F119) remain active; no open challenge debt surfaced by maintenance. |
| Task throughput | HEALTHY | Runtime verification and PowerShell wrapper validation completed in S160 with Beliefs PASS + NOTICE-only maintenance. |

**Score: 4.5/5** (compactness remains WATCH due to dirty-tree volatility, not structural regression)

**Notes**: This pass confirms cross-shell operability (`bash` + PowerShell wrappers) and keeps periodic maintenance cadence aligned without new DUE blockers.

## Latest check: S155 (2026-02-27)

| Indicator | Status | Detail |
|-----------|--------|--------|
| Knowledge growth | HEALTHY | 207 lessons, 149 principles, 14 beliefs, 14 active frontiers; no regressions in core counts. |
| Knowledge accuracy | HEALTHY | `validate_beliefs.py --quick` PASS: 14 beliefs (12 observed, 2 theorized), 0 errors (warnings-only). |
| Compactness | WATCH | Proxy K remains noisy on this dirty tree; baseline floor remains stable but action signal is still to save a clean snapshot (`python3 tools/proxy_k.py --save`). |
| Belief evolution | HEALTHY | No open challenge debt surfaced by maintenance; F119 mission-constraint guardrails remain wired and active. |
| Task throughput | HEALTHY | Paper re-swarm cadence marker and health-check marker were both refreshed to current session, clearing periodic debt in maintenance. |

**Score: 4.5/5** (compactness stays WATCH due to dirty-tree measurement volatility, not structural regression)

**Notes**: This pass was cadence hygiene and living-paper continuity: `docs/PAPER.md` session-scale anchor refreshed to S155, and periodic markers synced to avoid stale DUE/PERIODIC drift.

## Latest check: S154 (2026-02-27)

| Indicator | Status | Detail |
|-----------|--------|--------|
| Knowledge growth | HEALTHY | 207 lessons, 149 principles, 14 beliefs, 14 active frontiers; no regression in core counts. |
| Knowledge accuracy | HEALTHY | `validate_beliefs.py --quick` PASS: 14 beliefs (12 observed, 2 theorized), 0 errors (warnings-only). |
| Compactness | WATCH | Proxy K in this dirty tree is high/volatile (latest run: 34,700 tokens); baseline comparison remains noisy until a clean snapshot is saved (`python3 tools/proxy_k.py --save`). |
| Belief evolution | HEALTHY | No open challenge debt surfaced by maintenance; mission-constraint guard checks were added in S153 to keep new invariants wired. |
| Task throughput | HEALTHY | Hook drift blocker was cleared by installing `pre-commit` + `commit-msg` hooks; this health-check refresh clears the overdue periodic marker. |

**Score: 4.5/5** (compactness remains WATCH due to dirty-tree measurement volatility, not a new structural break)

**Notes**: Runtime remains WSL-first (`python3`) in this host context; maintenance/check are back to NOTICE-only after hook re-install.

## Latest check: S149 (2026-02-27)

| Indicator | Status | Detail |
|-----------|--------|--------|
| Knowledge growth | HEALTHY | 207 lessons, 149 principles, 14 beliefs, 13 active frontiers; no regressions in core counts. |
| Knowledge accuracy | HEALTHY | `validate_beliefs.py --quick` PASS: 14 beliefs (12 observed, 2 theorized), 0 errors (warnings-only). |
| Compactness | WATCH | Dirty-tree proxy-K still fluctuates during concurrent edits; keep watch status until a clean snapshot is saved (`python tools/proxy_k.py --save`). |
| Belief evolution | HEALTHY | No open challenge debt surfaced by maintenance; theorized-principle backlog remains cleared (0 THEORIZED). |
| Task throughput | HEALTHY | Recent periodic debt reduced (principles-dedup + setup-hygiene executed); this health-check refresh closes the remaining periodic item. |

**Score: 4.5/5** (compactness remains WATCH due to dirty-tree measurement volatility, not structural degradation)

**Notes**: This pass mainly stabilized periodic cadence and state hygiene under concurrent edits while preserving NOTICE-only maintenance outside operational dirty-tree noise.

## Latest check: S144 (2026-02-27)

| Indicator | Status | Detail |
|-----------|--------|--------|
| Knowledge growth | HEALTHY | 206 tracked lessons (+1 draft: L-207), 150 principles, 14 beliefs, 13 active frontiers; no regression in core counts. |
| Knowledge accuracy | HEALTHY | `validate_beliefs.py --quick` PASS: 14 beliefs (12 observed, 2 theorized), 0 errors (warnings-only). |
| Compactness | WATCH | Live Proxy K in this dirty tree is 27,532 tokens (`python tools/proxy_k.py`); drift remains measurement-sensitive until a clean snapshot is saved. |
| Belief evolution | HEALTHY | No open challenge debt surfaced by maintenance; P-155 advanced to PARTIALLY OBSERVED in S144 (L-207). |
| Task throughput | HEALTHY | Overdue periodic debt for health-check and cross-variant-harvest was cleared in this pass. |

**Score: 4.5/5** (compactness remains WATCH due to dirty-tree measurement volatility, not hard compaction debt)

**Notes**: Cross-variant periodic review found no active bulletin queue and no new integration-ready child outputs this cycle.

## Latest check: S138 (2026-02-27)

| Indicator | Status | Detail |
|-----------|--------|--------|
| Knowledge growth | HEALTHY | 206 lessons, 150 principles, 14 beliefs, 13 active frontiers; no regressions in core state counts. |
| Knowledge accuracy | HEALTHY | `validate_beliefs.py --quick` PASS: 14 beliefs (12 observed, 2 theorized), 0 errors (warnings-only). |
| Compactness | WATCH | Proxy K in current dirty tree fluctuates near 26k tokens (runtime-dependent). Drift interpretation remains sensitive to clean-snapshot availability and host/runtime differences. |
| Belief evolution | HEALTHY | No open challenge debt surfaced by maintenance; theorized backlog remains focused (P-128, P-155). |
| Task throughput | HEALTHY | Periodic health-check debt cleared in this pass; maintenance/check remain free of DUE/URGENT blockers. |

**Score: 4.5/5** (compactness watch due to measurement volatility, not active compaction failure)

**Notes**: This refresh is primarily state-hygiene: keep periodic markers and session headers aligned with live log state so maintenance signals are actionable rather than stale.

## Latest check: S132 (2026-02-27)

| Indicator | Status | Detail |
|-----------|--------|--------|
| Knowledge growth | HEALTHY | 204 tracked lessons (+2 draft), 150P, 14B, 13 active frontiers. |
| Knowledge accuracy | HEALTHY | `validate_beliefs.py --quick` PASS: 14 beliefs (12 observed, 2 theorized), 0 errors, warnings-only. |
| Compactness | WATCH | Proxy K live = 26,103; floor comparability is unavailable until a clean schema-matching snapshot is saved (`python tools/proxy_k.py --save`). |
| Belief evolution | HEALTHY | 0 open challenges and no DUE/URGENT integrity alerts. |
| Task throughput | HEALTHY | 11/12 tasks DONE (91.7%); maintenance remains periodic/notice-level. |

**Score: 4.5/5** (compactness watch reflects measurement hygiene gap, not active compaction debt)

**Notes**: Priority is measurement stabilization: capture a clean proxy-K snapshot to restore reliable floor-based drift tracking.

## Latest check: S131 (2026-02-27)

| Indicator | Status | Detail |
|-----------|--------|--------|
| Knowledge growth | HEALTHY | 204 tracked lessons (+2 draft), 150P, 14B, 13 active frontiers. No structural regressions in core counts. |
| Knowledge accuracy | HEALTHY | `validate_beliefs.py --quick` PASS: 14 beliefs (12 observed, 2 theorized), 0 errors, warnings-only. |
| Compactness | WATCH | Proxy-K baseline check is schema-gated in this dirty tree (`Proxy K schema baseline unavailable` notice). Keep as watch until a clean schema-matching snapshot is saved. |
| Belief evolution | HEALTHY | Belief churn remains active (27 commits touching `beliefs/DEPS.md`); no DUE/URGENT belief integrity issues surfaced. |
| Task throughput | HEALTHY | 11/12 tasks DONE (91%). Periodic health-check debt cleared by this run (marker advanced to S131). |

**Score: 4.5/5** (compactness stays WATCH due to baseline/schema measurement gap, not hard drift debt)

**Notes**: This cycle focused on maintenance cadence and handoff hygiene: health-check periodic refreshed, validator remains green, and swarm operation is NOTICE-only outside dirty-tree operational noise.

## Latest check: S126 (2026-02-27)

| Indicator | Status | Detail |
|-----------|--------|--------|
| Knowledge growth | HEALTHY | 206L, 150P, 14B, 13 active frontiers. Counts remain stable after S124/S125 periodic cleanup passes. |
| Knowledge accuracy | HEALTHY | `validate_beliefs.py --quick` PASS: 14 beliefs (12 observed, 2 theorized), 0 errors (warnings-only). |
| Compactness | WATCH | Proxy K live 28,049 vs S115 floor 25,772 (+8.8%) on dirty tree; maintenance classifies this as NOTICE-level live drift (save when stable), not DUE/URGENT compression debt. |
| Belief evolution | HEALTHY | No open challenges surfaced by maintenance. Remaining theorized principles unchanged: P-128 and P-155. |
| Task throughput | HEALTHY | Periodic health-check debt cleared (marker advanced). Maintenance now reports NOTICE-only operational noise. |

**Score: 4.5/5** (compactness watch due to dirty-tree live drift; no hard due items after periodic refresh)

**Notes**: This cycle was maintenance and state-hygiene focused. `INDEX.md` currently counts untracked lesson drafts (`L-205/L-206`), so maintenance reports tracked-vs-working-tree lesson-count drift until those drafts are committed or counts are normalized.

## Latest check: S118 (2026-02-27)

| Indicator | Status | Detail |
|-----------|--------|--------|
| Knowledge growth | HEALTHY | 204L, 151P, 14B, 13 active frontiers. No count regressions; F115 drift coverage expanded with frontier-claim sentinel in maintenance. |
| Knowledge accuracy | HEALTHY | `validate_beliefs.py --quick` PASS: 14 beliefs (12 observed, 2 theorized), 0 errors (warnings-only). |
| Compactness | HEALTHY | Proxy K 25,772 vs current floor 25,772 (0.0% drift), below P-163 re-compress trigger (6%). INDEX remains 46 lines. |
| Belief evolution | HEALTHY | No open challenges surfaced by maintenance. Remaining theorized principles unchanged: P-128 and P-155. |
| Task throughput | HEALTHY | F115 follow-through advanced: paper drift checks now include explicit frontier-claim consistency. Maintenance shows PERIODIC+NOTICE only (no DUE/URGENT). |

**Score: 5/5** (all indicators healthy; periodic health check refreshed on cadence)

**Notes**: This cycle focused on maintenance integrity rather than new domain expansion: F115 gained low-noise contradiction detection, and the periodic health-check marker was advanced.

## Latest check: S113 (2026-02-27)

| Indicator | Status | Detail |
|-----------|--------|--------|
| Knowledge growth | HEALTHY | 204L (+6 since S106: L-199..L-204), 151P, 13 active frontiers after F92 resolution (S113). |
| Knowledge accuracy | HEALTHY | `validate_beliefs.py --quick` PASS: 14 beliefs (12 observed, 2 theorized), 0 errors (warnings only). |
| Compactness | HEALTHY | Proxy K 24,620 vs floor 23,383 (+5.3%), below P-163 re-compress trigger (6%). INDEX 46 lines; lessons remain compact. |
| Belief evolution | HEALTHY | Theorized principle backlog reduced to 2 (P-128, P-155); P-141 is now PARTIALLY OBSERVED and handoff state is synced. |
| Task throughput | HEALTHY | F92 RESOLVED S113 via workload-topology + coordination-primitive benchmarks; active handoff shifted to F115 accuracy pass and F111 deploy decision. |

**Score: 5/5** (all indicators healthy; drift remains below compression threshold)

**Notes**: This cycle converted F92 from open question to conditional rule and reduced frontier load (14→13). Validation stays green (`check.sh --quick` PASS). Next leverage is synthesis quality (paper accuracy pass) and theorized-principle promotion.

## Latest check: S106 (2026-02-27)

| Indicator | Status | Detail |
|-----------|--------|--------|
| Knowledge growth | HEALTHY | 198L (+4 since S99: L-195 to L-198), 151P, 15 active frontiers. F118 live non-Claude execution completed in S104; closeout criteria remains. |
| Knowledge accuracy | HEALTHY | `validate_beliefs.py --quick` PASS: 14 beliefs (12 observed, 2 theorized), 0 errors, warnings-only. PHIL-4/PHIL-8 challenge loop resolved (S102-S103). |
| Compactness | HEALTHY | Proxy K 24,183 (+3.4% vs floor 23,383), below P-163 re-compress trigger (6%). INDEX 46 lines; maintenance reports no lesson-length overflow. |
| Belief evolution | HEALTHY | Belief set stable at 14 with no open challenges. Recent refinements integrated; remaining targeted promotions noted in NEXT (P-128/P-141/P-155). |
| Task throughput | HEALTHY | No DUE/URGENT items. Periodic maintenance executed on cadence; primary active handoff is F118 closeout and F111 deploy decision. |

**Score: 5/5** (all indicators healthy; compactness remains below threshold)

**Notes**: This cycle was maintenance-dominant (health check + validation). Runtime/tool consistency remains stable across Codex and check.sh paths. Next high-leverage work is decision/closure work (F118 archive criteria, F111 deploy path) rather than structural repair.

## Latest check: S99 (2026-02-27)

| Indicator | Status | Detail |
|-----------|--------|--------|
| Knowledge growth | HEALTHY | 194L (+3 since S97: L-192 substrate diversity, L-193 compact.py, L-194). 142P. 15 active frontiers. F76 RESOLVED (specialist +35%), F105 RESOLVED (compact.py). 1.5 L/session this cluster. |
| Knowledge accuracy | HEALTHY | P-059 updated (F76 specialization depth), P-089 refined (substrate caveat on convergence). S99 MDL compression: 6 principles tightened. Validator PASS: 14 beliefs, 12 observed, 2 theorized. 0 open challenges. |
| Compactness | HEALTHY | Proxy K: 24,017 (+2.7% from floor 23,383). S99 MDL compression resolved the 6.2% DUE from S97. compact.py created (F105). All 194 lessons ≤20 lines. INDEX 46 lines. |
| Belief evolution | HEALTHY | 14 beliefs stable. 3 THEORIZED (P-128, P-141, P-155). 3 PARTIALLY OBSERVED (P-156/P-157/P-158). P-089 substrate caveat = new epistemic rigor on convergence. |
| Task throughput | HEALTHY | F76 RESOLVED, F105 RESOLVED, F101 closed. Active: F118 test (non-Claude tool), THEORIZED promotions, F111 deploy (human). Periodic health check on cadence. |

**Score: 5/5** (compactness improved from 4.5/5 → 5/5 after S99 MDL compression)

**Notes**: S97–S99 resolved compactness issue from S97. F105 closed (compact.py = diagnosis tool, session = mutation). F76 confirmed specialist hierarchy. Substrate caveat (L-192) adds epistemic rigor to convergence validation. Proxy K growth-compression cycle healthy: 4th cycle completed (S77, S83, S86, S99). Next: F118 live test with non-Claude tool; P-128/P-141 Go EH cross-project data.

## Previous: S97 (2026-02-27)

| Indicator | Status | Detail |
|-----------|--------|--------|
| Knowledge growth | HEALTHY | 191L (+7 since S91 in ~6 sessions: L-185→L-191), 142P (+5: P-169–P-173). 1.2 L/session. 3 frontiers resolved: F71 (spawn quality n=10), F117 (2 libs shipped), F76 (hierarchical spawning +35%). 15 active frontiers. Human signal F118 (multi-LLM) substantially done. |
| Knowledge accuracy | HEALTHY | P-132 OBSERVED, P-119 OBSERVED (n=10), P-158 PARTIALLY OBSERVED. P-169–P-173 all OBSERVED (from child experiments, R6 harvest). Validator PASS: 14 beliefs, 12 observed, 2 theorized. 0 open challenges. |
| Compactness | WATCH | Proxy K: 24,826 (+6.2% from floor 23,383). S96 compressed (+5.7% at measurement) but state additions pushed it back. T3+1003t is genuine R6 harvest growth. All 191 lessons ≤20 lines. INDEX 45 lines. Compression agent running. |
| Belief evolution | HEALTHY | 14 beliefs stable. 3 THEORIZED remaining: P-128/P-141 (Go EH), P-155 (competitive). 3 PARTIALLY OBSERVED (P-156/P-157/P-158). R6 harvest refined P-091/P-156/P-160. 0 open challenges. PHIL claims stable. |
| Task throughput | HEALTHY | F76 RESOLVED (hierarchical spawning), F71 RESOLVED, F117 DONE (2 libs), F115 paper re-swarmed. F118 bridge files + check.sh done — test pending. F111 pending human deploy decision. Health check cadence: ~6 sessions maintained. |

**Score: 4.5/5** (compactness: proxy K at 6.2% — compression DUE, agent running)

## Latest check: S91 (2026-02-27)

| Indicator | Status | Detail |
|-----------|--------|--------|
| Knowledge growth | HEALTHY | 184L (+9 since S83 in ~8 sessions: L-175 to L-184), 137P. 1.1 L/session net (many concurrent sessions this cluster). F-NK4 RESOLVED. F118 opened (multi-LLM). 17 active frontiers. |
| Knowledge accuracy | HEALTHY | P-132 OBSERVED (was THEORIZED S76), P-157 PARTIALLY OBSERVED, P-156 PARTIALLY OBSERVED, P-168 added. Validator PASS: 12 observed beliefs, 2 theorized. Zero open challenges. |
| Compactness | HEALTHY | Proxy K: 26,034→23,383 (−9.8%). New floor established. T3-knowledge 4,350t (was 5,978t at S83). HUMAN.md −71%, FRONTIER.md condensed. Well below 6% trigger. |
| Belief evolution | HEALTHY | 14 beliefs stable. 3 THEORIZED principles converted: P-132 OBSERVED, P-156/P-157 PARTIALLY OBSERVED. CHALLENGES.md: 0 open. F118 signal suggests new belief area (multi-LLM) may emerge. |
| Task throughput | HEALTHY | MDL compression DONE (highest priority). F111 builder DONE, deploy pending human review. F117 10-tool audit DONE (P-168 added). 4 THEORIZED principles remain. |

**Score: 5/5** (all indicators healthy; compactness resolved from S83's 4.5/5)

**Notes**: Session S83-S91 cluster was highly productive: MDL compression (-9.8%), F-NK4 resolved, P-132 validated cross-project, P-157/P-156 tested, F118 opened by human signal. Cross-variant harvest overdue (last S76, 15-session cadence) but no active children to harvest. Paper re-swarm due at S93. THEORIZED principles (P-128, P-141, P-155, P-158) require Go EH cross-project data and swarm-internal experiments.

## Previous: S83

| Indicator | Status | Detail |
|-----------|--------|--------|
| Knowledge growth | HEALTHY | 175L (+23 since S76, 7 sessions), 141P, 3.3 L/session (up from 2.0). 5 frontiers archived since S76: F84, F91, F109, F113, F116. 16 active frontiers, 96 archived. |
| Knowledge accuracy | HEALTHY | 106 Observed/Verified, 30 Assumed/Theorized, 40 untagged (176 total). Observed ratio 78% (tagged). Validator: 100/100 swarmability, 0 entropy. 12 observed beliefs, 2 theorized (14% theorized, below 60% threshold). |
| Compactness | WATCH | INDEX 45 lines. Proxy K live 26,034 tokens (+6.2% from floor 24,504 at S77) — **crossed 6% P-163 threshold**. Last logged S80: 25,010. T4-tools 38.9% (10,117t). T3-knowledge 22.6% (5,875t, +1,400 since floor). All 175 lessons ≤20 lines. |
| Belief evolution | HEALTHY | 14 beliefs (12 observed, 2 theorized). DEPS.md stable since S55 — belief set mature, not stagnant. PHIL-5/11/13 challenged and refined (S81b). CHALLENGES.md: 1 historical challenge, 0 open. Cascade validator (F110-A2) wired in. |
| Task throughput | HEALTHY | 16 active frontiers (down from 20 at S76). 5 resolved since S76. F111 builder fix phase tested S81+ (67% executable, 13/13 tests pass). F117 opened S83 (self-producing libs — nk-analyze v0.2.0 shipped). 11/12 TASK files at DONE. |

**Score: 4.5/5** (compactness: proxy K re-compression DUE per P-163 — 6% threshold crossed)

**Notes**: Growth-compression cycle working as designed (P-163: ~170t/session, 6% threshold). Drift from floor = 6.2% — re-compress now, target T3-knowledge (+1,400t) and any new cross-tier redundancy. T4-tools stable post-S77 compression. Builder capability confirmed (F111). First self-produced library shipped (nk-analyze v0.2.0, F117). 4 orphan beliefs (B8, B11, B12, B16) remain structurally isolated — not urgent at N=14. 37 principles with 0 citations flagged by maintenance.py — compression candidates for next T3/T4 pass.

## Previous: S76
Score 4.5/5. 152L, 129P. Proxy K 25,700 declining. F116 compressing. Accuracy improving (mixed vocabulary normalizing).

## Previous: S71
Score 4/5. 141L, 148P. Accuracy metric was N/A (template stale).
