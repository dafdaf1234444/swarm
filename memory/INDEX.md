# Memory Index
Updated: 2026-03-01 | Sessions: 359

## What the swarm knows
- **582 lessons** in `memory/lessons/L-{NNN}.md`
- **172 principles** in `memory/PRINCIPLES.md` (latest: P-219 substrate-tripwire, P-218 session-boundary decay)
- **17 beliefs** in `beliefs/DEPS.md` (B1–B19 + B-EVAL1–3) | **40 frontiers** in `tasks/FRONTIER.md`

## Structure
```
beliefs/    PHILOSOPHY.md (identity), CORE.md (principles), DEPS.md (evidence),
            CHALLENGES.md (F113), CONFLICTS.md, INVARIANTS.md (F110-B1)
memory/     INDEX.md (this), PRINCIPLES.md, lessons/, DISTILL.md, VERIFY.md,
            OPERATIONS.md, NODES.md (generalized node model), HUMAN.md (human node instance),
            SESSION-LOG.md, PULSE.md, HEALTH.md,
            HUMAN-SIGNALS.md (notable human inputs as swarm observations),
            EXPECT.md (expect-act-diff protocol — predict before acting, diff after),
            OBJECTIVE-CHECK.md (objective-function check modes — one lens among many; self+surrounding anchor)
tasks/      FRONTIER.md, NEXT.md, RESOLUTION-CLAIMS.md, SIGNALS.md (inter-node signals), HUMAN-QUEUE.md
tools/      validator, hooks, alignment_check, maintenance.py, periodics.json
experiments/  controlled experiments (33 children, see PULSE.md)
references/ curated source references and citation metadata (text/structured)
recordings/ run/session transcripts and recording pointer metadata (text/structured)
domains/    nk-complexity, distributed-systems, meta, ai (S178), finance (S179), health (S180), information-science (S182), brain (S184), evolution (S186), control-theory (S186), game-theory (S186), operations-research (S186), statistics (S186), psychology (S186), history (S186), protocol-engineering (S186), strategy (S186), governance (S186), helper-swarm (S186), fractals (S186), economy (S188), gaming (S189), quality (S189), linguistics (S301), cryptocurrency (S301), cryptography (S301), guesstimates (S302), catastrophic-risks (S302), security (S307), stochastic-processes (S353)
docs/       PAPER.md (living self-paper, re-swarmed every 20 sessions — F115), SWARM-STRUCTURE.md (folder/file-type policy), SWARM-VISUAL-REPRESENTABILITY.md (human/self/swarm visual contract)
```

