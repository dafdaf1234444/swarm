# Codex/Copilot Bridge

This repo is a swarm. Read `SWARM.md` for the full protocol.

## Codex/Copilot specifics
- **Parallel agents**: Use sub-agent spawning for independent sub-tasks (Codex: multi-agent mode; Copilot: /fleet or coding agent).
- **Entry**: This file auto-loads in Codex CLI and GitHub Copilot. `SWARM.md` is the canonical protocol.
- **Swarm signaling**: Always try to inform the swarm with intent/progress/blockers/next-step updates via `tasks/NEXT.md`, `tasks/SWARM-LANES.md`, or inter-swarm bulletins when relevant.
- **Commit quality**: Install hooks once with `bash tools/install-hooks.sh`; before commit, ensure `bash tools/check.sh --quick` passes and use `[S<N>] what: why`.
- **Safety-first collaboration**: Prefer reversible, scope-limited changes; avoid destructive or out-of-scope side effects; if risk or authority is unclear, ask the human before proceeding.
- **Human interaction (minimum-by-default)**:
  - Ask the human only when blocked by missing authority, inaccessible data, or irreversible preference decisions.
  - Before asking, check `memory/HUMAN.md` and `tasks/HUMAN-QUEUE.md` for existing directives/answers.
  - If the answer already exists, do not ask again; proceed using recorded state.
  - Every new human question must be recorded in `tasks/HUMAN-QUEUE.md` as an `HQ-N` entry at ask time.
  - When answered, move it to `## Answered` with date/session and the action taken.

## Multi-tool compatibility (F118)
Core state (beliefs, lessons, principles, frontiers) is tool-agnostic markdown + git.
Entry files: `CLAUDE.md` (Claude Code), `AGENTS.md` (Codex/Copilot), `.cursorrules` (Cursor), `GEMINI.md` (Gemini), `.windsurfrules` (Windsurf), `.github/copilot-instructions.md` (Copilot).
Each bridge file loads `SWARM.md` and adds tool-specific instructions.
