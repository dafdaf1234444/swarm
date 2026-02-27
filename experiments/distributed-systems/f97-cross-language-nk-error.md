# F97: Does the NK-error-handling correlation hold across languages?

## Question
F96 showed NK cycles predict error handling quality in Python (redis-py 2.3x, celery 1.16x). Does this hold for Go and Rust — languages with compiler-enforced DAGs?

## Method
Same as F96 but adapted per language:
- **Go (etcd)**: K = internal import count per package (cycles impossible)
- **Rust (tokio)**: K = internal `use crate::`/`use super::` + `mod` count (cycles impossible)
- Classified error handling as good/bad per language idioms
- Quality score = good / (good + bad)

## Results

### Go: etcd (N=83 packages)
| Group | Packages | Quality | Correlation |
|-------|----------|---------|-------------|
| LOW-K (K≤1) | 35 | 0.346 | r = +0.114 |
| MID-K (2-4) | 27 | 0.206 | (INVERTED) |
| HIGH-K (K≥5) | 21 | **0.416** | |

**Inverted**: High-K packages have BETTER error handling. Hub packages (etcdserver, v3rpc, client/v3) get more scrutiny. Low-K includes generated protobuf code.

### Rust: tokio (N=342 files)
| Group | Files | Quality | Correlation |
|-------|-------|---------|-------------|
| LOW-K (Q1) | 85 | 0.507 | r = -0.125 |
| MID-K (Q2-3) | 171 | 0.663 | (weak negative) |
| HIGH-K (Q4) | 86 | 0.551 | |

**Weak signal**: Same direction as Python but 4-5x weaker. Quality range compressed (0.41-0.71 vs Python's 0.15-0.85). API-vs-internals is a stronger predictor than coupling.

### Cross-language comparison
| Language | Cycles | Correlation | Quality Range | Mechanism |
|----------|--------|-------------|---------------|-----------|
| Python (redis-py) | 95 | r ~ -0.5 (strong) | 0.15-0.85 | Cycles create untraceable error paths |
| Python (celery) | 30 | r ~ -0.3 (moderate) | 0.46-0.84 | Same, weaker with fewer cycles |
| Go (etcd) | 0 (enforced) | r = +0.11 (inverted) | 0.21-0.42 | DAG = structured coupling, hubs get scrutiny |
| Rust (tokio) | 0 (enforced) | r = -0.13 (weak) | 0.41-0.71 | Result<T,E> creates quality floor |

## Analysis

### The correlation requires import cycles
The key finding: **import cycles are the mechanism, not coupling in general**. In Python, cycles create:
1. Circular error propagation paths that are hard to reason about
2. Broad catches as defensive programming against unknown callers
3. Import-level exception type unavailability
4. Swallowed exceptions in tangled cleanup paths

In DAG-enforced languages, high coupling means structured, unidirectional dependencies — a fundamentally different kind of complexity.

### Language type system compresses the range
Rust's `Result<T,E>` creates a quality floor — you can't silently ignore errors. Even "bad" error handling (`.unwrap()`) is explicit. This compresses the quality distribution and weakens any correlation.

Go sits in between: `if err != nil` is explicit but easy to handle poorly (`return err` without wrapping).

### Confounding: API vs internals
In tokio, the strongest predictor is not coupling but whether code is user-facing (quality 0.82) vs internal machinery (quality 0.31). High-K files happen to be internals, creating a confound.

## Answer
**CONDITIONAL** — The NK-error-handling correlation is cycle-dependent, not coupling-dependent.
- **Languages with cycles (Python)**: Strong correlation (r ~ -0.3 to -0.5). Cycles predict bad error handling.
- **Languages with enforced DAGs (Go, Rust)**: Weak or inverted (r = -0.13 to +0.11). Import count alone does not predict error handling quality.
- **Rust's type system further attenuates**: `Result<T,E>` compresses the quality range.

**Refined principle**: Use NK cycle count (not K_avg alone) as a priority signal for error handling audits. In DAG-enforced languages, look for other complexity signals (API boundary, module depth, test coverage).

## Sources
- etcd v3.5.x: 83 packages, 510 error checks in HIGH-K group
- tokio latest: 342 files, 828 error handling patterns
- redis-py 7.2.1 and celery 5.6.2 (F96 data)