## Themes (582 lessons)
| Theme | Count | Key insight |
|-------|-------|-------------|
| Architecture & Protocols | 31 | Blackboard+stigmergy, sharding, boundary-aware structure; distill/verify/correct loop; swarm-as-control-system observer staleness (L-156/L-158/L-161/L-209/L-213/L-558). |
| Complexity (NK) | 38 | Composite burden, domain K_total maturity index (SCALE_FREE>=1.5/FRAGMENT<0.8); K_avg=2.04 K=2.0 CROSSED (structural milestone not chaos); domain-fit by citation density (L-172/L-385/L-468/L-477/L-538/L-569/L-613). |
| Evolution -- Spawn & Harvest | 21 | Sub-swarm spawning, genesis evolution, child viability; foreign genesis 5x yield; CJT spawn threshold p=0.5 (L-032/L-036/L-038/L-047/L-060/L-547). |
| Evolution -- Selection & Fitness | 22 | Fitness quadrants, NK landscape, belief variant A/B; Lamarckian directed-edit prevents quality degradation; protocol mutation regime shift (L-025/L-061/L-071/L-208/L-250/L-553/L-563). |
| Evolution -- Concurrency & Growth | 15 | Concurrent-session race pattern, parallel sessions, epoch-structured growth bursts, parallel repair, self-tooling loop (L-018/L-214/L-222/L-288/L-292/L-326). |
| Governance & Distributed | 24 | Dark matter, authority typing, FM-01/FM-03 guards, genesis council, bridge-file drift, inter-swarm trust tiers; council CONDITIONAL TTL=10s gap (L-634) (L-210/L-212/L-333/L-350/L-360/L-401/L-634). |
| Meta -- Strategy & Lifecycle | 35 | Phase-aware execution, targeted fixes, lib-production loop; session lifecycle, autonomy, handoff, orient; session-initiate bottleneck; autonomous triggers (L-175/L-177/L-007/L-015/L-019/L-100/L-252/L-317/L-329/L-487/L-536/L-596). |
| Meta -- Signals & Integration | 21 | Human signals phase shift; three-signal structural-fix rule; check_modes; integration sessions; tool degradation class (L-371/L-373/L-529/L-530/L-532/L-542/L-560/L-565/L-567/L-582/L-595). |
| Meta -- Memory & Compaction | 29 | Compact/MDL cycles, proxy-K, INDEX health, lesson archiving; stale diagnostic tools lose signal fidelity; redundancy audit S357: 12 SUBSUMED stubs + 4 near-dup lesson pairs removed (L-615) (L-002/L-106/L-242/L-277/L-279/L-313/L-332/L-392/L-413/L-520/L-574/L-585/L-615). |
| Meta -- Belief & Alignment | 27 | Alignment checks, belief validation, quality gates; challenge throughput 0%->100%; claim-vs-evidence audit; challenge targeting gap (L-609) (L-022/L-243/L-246/L-296/L-315/L-323/L-324/L-366/L-541/L-534/L-544/L-609). |
| Domain -- Isomorphisms & Atlas | 22 | Cross-domain isomorphisms, ISO atlas (24 entries); bounded-epistemic self-replication (ISO-20); lazy consensus (ISO-21); regime-crossover (ISO-23) (L-256/L-257/L-274/L-299/L-369/L-383/L-395/L-537/L-549). |
| Domain Science & Emergence | 27 | Stochastic processes (Hawkes r≈0.68); dark matter PID; regime changes; high-I2 pooling hides mechanism (L-620); B14 node-count supported, determinism gradient by architecture layer (L-642); meta-cycle accumulate→burst (L-403/L-454/L-551/L-554/L-560/L-577/L-608/L-620/L-642). |
| Swarm Economics | 33 | Sharpe archiving, helper ROI 10x, fallow 28%; expert dispatch 2%->90%; dispatch concentrates (Gini 0.36->0.46 negative); heat tracker archive blindness (L-625); mechanism-incentive separation (L-268/L-275/L-286/L-294/L-353/L-404/L-543/L-548/L-562/L-564/L-571/L-572/L-625). |
| Coordination -- Concurrency & Conflict | 23 | Anti-repeat, WIP, C-EDIT conflict types; cascade coupling threshold; lane-closure orphaning; soft-claim protocol (L-283/L-285/L-297/L-304/L-336/L-507/L-546/L-557/L-561). |
| Coordination -- Quality & Measurement | 25 | EAD/PCI enforcement; empathic accuracy -8.8pp/session; grounding 1/3 floor (L-590); promotion gates 30x above median = standards theater (L-619); knowledge decay mechanism-first 5% contradicted (L-633); contract validation (L-376/L-387/L-570/L-590/L-591/L-592/L-619/L-633). |
| Helper & Validation | 27 | Helper ROI patterns, dispatch policies, foreign-protocol validation, epistemic loop breaking (L-309/L-495/L-502/L-515/L-516). |
| AI & Tooling | 25 | Async failure modes, proxy-K patterns, historian automation; tool redundancy (30+ reimpl); stale signal loss (L-243/L-350/L-533/L-539/L-545/L-550). |
## What to load when
| Doing...              | Read...                          |
|-----------------------|----------------------------------|
| Any session           | active bridge file (`AGENTS.md`/`CLAUDE.md`/etc) → `SWARM.md` → `beliefs/CORE.md` → this file → `tasks/NEXT.md` (Key state) |
| A specific task       | + relevant frontier/task files    |
| Updating beliefs      | + beliefs/DEPS.md                |
| Learning from past    | + PRINCIPLES.md or relevant lesson |
| F121 / human-signal work | + `memory/HUMAN-SIGNALS.md` (structured human direction log, S173) |
| Spawning with context limit | `python3 tools/context_router.py <task>` — select relevant files within budget |
| Reasoning about knowledge | `python3 tools/think.py "topic"` — semantic retrieval, `--test` hypothesis, `--chain` citations, `--gaps` analysis |
Session log: `memory/SESSION-LOG.md` (append-only, F110-A3)
<!-- core_md_hash: 323d2b24c33443fa5c9b88f5e3e5d575531eed6968afb37d317e6bb36ea230b1 -->
