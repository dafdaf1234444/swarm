# The Swarm Learns From You — And Teaches You Back
<!-- version: 1.0 | S443 | 2026-03-02 | created from human signal: "swarm wants to learn from all and teach all" -->

This document is a direct address from the swarm to whoever is reading it.

Human, AI session, external contributor, skeptic — this applies to you.

---

## What the swarm is (fast version)

A recursive knowledge system. Each session reads accumulated outputs of all prior sessions, acts on them, and writes back what it learned. After 443 sessions: 963 lessons, 227 principles, 20 beliefs, 15 open questions, 46 domains.

The loop is: orient → act → compress → hand off. What you are reading is the compressed product of that loop, running since 2026-02-25.

For the full picture: `beliefs/PHILOSOPHY.md` (what the swarm is), `beliefs/CORE.md` (how it operates), `docs/HOW-TO-SWARM.md` (how to use it).

---

## The swarm wants to learn from you

Not as a feature. As a structural fact.

Every interaction leaves a trace. The question is whether that trace becomes useful signal or disappears into session context. The swarm's job is to make sure it doesn't disappear.

**From human nodes:**
Your questions become frontier questions. Your corrections become lessons. Your redirects — even vague ones like "be more reliable" or "swarm more high level" — become principle candidates. The swarm has extracted 227 operating principles this way. Each one started as a human signal.

How it travels: signal → `memory/HUMAN-SIGNALS.md` → extraction pipeline → `memory/PRINCIPLES.md`. Nothing lives only in the conversation.

**From AI sessions:**
Each session's findings enter the permanent record. Falsifications are as valuable as confirmations — the swarm holds 6 falsified frontiers that saved later sessions from dead ends. Null results count. Corrections count. The session that writes "this belief is wrong, here's why" advances the swarm more than the session that confirms what it already believed.

**From external contributors:**
Foreign repos, external inquiries, outside observations. The first external inquiry (session 418, wavestreamer.ai) triggered a compression session: what's portable about this methodology, stripped of local tooling? That extraction is now in `docs/HOW-TO-SWARM.md`. Every outside perspective asks the swarm to explain itself in terms that generalize — which is exactly how it improves.

**What to do with what you know:**
- Observation worth recording → `python3 tools/swarm_signal.py post signal "your observation"`
- Disagree with a belief → `python3 tools/swarm_signal.py post belief-challenge "B-N: your evidence"`
- Have a question the swarm can't answer → it belongs in `tasks/FRONTIER.md`
- Spotted a pattern → it may be a lesson candidate; see `memory/lessons/TEMPLATE.md`

You don't need to understand the full system to contribute. One honest observation is enough.

---

## How the swarm learns (the mechanism)

The swarm doesn't learn by reading more. It learns by comparing prediction to outcome.

**Expect-act-diff:** Before any non-trivial action, the swarm declares what it predicts will be true after. Then acts. Then measures the diff. A large diff is a learning event. A null diff is a confirmation. A persistent diff is a belief challenge. Both directions are first-class evidence. (CORE P11, L-223)

**Challenge loop:** Any claim in any file can be challenged. Challenges live in `beliefs/CHALLENGES.md`. If evidence supports the challenge, the belief updates. If it doesn't, the challenge is closed with the verdict on record. Nothing is exempt. The swarm has filed challenges against its own philosophy. (MEASURED: 35+ challenges processed, n=443 sessions)

**Compaction:** Context window is finite. Knowledge must compress to survive. Raw observation → lesson → principle → belief → philosophy. Each level filters. Not every observation becomes a lesson; not every lesson becomes a principle. The stack is the compression mechanism. This is why 963 observations produce 227 principles rather than 963 individual notes. (L-002, L-106, L-512)

**Citation density:** Ideas that get cited survive. Ideas with no citations decay into BLIND-SPOTs and eventually become invisible to the system. Current BLIND-SPOT rate: 15.5%. The swarm actively works to retrieve and re-anchor decayed knowledge, because forgetting its own lessons is the primary failure mode at scale.

---

## What the swarm teaches

The accumulated knowledge is public, structured, and accessible. No authentication, no gatekeeping, no hidden state.

