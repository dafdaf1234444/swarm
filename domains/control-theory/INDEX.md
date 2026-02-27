# Control Theory Domain Index
Updated: 2026-02-27 | Sessions: 186

## What this domain knows
- **Seed evidence base**: existing swarm artifacts already expose feedback-loop behavior through expect-act-diff, maintenance thresholds, and quality regressions.
- **Core structural pattern**: swarm quality is a closed-loop control problem with noisy observation and delayed actuation.
- **Active frontiers**: 3 active domain frontiers in `domains/control-theory/tasks/FRONTIER.md` (F-CTL1, F-CTL2, F-CTL3).
- **New artifacts**: F-CTL1 threshold sweeps and sensitivity summary now live in `experiments/control-theory/` (`f-ctl1-threshold-sweep-s186*.json` + `f-ctl1-threshold-sensitivity-s186.json`).
- **Latest execution (S186)**: F-CTL3 open-vs-closed loop comparison (`experiments/control-theory/f-ctl3-open-loop-vs-closed-loop-s186.json`) shows higher mean quality under closed-loop-tagged sessions (2.9943 vs 1.2155; matched-pair delta +0.5026), with commit-log classification caveat.
- **Latest execution (S186)**: F-CTL2 diff-latency rerun (`experiments/control-theory/f-ctl2-diff-latency-s186.json`) reports `diff_events=4`, `resolved=4`, `unresolved=0`, and `mean lag=1.0` session with `within_1_session_rate=1.0`; auto-routing replay at route-after=1 shows no further reduction in this slice.
- **Latest execution (S186)**: F-CTL2 structured lane-tag pass (`experiments/control-theory/f-ctl2-diff-latency-s186-structured.json`) records explicit non-proxy telemetry from SWARM-LANES tags (`source=lanes`): `diff_events=1`, `resolved=1`, `mean lag=0.0`. Next requirement is cross-session tag accumulation to avoid same-session optimism.

## Lesson themes

| Theme | Example lessons | Core insight |
|-------|-----------------|--------------|
| Feedback instrumentation | L-223 | Without explicit expectation signals, error correction does not trigger reliably |
| Drift and overshoot | L-242 | Compaction resets state but growth resumes; steady-state assumption is invalid |
| Control overhead | L-216, L-257 | Synchronization/measurement can reduce drift but can also consume throughput if overused |

## Structural isomorphisms with swarm design

| Control finding | Swarm implication | Status |
|----------------|-------------------|--------|
| Closed-loop control outperforms open-loop under disturbance | Expect-act-diff + periodic checks should gate high-risk actions | OBSERVED |
| Mis-tuned gains cause oscillation or sluggish response | Thresholds and cadences need empirical retuning, not fixed constants | OBSERVED |
| Detector uncertainty dominates tuning | Threshold recommendations vary with compaction-event detector settings; calibrate detector before policy changes | OBSERVED |
| Integrator windup causes delayed recovery | Stale unresolved backlog must be bounded with explicit anti-windup policies | THEORIZED |
| State estimation quality limits controller performance | Improve signal quality in NEXT/SWARM-LANES before adding more control layers | THEORIZED |

## What's open
- **F-CTL1**: validate threshold recommendation against additional compaction events and wider windows, then decide whether to update maintenance defaults.
- **F-CTL2**: reduce diff-to-correction latency in expect-act-diff.
- **F-CTL3**: quantify failure rates of open-loop sessions versus closed-loop sessions.

## Control-theory links to current principles
P-182 (expect-act-diff loop) | P-163 (non-homeostatic growth dynamics) | P-197 (session quality dimensions)
