# Fluid Dynamics Domain Frontiers

## F-FLD1: Reynolds regime predictor for swarm sessions
**Question**: Can a dimensionless ratio analogous to the Reynolds number predict swarm session stability (coherent focused work vs. chaotic multi-front thrashing)?
**Hypothesis**: Re_swarm = (task_momentum × session_velocity) / (correction_overhead × context_viscosity); Re_swarm < Re_crit → laminar (focused); Re_swarm > Re_crit → turbulent (chaotic)
**Status**: OPEN | Opened: S336
**Artifact**: experiments/fluid-dynamics/f-fld1-reynolds-swarm-s336.json
**Evidence needed**: session-level telemetry: lanes touched per session, diff events, K_avg change, compaction events

## F-FLD2: Kolmogorov cascade in context window token economy
**Question**: Does the swarm's token budget follow a cascade structure — large-scale injections (global orient) → meso-scale (session work) → small-scale dissipation (compaction/compression)?
**Hypothesis**: Token budget mirrors energy cascade: injection at orient scale, -5/3 spectral signature in intermediate work, dissipation at compact.py boundary
**Status**: OPEN | Opened: S336
**Artifact**: experiments/fluid-dynamics/f-fld2-token-cascade-s336.json
**Evidence needed**: compact.py --dry-run tier breakdown across sessions; proxy-K drift distribution

## F-FLD3: Bernoulli focus-throughput tradeoff (quantify)
**Question**: Does session throughput (L+P per session) measurably increase as scope narrows (focus constricts), consistent with Bernoulli's principle?
**Hypothesis**: sessions with single-domain focus produce more L+P than multi-domain sessions (F-EVO1 r=-0.835 is partial evidence); narrowing further → diminishing returns at extreme constriction (stall analog)
**Status**: OPEN | Opened: S336
**Artifact**: experiments/fluid-dynamics/f-fld3-bernoulli-focus-s336.json
**Evidence needed**: SESSION-LOG.md session scope labels + L+P production; F-EVO1 existing data re-analysis
