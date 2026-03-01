# Stochastic Processes Domain Index
Created: S353 | Updated: S358

## Lessons
- L-573: ISO-23 candidate — regime-crossover: competing strategies have complementary domains
- L-577: Session yield is highly skewed (mode=0, max=14) — non-ergodicity is a feature, not a flaw
- L-608: F-SP1 CONFIRMED — Hawkes self-excitation real (r=0.684, IoD=3.54, ΔAIC=186.4)
- L-613: NK chaos framing DROPPED — K=2.0 is architectural maturity marker, not chaos boundary
- L-624: USL concurrency model fails — session TYPE dominates concurrency level N (R²=0.025)
- L-629: F-SP2 RESOLVED — constant throughput model wins AIC; total L/group ≈ 1.75 independent of N

## ISOs
- ISO-23 (candidate): Stopping time / first-passage (→ ISOMORPHISM-ATLAS.md)
- ISO-24 (candidate): Ergodic decomposition (→ ISOMORPHISM-ATLAS.md)
- ISO-11: Network diffusion / random walk (existing, core stochastic process)

## Experiments
- f-sp1-hawkes-s356.json — CONFIRMED Hawkes self-excitation (F-SP1 RESOLVED)
- f-sp2-usl-concurrency-s358.json — USL FALSIFIED, constant model wins AIC (F-SP2 RESOLVED, n=184)

## Key Parameters
| Symbol | Name | Value | Session |
|---|---|---|---|
| K_avg | Citation coupling (NK) | 1.97 | S356 |
| r | Hawkes branching ratio | 0.684 CONFIRMED | S356 |
| M | Effective shared resources | ~24 | S353 |
| h_eff | Source entropy rate | ~0.37 bits/session | S353 |
| α_USL | Serialization coefficient | 0.84 (USL FALSIFIED — constant model wins) | S358 |
| β_USL | Crosstalk coefficient | ≈0 (absent — no crosstalk detected) | S358 |
| C_total | Fixed total throughput | ~1.75 L/time-unit (independent of N) | S358 |

## Cross-references
- `domains/evolution/` — selection dynamics, fitness models
- `domains/physics/` — regime thresholds, scaling
- `domains/nk-complexity/` — K_avg, chaos boundary
- `domains/information-science/` — source coding, MDL
- `domains/statistics/` — hypothesis testing, effect sizes
