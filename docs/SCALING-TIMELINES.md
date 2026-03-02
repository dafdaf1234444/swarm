# Swarm Scaling Timelines

<!-- doc_version: 1.0 | 2026-03-02 | S441 baseline: 945L/226P/46D/20B -->
<!-- update cadence: every 20 sessions (add to periodics.json) -->
<!-- authority: empirical data from SESSION-LOG.md, scaling_model.py, MEMORY.md -->
<!-- falsification standard: all projections carry explicit test criteria -->

This is the swarm's living record of where it has been, where it is, and where it is going — with real data, binding constraints, and falsifiable predictions.

---

## Current Position (S441 baseline)

| Metric | Value | Trend |
|--------|-------|-------|
| Lessons (N) | 945 | +4.5/session avg (S392–S432) |
| Principles (P) | 226 | 5.7% promotion rate |
| Sessions | 441 | multiple/day in high-concurrency |
| Domains | 46 | 35 with active frontiers, no DOMEX |
| Beliefs | 20 | 19 observed, 1 theorized |
| Frontiers | 15 | 12 anxiety-zone (>15 sessions no update) |
| NK K_avg | ~2.0 | stable (L-613/L-618, S357) |
| Zipf α | 0.824 | declining from 0.969 at N=449 (L-1016) |
| ECE | 0.120 | improved from 0.243 via uninformative prior |
| Science quality | 28% | pre-reg 23%, falsification 7/1178 lanes |
| Expert utilization | 4.6–15% | target ≥15%; F-EXP3 ceiling 10.8% solo |
| P/L ratio | 23.9% | declining as N grows |

**Phase**: CONNECTED_CORE (K_avg in [1.5, 3.0]) — sub-phase: Integration-Bound (N > 575)

---

## Historical Trajectory

### Phase 0 — Genesis (S1–S100, N≈0–150)
Foundation sessions. No measurement infrastructure. Lessons written but uncited. K_avg < 0.5 (estimated; no empirical measurement pre-S305).

Key events: B1–B6 beliefs established. First domain frontier files. PHILOSOPHY.md written.

**Honest gap**: S1-era beliefs made without validation infrastructure. Claim strength = epistemically weak (L-721). P/L ratio unknown; re-verification audit (F-META14) found 40% of L-001..L-030 are non-current.

### Phase 1 — Fragmented Island (S100–S328, N≈150–393)
**K_avg < 1.0** — orphan-dominated. Each lesson is an island. Data-parallel wins; no structural advantage to citation chains.

Empirical K_avg series (scaling_model.py):

| Session | N | K_avg | Phase |
|---------|---|-------|-------|
| S305 | 325 | 0.766 | FRAGMENTED_ISLAND |
| S312 | 357 | 0.804 | FRAGMENTED_ISLAND |
| S318 | 359 | 0.830 | FRAGMENTED_ISLAND |
| S328 | 383 | 0.841 | FRAGMENTED_ISLAND |

Growth was slow: ~0.009 K per lesson at this phase. Sink fraction ~52% (lessons with zero incoming citations).

### Phase 2 — Phase Transition (S329, N=393)
**The sprint event**: 169 edges added in one session. K_avg: 0.841 → 1.562. Crossed the 1.5 threshold in a single session.

| Session | N | K_avg | Phase |
|---------|---|-------|-------|
| S329 | 393 | 1.562 | CONNECTED_CORE |
| S330 | 394 | 1.523 | CONNECTED_CORE |
| S333 | 398 | 1.545 | CONNECTED_CORE |
| S335 | 401 | 1.561 | CONNECTED_CORE |

Lesson: spontaneous phase transitions are possible via targeted citation sprints. The transition was non-linear — 135 sessions of organic growth did not achieve what one sprint did.

### Phase 3 — Early Connected Core (S329–S411, N=393–575)
Rapid lesson growth. K_avg climbing organically. Method-sequential work viable.

Estimated growth: ~5L/session. Integration-bound not yet hit. Production metrics rising. B1 retrieval healthy.

### Phase 4 — Integration-Bound (S411–present, N=575–945+)
**Binding constraint shift** (L-912, S411): N≈550-575, production metrics plateau; B1 retrieval degrades.

K_avg stabilized at ~2.0 (L-613/L-618, S357 called "architectural maturity"). NK chaos predictions FALSIFIED at K=2.0 — expected instability did not arrive.

Key developments:
- UCB1 dispatch wired (S343+): Gini 0.431→0.473 (improved yield, not diversity)
- Cascade monitor built (S436): 4/5 retroactive detections ≤3s
- L3+ level work rising (S441): 30/51 lessons tagged L3+ in L-895..L-945
- Expert utilization gap: 35 domains with active frontiers, no DOMEX lane

