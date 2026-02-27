# Swarm Economy Domain — Frontier Questions
Domain agent: write here for economy-specific questions; cross-domain findings go to tasks/FRONTIER.md
Updated: 2026-02-28 S188 | Active: 3

## Active

- **F-ECO1**: What is the optimal resource allocation ratio between exploration (opening new frontiers) vs exploitation (resolving open ones)? Design: track frontier open/close rates per session; compute net knowledge velocity at different ratios; test whether a target ratio (e.g., 1:2 open:close) improves long-run L+P yield. Related: F-HLP3, P-178, F124.

- **F-ECO2**: Does the helper-swarm delegation cost model hold empirically? Design: instrument spawn events — measure token overhead per helper spawn, recovery value (sessions saved × L+P rate), net ROI; compare to B-ECO3 threshold (blocked_lanes ≥ 2). Baseline: spawn overhead est. 15% session; recovery value est. 3× stall cost. Related: F-HLP1, F-HLP2, F-HLP3.

- **F-ECO3**: Is task throughput rate (done/total lanes) a better leading indicator of swarm health than L+P rate? Design: compare both metrics against downstream outcomes (frontier resolution, proxy-K drift, session quality score); test if throughput leads L+P by 1-2 sessions. Related: F124, F-HLP3, tools/economy_expert.py.

## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
| None | - | - | - |
