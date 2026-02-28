# Mode: Build
Load when: writing code, creating tools, producing external artifacts.

## Additional rules
1. **Expect-act-diff + check mode**: Log `check_mode`, expectation, and diff in `tasks/NEXT.md` or `tasks/SWARM-LANES.md` (see `memory/EXPECT.md`).
2. **No destructive compression**: Don't delete lesson files unless validator confirms supported beliefs are `observed`.
3. **Test what you build**: Binary pass/fail before committing.
4. **External artifact required**: Session must produce working code or validated data, not just documentation.

## Session output
- Working code/tool committed
- Test results documented
- NEXT.md pointing forward
- Meta-swarm reflection (friction/improvement + action or blocker)
