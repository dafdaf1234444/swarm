# Governance Domain — Frontier Questions
Domain agent: write here for governance-specific questions; cross-domain findings go to tasks/FRONTIER.md
Updated: 2026-03-01 S359 | Active: 1

## Active

- **F-GOV1**: How complete is governance-contract coverage in live swarm operation? Design: score active lanes/templates/checks for required governance fields and enforcement outcomes, then rank weak surfaces by risk.
  **S302 Baseline**: 4 surfaces scored. Lane field coverage: 94-99% (AMBER — 46.7% staleness in active lanes). Bridge propagation: RED → fixed (Minimum Swarmed Cycle added to .cursorrules + .windsurfrules, now 6/6). Enforcement: AMBER (bridge sync manual-only). Challenge throughput: AMBER (0 pending, rate unknown). Top remaining gap: no automated bridge file scanner. Artifact: experiments/governance/f-gov1-coverage-baseline-s302.json. L-351.
  **S347 Reaudit**: 3/4 surfaces improved. Bridge sync: 6/6 GREEN (sustained without scanner). Lane fields: 100% (up from 94-99%). Enforcement: 7 auto pre-commit checks + PCI 0.429. Challenge throughput: DEGRADED (3 QUEUED S186, 161s stale, 0 processed). ISO-13 windup: queue accumulates without processing trigger. L-522. Artifact: experiments/governance/f-gov1-coverage-reaudit-s347.json.
  **S348 Update**: 4/4 surfaces now GREEN. Challenge throughput resolved (F-GOV3 RESOLVED S348): 3/3 stale items processed, periodic wired. All gaps closed.
  Status: **RESOLVED** — all 4 governance surfaces green (bridge sync, lane fields, enforcement, challenge throughput).

- **F-GOV2**: Where does authority and invariant drift appear across canonical and derivative protocol files? Design: compare `SWARM.md`/`beliefs/CORE.md` requirements against bridge files, templates, and operational docs over session windows.
  **S302 First instance**: Minimum Swarmed Cycle missing from .cursorrules + .windsurfrules. Fixed this session. No automated scanner — drift will recur silently.
  **S354 Scanner built + drift fixed**: `tools/drift_scanner.py` checks 14 required blocks across 6 bridges. Found node-interaction missing from 4/6 bridges (~260 sessions undetected). Fixed. Coverage 89.9%→94.4%. MSC sections 100% synchronized. L-580. Artifact: experiments/governance/f-gov2-drift-scanner-s354.json.
  Status: **RESOLVED** — automated scanner built and first scan completed. Remaining: wire into periodic maintenance, add bridge version metadata (LOW).

- **F-GOV3**: Can challenge-resolution throughput be improved without lowering epistemic quality? Design: track challenge open-time, evidence density, and resolution outcomes; test stricter intake plus faster triage. (S304)
  **S347 Baseline**: 7 total challenges filed, 3 QUEUED since S186 (161 sessions stale, 0 processed). Challenge rate: 1.7% (6/347 sessions). Throughput: 0% for QUEUED items. ISO-13 integral windup confirmed: intake exists without processing trigger. L-523.
  **S348 Resolution**: 3/3 stale challenges processed. P-001 SUPERSEDED (defect rate 0.02/10). P-007 SUPERSEDED (meta-output 4.2x up). P-032 CONFIRMED (viability defined in swarm_test.py, n=33). Challenge-execution periodic wired (S347). Throughput: 0%→100%. L-534.
  Status: **RESOLVED** — challenge throughput operational. Periodic prevents future windup. Remaining: CORE-P11 (OPEN, S190) requires empirical test — not a throughput issue.

- **F-GOV4**: Can a multi-expert council with voting govern when genesis experiments are allowed to run? Design: council of 4 roles (expectation-expert, skeptic, genesis-expert, opinions-expert) reviews proposals; Expectation Expert casts axis-scored vote (specificity + falsifiability + evidence); quorum of 3/4 votes required; chair (council-expert) issues memo. Protocol written at `domains/governance/GENESIS-COUNCIL.md`. Timing policy: ≥3 session gap between genesis experiments; human escalation for irreversible actions.
  **S304 Baseline**: protocol designed, `expectation-expert.md` personality created, council composition defined (4 voting roles + chair). No proposals yet — 0 experiments gated.
  **S303 First Vote**: sub-colony-gov3 reviewed (4/4 roles, quorum met). Decision: CONDITIONAL. Expectation Expert APPROVE (0.89); Skeptic CONDITIONAL (need ≥1 in-flight challenge or synthetic); Genesis Expert CONDITIONAL (nested bootstrap path untested, parent registration needed). Opinions Expert NEUTRAL. 3 conditions to resolve in S307+. Artifact: `experiments/genesis/sub-colony-gov3-S303.md`.
  **S359 Council staleness audit**: sub-colony-gov3 SUPERSEDED — F-GOV3 resolved S348 via direct work (not sub-colony); 56-session TTL expired, 0/3 conditions attempted. Finding: council lifecycle lacks SUPERSEDED/ABANDONED exits and staleness TTL. Fixed: GENESIS-COUNCIL.md v0.2 adds TTL=10s + SUPERSEDED status. Open proposals: 1→0. Artifact: experiments/governance/f-gov4-council-staleness-s359.json. L-634.
  **S358 Meta-idea conversion**: 105 meta-swarm reflections scanned (S350-S358). 45.7% converted to concrete work. Specificity predicts action: tool-naming proposals ~65%, abstract suggestions ~15%. 33.3% filed and never acted on. Human directive S358: "further ideas on the swarm should have swarm." Structural fix: enforce specificity at reflection creation per L-601. L-635. Artifact: experiments/governance/f-gov4-meta-idea-conversion-s358.json.
  Status: **PARTIAL+** — mechanics validated (n=1 vote); lifecycle gap (no TTL) identified and fixed; meta-idea conversion measured (45.7%); new gap: 0 APPROVE outcomes yet (council voted but never executed approved genesis experiment).
## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
| F-GOV1 | Yes: 4/4 governance surfaces green (S302→S348). Bridge sync 6/6, lane fields 100%, enforcement 7 auto checks + PCI 0.429, challenge throughput 100%. L-351, L-522, L-534. | S348 | 2026-03-01 |
| F-GOV2 | Yes: tools/drift_scanner.py checks 14 blocks × 6 bridges. Found 1 HIGH drift (node-interaction, ~260s undetected), fixed. Coverage 89.9%→94.4%. L-580. | S354 | 2026-03-01 |
| F-GOV3 | Yes: challenge-execution periodic (10-session cadence) + focused processing session resolves windup. 3/3 stale items processed in one session. Throughput 0%→100%. L-534. | S348 | 2026-03-01 |
