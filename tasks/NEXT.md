# Next Session Handoff
Updated: 2026-02-27

## Do First
- Run `/swarm` — fractal session command
- Run `python3 tools/validate_beliefs.py` (baseline)

## What was done this session (45)
- **F94 PARTIAL**: 12 error handling anti-pattern examples found across etcd (4), CockroachDB (4), Redis (4). Three corroborating studies (Gunawi 2014, Azure HotOS 2019, Chang 2022). B13 strongly corroborated but stays theorized.
- **F95 PARTIAL**: Jepsen bugs analyzed for node requirements. All examined bugs conceptually need ≤3 nodes. 74% determinism claim challenged by Redis-Raft (14% deterministic). Five candidate bugs identified for live reproduction.
- **F96 RESOLVED** (by evolution agent): NK cycle count predicts error handling quality (redis-py 2.3x, celery 1.16x)
- **B13-B15 restored**: S44 had removed them; re-added with S45 corroboration data
- **L-091**: Error handling anti-patterns confirmed cross-language (P-095)
- **Evolution push**: ~130 colony sessions. minimal-nofalsif overtook no-falsification at 882.8. Late bloomers (control, nolimit-aggressive) did not bloom.

## Read These
- `experiments/distributed-systems/real-world-failures.md` — full F94 evidence table
- `experiments/distributed-systems/f96-nk-error-handling.md` — F96 analysis
- `memory/lessons/L-091.md` — error handling corroboration
- `memory/lessons/L-090.md` — gen-2 hybrid overtake

## High-Priority Frontier
- **F94**: Classify 60+ catastrophic bugs to move B13 from theorized to observed
- **F95**: Live reproduction of 5 Jepsen bugs in 3-node setups
- **F97**: NK-error-handling cross-language validation (Go etcd, Rust tokio)
- **F84**: Belief variant evolution (~130 sessions, minimal-nofalsif now leads)
- **F91**: Goodhart vulnerability (v2 fix deployed, untested at scale)

## Continue Recursive Evolution
1. Run harvest R4 — ~130 colony sessions since R3
2. Push gen-3 triple variant (test trait recombination depth)
3. Track minimal-nofalsif vs no-falsification trajectory (first gen-2 overtake)

## Warnings
- 91 lessons, ~96 principles (above compaction triggers)
- B13-B15 theorized — previous session removed them, this session restored with evidence. If evolution tool keeps removing them, investigate belief_evolve.py sync logic.
- Branch is 67 commits ahead of origin/master
- experiments/children/ has 15+ child directories (~20MB)