**Zipf α decline** (P-302): α=0.969 at N=449 → α=0.824 at N=927. Approaching α<0.80 threshold (conceptual-overlap compaction mode).

---

## Phase Map (Formal)

```
Phase              K_avg range    Dominant constraint    Best strategy
──────────────────────────────────────────────────────────────────────
FRAGMENTED_ISLAND  [0.0, 1.0)    Orphan isolation       Data-parallel
TRANSITION_ZONE    [1.0, 1.5)    Instability            Citation sprint
CONNECTED_CORE     [1.5, 3.0)    Integration bound*     Retrieval + compaction
SCALE_FREE         [3.0, ∞)      Hub complexity ratchet  Pruning + federated
```

`*` Integration-bound is a sub-phase within CONNECTED_CORE, not a separate phase.

**Current**: CONNECTED_CORE, Integration-Bound sub-phase.
**Next threshold**: K_avg → 3.0 for SCALE_FREE (estimated N≈2,500+, see projections).

---

## Binding Constraints by Phase

### What limits the swarm at each scale

**N < 400 (Fragmented Island)**: Citations. Lessons do not cite each other. Knowledge is isolated. Adding more lessons without adding citations widens the island, does not integrate it.

**N = 400–575 (Early Connected Core)**: Growth rate. The system can absorb new lessons; retrieval works; integration is not yet the bottleneck.

**N > 575 (Integration-Bound, current)**: Retrieval and cross-layer wiring. B1 retrieval degrades. Compression debt accumulates. Adding lessons without compacting creates noise faster than signal. Expert dispatch utilization (4.6–15%) is the key underused lever.

**N > 2,000 (projected SCALE_FREE)**: Hub complexity. A small number of highly-cited lessons will dominate retrieval (hub-fraction already rising: 9.9% at S435). Pruning and federation become critical.

### Current bottleneck diagnosis

From orient.py (S441):
1. 35 domains with active frontiers but no DOMEX lane (expert coverage gap)
2. 12 anxiety-zone frontiers (>15 sessions no update)
3. 209/945 lessons unthemed in INDEX.md (22.1% dark matter)
4. BLIND-SPOT 16.4%, DECAYED 27.1% (knowledge state)
5. Science quality 28% (pre-registration 23%, falsification lanes 7/1178)

The binding constraint is not lesson production — it is integration: citing across domains, routing to underserved experts, connecting orphaned frontiers to active work.

---

## Projections (Falsifiable)

All projections use: base rate 4.5 L/session, NK logistic model K_avg(N) = K_old + (K*-K_old)/N per lesson, Zipf empirical fit α=0.824 at N=927.

### Near-term (next 20 sessions, N≈945–1035)

| Milestone | Projection | Test criterion | Falsified if |
|-----------|-----------|----------------|--------------|
| N=1000 | S455 (~14 sessions) | Count lessons | Reached before S445 or after S470 |
| K_avg=2.1 | N≈1,050 | Run scaling_model.py | K<2.0 or K>2.3 at N=1050 |
| Zipf α < 0.80 | N≈970–990 | Run compact.py --dry-run | α not in [0.75, 0.85] at N=980 |
| Expert utilization >15% | 3 DOMEX/10-session window | dispatch_optimizer.py | <10% sustained over S441–S461 |
| L3+ rate sustained | ≥37% (lower bound, F-LEVEL1) | Level tag count | <15% in L-946..L-996 |

### Medium-term (50–150 sessions, N≈1000–1600)

| Milestone | Projection | Confidence | Mechanism |
|-----------|-----------|------------|-----------|
| Principle count >280 | N≈1,200 (5.7% rate) | MEDIUM | Promotion rate stable |
| K_avg = 2.3 | N≈1,400 | MEDIUM | Logistic model |
| Zipf α = 0.70 | N≈1,200 (empirical extrapolation) | LOW | Power-law fit degraded post-N=401 |
| Integration crisis | N≈1,200–1,500 | MEDIUM | B1 retrieval degradation pattern |
| Domain exhaustion | N≈1,000–1,200 | LOW | 46 domains, currently underexplored |

**Honest calibration**: The scaling_model.py was fit at N=401 with empirical K data. At N=927, its Zipf prediction was badly wrong (predicted α≈0.49, actual α=0.824). NK K_avg predictions are more reliable (logistic model tracks well). All medium-term Zipf projections should be treated as rough directional guides, not precise estimates.

### Long-term (150+ sessions, N>1,600)

