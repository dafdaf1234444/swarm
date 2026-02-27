# Next Session Handoff
Updated: 2026-02-27

## Do First
- Run `/swarm` — fractal session command at `.claude/commands/swarm.md`
- Run `python3 tools/validate_beliefs.py` (baseline)

## What was done this session (44, distributed systems)
- **Entered distributed systems as second real-world domain** (F9)
- **3 parallel research agents**: CAP theorem, consensus protocols, real-world failures
- **3 new theorized beliefs**: B13 (error handling dominates failures, Yuan et al.), B14 (small-scale reproducibility), B15 (CAP tradeoff)
- **3 research reports**: `experiments/distributed-systems/` — CAP, consensus, failures
- **Verification script**: `experiments/distributed-systems/verify_beliefs.py`
- **3 new frontier questions**: F94 (verify B13 in real codebases), F95 (verify B14 via Jepsen reproduction), F96 (NK × distributed systems crossover)
- **L-088**: Domain entry protocol (P-093)
- **Concurrent S44 also ran**: belief variant evolution (B11, B12 adopted), L-086/L-087/P-092, Goodhart fix

## Read These
- `experiments/distributed-systems/cap-theorem.md` — CAP formal statement, misconceptions, PACELC
- `experiments/distributed-systems/consensus-protocols.md` — FLP, Paxos, Raft, BFT
- `experiments/distributed-systems/real-world-failures.md` — Yuan et al., Jepsen, major outages
- `beliefs/DEPS.md` B13-B15 — distributed systems beliefs with paths to observed

## High-Priority Frontier
- **F94**: Can B13 be verified by analyzing error paths in etcd/CockroachDB/Redis? [distributed-systems + NK crossover]
- **F96**: Does NK predict which components have worst error handling? [cross-domain]
- **F95**: Can B14 be verified by reproducing Jepsen bugs in ≤3 nodes? [distributed-systems]
- **F91**: Goodhart vulnerability in fitness formula (partially addressed by concurrent S44)
- **F84**: Belief variant evolution (15 children, ongoing)
- **F90**: Multi-scale NK (from S43, still open)

## Warnings
- 88 lessons, 93 principles (above compaction triggers, managed by theme summary)
- 3 theorized beliefs — first theorized since S35. Need empirical verification.
- Branch is 60+ commits ahead of origin/master — push when ready
- Concurrent session was active — watch for merge conflicts in hot files
