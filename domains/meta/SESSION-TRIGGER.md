# Session Trigger Manifest

Machine-readable session-trigger conditions for autonomous swarm initiation.
Updated by orient.py; read by automation layer.

## Schema
Each trigger: condition | urgency | trigger_source | last_checked | threshold

## Active Triggers

### Infrastructure Triggers
- **maintenance_due**: Any DUE maintenance items exist | HIGH | maintenance.py | 2026-03-01T03:20:00Z | count > 0
- **compaction_needed**: Proxy-K drift >15% or lesson count >500 | HIGH | proxy_k.py | 2026-03-01T03:20:00Z | drift > 15% OR lessons > 500
- **stale_tools**: Infrastructure components >50 sessions without evolution | MEDIUM | orient.py | 2026-03-01T03:20:00Z | count > 10
- **periodics_due**: Periodic maintenance overdue >2x cadence | MEDIUM | maintenance.py | 2026-03-01T03:20:00Z | overdue_ratio > 2.0

### Knowledge Triggers
- **frontier_stagnation**: Open frontiers >30 sessions without progress | MEDIUM | frontier_monitor.py | 2026-03-01T03:20:00Z | max_age > 30
- **challenge_backlog**: CHALLENGES.md entries >10 sessions old | MEDIUM | challenges.py | 2026-03-01T03:20:00Z | count > 0 AND age > 10
- **belief_staleness**: Core beliefs not validated >100 sessions | LOW | validate_beliefs.py | 2026-03-01T03:20:00Z | max_age > 100
- **knowledge_overflow**: Lessons created but not compacted >20 in 5 sessions | MEDIUM | lesson_monitor.py | 2026-03-01T03:20:00Z | rate > 4/session

### Expert Triggers
- **dispatch_imbalance**: Top-3 domains without active DOMEX lanes | HIGH | dispatch_optimizer.py | 2026-03-01T03:20:00Z | unclaimed_top3 > 0
- **expert_starvation**: No expert utilization >5 sessions | MEDIUM | expert_monitor.py | 2026-03-01T03:20:00Z | sessions_since_expert > 5

### Human Interface Triggers
- **human_queue**: Unanswered human signals >3 sessions old | HIGH | human_queue.py | 2026-03-01T03:20:00Z | count > 0 AND age > 3
- **human_signal_backlog**: HUMAN-SIGNALS.md >20 unprocessed entries | MEDIUM | signal_processor.py | 2026-03-01T03:20:00Z | unprocessed > 20

### Crisis Triggers
- **git_corruption**: Repository integrity check fails | CRITICAL | git_check.py | 2026-03-01T03:20:00Z | status != "clean"
- **belief_contradiction**: Core philosophy contradicts measured evidence | HIGH | belief_validator.py | 2026-03-01T03:20:00Z | contradictions > 0
- **cascade_failure**: Multiple critical tools failing simultaneously | CRITICAL | cascade_detector.py | 2026-03-01T03:20:00Z | failing_tools > 3

## Urgency Levels
- **CRITICAL**: Immediate session required (swarm integrity at risk)
- **HIGH**: Session needed within 1 hour
- **MEDIUM**: Session beneficial within 6 hours
- **LOW**: Session optional, schedule when convenient

## Integration Points
- orient.py updates this file each run
- Automation layer reads highest urgency trigger
- Human dashboard surfaces top 3 triggers
- External schedulers query for session_needed status

## Autonomous Session Path
1. External monitor queries SESSION-TRIGGER.md
2. If urgency ≥ HIGH: initiate swarm session
3. Session runs orient.py → updates triggers
4. Session acts on highest priority trigger
5. Session updates trigger status before handoff