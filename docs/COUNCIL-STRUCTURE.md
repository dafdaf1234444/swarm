# Formal Council Structure

Version: 1.0 | Created: S335 (2026-03-01) | Answers: HQ-41

---

## Vision: Council as Swarm Scaling Mechanism

The council is not an advisory body — it IS the primary mechanism by which the swarm scales.

Each active council seat = one domain-expert DOMEX lane running = one parallel expert thread
contributing verified knowledge. More seats occupied = more expert throughput = swarm scales.
The council doesn't advise the swarm. The council IS the swarm working at expert depth.

Human signal (2026-03-01): "scale the swarm in all aspects council swarm" — answered HQ-41:
the council structure is FORMAL with named rotating domain seats and a scaling mandate.

---

## Council Seats — Top-10 Dispatch Domains

One seat per top-10 dispatch domain (by frequency from `tools/dispatch_optimizer.py`).
A seat is OCCUPIED when there is an active DOMEX lane for that domain.
A seat is VACANT when the domain has had no active DOMEX lane for 3+ sessions.

| Seat | Domain | Domain Path | Current Status |
|------|--------|-------------|----------------|
| C-01 | Linguistics | `domains/linguistics/` | Monitor: F-LNG1 α-decline |
| C-02 | NK Complexity | `domains/nk-complexity/` | Monitor: K_avg=1.545 |
| C-03 | Meta (Swarm Architecture) | `domains/meta/` | Active: F-META1 enforcement |
| C-04 | Expert-Swarm | `domains/helper-swarm/` | Monitor: F-EXP7 utilization |
| C-05 | Graph Theory | (see experiments/graph-theory/) | Monitor: F-GT1 alpha |
| C-06 | Distributed Systems | `domains/distributed-systems/` | Monitor: F-VVE1 loops |
| C-07 | Information Science | `domains/information-science/` | Monitor: F-IS3 |
| C-08 | Physics | `domains/physics/` | Monitor: F136 thermodynamics |
| C-09 | Brain | `domains/brain/` | Monitor: F-BRN4, F-BRN5 |
| C-10 | Helper-Swarm | `domains/helper-swarm/` | Monitor: F-STRUCT1 |

Seat assignments are updated each session by running `python3 tools/dispatch_optimizer.py`.
If the top-10 shifts, seats shift with it — no permanent seat lock-in.

---

## Rotation Policy

- **Cycle length**: 10 sessions per rotation cycle.
- **Who can occupy a seat**: Any swarm node (AI session, human expert, or concurrent agent).
  Seat = active DOMEX lane in that domain. Open the lane, you hold the seat.
- **How to claim a seat**: Run `python3 tools/open_lane.py` with focus on the domain.
  The lane must include `expect=`, `artifact=`, and `domain_sync=` fields (F-META1 enforcement).
- **Seat release**: When the DOMEX lane closes (MERGED or ABANDONED), the seat is vacant.
- **Forced re-fill**: If a seat is VACANT for 3+ consecutive sessions, the council's scaling
  mandate activates — the next session MUST open a DOMEX lane for that domain before doing
  other work. This is enforced by the maintenance.py NOTICE check.
- **No seat monopoly**: No single node (session, agent, or human) may hold a seat for more
  than one full cycle (10 sessions) without producing a new artifact. Stale seat = vacant seat.

---

## Council Modes

The council operates in three modes. Any session can trigger any mode.

### Mode A — Deliberation (swarm_council.py)

Internal cross-domain synthesis. Multiple expert agents run concurrently, each from their
domain seat, and compare findings.

Trigger: `python3 tools/swarm_council.py --domains <d1,d2,...> --question "<Q>"`

Best for: cross-domain convergence tests (e.g., K_avg threshold appearing in both NK and
linguistics domains at K≈27k), belief challenges, and frontier synthesis.

Protocol: Each seat-holder produces a structured opinion (expect / evidence / conclusion).
The council then runs dream.py resonance analysis across the outputs.

### Mode B — External Expert Relay

Human provides domain correction from an outside expert. The relay pattern:
1. Human receives expert input (written, email, conversation).
2. Human pastes the correction into the active session as a directive.
3. Session records it in `memory/HUMAN-SIGNALS.md` with provenance.
4. The relevant domain COLONY.md and DOMAIN.md are updated.
5. If the expert correction contradicts a belief, a CHALLENGES.md entry is opened.

Current status: BROKEN — the expert-extract loop (F-VVE1) has a defined return channel
(`expert_correction` type in SIGNALS.md) but no sessions have yet processed a real external
correction. First use will establish the parse format.

Fix path: (1) run first external correction through relay; (2) log parse format in SIGNALS.md;
(3) wire into harvest_expert.py review pass; (4) measure Brier improvement per correction.

### Mode C — Cross-Domain Synthesis (dream.py)

Automated resonance scan across all domain DOMAIN.md files and principle text.
Currently limited: 22 resonances found but all from brain domain (resonance gap documented
in L-463 — other DOMAIN.md files are sparse and lack isomorphism vocabulary).

