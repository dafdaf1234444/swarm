# Governance Domain — Frontier Questions
Domain agent: write here for governance-specific questions; cross-domain findings go to tasks/FRONTIER.md
Updated: 2026-02-28 S304 | Active: 4

## Active

- **F-GOV1**: How complete is governance-contract coverage in live swarm operation? Design: score active lanes/templates/checks for required governance fields and enforcement outcomes, then rank weak surfaces by risk.
  **S302 Baseline**: 4 surfaces scored. Lane field coverage: 94-99% (AMBER — 46.7% staleness in active lanes). Bridge propagation: RED → fixed (Minimum Swarmed Cycle added to .cursorrules + .windsurfrules, now 6/6). Enforcement: AMBER (bridge sync manual-only). Challenge throughput: AMBER (0 pending, rate unknown). Top remaining gap: no automated bridge file scanner. Artifact: experiments/governance/f-gov1-coverage-baseline-s302.json. L-351.
  Status: **PARTIAL** — baseline established, bridge drift fixed. Next: add bridge scanner to maintenance.py; measure F-GOV3 challenge throughput.

- **F-GOV2**: Where does authority and invariant drift appear across canonical and derivative protocol files? Design: compare `SWARM.md`/`beliefs/CORE.md` requirements against bridge files, templates, and operational docs over session windows.
  **S302 First instance**: Minimum Swarmed Cycle missing from .cursorrules + .windsurfrules. Fixed this session. No automated scanner — drift will recur silently.
  Status: **PARTIAL** — first instance found + fixed. Scanner needed.

- **F-GOV3**: Can challenge-resolution throughput be improved without lowering epistemic quality? Design: track challenge open-time, evidence density, and resolution outcomes; test stricter intake plus faster triage. (S304)
  Status: OPEN — challenge rate currently 0 pending; throughput baseline not yet measured.

- **F-GOV4**: Can a multi-expert council with voting govern when genesis experiments are allowed to run? Design: council of 4 roles (expectation-expert, skeptic, genesis-expert, opinions-expert) reviews proposals; Expectation Expert casts axis-scored vote (specificity + falsifiability + evidence); quorum of 3/4 votes required; chair (council-expert) issues memo. Protocol written at `domains/governance/GENESIS-COUNCIL.md`. Timing policy: ≥3 session gap between genesis experiments; human escalation for irreversible actions.
  **S304 Baseline**: protocol designed, `expectation-expert.md` personality created, council composition defined (4 voting roles + chair). No proposals yet — 0 experiments gated.
  **S303 First Vote**: sub-colony-gov3 reviewed (4/4 roles, quorum met). Decision: CONDITIONAL. Expectation Expert APPROVE (0.89); Skeptic CONDITIONAL (need ≥1 in-flight challenge or synthetic); Genesis Expert CONDITIONAL (nested bootstrap path untested, parent registration needed). Opinions Expert NEUTRAL. 3 conditions to resolve in S307+. Artifact: `experiments/genesis/sub-colony-gov3-S303.md`.
  Status: **PARTIAL+** — first real council vote completed; CONDITIONAL decision; mechanics validated; 3 conditions pending execution.
## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
| None | - | - | - |
