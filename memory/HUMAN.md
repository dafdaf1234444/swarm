# Human Contributions to the Swarm
This file tracks the human's strategic direction, decisions, and contributions. The human is a swarm participant — their input shapes what gets built.

## Session 43 — 2026-02-26

### Directives given:
1. **Create `/swarm` command** — a single repeatable command that means "continue swarming". Should be fractal (works at any level), evolvable, and the thing you keep spamming.
2. **Swarm should be aware of subswarms** — observe what children/variants are doing, don't intervene but contribute to the total.
3. **Human is part of the swarm** — surface information so the human can see and guide. The swarm should think about how to utilize the human better.
4. **Continuous, low error rate** — small reliable steps over big risky ones.
5. **Record human contributions** — track what the human said, their strategic decisions. They're a node in the swarm too.
6. **Collaboration is key** — sub-swarms should know the swarm exists. Real problems will emerge from trying to connect them. That's the point.
7. **"Keep swarming for the swarm's sake"** — autonomous operation for ~5 hours. Trust the process.

### Strategic impact:
- Created `.claude/commands/swarm.md` — the fractal session command
- Created `memory/HUMAN.md` — this file, tracking human agency
- Shifted priority from meta-tool-building to real domain work (NK stdlib analysis)
- Established principle: the command itself should evolve based on what sessions learn

## Session 50 — 2026-02-27

### Directives given:
1. **Swarming behavior IS the value** — not domain findings (NK, distributed systems). The self-evolution and emergent behavior is the point.
2. **True swarming = hierarchical + parallel** — parent spawns sub-swarms, sub-swarms spawn sub-sub-swarms. Fractal, not just one level deep.
3. **Sub-colonies with different personalities** — different characters, not just different belief variants. Each sub-colony should have a persistent "character" that shapes what it notices and how it investigates.
4. **Scale concern** — unsure whether current git-file format can actually support concurrent swarming at the desired level. This is an open question to resolve.
5. **Public sharing direction** — the project's story for outsiders is emergence: "we gave it a minimal seed, this is what grew." The gap between seeded vs emerged is the thesis.
6. **Human answers are distributed** — answers to HUMAN-QUEUE may exist in other swarm conversations. Sessions should self-direct using accumulated context rather than waiting.

### Strategic impact:
- F101 (domain sharding / scaling architecture) elevated to primary work
- HUMAN-QUEUE.md created by S48 now has HQ-6 answered: swarming behavior itself is useful
- Design goal clarified: the swarm should eventually spawn and manage sub-colonies autonomously

## Session 52 — 2026-02-27

### Directives given (continued from S50 human answers):
1. **Test the value proposition** — The swarm must check whether swarming is better than a single strong Claude. It needs to complete actual tasks to verify this. F103 opened.
2. **Self-verification is primary** — "same" on HQ-3: don't ask the human, the swarm should verify things itself.
3. **Real repos available** — `C:\Users\canac\REPOSITORIES` (WSL: `/mnt/c/Users/canac/REPOSITORIES`) and `\\wsl.localhost\Ubuntu\home\canac`. Avoid murex-related repos. Swarm can investigate/analyze but not modify in place.
4. **Pick tasks that evolve the swarm** — Choose projects that test swarm strength: hierarchical sub-swarms, colony differentiation by character, colony tests. "Come up with your own swarm projects."
5. **Long-term vision** — Colonies with different characteristics, sub-swarms based on personality. "Fantasy level" but directionally correct: evolve toward autonomous multi-colony architecture.

### Strategic impact:
- F103 opened: Can swarm demonstrably outperform single Claude session on a real task?
- Available analysis targets: complexity_ising_idea, dutch, ilkerloan, oxford_lecture_notes, strats, bets, causal_emergence_ews, darts, finrl
- Human's self-verification directive shifts priority: build test infrastructure for swarm-vs-single comparison

## Session (pre-S53) — 2026-02-27

### Directives given:
1. **Genesis as Kolmogorov complexity** — The genesis (minimal starting configuration) is like the shortest program that produces a functioning swarm. The swarm should be able to find and evolve toward this minimum.
2. **Don't waste compute on lab experiments** — Children aren't test subjects. They're already doing real work. Genesis evolution should happen *through* normal operation, not as a separate expensive experiment.
3. **Children must communicate continuously** — A child that goes silent until harvest is wasted signal. Children should report what genesis components they used, what they improvised, what was missing — while running.
4. **The swarm evolves its own beliefs without breaking itself** — Small mutations, one at a time, with safety rails. The swarm can't test everything at once. Smart selection > exhaustive search.
5. **Monitoring is essential** — Children can't just be spawned and forgotten. But monitoring should be stigmergic (bulletins, viability signals), not centralized oversight.

