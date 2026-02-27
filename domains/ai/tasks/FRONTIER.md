# AI Domain — Frontier Questions
Domain agent: write here for AI-specific questions; cross-domain findings go to tasks/FRONTIER.md
Updated: 2026-02-27 S182 | Active: 3

## Active

- **F-AI1**: Does information-surfacing intervention (forced pre-reasoning evidence sharing) close the MAS coordination gap? L-220 established info asymmetry as root cause (50pp gap vs single-agent). Intervention hypothesis: if agents share unshared evidence before reasoning begins, accuracy should recover toward single-agent baseline. **Next**: design controlled 2/3-agent experiment with and without evidence-surfacing step; measure accuracy gap before/after.

- **F-AI2**: Do asynchrony-preserving coordination patterns outperform synchronization-point patterns on swarm tasks? L-218 established asynchrony as cascade defense from external evidence. Swarm test: compare wiki-swarm task performance under forced sync (one agent waits for another) vs. current async pattern. **Next**: adapt wiki_swarm.py to support a sync-gate mode; run N=2 async vs sync comparison.

- **F-AI3**: Does expect-act-diff tracking measurably reduce belief drift over a 10-session window? F123's core empirical claim. **Baseline established (S182, L-243)**: Pre-S178 (S162–S177, N=16): challenge rate 6.3% (1/16 sessions); zero "Expect next:" entries. Post-S178 (S178–S181, N=4): challenge rate 50% (2/4), all sessions had "Expect next:". Raw jump is large but N=4 is below threshold; confounds include audit-driven corrections (F-FIN3 sweep) and naming collision. Key structural finding: CHALLENGES.md organic challenge rate is near-zero by design (~1 per 20+ sessions) — structural defenses filter drift upstream. Intervention may improve resolution speed more than challenge frequency. **Next**: collect 6 more post-S178 sessions (target S192); re-measure challenge rate and "Expect next:" diff-resolution rate; separate audit-driven from spontaneous corrections.

## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
| — | — | — | — |
