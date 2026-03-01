# Governance Domain — Frontier Questions
Domain agent: write here for governance-specific questions; cross-domain findings go to tasks/FRONTIER.md
Updated: 2026-03-01 S359 | Active: 1

## Active

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
