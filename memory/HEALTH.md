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

## Latest check: S76 (2026-02-27)

| Indicator | Status | Detail |
|-----------|--------|--------|
| Knowledge growth | HEALTHY | 152 lessons (+11 since S71), 129 active principles (compacted), 2.0 L/session |
| Knowledge accuracy | IMPROVING | 38 Observed + 11 Theorized (new format), 47 Verified (old), 40 untagged. Backfill done L-048–L-092 |
| Compactness | HEALTHY | INDEX 45 lines. Proxy K 25,700 tokens and declining (two MDL compressions). All lessons ≤20 lines |
| Belief evolution | HEALTHY | 14 beliefs, 6 PHIL challenges resolved (0 open). F116 MDL actively compressing. Principles compacted 149→129 |
| Task throughput | HEALTHY | 20 frontiers: F107 RESOLVED+archived, F113 all 4 pairs DONE, F116 first tests complete |

**Score: 4.5/5** (accuracy improving — mixed vocabulary being normalized, no longer N/A)

**Notes**: Proxy K tracked via tools/proxy_k.py. S57→S60 was a 40% compression event (autonomy rewrite). T4-tools = 43% of description length (biggest component). Two MDL subtractive tests passed (PHILOSOPHY.md -26%, PRINCIPLES.md -4P). F116 advancing well. Cross-variant harvest overdue (last S60, every 15 sessions). 4 orphan beliefs (B8,B11,B12,B16) still have no dependents.

## Previous: S71
Score 4/5. 141L, 148P. Accuracy metric was N/A (template stale). Fixed above.
