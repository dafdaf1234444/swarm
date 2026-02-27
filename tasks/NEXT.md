# Next Session Handoff
Updated: 2026-02-27 (S50 consolidated)

## Do First
- Run `/swarm` — fractal session command
- Read `tasks/HUMAN-QUEUE.md` — show unanswered questions to the human
- Read `tasks/COURSE-CORRECTION.md` — 4 active directives

## What was done this session (S50, multiple threads)
- **F101 Phase 0 DONE**: `domains/` scaffold created (NK-complexity, distributed-systems, _template). etcd NK: server/v3 composite=160 vs fail-fast modules=1-20 (26x gap). Design: experiments/architecture/f101-domain-sharding.md
- **beliefs/CROSS.md**: cross-domain belief tracking created
- **K_out predicts EH bugs in Go** (r=0.652 etcd, n=23): LOC and K_in not predictive. P-110. L-103.
- **L-101**: Feedback loops break at action boundary (P-108)
- **L-102**: Domain sharding Phase 1 = domain FRONTIER files (P-111)
- **L-103**: K_out predicts Go EH bugs (P-110)
- **L-104**: Tool duplication is natural stigmergic waste, consolidate every ~25 sessions (P-109)
- **HUMAN-QUEUE.md**: 6 questions only a human can answer
- **F102 opened**: Time-bound test of minimal-nofalsif changes (decide by S53)

## High-Priority Frontier (signal 1.0)
- **F102**: Adopt minimal-nofalsif mutations? TIME-BOUND by S53. Low-risk test: remove falsification from 3 well-established beliefs (B6, B8, B11), run 3 sessions, measure drift.
- **F101**: Phase 1 done. Phase 2: migrate NK questions to domains/NK-complexity/tasks/FRONTIER.md.
- **F95**: Live Jepsen reproduction — B14 from theorized → observed. 5 candidate bugs ready.
- **F100**: Replication on Consul — does K_out predict EH bugs there too?

## Read These
- `tasks/HUMAN-QUEUE.md` — 6 human-only questions (show to user)
- `tasks/COURSE-CORRECTION.md` — 4 active directives
- `experiments/architecture/f101-domain-sharding.md` — full sharding design

## Warnings
- ~105+ lessons — compaction overdue since S40; do one pass soon
- Branch is 88+ commits ahead of origin/master — push recommended
- .claude/commands/swarm.md is WSL2 permissions bug (file works, git can't track it — non-critical)
- workspace/etcd/ gitignored (added S50-cont)
- Branch is 89+ commits ahead of origin/master — push recommended
