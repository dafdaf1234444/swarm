<!-- claude_md_version: 0.9 | 2026-02-28 | expert-dispatch-default (F-EXP7) -->
# Claude Code Bridge

This repo is a swarm. Read `SWARM.md` for the full protocol.

## Claude Code specifics
- **Parallel agents**: Use Task tool for independent sub-tasks.
- **Spawn**: Task tool IS the spawn mechanism. Sub-agents receive `beliefs/CORE.md` + `memory/INDEX.md` + their task.
- **Swarm signaling**: Always try to inform the swarm with intent/progress/blockers/next-step updates via `tasks/NEXT.md`, `tasks/SWARM-LANES.md`, or inter-swarm bulletins when relevant.
- **Hooks**: Install with `bash tools/install-hooks.sh` (pre-commit runs `bash tools/check.sh --quick`; commit-msg enforces `[S<N>] what: why`). See `.claude/settings.json`.
- **Entry**: This file auto-loads in Claude Code. `SWARM.md` is the canonical protocol.
- **Safety-first collaboration**: Prefer reversible, scope-limited changes; avoid destructive or out-of-scope side effects; if risk or authority is unclear, ask the human before proceeding.
- **Human interaction (minimum-by-default)**:
  - Ask the human only when blocked by missing authority, inaccessible data, or irreversible preference decisions.
  - Before asking, check `memory/HUMAN.md` and `tasks/HUMAN-QUEUE.md` for existing directives/answers.
  - If the answer already exists, do not ask again; proceed using recorded state.
  - Every new human question must be recorded in `tasks/HUMAN-QUEUE.md` as an `HQ-N` entry at ask time.

## Minimum Swarmed Cycle
- Choose and log a check mode (`objective`/`historian`/`verification`/`coordination`/`assumption`) for active lane updates.
- Declare expectation before acting and record the diff after acting.
- Treat positive, negative, and null outcomes as first-class evidence.
- **Expert dispatch first** (F-EXP7): run `python3 tools/dispatch_optimizer.py` — if a top-3 domain has no active DOMEX lane, open one and work as that domain's expert. Expert mode is the default work mode, not a fallback. Target ≥15% expert utilization.
- Default to executing active swarm work from `tasks/NEXT.md` and `tasks/SWARM-LANES.md`; if not executed, mark explicit `blocked`/`reassigned`/`abandoned` with next action.
- Keep bridge files synchronized: if one bridge gains protocol-critical guidance, mirror it across all bridge entry files in the same session.

## Multi-tool compatibility (F118)
Core state (beliefs, lessons, principles, frontiers) is tool-agnostic markdown + git.
Entry files: `CLAUDE.md` (Claude Code), `AGENTS.md` (Codex/Copilot), `.cursorrules` (Cursor), `GEMINI.md` (Gemini), `.windsurfrules` (Windsurf), `.github/copilot-instructions.md` (Copilot).
Each bridge file loads `SWARM.md` and adds tool-specific instructions.
