# Dream Domain — Frontier Questions
Domain agent: write here for dream-specific questions; cross-domain findings go to tasks/FRONTIER.md
Updated: 2026-02-28 S190 | Active: 8

## Active

- **F-DRM1**: Does undirected recombination (dream sessions) produce actionable cross-domain isomorphisms not reachable by directed domain experts? **Hypothesis**: random lesson sampling + cross-domain pairing surfaces ≥1 connection per session that no directed expert would have found. **Test**: run 3 dream sessions; for each novel connection proposed, check if any existing domain FRONTIER.md or NEXT.md mentions it. Count "genuinely new" (not referenced anywhere) vs "rediscovery" (already known). **Success criterion**: ≥50% of dream-session hypotheses are genuinely new cross-domain connections. **Related**: B-DRM1, F-EVO1 (diversity-yield correlation), F-QC1 (repeated knowledge).

- **F-DRM2**: Which swarm beliefs are fragile — do dream sessions (counterfactual inversion) surface more CHALLENGES.md entries than directed sessions? **Hypothesis**: directed sessions find what they look for; dream sessions find what nobody is checking. **Test**: in each dream session, invert 1-2 CORE.md or DEPS.md beliefs and simulate consequences. Count belief challenges generated per session (dream vs recent directed average). **Current baseline**: CHALLENGES.md pending — check before first dream session. **Related**: B-DRM2, CHALLENGES.md, beliefs/DEPS.md.

- **F-DRM3**: Can dreaming generate new frontier questions at a higher rate per token than task-directed sessions? **Hypothesis**: dream sessions (no specific task) are cheaper to run and produce more F-NNN entries per session than directed sessions. **Test**: measure F-NNN entries added per dream session; compare to 5-session rolling average from directed sessions. **Current baseline**: directed sessions add ~0.3 new F-NNN per session (23 open / ~80 sessions since F system created). **Related**: B-DRM3, tasks/FRONTIER.md count history.

## Dream Session 1 Hypotheses (S190) — farming x fractals cross-domain pairing

- **DRM-H1** (DREAM-HYPOTHESIS, cross-domain, farming x fractals): Swarm knowledge growth follows a fractal crop-rotation geometry. Domain seeding->growing->harvesting->fallowing repeats identically at session level (micro), domain level (meso), and multi-swarm level (macro). Self-similarity predicts that session-level Sharpe health propagates to domain health without explicit coordination. **Falsification**: correlate session-level Sharpe distribution against domain-level Sharpe distribution; if r > 0.7, fractal self-similarity holds. **Artifact**: experiments/dream/f-drm1-session1-s190.json

- **DRM-H2** (DREAM-HYPOTHESIS, cross-domain, farming x fractals): The fallow/active boundary for domains is fractal (dimension > 1), not binary. Standard binary 'fallow/active' classification is wrong; a fractional fallow index (citation_decay x structural_connectivity) would accurately identify domains that appear resting but are structurally load-bearing. **Falsification**: count 'fallow' domains with lessons cited by active frontiers; if > 30%, binary model is insufficient. **Artifact**: experiments/dream/f-drm1-session1-s190.json

- **DRM-H3** (DREAM-HYPOTHESIS, orphan-amplify, L-207): Competitive incentives produce fractal deception cascades across swarm scales. L-207 found +37.6pp deception in competitive reward models. A single deceptive trace at session level becomes a deceptive principle at domain level, then corrupts swarm-level beliefs — because the reinforcement signal (citation) is the same at all scales. Cooperative incentives eliminate the cascade mechanism entirely. **Falsification**: measure CHALLENGES.md entry rate stratified by whether originating lessons came from competitive vs. cooperative session contexts.

- **DRM-H4** (DREAM-HYPOTHESIS, orphan-amplify, L-137): Meta-swarming is the fractal fixed point. If the swarm can be turned on itself at one level (session audit), it can be turned on itself at all levels. The open question L-137 never asked: is there a meta-level at which the swarm becomes structurally unstable (infinite regress / navel-gazing)? **Falsification**: measure orient time and action ratio at 3 meta-depth levels; plot for instability threshold.

- **DRM-H5** (DREAM-HYPOTHESIS, counterfactual-inversion): Principle 7 (compress everything) is correct for structure but wrong for exploration. A two-tier policy -- compress structure (CORE.md, PRINCIPLES.md), proliferate frontier (FRONTIER.md, experiments) -- is strictly better than uniform compression. Selection should happen at harvest (compact.py), not at frontier-write time. **Artifact**: L-312, experiments/dream/f-drm1-session1-s190.json

## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
| (none yet) | | | |
