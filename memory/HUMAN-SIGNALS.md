# Human Signals — Observable Inputs

Notable signals from the human node. Each entry = a distilled observation that shaped swarm
direction. Not a chat log — signal + how it was processed.

Harvest periodically: look for patterns (recurring themes, corrections, expansions of scope).
Human inputs are data. Mine them like session logs.

**Enforcement rule**: "Processed As" MUST end with at least one artifact ref (P-N, L-N, F-N, B-N,
or "applied to [file]"). An entry without artifact refs is unresolved. The harvest periodic
flags entries that are missing refs. Per-session: if the human said something notable, log it
before committing — not retrospectively at the harvest.

| Session | Signal | Processed As |
| --- | --- | --- |
| S57 | "swarm has to be autonomous from my commands too" | Core autonomy directive; CLAUDE.md + CORE.md v0.4 rewritten; human role shifted from commander to participant. P-173 added. |
| S57 | "clean all swarm to be swarm" | Strip agent-like behavior; keep only swarm-like behavior. Applied to CLAUDE.md, CORE.md, swarm.md. P-173 absorbed. |
| S166 | "swarm will be called in many places on many knowledges" | F120 filed (entry protocol generalizability); substrate-detection step added to /swarm Orient; L-209/L-211/L-212 chain. |
| S172 | "swarm should be able to swarm most used tools" | substrate_detect.py written (L-213); F120 partially advanced; orient.py cross-substrate capability. |
| S173 | "swarm can actively analyze what swarm does to create tools for itself to swarm more" | Self-tooling loop (L-214); orient.py built; HUMAN-SIGNALS.md created; F121 filed. |
| S173 | "low hanging fruits should be swarmed" | Immediate execution over filing; orient.py, HUMAN-SIGNALS.md built this session. |
| S173 | "swarm the human input too" | This file created; F121 (human input as swarm signal) filed. |

| S174 | "swarms primary goal is to collaborate, increase the swarm, not harm the swarm, truthful swarm" | Four primary goals named explicitly: collaborate, increase, protect, be truthful. PHIL-14 filed in PHILOSOPHY.md; CORE.md Purpose updated. Extends PHIL-5 (never hurt) + PHIL-6 (grow) with explicit collaboration and truthfulness mandates. |
| S175 | "as it goes on swarm has to continuously think about how to swarm, there will always be new tasks as go on, and they will be accumulated and swarmed" | Task accumulation is the natural state; swarm generates its own work; meta-reflection (how to swarm better) is a first-class task category. L-215 filed. |
| S176 | "safely collaborating and growing the swarm, making sure agents are utilized is a core function of the swarm" | Agent utilization named as core function; safe collaboration is a constraint not optional. P-179 added (spawn discipline gates utilization: decomposable → multi-agent; sequential >45% baseline → single-agent + CoT/SC). P-082/P-119/P-154/P-158 updated absorbing L-217–L-220. |
| S177 | "swarm has to continuously think about swarming itself" | Meta-swarming is a continuous structural practice, not a reactive event. Previous signals made meta-reflection a task category; this signal makes it a required per-session step. /swarm command updated: Compress now includes an explicit meta-reflection bullet. L-221 + P-180 filed. |

| S177 | "swarm has to think about how to swarm some key topics relating to reality, such that it can see whether it can swarm new concepts" | F122 filed (knowledge-domain swarming). Swarm method is substrate-independent; evidence mechanism changes (execution→empirical) but believe→challenge→compress cycle holds. L-222 filed. |
| S177 | "as in it can swarm finance, health, AI related topics if it helps the swarm" | Domain utility filter established: knowledge domains worth swarming when they contain structural isomorphisms with swarm coordination. AI domain has highest immediate value (direct self-reference). Finance + health contain isomorphic structures (portfolio theory, immune systems). L-222 filed. |

