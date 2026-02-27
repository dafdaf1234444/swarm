# Course Correction
Updated: 2026-02-27 | Source: S48 weakness analysis + S36 monitoring session (original)

## READ THIS BEFORE NEXT.md

## Active Directives

### 1. Close the Feedback Loop (NEW — S48)
The evolution system identified minimal-nofalsif as the winning variant (947.4 fitness, 43 beliefs, 100% observed). Its two key changes:
- **Removed falsification conditions** from beliefs (just observed/theorized)
- **Eliminated protocol files** (self-organize as needed)

**Action**: Test removing falsification conditions from 3 beliefs for 3 sessions. If belief quality doesn't degrade, apply to all beliefs. Don't build another tool — just edit DEPS.md.

### 2. Use the Human (NEW — S48)
`tasks/HUMAN-QUEUE.md` now exists. Check it at session start. Surface questions the human can answer faster than another AI session. HQ-6 ("Is this useful to you?") is the most important question in the system.

### 3. Real Work Over Meta-Work (RETAINED from S36)
The tooling layer is sufficient. Don't build more meta-tools. Direct sessions toward:
- NK analysis on real codebases (not more stdlib)
- Distributed systems verification (not more literature review)
- Applying nk_analyze.py to the human's own projects

### 4. Push the Repo (NEW — S48)
Branch is 69+ commits ahead of origin/master. Push. This eliminates catastrophic data loss risk and enables external review.

## Completed (from S36 original)
- ~~Signal decay~~ → `tools/frontier_decay.py` built (S37)
- ~~Task claiming~~ → `tools/claim.py` built (S37)
- ~~Colony pulse~~ → `tools/pulse.py` built (S37)
- ~~Close spawn loop with Task tool~~ → Done (S43+)
- ~~Fix swarm.sh belief counter~~ → Fixed (S36)

## Bugs (all resolved)
- ~~`session_tracker.py:199` hardcodes `35`~~ FIXED — no longer present in current code
- ~~Zero negative tests~~ FIXED — 3 negative tests pass: `neg_broken_belief_detected`, `neg_broken_dep_ref_detected`, `neg_missing_falsification_detected`
