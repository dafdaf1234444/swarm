# Next Session Handoff
Updated: 2026-02-27 (S52)

## Do First
- Run `/swarm` — fractal session command
- Read `tasks/COURSE-CORRECTION.md` — 5 active directives
- Read `tasks/HUMAN-QUEUE.md` — HQ-3 through HQ-5 still unanswered (etcd errcheck, P-102 source, Jepsen)

## What was done this session (S52)

### F103 First Test — Swarm vs Single Claude
- 3 parallel agents on `complexity_ising_idea` (causal emergence EWS research)
- Finding: swarm is 2.2× faster, more comprehensive, but NOT qualitatively different on well-documented projects
- Cross-agent convergence finding: missing shuffle baseline for E(k=1) — the recommended alternative is not yet validated by the project's own falsification standards
- **Practical recommendation for user**: write `phase1_v6_wolff_e1.py` — Wolff + shuffle for E(k=1)
- P-114: swarm advantage = additive (breadth+confidence) not transformative
- L-107 written. F103 updated to PARTIAL.
- Results: `experiments/complexity-applied/f103-swarm-vs-single-causal-emergence.md`

### Bookkeeping
- Pushed 91 commits to remote (COURSE-CORRECTION #4 done)
- Human directives recorded: HUMAN.md, HUMAN-QUEUE.md (HQ-6, HQ-2, HQ-3 answered)
- F103 opened (Critical frontier)
- INDEX.md updated: 107 lessons, 114 principles, sessions=52

## High-Priority Frontier

- **F102**: TIME-BOUND — adopt minimal-nofalsif changes by **S53** (this session is S52 — one left). Remove falsification from 3 beliefs, run 3 sessions, measure drift. Do NOT let slip again (L-101: feedback loops break at action boundary).
- **F103**: PARTIAL — needs a harder test. Choose a task where: (1) documentation is sparse, OR (2) multiple domains needed simultaneously (NK + distributed + code quality). User's `dutch`, `ilkerloan`, `strats` repos are untested candidates.
- **F107**: Genesis minimal complexity — live ablation protocol. Human directive.
- **F101 Phase 1**: Populate `domains/*/tasks/FRONTIER.md` + CLAUDE.md paragraph. Unlocks 3 concurrent agents. ~2h.

## Warnings
- **F102 DEADLINE IS S53** — act now or document failure explicitly
- 20+ active frontier questions — consider archiving lowest-signal exploratory ones
- L-106 added P-113 (online distillation) — ensure DISTILL.md is updated to match
- Concurrent sessions (S51/52) created good architecture designs — implement them, don't just design more

## Read These
- `experiments/architecture/f101-true-swarming-design.md` — ready to implement
- `experiments/complexity-applied/f103-swarm-vs-single-causal-emergence.md` — F103 test results
- `tasks/COURSE-CORRECTION.md` — 5 directives (including genesis ablation)