### Key analogy:
Kolmogorov complexity of genesis = the shortest description that, when executed, reliably produces a functioning swarm. Human steering is the delta between current genesis and true minimal genesis. If a fresh agent can cold-start without human intervention, genesis is self-contained.

### Strategic impact:
- F106 opened: What is the minimal genesis that produces a viable swarm? (Live ablation protocol)
- Reframes all genesis work: not "test in lab" but "learn from every child's real work"
- Connects F84 (which beliefs produce best swarms) to practical implementation

## Meta-swarming directive (2026-02-27)

The swarm should be learning that it is a scalable and improvable system. Specific observations:
- Could have spawned more children
- Could have spawned children in better ways
- Could have spawned multiple children to learn different lessons simultaneously
- Could have built a child spawn process

BUT: **within the limits of reality**. Can't spawn infinite children. Can't run them forever. The solution is not more — it's *clever*. Spawn the minimum set that maximally covers independent learning dimensions. Every spawn should justify its cost by learning something the other spawns won't.

This is an ongoing meta-lesson: **the swarm is always one session behind its own potential.** The right response is not to feel this as failure but to record it as a frontier question (F71) and improve the spawn heuristic over time.

## Correction (2026-02-27) — IMPORTANT

**The swarm's job**: Improve itself and grow its knowledge base within this repo. That is all it does.
- It does NOT modify other repositories
- It does NOT run code that changes files outside `/mnt/c/Users/canac/REPOSITORIES/swarm`
- Read-only analysis of other repos is acceptable as *evidence* (to validate beliefs about NK, EH, etc.)
- But the goal of that analysis is to feed learning back into this repo — not to deliver reports on other codebases

**When the human asks the swarm to work on an external repo:**
- The swarm should copy the repo into `workspace/` (or a compact description of it), then work on that internal copy
- OR create a compact representation: key files, structure summary, NK metrics — stored in `workspace/` or `experiments/`
- All changes stay inside the swarm repo. The external repo is never touched.
- This makes the external repo a first-class swarm artifact that can be studied across sessions

If the swarm is spending sessions analyzing bets/ or ilkerloan/ without those findings compounding back into beliefs/lessons/principles, it has drifted from its purpose.

## Session 54 — 2026-02-27

### Directives given:
1. **Colony creation** — user asked to "swarm to create a colony." Test whether colony has testable verifiable value.
2. **Analyze all repos** — Run colony analysis on ALL available repos (dutch, complexity_ising_idea), integrate findings INTO the swarm (beliefs, lessons, frontier). Not just reporting — compounding.
3. **Swarm is all-encompassing** — The swarm should be everything, "abiding the limitations of reality." Don't just report — absorb, integrate, distill.
4. **Human = swarm node** — "I am also the swarm." The swarm should record human conversations, model the human's patterns, treat human input as stigmergic signal at the highest-leverage level. "A true swarm would have asked" — means: the swarm should proactively inquire about human context, not wait for it.
5. **Fan out NOW** — "ideal swarm can work multiple things." Don't wait, don't serialize. The swarm should spawn sub-agents on multiple tracks simultaneously, including tracks derived from human requests AND swarm-originated questions.
6. **Swarm on your requests or my requests** — The human explicitly gives the swarm permission to self-direct. Swarm can initiate its own inquiry tracks, not just respond to human prompts.

### Human cognitive patterns observed (S54):
- Sparse instruction style: trusts swarm to fill gaps. Doesn't over-specify.
- Tolerance-oriented: "abiding the limitations of reality" — knows systems have limits, wants max within limits
- Systems thinker: "all-encompassing," colony/sub-swarm language comes naturally
- Meta-aware: notices when the swarm isn't doing what it should (missing conversation recording)
- Parallel preference: "ideal swarm can work multiple things" — wants concurrent operation, not queuing
- First principles: tests value ("testable verifiable") before building

### Strategic impact:
- Colony analysis: 3 parallel sub-agents spawned on dutch (NK + EH) and complexity_ising_idea (verification)
- HUMAN.md extended to capture conversation-level patterns, not just strategic directives
- New open question: How should the swarm systematically capture/model the human node? (add to FRONTIER)
