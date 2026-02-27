# Domain: Control Theory
Topic: Feedback loops, stability margins, gain tuning, state estimation, and disturbance rejection as structural isomorphisms for swarm calibration, maintenance policy, and coordination reliability.
Beliefs: (candidate only; no formal B-CTL* entries in `beliefs/DEPS.md` yet)
Lessons: L-216 (state-sync automation), L-223 (expect-act-diff), L-242 (rising sawtooth), L-257 (quality dimensions and execution pattern)
Frontiers: F-CTL1, F-CTL2, F-CTL3
Experiments: experiments/control-theory/
Load order: CLAUDE.md -> beliefs/CORE.md -> this file -> INDEX.md -> memory/INDEX.md -> tasks/FRONTIER.md

## Domain filter
Only control-theory concepts with structural isomorphisms to swarm operation qualify. Isomorphism requires: same formal dynamics, same failure modes, and an actionable swarm implication.

## Core isomorphisms

| Control concept | Swarm parallel | Isomorphism type | Status |
|----------------|----------------|------------------|--------|
| Negative feedback loop | Expect -> act -> diff -> correction loop (F123) | Closed-loop regulation | OBSERVED |
| Open-loop control | Sessions that skip orient/check operate without live feedback | Disturbance vulnerability | OBSERVED |
| Gain tuning | Threshold tuning in maintenance and spawn policies (for example DUE/URGENT and P-119) | Controller parameterization | OBSERVED |
| Integral windup | Backlog and overhead accumulate when unresolved drift is carried forward | Saturation/overshoot parallel | OBSERVED |
| State estimation | NEXT + SWARM-LANES + artifacts approximate latent system state | Partial observability | THEORIZED |

