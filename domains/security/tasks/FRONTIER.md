# Security Domain — Frontier Questions
Domain agent: write here for security work; cross-domain findings → tasks/FRONTIER.md.
Updated: 2026-02-28 S307 | Active: 1

## Active

### F-SEC1: Inter-swarm genesis sharing protocol — integrity, trust tiers, hostile signal detection
**Status**: OPEN | S307 | Human signal: "inter swarm genesis sharing protocol for interswarm security expert swarm"
**Question**: Does a 5-layer genesis sharing security protocol (bundle integrity + authority tiers + drift threshold + hostile signal heuristic + minimum transfer unit) prevent belief injection and genesis replay attacks in multi-colony swarms?
**Hypothesis**: Formalizing trust tiers (T1/T2/T3) for inter-swarm signals will reduce undetected belief drift by surfacing parent→child vs child→parent vs sibling trust boundaries. [THEORIZED n=0]
**Approach**:
1. Implement genesis bundle hash verification in genesis_evolve.py (SHA-256 of genesis.sh + CORE.md)
2. Add bulletin authority tier field to experiments/inter-swarm/PROTOCOL.md
3. Add belief drift check to merge_back.py (flag if diff >30%)
4. Wire hostile-signal heuristic to check.sh FM guard (new FM-10)
5. Test: spawn 2 child colonies, mutate one child's beliefs, verify parent detects at merge-back
**Success**: parent catches ≥90% of simulated belief injection attempts AND genesis bundle mismatch triggers human escalation
**Related**: F-HUM1, F-SCALE1, F-STRUCT1, F-GOV4, FM-09, L-401

## Resolved
(none yet)
