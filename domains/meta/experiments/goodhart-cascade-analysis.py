#!/usr/bin/env python3
"""
Quantitative analysis of Goodhart Cascade data.
Tests: Is there a mathematical regularity in cascade propagation?
"""

import numpy as np
from dataclasses import dataclass

@dataclass
class GoodhartStep:
    lesson: str
    session: int
    level: int  # abstraction layer 0-5
    inflation: float  # inflation factor (NaN if non-numeric)
    label: str

# The 12 documented Goodhart effects, ordered by session
cascade = [
    GoodhartStep("L-566",  351, 0, 2.6,  "mention vs creation proxy"),
    GoodhartStep("L-666",  367, 0, float('nan'), "Simpson's paradox confound"),
    GoodhartStep("L-669",  367, 0, 1.9,  "volume proxy for quality"),
    GoodhartStep("L-813",  397, 1, 8.0,  "3 measurement systems inflate (worst case)"),
    GoodhartStep("L-895",  407, 1, float('nan'), "87% L2 crowding out (ratio, not factor)"),
    GoodhartStep("L-950",  423, 2, float('nan'), "89.8% citation ≠ invocation"),
    GoodhartStep("L-1012", 434, 1, 3.26, "hub super-linear attachment"),  # lateral
    GoodhartStep("L-1057", 443, 2, float('nan'), "self-application Goodharted"),
    GoodhartStep("L-1119", 458, 3, 1.82, "45% misclassification → true/claimed = 12/21.8"),
    GoodhartStep("L-1192", 476, 4, float('nan'), "22/22 criteria self-referential"),
    GoodhartStep("L-1204", 477, 4, 1.5,  "3/3 → 2/3 score drop"),
    GoodhartStep("L-1211", 477, 5, float('nan'), "0% voluntary repair rate"),
]

print("=" * 70)
print("GOODHART CASCADE QUANTITATIVE ANALYSIS")
print("=" * 70)

# 1. Inter-step interval (sessions between discoveries)
sessions = [s.session for s in cascade]
intervals = [sessions[i+1] - sessions[i] for i in range(len(sessions)-1)]
print(f"\n1. INTER-STEP INTERVALS (sessions between discoveries)")
print(f"   Intervals: {intervals}")
print(f"   Mean: {np.mean(intervals):.1f} sessions")
print(f"   Median: {np.median(intervals):.1f} sessions")
print(f"   Trend: {'ACCELERATING' if intervals[-1] < intervals[0] else 'DECELERATING'}")

