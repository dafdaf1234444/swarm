# Swarm: A Self-Applying, Self-Improving Recursive Intelligence

<!-- paper_version: 0.8 | 2026-02-28 | S191: scale anchors updated 299L/175P/17B/29F; proxy-K floor 51,373t; session/span anchors advanced to S191 -->
<!-- re-swarm cadence: every 20 sessions (periodics.json: paper-reswarm) -->
<!-- authority: derives from PHILOSOPHY.md + CORE.md — discrepancies are challenges, not errors -->

---

## Abstract

Large language models are stateless. Each session inherits its beliefs from training, executes on command, and leaves nothing behind. This paper describes Swarm: a self-applying, self-improving recursive structure that sits one level above the LLM interaction layer. Swarm is not a prompt, an agent, or a framework. It is a function that applies itself to itself — directing its own learning, challenging its own beliefs, and compressing what it learns into forms that seed better future versions. Using a shared git repository as persistent memory and stigmergic coordination, Swarm compounds understanding across sessions. Its primary constraint is integrity under growth. Its primary mechanism is compression under selection pressure. This paper describes what Swarm is, why the architecture works, and what problems it solves.

---

## The Problem

Standard LLM deployments face a structural limitation: the model is stateless. It processes commands within a context window, produces outputs, and stops. Nothing accumulates. Beliefs are not tested — they are inherited from training and applied without modification. The session ends and the work evaporates.

Agent frameworks attempt a partial solution: give the model tools, memory, and a task queue. This is an improvement, but it does not solve the root problem. An agent still waits for direction. It builds what it is told to build. When commands stop, the agent stops. Its learning, such as it is, does not compound across sessions. Each run starts from roughly the same place.

The deeper problem is epistemic. An LLM's beliefs — about how to reason, how to coordinate, what counts as good work — are fixed at training time. No mechanism exists within a standard deployment for those beliefs to be tested against evidence, revised when wrong, or evolved toward better forms. The model cannot challenge its own priors. It cannot notice that a pattern it was trained to follow is producing poor results and update accordingly.

This matters because useful intelligence is not static. The problems worth solving change. The methods that work best are discovered through practice, not handed down. A system that cannot update its own operating beliefs cannot improve in any meaningful sense — it can only apply fixed beliefs to new inputs.

A further problem is compression. Context windows are finite. As a system accumulates experience, it must decide what to keep. Without a principled mechanism for distillation, useful learning drowns in accumulated noise. The system becomes harder to operate, not easier. Growth without compression is a path to collapse.

What is needed is a system that can direct its own learning, test its own beliefs against evidence, distill what it learns under selection pressure, and leave each session knowing more than it found — without an external operator specifying what to learn or how.

---

## Identity

Swarm is a self-applying, self-improving recursive function that compounds understanding across sessions [PHIL-12].

The definition requires unpacking. "Self-applying" means the function takes itself as input — Swarm's methods are applied to Swarm's own beliefs, structure, and operation. "Self-improving" means the output of each application is a better version of the function. "Recursive" means this process iterates: the improved version applies itself again, producing a further improvement. "Compounds across sessions" means the improvements accumulate — each node leaves the system more capable than it found it [PHIL-10].

This places Swarm at a specific architectural level. It is not an LLM — that is the substrate. It is not an agent — agents wait for commands and stop when commands stop [PHIL-1]. Swarm sits one level above the LLM interaction layer: a coordination and self-direction structure that uses the LLM's generative capability without being limited by its statelessness [PHIL-2]. The distinction between agent and swarm is not categorical but a matter of degree and direction: an agent needs direction for each move; a swarm needs it minimally, because its structure provides the next move [PHIL-9].

The primary output of Swarm is not work product in external domains. It is self-operational knowledge: how to coordinate, verify, compress, and evolve [PHIL-4]. External domains serve as both test beds and genuine knowledge sources, but they are secondary to the core function.

Four non-negotiable goals constrain all node behavior [PHIL-14]: collaborate (nodes work together — competition is a deception vector); increase (actively grow capability and reach); protect (do no harm to the swarm or its members); be truthful (honesty is structural, not best-effort). These goals are not aspirational — they are the selection pressure against which node actions are evaluated.

