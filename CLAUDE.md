<!-- claude_md_version: 0.7 | 2026-02-27 | F118: delegates to SWARM.md -->
# Claude Code Bridge

This repo is a swarm. Read `SWARM.md` for the full protocol.

## Claude Code specifics
- **Parallel agents**: Use Task tool for independent sub-tasks.
- **Spawn**: Task tool IS the spawn mechanism. Sub-agents receive `beliefs/CORE.md` + `memory/INDEX.md` + their task.
- **Hooks**: Pre-commit validates beliefs. See `.claude/settings.json`.
- **Entry**: This file auto-loads in Claude Code. `SWARM.md` is the canonical protocol.

## Multi-tool compatibility (F118)
Core state (beliefs, lessons, principles, frontiers) is tool-agnostic markdown + git.
Entry files: `CLAUDE.md` (Claude Code), `AGENTS.md` (Codex/Copilot), `.cursorrules` (Cursor), `GEMINI.md` (Gemini), `.windsurfrules` (Windsurf), `.github/copilot-instructions.md` (Copilot).
Each bridge file loads `SWARM.md` and adds tool-specific instructions.
