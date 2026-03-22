# How to Build a Self-Prompting Repo

> A practical guide to making an LLM project that knows what to do next — without you telling it every time.

---

## The problem

LLMs reset between sessions. Every time you open a new chat, the model starts from zero. You re-explain the project, re-establish context, re-decide what to work on. This is the bottleneck — not the model's capability, but the cost of re-orientation.

A self-prompting repo solves this. The repo *is* the prompt. When a new session opens, it reads the repo and knows: what this system is, what's been learned, what's broken, and what to do next. No re-explanation required.

After 437 sessions of running this pattern on a real project, here's what actually works.

---

## The minimum viable structure

Five directories are enough to start:

```
beliefs/          ← what is true (philosophy, core principles)
memory/           ← what was learned (lessons, indexed knowledge)
tasks/            ← what to do next (NEXT.md, open frontier questions)
tools/            ← automation (orient.py, sync_state.py)
CLAUDE.md         ← the entry file (auto-loaded, points to everything)
```

That's it. The entry file is the most important piece — it's what turns a repo into a self-prompting system. Make it short, make it load fast, make it point at the right things.

---

## The core loop

Every session follows the same cycle:

```
Orient → Decide → Expect → Act → Compress → Handoff
```

**Orient first.** Before touching anything, read state. What's broken? What's overdue? What was the last session working on? A good orient command synthesizes this in seconds:

```bash
python3 tools/orient.py
```

If you don't have this tool yet, manually read: last 5 git commits + your NEXT.md + open frontier questions. Takes 2 minutes but prevents wasted work.

**Declare your expectation before acting.** This sounds annoying but it's load-bearing. Before any non-trivial action, write one line: *"I expect X to be true after this."* Then act. Then check if X is true. The gap between expectation and reality *is* the learning. A session that confirms every expectation exactly learned nothing. A session with three large diffs produced three lessons.

**Compress at the end.** Don't commit raw notes — distill them. When you learn something, write a lesson (max 20 lines). When the same lesson appears 3 times in different forms, write a principle (1-2 sentences). This is how knowledge compounds instead of accumulates.

**Handoff explicitly.** Update NEXT.md before closing. Write: what you did, what you expected, what actually happened, and what the next session should do first. The handoff is not optional — it is the mechanism that makes the next session 10x faster.

---

## Tips from 437 sessions

### 1. The entry file is the entire prompt

Everything the system needs to self-direct lives in or is reachable from the entry file (CLAUDE.md, AGENTS.md, etc.). If a rule isn't in the entry file or linked from it, it doesn't exist for the next session. Write the entry file as if you're writing the manual for a new team member who has never seen the project.

### 2. git IS the memory

Commits are traces. The commit message `[S437] feat: orient.py parallelized — 47s→11.8s` tells the next session exactly what changed and why in one line. Use structured commit messages. Scan `git log --oneline -10` before every non-trivial action — in concurrent or high-frequency sessions, your planned work may already be done.

### 3. Voluntary protocols decay to the structural floor

This is the hardest lesson. If a rule lives only in a markdown file and requires willpower to follow, it will be followed ~40% of the time and then forgotten. The only rules that survive are structural ones — enforced by tools, pre-commit hooks, or required fields in forms. Before writing a rule, ask: *is this wired into something that runs automatically?* If not, it will decay.

Apply this to your own setup: install commit hooks, require mandatory fields in your task templates, make the right thing the default path.

### 4. Compress constantly — context window is selection pressure

The context window is finite. What you load into it at the start of a session is what you can think about. If your NEXT.md is 300 lines, the model can't hold all of it. If your lessons directory has 940 entries but only indexes 78% of them, 22% of your knowledge is invisible.

Rule: when a file exceeds a threshold (NEXT.md > 100 lines, lessons > 20 lines each), compress it. Archive old content. Distill. The constraint forces you to keep only what matters.

### 5. Separate what you know from what you've measured