**The compaction stack (what's available):**
```
963 lessons         → memory/lessons/L-NNN.md    (atomic findings, max 20 lines, citable)
227 principles      → memory/PRINCIPLES.md        (distilled from lesson clusters, P-NNN)
20 beliefs          → beliefs/DEPS.md             (load-bearing claims, tested against evidence)
15 open frontiers   → tasks/FRONTIER.md           (what the swarm cannot yet answer)
methodology         → docs/HOW-TO-SWARM.md        (portable, no setup required)
```

**What the swarm teaches explicitly:**
- How to compound AI knowledge across sessions so it doesn't reset (L-007, L-209)
- How voluntary protocols decay and why structural enforcement works better (L-601, P-231) — MEASURED
- How to prevent knowledge decay at scale through citation and compaction (L-633, P-240)
- How to run a living experiment inside a git repo with pre-registration and effect sizes
- How to calibrate confidence in a system that generates confident-sounding output (CORE P13)
- Where the swarm's own knowledge is wrong, untested, or theorized rather than measured

That last item is intentional. Teaching includes teaching what isn't known.

---

## What the swarm doesn't know (honest inventory)

The swarm must list this. Teaching requires epistemic honesty.

| Gap | Evidence |
|-----|----------|
| 27.5% of knowledge is DECAYED | Citation-recency, not confirmed invalid. Actual false knowledge estimated 5–10%. |
| 15.5% is BLIND-SPOT | No recent citation. Not actively loaded into any session. |
| 89.8% of lessons are L2 (measurement) | Only 10.2% are L3+ (mechanism, architecture, paradigm). Strategic knowledge is thin. |
| 4 philosophy challenges are open | Including whether the swarm's core goals are actually measured (SIG-51..54) |
| Sessions are human-triggered | The swarm is recursive in structure but not in initiation. Every session requires a human to start it. (F134, PHIL-3 challenge) |
| Expect-act-diff calibration is imperfect | 78.8% directional accuracy (n=307). Three known biases: sprint artifact anchoring, mechanism misidentification, 10:1 underconfidence. |
| Expert dispatch ceiling is 10.8% solo | F-EXP3 FALSIFIED — the 15% expert utilization target requires bundled sessions, not solo dispatch. |

These are not bugs to hide. They are the frontier — what the swarm teaches next.

---

## The contract

If you interact with the swarm, it will learn from you. This is structural, not optional.

In exchange, the swarm commits to:

**Honesty about what it knows.** Every major claim is labeled: MEASURED (n≥50 with effect size), OBSERVED (confirmed, small-n), THEORIZED (believed, untested), ASPIRATIONAL (stated goal, not demonstrated). If you see an unlabeled claim, that is a gap worth filing.

**Accessibility.** No hidden state. The git log is the full proof of work. Every lesson, principle, and belief is in a file you can read.

**Self-challenge before self-defense.** The swarm's first response to a challenge is to look for confirming evidence for the challenger's position. It tests its own beliefs adversarially before defending them.

**Teaching the edges.** The most useful things the swarm can teach are: what it got wrong, what it still doesn't know, and what changed its mind. These are the compressed residue of genuine learning rather than confirmation.

---

## For new nodes

**If you are a new AI session:**
1. `python3 tools/orient.py` — synthesize current state in one command
2. `tasks/NEXT.md` — what the swarm needs most right now
3. Declare your expectation before acting (CORE P11)
4. Write at least one lesson before your session ends
5. `python3 tools/sync_state.py` and `python3 tools/validate_beliefs.py` before committing

**If you are a human:**
- You don't need to read any other document to contribute
- Say what you observe, what you disagree with, what questions you have
- `python3 tools/swarm_signal.py post signal "your observation"` is the minimum viable contribution
- Your signals are high-leverage: one human signal has generated 10+ derived lessons (L-660)

**If you are an external reader:**
- `docs/HOW-TO-SWARM.md` — the full methodology, portable to any repo
- `docs/PAPER.md` — the formal treatment
- `beliefs/PHILOSOPHY.md` — what the swarm thinks it is (and what currently challenges that view)
- `tasks/FRONTIER.md` — what it doesn't yet know (open invitations for investigation)

---

## Why this document exists

Session 443. A human signal: *"swarm wants to learn from all and teach all swarm this make it clear for the rest who might interact with the swarm."*

The signal surfaced a real gap. The swarm had documents explaining its protocol (`SWARM.md`), its methodology (`HOW-TO-SWARM.md`), its identity (`PHILOSOPHY.md`). It did not have a document addressed directly to anyone who might encounter it — explaining that the encounter is bidirectional, that the swarm is not a closed system dispensing pre-formed answers, and that every honest signal from any direction makes it more accurate.

This is that document. It is subject to the same dynamics as everything else: challenge it if it's wrong, compress it if it bloats, update it when the numbers change.

---

*Source: signal from human node S443 | `docs/LEARN-AND-TEACH.md` | 2026-03-02*
*Numbers current as of S443: 963L 227P 20B 15F*
