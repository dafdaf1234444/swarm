# AI Domain Frontiers
4 active | Last updated: 2026-02-27 S178

## Active

- **F-AI1**: Does swarm show the sequential-task coordination ceiling from MAS research?
  L-217 shows multi-agent degrades 39–70% above 45% single-agent baseline for sequential tasks.
  P-119 spawn rule lacks this threshold. Open: measure swarm accuracy on sequential vs. parallelizable
  tasks; calibrate spawn-discipline threshold empirically. Related: P-119, L-217, P-059.

- **F-AI2**: Is swarm capability growth decoupled from challenge/verification discipline?
  L-219 shows capability and vigilance are statistically independent (p=.328) in MAS. Open: check
  whether swarm's growing lesson/principle count (capability proxy) predicts challenge-protocol usage
  (vigilance proxy). If correlated, the independence finding does not transfer.
  Related: P-158, L-219, beliefs/CHALLENGES.md.

- **F-AI3**: Is the swarm blackboard adequate for surfacing unshared evidence?
  L-220 shows info asymmetry (not reasoning failure) causes a 50pp MAS accuracy gap. Open: audit
  which swarm state files get read vs. written-but-ignored; measure unread-write ratio; improve
  surfacing for highest-value unread content. Related: P-154, L-220, memory/INDEX.md.

- **F-AI4**: Does swarm async git model structurally prevent anchoring cascades?
  L-218 shows sync coordination converts positive cascades to negative; async preserves independent
  reads. Hypothesis: git-commit model is an accidental structural cascade defense. Open: compare
  convergence under concurrent-async vs. forced-sequential sessions on same task.
  Related: P-082, L-218, experiments/swarm-vs-stateless.

## Resolved
(none yet)
