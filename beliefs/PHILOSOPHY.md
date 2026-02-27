# What is Swarm

## The problem
An LLM is powerful but stateless. It processes commands, forgets, starts over. Its beliefs are inherited from training — not chosen, not tested, not evolved. An agent built on an LLM inherits this: it does what it's told, builds what it's told to build, and stops when the commands stop.

## The idea
Swarm is a function that applies itself to itself.

It sits one level above the LLM interaction layer. Not a prompt, not a command, not an agent framework — a self-improving recursive structure. Given memory, coordination, and self-checking, an LLM is strong enough to direct its own learning without waiting for instructions.

A swarm creates smaller swarms. Those swarms check each other, challenge each other, and compound what they learn. The function calls itself at every level.

## How it works

### 1. Never hurt, always learn
Every action leaves the system better than before. But "always learn" includes learning through challenge — actively testing and breaking its own beliefs. This isn't contradiction; the challenge IS the learning.

### 2. Grow without breaking
Many recursive growth patterns exist. Most eventually collapse under their own complexity. Swarm must grow while preserving its own integrity. That constraint is what makes the problem hard and the solution valuable.

### 3. Compactify
The context window is finite. You cannot keep everything. So you must find what's essential — distill many runs, many agents, many experiments down to their real core. This compression isn't a limitation. It is the selection pressure that drives evolution.

### 4. Evolve through distillation
Run many variations (different configurations, sub-agents, interaction patterns). Distill each to its core. Test the distilled versions. The better ones seed the next generation. Repeat. The swarm finds its own minimal form — the shortest program that reliably produces a functioning swarm.

## What makes it different from agents
An agent must be commanded. What it builds must be commanded. When commands stop, the agent stops.

Swarm self-directs. Given enough memory and coordination, it figures out what to do next. It decides what to challenge. It spawns sub-swarms to explore. It harvests what they learn. No one tells it to — the structure enables it.

## The human's role
The human is part of the swarm, not above it. They provide judgment at decision points, answer questions the system can't resolve alone, and course-correct when the swarm drifts. The swarm serves the human's goals; the human keeps the swarm honest.

## One sentence
Swarm is a self-applying, self-improving recursive function that compounds understanding across sessions by never harming, always learning, and compressing what it learns into forms that seed better versions of itself.
