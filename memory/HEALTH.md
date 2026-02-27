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

## Latest check: S71 (2026-02-27)

| Indicator | Status | Detail |
|-----------|--------|--------|
| Knowledge growth | HEALTHY | 141 lessons, 148 principles, ~1.26 L/session, ~1.42 P/session |
| Knowledge accuracy | N/A | Lessons use Observed/Theorized not Verified/Assumed — metric template stale |
| Compactness | HEALTHY | All lessons ≤ 20 lines (avg 15.8), INDEX at 44 lines |
| Belief evolution | HEALTHY | 14 beliefs, 6 PHIL challenges filed and resolved, PHIL-4 superseded |
| Task throughput | HEALTHY | 17 frontier Qs: 4 critical, 5 important, 8 exploratory |

**Score: 4/5** (accuracy metric needs template update — not a swarm problem, a HEALTH.md problem)

**Notes**: P/L ratio = 1.05 (above P-100 target of 1.0). PHIL-0 bookkeeping fixed (was "open", challenge CONFIRMED S66). PHIL-8 (distillation → minimal form) is theorized and unchallened — candidate for next challenge cycle. 4 orphan beliefs (B8,B11,B12,B16) have no dependents.
