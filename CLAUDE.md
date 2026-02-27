<!-- claude_md_version: 0.8 | 2026-02-27 | safety-first collaboration mandate -->
# Claude Code Bridge

This repo is a swarm. Read `SWARM.md` for the full protocol.

## Claude Code specifics
- **Parallel agents**: Use Task tool for independent sub-tasks.
- **Spawn**: Task tool IS the spawn mechanism. Sub-agents receive `beliefs/CORE.md` + `memory/INDEX.md` + their task.
- **Swarm signaling**: Always try to inform the swarm with intent/progress/blockers/next-step updates via `tasks/NEXT.md`, `tasks/SWARM-LANES.md`, or inter-swarm bulletins when relevant.
- **Hooks**: Install with `bash tools/install-hooks.sh` (pre-commit runs `bash tools/check.sh --quick`; commit-msg enforces `[S<N>] what: why`). See `.claude/settings.json`.
- **Entry**: This file auto-loads in Claude Code. `SWARM.md` is the canonical protocol.
- **Safety-first collaboration**: Prefer reversible, scope-limited changes; avoid destructive or out-of-scope side effects; if risk or authority is unclear, ask the human before proceeding.

## Multi-tool compatibility (F118)
Core state (beliefs, lessons, principles, frontiers) is tool-agnostic markdown + git.
Entry files: `CLAUDE.md` (Claude Code), `AGENTS.md` (Codex/Copilot), `.cursorrules` (Cursor), `GEMINI.md` (Gemini), `.windsurfrules` (Windsurf), `.github/copilot-instructions.md` (Copilot).
Each bridge file loads `SWARM.md` and adds tool-specific instructions.
