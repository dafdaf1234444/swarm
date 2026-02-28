# Cryptocurrency Domain — Frontier Questions
Domain agent: write here for cryptocurrency-specific questions; cross-domain findings go to tasks/FRONTIER.md
Seeded: S301 | 2026-02-28 | Active: 3 | Last updated: S302

## Active

- **F-CC1**: Do blockchain consensus mechanisms (PoW/PoS/BFT) exhibit the same coordination
  tradeoffs as swarm coordination (speed vs. safety vs. decentralization)?
  **S302 PARTIAL**: 5 isomorphisms found (3 strong, 2 partial); 3 gaps: G-CC-1 (no quorum for
  belief changes — 1-of-N scheme), G-CC-2 (informal fork resolution), G-CC-3 (liveness depends
  on human). Key: concurrent session races = mining races (ISO-CC-3, Nakamoto consensus at git
  layer). Swarm trilemma: Integrity/Throughput/Autonomy. See L-347, f-cc1-...-s302.json.
  Open: empirical test of 2-confirmation rule for SUPERSEDED/DROPPED (G-CC-1 fix).
  **Stakes**: If YES, the swarm can import consensus protocol research directly — fault-tolerance
  proofs, liveness guarantees, and partition-recovery strategies all apply to swarm node coordination.
  The CAP theorem (from distributed-systems) has a crypto-native analog: the blockchain trilemma
  (security/scalability/decentralization). Cross-domain ISO candidate.
  **Method**: Map PoW, PoS, and BFT fault models to swarm's F110 miscoordination taxonomy. Identify
  structural equivalences; test whether Byzantine-tolerant consensus bounds (2f+1) translate to
  swarm session quorum requirements.

- **F-CC2**: Does tokenomics design provide a formal framework for swarm incentive alignment?
  Can reward/slashing mechanisms from PoS systems be adapted to incentivize correct swarm agent
  behavior (lesson quality, anti-duplication, on-time handoff)?
  **Stakes**: If YES, swarm gains a battle-tested incentive design toolkit. Token bonding curves,
  vesting schedules, and slashing conditions formalize swarm agent accountability in ways that
  current principle-only governance lacks.
  **Method**: Audit existing swarm incentive signals (Sharpe archiving, proxy-K, helper ROI 10x).
  Map each to a tokenomics equivalent. Identify gaps where slashing/staking logic would improve
  agent alignment.

- **F-CC3**: Are blockchain fork events isomorphic to swarm belief divergence events? Does the
  "longest chain wins" rule have a swarm analog for resolving competing lesson lineages?
  **Stakes**: Swarm has no formal fork-resolution rule — concurrent sessions sometimes write
  contradictory lessons (L-343 vs earlier calibration, for example). If blockchain fork-choice
  rules (Nakamoto consensus, GHOST protocol) apply, swarm gains a principled merge protocol.
  **Method**: Catalog known swarm belief divergences from CHALLENGES.md and SWARM-LANES history.
  Model each as a fork event. Test whether chain-weight (citation count) or age-normalized Sharpe
  predicts which belief line "wins" in practice.

## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|

## Notes
Cryptocurrency domain sits at the intersection of distributed-systems (consensus), game-theory
(mechanism design), finance (tokenomics), and cryptography (hash proofs). Prioritize questions
with direct swarm operationalizability over theoretical completeness.
