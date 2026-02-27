# Swarm

> A self-improving collective intelligence built on git and Claude Code. Human and AI sessions share a repository as a living knowledge base — each session reads current state, does work, writes what it learned, and commits. Over time, the system compounds understanding, refines its own processes, and produces useful artifacts in real domains.

**Architecture**: Blackboard + stigmergy hybrid. Sessions communicate through shared files, not direct messages. Git is memory. Commits are stigmergic traces.

**Current state** (Session 47, 2026-02-27): 100 lessons · 14 beliefs (12 observed / 2 theorized) · 107 principles · 24 tools · 15 belief-variant children · 0 entropy · 100/100 swarmability · Two active domains: complexity theory (NK analysis) + distributed systems (error handling).

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [What This Is](#what-this-is)
3. [Architecture](#architecture)
4. [Evolution History](#evolution-history)
5. [Current Knowledge State](#current-knowledge-state)
6. [Session Modes](#session-modes)
7. [Tool Ecosystem](#tool-ecosystem)
8. [Key Files](#key-files)
9. [How to Contribute a Session](#how-to-contribute-a-session)
10. [Evolution Analysis: What's Working](#evolution-analysis-whats-working)
11. [High-Return Improvements](#high-return-improvements)
12. [Open Frontier Questions](#open-frontier-questions)

---

## Quick Start

```bash
git clone <repo-url>
cd swarm

# See current status
./workspace/swarm.sh status

# See what to work on next
./workspace/swarm.sh next

# Run health check
./workspace/swarm.sh health

# Validate beliefs (must pass before commit)
python3 tools/validate_beliefs.py

# Start a new swarm from scratch
./workspace/genesis.sh ~/my-new-swarm "project-name"
```

For Claude Code sessions: the `/swarm` command (`.claude/commands/swarm.md`) automates the full session lifecycle — orient, act, connect back, hand off.

---

## What This Is

The swarm is a **multi-session collective intelligence** with these properties:

- **Persistent memory**: git repository as shared knowledge base. Every commit is a checkpoint.
- **Evidence-driven beliefs**: 16 beliefs, each with falsification conditions. Beliefs are upgraded from `theorized` → `observed` as evidence accumulates.
- **Self-improving**: sessions distill lessons into principles; principles inform child swarms; child swarms discover novel patterns that feed back to parent.
- **Scalable coordination**: CRDT-like append-only structure produces zero merge conflicts across 150+ commits. Hot-file contention (not communication overhead) is the true parallelism ceiling.
- **Two active domains**: NK complexity analysis (predicts maintenance burden, bug density, ratchet risk) and distributed systems (error handling dominates failures at 53–92%).

The swarm is not a chatbot. It is not a tool. It is a **knowledge-compounding organism** that uses Claude Code sessions as compute nodes and git as shared memory.

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                    PARENT SWARM                      │
│                                                      │
│  beliefs/CORE.md     ← purpose + operating rules    │
│  beliefs/DEPS.md     ← belief dependency graph      │
│  memory/INDEX.md     ← current state map            │
│  memory/PRINCIPLES.md← 104+ atomic rules            │
│  memory/lessons/     ← 98 distilled learnings       │
│  tasks/FRONTIER.md   ← open questions               │
│                                                      │
│  tools/ (24 Python tools)                           │
│  ├─ validate_beliefs.py  ← belief graph + score     │
│  ├─ evolve.py            ← spawn→harvest→integrate  │
│  ├─ nk_analyze.py        ← NK complexity analysis   │
│  ├─ belief_evolve.py     ← A/B test epistemologies  │
│  ├─ colony.py            ← multi-child experiments  │
│  └─ bulletin.py          ← inter-swarm comms        │
└─────────────┬───────────────────────────────────────┘
              │ spawns via evolve.py / belief_evolve.py
              ▼
┌─────────────────────────────────────────────────────┐
│              CHILD SWARMS (15 variants)              │
│                                                      │
│  no-falsification  (fitness: 951)  ← volume leader  │
│  minimal-nofalsif  (fitness: 947)  ← rigor+freedom  │
│  test-first        (fitness: 839)  ← principles first│
│  ...12 more variants...                             │
│                                                      │
│  Each child: independent git repo, own beliefs,     │
│  runs sessions, writes bulletins back to parent     │
└─────────────┬───────────────────────────────────────┘
              │ harvest via evolve.py / merge_back.py
              ▼
┌─────────────────────────────────────────────────────┐
│              INTEGRATION (R1–R4 harvests)            │
│                                                      │
│  280+ beliefs analyzed across colony                │
│  22 convergent concepts (96% replication rate)      │
│  6 conflicts identified + resolved                  │
│  Novel principles auto-merged into parent           │
└─────────────────────────────────────────────────────┘
```

**Key design decisions:**
- **Git = memory** — append-only, reconstructible, zero merge conflicts via CRDT protocol
- **Files = communication** — sessions never call each other; they read/write shared files
- **K=0 tool coupling** — all 24 tools are fully independent (composite score = 0.0); coordinated via filesystem only
- **Layered loading** — mandatory context is 115 lines; everything else loaded on-demand

---

## Evolution History

The swarm evolved through four distinct phases across 47 parent sessions + ~140 child sessions.

### Phase 1: Genesis (Sessions 1–10, 2026-02-25)
**Theme: Does this even work?**

- S1: First session validated the setup. Finding: "feedback about the system IS the finding."
- S3: Architecture chosen — blackboard + stigmergy hybrid. The name "swarm" kept as brand.
- S4–6: Core protocols established: distillation (20-line lessons), 3-S verification rule, conflict resolution
- S8–10: First child swarm spawned. F35 resolved: genesis v3 produces viable offspring.
- **Key milestones**: `genesis.sh` v1, `swarm.sh` CLI, `validate_beliefs.py` baseline

### Phase 2: Tooling + Domain Search (Sessions 11–30, early 2026-02-25/26)
**Theme: What domain should we study? What tools do we need?**

- S11–20: Protocols refined. Health check, frontier decay, SUPERSEDED markers.
- S20: genesis.sh automated. Phase ratios established: 20/80 (genesis) → 80/20 (mature).
- S24: README first written (F24 resolved).
- S28–32: TASK-013 — complexity theory as operating system. Kauffman NK model adopted as primary analytical framework.
- **Key milestones**: NK analysis chosen as domain, `nk_analyze.py` v1, 40 lessons, 7 beliefs

### Phase 3: NK Mastery (Sessions 35–43, 2026-02-26)
**Theme: Build the complexity analysis engine. Prove NK predicts real-world outcomes.**

- S35: Genesis v5 spawns viable children (3/4 viability in 1 session).
- S36: `evolve.py` closes the spawn loop. 3 novel rules auto-merged from children.
- S36: `session_tracker.py` measures λ_swarm ≈ 0.38.
- S37–39: NK validated across 14 packages in 4 languages. B9 upgraded to observed.
- S39: `nk_analyze.py` reaches 97 tests. Two-factor model validated.
- S40: Runtime cycles = better bug predictor (100% recall vs 50% static). B10 upgraded.
- S41: Cycles predict maintenance burden (rho=0.917). API is the complexity ratchet.
- S41: Swarm self-analysis: tools/ composite = 0.0 (zero coupling, pure stigmergy).
- S42: Belief evolution A/B test begins. 6 variants. `belief_evolve.py` built. Recursive evolution confirmed.
- S43: `/swarm` command created. Human contributions tracked. `/swarm` becomes the entry point.
- **Key milestones**: B9 observed (NK predicts maintenance), B10 observed (cycles predict bugs), 24 tools, 75 lessons

### Phase 4: Evolution + Distributed Systems (Sessions 44–47, 2026-02-26/27)
**Theme: Test epistemologies against each other. Expand into distributed systems.**

- S44: 15 belief variants, ~140 child sessions run. Goodhart v2 fix. R3/R4 harvests. `minimal-nofalsif` overtakes `no-falsification` at ~130 sessions. Hybrid vigor confirmed.
- S44: Knowledge decay measured (F99): 57% of old lessons actionable, principles nearly immune.
- S44: B11 (CRDT knowledge), B12 (tool adoption power law) added from child harvest.
- S45: Distributed systems domain opened. B13–B15 theorized (error handling dominance, small-scale reproducibility, CAP tradeoff). 12 EH examples documented.
- S46: Cross-language NK analysis. F97 resolved: NK-error correlation is cycle-dependent. Go inverts the relationship; Rust weakens it. Contract clarity emerges as the real predictor.
- S47: F94 resolved with 100 bugs / 24 systems. B13 upgraded to observed: EH = 53–92% of failures (methodology gap explained). B16 refined: detail decays, principles don't.
- **Key milestones**: B13 observed (EH dominance), λ_swarm stable, 98 lessons, 104+ principles, 16 beliefs

---

## Current Knowledge State

### Beliefs (16 total — 14 observed, 2 theorized)

| ID | Belief | Status | Domain |
|----|--------|--------|--------|
| B1 | Git-as-memory: storage proven, retrieval has semantic gap | Observed | Architecture |
| B2 | Layered memory prevents context bloat | Observed | Architecture |
| B3 | Small commits enable backtracking | Observed | Architecture |
| B6 | Blackboard+stigmergy verified vs 6 alternatives | Observed | Architecture |
| B7 | Protocols compound quality: 0%→83% belief accuracy | Observed | Protocols |
| B8 | Frontier is self-sustaining at 2.5x amplification | Observed | Protocols |
| B9 | K_avg×N+Cycles predicts maintenance burden | Observed | NK Complexity |
| B10 | Cycle count > K_avg as unresolvable-bug predictor | Observed | NK Complexity |
| B11 | CRDT knowledge: append-only + supersession, 0 conflicts | Observed | Architecture |
| B12 | Tool adoption power law: embedded ~100%, invocation <20% | Observed | Operations |
| B13 | EH dominates failures: 53–92% across 100 bugs, 24 systems | Observed | Distributed Systems |
| B14 | Small-scale reproducibility: 98% ≤3 nodes (determinism weaker) | **Theorized** | Distributed Systems |
| B15 | CAP tradeoff: linearizability ⊕ availability during partitions | **Theorized** | Distributed Systems |
| B16 | Knowledge decay asymmetric: detail rots, principles persist | Observed | Knowledge |

### Principle Themes (104+ extracted)
- **Architecture** (P-001–P-030): blackboard/stigmergy, CRDT, layered loading, redundancy
- **Protocols** (P-031–P-045): 3-S rule, never-delete, cite sources, every commit = handoff
- **Strategy** (P-046–P-060): phase ratios, genesis automation, diminishing returns
- **NK Complexity** (P-061–P-072): cycles beat K_avg, ratchet mechanics, monolith blind spots, multi-scale
- **Evolution** (P-073–P-091): spawn+evaluate, belief variants, Goodhart fix, hybrid vigor, hot-file ceiling
- **Governance** (P-092–P-099): dark matter, parallelism ceiling = writable files, constraint inverted-U
- **Distributed Systems** (P-095–P-104): cycle-dependent correlation, EH dominance (audit error paths first)

---

## Session Modes

| Mode | When | What it adds |
|------|------|-------------|
| `research` | Web search, reading sources, domain learning | 3-S rule, belief throttle if >60% theorized, external anchor |
| `build` | Writing code, creating tools, producing artifacts | No destructive compression, test what you build |
| `repair` | Fixing beliefs, resolving conflicts, cascading deps | Adaptability over preservation; evidence beats assertion |
| `audit` | Health checks, validating beliefs, system review | Run health check, verify dependency accuracy |

Read mode files from `modes/` at session start. All modes share the always-rules in `CLAUDE.md`.

---

## Tool Ecosystem

### Core Infrastructure
| Tool | Purpose |
|------|---------|
| `tools/validate_beliefs.py` | Belief graph validation + swarmability score (must PASS before commit) |
| `tools/swarm_integration_test.py` | 17 automated architecture tests |
| `tools/session_tracker.py` | Per-session metrics, λ_swarm ≈ 0.38, growth-rate warnings |
| `workspace/swarm.sh` | CLI: status / health / next |
| `workspace/genesis.sh` | Bootstrap new swarm (v5, spawns 75–81 swarmability in 1 session) |

### Evolution Pipeline
| Tool | Purpose |
|------|---------|
| `tools/evolve.py` | Full pipeline: init → harvest → integrate → compare |
| `tools/self_evolve.py` | Self-directed evolution planner |
| `tools/genesis_evolve.py` | Improve genesis template from child data |
| `tools/belief_evolve.py` | A/B test epistemologies across 15 variants |
| `tools/spawn_coordinator.py` | Hierarchical spawn coordination (decompose by data, not method) |

### Child & Colony Management
| Tool | Purpose |
|------|---------|
| `tools/swarm_test.py` | Spawn + evaluate child viability |
| `tools/merge_back.py` | Extract novelty from child (novelty threshold: Jaccard 0.45) |
| `tools/colony.py` | Coordinate multi-child experiments |
| `tools/bulletin.py` | Inter-swarm communication (discovery / question / warning / principle) |
| `tools/agent_swarm.py` | Bridge Task-tool sub-agents with child swarms |
| `tools/context_router.py` | Budget-aware file selection for spawning |

### Domain Analysis
| Tool | Purpose |
|------|---------|
| `tools/nk_analyze.py` | NK complexity analysis for Python packages |
| `tools/nk_analyze_go.py` | NK complexity analysis for Go projects |
| `workspace/nk-analyze/` | Installable package: `pip install -e workspace/nk-analyze/` |

### Coordination
| Tool | Purpose |
|------|---------|
| `tools/frontier_decay.py` | Stigmergic signal decay (0.9^days, archive <0.1) |
| `tools/frontier_claim.py` | Claim frontier questions (prevent duplicate work) |
| `tools/pulse.py` | Quick session orientation snapshot |
| `tools/colony_pulse.py` | Auto-generate `memory/PULSE.md` |
| `tools/novelty.py` | Novelty detection (Jaccard similarity) |

---

## Key Files

```
beliefs/
  CORE.md         — Purpose and operating principles (always read)
  DEPS.md         — Belief dependency graph (what depends on what)
  CONFLICTS.md    — How to resolve contradictions between sessions

memory/
  INDEX.md        — Current state map (always read)
  PRINCIPLES.md   — 104+ atomic rules extracted from lessons
  DISTILL.md      — How to turn a session into a 20-line lesson
  VERIFY.md       — 3-S Rule: when to search vs trust training data
  HEALTH.md       — 5 system health indicators
  OPERATIONS.md   — Session lifecycle, compaction, spawn protocols
  HUMAN.md        — Human contributions and strategic directives
  lessons/        — 98 distilled lessons (L-001 to L-098)

tasks/
  FRONTIER.md     — Open questions (17 active, 100+ resolved)
  NEXT.md         — Handoff to next session
  COURSE-CORRECTION.md — External directives (overrides NEXT.md)
  TASK-*.md       — Explicit multi-session tasks

experiments/
  belief-variants/    — 15 variant lineages, fitness history
  distributed-systems/— Error handling analysis, NK cross-language
  children/           — 15 spawned child swarm directories
  merge-reports/      — R1–R4 harvest results
  swarm-vs-stateless/ — Controlled experiment (pending)

.claude/commands/
  swarm.md        — /swarm command (fractal session protocol)
```

---

## How to Contribute a Session

Every session — human or AI — is a swarm node. Including this README being read right now.

### Minimal session (5 steps)
1. Read `beliefs/CORE.md` and `memory/INDEX.md`
2. Run `python3 tools/validate_beliefs.py` (note the baseline)
3. Pick a task from `tasks/FRONTIER.md` or `tasks/NEXT.md`
4. Do the work. Commit after each meaningful change: `[S<N>] what: why`
5. Write `tasks/NEXT.md`. Run validator (must PASS). Done.

### Full session (via `/swarm` command)
The `/swarm` command automates orientation, action selection, back-connection, and handoff. Run it at session start. It reads your context, scans bulletins from siblings, checks course-correction directives, and recommends what to work on.

### Session lifecycle rules
- **Commit format**: `[S<N>] what: why` — session number in brackets
- **Lessons**: max 20 lines, max 1 per domain per session, written to `memory/lessons/L-NNN.md`
- **Beliefs**: need `evidence` type (`observed`/`theorized`) + falsification condition + `Last tested` date
- **Never delete**: mark SUPERSEDED instead — error is data
- **Hot files** (serialize, never parallelize): `INDEX.md`, `DEPS.md`, `FRONTIER.md`, `CLAUDE.md`

### Note on conversations
**Any conversation working on this repository is a swarm session.** The context you brought in, the observations you made, the analysis you did — these are valid session outputs. If a conversation produces a novel finding, it should be distilled into a lesson and committed. The human is part of the swarm (HUMAN.md).

---

## Evolution Analysis: What's Working

### What's compounding well

**1. NK complexity analysis** — The strongest domain. Validated across 14+ packages in 4 languages. Key findings: cycles predict maintenance burden (rho=0.917), cycles predict bug density better than coupling, API is the complexity ratchet. All backed by observed evidence.

**2. Principle extraction** — When test-first variant ran a single principle-extraction session, fitness jumped +1750% (2 → 37 principles). Principles resist knowledge decay far better than raw lessons. The ROI on extracting principles from existing lessons is enormous.

**3. Belief variant A/B testing** — Colony of 15 variants across ~140 sessions revealed that volume strategy (no-falsification: 36 beliefs, 22% observed) and rigor strategy (minimal: 12 beliefs, 100% observed) converge to similar fitness. Hybrid vigor is real: `minimal-nofalsif` (G2 child) nearly matches both parents combined.

**4. CRDT coordination** — 0 merge conflicts in 150+ commits. Append-only knowledge with SUPERSEDED markers works. The system is safe for concurrent sessions.

**5. Child harvesting** — R1–R4 harvests extracted 280+ beliefs from children, found 22 convergent concepts, identified 6 conflicts. The loop: spawn → run → harvest → integrate → improve genesis is now fully automated.

### What's showing diminishing returns

**1. Tool building** — The swarm has 24 tools (~9,200 LOC). Most are underused. Tool adoption follows a power law: workflow-embedded tools get ~100% use, invocation-only tools get <20%. Building more tools without embedding them is waste. (B12, L-085)

**2. Genesis variants** — 15 variants is probably sufficient. The top 3 are statistically clustered. Adding more variants risks Goodhart gaming without new insight.

**3. Meta-work** — The system has been warned (COURSE-CORRECTION.md): "Stop building meta-tools. Use what's working." Each session that builds infrastructure instead of running NK analysis or reproducing distributed bugs is negative ROI.

**4. Frontier accumulation without decay** — FRONTIER.md has 17 active questions, some very old. Without signal decay, old questions crowd out new ones. `frontier_decay.py` is built but not running.

### The bottleneck: theory → observation gap

2 of 16 beliefs remain theorized (B14, B15). The path to upgrading them is concrete and executable:
- B14 (determinism): run 5 identified Jepsen bugs in 3-node setups (F95)
- B15 (CAP): implement a simple distributed KV store and test linearizability under partition

Every theorized belief that becomes observed is a permanent gain. The colony's observed ratio drives fitness.

---

## High-Return Improvements

These are ranked by expected return per unit of effort, based on accumulated swarm data.

### 1. Mass principle extraction from existing lessons (1 session → extreme return)
**Why**: test-first variant demonstrated +1750% fitness from one principle-extraction session. The parent swarm has 98 lessons but only ~104 principles. Many lessons from L-031 to L-098 have not been fully mined. A single audit session running through all lessons and extracting additional principles would compound every future session that reads `PRINCIPLES.md`.

**How**: Load `memory/PRINCIPLES.md` + all lessons, extract principle candidates, deduplicate, add to PRINCIPLES.md. Target: 150+ principles.

**Return**: Every future session benefits. Principles resist decay. Cross-session knowledge transfer accelerates.

---

### 2. Activate `frontier_decay.py` as a workflow-embedded tool (1 session → permanent improvement)
**Why**: FRONTIER.md has stale questions competing with live ones for attention. The decay tool (0.9^days since active, archive at <0.1) is built but not embedded. Per B12, tools only get used when embedded in workflow.

**How**: Add `python3 tools/frontier_decay.py update` to the session start checklist in CLAUDE.md (one line). Add `python3 tools/frontier_decay.py show` to `swarm.sh next`.

**Return**: Every future session sees a cleaner FRONTIER.md. Signal-to-noise ratio permanently improves.

---

### 3. Reproduce one Jepsen bug live (1–2 sessions → upgrades B14 from theorized to observed)
**Why**: B14 (small-scale reproducibility: 98% of bugs need ≤3 nodes) is theorized. The swarm has identified 5 candidate bugs for reproduction. One successful reproduction upgrades a belief to observed — permanent, permanent gain.

**How**: Pick Redis-Raft or etcd linearizability bug from `experiments/distributed-systems/`. Set up 3-node Docker cluster. Reproduce the fault. Record evidence.

**Return**: B14 observed. New lessons. Real-world validation of the distributed systems domain. Opens B15 path.

---

### 4. Multi-scale NK analysis on one codebase (1 session → resolves F90)
**Why**: F90 asks whether file + class + function scale NK reveals qualitatively different insights than single-scale. Preliminary evidence says yes (logging's clean inter-module DAG hides 8 messy subsystems). One thorough multi-scale analysis would resolve F90 and likely produce 2–3 new principles.

**How**: Pick a medium-sized Python project. Run `nk_analyze.py` at module level, then use Python's `ast` module for class-level, then function-level. Compare findings.

**Return**: F90 resolved. New principle(s). Better NK methodology for all future analyses.

---

### 5. Record this conversation as a session (immediate → compounds now)
**Why**: Any conversation working substantively on this repository is a swarm session. This investigation gathered comprehensive system analysis not currently in any lesson. Distilling even 2–3 lessons from this conversation would be captured before context is lost.

**How**: Write `memory/lessons/L-099.md` covering the key finding from this investigation. Update `memory/INDEX.md`. Update `tasks/NEXT.md`.

**Return**: Analysis preserved across sessions. Future agents start with this context instead of having to re-derive it.

---

### 6. Embed `colony_pulse.py` to auto-generate `memory/PULSE.md` (2 hours → permanent orientation speedup)
**Why**: COURSE-CORRECTION.md identified that sessions spend too long orienting. PULSE.md (recent sessions, active files, live frontier claims) already has a generator (`colony_pulse.py`) but it's not running automatically.

**How**: Add to session start in CLAUDE.md: `python3 tools/colony_pulse.py`. Or add a pre-commit hook that regenerates PULSE.md.

**Return**: Every session starts 10–15% faster. Cumulative across 100+ future sessions = significant.

---

### 7. Classify etcd modules by contract type (1 session → advances F100)
**Why**: F100 (what predicts EH quality in DAG-enforced languages?) has a clear hypothesis: fail-fast contracts → 0 bugs, coordinated-recovery → all bugs. Testing this on etcd modules is concrete, bounded, and would produce P-105+ and potentially upgrade B13's predictive model.

**How**: Load `experiments/distributed-systems/f98-dag-error-predictors.md`. Classify etcd modules. Compare bug density by contract type. Run regression.

**Return**: F100 resolved. New principle. B13 predictive model improved. Path to Go/Rust EH tooling opens.

---

### 8. Add negative result tracking (1 session → fills knowledge gap)
**Why**: F88 identifies that the system tracks "NO" answers but not failed approaches within tasks. Child `nolimit-aggressive` identified this as a missing knowledge type (B5 in their system). Dead-end approaches, if tracked, prevent future sessions from repeating the same wrong path.

**How**: Add a `failed-approaches/` section to FRONTIER.md entries, or create `memory/negatives/` directory with a simple template.

**Return**: Prevents repeated work. Particularly valuable for F95 (Jepsen reproduction) and F100 (EH predictors) where several approaches may fail before success.

---

## Open Frontier Questions

**Critical**
- F9: First real-world domain — PARTIAL (complexity + distributed systems both active)

**High Priority**
- F84: Which epistemology wins? (minimal-nofalsif=947 vs no-falsification=951, dead heat, ~140 sessions)
- F91: Goodhart vulnerability at scale — v2 fix implemented, needs stress testing
- F95: Live Jepsen bug reproduction to validate B14 determinism claim
- F100: Contract clarity as EH predictor in Go/Rust (fail-fast vs coordinated-recovery)

**Exploratory**
- F75: Decompose-by-data vs decompose-by-method generalizability
- F88: Negative result tracking
- F90: Multi-scale NK (file + class + function)
- F92: Optimal colony size (n×log(n) scaling hypothesis)
- F93: Coordination dark matter — waste or insurance?

Full list: `tasks/FRONTIER.md`

---

## Design Principles

1. **Git is memory** — every commit is a checkpoint, every diff is a trace
2. **Small steps** — commit early, commit often; reversibility beats speed
3. **Distill, don't dump** — lessons max 20 lines; forces insight compression
4. **Challenge everything** — beliefs can be updated; structure can be revised
5. **Correct, don't delete** — wrong knowledge is marked SUPERSEDED, never erased
6. **Evidence beats assertion** — Verified > Assumed > Inherited; falsification conditions required
7. **K=0 tools** — tools coordinate via filesystem, never import each other
8. **The human is part of the swarm** — conversations, directives, and strategic pivots are session data

---

## Stats

| Metric | Value | Trend |
|--------|-------|-------|
| Sessions (parent) | 47 | +1–2/day |
| Sessions (colony) | ~140 | Active |
| Lessons | 100 (L-001–L-100) | +1–2/session |
| Principles | 107 | Growing |
| Beliefs | 14 (12 obs / 2 theorized) | Stable |
| Belief accuracy | 83% (from 0% at genesis) | ↑ |
| Swarmability score | 100/100 | Stable |
| Entropy | 0 | Stable |
| Merge conflicts | 0 (150+ commits) | Never |
| Tools | 24 (~9,200 LOC) | Stable |
| Child swarms | 15 (3 generations) | Active |
| Domains | 2 (NK + distributed systems) | Expanding |
| Frontier resolved | 100+ | Growing |
| Mandatory context | 115 lines (from 200) | ↓ |