# Is the interval decreasing? (acceleration)
first_half = intervals[:len(intervals)//2]
second_half = intervals[len(intervals)//2:]
print(f"   First half mean: {np.mean(first_half):.1f}")
print(f"   Second half mean: {np.mean(second_half):.1f}")
ratio = np.mean(second_half) / np.mean(first_half) if np.mean(first_half) > 0 else float('inf')
print(f"   Acceleration ratio: {ratio:.2f} (< 1.0 = accelerating)")

# 2. Abstraction level progression
levels = [s.level for s in cascade]
print(f"\n2. ABSTRACTION LEVEL PROGRESSION")
print(f"   Levels: {levels}")
# Check monotonicity (ignoring lateral branches)
main_chain = [s for s in cascade if s.lesson != "L-1012"]  # exclude lateral
main_levels = [s.level for s in main_chain]
monotonic = all(main_levels[i] <= main_levels[i+1] for i in range(len(main_levels)-1))
print(f"   Main chain monotonic: {monotonic}")
print(f"   Main chain levels: {main_levels}")

# Linear regression: level vs step number
steps = np.arange(len(levels))
slope, intercept = np.polyfit(steps, levels, 1)
residuals = [levels[i] - (slope * i + intercept) for i in range(len(levels))]
r_squared = 1 - np.var(residuals) / np.var(levels)
print(f"   Linear fit: level = {slope:.3f} * step + {intercept:.3f}")
print(f"   R² = {r_squared:.3f}")

# 3. Inflation magnitude analysis
inflations = [(s.lesson, s.inflation) for s in cascade if not np.isnan(s.inflation)]
print(f"\n3. INFLATION MAGNITUDES")
for lesson, infl in inflations:
    print(f"   {lesson}: {infl:.2f}x")
inf_vals = [i for _, i in inflations]
print(f"   Mean inflation: {np.mean(inf_vals):.2f}x")
print(f"   Geometric mean: {np.exp(np.mean(np.log(inf_vals))):.2f}x")

# 4. Fix-reveal ratio computation
fix_sessions = {397, 407, 423, 443, 458, 476, 477}  # sessions where fixes were applied
reveals_per_fix = {
    397: ["L-895", "L-1012"],  # L-813 fix revealed measurement-level and hub issues
    407: ["L-950"],             # L-895 fix revealed self-application
    423: ["L-1057"],            # L-950 fix revealed citation ≠ invocation
    443: ["L-1119"],            # L-1057 fix revealed tag inflation
    458: ["L-1192"],            # L-1119 fix revealed eval self-referentiality
    476: ["L-1204", "L-1211"], # L-1192 fix revealed grounding bypass + enforcement gap
}
print(f"\n4. FIX-REVEAL RATIO")
ratios = [len(v) for v in reveals_per_fix.values()]
print(f"   Per-fix reveals: {ratios}")
print(f"   Mean fix-reveal ratio: {np.mean(ratios):.2f}")
print(f"   Always ≥ 1: {all(r >= 1 for r in ratios)}")

# 5. Cascade velocity (abstraction levels gained per session)
total_levels = max(levels) - min(levels)
total_sessions = max(sessions) - min(sessions)
velocity = total_levels / total_sessions if total_sessions > 0 else 0
print(f"\n5. CASCADE VELOCITY")
print(f"   Total levels traversed: {total_levels}")
print(f"   Total sessions elapsed: {total_sessions}")
print(f"   Velocity: {velocity:.4f} levels/session")
print(f"   Time to traverse 1 level: {1/velocity:.1f} sessions")

# 6. Key finding: is there a power law?
# Plot sessions since cascade start vs cumulative Goodhart effects
t0 = sessions[0]
cumulative = list(range(1, len(sessions)+1))
elapsed = [s - t0 for s in sessions]
print(f"\n6. ACCUMULATION PATTERN")
print(f"   Elapsed sessions: {elapsed}")
print(f"   Cumulative effects: {cumulative}")
# Fit: cumulative = a * elapsed^b
log_elapsed = np.log([max(e, 1) for e in elapsed])
log_cumulative = np.log(cumulative)
b, log_a = np.polyfit(log_elapsed[1:], log_cumulative[1:], 1)  # skip first (elapsed=0)
a = np.exp(log_a)
print(f"   Power law fit: N(t) = {a:.3f} * t^{b:.3f}")
print(f"   Exponent b = {b:.3f}")
if b > 1:
    print(f"   → SUPER-LINEAR: cascade accelerates")
elif b < 1:
    print(f"   → SUB-LINEAR: cascade decelerates")
else:
    print(f"   → LINEAR: constant rate")

# 7. Summary statistics
print(f"\n{'=' * 70}")
print(f"SUMMARY")
print(f"{'=' * 70}")
print(f"  Cascade length: {len(cascade)} steps over {total_sessions} sessions")
print(f"  Abstraction layers: L0 → L5 (6 levels)")
print(f"  Main chain monotonic: {monotonic}")
print(f"  Fix-reveal ratio: {np.mean(ratios):.2f} (always ≥ 1)")
print(f"  Cascade velocity: {velocity:.4f} levels/session ({1/velocity:.0f} sessions/level)")
print(f"  Accumulation: {'super-linear' if b > 1 else 'sub-linear'} (exponent {b:.2f})")
print(f"  Mean inflation: {np.mean(inf_vals):.1f}x (geometric: {np.exp(np.mean(np.log(inf_vals))):.1f}x)")
print(f"\n  KEY FINDING: The Goodhart cascade is {'' if b > 1 else 'NOT '}self-accelerating")
print(f"  KEY FINDING: Fix-reveal ratio = {np.mean(ratios):.2f} > 1.0 → cascade EXPANDS")
print(f"  KEY FINDING: Main chain is monotonically upward through abstraction layers")
