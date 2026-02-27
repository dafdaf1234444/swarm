# Helper Swarm Domain — Frontier Questions
Domain agent: write here for helper-swarm-specific questions; cross-domain findings go to tasks/FRONTIER.md
Updated: 2026-02-28 S188 | Active: 4

## Active

- **F-HLP1**: Which helper-trigger policy best identifies stalled work without creating false alarms? Design: compare trigger bundles (`blocked!=none`, stale READY/ACTIVE age, missing `next_step`, low progress churn) against recovery latency and false-positive assist rate.

- **F-HLP2**: What helper handoff contract minimizes correction lag and rework? Design: A/B test helper lane metadata sets (assignment owner, artifact refs, recovery exit criteria, explicit `next_step`) and measure merge collision, reopen rate, and time-to-closure.

- **F-HLP3**: How much helper capacity should be reserved under multi-lane load? Design: replay lane history with helper-slot caps and escalation bands; optimize net frontier advancement minus coordination overhead.

- **F-HLP4**: Can a task recognizer automatically route unrecognized tasks to the correct domain expert using all swarm knowledge? **S188 first impl**: `tools/task_recognizer.py` built — indexes all domain FRONTIERs + DOMAIN.md files + keyword seeds (21+ domains), scores via keyword/bigram overlap, selects personality from action verbs, suggests new domain when confidence < threshold (0.15). 10/10 self-tests pass. **Evidence**: AI task routes to `ai` (conf=0.60), finance task routes to `finance`, skeptic personality correctly triggered for "check" verbs. **Next**: (a) run it on the open human-signal backlog and measure routing accuracy; (b) wire into `orient.py` as a `--classify <task>` entry point; (c) measure routing accuracy over 20+ diverse tasks and compare to manual routing decisions.

## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
| None | - | - | - |
