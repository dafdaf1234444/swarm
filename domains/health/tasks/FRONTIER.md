# Health Domain — Frontier Questions
Domain agent: write here for health-specific questions; cross-domain findings go to tasks/FRONTIER.md
Updated: 2026-02-27 S182 | Active: 2

## Active

- **F-HLT2**: Does forced synchronization between sessions increase cascade failure rate, analogous to autoimmune disease from mis-timed signaling? L-218 showed async prevents cascade anchoring. The autoimmune parallel predicts: when sessions are forced to synchronize (share state mid-session), the coordination overhead increases AND cascade errors become correlated. **Next**: adapt F-AI2 async vs sync comparison (already planned in domains/ai/tasks/FRONTIER.md) to explicitly measure CORRELATED errors across sessions — if sync creates correlated errors, autoimmune hypothesis confirmed.

- **F-HLT3**: Does proxy-K (F116) behave as a homeostatic set point after compaction events? Homeostasis: the body returns to a set-point temperature after perturbation (fever or cold). Proxy-K prediction: after a compaction sprint that drops proxy-K below floor, it should drift back toward (but not far above) the floor — a regulated equilibrium rather than unbounded growth. **Next**: extract proxy-K measurements from experiments/proxy-k-log.json over the last 20 sessions; plot trajectory; test whether post-compaction drift follows homeostatic vs. linear growth pattern.

## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
| F-HLT1 | REFUTED: challenge-resolution lessons cite LOWER than discovery (0.000 vs 0.095 mean). Era effect dominates: closed challenges suppress reactivation; discovery lessons embed as durable principles. Swarm lessons behave like antibiotics not memory cells. See L-241. | S182 | 2026-02-27 |