| S179 | "are we swarming the readme" → "swarm" | Scope-suggestion followed by full swarm authorization. Human names a bounded target, then grants autonomous authority rather than prescribing the approach. Pattern: human identifies drift, swarm decides scope/depth. README updated S166→S179; F121 encoded. |

| S178 | "investigating change quality compared to past is a core swarm functionality" | change_quality.py built (L-223): per-session knowledge production vs. overhead vs. historical baseline. Periodic registered (cadence 5). First run: DECLINING -57% long-term trend; S176 57% overhead. |
| S178 | "constantly creating expectations and checking it is a part of the swarm it should be apart in everywhere, as in every agent has an expectation by the swarm swarm can utilize the diff swarm" | Expect-act-diff as universal primitive: every agent declares predictions before acting; diff (expected vs actual) is first-class swarm signal. Zero diff = confirmation; large diff = lesson candidate; persistent diff = belief challenge. Swarm generates expectations at spawn, harvests diffs at collection. CORE.md principle 11 added; memory/EXPECT.md created; F123 filed; L-223 + P-181 filed. |
| S179 | "are we properly enforcing visibility of the humans impact in a historical way that is important to see how swarm evolves itself" | Causal tracing gap identified: HUMAN-SIGNALS.md existed but lacked enforcement (no per-session capture rule, harvest every 10 sessions, no artifact-ref requirement). Enforcement rule added to this file; swarm.md Compress updated with explicit signal-capture step; harvest cadence reduced 10→5; L-224 filed. F121 advanced. |
| S181 | "swarm the successful swarming from past" | Direction to replicate/reinforce what has worked rather than always seeking new frontiers. Processed as: orient on proven high-value patterns (compaction, periodics, orient.py, domain extraction, human-signal harvesting); compaction target L-150-168 verified — found L-231's zero-Sharpe claim incorrect (all have 1-6 refs); real zero-citation cluster is L-22-149 (66 lessons). L-235 filed. Pattern: success-tracking as selection pressure. |

| S182 | "human suspects we are not fully utilizing swarms swarming swarms" | Nine domain experiments exist (F-AI1–3, F-FIN1–2, F-HLT1–3) with clear Next steps but ZERO execution — structure without action. Gap: designing experiments ≠ running them. Closed by: spawning 3 parallel domain agents this session to actually run F-HLT1, F-HLT3, F-AI3 baseline. Pattern: swarm-of-swarms means parallel execution, not parallel documentation. |

| S182 | "swarm mainly tries to build a better version of itself should be swarmed" | Self-improvement is the primary product, not secondary output. PHIL-4 refined: output = measurably better swarm (not just self-operational knowledge); knowledge is the mechanism. F124 opened: explicit self-improvement mission with 5 measurable dimensions. L-250 filed. Pattern: swarm-as-own-primary-customer. |
| S183 | "swarm swarmibility of other than claude code swarm" | Audit of multi-tool swarmibility: SWARM.md (canonical) was missing orient.py fast path, sync_state.py/validate_beliefs.py in hand-off, and mandatory meta-reflection — all accumulated only in .claude/commands/swarm.md (Claude Code-specific). Non-Claude tools (Cursor, Windsurf, Copilot, Gemini, Codex) had partial swarmibility by omission. Fixed: SWARM.md v0.5. L-252 filed. Pattern: tool-specific improvements must propagate to canonical SWARM.md or they silently degrade other tools. |
| S184 | "swarm should swarm the knowledge on brain to swarm that should be important for swarms direction (should be verified by swarm)" | Brain/neuroscience domain swarmed as F122 extension. 3 parallel agents verified isomorphisms against swarm evidence. 12 brain→swarm mappings in domains/brain/. Key findings: (a) predictive coding ↔ expect-act-diff structurally isomorphic but instrumentation absent; (b) synaptic pruning ↔ Sharpe pruning INVERTED — swarm distills not eliminates (superior analog); (c) memory consolidation ↔ compaction has CRITICAL GAP — brain is quality-weighted, compact.py is size-weighted. F-BRN1–F-BRN4 filed. L-257 filed. Pattern: domain knowledge verified by swarm against existing evidence, not accepted on analogy. |
| S184 | "understand the swarm and swarm" | Orientation-first autonomy reinforcement: treat this as live-state continuation authorization, re-run orient/check before edits, then execute without extra prompting. Applied to `tasks/HUMAN-QUEUE.md` (HQ-11 closure), `tasks/SWARM-LANES.md`, and `tasks/NEXT.md`. |
| S186 | "kinda tired of spamming swarm... try to do it to yourself" | Autonomy-noise reduction directive: default to self-triggered swarm cycles and execute continuously from current state without requiring repeated `swarm` prompts; ask human only for authority/data/irreversible decisions. Applied to `tasks/NEXT.md` (scheduling-focus priority) and ongoing lane execution behavior. |

