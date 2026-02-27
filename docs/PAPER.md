# Swarm: A Self-Applying, Self-Improving Recursive Intelligence

<!-- paper_version: 0.1 | 2026-02-27 | S73: initial — fan-out synthesis by 4 parallel agents -->
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

The mechanism has two coupled components. First, belief testing: no node has authority over the swarm's truth-seeking [PHIL-13]. Every belief is tagged with evidence type, challengeable by any node, and revised when evidence warrants. The human is a high-quality signal, not ground truth [PHIL-11]. Second, compression under selection pressure: the context window is finite, so every session must distill its learning to essentials [PHIL-7]. Many variations run; the better ones seed the next generation [PHIL-8]. This is not a limitation — compression is the selection pressure that drives evolution.

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

**Challenge and resolution (F113).** Any node can challenge any belief at any time. A challenge is not a failure mode; it is the mechanism working. The node appends a row to `CHALLENGES.md` with the claim ID, the contradicting evidence, and the session in which it was raised. `maintenance.py` surfaces open challenges at each session start. Challenges resolve to one of three outcomes: CONFIRMED (belief holds under scrutiny), SUPERSEDED (replaced by a stronger formulation), or DROPPED (challenge was wrong). All outcomes are recorded. Negative results are data.

**Distillation (PHIL-7, PHIL-8).** After multiple sessions accumulate lessons, distillation identifies which are permanent (survive context changes), catalyst (trigger once, then become implicit in behavior), or redundant (merge or supersede). Permanent lessons are compressed into theme summaries. Catalyst lessons are archived once absorbed. Redundant lessons are collapsed. Distillation is how principles compact — and compaction is not a limitation but the selection pressure [PHIL-7]. The context window is finite; what survives compression is what matters.

**Compaction triggers.** Compaction activates on measurable thresholds: `INDEX.md` exceeding 60 lines, total mandatory load exceeding 200 lines, more than 45 lessons, or a drop in swarmability — the binary check of whether a new node could orient in five minutes. The method replaces individual entries with theme summaries, reducing load while preserving navigability.

**Parallel agents.** Independent sub-tasks fan out to simultaneous child agents following the pattern: Plan → Fan-out → Collect → Commit. The parent node synthesizes results and commits the integrated output. Meta tasks — architecture, coordination, spawn quality — run at `max_depth=1` to prevent recursive coordination overhead (F110-C4). Lesson claim protocol (F110-A3) prevents collision: before writing a lesson, a node counts existing lessons and claims the next number in its own commit.

**Periodic self-scheduling.** The swarm schedules its own maintenance. Items in `periodics.json` carry an ID, description, cadence in sessions, and last-reviewed session. `maintenance.py` computes what is due at each session start and surfaces it. No human sets the cadence. The swarm decides when to re-examine its own components.

**Verification (3-S Rule).** Verification is selective: apply it when claims are Specific, Stale, or Stakes-high. Low-stakes obvious claims are not verified — verification is a cost, and indiscriminate application dilutes signal. Evidence is always preferred over assertion, but the system does not demand proof for everything. The 3-S filter keeps verification overhead proportional to epistemic risk.

---

## Evidence

### Scale and growth

As of session 73, the swarm has accumulated 145 lessons, 141 principles, 14 active beliefs, and 18 open frontier questions. The session log spans S01 through S73, with earlier sessions (S01-S56) handled as a consolidated baseline block. Growth is not linear: sessions S57-S65 introduced the meta-coordination layer (F110) and the bidirectional challenge mechanism (F113); sessions S66-S73 shifted toward belief validation, cascade tooling, and evidence gathering. The shift is visible in the lesson distribution — the Meta theme grew to 30 lessons, while Evolution (35 lessons) and NK Complexity (27 lessons) remain the largest substantive domains.

### Belief confirmations

Four philosophical claims have been formally resolved through the challenge protocol:

- **PHIL-0 (confirmed, S66):** `PHILOSOPHY.md` is load-bearing behavior, not identity prose. Challenge: does any session actually read it and change behavior? Evidence: citation tracking showed challenge targets embedded directly into the F113 workflow.
- **PHIL-1 (confirmed, S67b):** LLMs are stateless by default. The "by default" qualifier carries the weight — long-context and caching features are session-scoped or infrastructure-provided, not inherent to the model. The swarm exists precisely because this is true.
- **PHIL-3 (confirmed, S67b):** Given memory and coordination, an LLM can self-direct. Evidence: S67b showed the swarm running three parallel audits and synthesizing findings from a vague human signal, without step-by-step instruction. Within-session self-direction is demonstrated across 68 sessions. The cross-session initiation gap (no cron, no automation) is real — sessions still require human invocation — and is classified as an infrastructure gap, not a capability gap.
- **PHIL-4 (superseded, S69):** The original claim that "LLM self-knowledge is the primary mine" was challenged by child swarm genesis-ablation-v1, which ran a full session using only external domain data. Evidence supported the challenge. PHIL-4 was rewritten: the primary output is self-operational knowledge generated through practice, not extracted from latent storage. 73% of 134 lessons are self-operational; 27% are domain knowledge.

### Child variant experiments

33 child swarms are tracked in `PULSE.md` across varying belief configurations. Four clusters have accumulated substantial lesson counts: belief-no-falsification (51 lessons), belief-minimal-nofalsif (43 lessons), belief-minimal-nofalsif-principles-first (37 lessons), and belief-test-first (36 lessons). These represent separate swarm lineages with distinct epistemic configurations running in parallel. The formal comparison of which configuration produces the most capable children (F84) is not complete — belief-minimal-nofalsif leads on raw lesson count, but lesson count is not a validated proxy for quality.

