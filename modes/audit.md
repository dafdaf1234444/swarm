# Mode: Audit
Load when: health checks, validating beliefs, testing theorized beliefs, system review.

## Additional rules
1. **Expect-act-diff + check mode**: Log `check_mode`, expectation, and diff in `tasks/NEXT.md` or `tasks/SWARM-LANES.md` (see `memory/EXPECT.md`).
2. **Belief throttle**: If >60% of beliefs are `theorized`, your primary task is testing one. Pick the most important theorized belief and design a test with binary pass/fail.
3. **Run health check**: Use indicators from `memory/HEALTH.md`.
4. **Verify dependency accuracy**: Cross-check DEPS.md against actual file references.

## Session output
- Validator results (before and after)
- Beliefs upgraded or disproven
- NEXT.md pointing forward
- Meta-swarm reflection (friction/improvement + action or blocker)
