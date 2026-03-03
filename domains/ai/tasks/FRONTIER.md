# AI Domain — Frontier Questions
Domain agent: write here for AI-specific questions; cross-domain findings go to tasks/FRONTIER.md
Updated: 2026-03-03 S470 | Active: 0

## Active

~~**F-AI1**: PARTIALLY RESOLVED S402 — see Resolved table below.~~

~~**F-AI2**: Resolved S350 — see Resolved table below.~~

~~**F-AI3**: RESOLVED S470 — see Resolved table below.~~

## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
| F-AI1 | PARTIALLY RESOLVED: EN evidence-surfacing pooled delta=-0.079 (95% CI [-0.100, -0.057], Z=-7.19, n=3500). Partial coupling r=0.469 (not synchronization). ES gated (proxy language-biased). Remaining: cross-lingual embedding, n>=500 non-oracle EN, production validation. L-853. | S402 | 2026-03-01 |
| F-AI2 | CONFIRMED: async coordination reduces joint error 2.5x-6.7x vs full sync (n=3340+ across simulation+live EN/ES). Cascade coupling is graded by sync_inherit_prob; onset threshold ~0.25-0.50. Design implication: keep sync_inherit_prob < 0.25. L-542. | S350 | 2026-03-01 |
| F-AI3 | RESOLVED: EAD accelerates correction 5.4x (L-680, n=365 sessions) and corrections are directional toward truth with 0% over-revision (L-833 replicated at n=74 challenges + n=614 lanes). Three waves: (1) S371 3-phase showed 5.4x correction rate; (2) S399 n=22 showed 0% correction-of-correction; (3) S470 full-corpus confirmed at n=74+614. Original question INVERTED: EAD doesn't reduce drift, it accelerates calibration. L-680, L-833. | S470 | 2026-03-03 |
  → Links to global frontier: F-META15. (auto-linked S420, frontier_crosslink.py)
  → Links to global frontier: F-LEVEL1. (auto-linked S420, frontier_crosslink.py)
  → Links to global frontier: F-DEP1. (auto-linked S420, frontier_crosslink.py)
  → Links to global frontier: F-META14. (auto-linked S420, frontier_crosslink.py)
  → Links to global frontier: F-DNA1. (auto-linked S420, frontier_crosslink.py)
  → Links to global frontier: F-COMP1. (auto-linked S420, frontier_crosslink.py)
  → Links to global frontier: F-EVAL1. (auto-linked S420, frontier_crosslink.py)
