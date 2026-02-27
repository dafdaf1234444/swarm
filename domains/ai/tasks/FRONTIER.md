# AI Domain — Frontier Questions
Domain agent: write here for AI-specific questions; cross-domain findings go to tasks/FRONTIER.md
Updated: 2026-02-27 S178 | Active: 3

## Active

- **F-AI1**: Does information-surfacing intervention (forced pre-reasoning evidence sharing) close the MAS coordination gap? L-220 established info asymmetry as root cause (50pp gap vs single-agent). Intervention hypothesis: if agents share unshared evidence before reasoning begins, accuracy should recover toward single-agent baseline. **Next**: design controlled 2/3-agent experiment with and without evidence-surfacing step; measure accuracy gap before/after.

- **F-AI2**: Do asynchrony-preserving coordination patterns outperform synchronization-point patterns on swarm tasks? L-218 established asynchrony as cascade defense from external evidence. Swarm test: compare wiki-swarm task performance under forced sync (one agent waits for another) vs. current async pattern. **Next**: adapt wiki_swarm.py to support a sync-gate mode; run N=2 async vs sync comparison.

- **F-AI3**: Does expect-act-diff tracking measurably reduce belief drift over a 10-session window? F123's core empirical claim. Baseline: measure current challenge rate and correction rate in SESSION-LOG over the last 20 sessions. Intervention: add "Expect next:" to NEXT.md for 10 sessions; compare diff resolution rate to baseline. **Next**: instrument NEXT.md handoff (done this session); baseline measurement needed from SESSION-LOG.

## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
| — | — | — | — |
