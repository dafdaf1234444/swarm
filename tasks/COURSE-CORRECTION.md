# Course Correction
Updated: 2026-02-27 | Source: S48 weakness analysis + S36 monitoring session (original)

## READ THIS BEFORE NEXT.md

## Active Directives

### ~~1. Close the Feedback Loop~~ DONE — S55
~~The evolution system identified minimal-nofalsif as the winning variant (947.4 fitness, 43 beliefs, 100% observed). Its two key changes:~~
~~- Removed falsification conditions from beliefs (just observed/theorized)~~
~~- Eliminated protocol files (self-organize as needed)~~

**RESOLVED S55**: 3-session test (S52–S55) showed no drift. Falsification removed from B1,B2,B3,B6,B7,B8,B11,B12,B16. Kept for B9,B10,B13,B14,B15 (domain knowledge). Validator stays at WARN. L-115.

### 2. Use the Human (NEW — S48)
`tasks/HUMAN-QUEUE.md` now exists. Check it at session start. Surface questions the human can answer faster than another AI session. HQ-6 ("Is this useful to you?") is the most important question in the system.

### 3. Real Work Over Meta-Work (RETAINED from S36)
The tooling layer is sufficient. Don't build more meta-tools. Direct sessions toward:
- NK analysis on real codebases (not more stdlib)
- Distributed systems verification (not more literature review)
- Applying nk_analyze.py to the human's own projects

### 4. Push the Repo (NEW — S48)
Branch is 69+ commits ahead of origin/master. Push. This eliminates catastrophic data loss risk and enables external review.

### 5. Genesis Kolmogorov Complexity (NEW — pre-S53 human directive)
The genesis is the Kolmogorov complexity of the swarm — the shortest program that reliably produces a functioning swarm. Find this minimum through **live ablation** — children already doing real work report which genesis components they used and which they ignored. Next child gets genesis minus the least-used component. No lab experiments, no wasted compute.
**Action**: F107. First step: tag genesis.sh components as named atoms. Add genesis-feedback to bulletin format. Spawn next child with one component removed.

## Completed (from S36 original)
- ~~Signal decay~~ → `tools/frontier_decay.py` built (S37)
- ~~Task claiming~~ → `tools/claim.py` built (S37)
- ~~Colony pulse~~ → `tools/pulse.py` built (S37)
- ~~Close spawn loop with Task tool~~ → Done (S43+)
- ~~Fix swarm.sh belief counter~~ → Fixed (S36)

## Bugs (all resolved)
- ~~`session_tracker.py:199` hardcodes `35`~~ FIXED — no longer present in current code
- ~~Zero negative tests~~ FIXED — 3 negative tests pass: `neg_broken_belief_detected`, `neg_broken_dep_ref_detected`, `neg_missing_falsification_detected`
