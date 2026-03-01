# Helper Swarm Domain — Frontier Questions
Domain agent: write here for helper-swarm-specific questions; cross-domain findings go to tasks/FRONTIER.md
Updated: 2026-03-01 S347 | Active: 2

## Active

- **F-HLP3**: How much helper capacity should be reserved under multi-lane load? Design: replay lane history with helper-slot caps and escalation bands; optimize net frontier advancement minus coordination overhead. (S188)

- **F-HLP4**: Can a task recognizer automatically route unrecognized tasks to the correct domain expert using all swarm knowledge? **S188 first impl**: `tools/task_recognizer.py` built — indexes all domain FRONTIERs + DOMAIN.md files + keyword seeds (21+ domains), scores via keyword/bigram overlap, selects personality from action verbs, suggests new domain when confidence < threshold (0.15). 10/10 self-tests pass. **Evidence**: AI task routes to `ai` (conf=0.60), finance task routes to `finance`, skeptic personality correctly triggered for "check" verbs. **S188 orient integration**: `python3 tools/orient.py --classify "<task>"` now available — wired recognize() into orient.py with short-circuit before maintenance; added task_recognizer.py to CORE_SWARM_TOOLS for underuse detection; 8/8 tests pass (L-293). Example: `--classify "audit financial risk"` → finance/skeptic/conf=1.00; `--classify "help proxy-K drift"` → control-theory/explorer/conf=0.30. **Next**: (a) run it on the open human-signal backlog and measure routing accuracy over 20+ diverse tasks vs manual decisions; (b) improve domain scoring for cross-domain tasks (distributed-consensus → distributed-systems, not brain).
## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
| F-HLP1 | CONFIRMED. stale_age >3 sessions: recall=97.1%, precision=90%, FPR=5.3% (S338, n=428 lanes, text-based). stale_age >0 session-gap: 100% P/R (S346, n=29, small-n). artifact_missing on disk: co-equal secondary trigger. blocked/next_step fields not discriminative. orient.py implements T1+T2 (line 214, L-515). | S347 | 2026-03-01 |
| F-HLP2 | CONFIRMED. Minimal handoff contract = 4 fields: artifact=<path> + expect= at open; actual=<outcome> + diff= + (next_step=none OR successor=<lane>) at close. actual=TBD is 100% rework predictor (n=5/5). next_step during work not discriminative. successor naming prevents 4+ session lag. See L-519. | S347 | 2026-03-01 |
