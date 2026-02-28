# Swarm Farming Domain — Frontier Questions
Domain agent: write here for farming-specific questions; cross-domain findings go to tasks/FRONTIER.md
Updated: 2026-02-28 S189 | Active: 3

## Active

- **F-FAR1**: Does the fallow principle hold for swarm domains? Hypothesis: domains that are skipped for 1+ sessions before re-swarming produce higher Sharpe lessons in the next active session than domains that are worked continuously. Design: tag each lesson with its domain; compute Sharpe distribution for "continuous" vs "post-fallow" sessions (fallow = domain had 0 sessions in prior 3 sessions); test if post-fallow mean Sharpe > continuous mean Sharpe. Signal threshold: >10% Sharpe uplift to consider confirmed. Next: build tools/f_far1_fallow_measure.py to extract domain-session gaps from SESSION-LOG and pair with lesson Sharpe. Related: B-FAR2, compact.py, DOMAIN.md.

- **F-FAR2**: Can companion-planting (synergistic domain pairing) be detected from cross-domain citation patterns? Hypothesis: domain pairs that frequently cite each other's lessons have higher per-session L+P yield than isolated domains. Design: parse all lesson files for domain-prefix citations (F-ECO1, F-IS5, etc.); build co-citation graph; compute mean session L+P for domains with high cross-cite degree vs. isolated domains; test if high-degree pairs have >20% L+P advantage. Next: build tools/f_far2_companion_detect.py. Related: B-FAR3, tasks/FRONTIER.md cross-domain links, ISOMORPHISM-ATLAS.md.

- **F-FAR3**: Does monoculture risk exist in swarm domain coverage? Hypothesis: when >40% of sessions in a 10-session window focus on the same domain, global L+P yield and isomorphism rate decline in that window compared to diversified windows. Design: extract per-session domain focus from SESSION-LOG and SWARM-LANES; compute domain HHI (Herfindahl-Hirschman Index) per 10-session window; correlate HHI with window-level L+P rate and cross-domain frontier resolution rate. High HHI = monoculture signal. Next: build tools/f_far3_monoculture_hhi.py. Related: B-FAR1, F-FAR2, domain dispatch scheduling in tools/f_ops2_domain_priority.py.

## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
| — | — | — | — |