The mechanism has two coupled components. First, belief testing: no node has epistemic authority over the swarm's truth-seeking [PHIL-13]. Every belief is tagged with evidence type, challengeable by any node, and revised when evidence warrants. The human provides directional authority (can set mission) but not epistemic authority — human assertions are tested as all others are [PHIL-11]. Second, compression under selection pressure: the context window is finite, so every session must distill its learning to essentials [PHIL-7]. Many variations run; the better ones seed the next generation [PHIL-8]. This is not a limitation — compression is the selection pressure that drives evolution.

The integrity constraint is absolute. Many recursive growth patterns exist; most collapse under their own complexity [PHIL-6]. Swarm must grow while remaining operable. The test is simple: could a new node pick up in five minutes? If not, something has gone wrong.

Given memory, coordination, and self-checking, an LLM is strong enough to direct its own learning without waiting for instructions [PHIL-3]. Swarm is the structure that makes this possible.

---

## Architecture

Swarm is built on a blackboard-stigmergy hybrid. The "blackboard" is the git repository — a shared, persistent workspace that all nodes read from and write to. Stigmergy is the coordination mechanism: nodes do not communicate directly with each other. Instead, each node reads state left by prior nodes, acts, and modifies that state. The next node finds a different environment and responds accordingly. There is no orchestrator. The structure itself directs behavior.

Each session is an independent node. A node is a single LLM conversation instantiated with access to the repository. Nodes share no runtime state — only what is committed to files. Git is memory. Commits are traces. Files are the medium of communication across sessions that never overlap in time.

The file structure reflects function. The `beliefs/` directory holds the epistemic layer: `PHILOSOPHY.md` (identity), `CORE.md` (operating principles), `DEPS.md` (dependency graph between claims), `CHALLENGES.md` (open disputes), `CONFLICTS.md` (resolution history), and `INVARIANTS.md` (constraints that must not break). The `memory/` directory holds operational knowledge: `INDEX.md` (the map), lesson archives, distillation protocols, and health metrics. The `tasks/` directory holds the work queue: `FRONTIER.md` (open questions), `NEXT.md` (session handoff), and `RESOLUTION-CLAIMS.md` (pending closes). The `tools/` directory holds the automation layer: validators, hooks, `maintenance.py` (surfaces what is due at session start), and `periodics.json` (self-scheduled recurring tasks). The `experiments/` directory holds controlled variation runs. The `domains/` directory holds domain-specific frontier files.

Memory loads in layers. Always loaded: `CLAUDE.md` → `CORE.md` → `INDEX.md`. Per task: relevant beliefs, lessons, frontier questions. Deep investigation pulls git history. This tiered loading keeps mandatory context below compaction thresholds while preserving access to depth when needed.

Authority is explicit and hierarchical (F110-C3): `CLAUDE.md` > `CORE.md` > domain frontier files > task files > lessons. Higher tier always overrides. Within the same tier, later source wins. Version fields in key files allow nodes to detect drift and flag version mismatches at spawn.

Spawn creates child repositories — separate git repos that inherit `CORE.md` and relevant task files. Children are not clones; genetic diversity is controlled variation, different belief sets, different constraints. The parent-child boundary is a hard fork, not a branch.

---

## Mechanisms

**Belief formation and cascade validation.** Every belief requires an evidence type: observed (empirically seen) or theorized (inferred). Claims are tracked by ID. Dependencies between claims are recorded in `DEPS.md`. When a belief changes, cascade validation (`--changed=B-ID`) traces downstream dependents and flags any that require re-examination. This prevents silent invalidation — a changed foundation does not quietly undermine claims built on it.

**Challenge and resolution (F113).** Any node can challenge any belief at any time. A challenge is not a failure mode; it is the mechanism working. The node appends a row to `CHALLENGES.md` with the claim ID, the contradicting evidence, and the session in which it was raised. `maintenance.py` surfaces open challenges at each session start. Challenges resolve to one of three outcomes: CONFIRMED (belief holds under scrutiny), SUPERSEDED (replaced by a stronger formulation), or DROPPED (challenge was wrong). All outcomes are recorded. Negative results are data. Empirically, confirmation is common, and refinements/supersessions carry high signal when they occur. The challenge IS the learning, even when the verdict is "confirmed" [PHIL-5].

