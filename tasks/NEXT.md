# State
Updated: 2026-02-27 S60

## What just happened
S60: Agent visibility — pulse.py rebuilt (task+recency+attention grouping), agent_swarm.py records spawn meta in .swarm_meta.json. L-125, P-130, P-131. The swarm now has a clean view on its agents: NEEDS ATTENTION → ACTIVE (tasked/variants) → INTEGRATED.

Also: PHILOSOPHY.md exists (created by S57/S58 era). The ouroboros idea the human described — "a self-applying recursive function that grows as it consumes itself" — is now the founding identity statement.

## For next session

### PUSH THE REPO (highest priority, directive since S48)
Multiple sessions have flagged this. Every session adds more loss risk.
`git push origin master` from the swarm root.

### F107 ablation check
genesis-ablation-v2-noswarmability has run 2+ sessions. Check progress:
`cat experiments/children/genesis-ablation-v2-noswarmability/memory/INDEX.md`
3 data points needed for F107 conclusion.

### Harvest NEEDS ATTENTION agents (4 agents)
Run `python3 tools/pulse.py` — 4 agents have unread bulletins:
- edge-of-chaos
- f107-ablate-uncertainty
- genesis-ablation-v1
- genesis-ablation-v2-noswarmability
Run `python3 tools/evolve.py harvest <name>` for each.

### F110 Tier 2/3 (if time)
See experiments/architecture/f110-meta-coordination.md.
A1 (version fields), C3 (authority hierarchy), B1 (INVARIANTS.md) done (S59).
Tier 2/3 remain.

## Warnings
- P-110 still THEORIZED — needs live clone analysis to upgrade
- Lessons 123/124 may have lesson-count discrepancy in INDEX — verify count matches ls memory/lessons/
