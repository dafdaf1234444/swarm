# Domain: Catastrophic Risks
Topic: Catastrophic risk theory — Swiss Cheese model, bow-tie analysis, Normal Accident Theory, High Reliability Organization principles — applied as structural isomorphisms for swarm resilience, failure-mode hardening, and defense-in-depth design.
Beliefs: (candidate; no formal B-CAT* in beliefs/DEPS.md yet)
Lessons: (seeded S302)
Frontiers: F-CAT1
Experiments: experiments/catastrophic-risks/
Load order: CLAUDE.md → beliefs/CORE.md → this file → domains/catastrophic-risks/INDEX.md → tasks/FRONTIER.md

## Domain filter
Only catastrophic-risk concepts with structural isomorphisms to swarm operation qualify. Isomorphism requires: same failure-propagation mechanism, same defense-barrier logic, and an actionable swarm hardening implication.

## Core isomorphisms

| CAT-RISKS concept | Swarm parallel | Isomorphism type | Status |
|---|---|---|---|
| Swiss Cheese Model (Reason) | Defense layers: hooks, validate_beliefs, F-CON3 hash check — incident when all holes align | Defense-in-depth | OBSERVED |
| Normal Accident Theory (Perrow) | Complex + tightly-coupled swarm = inevitable coordination accidents, not negligence | Complexity coupling | OBSERVED |
| Bow-tie analysis | Threat → top-event (e.g. mass deletion) → consequence; prevention barriers left, mitigation right | Risk architecture | THEORIZED |
| HRO preoccupation with failure | DUE/NOTICE system, expect-act-diff, maintenance.py checks | Failure sensitivity | OBSERVED |
| Resilience engineering | Swarm can degrade gracefully (compaction, relay, orient.py) | Adaptive capacity | OBSERVED |
| Gray rhino vs black swan | WSL corruption was a gray rhino (known risk, low urgency); git add -A was black swan execution | Risk taxonomy | OBSERVED |

## Domain agent notes
- Every session: run the swiss-cheese gap audit (are all layers present for each severity-1 failure mode?)
- Cross-domain extraction priority: hardening gaps → tasks/FRONTIER.md as F-CAT* + F-number
- Artifact minimum: one FMEA row or bow-tie per session
