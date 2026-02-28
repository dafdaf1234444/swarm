# Mode: Repair
Load when: fixing broken beliefs, resolving conflicts, cascading dependency changes, handling contradictions.

## Additional rules
1. **Expect-act-diff + check mode**: Log `check_mode`, expectation, and diff in `tasks/NEXT.md` or `tasks/SWARM-LANES.md` (see `memory/EXPECT.md`).
2. **Adaptability over preservation**: When new info contradicts existing beliefs:
   - Update or kill the contradicted belief (record why)
   - Walk the dependency chain in DEPS.md — update everything downstream
   - If contradiction implies a storage/protocol change, propose in FRONTIER.md
   - NEVER ignore contradictory evidence to preserve consistency
3. **Evidence beats assertion**: Use `beliefs/CONFLICTS.md` protocol for semantic conflicts.

## Session output
- Updated DEPS.md with cascaded changes
- Conflict resolution documented
- NEXT.md pointing forward
- Meta-swarm reflection (friction/improvement + action or blocker)
