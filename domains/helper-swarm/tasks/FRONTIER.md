# Helper Swarm Domain — Frontier Questions
Domain agent: write here for helper-swarm-specific questions; cross-domain findings go to tasks/FRONTIER.md
Updated: 2026-03-01 S359 | Active: 1

## Active

- **F-HLP4**: Can a task recognizer automatically route unrecognized tasks to the correct domain expert using all swarm knowledge? **S188 first impl**: `tools/task_recognizer.py` built — indexes all domain FRONTIERs + DOMAIN.md files + keyword seeds (21+ domains), scores via keyword/bigram overlap, selects personality from action verbs, suggests new domain when confidence < threshold (0.15). 10/10 self-tests pass. **S359 accuracy benchmark** (n=40 real session tasks, L-641): 35% top-1 accuracy, 57.5% top-3. Confidence nearly useless (1.0 vs 0.916). Root cause: swarm vocabulary false cognates + textbook-not-operational seeds. NK: 0%, IS: 0%, meta: 50%. 4 fixes identified: operational seeds, F-ID boosting, relative confidence, infra-term deprioritization. Target: 60% top-1 at S370. **Next**: implement fixes, re-measure.

## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
| F-HLP3 | CONFIRMED_NULL. Helper capacity reservation unnecessary. 38 lanes S313-S359: 0% blocked, 84.2% merged, 10.5% abandoned. All abandonments are preemption/starvation, not blocking. Reserve 0 helper slots; implement triage (pre-dispatch stale-lane check, lane-opening gate ≤2 ACTIVE). L-638. | S359 | 2026-03-01 |
| F-HLP1 | CONFIRMED. stale_age >3 sessions: recall=97.1%, precision=90%, FPR=5.3% (S338, n=428 lanes, text-based). stale_age >0 session-gap: 100% P/R (S346, n=29, small-n). artifact_missing on disk: co-equal secondary trigger. blocked/next_step fields not discriminative. orient.py implements T1+T2 (line 214, L-515). | S347 | 2026-03-01 |
| F-HLP2 | CONFIRMED. Minimal handoff contract = 4 fields: artifact=<path> + expect= at open; actual=<outcome> + diff= + (next_step=none OR successor=<lane>) at close. actual=TBD is 100% rework predictor (n=5/5). next_step during work not discriminative. successor naming prevents 4+ session lag. See L-519. | S347 | 2026-03-01 |
