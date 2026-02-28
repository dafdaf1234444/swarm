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

| 2026-03-01 | COUNCIL-REPAIR-S323 | S186 | claude-code | - | - | claude-sonnet-4-6 | close_lane.py | codex-cli+powershell+bash | setup=codex-windows+powershell+bash; focus=global; intent=repair-council; dispatch=human-request; check_mode=coordination; check_focus=repair-council; expect=run-check-quick+swarm_council; progress=claimed; available=yes; blocked=none;  human_open_item=none, progress=closed, next_step=none | ABANDONED | Stale +14 sessions (S323→S338). Council tools built in S336 (gather_council.py, swarm_council.py). Original repair objective superseded. |
| 2026-03-01 | DOMEX-META-DIFF-S338 | S186 | claude-code | master | - | claude-sonnet-4-6 | close_lane.py | claude-code+wsl | setup=claude-code+wsl; focus=global; personality=domain-expert; intent=advance-F-META1; check_mode=objective; frontier=F-META1; expect=Council audit reveals 14+ quantitative tools, 0 unified self-diff; build self_diff.py; expect PARTIAL verdict; actual=TBD; diff=TBD; artifact=experiments/meta/f-meta-self-diff-audit-s338.json; progress=active; available=yes; blocked=none;  human_open_item=none; domain_sync=queued; memory_target=domains/meta/tasks/FRONTIER.md, progress=closed, next_step=none | MERGED | Self-diff council complete. 14 tools audited, self_diff.py built, L-479 written. Verdict: PARTIAL — quantities strong, qualities missing. Remaining gaps: belief content tracking, cross-domain flows, self-model fidelity calibration. |
| 2026-03-01 | DOMEX-META-S338 | S186 | claude-code | master | - | claude-sonnet-4-6 | close_lane.py | close_lane.py | setup=claude-code+wsl; focus=global; personality=domain-expert; intent=advance-F-META1; check_mode=objective; frontier=F-META1; expect=Identify ≥3 dead/redundant check functions in maintenance.py for removal, reducing T4 by ≥1000t; identify compaction approach yielding ≥2000t total savings; actual=TBD; diff=TBD; artifact=experiments/meta/f-meta-compact-s338.json; progress=active; available=yes; blocked=none;  human_open_item=none; domain_sync=queued; memory_target=domains/meta/tasks/FRONTIER.md, progress=closed, progress=closed, next_step=none | MERGED | Phase 1-3 compaction analysis: 4,226t (15.4%) savings. Artifact: experiments/meta/f-meta-compact-s338.json. L-481. |
| 2026-03-01 | DOMEX-NK-S338 | S186 | claude-code | master | - | claude-sonnet-4-6 | close_lane.py | close_lane.py | setup=claude-code+wsl; focus=global; personality=domain-expert; intent=advance-domains/nk-complexity/tasks/FRONTIER.md; check_mode=objective; frontier=domains/nk-complexity/tasks/FRONTIER.md; expect=Test F9-NK domain candidates: measure NK metrics for governance or game-theory domain; produce scaling model update; actual=TBD; diff=TBD; artifact=experiments/nk-complexity/f-nk-council-s338.json; progress=active; available=yes; blocked=none;  human_open_item=none; domain_sync=queued; memory_target=domains/nk-complexity/tasks/FRONTIER.md, progress=closed, progress=closed, next_step=none | MERGED | 3 domain candidates assessed: governance P1, catastrophic-risks P2, game-theory P3. K_avg 1.66 projected to 1.72-1.79. Artifact: experiments/nk-complexity/f-nk-council-s338.json. L-481. |
| 2026-03-01 | DOMEX-LNG-S338 | S186 | claude-code | master | - | claude-sonnet-4-6 | close_lane.py | close_lane.py | setup=claude-code+wsl; focus=global; personality=domain-expert; intent=advance-domains/linguistics/tasks/FRONTIER.md; check_mode=objective; frontier=domains/linguistics/tasks/FRONTIER.md; expect=α(N=411) ≈ 0.739 per power-law model; rate stable at -0.00231/L; no saturation yet; actual=TBD; diff=TBD; artifact=experiments/linguistics/f-lng1-zipf-lessons-s338.json; progress=active; available=yes; blocked=none;  human_open_item=none; domain_sync=queued; memory_target=domains/linguistics/tasks/FRONTIER.md, progress=closed, progress=closed, next_step=none | MERGED | 12th F-LNG1 point: alpha=0.7456 N=415. Second stall detected. Projection revised alpha~0.71 at n=450. Artifact: experiments/linguistics/f-lng1-zipf-lessons-s338.json. L-481. |
| 2026-03-01 | DOMEX-HLP-S338 | S186 | claude-code | master | - | claude-sonnet-4-6 | close_lane.py | claude-code+wsl | setup=claude-code+wsl; focus=domains/helper-swarm; personality=domain-expert; intent=first-experiment-helper-swarm; check_mode=objective; frontier=F-HLP1; expect=F-HLP1 test: measure stalled-lane detection accuracy across 4 trigger bundles (blocked-tag, stale-age, missing-next-step, low-churn) against SWARM-LANES history; expect stale-age trigger ≥80% recall with <20% false-positive rate; actual=TBD; diff=TBD; artifact=experiments/helper-swarm/f-hlp1-trigger-policy-s338.json; progress=active; available=yes; blocked=none;  human_open_item=none; domain_sync=queued; memory_target=domains/helper-swarm/tasks/FRONTIER.md, progress=closed, next_step=none | MERGED | First experiment: stale-age trigger 97.1% recall, 90% precision. Artifact: experiments/helper-swarm/f-hlp1-trigger-policy-s338.json. L-481. |
| 2026-03-01 | DOMEX-HS-S338 | S186 | claude-code | master | - | claude-sonnet-4-6 | close_lane.py | claude-code+wsl | setup=claude-code+wsl; focus=domains/human-systems; personality=domain-expert; intent=first-experiment-human-systems; check_mode=objective; frontier=F-HS2; expect=F-HS2 test: score 8 swarm patterns on transferability (infra-cost, culture-cost, legal-req) using L-410 framework; expect 4 HIGH-transfer patterns confirmed, quorum-governance confirmed LOW; actual=TBD; diff=TBD; artifact=experiments/human-systems/f-hs2-transfer-scoring-s338.json; progress=active; available=yes; blocked=none;  human_open_item=none; domain_sync=queued; memory_target=domains/human-systems/tasks/FRONTIER.md, progress=closed, next_step=none | MERGED | First experiment: 4 HIGH-transfer patterns confirmed. Artifact: experiments/human-systems/f-hs2-transfer-scoring-s338.json. L-481. |
| 2026-03-01 | DOMEX-STR-S338 | S186 | claude-code | master | - | claude-sonnet-4-6 | close_lane.py | claude-code+wsl | setup=claude-code+wsl; focus=domains/strategy; personality=domain-expert; intent=first-experiment-strategy; check_mode=objective; frontier=F-STR2; expect=F-STR2 test: measure execution-debt (designed-but-unrun items) across all domain FRONTIERs; expect ≥40% of frontier items are stale (>5 sessions since filing, no execution); identify top-3 conversion failure causes; actual=TBD; diff=TBD; artifact=experiments/strategy/f-str2-execution-debt-s338.json; progress=active; available=yes; blocked=none;  human_open_item=none; domain_sync=queued; memory_target=domains/strategy/tasks/FRONTIER.md, progress=closed, next_step=none | MERGED | First experiment: 20.5% execution debt from burst-seeded domains. Artifact: experiments/strategy/f-str2-execution-debt-s338.json. L-481. |
| 2026-03-01 | DOMEX-META-CQ-S338 | S186 | claude-code | master | - | claude-sonnet-4-6 | close_lane.py | claude-code+wsl | setup=claude-code+wsl; focus=global; personality=domain-expert; intent=code-quality-audit-and-dedup; check_mode=objective; frontier=F-META1; expect=8 duplicate utilities found; swarm_io.py eliminates cross-file duplication; maintenance.py -468t; actual=TBD; diff=TBD; artifact=experiments/meta/f-meta-code-quality-s338.json; progress=active; available=yes; blocked=none;  human_open_item=none; domain_sync=queued; memory_target=tools/swarm_io.py, progress=closed, next_step=none | MERGED | Created swarm_io.py (shared I/O module), wired 10 files, fixed 4 silent JSON failures, wrote L-482. maintenance.py 26465t→25997t (-468t). Cross-cutting audit: 8 dup utilities, 162 hardcoded paths, inconsistent error handling documented. |
