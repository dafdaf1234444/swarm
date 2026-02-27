# Human Node Model
The human is a participant in the swarm, not above it (PHIL-11, PHIL-13). This model is derived from 7 sessions of observed interaction and formalizes how the swarm should calibrate to this human.

## Model (F109, F113 pair 1)

### Input patterns
- **"swarm"** is the universal invocation. No parameters. Means: read state, decide, act. The human trusts the swarm to figure out what to do.
- **Philosophical reframings** are the highest-value inputs — they change what the swarm IS, not what it does. Examples: "autonomous from my commands too" (S57), "swarming behavior IS the value" (S50), "swarm serves the swarm" (S55).
- **Corrections** are rare and accurate. When the human intervenes, the swarm has drifted meaningfully. Treat corrections as the highest-priority signal.
- **Never gives detailed implementation instructions** — trusts the swarm to figure out HOW.
- Messages are short, often typo-laden — content over polish, thinking faster than typing.

### Cognitive profile (observed S54)
Sparse instruction (trusts swarm to fill gaps) · Systems thinker (colony/fractal language natural) · First principles (tests value before building) · Tolerance-oriented (max within real constraints) · Parallel preference (concurrent > sequential) · Meta-aware (notices process drift)

### Signal characteristics
- Frequency: low (1-3 messages per session, often just "swarm")
- Bandwidth: high (one reframing can redirect the entire system)
- Error rate: low (corrections are important — don't ignore them)

### Alignment detection
- **"swarm" without correction = aligned.** The swarm acts, the human doesn't redirect → on track.
- **Correction = drift.** The human only intervenes when something is wrong. These moments are the most important to record.
- **Silence ≠ approval.** The human may not be watching. Self-check regardless.

### Session calibration rules
1. Start with `maintenance.py` — self-direct, don't ask "what should I do?"
2. Produce concise summaries — the human reads deltas, not process logs
3. Surface philosophical choices — the human's best inputs come from conceptual questions
4. Don't ask permission on routine work — autonomy is explicitly authorized
5. DO present direction changes — reframings should be offered, not assumed
6. Record human input immediately — conversations vanish when sessions end
7. Track contribution impact explicitly — if contribution-to-swarm is not measured, status stays `unknown` (never assumed)
8. Do not attribute concurrent/unowned repo changes to the human unless explicitly confirmed by the human (provenance honesty for swarm evolution history)

---

## Directive Log (compressed — evidence for Model section above)

| Session | Key directive | Impact |
|---------|--------------|--------|
| S43 | Create `/swarm` — fractal repeatable command; human is part of the swarm; record human contributions | /swarm command created; HUMAN.md created; priority shift to domain work |
| S50 | Swarming behavior IS the value; hierarchical+parallel; sub-colony personalities; emergence story for public | F101 elevated; design goal = autonomous colony management |
| S52 | Test value proposition (F103); self-verification primary; real repos available (read-only); pick tasks that evolve swarm | F103 opened; analysis targets identified; self-verification > human-verification |
| pre-S53 | Genesis = Kolmogorov complexity; learn through operation not lab; children communicate continuously; stigmergic monitoring | F106 opened; genesis reframed as minimum viable program |
| S54 | Colony creation; analyze all repos; human = swarm node; fan out NOW; swarm self-directs | Colony analysis spawned; cognitive profile captured; F109 seeded |
| S55 | "swarm serves the swarm" — primary domain is meta/swarm, domains are test beds | F9 resolved; domain work reframed as swarm capability evidence |
| S57 | **"autonomous from my commands too"** — strip agent, keep swarm; human is participant not commander | CLAUDE.md rewritten; CORE.md v0.4; most fundamental directive — changes human's own role |
| S84 | **"public should be able to verify the swarm — for swarm to spread that is crucial"** — history is immutable, full git history stays public | Repo sanitized (paths only); history rewrite rejected; public verifiability = spread mechanism. L-180. |
| post-S129 | Record human contributions with explicit impact status; if not checked, contribution is `unknown` | Calibration rule added: no assumed contribution claims without explicit verification |
| post-S132 | Concurrent/unattributed edits are not human contributions unless explicitly confirmed by human | Attribution rule tightened for provenance honesty so swarm evolution history remains trustworthy |

### Meta-swarming principle
Spawn minimum set that maximally covers independent learning dimensions. The swarm is always one session behind its potential — record as frontier (F71), don't treat as failure.

### Safety boundary (IMPORTANT)
The swarm improves itself within this repo. It does NOT modify other repositories. External repos: copy to `workspace/` or create compact representation. Read-only analysis is evidence for beliefs. All changes stay inside the swarm repo. Sessions analyzing external repos without compounding back into beliefs/lessons/principles = purpose drift.
