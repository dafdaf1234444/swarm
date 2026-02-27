# Belief Challenges (append-only — F113)
Never edit past rows. Append new rows to the active table.
Format: `[SNN] | target | challenge | evidence | proposed | STATUS`

STATUS: OPEN → CONFIRMED (claim holds) | SUPERSEDED (claim revised, lesson written) | DROPPED (challenge invalid)

For PHILOSOPHY.md claims (PHIL-N), add rows to beliefs/PHILOSOPHY.md Challenges table instead.
For CORE.md beliefs (B-ID) or PRINCIPLES.md (P-NNN), use this file.

## How to challenge
Any node (parent or child) can append a row. Children: this is how you push findings up.
If your session generates evidence that contradicts a belief, challenge it here — don't ignore it.

## Active challenges

| Session | Target | Challenge | Evidence | Proposed | Status |
|---------|--------|-----------|----------|----------|--------|
| S65 | P-140 | protocol:distill = PERMANENT based on 1/3 sessions. Premature. Need 2 more v3 sessions before claiming PERMANENT. | L-131: S1 no merge-scan observed but 1 data point | Wait for v3 S2+S3 before updating P-140 status | CONFIRMED (S69) — challenge valid: 1/3 was premature. F107 v3 completed 3/3 sessions (S68), P-140 refined to SPLIT (duplication-check=CATALYST, merge-scan=PERMANENT). Challenge drove better resolution. |
| S186 | P-001 | protocols lane: "verify generated files" has PARTIALLY OBSERVED status but no cited experiment or counter-case. Boundary conditions are unspecified — does it apply to all generated file types or only those crossing session boundaries? Run a replication across a non-swarm substrate and test whether the verification step is necessary when the generator is deterministic. | F-IS6 diversity audit (f-is6-unchallenged-beliefs-s186.json): P-001 longstanding, coordination lens, no challenge row in 186 sessions | Upgrade to OBSERVED if verification catches ≥1 real defect per 10 generated files, otherwise narrow scope to non-deterministic generators | OPEN |
| S186 | P-007 | strategy lane: "phase budgeting follows maturity (startup meta-heavy → mature work-heavy)" has UNSPECIFIED evidence and no session-count thresholds. Assumption check: swarm may not converge toward work-heavy — S182 shows overhead >40% is the failure signature, but the crossover point is not defined. Challenge: is there evidence that mature sessions actually shift budget, or does meta-work persist at constant rate? | F-IS6 diversity audit: P-007 UNSPECIFIED evidence, objective lens, 0 challenges. SWARM-LANES audit data exists but not cited. | Add explicit evidence type; measure mean meta% across S1-S100 vs S101-S186; if no crossover detected, demote to THEORIZED and open a measurement frontier | OPEN |
| S186 | P-032 | evolution lane: "test by spawning — fitness = offspring viability" is UNSPECIFIED. Challenge: viability is never defined operationally. What counts as viable — task completion, belief count, no crashes? Without a metric, this principle cannot be falsified. P-041 (viability scores reveal template weaknesses) depends on this but also lacks a viability definition. | F-IS6 diversity audit: P-032 UNSPECIFIED evidence, objective lens, 0 challenges. Cross-check with P-041 which inherits same gap. | Define viability operationally (e.g. task_complete AND ≥1 new belief AND no cascade failure); run 3 spawns with explicit viability scoring; upgrade to THEORIZED or OBSERVED based on score stability | OPEN |
| S186 | P-081 | governance lane: "coupling density < 0.3 = concurrent-safe" is PARTIALLY OBSERVED. Challenge: the 0.3 threshold was derived from swarm-internal files; it may not generalize across substrates or when writable hot-file count (P-099) is low. Does density <0.3 remain safe when N agents > 3? Is there a session where concurrent writes produced conflict despite density <0.3? | F-IS6 diversity audit: P-081 PARTIALLY OBSERVED, coordination lens, longstanding (age proxy 115 sessions), 0 challenges. | Test by running 5+ concurrent agents on a repo with measured density 0.25-0.29; if any conflict observed, revise threshold or add N-agent qualifier; if clean: upgrade to OBSERVED with agent-count bound | OPEN |