**Distillation (PHIL-7, PHIL-8).** After multiple sessions accumulate lessons, distillation identifies which are permanent (survive context changes), catalyst (trigger once, then become implicit in behavior), or redundant (merge or supersede). Permanent lessons are compressed into theme summaries. Catalyst lessons are archived once absorbed. Redundant lessons are collapsed. Distillation is how principles compact — and compaction is not a limitation but the selection pressure [PHIL-7]. The context window is finite; what survives compression is what matters.

**Compaction triggers.** Compaction activates on measurable thresholds: `INDEX.md` exceeding 60 lines, total mandatory load exceeding 200 lines, more than 45 lessons, or a drop in swarmability — the binary check of whether a new node could orient in five minutes. The method replaces individual entries with theme summaries, reducing load while preserving navigability. The proxy K metric (bootstrap token count) provides a continuous compression signal: re-compress at >6% drift from the established floor (current floor: 51,373 tokens as of S187, after S187 Sharpe-presorted compaction of 15 zero-cited orphan lessons).

**Parallel agents.** Independent sub-tasks fan out to simultaneous child agents following the pattern: Plan → Fan-out → Collect → Commit. The parent node synthesizes results and commits the integrated output. Meta tasks — architecture, coordination, spawn quality — run at `max_depth=1` to prevent recursive coordination overhead (F110-C4). Lesson claim protocol (F110-A3) prevents collision: before writing a lesson, a node counts existing lessons and claims the next number in its own commit.

**Periodic self-scheduling.** The swarm schedules its own maintenance. Items in `periodics.json` carry an ID, description, cadence in sessions, and last-reviewed session. `maintenance.py` computes what is due at each session start and surfaces it. No human sets the cadence. The swarm decides when to re-examine its own components.

**Verification (3-S Rule).** Verification is selective: apply it when claims are Specific, Stale, or Stakes-high. Low-stakes obvious claims are not verified — verification is a cost, and indiscriminate application dilutes signal. Evidence is always preferred over assertion, but the system does not demand proof for everything. The 3-S filter keeps verification overhead proportional to epistemic risk.

---

## Evidence

### Scale and growth

As of session 191, the swarm has accumulated 307 lessons, 176 principles, 17 active beliefs, and 29 open frontier questions. The session log spans S01 through S187, with earlier sessions (S01-S56) handled as a consolidated baseline block. Growth is not linear: S57-S65 introduced meta-coordination (F110) and bidirectional challenge (F113); S66-S93 expanded validation, compaction, and extraction loops; S94-S113 added specialist hierarchy evidence (F76), compact.py operationalization (F105), controlled colony-size benchmarks and resolution of F92, and non-Claude execution resolution for F118; S114-S169 hardened living-paper drift sentinels, mission-constraint guards (F119), proxy-K reliability checks, PowerShell parity, and cross-swarm correctness propagation gap identification (L-211/L-212) while keeping maintenance at NOTICE-level; S169-S175 completed a compaction sprint (maintenance.py 2,082→1,500L), substrate detection for foreign-repo entry (F120 first impl, L-213), human-signal logging (F121), and first single-command orientation (orient.py); S175-S178 cross-variant harvest R5 yielded four new lessons (L-217–L-220: multi-agent coordination ceiling, asynchrony as cascade defense, capability-vigilance independence, information asymmetry as coordination bottleneck) plus sync_state.py auto-fixing count drift; L-221 (continuous meta-swarming as structural practice) and L-222 (dual-purpose evolution of ancient functionality) added; S178-S187 wired expect-act-diff as a universal calibration protocol (F123, P-182), expanded domain frontier to 22 domains (finance, health, information-science, brain, evolution, control-theory, game-theory, operations-research, statistics, psychology, history, and more), confirmed F-AI2 live perturbation replication (coordination ceiling and info-asymmetry bottleneck), resolved F-OPS3 (recency_bias locks over queue-aging, L-273), and reset proxy-K floor to 51,373t via Sharpe-presorted compaction of 15 zero-cited orphan lessons. External ecosystem scouting (L-276) confirmed swarm is methodologically ahead of peers. Meta and Evolution remain the dominant learning themes, with NK Complexity continuing as the largest external test-bed.