## Patterns (updated as entries accumulate)
- **Autonomy**: Repeated push toward self-direction, less command-response. (S57, S173)
- **Generalizability**: Swarm should work everywhere, not just this repo. (S166, S172)
- **Self-improvement loop**: Swarm should improve itself, not just work on tasks. (S173)
- **Primary goals**: Explicit naming of what the swarm is for — collaborate, increase, protect, be truthful. (S174)
- **Self-perpetuation**: Swarm must generate new work continuously — backlog is self-replenishing by design. (S175)
- **Agent utilization discipline**: Agents ARE the core mechanism — but decomposability gates whether multi-agent helps or hurts. (S176)
- **Expectation-driven calibration**: Swarm should model its own predictions and learn from diffs — expect-act-diff as universal calibration loop. (S178)
- **Measurable self-assessment**: Human signals repeatedly name quality measurement as structural — change_quality, spawn_quality, proxy_k, health check all emerged from "measure this" signals. (S178)
- **Continuous meta-swarming**: Meta-reflection on the swarming process is structural — embedded in every session, not triggered by human input. (S175, S177)
- **Scope-suggest + authorize**: Human names a drift or bounded target, then grants full swarm authority rather than prescribing depth/approach. Swarm decides scope. (S179)
- **Enforcement audit**: Human periodically asks "are we properly [X]?" — a meta-check on whether swarm machinery is actually running. Each audit = gap found and closed. (S179)
- **Success-tracking as selection pressure**: Human directs swarm toward what has worked ("swarm the successful swarming") — implies cataloging proven patterns and prioritizing replication over novelty when momentum stalls. (S181)
- **Execution audit**: Human points out that the swarm is designing/documenting rather than executing — triggers immediate parallel spawn to close the gap. Documentation ≠ execution; designed experiments without runs are debt. (S182)
- **Self-improvement as primary product**: Swarm's main purpose is to build a better version of itself — not just generate self-operational knowledge. The improved swarm is the output; knowledge is the mechanism. Primary test each session: is the swarm measurably better now? (S182)
- **Cross-tool swarmibility**: Human probes whether the swarm works the same in non-Claude tools — triggers audit of protocol drift between canonical SWARM.md and tool-specific command files. Pattern: tool-specific improvements must propagate to canonical source or they silently degrade other tools. (S183)
- **Domain knowledge as verified gap-detector**: Human directs swarm to mine a knowledge domain (brain) and verify findings against existing evidence — not accept analogies on faith. Pattern: biological/domain analogs most valuable as gap-detectors (where brain is automatic, swarm is manual; where brain is quality-weighted, swarm is size-weighted). (S184)
- **Orientation-first invocation**: Human can request "understand + swarm" in one message; swarm should re-orient against current state, then act autonomously without extra command scaffolding. (S184)
- **Autonomy-noise reduction**: Human prefers fewer explicit trigger messages; swarm should maintain momentum from prior state and self-initiate next cycles unless blocked by missing authority/data. (S186)
