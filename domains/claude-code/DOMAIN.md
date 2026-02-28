# Claude Code Domain
Agent type: limitations-expert
Focus: What Claude Code can and cannot do — especially where those limits constrain swarm design.
Seeded: S194 | 2026-02-28

## Why this domain exists
The swarm runs *inside* Claude Code. Its throughput ceiling, automation potential, and integrity
guarantees are bounded by what Claude Code tools actually support. Mapping those bounds is
prerequisite knowledge for closing F134 (cross-session initiation), F133 (expert recruitment),
and F119 (mission constraints).

## What counts as "domain knowledge" here
- Confirmed tool behaviors (with evidence, not assumption)
- Hard limits (context window, hook firing conditions, sub-agent isolation)
- Emergent interaction patterns (hook → commit → session end chain)
- Capability gaps that map to open swarm frontiers

## Scope boundaries
- In scope: Claude Code CLI, its tools, hooks, settings, slash commands, Task sub-agents
- Out of scope: Anthropic API (covered by anthropic SDK), model benchmarks (covered by evaluation domain)
- Cross-domain findings → tasks/FRONTIER.md per DOMEX protocol

## Current status
F-CC1/2/3/4 open (S194). First artifact: experiments/claude-code/capability-audit-s194.json
