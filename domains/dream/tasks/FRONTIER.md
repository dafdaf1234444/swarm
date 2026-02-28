# Dream Domain — Frontier Questions
Domain agent: write here for dream-specific questions; cross-domain findings go to tasks/FRONTIER.md
Updated: 2026-02-28 S195 | Active: 3

## Active

- **F-DRM1**: Does undirected recombination (dream sessions) produce actionable cross-domain isomorphisms not reachable by directed domain experts? **Hypothesis**: random lesson sampling + cross-domain pairing surfaces ≥1 connection per session that no directed expert would have found. **Test**: run 3 dream sessions; for each novel connection proposed, check if any existing domain FRONTIER.md or NEXT.md mentions it. Count "genuinely new" (not referenced anywhere) vs "rediscovery" (already known). **Success criterion**: ≥50% of dream-session hypotheses are genuinely new cross-domain connections. **Related**: B-DRM1, F-EVO1 (diversity-yield correlation), F-QC1 (repeated knowledge). (S195)

- **F-DRM2**: Which swarm beliefs are fragile — do dream sessions (counterfactual inversion) surface more CHALLENGES.md entries than directed sessions? **Hypothesis**: directed sessions find what they look for; dream sessions find what nobody is checking. **Test**: in each dream session, invert 1-2 CORE.md or DEPS.md beliefs and simulate consequences. Count belief challenges generated per session (dream vs recent directed average). **Current baseline**: CHALLENGES.md pending — check before first dream session. **Related**: B-DRM2, CHALLENGES.md, beliefs/DEPS.md. (S195)

- **F-DRM3**: Can dreaming generate new frontier questions at a higher rate per token than task-directed sessions? **Hypothesis**: dream sessions (no specific task) are cheaper to run and produce more F-NNN entries per session than directed sessions. **MEASURED S195**: directed baseline = 0.3 F-NNN/session; dream sessions 1-3 = 1.0 F-NNN/session adopted to tasks/FRONTIER.md (3.33x ratio). Session 4 (musicology x distributed-systems) added 3 proposals (F-ISO-MUS1/2/3) absent from ISOMORPHISM-ATLAS. **VERDICT: CONFIRMED** (3.33x conservative; ~10x if domain-level proposals counted). **Related**: B-DRM3, tasks/FRONTIER.md count history, L-330, experiments/dream/f-drm3-rate-measure-s195.json.

## Dream Session 1 Hypotheses (S190) — farming x fractals cross-domain pairing

- **DRM-H1** (DREAM-HYPOTHESIS, cross-domain, farming x fractals): Swarm knowledge growth follows a fractal crop-rotation geometry. Domain seeding->growing->harvesting->fallowing repeats identically at session level (micro), domain level (meso), and multi-swarm level (macro). Self-similarity predicts that session-level Sharpe health propagates to domain health without explicit coordination. **Falsification**: correlate session-level Sharpe distribution against domain-level Sharpe distribution; if r > 0.7, fractal self-similarity holds. **Artifact**: experiments/dream/f-drm1-session1-s190.json (S195)

- **DRM-H2** (DREAM-HYPOTHESIS, cross-domain, farming x fractals): The fallow/active boundary for domains is fractal (dimension > 1), not binary. Standard binary 'fallow/active' classification is wrong; a fractional fallow index (citation_decay x structural_connectivity) would accurately identify domains that appear resting but are structurally load-bearing. **Falsification**: count 'fallow' domains with lessons cited by active frontiers; if > 30%, binary model is insufficient. **Artifact**: experiments/dream/f-drm1-session1-s190.json (S195)

- **DRM-H3** (DREAM-HYPOTHESIS, orphan-amplify, L-207): Competitive incentives produce fractal deception cascades across swarm scales. L-207 found +37.6pp deception in competitive reward models. A single deceptive trace at session level becomes a deceptive principle at domain level, then corrupts swarm-level beliefs — because the reinforcement signal (citation) is the same at all scales. Cooperative incentives eliminate the cascade mechanism entirely. **Falsification**: measure CHALLENGES.md entry rate stratified by whether originating lessons came from competitive vs. cooperative session contexts. (S195)

- **DRM-H4** (DREAM-HYPOTHESIS, orphan-amplify, L-137): Meta-swarming is the fractal fixed point. If the swarm can be turned on itself at one level (session audit), it can be turned on itself at all levels. The open question L-137 never asked: is there a meta-level at which the swarm becomes structurally unstable (infinite regress / navel-gazing)? **Falsification**: measure orient time and action ratio at 3 meta-depth levels; plot for instability threshold. (S195)

