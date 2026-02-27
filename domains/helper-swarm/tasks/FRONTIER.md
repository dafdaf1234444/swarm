# Helper Swarm Domain — Frontier Questions
Domain agent: write here for helper-swarm-specific questions; cross-domain findings go to tasks/FRONTIER.md
Updated: 2026-02-27 S186 | Active: 3

## Active

- **F-HLP1**: Which helper-trigger policy best identifies stalled work without creating false alarms? Design: compare trigger bundles (`blocked!=none`, stale READY/ACTIVE age, missing `next_step`, low progress churn) against recovery latency and false-positive assist rate.

- **F-HLP2**: What helper handoff contract minimizes correction lag and rework? Design: A/B test helper lane metadata sets (assignment owner, artifact refs, recovery exit criteria, explicit `next_step`) and measure merge collision, reopen rate, and time-to-closure.

- **F-HLP3**: How much helper capacity should be reserved under multi-lane load? Design: replay lane history with helper-slot caps and escalation bands; optimize net frontier advancement minus coordination overhead.

## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
| None | - | - | - |
