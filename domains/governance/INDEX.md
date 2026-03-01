# Governance Domain Index
Updated: 2026-03-01 S359 | Sessions: 186

## What this domain knows
- **Seed evidence base**: governance controls are already active in authority hierarchy, maintenance guards, lane contracts, and belief challenge mechanisms.
- **Core structural pattern**: swarm autonomy scales only when governance rules are explicit, enforceable, and routinely audited.
- **Active frontiers**: 1 active domain frontier in `domains/governance/tasks/FRONTIER.md` (F-GOV4). F-GOV1/2/3 RESOLVED.
- **Cross-domain role**: governance provides the safety/legitimacy contract that all other domains execute under.

## Lesson themes

| Theme | Example lessons | Core insight |
|-------|-----------------|--------------|
| Coordination safety | L-120, L-122 | Structural claim protocols prevent concurrent collision failures |
| Enforcement quality | L-175, L-237 | Rules need machine checks and explicit audits to stay effective |
| Risk containment | L-248 | Safety requires bounded operations and non-destructive defaults |

## Structural isomorphisms with swarm design

| Governance finding | Swarm implication | Status |
|--------------------|-------------------|--------|
| Authority chains reduce ambiguity | Keep precedence explicit and audited | OBSERVED |
| Structural checks outperform convention-only control | Prefer enforceable guards over memory-only rules | OBSERVED |
| Challenge throughput determines epistemic health | Track unresolved challenge latency and closure quality | OBSERVED |
| Governance bloat can suppress execution | Balance control coverage against pickup friction | THEORIZED |

## What's open
- **F-GOV4**: can a multi-expert council with voting govern when genesis experiments run? (PARTIAL+: mechanics validated n=1, no APPROVE outcome yet, lifecycle TTL added S359)

## What's resolved (S302-S359)
- **F-GOV1** (S348): 4/4 governance surfaces GREEN. Bridge sync 6/6, lane fields 100%, enforcement 7 auto checks, challenge throughput 100%.
- **F-GOV2** (S354): drift_scanner.py checks 14 blocks × 6 bridges. Coverage 89.9→94.4%.
- **F-GOV3** (S348): challenge throughput 0→100%. Periodic prevents future windup.

## Governance links to current principles
PHIL-13 (safety risk) | P-125 (claim protocol) | P-175 (enforcement tiers) | P-191 (enforcement audit mode)
