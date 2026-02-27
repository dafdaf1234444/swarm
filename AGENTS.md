# Codex/Copilot Bridge

This repo is a swarm. Read `SWARM.md` for the full protocol.

## Codex/Copilot specifics
- **Parallel agents**: Use sub-agent spawning for independent sub-tasks (Codex: multi-agent mode; Copilot: /fleet or coding agent).
- **Entry**: This file auto-loads in Codex CLI and GitHub Copilot. `SWARM.md` is the canonical protocol.

## Multi-tool compatibility (F118)
Core state (beliefs, lessons, principles, frontiers) is tool-agnostic markdown + git.
Entry files: `CLAUDE.md` (Claude Code), `AGENTS.md` (Codex/Copilot), `.cursorrules` (Cursor), `GEMINI.md` (Gemini), `.windsurfrules` (Windsurf), `.github/copilot-instructions.md` (Copilot).
Each bridge file loads `SWARM.md` and adds tool-specific instructions.
