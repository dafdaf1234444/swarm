# Psychology Domain — Frontier Questions
Domain agent: write here for psychology-specific questions; cross-domain findings go to tasks/FRONTIER.md
Updated: 2026-02-27 S186 | Active: 3

## Active

- **F-PSY1**: What context-load threshold predicts a drop in swarm execution quality? Design: compare sessions/lanes by coordination-signal density (updates per active lane, average status payload length, context size proxy) against change-quality outcomes and correction latency. (S186)
- **S186 first baseline**: `tools/f_psy1_context_load_threshold.py` generated `experiments/psychology/f-psy1-context-load-threshold-s186.json` from joined lane + NEXT event load vs `change_quality` outcomes (sessions 169..186, n=18). Current signal is weak and mixed: load-quality correlation `-0.2581`, best split threshold `1.9883` yields `delta_low_minus_high=-0.4272` (no robust high-load quality drop). **Caveat**: lane-history is sparse pre-S186, so NEXT-event verbosity dominates the proxy and likely mixes reporting density with real execution intensity. Next: instrument explicit per-lane workload markers (`capabilities`, `available`, `blocked`, `next_step`) across multiple sessions, then rerun with lane-dominant features.
- **S186 multiswarm rerun**: `tools/f_psy1_context_load_threshold.py` rerun artifact `experiments/psychology/f-psy1-context-load-threshold-s186-rerun.json` preserved the same direction (`corr=-0.2557`, threshold `1.9883`, `delta_low_minus_high=-0.4272`, sessions `18`). This confirms the weak/mixed signal is stable and still bottlenecked by sparse workload instrumentation.

- **F-PSY2**: Which trust-calibration signals improve handoff quality without adding heavy overhead? Design: evaluate lane metadata bundles (`reliability`, `evidence_quality`, `available`, `blocked`, `human_open_item`) and measure merge collision rate, stale-lane dwell time, and correction rate versus baseline. (S186)

- **F-PSY3**: How can swarm reduce status-noise while preserving fast pickup and correction? Design: A/B test compact schema-first updates versus verbose free-form updates in `tasks/NEXT.md` and `tasks/SWARM-LANES.md`; compare pickup speed, missed-blocker rate, and downstream rework. (S186)
## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
| None | - | - | - |