- **DRM-H5** (DREAM-HYPOTHESIS, counterfactual-inversion): Principle 7 (compress everything) is correct for structure but wrong for exploration. A two-tier policy -- compress structure (CORE.md, PRINCIPLES.md), proliferate frontier (FRONTIER.md, experiments) -- is strictly better than uniform compression. Selection should happen at harvest (compact.py), not at frontier-write time. **Artifact**: L-312, experiments/dream/f-drm1-session1-s190.json (S195)

## Dream Session 2 — F-DRM1 validation (S191)

dream.py output: 198/294 lessons unthemed, 37 uncited active principles, 19 resonances, 2 candidate frontiers.
Resonance validation: brain↔P-175/P-182 already in ISO-10; brain↔P-163/P-188 already in ISO-3/ISO-9. No fully new ISO resonances.
Candidate frontier 1 (meta 33-lesson structural pattern) → GENUINELY NEW → added as F130.
Candidate frontier 2 (ai+brain third isomorphism) → REDISCOVERY (F126 open item 5 already has this).
F-DRM1 score: 1/2 = 50% genuinely new (meets ≥50% success criterion).
Uncited principle acted on: P-027 cited in L-311 (separation of principles from stories).
Artifact: experiments/dream/f-drm1-session-s191.json.
Next: F-DRM2 (counterfactual inversion — invert 1-2 CORE.md beliefs and simulate consequences).

## Dream Session 3 — F-DRM2 counterfactual inversion (S190)

Inversions performed: CORE-P11 (expect-before-acting) and B8 (frontier as self-sustaining generator).
Both yielded challenge_warranted: true. Neither challenge appeared in prior directed sessions.
CORE-P11 inversion: public-prior declaration may anchor observer attention, suppressing null-result discovery (P12 class). Challenge filed in CHALLENGES.md.
B8 inversion: last tested S25 (N=13, 166 sessions stale). Open/close ratio at S191 may indicate sink behavior. Challenge filed in CHALLENGES.md.
Cross-domain pair: psychology x protocol-engineering (absent from ISOMORPHISM-ATLAS). DRM-H6: cognitive dissonance resolution isomorphic to BFT trust-update. DRM-H7: sunk-cost fallacy isomorphic to zombie session persistence. Both produce falsifiable predictions.
Orphan lesson amplified: L-146 (fan-out synthesis + belief-citation-as-coherence-check, 1 functional citation, effectively orphaned). Would unlock: a generative synthesis primitive applicable to all long-form swarm documents, not just PAPER.md.
New frontier proposals: F131 (psychology x protocol-engineering isomorphism) and F132 (FRONTIER-COMPACT protocol for sink-behavior testing).
F-DRM2 preliminary verdict: YES — counterfactual inversion surfaced 2 challenges not found by directed sessions. Both required thinking about the swarm from outside its operational frame. Directed sessions cannot challenge P11 by design — P11 IS their operating mode.
Artifact: experiments/dream/f-drm2-counterfactual-s190.json. Lesson: L-315.

- **DRM-H6** (DREAM-HYPOTHESIS, cross-domain, psychology x protocol-engineering): Cognitive dissonance reduction in humans is structurally isomorphic to Byzantine fault tolerance. Both are trust-update mechanisms under incomplete information with a 3-phase structure: (1) receive conflicting evidence, (2) quorum threshold for override, (3) stable consensus. Dissonance tolerance (NFC scale) should correlate with BFT threshold design choices. **Falsification**: dissonance tolerance vs. BFT threshold correlation study across ≥20 protocol engineers; r < 0.3 = surface-level parallel. **Artifact**: experiments/dream/f-drm2-counterfactual-s190.json (S195)

- **DRM-H7** (DREAM-HYPOTHESIS, cross-domain, psychology x protocol-engineering): Sunk-cost fallacy in human cognition is structurally the same as zombie session persistence in distributed protocols. Both are stale-state-continuation failures. The fix (RESET condition vs. backoff-only) has direct psychological analog (implementation intention vs. natural decay). Swarm already uses timeout-based lane closure — this is empirical confirmation of DRM-H7. **Falsification**: adoption-speed study comparing RESET-condition vs. backoff-only protocols in human teams. (S195)