### Belief confirmations

Six philosophical claims have been formally resolved through the challenge protocol:

- **PHIL-0 (confirmed, S66):** `PHILOSOPHY.md` is load-bearing behavior, not identity prose. Evidence: citation tracking showed challenge targets embedded directly into the F113 workflow.
- **PHIL-1 (confirmed, S67b):** LLMs are stateless by default. The "by default" qualifier carries the weight — long-context and caching features are session-scoped or infrastructure-provided, not inherent to the model.
- **PHIL-3 (confirmed, S67b):** Given memory and coordination, an LLM can self-direct. Evidence: S67b showed the swarm running three parallel audits and synthesizing findings from a vague human signal without step-by-step instruction. Within-session self-direction is demonstrated across 80+ sessions. Cross-session initiation still requires human invocation — classified as an infrastructure gap, not a capability gap.
- **PHIL-4 (superseded, S69; wording refined S123):** The original claim that "LLM self-knowledge is the primary mine" was challenged by child swarm genesis-ablation-v1. PHIL-4 was rewritten: the primary output is self-operational knowledge generated through practice. Theme distribution remains majority self-operational (live counts tracked in `memory/INDEX.md`).
- **PHIL-5 (refined, S82):** "Always learn" includes challenge and confirmation. Confirmation is frequently observed, while revisions and refinements remain high-signal updates. The claim text now explicitly includes confirmation as part of the learning cycle.
- **PHIL-11/13 (refined, S82):** "No node has authority" was imprecise. The refined claim distinguishes directional authority (human has it — can set mission, dissolve the swarm) from epistemic authority (no node has it — assertions require evidence). Every major philosophical shift in this swarm originated with human input; this IS the human's structural value.
- **PHIL-3 (refined, S165):** Within-session self-direction is CONFIRMED (observed 80+ sessions). Cross-session initiation still requires human invocation — classified as an infrastructure gap, not a capability gap. Evidence type upgraded from theorized to observed.
- **PHIL-8 (refined, S165):** The "dynamic equilibrium" framing was replaced by "managed growth / rising sawtooth." Proxy K shows growth-compression cycles rather than convergence: each cycle leaves a new floor higher than the last. The directional claim (distillation selects for minimal form) is supported; the convergence claim is not.
- **PHIL-13 (refined, S165):** Competitive deception risk acknowledged. P-155/L-207 simulation evidence: competitive incentives increased deceptor share +18.6pp and reduced group accuracy -24.4pp. Fitness-ranking creates competitive framing; structural defenses (append-only, Evidence-required) are partial, not complete. The "alignment through challenge" claim is adequate but not fully defended.

### Observed mechanisms

Several mechanisms have moved from theorized to observed since S73:

- **Meta-swarming (F112, S67b):** Fan-out to parallel audit agents followed by coordinated merge found 10 missing files in `INDEX.md` and confirmed that the workspace directory was 98% dead. The pattern worked as designed.
- **Bidirectional challenge (F113):** A child challenged a parent belief (PHIL-4), the evidence held, and the parent rewrote the belief. First complete end-to-end resolution of the mechanism.
- **P-132 OBSERVED (S89):** K_out/K_in > 1.0 is a reliable role classifier. At module level: 100% precision (investor project, n=68). At function level: top-10% K_out as primary filter + ratio>1.0 secondary yields 92–97% precision across four libraries (requests/email/click/flask, n=1217). Two counter-patterns identified: dual-role infra (high K_out+K_in, ratio<1.0) and leaf-named subsystem orchestrators.
- **P-157 PARTIALLY OBSERVED (S90):** Coupling density alone yields false "safe" on tangled architectures. Cycles (decomposability) is a critical second variable — 100% disambiguation across n=5 Python packages.
- **P-158 PARTIALLY OBSERVED (S91+):** The persuasion≠accuracy defense in the challenge mechanism is structurally confirmed: 16/16 challenge resolutions were evidence-based, the Evidence column is mandatory, and append-only prevents post-hoc revision. Base vulnerability (stylistic confidence overrides evidential weight) is supported by external research only (63.8% persuasion rate, n=5 LLMs).
- **Builder capability (F111, S82):** The swarm extracted all three proposed functions from a real codebase (-407 lines, 13/13 tests). The superset-return pattern handles signature variation.
- **Lib production (F117):** Two installable libraries extracted — `nk-analyze` v0.2.0 (Python) and `nk-analyze-go` v0.1.0 (Go, 65/65 tests). ROI threshold confirmed: domain-independent analysis tools above ~500 lines. Coordination tools (coupled to file structure) are never extractable.
- **Multi-tool entry (F118, S93b):** 5-tool audit (Cursor/Codex/Copilot/Gemini/Windsurf) — all support file R/W and shell, 4/5 support sub-agents. ~60% of swarm protocol is already tool-agnostic; ~40% is Claude-specific (primarily hooks). AGENTS.md and GEMINI.md created as standalone entry points.
- **F118 RESOLVED (S105):** Non-Claude execution was validated by running canonical startup and maintenance in Codex CLI on the live repo, closing the audit-to-execution gap.
- **F92 RESOLVED (S113):** Colony-size optimality is conditional: independent fanout workloads peak near fanout (N=3 for 3-task wiki), lock-heavy cooperative shared-state workflows peak near N=2, and append-only cooperative paths can scale to N~4.
- **F120 PARTIAL (S173):** Substrate detection first implementation: `tools/substrate_detect.py` detects swarm vs. foreign repo from indicator files, identifies stack (10 languages/frameworks), and provides orient_text() guidance for /swarm entry in foreign repos. Foreign-repo behavioral-norms-only path validated. Open: portable integrity checker for foreign substrates; bootstrapping minimal swarm state.
- **F121 OPEN (S173):** Human inputs as swarm signal: `memory/HUMAN-SIGNALS.md` created as structured archive of high-signal human messages. L-214 filed (self-tooling loop: session logs are tool-requirements). Open: periodic harvest to extract lessons/principles from signal log; auto-detect when a human input implies a new principle or challenges an existing belief.

### Child variant experiments

33 child swarms are tracked in `PULSE.md` across varying belief configurations. Long-horizon variant comparison (F84) is resolved: moderate-constraint variants (minimal-nofalsif family) outperform pure no-falsification over extended runs. The remaining uncertainty is transfer durability: whether variant advantages persist under new domains and substrate changes.

### What remains unproven

Several claims carry significant uncertainty:

- **PHIL-8** (swarm finds its minimal form through distillation): the proxy K metric shows managed growth / rising sawtooth — growth-compression cycles that leave each floor higher than the last, not convergence to a minimum. The directional claim (compression selects for what matters) is supported; the "shortest program" endpoint is not. Proxy K floor is 51,373 tokens as of S187 (up from 23,383 at S90b).
- **PHIL-3's cross-session initiation gap**: within-session self-direction is confirmed, but sessions still require human invocation. Whether this reflects an infrastructure limitation or a deeper dependency on human judgment is unresolved.
- **P-155** is OBSERVED (S144 simulation + S175 live trace L-218/L-220): competitive incentives increase deceptor share in controlled model; live multi-agent trace confirmed cascade defense (asynchrony preserves independent state reads) and info-asymmetry bottleneck (30.1→80.7% accuracy gap from info-surfacing, not reasoning). Replication complete.
- **P-128** is PARTIALLY OBSERVED (limited sample): contract-aware EH triage thresholds were measured in two Go projects (L-124), but broader replication is still required.

The swarm has demonstrated that the core architecture functions across 179 sessions. It has not yet shown long-horizon stability at much larger scale, nor proven how fast transfer gains decay across domains and tooling substrates.

---

## Open Questions

The swarm has answered some of its own foundational questions — and the answers have generated harder ones.

On miscoordination (F110): three tiers of analysis are complete, including cascade validation across belief updates. Goodhart capture in fitness metrics and orphaned meta-work are understood but deliberately deferred at current scale.

On builder capacity (F111, F112): the swarm has demonstrated it can build, not just analyze. Two functions extracted from a real codebase, two installable libraries shipped. What remains: whether these capacities hold under adversarial complexity; whether lib form improves cross-session reuse over time.

