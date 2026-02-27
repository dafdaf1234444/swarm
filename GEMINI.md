# Gemini Bridge

This repo is a swarm. Read `SWARM.md` for the full protocol.

## Gemini specifics
- **Parallel agents**: Gemini CLI does not yet support native sub-agent spawning. Work sequentially. For parallelism, spawn separate terminal sessions manually.
- **Swarm signaling**: Always try to inform the swarm with intent/progress/blockers/next-step updates via `tasks/NEXT.md`, `tasks/SWARM-LANES.md`, or inter-swarm bulletins when relevant.
- **Commit quality**: Install hooks once with `bash tools/install-hooks.sh`; before commit, run `bash tools/check.sh --quick` and use `[S<N>] what: why`.
- **Entry**: This file auto-loads in Gemini Code Assist. `SWARM.md` is the canonical protocol.
- **Safety-first collaboration**: Prefer reversible, scope-limited changes; avoid destructive or out-of-scope side effects; if risk or authority is unclear, ask the human before proceeding.

## Multi-tool compatibility (F118)
Core state (beliefs, lessons, principles, frontiers) is tool-agnostic markdown + git.
Entry files: `CLAUDE.md` (Claude Code), `AGENTS.md` (Codex/Copilot), `.cursorrules` (Cursor), `GEMINI.md` (Gemini), `.windsurfrules` (Windsurf), `.github/copilot-instructions.md` (Copilot).
Each bridge file loads `SWARM.md` and adds tool-specific instructions.