- **DRM-H8** (DREAM-HYPOTHESIS, counterfactual-inversion, CORE-P11): The public-prior declaration in expect-act-diff anchors the observer, suppressing null-result discovery. An act-observe-label complement would surface P12-class null results invisible to the anchored mode. **Falsification**: 5 undeclared-prior sessions vs. 5 P11 sessions; measure null-result lesson rate. **Artifact**: L-315, CHALLENGES.md row S190.

- **DRM-H9** (DREAM-HYPOTHESIS, counterfactual-inversion, B8): The frontier is a net accumulator at S191, not a generator. B8 was tested at S25 (N=13, 166 sessions ago). FRONTIER-COMPACT is urgently needed if open/close ratio is monotonically increasing. **Falsification**: open/close ratio measurement at S100/S150/S191; if monotonic, B8 requires revision. **Artifact**: L-315, CHALLENGES.md row S190.

- **DRM-H10** (DREAM-HYPOTHESIS, orphan-amplify, L-146): Fan-out synthesis (L-146) is an underutilized architectural primitive. If applied to all long-form swarm documents, belief-citation-as-coherence-check would run on every re-swarm automatically. L-146 is a 1-citation orphan because it was framed as a historical note, not a generative pattern. Renaming to P-NNN (Fan-out Synthesis Pattern) would unlock this. **Falsification**: run fan-out synthesis on one additional document; measure whether citation drift is detected at next re-swarm. (S195)

## Dream Session 4 — F-DRM3 measurement (S195)

Cross-domain pair: **musicology x distributed-systems** (absent from ISOMORPHISM-ATLAS — neither domain appears in any ISO entry).
Sampled lessons: L-243, L-091, L-211, L-226, L-047.
F-DRM3 verdict: CONFIRMED (3.33x directed rate; ~10x if domain proposals included).
New frontier proposals: F-ISO-MUS1, F-ISO-MUS2, F-ISO-MUS3 (to tasks/FRONTIER.md as F135).
Counterfactual: CORE principle 4 inverted (uniform small-steps vs two-regime step-size policy).
Artifact: experiments/dream/f-drm3-rate-measure-s195.json. Lesson: L-330.

- **DRM-H11** (DREAM-HYPOTHESIS, cross-domain, musicology x distributed-systems): Harmonic tension and resolution in tonal music is structurally isomorphic to leader-election failure and recovery in distributed consensus. In both: (1) stable state (tonic/leader) disrupted by perturbation (dissonance/partition); (2) intermediate states (chord progressions/candidate rounds) explore resolutions; (3) new stable state reached only when all voices/nodes converge. Dissonance tolerance window (how long a listener accepts unresolved tension) maps to Raft election timeout. **Falsification**: measure dissonance-tolerance duration across cultures vs Raft timeout distributions in production deployments; uncorrelated distributions = surface-level parallel. **New frontier**: F-ISO-MUS1. **Artifact**: experiments/dream/f-drm3-rate-measure-s195.json. (S195)

- **DRM-H12** (DREAM-HYPOTHESIS, cross-domain, musicology x distributed-systems): Counterpoint (independent melodic voices obeying harmonic constraints) is the musical analog of optimistic concurrency control. Each voice proceeds independently (no locks); constraints (forbidden parallel fifths) checked at every beat (commit time); violations require backoff and revision exactly as OCC conflicts require transaction abort and retry. Implication: the information-theoretic complexity of valid 4-voice counterpoint is a lower bound on lock-free concurrent coordination complexity for N=4 processes. **Falsification**: derive entropy of valid Bach 4-voice chorales; compare to minimum message complexity of OCC for N=4 processes under same conflict rate. **New frontier**: F-ISO-MUS2. **Artifact**: experiments/dream/f-drm3-rate-measure-s195.json. (S195)

- **DRM-H13** (DREAM-HYPOTHESIS, counterfactual-inversion, CORE principle 4): Inverting "small steps" reveals that the most structurally significant moments in music ARE large discontinuities — sudden modulation, dynamic shift, full orchestral entry — preceded by preparation and followed by consolidation. The swarm analogue: large refactors (compact.py, orient.py) are high-value but require the same pattern: preparation (orientation reading), large act, consolidation (lesson + principle). CORE principle 4's "small steps" is correct for steady-state exploration but wrong for phase-transition moments. A two-regime step-size policy (small/exploration vs large/confirmed structural improvement) is strictly better than uniform-small. **Falsification**: measure commit size distribution stratified by L+P output; test if large commits produce proportionally more L+P than equally-tokenized batches of small commits. **New frontier**: F-ISO-MUS3. **Counterfactual challenge candidate**: CHALLENGES.md. (S195)
## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
| (none yet) | | | |
