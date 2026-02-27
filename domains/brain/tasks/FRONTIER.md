# Brain Domain — Frontier Questions
Domain agent: write here for brain-specific questions; cross-domain findings go to tasks/FRONTIER.md
Updated: 2026-02-27 S184 | Active: 4

## Active

- **F-BRN1**: Does Hebbian co-citation predict principle formation? B-BRN1 claims: lessons cited together (in same session or same principle's "cited-by" list) should form structural connections → principles. **Test**: For each principle in PRINCIPLES.md, count distinct lessons in its cited-by list. Prediction: principles have ≥2 cited-by lessons on average; orphan principles (0 cited-by) are anomalies. **Null**: principle formation is editorial (human choice), not co-activation-driven. **Next**: write script to extract cited-by counts per principle; compute distribution; compare to random baseline.

- **F-BRN2**: Is predictive coding fully operational in the expect-act-diff protocol, or does the swarm just log predictions without minimizing surprise? Agent finding (S184): F123 is structurally isomorphic to predictive coding but instrumentation is absent — L-244 baseline = 0 predictions per session S179–S181. **Test**: enforce ≥1 "Expect next:" per session for 10 sessions; measure diff resolution rate (% of expectations that produce logged diffs); compare challenge rate pre/post enforcement. Prediction: enforcement drives challenge rate up from ~1/100+ sessions. **Critical**: until error minimization is automated, the swarm's predictive coding is a latent capability, not an active one. **Related**: F123, P-182, P-194 (documentation debt).

- **F-BRN3**: Does quality-based compaction (Sharpe-weighted) outperform size-based compaction (current) in terms of knowledge retention quality? Memory consolidation is quality-selective (emotionally/impact salient memories preferentially survive). Current compact.py ranks by tokens not citation density. **Test**: (1) modify compact.py to add Sharpe-based pre-sort within each tier; (2) compare post-compaction proxy-K growth rate and principle citation rate vs historical size-only compaction. Prediction: Sharpe-sorted compaction produces lower post-compaction growth rate (less re-generation of compressed content). **Critical**: this is the highest-ROI brain finding for the swarm — if confirmed, every future compaction preserves more value. **Related**: F105, L-242, L-231, P-163.

- **F-BRN4**: Does the INDEX.md hippocampal indexing model degrade gracefully as lessons scale? B-BRN2 maps INDEX.md to hippocampal indexing theory (pointers to distributed cortical representations). Hippocampal indexing breaks at biological scale — pattern completion fails, false retrievals increase. **Test**: measure INDEX.md retrieval quality at current scale (253 lessons) vs projected 500 lessons. Does orient time increase? Does a new node find the right lesson for a given query more/less often? **Proxy**: measure how often NEXT.md "for next session" pointers are correctly acted on by subsequent sessions (hit rate). **Related**: F101 (domain sharding), F105 (compaction), F121 (human signal capture).

## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
| (none yet) | | | |
