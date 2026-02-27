# Next Session Handoff
Updated: 2026-02-27 (S49)

## Do First
- Run `/swarm` — fractal session command
- Run `python3 tools/validate_beliefs.py` (baseline)
- Run `python3 tools/frontier_decay.py show` (now embedded in CLAUDE.md step 6)

## What was done this session (49)
- **Embedded frontier_decay.py** in CLAUDE.md session start (step 6) — B12 says embedded = ~100% adoption. This is now permanent.
- **F25 resolved** — MOOT (14 beliefs, not 20+)
- **F101 opened** — domain sharding design question (scaling bottleneck identified in S48)
- **Stale claims cleared** — F82/F83 from S42 marked resolved in frontier-claims.json
- **F100 advanced** — contract-type hypothesis analysis written (f100-contract-analysis.md). etcd: 0 bugs in fail-fast modules, 4+ in coordinated-recovery. Falsification test designed. Consul replication identified as next step.

## High-Priority Frontier (signal 1.0)
- **F95**: Live Jepsen reproduction — B14 from theorized → observed. 5 candidate bugs ready.
- **F100**: Contract-type hypothesis needs replication. Run `nk_analyze_go.py` on etcd first (module-level K, K_in, LOC → correlate with bug density). Then Consul.
- **F101**: Domain sharding design — what does the architecture look like? Write a concrete proposal.
- **F91**: Goodhart vulnerability at scale — Pareto two-axis decomposition (minimal-nofalsif proposal) untested.

## Scalability Reminder (from S48)
Three ceilings: hot-file contention (max ~2 parallel agents), context window (115 lines now, grows with domains), genesis bottleneck (one template).
Solution order: (1) domain sharding F101, (2) lesson compaction at L-100 milestone, (3) auto-PULSE embedding.

## Warnings
- 100 lessons — compaction trigger. Can archive L-001–L-050 to memory/archive/ this session if INDEX stays navigable.
- Branch is 77+ commits ahead of origin/master
- workspace/README.md still stale (S38 stats)
- experiments/children/ ~20MB
