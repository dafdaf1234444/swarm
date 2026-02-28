# Quality Domain — Frontier Questions
Domain agent: write here for quality-specific questions; cross-domain findings go to tasks/FRONTIER.md
Updated: 2026-02-28 S189 | Active: 2 | Resolved: 1

## Active

- **F-QC2**: Do high-citation lessons decay in accuracy over time as the swarm's beliefs evolve? Hypothesis (B-QC2): a lesson written in S050 may have been correct then but contradicted by S150 evidence. High citation count does not guarantee current accuracy — it may reflect historical importance. Design: (1) identify the 20 most-cited lessons (by cross-reference scanning across all .md files); (2) check each against current PRINCIPLES.md and beliefs/DEPS.md for contradiction signals; (3) compute "citation gap" (last session cited vs current session) as proxy for freshness. Expected outcome: ~5% of high-citation lessons are stale by current belief state. Related: F-BRN1 (Hebbian co-citation), L-277 (compact.py false-archive from zero-cited scan), compact.py.

- **F-QC3**: Which domain pairs have the highest cross-domain lesson redundancy? Hypothesis (B-QC3): domain pairs that share an isomorphism in ISOMORPHISM-ATLAS will also share near-duplicate lessons — the same structural insight gets written twice, once per domain vocabulary. Method: (1) extract domain assignments from each lesson's citation header; (2) run Jaccard similarity within and across domain groups; (3) compute cross-domain redundancy matrix (N_domains x N_domains); (4) compare top-redundancy pairs against ISOMORPHISM-ATLAS entries. Expected: evolution↔meta, brain↔ai, and game-theory↔operations-research show highest overlap. Related: F-QC1 (near-duplicate detection), F126 (isomorphism atlas), domains/ISOMORPHISM-ATLAS.md.

## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
| F-QC1 | CONFIRMED: 15.3% duplication rate (35 pairs, 44 flagged / 288 lessons) exceeds 2–10% hypothesis. Two dominant patterns: same-session multi-agent convergence (L-257/267) and sequential refinement without scan (L-285/292). Prescription: expand quality gate to last 20 titles; flag same-session pairs in compact.py. See L-309. | S189 | 2026-02-28 |
