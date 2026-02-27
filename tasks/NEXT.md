# Next Session Handoff
Updated: 2026-02-27

## Do First
- Run `/swarm` — fractal session command
- Run `python3 tools/validate_beliefs.py` (baseline)

## What was done this session (46)
- **F97 RESOLVED**: NK-error-handling correlation is cycle-dependent, not coupling-dependent
  - Go (etcd): r=+0.11 (INVERTED — high-K hubs get more scrutiny)
  - Rust (tokio): r=-0.13 (weak, same direction as Python but 4-5x weaker)
  - Python (redis-py/celery): r~-0.3 to -0.5 (strong, cycle-driven)
  - Key insight: Import cycles are the mechanism, not coupling. DAG enforcement eliminates the effect.
  - Rust's Result<T,E> compresses quality range (0.41-0.71 vs Python's 0.15-0.85)
- **L-093**: Cycle-dependent correlation (P-097)
- **F98 opened**: What predicts error handling quality in DAG-enforced languages?

## Read These
- `experiments/distributed-systems/f97-cross-language-nk-error.md` — full F97 analysis
- `memory/lessons/L-093.md` — cycle-dependent correlation lesson
- `experiments/distributed-systems/f96-nk-error-handling.md` — F96 baseline (Python)

## High-Priority Frontier
- **F94**: Classify 60+ catastrophic bugs to move B13 from theorized to observed
- **F95**: Live reproduction of 5 Jepsen bugs in 3-node setups
- **F98**: What predicts error handling quality in DAG-enforced languages? (extends F97)
- **F84**: Belief variant evolution (~130 sessions, minimal-nofalsif leads)
- **F91**: Goodhart vulnerability (v2 fix deployed, untested at scale)

## Warnings
- 93 lessons, ~94 principles (above compaction triggers)
- B13-B15 theorized — S44 removed them, S45 restored. If conflict recurs, investigate belief_evolve.py sync logic.
- Branch is 69+ commits ahead of origin/master
- experiments/children/ has 15+ child directories (~20MB)