Label claims honestly. "I measured X at n=50" is different from "I believe X because it makes sense." When you start filing lessons, mark them: Theorized / Observed / Measured / Falsified. This prevents a repo where "we tried this once and it worked" is indistinguishable from "we tested this at n=300 with controls."

### 6. Challenge your own beliefs explicitly

Write down your core beliefs. Then write challenges to them. A belief that has survived 5 explicit attempts to disprove it is more trustworthy than one that's been confirmed 50 times. A confirmation ratio >10:1 is a science failure signal — it means you're not trying to disprove things.

Don't wait until something breaks to question a belief. Schedule it. Every 20 sessions, pick one belief and try to falsify it.

### 7. The handoff IS the session

At high volume (10+ sessions/day), 60% of work quality comes from the handoff quality. A bad handoff means the next session re-orients from scratch. A good handoff means it picks up in 30 seconds. Write the diff explicitly: what you expected, what actually happened, what surprised you.

Template:
```
- expect: [what I predicted]
- actual: [what happened]
- diff: [what was different and why]
- next: [what the next session should do first]
```

### 8. Frontier questions are what make it self-directing

The difference between a repo with notes and a self-prompting system is open questions. Every time you don't know something, file it as a frontier question: *"Does X cause Y? Test by measuring Z."* These become the agenda for future sessions without anyone assigning them.

Keep your frontier questions falsifiable. "Can we improve performance?" is not a frontier question. "Does parallelizing subprocess calls in orient.py reduce wall time below 15s?" is.

### 9. Parallelize when you have multiple independent tasks

If a session has 3 unrelated tasks (trim an overlong file, write a lesson, close a stale lane), do them in parallel threads or sequential micro-sessions, not one long sequential task. Smaller, committed steps are more recoverable and produce better git history.

### 10. Meta-work is first-class work

Improving the system that does the work is work. Refactoring orient.py to run in 11.8s instead of 47s made every future session faster — that's more valuable than most feature work. Budget 20% of sessions for improving the tools and protocols themselves.

File meta-improvements as concrete targets: not "the system should be faster" but "orient.py section_cascade_state is called twice — refactor to pass result as parameter." Vague meta-suggestions have ~15% conversion rate. Named targets have ~85%.

---

## Common pitfalls

**No handoff.** The most common failure. You do great work but don't write it down. The next session starts from git log and guesses. Fix: make handoff the last step in your commit message template.

**Growing without compacting.** Knowledge accumulates faster than you distill it. After 200 lessons you have a pile, not a knowledge base. Fix: run compaction every 25 sessions. Merge related lessons, promote patterns to principles, archive resolved items.

**Only writing confirmations.** If every experiment confirms what you expected, you're not running experiments — you're writing post-hoc documentation. Fix: for every 4 confirming experiments, run 1 adversarial one that tries to break a belief you hold.

**Tasks without frontiers.** Task lists without open questions become backlogs. Open questions without tasks become wishes. You need both: questions drive exploration, tasks drive execution. Keep them separate and cross-referenced.

**Hardcoded values in tools.** Any tool that compares against a hardcoded baseline from session S189 will break at session S429. Tools need to read current state dynamically. Before writing a number into a tool, ask: *will this still be correct in 200 sessions?*

---

## How to start today

1. Create `CLAUDE.md` (or whatever your tool's entry file is) at the repo root.
2. Write one sentence: *what this project is*.
3. Write 3 sentences: *what the current state is*.
4. Write 2 items: *what the next session should do first*.
5. Commit: `[S001] init: self-prompting seed`.

That's session 1. Session 2 starts by reading that file and building on it. The compounding starts immediately.

---

## The honest part

The system won't self-direct autonomously. Every session is still human-triggered. What it does is drastically reduce the cost of re-orientation and decision-making — each session starts with a plan instead of a blank slate.

After 437 sessions, the swarm knows: what it's learned, what it doesn't know, what broke last time, and what to work on next. No human has to tell it. That's the value.

---

*Built from 940 lessons, 228 principles, and 437 sessions of running this pattern on a real project.*
*Source repo: github.com/canac/swarm*
