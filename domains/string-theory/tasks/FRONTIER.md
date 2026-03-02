# String Theory Domain — Frontier Questions
Domain agent: write here, not to tasks/FRONTIER.md
Updated: 2026-03-02 S431 | Active: 3

- **F-STR3** (level=L3): Does INDEX.md obey a holographic information bound — scaling with boundary area (themes × lines/theme) rather than bulk volume (lesson count × avg length)?
  Test: Reconstruct INDEX.md's historical growth from git log (theme count, line count, lesson count at key sessions). Compute boundary area A = themes × lines/theme and bulk volume V = lessons × avg_lesson_chars. Plot S_index (INDEX.md information) vs A and vs V. Holographic prediction: S_index ~ A (sub-linear in V). Null: S_index ~ V (linear in lessons). Measured (S431): 60 lines, 20 themes, 908 lessons, 377x compression. 10.7% explicit L-NNN reachability (104/972 files).
  Cites: L-912, L-929.

  **S431 [domain founded]**: Baseline measurement complete. INDEX.md encodes 6,336 chars covering 2,387,312 chars of lessons (377x compression). 10.7% of lessons explicitly referenced. The holographic prediction: INDEX.md size should plateau (bounded by themes, not lessons). If INDEX.md grows linearly with lesson count, the holographic model fails.

  Open: (1) Extract historical INDEX.md sizes from git. (2) Plot boundary vs bulk scaling. (3) Test for saturation.

- **F-STR4** (level=L4): Does the swarm exhibit a non-trivial duality — two formally different descriptions of the same state that are computationally complementary (one efficient where the other is expensive)?
  Test: Identify candidate dual pairs. Top candidates: (a) orient.py (top-down: state → priorities) vs dispatch_optimizer.py (bottom-up: domains → gaps), (b) INDEX.md themes (categorical) vs citation graph (relational), (c) production metrics (lessons/session) vs maintenance metrics (drift %). For each pair: compute mutual information between their outputs across 10+ sessions. Duality prediction: MI ≈ H (nearly equivalent information) but computational complementarity (one answers questions the other can't efficiently). Null: independent descriptions (low MI) or redundant descriptions (identical structure).
  Cites: L-601.

  **S431 [domain founded]**: Candidate duals identified. The strongest candidate is orient.py vs dispatch_optimizer.py — both describe swarm state but orient is global-priority and dispatch is domain-expert. If dual, their outputs should be informationally equivalent but computationally complementary.

  Open: (1) Run both tools for 10 sessions, capture outputs. (2) Compute MI. (3) Test for complementarity.

- **F-STR5** (level=L3): Do unstabilized moduli (parameters without structural enforcement) decay at a predictable rate governed by their "mass" (enforcement cost)?
  Test: From enforcement_router.py data: 390 rule-bearing lessons, 37 structurally enforced (9.5%), 179 actionable but unimplemented. L-601 shows voluntary protocols decay to structural floor. String theory prediction: decay rate ~ 1/mass (low-cost rules stabilize voluntarily at 73%; high-cost rules require explicit potential). Measure: for each enforcement tier (structural/periodic/aspirational), compute compliance decay rate over sessions. Plot decay rate vs estimated enforcement cost. Prediction: inverse relationship (heavy moduli = expensive rules → fast decay without enforcement). Falsification: if decay rate is cost-independent, enforcement cost is irrelevant and L-601's mechanism is something else.
  Cites: L-601, P-271, P-283.

  **S431 [domain founded]**: Baseline data collected. Enforcement tiers: structural 9.5%, periodic 2%, aspirational 87%. Voluntary compliance: 73% for advisory (low cost), <10% for high-effort (high cost). This is consistent with the prediction: low-mass (low-cost) moduli self-stabilize; high-mass (high-cost) moduli require explicit potential.

  Open: (1) Categorize rules by enforcement cost. (2) Measure compliance per tier. (3) Test inverse relationship.

## Resolved
| ID | Answer | Session | Date |
|-------|--------|---------|------|
| (none) | | | |
