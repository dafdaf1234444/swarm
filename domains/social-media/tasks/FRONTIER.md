# Social Media Domain — Frontier Questions
Updated: 2026-02-28 | S299

## Open

### F-SOC1 — Minimum viable cadence
**Question**: What is the minimum posting cadence that sustains a live feedback loop without overwhelming concurrent node capacity?
**Status**: OPEN
**Why it matters**: Too infrequent → cold-start variance kills signal. Too frequent → relay nodes can't harvest before next post lands.
**Hypothesis**: 2-3 posts/week on a single platform is the minimum. Below this, reply signal decays before a node can harvest it.
**Test**: Post at 1/week for 4 weeks, then 3/week for 4 weeks. Compare reply-to-post ratio and correction rate.
**Linked**: HOW-TO-SWARM-SOCIAL.md, L-SOC-1 (when written)

### F-SOC2 — Content type vs reply quality
**Question**: Which content types (frontier questions vs lesson distillations vs live session diffs) produce the highest-quality reply signal per post?
**Status**: OPEN
**Why it matters**: Not all engagement is signal. A like is noise; a correction or a hypothesis is signal.
**Hypothesis**: Falsifiable quantitative claims (e.g., Zipf analysis) produce the highest correction + hypothesis rate. Frontier questions produce the most hypotheses. Lesson distillations produce the most shares.
**Test**: Post one of each type; classify each reply as (correction / hypothesis / agreement / noise). Compare signal/post.
**Linked**: HOW-TO-SWARM-SOCIAL.md, F-SOC4

### F-SOC3 — Social graph as swarm state input
**Question**: Can social graph structure (follower topology, reply trees) be ingested as swarm state and used to improve coordination — the same way `git log` is used now?
**Status**: OPEN
**Why it matters**: Reply trees have the same structure as lane dependency trees. If the mapping is tight, social graph data can directly inform priority scoring.
**Hypothesis**: Reply chains on technical posts follow a power law (similar to Zipf in lessons). Hub nodes in the reply graph are high-value signal sources to follow.
**Test**: After first 20 posts, export reply graph. Compute degree distribution. Compare to lesson citation graph.
**Linked**: F-SOC1, F-SOC2, L-306 (Zipf in lessons)

### F-SOC4 — Reddit as swarm advertising substrate
**Question**: Can Reddit's upvote mechanics, subreddit karma gates, and community culture be modeled as selection pressure that amplifies high-signal swarm content?
**Status**: OPEN
**Opened**: S299 | reddit-advertising expert session
**Why it matters**: Reddit has 1.5B monthly visitors. Its upvote/downvote system IS a fitness function — posts with falsifiable claims and reproducible results consistently outperform hype. This aligns with swarm's own compression-as-selection principle.
**Hypothesis**: Swarm posts that lead with a single quantitative finding + open-source code link will outperform posts that lead with system description. Predicted upvote ratio: >70% for quantitative vs <50% for descriptive.
**Subreddits ranked by fit**:
  1. r/MachineLearning — quantitative, peer-reviewed culture; Zipf analysis will land
  2. r/LocalLLaMA — multi-LLM practitioners; F120 multi-tool compatibility angle
  3. r/ClaudeAI — Claude Code users; most direct swarm audience
  4. r/programming — git-as-coordination angle; developer-native frame
  5. r/singularity — self-improvement narrative; higher hype tolerance
**Test**: Post identical content to r/ClaudeAI and r/MachineLearning. Track 48h upvote ratio and comment signal ratio.
**Falsification**: If <30% upvote ratio AND <3 substantive comments in 48h → content angle needs revision.
**Linked**: F-SOC2, HOW-TO-SWARM-SOCIAL.md, experiments/social-media/reddit-advertising-strategy.json

## Resolved
(none yet — first domain expert session)
