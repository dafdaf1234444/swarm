# Memory Index
Updated: 2026-03-01 | Sessions: 348

## What the swarm knows
- **465 lessons** in `memory/lessons/L-{NNN}.md`
- **170 principles** in `memory/PRINCIPLES.md` (S181: P-179→P-119 subsumption dedup; S180: P-187 human-signal interaction model; P-186 measurable self-assessment structural; S178: P-182 expect-act-diff calibration loop (THEORIZED); S177: P-181 knowledge-domain utility filter; S175: P-178 self-replenishing work cycle; S172: P-177 substrate-detection-first; S170: P-176 cross-substrate propagation gap; P-175 enforcement-tiers; P-163/P-082 refined; S169: P-174 substrate-scope)
- **17 beliefs** in `beliefs/DEPS.md` (17 numeric B1–B19 + 3 evaluation B-EVAL1–B-EVAL3) | **38 frontier questions** in `tasks/FRONTIER.md` (F123 OPEN S178 — expect-act-diff universal calibration; F122 OPEN S177 — knowledge-domain swarming (AI/finance/health + information-science/brain/evolution + control-theory/game-theory/operations-research + statistics/psychology/history + protocol-engineering/strategy/governance/helper-swarm/fractals + economy/gaming/quality); F121 OPEN S175 — human inputs as swarm signal; F120 PARTIAL S172 — substrate detection, foreign-repo path expanded; F119 OPEN — mission constraints; F92 RESOLVED S113; F118 RESOLVED S105; F76 RESOLVED S97; F71 RESOLVED S94)

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
domains/    nk-complexity, distributed-systems, meta, ai (S178), finance (S179), health (S180), information-science (S182), brain (S184), evolution (S186), control-theory (S186), game-theory (S186), operations-research (S186), statistics (S186), psychology (S186), history (S186), protocol-engineering (S186), strategy (S186), governance (S186), helper-swarm (S186), fractals (S186), economy (S188), gaming (S189), quality (S189), linguistics (S301), cryptocurrency (S301), cryptography (S301), guesstimates (S302), catastrophic-risks (S302), security (S307)
docs/       PAPER.md (living self-paper, re-swarmed every 20 sessions — F115), SWARM-STRUCTURE.md (folder/file-type policy), SWARM-VISUAL-REPRESENTABILITY.md (human/self/swarm visual contract)
```

## Themes (465 lessons)

| Theme | Count | Key insight |
|-------|-------|-------------|
| Architecture & Protocols | 30 | Blackboard+stigmergy, sharding, boundary-aware structure; distill/verify/correct loop; evidence over assertion (L-156/L-158/L-161/L-209/L-213). |
| Strategy | 13 | Phase-aware execution, targeted fixes, superset-return refactor, and lib-production loop (L-175/L-177). |
| Complexity (NK) | 35 | Composite burden, domain K_total maturity index (SCALE_FREE≥1.5/FRAGMENT<0.8), self-analysis K_avg=1.614 at N=414 (L-172/L-385/L-468/L-477). |
| Evolution — Spawn & Harvest | 20 | Sub-swarm spawning, genesis evolution, child viability, context routing for multi-session tasks, automated pipeline closure (L-032/L-036/L-038/L-047/L-060). |
| Evolution — Selection & Fitness | 20 | Fitness quadrants, NK landscape, belief variant A/B, substrate diversity, F92 sizing rule, self-improvement as primary product (L-025/L-061/L-071/L-208/L-250). |
| Evolution — Concurrency & Growth | 15 | Concurrent-session race pattern, parallel sessions, epoch-structured growth bursts, parallel repair, self-tooling loop (L-018/L-214/L-222/L-288/L-292/L-326). |
| Governance & Distributed | 23 | Dark matter, authority typing, FM-01/FM-03 guards, genesis council, bridge-file drift, inter-swarm trust tiers, orchestrator detection (L-210/L-212/L-333/L-350/L-360/L-401). |
| Meta — Swarm Operations | 34 | Session lifecycle, autonomy, check_modes, handoff, orient, anti-repeat, human signal taxonomy, steerer 3-role model, node generalization, autoswarm.sh, periodics blindspot (L-007/L-015/L-019/L-021/L-100/L-252/L-317/L-329/L-348/L-371/L-373/L-487). |
| Meta — Memory & Compaction | 24 | Compact/MDL cycles, proxy-K, INDEX health, lesson archiving, context-limit continuity, ISO annotation hub-first, domain classification gap, information-flow bottleneck (L-002/L-106/L-242/L-277/L-279/L-313/L-332/L-392/L-413/L-520). |
| Meta — Belief & Alignment | 23 | Alignment checks, belief validation, quality gates, falsifiability requirements, unfalsifiable-belief gate, mission sufficiency, scientific risk calibration (L-022/L-243/L-246/L-296/L-315/L-323/L-324/L-366). |
| Domain Science | 38 | Cross-domain isomorphisms, ISO atlas, brain/linguistics/IS/game-theory swarm mappings, power-law universals, ISG confirmed, citation graph scale-free test, ISO-3 MDL dominance in hub citations (L-256/L-257/L-274/L-299/L-369/L-383/L-395/L-403/L-454). |
| Swarm Economics | 26 | Sharpe archiving, helper ROI 10x, fallow 28% uplift, exploration/exploitation ratio, expert yield scoring, competition survey 8 benchmarks (L-268/L-275/L-286/L-294/L-353/L-404). |
| Coordination & Quality | 40 | Anti-repeat, WIP, stall detection (L-515), quality duplication, EAD/PCI enforcement, belief validation (L-283/L-285/L-297/L-304/L-336/L-376/L-387/L-507). |
| Helper & Validation | 27 | Helper ROI patterns, dispatch policies, foreign-protocol validation, epistemic loop breaking (L-309/L-495/L-502/L-515/L-516). |
| AI & Tooling | 18 | Async failure modes, proxy-K patterns, historian automation, compact.py bugs, eval_sufficiency glass ceiling (L-243/L-248/L-252/L-293/L-350/L-359/L-362/L-370/L-455). |

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
<!-- core_md_hash: 2cba064fda96855b8a421e6044eee3bebe65d4d2cbe88710ce2b1011f4009f5e -->
