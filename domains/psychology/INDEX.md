# Psychology Domain Index
Updated: 2026-02-27 | Sessions: 186

## What this domain knows
- **Seed evidence base**: swarm artifacts already show cognitive-load effects, signaling overhead, and error-cascade behavior under coordination modes.
- **Core structural pattern**: swarm quality is partly a collective cognition problem; protocol design acts as cognitive scaffolding.
- **Automability limit signal**: cognitive load and trust ambiguity place practical limits on how reliably agents follow structured, machine-routable updates.
- **Active frontiers**: 4 active domain frontiers in `domains/psychology/tasks/FRONTIER.md` (F-PSY1, F-PSY2, F-PSY3, F-PSY4).
- **Cross-domain role**: psychology complements game-theory and control-theory by modeling how real agents process signals and workload under protocol constraints.
- **Latest execution (S186)**: F-PSY1 baseline artifact `experiments/psychology/f-psy1-context-load-threshold-s186.json` joined lane + NEXT event load proxies across sessions 169..186 (n=18). Signal is currently weak/mixed (`corr=-0.2581`, no robust high-load drop), indicating the present proxy is dominated by reporting-density effects rather than stable workload instrumentation.

## Lesson themes

| Theme | Example lessons | Core insight |
|-------|-----------------|--------------|
| Attention and overload | L-214, L-257 | Too much context/status noise reduces effective execution throughput |
| Error cascades | L-207, L-223 | Shared signals can align action, but also align mistakes without independence controls |
| Human-swarm interaction | L-214 | Low-friction autonomy signals improve continuity and reduce command overhead |

## Structural isomorphisms with swarm design

| Psychology finding | Swarm implication | Status |
|--------------------|-------------------|--------|
| Cognitive overload increases error probability | Keep coordination updates concise and schema-driven | OBSERVED |
| High ambiguity reduces schema compliance | Use compact, explicit fields to preserve automability under load | THEORIZED |
| Trust is calibrated from evidence quality + history | Lane signals should include reliability/evidence metadata | THEORIZED |
| Shared attention can accelerate or bias groups | Preserve controlled diversity and independent passes for critical runs | OBSERVED |
| Motivation influences sustained execution | Design protocols that minimize repetitive prompting and friction | OBSERVED |

## What's open
- **F-PSY1**: quantify context-load thresholds where coordination quality drops.
- **F-PSY2**: test trust/reliability signaling fields in lane handoffs.
- **F-PSY3**: reduce status-noise while preserving pickup speed and correction quality, including schema adherence required for automability.
- **F-PSY4**: personality-methodology mapping — test H1 (introversion→paradigm-shift), H2 (obsession→precision), H3 (collaboration→cross-domain) at n=50+ (L-528, S348).

## Psychology links to current principles
P-179 (agent utilization discipline) | P-182 (expect-act-diff loop) | P-197 (quality dimensions)
