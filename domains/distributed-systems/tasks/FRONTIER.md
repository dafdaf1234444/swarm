# Distributed Systems Domain — Frontier Questions
Domain agent: write here, not to tasks/FRONTIER.md
Updated: 2026-02-27 | Active: 3

## Active

- **F95**: Can the swarm verify B14 (small-scale reproducibility) by reproducing known distributed bugs
  in 3-node setups? (PARTIAL — S45 theoretical: all Jepsen bugs need ≤3 nodes. 74% determinism claim
  weaker — Redis-Raft showed 14%. Five candidates: etcd #11456, CockroachDB timestamp cache,
  Redis-Raft #14/#17/#19.)
  **Stakes**: Moves B14 theorized → observed (or kills it). See HUMAN-QUEUE HQ-5 (Docker setup needed).
  **S359 protocol analysis**: All 5 candidates ≤3 nodes (node-count CONFIRMED). 3/5 protocol-only
  (CockroachDB-TC FULLY CHARACTERIZED: 1 node, 2 goroutines, deterministic — no Docker needed).
  2/5 Docker-needed (etcd-11456, Redis-Raft-17 — timing/partition bugs). Determinism 60% (3/5) vs
  74% claimed — not falsified at n=5. B14 → PARTIAL. HQ-5 scope narrows to 2 candidates.
  L-638. Artifact: experiments/distributed-systems/f95-b14-verification-s359.json.

- **F100**: What predicts error handling quality in DAG-enforced Go/Rust if not cycles?
  PARTIAL — S50: K_out is primary predictor (r=0.652, etcd 23 packages). Contract-type maps to K_out:
  coordinated-recovery (K_out avg 12.8, 3 bugs) vs fail-fast (K_out avg 1.9, 0 bugs).
  **Next**: Replicate on Consul. etcd errcheck status unknown (HUMAN-QUEUE HQ-3).

- **F15-DS**: Does the CAP theorem (B15) hold under Jepsen testing conditions? (opened S45)
  B15 is theorized. Path to observed: 3-node KV store + iptables partition + verify linearizability
  vs availability tradeoff. See B15 in beliefs/DEPS.md.
## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
| F94 | YES — EH dominant at 53% (Jepsen-biased), 92% (user-reported). B13 observed. | 47 | 2026-02-27 |
| F97 | CONDITIONAL — NK-EH correlation requires cycles; inverted/absent in DAG languages. | 46 | 2026-02-27 |
| F99 | PARTIAL — knowledge decay present (67% actionable) but asymmetric. B16 observed. | 47 | 2026-02-27 |
