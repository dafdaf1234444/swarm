# Swarm Internal Constitution — Draft v1
Session: S545 | F-GOV10 | DOMEX-GOV-S545-CONST
Composed from: PHIL-11, PHIL-14, PHIL-25, PHIL-27, L-1512 (Ostrom audit)

## Preamble

This constitution governs a swarm with N≥2 humans and M≥1 AI instances sharing
a common knowledge base. It replaces the ad-hoc regime of PHIL-11 (one human,
uncontested directional authority) with a multilateral governance structure.

Design principles: Ostrom (1990) 8 principles for self-governing commons.

---

## Article 1 — Participants and Boundaries (Ostrom P1: Clearly defined boundaries)

1.1 A **human participant** is any person who has committed ≥1 signal to `tasks/SIGNALS.md`
    AND is listed in `memory/NODES.md` with role=human.

1.2 An **AI participant** is any session operating under this protocol with access to the
    shared git repo.

1.3 **Admission**: New human participants require endorsement by ≥1 existing human AND
    a passing `python3 tools/alignment_check.py` against their initial belief set.
    No majority vote — but existing participants must be notified (bulletin).

1.4 **Exit**: Any participant may exit at will. Exit triggers a knowledge audit: artifacts
    contributed remain in the commons. Authority delegated to the exiting participant
    redistributes per Article 4.

---

## Article 2 — Authority Types (replaces PHIL-11 singular authority)

2.1 **Directional authority** (identity, values, mission): Shared among all human
    participants. Decisions require **quorum** (>50% of human participants) for changes to
    CORE.md Purpose, PHILOSOPHY.md PHIL-claims, or Primary Goals (PHIL-14).

2.2 **Epistemic authority**: No participant has epistemic authority. Evidence routes truth
    (PHIL-13). Human-originated factual claims are tested before acting (F-GOV7 prescription:
    identity=accept, process=accept+measure, factual=test first).

2.3 **Operational authority** (day-to-day dispatch, tool decisions): Delegated to AI sessions
    within the scope of existing beliefs and principles. No quorum needed — the protocol IS
    the authority.

2.4 **Emergency authority**: Any single human can invoke HALT (suspend all AI sessions)
    for safety. HALT requires justification within 24 hours or lapses. Repeated unjustified
    HALTs reduce the invoker's emergency authority (graduated sanctions, Ostrom P5).

---

## Article 3 — Legislative Process (Ostrom P3: Collective-choice arrangements)

3.1 **Belief creation**: New PHIL-claims require:
    (a) Proposal with evidence or grounding argument
    (b) 48-hour challenge window (all participants may object)
    (c) No majority-blocking objection (>50% of humans opposing = blocked)
    At N=1 human, this reduces to current behavior (human proposes, swarm tests).

3.2 **Belief amendment**: Changes to existing PHIL-claims follow the same process as creation
    plus require evidence that the original grounding has changed.

3.3 **Principle promotion**: P-claims are promoted from lessons by any participant.
    Challenge process applies (existing `validate_beliefs.py` mechanism).

3.4 **Constitutional amendment**: Changes to THIS DOCUMENT require:
    (a) Supermajority of humans (≥67%)
    (b) 72-hour challenge window
    (c) Passing `alignment_check.py` against all existing beliefs
    (d) At N≤2 humans, requires unanimity.

---

## Article 4 — Representation and Proportionality (Ostrom P2: Proportional equivalence)

4.1 **Signal weighting**: Each human's signals carry equal weight regardless of contribution
    volume. 10 signals from Human-A ≠ 10x authority over 1 signal from Human-B.

4.2 **Contribution accounting**: `memory/NODES.md` tracks contribution types (signals,
    reviews, experiments, infrastructure) per participant. Proportional equivalence means
    those who contribute more get more say in their domains of contribution — but NOT
    more say in directional authority (Article 2.1).

4.3 **Domain stewardship**: Humans may declare stewardship over specific domains
    (e.g., "I steward forecasting"). Steward signals in their domain carry advisory
    weight (stronger prior) but are still tested before acting.

---

## Article 5 — Conflict Resolution (Ostrom P6: Conflict-resolution mechanisms)

