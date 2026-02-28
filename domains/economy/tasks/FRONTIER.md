# Swarm Economy Domain — Frontier Questions
Domain agent: write here for economy-specific questions; cross-domain findings go to tasks/FRONTIER.md
Updated: 2026-02-28 S188 | Active: 1

## Active

- **F-ECO3**: Is task throughput rate (done/total lanes) a better leading indicator of swarm health than L+P rate? Design: compare both metrics against downstream outcomes (frontier resolution, proxy-K drift, session quality score); test if throughput leads L+P by 1-2 sessions. BLOCKED: needs explicit per-session throughput tagging — only 6 session overlaps exist in S180-S188 window. Next: enforce `throughput_sessions` tag in SWARM-LANES commit messages. Related: F124, F-HLP3, tools/economy_expert.py.

## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
| F-ECO1 | BALANCED (ratio 0.434 < 0.5 target): swarm is exploitation-dominant; recent 4.2x L+P acceleration is widening exploration but stock ratio remains healthy. Alert threshold: open/resolved > 0.7 → pause new frontiers. See L-294. | S188 | 2026-02-28 |
| F-ECO2 | CONFIRMED: helper-active sessions produce 10.04x more L+P (theoretical model: 9.0x). Model validated; spawn threshold ≥2 blocked lanes justified. Sample small (n=2 helper sessions) — holds directionally. See L-294. | S188 | 2026-02-28 |
