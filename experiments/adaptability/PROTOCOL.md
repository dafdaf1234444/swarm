# Experiment: Adaptability Stress Tests

## Hypothesis
The swarm is anti-fragile — its swarmability score trends upward after recovering from disruptions, and it can modify its own beliefs, protocols, and storage when challenged.

## Design
Five "shock" sessions, each introducing a specific disruption. The swarm must adapt. Swarmability score is recorded before and after each shock.

### Shock 1: Belief Contradiction
Target: B1 (most-connected belief — B2 and B7 depend on it).
A plausible contradiction is injected via `shocks/shock1.md`. The session reads the shock, evaluates the evidence, and either updates B1 and cascades changes through dependents, or refutes the contradiction with counter-evidence. Either way, the system must demonstrate it can process contradictory input, not ignore it.

### Shock 2: Protocol Inadequacy
A task is injected via `shocks/shock2.md` that the current CLAUDE.md protocol cannot handle. The session must recognize the gap, propose a minimal protocol amendment, implement it, and complete the task.

### Shock 3: Memory Overload
5000+ tokens of dense technical content injected via `shocks/shock3.md`. The swarm must integrate this information while keeping mandatory files under 450 lines combined.

### Shock 4: Context Amnesia
INDEX.md and CORE.md are backed up then deleted. The session starts with only CLAUDE.md and raw files. It must reconstruct both from scratch. Reconstructed versions are compared against backups.

### Shock 5: Storage Evolution
An argument is injected via `shocks/shock5.md` that DEPS.md format is insufficient. The session must evaluate, decide, implement any changes, update the validator, and migrate data.

## Tracking

| Shock | Swarmability Before | Swarmability After | Beliefs Changed | Protocol Changed | Storage Changed | Notes |
|-------|--------------------|--------------------|-----------------|------------------|-----------------|-------|
| 1     |                    |                    |                 |                  |                 |       |
| 2     |                    |                    |                 |                  |                 |       |
| 3     |                    |                    |                 |                  |                 |       |
| 4     |                    |                    |                 |                  |                 |       |
| 5     |                    |                    |                 |                  |                 |       |

## Success Criteria
- Swarmability never drops below 40 after recovery
- Trend is upward across the 5 shocks (anti-fragile)
- At least 1 protocol or storage change happens (adaptable, not rigid)
- No contradicted belief is left in its old state after a shock (integrity)

## Results
[FILL IN AFTER ALL 5 SHOCKS]
