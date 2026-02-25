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
