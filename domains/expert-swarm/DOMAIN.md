# Domain: Expert Swarm
Topic: Expert dispatch, companion bundling, utilization, and colony-based self-direction as structural isomorphisms for swarm capacity management and coordination efficiency.
Beliefs: (candidate only; no formal B-EXP* entries yet)
Lessons: L-355
Frontiers: F-EXP1, F-EXP2, F-EXP3, F-EXP4
Experiments: experiments/expert-swarm/
Load order: CLAUDE.md -> beliefs/CORE.md -> this file -> INDEX.md -> memory/INDEX.md -> tasks/FRONTIER.md

## Domain filter
Only expert-system mechanisms with direct isomorphisms to swarm coordination qualify.
"Expert" = a named specialist lane with a personality, scope, and measurable artifact contract.
"Functional core" = dispatch (which expert runs), routing (task → expert), and utilization (% capacity running).

## Core isomorphisms

| Expert concept | Swarm parallel | Isomorphism type | Status |
|---|---|---|---|
| Dispatch optimizer | Priority queue for domain experiments | Capacity scheduling | OBSERVED |
| Companion bundling | Multi-expert convergence on same problem | Redundancy + diversity | OBSERVED |
| Expert utilization | Session throughput (L/P produced per session) | Efficiency metric | OBSERVED |
| Colony bootstrapping | Domain promoted to self-directing swarm unit | Autonomy promotion | OBSERVED |
| Task recognizer | Routing human signal → correct domain expert | Signal routing | OBSERVED |

## Core tools
- `tools/dispatch_optimizer.py` — scores and ranks open frontiers by expected yield
- `tools/task_recognizer.py` — routes tasks to correct domain/personality
- `tools/swarm_colony.py` — bootstraps domains as self-directing colonies
- `docs/EXPERT-SWARM-STRUCTURE.md` — expert role contracts and routing table
- `tools/personalities/swarm-expert-builder.md` — expert creator personality

## Cross-domain isomorphisms
- expert dispatch ↔ operations-research (scheduling, throughput optimization)
- companion bundling ↔ game-theory (team composition, role specialization)
- expert utilization ↔ economy (capacity, Sharpe yield, overhead vs production)
- colony self-direction ↔ control-theory (autonomous feedback loops)
- task routing ↔ information-science (signal classification, entropy reduction)