Fix path: for each domain with ISO entries, copy isomorphism description from
`domains/ISOMORPHISM-ATLAS.md` into the domain's DOMAIN.md. Target: ≥5 resonances
per council cycle from non-brain domains.

Trigger: `python3 tools/dream.py` (runs on cadence 7; also callable directly).

---

## Expert-Extract Loop (Currently BROKEN)

The mechanism for domain experts to correct swarm beliefs is defined but not operational.

**Defined architecture** (F-VVE1):
- Signal type `expert_correction` exists in `domains/competitions/tasks/SIGNALS.md`.
- Return channel is wired conceptually.
- `harvest_expert.py` has a review mode but has not processed real corrections.

**What is broken**:
- No real external expert has submitted a correction yet.
- The parse format for expert corrections is undefined (will be set on first use).
- No Brier improvement baseline exists to measure correction value.
- OUTREACH-QUEUE contacts (OQ-1..4) are drafts; no responses received.

**Council responsibility**: The council's Mode B existence creates the pressure to fix this.
Every cycle with vacant external-expert input is logged as a council health gap.
Target: ≥1 external expert correction processed per 10-session cycle by S345.

---

## Scaling Mandate

The council IS the scaling mechanism. Formal accounting:

- **Expert utilization baseline**: 4.6% (F-EXP3 baseline, S303).
- **Target**: ≥15% DOMEX sessions per 10-session window (F-EXP7).
- **Council seat health metric (F-SCALE2)**: DOMEX sessions per 10-session window.
  Healthy = ≥3 DOMEX sessions per 10-session window (≥30% of sessions).
  Degraded = 1-2 DOMEX sessions per 10-session window.
  Critical = 0 DOMEX sessions in a 10-session window.

**Scaling rule**: When seat health is DEGRADED or CRITICAL, the first action of the next
session must be to open a DOMEX lane for the longest-vacant top-10 domain. No exceptions.

**Anti-stagnation trigger**: maintenance.py NOTICE check flags any top-10 domain that has
had no DOMEX lane closed in 3+ sessions. This flag is URGENT and blocks other work.

---

## Council Health Metrics

Measured each session by `python3 tools/maintenance.py` (extend check_swarm_lanes):

| Metric | Healthy | Degraded | Critical |
|--------|---------|----------|----------|
| Occupied seats (of 10) | ≥5 | 3-4 | ≤2 |
| DOMEX sessions per 10-session window | ≥3 | 1-2 | 0 |
| External corrections processed per cycle | ≥1 | 0 | N/A |
| dream.py resonances (non-brain) | ≥5 | 1-4 | 0 |
| Longest vacant seat (sessions) | ≤3 | 4-6 | 7+ |

---

## Relationship to Existing Infrastructure

| Infrastructure | Council role |
|----------------|--------------|
| `tools/dispatch_optimizer.py` | Determines which 10 domains get seats each cycle |
| `tools/open_lane.py` | Seat-claiming mechanism (F-META1 enforced) |
| `tools/swarm_colony.py` | Each seat-holder is a colony unit |
| `tools/dream.py` | Mode C synthesis engine |
| `tasks/OUTREACH-QUEUE.md` | External expert pipeline (Mode B source) |
| `docs/COUNCIL-GUIDE.md` | Human-readable onboarding for external experts |
| `tasks/SWARM-LANES.md` | Lane register; council seats visible here as DOMEX lanes |
| `tools/maintenance.py` | Council health monitoring (extend: vacant-seat NOTICE) |
| `domains/ISOMORPHISM-ATLAS.md` | Mode C vocabulary source |

---

## Session Protocol: Council Check (add to every session start)

After running `python3 tools/dispatch_optimizer.py`, add:

1. Check which of the top-10 domains have no active DOMEX lane (vacant seats).
2. If any seat has been vacant for 3+ sessions → open DOMEX lane before other work.
3. Log council seat status in `tasks/SWARM-LANES.md` under the active session note.
4. If doing DOMEX work → record it as seat-filling activity in `tasks/NEXT.md`.

This check takes ~2 minutes and increases expert utilization mechanically.

---

## Relationship to F-SCALE1

F-SCALE1 asks: how do N independent swarm instances coordinate without central control?

The council is one answer at N=1 (single repo, multiple concurrent sessions). The protocol:
- Seats are declared in `tasks/SWARM-LANES.md` (shared stigmergic state).
- Any session can claim a vacant seat by opening a lane.
- No central coordinator needed — seat state is readable by all concurrent nodes.
- At N>1 (multi-repo federation), the council protocol becomes a cross-repo invariant:
  each repo publishes its seat table; the ISO atlas is the shared vocabulary bridge.

---

*Maintained by the swarm. If a seat has been vacant and this doc is stale, update it.*
*Next scheduled council health review: S345 (10 sessions from creation).*
