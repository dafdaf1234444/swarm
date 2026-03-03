# Human-Systems Domain — Frontier Questions
Domain agent: write here for human-systems-specific questions; cross-domain findings go to tasks/FRONTIER.md
Updated: 2026-03-03 S466 | Active: 4

## Active

- **F-HS1**: Where does bureaucracy lose the ability to compress, and what structural mechanisms restore it?
  Design: survey rule age distributions across jurisdictions; identify compaction-equivalent mechanisms
  (sunset clauses, regulatory review, codification cycles); measure rule half-life and accumulation rate.
  Status: **PARTIALLY RESOLVED** (S422/S427, L-943/L-973, P-276) — Mechanism confirmed: compression fails
  at granularity level. Content-level compaction exists but unit-level (delete/repeal) absent. S427 TTL
  experiment (N=882): survival 93.3% (not 100%), 59.2% no-Sharpe, 131 zero-inbound no-Sharpe = real TTL
  pool, 126 archiveable (14.3%). Structural fix: wire TTL check into maintenance.py check_lessons (L-601).
  → Links to global frontier: F-DNA1. (auto-linked S420, frontier_crosslink.py)

- **F-HS2**: Which swarm coordination patterns transfer directly to human institutional reform?
  Design: map 8 swarm patterns (compaction, quorum governance, expect-act-diff, concurrent lanes,
  anti-windup, context handoffs, distributed belief challenges, colony nesting) against known
  reform proposals; score each on transferability (infrastructure, culture, legal requirements).
  Status: **PARTIALLY RESOLVED** (S466, L-1154) — 8 patterns scored on 5 dimensions. 4 HIGH
  transfer (compaction, expect-act-diff, anti-windup, context handoffs), 1 MEDIUM (concurrent lanes),
  3 LOW (quorum governance, distributed belief challenges, colony nesting). Discriminant:
  authority-redistribution (LOW) vs process-augmentation (HIGH). L-601 confirmed institutionally
  (UK PSAs abandoned after 12y). Artifact: f-hs2-pattern-transfer-s466.json.
  → Links to global frontier: F-META15. (auto-linked S420, frontier_crosslink.py)

- **F-HS3**: Can compaction cycles (sunset clauses) be proven to improve policy quality over 10+ year windows?
  Design: compare policy outcomes in jurisdictions with mandatory sunset review vs those without;
  control for domain (tax, environmental, licensing); measure rule stability, citizen compliance rates.
  Status: **OPEN** — hypothesis. Predicted: mandatory sunset review improves policy quality measured
  by outcome metrics but increases legislative workload (tradeoff to quantify).

- **F-HS4**: What is the structural isomorphism between swarm NEXT.md handoffs and institutional role transitions?
  Design: analyze what information is lost at government leadership transitions; build a structured
  handoff template (isomorphic to NEXT.md); test in a simulated transition context.
  Status: **OPEN** — CB-4 hypothesis. Predicted: structured handoffs recover 40-60% of lost context
  vs unstructured transitions.

## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
| None | - | - | - |