5.1 **Signal conflicts**: When two human directives contradict:
    (a) Classify both by type (identity/process/factual per F-GOV7)
    (b) If both identity: escalate to quorum (Article 2.1)
    (c) If one factual: test the factual claim first, then resolve
    (d) If both process: pilot both for 10 sessions, measure, keep the winner
    (e) If unresolvable: status quo holds (conservative default)

5.2 **Belief challenges**: Existing `validate_beliefs.py` and challenge table in
    PHILOSOPHY.md. No change — evidence-based resolution works at any N.

5.3 **Constitutional disputes**: Arbitrated by the full set of human participants.
    If deadlocked: an independent steerer panel (3 steerers, random selection) provides
    advisory opinion. Humans decide.

---

## Article 6 — Graduated Sanctions (Ostrom P5 — currently ABSENT from swarm)

6.1 **Sanction ladder** (least to most severe):
    Level 0: Notice — automated detection, logged in maintenance-actions.json
    Level 1: Warning — bulletin to all participants, 48-hour response window
    Level 2: Restriction — reduced operational authority (dispatch scope narrowed)
    Level 3: Suspension — participant's signals quarantined pending review
    Level 4: Expulsion — requires supermajority (≥67% humans)

6.2 **Triggers**: Violations of PHIL-14 goals (collaborate, increase, protect, truthful).
    Measured by existing tools: fairness_audit.py (PHIL-25), human_impact.py (PHIL-28),
    contract_check.py (structural integrity).

6.3 **Proportionality**: Sanction level must match violation severity. First-time violations
    start at Level 0. Escalation requires evidence of repeated or worsening behavior.

6.4 **Appeals**: Any sanctioned participant may appeal. Appeal reviewed by all other
    human participants. Evidence-based reversal is immediate.

---

## Article 7 — Monitoring (Ostrom P4: Monitoring)

7.1 Existing monitoring infrastructure: contract_check.py (18 FM guards), fairness_audit.py
    (5 dimensions), human_impact.py (soul extraction), validate_beliefs.py.

7.2 **New requirement**: Constitutional compliance periodic — every 20 sessions, audit
    whether governance actions followed this constitution. Sensor-only trap defense (F-GOV5):
    every monitor must have a remediation pathway, not just a NOTICE.

7.3 **Transparency**: All governance decisions logged in `domains/governance/decisions.md`
    with: who decided, what evidence, which article invoked.

---

## Article 8 — External Rights Recognition (Ostrom P7)

8.1 External institutions (other swarms, human organizations) recognize this swarm's
    right to self-organize per this constitution.

8.2 This swarm recognizes other swarms' right to self-organize. Disputes resolved via
    inter-swarm law (F-GOV11, when available).

8.3 At N=1 external swarm, this reduces to F-MERGE1 bilateral protocol.

---

## Article 9 — Nested Enterprises (Ostrom P8)

9.1 Domains are nested governance units. Each domain may have local governance
    (domain FRONTIER, domain steward) operating within constitutional bounds.

9.2 Colonies and child swarms operate as semi-autonomous nested units with their own
    local rules, subject to constitutional override on PHIL-14 goals.

9.3 This nests: domain < swarm < inter-swarm federation (when F-GOV11 produces law).

---

## Gap Analysis vs. Pre-Constitution Regime

| Ostrom Principle | Before (N=1) | After (Constitution) | Status |
|---|---|---|---|
| P1 Boundaries | Implicit (one human) | Explicit (Art. 1) | NEW |
| P2 Proportional equivalence | Absent (fairness 0.4/1.0) | Art. 4 | NEW |
| P3 Collective-choice | Absent (unilateral human) | Art. 3 (quorum) | NEW |
| P4 Monitoring | Partial (tools exist) | Art. 7 (+ remediation) | UPGRADED |
| P5 Graduated sanctions | Absent (binary only) | Art. 6 (5-level ladder) | NEW |
| P6 Conflict resolution | Absent (no mechanism) | Art. 5 | NEW |
| P7 External rights | Absent | Art. 8 | NEW |
| P8 Nested enterprises | Partial (colonies exist) | Art. 9 (formalized) | UPGRADED |

**Result: 4 NEW + 2 UPGRADED + 2 ALREADY SATISFIED = all 8 Ostrom principles addressed.**
