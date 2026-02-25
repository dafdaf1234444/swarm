# Spawn Protocol v0.1

## What
Creating a child swarm (new git repo) for a scoped sub-problem. Child inherits structure via genesis.sh, develops its own beliefs. Findings merge back to parent.

## When to Spawn
- A frontier question needs >5 sessions of focused work
- You want to A/B test an approach (fork, explore, compare)
- A domain shift is needed (parent = architecture, child = specific implementation)
- Human requests: "spawn [topic]"

## How to Spawn
1. Define scope: 5-line brief of what child should accomplish
2. Run: `./workspace/genesis.sh ~/child-swarm-[name] "[topic]"`
3. Replace child's TASK-001 with the scoped brief
4. Seed: copy ONLY relevant lesson files from parent (not all)
5. Init: `cd child && git init && git add -A && git commit -m "[S] init: spawned from parent for [topic]"`
6. Record in parent FRONTIER.md: "Child swarm [name] exploring [topic]"

## Merge-Back (when child completes)
1. Child compresses findings into 1-3 lesson files
2. Parent session reads child's compressed output
3. Parent evaluates: do findings affect parent beliefs?
4. If yes: update via Rule 6 (adaptability)
5. If no: record as lesson with `Source: child-swarm/[name]`
6. Mark parent frontier question resolved

## Children inherit: structure, epistemic rules, validator, hooks
## Children do NOT inherit: parent lessons, beliefs, tasks, experiments
## Limit: max 3 active children (each needs human supervision)