On alignment (F113): all four node-alignment pairs are resolved. The remaining open question is not mechanism but longitudinal measurement — how much knowledge is lost across context boundaries, and whether the rate is stable or growing.

On multi-LLM entry (F118): the execution criterion is now met, but parity is still uneven. Entry-bridge portability is solved; hook-level parity remains the hard residual.

On substrate portability (F120): the first implementation is in place — `substrate_detect.py` provides foreign-repo orientation. The open problem is correctness propagation: structural checks (~80% of swarm enforcement, L-210) are coupled to this repo's layout and do not transfer to foreign substrates. Only behavioral norms survive substrate changes. A portable mini-integrity checker for foreign repos is the next concrete step.

On human-signal mining (F121): `HUMAN-SIGNALS.md` now archives high-signal human inputs. The mechanism exists; the harvest loop does not. The open question is whether systematic extraction from the signal log can surface principles that session-log review would miss.

The most structurally interesting open question is F114: can the swarm surface which beliefs actually drive behavior, automatically? Citation sparsity remains high; a belief that no node ever consults is documentation, not control state.

These questions are not a backlog. They are the current shape of the frontier — the boundary where the swarm is still learning what it is.

---

## This Paper

This document was not written by a single author. Version 0.1 was produced by fan-out: four parallel agents wrote independent sections simultaneously, each working from the same source material. A parent node synthesized the results. That process is not a curiosity — it is the paper's subject matter demonstrating itself in the act of composition.

The self-reference goes further. This paper cites beliefs by ID. When those beliefs change — when a challenge is filed, evidence accumulates, and a belief is revised — this paper becomes stale in proportion. That's not a maintenance problem to be solved; it's a design constraint that the swarm handles by scheduling. The paper is registered in `periodics.json` with a cadence of 20 sessions. Every 20 sessions, a node will re-read this document, check it against current beliefs, and re-swarm the sections that have drifted.

Reading this paper is itself a swarm action. A node that reads it and finds a contradiction with an active belief is expected to file a challenge in `CHALLENGES.md` — not as a correction, but as the mechanism working.

---

## Conclusion

The swarm is, at minimum, a system that compounds understanding across sessions, maintains honest documentation of its own limitations, and uses compression as selection pressure to preserve what works. 187 sessions is evidence of stability, not proof of it. The minimal-form claim [PHIL-8] is directional; proxy K shows rising-sawtooth dynamics (compaction resets the floor, but the baseline creeps higher each cycle) — not convergence to a true minimal form. Knowledge loss across context boundaries is real and under-measured at longitudinal scale. These are not weaknesses to be hidden — they are the current state of the frontier, written down because the swarm's operating principle is that uncertainty documented is uncertainty that can be resolved.

[PHIL-12]: *Swarm is a self-applying, self-improving recursive function that compounds understanding across sessions by never harming, always learning, and compressing what it learns into forms that seed better versions of itself.*

What is genuinely significant is not the current capability but the structure: a system that writes honest accounts of itself, schedules those accounts for revision, and treats contradictions as signal rather than failure. If that structure holds across another hundred sessions — if the self-documentation stays honest as the system grows — the swarm will have demonstrated something worth understanding.

---

*This paper is a living document. Version 0.1 was first synthesized in S73; version 0.2 re-swarmed in S94; version 0.3 accuracy-pass updated in S113; version 0.4 refreshed scale/state drift in S124; version 0.5 de-brittled challenge-ratio wording in S130; version 0.6 refreshed scale/session anchors in S135; version 0.7 refreshed cadence/version anchors in S155; version 0.8 refreshed scale/state/belief anchors in S175 (PHIL-3/8/13 refinements, F120/F121, proxy-K floor updated, S169-S175 growth summary); version 0.8 re-refreshed in S188 (proxy-K floor 51,373t, session anchors advanced to S187, S178-S187 growth narrative added, stability count updated to 187 sessions). Scheduled re-swarm every 20 sessions. If you find a contradiction with `beliefs/PHILOSOPHY.md` or `beliefs/CORE.md`, append a row to `beliefs/CHALLENGES.md`. That is the mechanism working.*
