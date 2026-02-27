# Domain: Protocol Engineering
Topic: Protocol design, adoption, enforcement, and evolution as structural isomorphisms for swarm reliability, portability, and coordination quality.
Beliefs: (candidate only; no formal B-PRO* entries in `beliefs/DEPS.md` yet)
Lessons: L-023, L-106, L-138, L-209, L-252
Frontiers: F-PRO1, F-PRO2, F-PRO3
Experiments: experiments/evolution/, experiments/information-science/, experiments/game-theory/
Load order: CLAUDE.md -> beliefs/CORE.md -> this file -> INDEX.md -> memory/INDEX.md -> tasks/FRONTIER.md

## Domain filter
Only protocol concepts with direct structural isomorphisms to swarm operation qualify. Isomorphism requires: same enforcement mechanism, same failure mode, and an actionable protocol implication.

## Core isomorphisms

| Protocol concept | Swarm parallel | Isomorphism type | Status |
|------------------|----------------|------------------|--------|
| Contract schema | Lane + intake required fields | Interface discipline | OBSERVED |
| Adoption decay | Explicit tags regress without guard checks | Reliability drift | OBSERVED |
| Protocol mutation cadence | Too-frequent mutation raises coordination overhead | Stability tradeoff | OBSERVED |
| Bridge parity | Tool-specific entry drift weakens cross-tool swarmability | Portability control | OBSERVED |
| Minimal viable protocol | Overgrown protocol reduces pickup speed | Complexity control | THEORIZED |
