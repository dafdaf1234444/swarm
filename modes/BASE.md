# Modes Base

Shared baseline for all mode docs (`modes/audit.md`, `modes/build.md`, `modes/repair.md`, `modes/research.md`).

## Required Protocol

- Choose and log `check_mode` (`objective`, `historian`, `verification`, `coordination`, or `assumption`).
- Apply expect-act-diff from `memory/EXPECT.md`.
- Include one meta-swarm reflection (process friction/improvement) in session notes.
- Run quick integrity before handoff: `bash tools/check.sh --quick` (or PowerShell equivalent).

## Coordination Contract

For active lanes in `tasks/SWARM-LANES.md`, `Etc` must include:

- `setup`
- `focus`
- `available`
- `blocked`
- `next_step`
- `human_open_item`

Use explicit values even for no-op state (`blocked=none`, `human_open_item=none`).
