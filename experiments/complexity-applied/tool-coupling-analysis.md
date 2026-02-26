# NK Analysis: Swarm Tool Coupling

## Summary
Applied Kauffman NK landscapes and Simon near-decomposability to the swarm's 7 Python tools.

## NK Parameters
- **N** = 7 tools (validate_beliefs, swarm_test, merge_back, colony, swarm_integration_test, bulletin, session_tracker)
- **K** = 1.29 average inter-tool dependencies
- **K/N** = 0.18 (well below 0.3 near-decomposability threshold)

## Coupling Map
```
colony.py (orchestrator)
  ├── swarm_test.py (spawn/evaluate)
  │   └── validate_beliefs.py (health checks)
  └── merge_back.py (intelligence extraction)

swarm_integration_test.py (test harness)
  └── validate_beliefs.py

[Independent]
  ├── bulletin.py (side channel)
  └── session_tracker.py (metrics)
```

## Simon Tiers
| Tier | Tools | Role |
|------|-------|------|
| 1. Core | validate_beliefs | Integrity checks |
| 2. Lifecycle | swarm_test, merge_back | Child swarm management |
| 3. Orchestration | colony | Multi-child coordination |
| 4. Testing | swarm_integration_test | End-to-end validation |
| 5. Telemetry | bulletin, session_tracker | Non-blocking observation |

## Assessment
- **Near-decomposable**: Yes (K/N = 0.18 < 0.3)
- **Cyclomatic complexity**: 0 (no circular deps)
- **Evolvability**: HIGH (add tools without global refactor)
- **Bottleneck**: validate_beliefs.py (3 callers — hub node)
- **Coupling method**: subprocess calls (loose), not Python imports (tight)
