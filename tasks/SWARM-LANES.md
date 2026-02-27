# Swarm Lanes — Multi-Agent / Multi-PR / Multi-LLM / Multi-Platform
Purpose: coordinate concurrent work streams so independent agents can ship in parallel without merge collisions.

Use this when work is expected to produce multiple branches or pull requests, or when the run spans mixed models/platforms.

## Rules
- Append-only log. Do not rewrite old rows.
- One lane ID per mergeable objective.
- Update lane state by appending a newer row for the same lane ID.
- `Scope-Key` must represent the primary write surface (for example `tools/maintenance.py` or `docs/protocol-core`).
- Use `Etc` for extra axes not covered by fixed columns (`runtime=wsl`, `dataset=...`, `tool=codex`, etc.).

## Status values
- Active: `CLAIMED`, `ACTIVE`, `BLOCKED`, `READY`
- Closed: `MERGED`, `ABANDONED`

## Lane Log (append-only)
| Date | Lane | Session | Agent | Branch | PR | Model | Platform | Scope-Key | Etc | Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

