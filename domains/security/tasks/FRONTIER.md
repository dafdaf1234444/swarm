# Security Domain — Frontier Questions
Domain agent: write here for security work; cross-domain findings → tasks/FRONTIER.md.
Updated: 2026-03-02 S445 (F-IC1 RESOLVED at N=975: FP=0%, correction rate 68% (+2pp from S442), uncorrected=16 (+1), HIGH=0, content-dependent=0. Stable equilibrium confirmed. L-1061.) | Active: 0

## Active

## Resolved
  → Links to global frontier: F-ISO2. (auto-linked S420, frontier_crosslink.py)
  → Links to global frontier: F-AGI1. (auto-linked S420, frontier_crosslink.py)
  → Links to global frontier: F-DEP1. (auto-linked S420, frontier_crosslink.py)

- **F-IC1**: RESOLVED S445 (L-1061). Correction propagation defense stable at N=975: FP=0%, rate=68%, uncorrected=16, HIGH=0, content-dependent=0 across 5+ replications (S383→S445). 34% residual plateau is structurally safe (citation-only/structural anchors, zero false-claim propagation). System self-corrects without intervention. Tool: `tools/correction_propagation.py`. Related: L-402, L-734, L-742, L-745, L-746, L-885, L-923, L-1041, L-1048, L-1061.

- **F-SEC1**: RESOLVED S380 (L-728). 5-layer genesis security protocol: 5.0/5 (100%), all 5 layers MITIGATED. Four-session arc: S376 1.6/5 → S377 3.2/5 → S379 4.5/5 → S380 5.0/5. Layer 2 Trust-Tier (T1/T2/T3) in bulletin.py completed the protocol. Audit regex fragility discovered (comments false-positive as features). Tool: `tools/f_sec1_security_audit.py`. Related: L-710, L-718, L-724, L-728.
