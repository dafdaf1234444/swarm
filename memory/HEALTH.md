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

## Latest check: S83 (2026-02-27)

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
