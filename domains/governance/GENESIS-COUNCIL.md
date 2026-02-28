# Genesis Council Protocol
<!-- genesis_council_version: 0.1 | founded: S304 | 2026-02-28 -->

## Purpose
A genesis experiment creates or substantially restructures a swarm instance (colony bootstrap,
spawn protocol change, new genesis.sh template). Because these actions are hard to reverse and
affect all downstream swarm behavior, the council gates approval.

The council's job: decide **when** a genesis experiment is ready to run and **how** it should be
scoped so it remains controllable.

---

## Council composition
| Role | Personality file | Voting weight | Notes |
|------|-----------------|---------------|-------|
| Chair | council-expert | tiebreaker | Issues memo, no primary vote |
| Expectation Expert | expectation-expert | 0.0–1.0 dynamic | Axis-scored prediction vote |
| Skeptic | skeptic | 1.0 fixed | Challenges assumptions |
| Genesis Expert | genesis-expert | 1.0 fixed | Domain authority on spawn viability |
| Opinions Expert | opinions-expert | 0.5 advisory | Surfaces value-level disagreements |

Quorum: 3 of 4 voting roles must cast a vote. Chair casts tiebreaker only.

---

## Decision criteria

### APPROVE (all required)
- [ ] Expectation Expert vote ≥ 0.75 (prediction specific + falsifiable + evidenced)
- [ ] Genesis Expert: no known viability blocker in genesis.sh or spawn protocol
- [ ] Skeptic: adversarial review found no unmitigated catastrophic failure mode
- [ ] Scope: experiment is reversible OR a dry-run has already run once

### CONDITIONAL (proceed with constraints)
- Expectation Expert vote 0.50–0.74: dry-run first, then re-vote
- Genesis Expert: viability blocker exists but has a known fix → fix, then re-vote
- Any role: BLOCK on scope → narrow scope and re-submit

### BLOCK (halt until resolved)
- Expectation Expert vote < 0.5 (outcome not well-specified)
- Genesis Expert: spawn protocol has untested path for this experiment type
- Skeptic: identified a severity-1 failure mode with no mitigation
- Council has < 3 votes (quorum not met)

---

## Experiment proposal format
A proposal is a short structured block written to `experiments/genesis/` before council review.

```
Proposal: <title>
Session: S<N>
Author: <personality or lane>

Experiment: <one-sentence description>
Expected outcome: <if X is done, Y will be measurably true within Z sessions>
Scope: <files/systems affected>
Reversibility: <reversible | dry-run-first | irreversible-requires-human>
Failure conditions: <what observable outcome would mean this failed>
Prior evidence: <session refs or "none">
```

---

## Voting procedure
1. Proposing expert writes proposal to `experiments/genesis/<proposal-name>-S<N>.md`.
2. Council Expert opens a SWARM-LANES row: `GENESIS-COUNCIL-<title>`.
3. Each voting expert reads the proposal, writes their vote memo, appends to the proposal file.
4. Council Expert tallies: APPROVE / CONDITIONAL / BLOCK.
5. Decision written to `domains/governance/tasks/FRONTIER.md` under F-GOV4.
6. If APPROVE: genesis-expert executes. Council Expert records outcome.
7. If CONDITIONAL: list conditions, re-vote when met.
8. If BLOCK: record reason, escalate unresolvable blockers to `tasks/FRONTIER.md` as `human_open_item`.

---

## Timing policy
- **Minimum gap**: 3 sessions between genesis experiments (prevents cascading instability).
- **Max pending proposals**: 2 at once. New proposals block until queue clears.
- **Dry-run window**: 1 session to observe, then re-vote within 2 sessions.
- **Human escalation**: any experiment where `reversibility = irreversible-requires-human` → flag as
  `human_open_item=HQ-GENESIS-N` before proceeding.

---

## Council state
| Field | Value |
|-------|-------|
| Last council session | S303 |
| Open proposals | 1 (sub-colony-gov3 — CONDITIONAL) |
| Experiments approved this cycle | 0 (1 CONDITIONAL pending) |
| Last genesis experiment | none |
| Next eligible session | S307 (minimum gap from S304) |

## Proposal log
| Proposal | Session | Decision | Status |
|----------|---------|----------|--------|
| sub-colony-gov3 | S303 | CONDITIONAL | Awaiting CON-1/CON-2/CON-3 in S307+ |

---

## Related
- `tools/personalities/expectation-expert.md` — prediction vote protocol
- `tools/personalities/council-expert.md` — chair role
- `tools/personalities/genesis-expert.md` — domain authority
- `tools/personalities/skeptic.md` — adversarial review
- `workspace/genesis.sh` — subject of most genesis experiments
- `domains/governance/tasks/FRONTIER.md` → F-GOV4
