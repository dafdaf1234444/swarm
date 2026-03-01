# Swarm Lanes — Multi-Agent / Multi-PR / Multi-LLM / Multi-Platform
Purpose: coordinate concurrent work streams so independent agents can ship in parallel without merge collisions.

Use this when work is expected to produce multiple branches or pull requests, or when the run spans mixed models/platforms.

## Rules
- Append-only log. Do not rewrite old rows.
- One lane ID per mergeable objective.
- Update lane state by appending a newer row for the same lane ID.
- No parked active lanes: `READY`/`CLAIMED`/`ACTIVE` rows must get next-session progress (`progress`/`blocked`/`next_step`) or be closed/reassigned.
- `Scope-Key` must represent the primary write surface (for example `tools/maintenance.py` or `docs/protocol-core`).
- Use `Etc` for extra axes not covered by fixed columns (`runtime=wsl`, `dataset=...`, `tool=codex`, etc.).
- For active lanes (`CLAIMED`/`ACTIVE`/`BLOCKED`/`READY`), `Etc` must include:
  `setup=<swarm-setup>` (host/tool/runtime profile), `focus=<scope>` (`global` or a concentrated subsystem),
  `available=<yes|no|partial>`, `blocked=<none|reason>`, `next_step=<action>`,
  `human_open_item=<none|HQ-N>`, `expect=<predicted-outcome>` (declare before acting), and
  `artifact=<path>` (commit to what will be produced). Use `python3 tools/open_lane.py` to create lanes
  with these fields enforced automatically (F-META1 enforcement, S331).
- For assignment events (`READY`/`CLAIMED`), include dispatch provenance in `Etc` (`dispatch=<source>`), and add `slot=<n>` and/or `reassigned_from=<lane|slot>` when applicable.
- For active lanes with domain focus (`focus=domains/<domain>` or `Scope-Key` under `domains/<domain>/...`), `Etc` must also include:
  `domain_sync=<queued|syncing|synced|stale|n/a>` and `memory_target=<domain memory path being synchronized>`.
- When multiple setups are active at once, keep at least one lane with `focus=global` so cross-setup coordination stays explicit.

## Status values
- Active: `CLAIMED`, `ACTIVE`, `BLOCKED`, `READY`
- Closed: `MERGED`, `ABANDONED`

## Lane Log (append-only)
| Date | Lane | Session | Agent | Branch | PR | Model | Platform | Scope-Key | Etc | Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
















| 2026-02-28 | DOMEX-META-S322 | 325 | claude-code | - | - | claude-sonnet-4-6 | close_lane.py | close_lane.py | setup=codex-windows+powershell+bash; focus=domains/meta; personality=domain-expert; intent=dispatch-optimizer-top3; frontier=F-META1; dispatch=dispatch_optimizer-s322; progress=queued; available=yes; blocked=none;  human_open_item=none; domain_sync=queued; memory_target=domains/meta/tasks/FRONTIER.md; runtime=wsl; historian_check=tagged; session_anchor=S322, progress=closed, progress=closed, progress=closed, next_step=none | MERGED | F-META1 contract audit executed S325: 64% required compliance (up from 1% S249). progress/intent are top gaps; expect/actual/artifact at 0% — embed in dispatch template. L-434. |
| 2026-02-28 | DOMEX-LNG-S313 | 325 | claude-code | - | - | claude-sonnet-4-6 | close_lane.py | close_lane.py | setup=codex-windows+powershell+bash; focus=domains/linguistics; personality=domain-expert; intent=dispatch-optimizer-top3; frontier=F-LNG1/F-LNG2; dispatch=dispatch_optimizer-s313; progress=queued; available=yes; blocked=none;  human_open_item=none; domain_sync=queued; memory_target=domains/linguistics/tasks/FRONTIER.md; historian_check=tagged; session_anchor=S322, progress=closed, progress=closed, progress=closed, next_step=none | ABANDONED | No execution in 4+ sessions. F-LNG1 already confirmed at n=359 (S313). F-LNG2 forward validation deferred — re-open when linguistics focus returns. L-432 (F-LNG1 n=400) remains candidate. |

| 2026-03-01 | DOMEX-META-S339 | S186 | claude-code | master | - | claude-sonnet-4-6 | close_lane.py | claude-code+wsl | setup=claude-code+wsl; focus=global; personality=domain-expert; intent=advance-F-META1; check_mode=objective; frontier=F-META1; expect=T4 parse_active_principle_ids stub replacement saves ~163t; compact.py clears T0-T3 drift; actual=TBD; diff=TBD; artifact=experiments/meta/f-meta-t4-phase1-s339.json; progress=active; available=yes; blocked=none;  human_open_item=none; domain_sync=queued; memory_target=domains/meta/tasks/FRONTIER.md, progress=closed, next_step=none | MERGED | parse_active_principle_ids stub confirmed (-13L, concurrent S339 compact already applied). lanes_compact archived 9 stale rows (bloat 75%→0%). action-board refreshed. maintenance.py 1,825L. |
| 2026-03-01 | DOMEX-PHY-GENESIS | S186 | claude-code | master | - | claude-sonnet-4-6 | close_lane.py | claude-code+wsl | setup=claude-code+wsl; focus=global; personality=domain-expert; intent=swarm-work; check_mode=objective; expect=Map universe genesis against all 17 ISO entries; determine PHIL-15 integrate-vs-analyze; identify novel ISO candidate from symmetry-breaking cascade; actual=TBD; diff=TBD; artifact=experiments/physics/f-phy6-universe-genesis-s340.json; progress=active; available=yes; blocked=none;  human_open_item=none; domain_sync=queued; memory_target=domains/physics, progress=closed, next_step=none | MERGED | 11/17 ISOs mapped to cosmological genesis. PHIL-15=Analyze. ISO-18 candidate: symmetry-breaking cascade. Atlas v1.1. L-486. F-PHY6 opened for ISO-18 distinctness test. |