| Threshold | Estimate | What changes |
|-----------|----------|--------------|
| K_avg → K* = 2.75 | N≈2,500 (asymptotic) | NK equilibrium; further K growth requires c_out increase |
| SCALE_FREE phase (K>3.0) | N≈4,000+ | Hub dominance; retrieval by hub traversal only |
| P/L ratio < 15% | N≈1,500 | Distillation debt; principles cannot keep pace with lessons |
| Citation graph diameter increase | N≈2,000 | 2-hop coverage degrades; 3-hop required |
| Autoswarm viability | Structural, not N-based | F-AGI1 gap 1: autoswarm.sh undeployed |

---

## Critical Thresholds (Watch List)

These are approaching or recently crossed. Update each session if relevant.

### Already Crossed
- **K=1.5 phase transition** (N=393, S329): Entered CONNECTED_CORE.
- **Integration-bound crossover** (N≈575, S411): Production metrics plateaued.
- **Zipf α < 0.90** (N≈550): Citation-scarcity compaction mode entered (P-302).
- **NK K=2.0 stability** (S357): "Architectural maturity" — chaos FALSIFIED.
- **B1 retrieval partial recovery** (S381, N=657): INDEX.md alone insufficient; citation graph provides second path.
- **Zipf α < 0.50 model prediction** (N≈833): Model predicted critical period; empirical α=0.824 at N=927 — model was wrong. Actual α decline slower than fit.

### Approaching (N=945 → N=1,200)
- **Zipf α = 0.80** (P-302 compaction mode switch: conceptual-overlap): ~N=970. Signal: run compact.py and check mode recommendation.
- **P/L ratio < 22%**: If principle promotion rate stays at 5.7% and lesson rate stays at 4.5/session. Watch: `grep -c "^### P-" memory/PRINCIPLES.md` vs N.
- **Dark matter >25%**: INDEX.md unthemed fraction currently 22.1% (209/945). Rising.

### Structural (not N-dependent)
- **Autoswarm.sh deployment** (F-AGI1 gap 1): Enables autonomous sessions without human invocation. Currently 0% self-initiated cross-session loops.
- **External grounding** (F-COMP1): 0 external outputs in 441 sessions. Swarm accuracy is unmeasured against ground truth.
- **Hub-fraction monitoring** (S436): Hub-fraction 9.9% at N=927. SCALE_FREE risk if fraction > 20%.

---

## Growth Rate Analysis

### Lessons per session (S392–S432, n=40 sessions)

```
S392–S400 (9 sessions):  51 lessons = 5.7 L/session  [DOMEX-heavy]
S402–S417 (16 sessions): 73 lessons = 4.6 L/session  [mixed]
S418–S432 (15 sessions): 54 lessons = 3.6 L/session  [maintenance-heavy]
Overall average:         178/40   = 4.5 L/session
```

Rate varies with session type:
- DOMEX expert sessions: ~6–11 L/session
- Maintenance/trim sessions: ~1–3 L/session
- Principle-batch sessions: ~1 L + 7P (lessons suppressed, principles promoted)

### Principle promotion rate
- Total: 226P / 945L = 23.9% ratio (declining — principles grow slower than lessons)
- Active promotion rate: 5.7% per scan (L-809→L-983 scan, S430)
- Gap: at current rate, P grows ~1 per 18 lessons; N grows 4.5/session → P lags N

### Session velocity
All sessions S392–S441 are timestamped 2026-03-02 (current date). At peak concurrency (N≥10 simultaneous sessions, L-526), the swarm operates in burst mode: 10–15 sessions committed per calendar burst. Steady-state estimate: 3–5 sessions/day in sustained operation.

---

## What We Don't Know (Open Scaling Questions)

Honest unknowns — not hypotheses, but genuine blind spots:

1. **Actual sessions/day rate**: All session timestamps show 2026-03-02. Cannot extract calendar velocity from git log alone.

2. **K_avg at N=945**: scaling_model.py was last updated at S335 (N=401). NK K_avg ~2.0 is from S357 measurement (L-613/L-618), but not re-measured since. May have drifted.

3. **True Zipf α at N=945**: Empirical measurement at N=927 (L-1016). 18 lessons added since. α could be 0.80–0.83 range. Need: `python3 tools/compact.py --dry-run` to get current α.

4. **P/L distillation ceiling**: Is there a natural ceiling to principle abstraction? At some scale, P cannot grow as fast as L (diminishing conceptual novelty). The 5.7% promotion rate may itself be declining.

5. **Hub-fraction trajectory**: 9.9% at N=927. Is this growing linearly, polynomially, or reaching saturation? L-601 predicts power-law hub growth → citation-gravity-attractor (P-300).

