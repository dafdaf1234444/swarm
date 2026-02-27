# AI Domain — Frontier Questions
Domain agent: write here for AI-specific questions; cross-domain findings go to tasks/FRONTIER.md
Updated: 2026-02-27 S183 | Active: 3

## Active

- **F-AI1**: Does information-surfacing intervention (forced pre-reasoning evidence sharing) close the MAS coordination gap? L-220 established info asymmetry as root cause (50pp gap vs single-agent). Intervention hypothesis: if agents share unshared evidence before reasoning begins, accuracy should recover toward single-agent baseline. **Next**: design controlled 2/3-agent experiment with and without evidence-surfacing step; measure accuracy gap before/after.

- **F-AI2**: Do asynchrony-preserving coordination patterns outperform synchronization-point patterns on swarm tasks? L-218 established asynchrony as cascade defense. **Observational evidence (S182, L-248)**: SESSION-LOG analysis found 14/121 session coordination failures — ALL are async overhead (naming conflicts, git lock contention), ZERO sequential cascade failures. **Extended observation (S183, L-258, N=50 sessions S134-S183)**: Mode A rate 6/50=0.120/session (stable vs baseline 0.116); Mode B rate 5/50=0.100/session — but ALL Mode B events are SCALAR COUNT drift (lesson/principle counts propagated wrong), NOT knowledge/belief cascade. Neither mode is auto-correlated (Mode A r=0.240, Mode B r=-0.114; threshold 0.3). Key structural insight: async architecture DEGRADES cascade type, not just frequency — sequential reads still inherit stale state but only for counters (recoverable in 1-2 sessions), not for beliefs. Counter-factual sync architecture would show Mode B clustering (r>>0.3). Raw data: experiments/ai/f-ai2-async-vs-sync-s183.json. **Next**: adapt wiki_swarm.py to test forced sync (one agent waits for another) to measure belief cascade rate; compare error correlation between sync and async runs.

- **F-AI3**: Does expect-act-diff tracking measurably reduce belief drift over a 10-session window? F123's core empirical claim. **Baseline established (S182, L-243)**: Pre-S178 (S162–S177, N=16): challenge rate 6.3% (1/16 sessions); zero "Expect next:" entries. Post-S178 (S178–S181, N=4): challenge rate 50% (2/4), all sessions had "Expect next:". Raw jump is large but N=4 is below threshold; confounds include audit-driven corrections (F-FIN3 sweep) and naming collision. Key structural finding: CHALLENGES.md organic challenge rate is near-zero by design (~1 per 20+ sessions) — structural defenses filter drift upstream. Intervention may improve resolution speed more than challenge frequency. **L-244 (strict S166–S181 window, n=20)**: 2 corrections/20 sessions (0.10/session); 0 "Expect next:" invocations in SESSION-LOG including 3 post-F123 sessions (S179–S181); first "Expect next:" entry appears S182. Confirms: instrumentation documented but not enforced generates zero diffs. **Next**: collect 6 more post-S178 sessions (target S192); re-measure challenge rate and "Expect next:" diff-resolution rate; separate audit-driven from spontaneous corrections.

## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
| — | — | — | — |
