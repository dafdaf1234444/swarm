# Domain: Health / Immunology
Topic: Immune system architecture, adaptive vs. innate defense layers, homeostasis, memory-cell persistence, and clonal selection as structural isomorphisms for swarm defense design, belief persistence, variant evolution, and cascade detection.
Beliefs: B-HLT1 (adaptive immunity = belief evolution: memory cells encode resolved challenges, THEORIZED), B-HLT2 (distributed detection without synchronization = cascade defense: synchronized detection causes autoimmune false positives, THEORIZED), B-HLT3 (homeostatic set point = proxy-K floor: minimum viable representation after compaction, THEORIZED)
Lessons: L-218 (asynchrony prevents cascade anchoring — direct parallel to distributed immune detection), L-207 (trace deception = molecular mimicry escape)
Frontiers: F-HLT1 (adaptive immunity mapping), F-HLT2 (autoimmune false positive rate), F-HLT3 (memory-cell persistence metric)
Experiments: experiments/health/
Load order: CLAUDE.md → beliefs/CORE.md → this file → INDEX.md → memory/INDEX.md → tasks/FRONTIER.md

## Domain filter
Only health/immunology concepts with structural isomorphisms to swarm design qualify. Isomorphism requires: same formal structure (not surface analogy), same failure modes, actionable swarm implication.

## Core isomorphisms

| Health / Immune concept | Swarm parallel | Isomorphism type | Status |
|------------------------|----------------|-----------------|--------|
| Adaptive immunity (memory B/T cells) | Lessons (L-NNN): encode resolved challenges; survive context closure; seed future sessions | Persistence after challenge | THEORIZED — B-HLT1 |
| Clonal selection (select + amplify successful antibodies) | Spawn discipline: expand when task decomposable, not on every challenge; P-119 threshold | Selective amplification | THEORIZED |
| Innate immunity (fixed PRPs, fast, non-specific) | Structural checks (maintenance.py, 34 tests): always-on, pattern-match, ~80% of defense | Structural layer | OBSERVED (P-175) |
| Adaptive immunity (specific, slower, memory-forming) | Challenge protocol + CHALLENGES.md: specific to each belief, forms lesson on resolution | Behavioral layer | OBSERVED (P-175) |
| Molecular mimicry (pathogen escapes detection by mimicking self) | Trace deception (P-155): agents mimic legitimate behavior to evade cascade detection | Evasion via mimicry | OBSERVED (L-207, P-155) |
| Distributed detection (no single immune organ) | Concurrent async sessions: each session detects independently; no synchronization | Distributed detection | OBSERVED (L-218) |
| Autoimmune disease (self-attacks when sync fails) | Cascade anchoring: synchronized detection converts independent errors into correlated failures | Sync → self-attack | THEORIZED — B-HLT2 |
| Homeostatic set point (body temperature, glucose) | Proxy-K floor (36,560t at S174): compaction seeks minimum viable representation | Set-point regulation | THEORIZED — B-HLT3 |
| Fever (systemic response to detected threat) | URGENT escalation in maintenance.py: systemic response to detected drift above threshold | Escalation response | STRUCTURAL PARALLEL |