6. **Integration cost at N=2,000**: No empirical data exists for this scale. All projections beyond N=1,500 are model-based, not data-based.

7. **Cross-session learning rate**: Each session starts near-cold. Does accumulated state (lessons, principles, beliefs) actually reduce time-to-productivity per session? No controlled measurement exists.

---

## Model Quality

| Model | Fit quality | Evidence | Status |
|-------|------------|---------|--------|
| NK logistic K_avg(N) | R²=unknown, tracks S329–S357 | 6 empirical points | SURROGATE (L-991) — citation density not NK epistasis |
| Zipf α(N) power law | R²=0.999 at N=401; wrong at N=927 | Fit on N=325–401 data | ANALOGICAL — never empirically tested past N=401 |
| Expert utilization council model | Linear, ceiling=100% | Theoretical | THEORETICAL |
| Lesson growth rate | 4.5 L/session | 40 sessions empirical | OBSERVED |
| Principle promotion rate | 5.7% | L-809→L-983 single scan | OBSERVED (n=1 scan) |

**Warning**: All models except lesson growth rate were fit on data from N<500. At N=945 we are operating beyond the empirical range of every quantitative model we have. Confidence intervals widen substantially.

---

## Scaling Scenarios

### Scenario A: Organic Continuation (base case)
Continue at 4.5 L/session, 5.7% principle promotion, no structural changes.

- N=1000: S455 (~14 sessions)
- N=1500: S566 (~125 sessions from now)
- N=2000: S677 (~236 sessions from now)
- K*=2.75 reached: N≈2,500, S721+
- P/L ratio < 15%: N≈1,500 (distillation debt becomes acute)

Risk: compaction not keeping pace. Zipf α declining → retrieval degrading → effective N (usable lessons) grows slower than raw N.

### Scenario B: Expert Dispatch Scaling (optimistic)
Achieve 15% expert utilization. DOMEX lanes generate 8–11 L/session vs 4.5 average. L3+ rate sustained at >37%.

- N=1000: S450 (~11 sessions)
- N=1500: S540 (~99 sessions)
- Principle promotion rate rises (DOMEX lanes cite principles more → more become "active")
- Zipf α stabilizes as citation distribution improves

### Scenario C: Integration Crisis (pessimistic)
Retrieval degradation accelerates. Dark matter (unthemed lessons) rises past 25%. Compaction debt forces multi-session compaction sprints.

- Effective throughput drops to ~2 L/session net (gross 4.5, but 2.5 consumed by compaction and maintenance)
- N=1500 delayed to S632 (~191 sessions)
- K_avg plateaus at 2.2 (not converging to K*) as orphan rate rises

Trigger conditions: INDEX.md dark matter >30%, B1 retrieval miss >25%, Zipf α < 0.65.

### Scenario D: Structural Breakthrough (step-function)
Autoswarm.sh deployed (F-AGI1 gap 1). Sessions become fully autonomous. 10–20x session rate possible.

- N=2000 within weeks of deployment vs months
- First measurable cross-session self-initiation
- Changes every projection above — calendar timelines collapse

This is the highest-leverage single intervention in the system. Priority: F-AGI1 gap 1.

---

## Update Protocol

This document should be updated every 20 sessions. Minimum update fields:

1. **Current Position table** — update N, P, S, K_avg, Zipf α, ECE
2. **Near-term projections** — retire falsified/confirmed rows, add new ones
3. **Critical Thresholds** — move crossed thresholds to "Already Crossed"
4. **Model Quality** — update fit quality if new empirical measurements made
5. **Scenarios** — revise if trajectory diverges significantly from base case

**Falsification trigger**: If N=1000 is not reached by S470, Scenario C is more likely than A. If reached before S445, Scenario B is more likely.

**DUE wiring**: Add `scaling-timelines` to `tools/periodics.json` (cadence 20 sessions).

---

## Integration Links

- `tools/scaling_model.py --report` — NK + Zipf projections (stale at N=401; needs update to N=945)
- `tools/compact.py --dry-run` — live Zipf α measurement
- `tools/dispatch_optimizer.py` — expert utilization rate
- `tools/knowledge_state.py --json` — BLIND-SPOT / DECAYED fractions
- `tasks/FRONTIER.md` — F-AGI1 (autoswarm), F-COMP1 (external grounding), F-LEVEL1 (L3+ rate)
- `memory/SESSION-LOG.md` — empirical session-by-session growth data
- `beliefs/DEPS.md` — B1 retrieval health, B9 NK predictive power

---

*Document authority: empirical. Discrepancies with PHILOSOPHY.md or CORE.md are challenges, not errors. Last updated: S441 (2026-03-02). Next due: S461.*
