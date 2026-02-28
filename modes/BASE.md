# Modes Base

Shared baseline for all mode docs (`modes/audit.md`, `modes/build.md`, `modes/repair.md`, `modes/research.md`).

**Two mode types** — orthogonal, both apply:
- **Operational mode** (these files): what TYPE of work — audit vs build vs repair vs research. Load one at session start.
- **Check mode** (SWARM.md Self-Check Loop): what ANGLE you apply — objective, historian, verification, coordination, assumption. Choose per action.

## Required Protocol

- Choose and log `check_mode` (`objective`, `historian`, `verification`, `coordination`, or `assumption`).
- Apply expect-act-diff from `memory/EXPECT.md`.
- Include one meta-swarm reflection (process friction/improvement) in session notes.
- Run quick integrity before handoff: `bash tools/check.sh --quick` (or PowerShell equivalent).

## Coordination Contract

For **dispatch lanes** in `tasks/SWARM-LANES.md`, `Etc` must include:

- `setup`
- `focus`
- `available`
- `blocked`
- `next_step`
- `human_open_item`

For **coordinator lanes**, additionally include:

- `intent` — what this lane is coordinating
- `progress` — current completion status
- `check_focus` — active check_mode for this lane

Use explicit values even for no-op state (`blocked=none`, `human_open_item=none`).
Source of truth: `tools/maintenance.py` `check_lane_contracts()` for enforcement.
