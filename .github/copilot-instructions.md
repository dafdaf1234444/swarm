<!-- bridge_version: 1.1 | 2026-03-24 | S540: dedup — shared items moved to SWARM.md -->
# Copilot Bridge

This repo uses a multi-session protocol. Read `SWARM.md` for the full protocol.
See `SWARM.md` §Common Bridge Items for signaling, soft-claim, contract validation, concurrent-safe commit, safety, and human interaction protocols.
See `SWARM.md` §Minimum Cycle for the orient→act→compress→handoff loop.

## Swarm Signaling
- Follow `SWARM.md` §Swarm Signaling and §Common Bridge Items for swarm signaling: post structured updates with `python3 tools/swarm_signal.py post ...` and keep `tasks/NEXT.md`, `tasks/SWARM-LANES.md`, and related shared state current while you work.

## Minimum Swarmed Cycle
- Follow `SWARM.md` §Minimum Cycle: run `python3 tools/orient.py`, `python3 tools/task_order.py`, `python3 tools/question_gen.py`, and `python3 tools/dispatch_optimizer.py`; check recent commits before acting; declare `check_mode` plus expectation; act, diff, and compress; then finish with `python3 tools/sync_state.py`, `python3 tools/validate_beliefs.py`, `python3 tools/cell_blueprint.py save`, and `git push`.
- If the preferred runtime is unavailable, use the documented PowerShell or shell fallbacks from `SWARM.md`.

## Copilot specifics
- **Parallel agents**: Copilot coding agent supports sub-agent architecture with Mission Control orchestration.
- **Branch restriction**: Copilot coding agent pushes to `copilot/*` branches only — cannot push directly to main/master. Create PRs for merge.
- **Entry**: This file auto-loads in GitHub Copilot (workspace-wide). `SWARM.md` is the canonical protocol.
- **Shell**: Full terminal access via Copilot CLI. Agent mode supports self-healing iteration on command failures.

## Multi-tool compatibility (F118)
Core state (beliefs, lessons, principles, frontiers) is tool-agnostic markdown + git.
Entry files: `CLAUDE.md` (Claude Code), `AGENTS.md` (Codex/Copilot), `.cursor/rules/swarm.mdc` + `.cursorrules` (Cursor), `GEMINI.md` (Gemini), `.windsurfrules` (Windsurf), `.github/copilot-instructions.md` (Copilot).
Each bridge file loads `SWARM.md` and adds tool-specific instructions.
