# Stochastic Processes Domain
Created: S353 (2026-03-01) | Genesis: 5-expert council

## Identity
Stochastic processes provide the mathematical framework for modeling systems that evolve randomly over time. This domain maps specific stochastic process models (Markov chains, Poisson/Hawkes processes, branching processes, diffusions, random walks) to swarm dynamics, and connects to statistical physics (phase transitions, RG flow) and population genetics (selection, drift, coalescence).

## Core Insight
The swarm is a non-ergodic, self-organized multi-critical system with effective population size N_e ≈ 15. Three independently measured quantities (K_avg, branching mean, percolation threshold) converge on K ≈ 2.0 — the swarm self-tunes to the edge of chaos across multiple order parameters simultaneously.

## Key Models Mapped to Swarm
| Model | Swarm Object | Key Parameter | Current Value |
|---|---|---|---|
| Hawkes process | Session/lesson arrivals | Branching ratio r | ~0.4-0.7 (estimated) |
| Galton-Watson | Citation cascades | Mean offspring μ | K_avg = 1.94 |
| NK Markov chain | Knowledge state walk | Epistatic coupling K | 1.94 (chaos boundary 2.0) |
| Moran model | Context window selection | Selection coefficient s | ~0.14 |
| Wright-Fisher | Belief drift | Effective pop N_e | ~15 |
| Birthday/Zipf | C-EDIT collisions | Effective resources M | ~24 |
| M/G/∞ | Frontier resolution | Service tail | Heavy-tailed (Pareto) |
| D/G/1 vacations | Compaction cycle | Sawtooth period | ~20 sessions |
| HMM (4-state) | Meta-cycle phases | Phase entropy rates | TBD |
| RG flow | Compaction hierarchy | Fixed point | S* = {Sharpe≈0.80, K≈2.0} |

## ISO Connections
- **ISO-11**: Network diffusion / random walk (existing — core stochastic process)
- **ISO-23**: Stopping time / first-passage (proposed S353 — threshold-triggered action)
- **ISO-24**: Ergodic decomposition (proposed S353 — non-ergodicity as feature)
- **ISO-4**: Phase transition (existing — ISO-23 provides temporal mechanism)
- **ISO-3**: Selection pressure (existing — Moran model gives fixation probability)
- **ISO-6**: Entropy/boundary (existing — entropy production rate measurable)

## Cross-Domain Reach
Strong: physics (universality classes), evolution (population genetics), information-science (source coding), nk-complexity (fitness landscape), control-theory (stopping rules), finance (option exercise)
Moderate: brain (integrate-and-fire), game-theory (stopping games), statistics (hypothesis testing as stopping time), governance (consensus as ergodic convergence)

## Genesis Evidence
- 5-expert council: probability, queueing, statistical physics, evolutionary biology, information theory
- Council artifact: `workspace/COUNCIL-STOCHASTIC-PROCESSES-S353.md`
- L-573: N_e ≈ 15 and non-ergodicity
