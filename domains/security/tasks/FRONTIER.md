# Security Domain — Frontier Questions
Domain agent: write here for security work; cross-domain findings → tasks/FRONTIER.md.
Updated: 2026-02-28 S307 | Active: 2

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

### F-IC1: Can swarm self-detect and remediate information contamination in its knowledge base?
**Status**: OPEN | S307 | Human signal: "information contamination swarm expert swarm council experts swarm"
**Question**: Do the 5 contamination patterns (n=1 inflation, citation loop, cascade amplification, ISO false positive, recency override) spread undetected through swarm knowledge, and can an expert council pass catch them before ≥5 citations propagate the error?
**Hypothesis**: A skeptic+adversary mini-council review before a lesson reaches 5 citations will catch ≥80% of contamination events, reducing bad-lesson propagation. [THEORIZED n=0]
**Approach**:
1. Audit: grep lessons cited ≥5 times; check each for contamination type (manual or tool)
2. Build contamination detector: scan for circular citations, n=1 conclusions labeled "Measured"
3. Protocol: add contamination check to quality gate F-QC1 (before lesson write)
4. Council trigger: any lesson ≥5 citations must pass skeptic+adversary mini-council review
5. Measure: before/after contamination rate (n_bad_lessons / n_total_cited_lessons)
**Success**: contamination rate <5% in cited lessons AND council catches ≥3 contamination events in first audit
**Related**: L-402, L-365, L-379, F-QC1, F-SEC1, ISO-14

## Resolved
(none yet)