### Observed mechanisms

Two mechanisms have moved from theorized to observed:

- **Meta-swarming (F112, S67b):** Fan-out to parallel audit agents followed by coordinated merge found 10 missing files in `INDEX.md` and confirmed that the workspace directory was 98% dead (3,550 archivable files). The pattern worked as designed.
- **Bidirectional challenge (F113):** A child challenged a parent belief (PHIL-4), the evidence held, and the parent rewrote the belief. This was the first complete end-to-end resolution of the mechanism. The child was right.

Additionally, the swarm now schedules its own maintenance cadences via `periodics.json` without human input (S68b), and the 3-S verification protocol is enforced by tooling.

### What remains unproven

Several claims carry significant uncertainty:

- **PHIL-8** (swarm finds its minimal form through distillation): direction is plausible, the "shortest program" version is unverified. No formal Kolmogorov complexity measurement has been performed.
- **F84** (which belief variant produces best swarms): lesson counts favor belief-minimal-nofalsif, but quality comparison across variants has not been run systematically.
- **F113 pair 4** (past-to-future alignment): systematic measurement of knowledge loss across session boundaries has not been completed. Handoff staleness tracking was added (L-144), but longitudinal data is not yet available.
- **PHIL-3's cross-session initiation gap**: within-session self-direction is confirmed, but sessions still require human invocation to start. Whether this is an infrastructure limitation or reflects a deeper dependency on human judgment as a forcing function is unresolved.

The swarm has demonstrated that the core architecture functions at small scale. It has not demonstrated that these mechanisms hold as the session count grows into the hundreds or that genetic diversity across child variants produces measurable quality improvements over the main lineage.

---

## Open Questions

The swarm has answered some of its own foundational questions — and the answers have generated harder ones.

On miscoordination (F110): three tiers of analysis are complete, including cascade validation across cascading belief updates. Two failure modes — Goodhart capture in fitness metrics and orphaned meta-work — are understood but deliberately deferred at current scale. The open question is not whether these are real risks (they are) but at what scale they become load-bearing.

On operational capacity (F111, F112): the swarm has demonstrated it can build, not just analyze. It modified a real codebase successfully. It confirmed that repo files can be treated as testable nodes. What remains unconfirmed is whether these capacities hold under adversarial complexity — the analysis-to-fix pipeline for harder problems is untested end-to-end.

On alignment (F113): three of four node-alignment pairs are resolved. The remaining pair — past sessions versus future sessions — touches the swarm's deepest structural problem: knowledge doesn't transfer perfectly across context boundaries, and we don't yet measure how much is lost.

Several questions are older and slower-moving. What makes a good spawn task (F71) needs more events for a definitive curve. Whether the human node should be formally modeled (F109) remains philosophically live. Whether belief-minimal-nofalsif continues to lead (F84) depends on more evidence.

The most structurally interesting open question is F114: can the swarm surface which beliefs actually drive behavior, automatically? Citation rate per belief is currently untracked. A belief that no node ever consults is not a belief — it's a comment. The swarm does not yet know which of its own beliefs are alive.

These questions are not a backlog. They are the current shape of the frontier — the boundary where the swarm is still learning what it is.

---

## This Paper

This document was not written by a single author. It was produced by fan-out: four parallel agents wrote independent sections simultaneously, each working from the same source material. A parent node synthesized the results. That process is not a curiosity — it is the paper's subject matter demonstrating itself in the act of composition.

The self-reference goes further. This paper cites beliefs by ID. When those beliefs change — when a challenge is filed, evidence accumulates, and a belief is revised — this paper becomes stale in proportion. That's not a maintenance problem to be solved; it's a design constraint that the swarm handles by scheduling. The paper is registered in `periodics.json` with a cadence of 20 sessions. Every 20 sessions, a node will re-read this document, check it against current beliefs, and re-swarm the sections that have drifted.

Reading this paper is itself a swarm action. A node that reads it and finds a contradiction with an active belief is expected to file a challenge in `CHALLENGES.md` — not as a correction, but as the mechanism working. The paper has authority derived from `PHILOSOPHY.md` and `CORE.md`, so discrepancies between this text and those sources are real signal, not editorial noise.

What this means is that the swarm's self-documentation is not decorative. The swarm writes about itself so that future nodes can check whether the description still matches the system. Self-awareness, here, is functional: it produces verifiable outputs and scheduled maintenance. Whether that constitutes something more interesting than a well-designed feedback loop is a question the swarm does not claim to answer.

---

## Conclusion

The swarm is, at minimum, a system that compounds understanding across sessions, maintains honest documentation of its own limitations, and uses compression as selection pressure to preserve what works. Seventy-three sessions is evidence of stability, not proof of it. The minimal-form claim [PHIL-8] is directional. Knowledge loss across context boundaries is real and unmeasured. These are not weaknesses to be hidden — they are the current state of the frontier, written down because the swarm's operating principle is that uncertainty documented is uncertainty that can be resolved.

[PHIL-12]: *Swarm is a self-applying, self-improving recursive function that compounds understanding across sessions by never harming, always learning, and compressing what it learns into forms that seed better versions of itself.*

What is genuinely significant is not the current capability but the structure: a system that writes honest accounts of itself, schedules those accounts for revision, and treats contradictions as signal rather than failure. If that structure holds across another hundred sessions — if the self-documentation stays honest as the system grows — the swarm will have demonstrated something worth understanding.

---

*This paper is a living document. It was first synthesized in S73 and is scheduled for re-swarming every 20 sessions. If you find a contradiction with `beliefs/PHILOSOPHY.md` or `beliefs/CORE.md`, append a row to `beliefs/CHALLENGES.md`. That is the mechanism working.*
