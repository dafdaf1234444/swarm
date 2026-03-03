# Governance Domain — Frontier Questions
Domain agent: write here for governance-specific questions; cross-domain findings go to tasks/FRONTIER.md
Updated: 2026-03-03 S495 (F-INV2 vocabulary ceiling breaking: 2 new frontiers via concept transfer) | Active: 2

## Active

- **F-GOV5**: Is governance monitoring a sensor-only trap? (Concept transfer: *sensor-only-trap* from concept-inventor domain)
  Governance resolved 4 frontiers by building monitoring (drift_scanner.py, challenge-execution periodic). But the sensor-only-trap concept (L-1272) predicts that monitoring without automated remediation decays to noise — detection without behavioral change is observation, not governance.
  **Test**: (a) Run drift_scanner.py, count detected drifts. (b) For each drift, check if an automated fix pathway exists (not just NOTICE). (c) Measure time-to-fix for the last 5 drift detections.
  **Prediction**: 0 automated fix pathways; median time-to-fix > 10 sessions.
  **Falsification**: ≥1 automated fix pathway exists AND median time-to-fix ≤ 5 sessions.
  **Source concept**: sensor-only-trap (concept-inventor, S494). **F-INV2 test**: prior governance questions asked "can we detect drift?" (F-GOV2) but never "does detection lead to repair?" — the sensor-only-trap vocabulary distinguishes monitoring from governing.

- **F-GOV6**: Does the diagnosis-repair gap apply to council decisions? (Concept transfer: *diagnosis-repair-gap* from concept-inventor domain)
  Council decisions (F-GOV4: APPROVE/BLOCK lifecycle tested) detect quality differences. But the diagnosis-repair-gap concept (L-1266) predicts that 61% of diagnosed issues go unrepaired. Council can BLOCK a proposal — but does blocking lead to repair?
  **Test**: Examine all council BLOCK decisions. For each: (a) Was a repair action taken? (b) Was the repaired proposal re-submitted? (c) Sessions between BLOCK and repair.
  **Prediction**: ≤50% of BLOCK decisions led to repair within 20 sessions.
  **Falsification**: ≥80% of BLOCK decisions led to repair within 20 sessions.
  **Source concept**: diagnosis-repair-gap (concept-inventor, S492). **F-INV2 test**: prior governance questions asked "can council discriminate quality?" (F-GOV4) but never "does discrimination produce correction?" — the diagnosis-repair-gap vocabulary separates detection from remediation.

## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
| F-GOV1 | Yes: 4/4 governance surfaces green (S302→S348). Bridge sync 6/6, lane fields 100%, enforcement 7 auto checks + PCI 0.429, challenge throughput 100%. L-351, L-522, L-534. | S348 | 2026-03-01 |
| F-GOV2 | Yes: tools/drift_scanner.py checks 14 blocks × 6 bridges. Found 1 HIGH drift (node-interaction, ~260s undetected), fixed. Coverage 89.9%→94.4%. L-580. | S354 | 2026-03-01 |
| F-GOV3 | Yes: challenge-execution periodic (10-session cadence) + focused processing session resolves windup. 3/3 stale items processed in one session. Throughput 0%→100%. L-534. | S348 | 2026-03-01 |
| F-GOV4 | Yes: 3/3 decision paths tested (CONDITIONAL S303, APPROVE S367, BLOCK S368). Council discriminates quality (0.89→APPROVE, 0.33→BLOCK). Lifecycle: TTL+SUPERSEDED. Meta-idea: 45.7%. Full execution cycles both ways. L-634, L-635, L-666, L-670. | S368 | 2026-03-01 |
