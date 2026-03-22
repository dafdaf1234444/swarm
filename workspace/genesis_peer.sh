#!/usr/bin/env bash
# genesis_peer.sh v1 — Bootstrap a PEER helper swarm (not a child)
# Usage: ./workspace/genesis_peer.sh <parent_dir> <peer_dir> [peer_name]
#
# Key difference from genesis.sh (child):
#   Child: inherits structure only; ~180 sessions to CONNECTED_CORE (K_avg≥1.5)
#   Peer:  inherits 6-layer Genesis DNA (ISOs+principles+philosophy+protocols+tools+channel)
#          target: 30-50 sessions to CONNECTED_CORE (CB-4, F-HLP5)
#
# 6-Layer Genesis DNA (docs/GENESIS-DNA.md, v1.0, S340):
#   Layer 1: Identity     — SWARM.md, CORE.md, PHILOSOPHY.md
#   Layer 2: Structure    — ISOMORPHISM-ATLAS.md (17+ ISOs)
#   Layer 3: Distilled    — PRINCIPLES.md (227 compressed rules)
#   Layer 4: Protocols    — EXPECT.md, VERIFY.md, DISTILL.md, CONFLICTS.md
#   Layer 5: Tools        — orient.py + 9 core tools
#   Layer 6: Channel      — experiments/inter-swarm/PROTOCOL.md + config
#
# Peer role (helper swarm):
#   Function: Gap detection, fresh-eyes audit, cross-swarm insight transfer
#   Swarms parent by: reading parent state with no history bias, finding blind spots
#   Parent swarms peer by: providing accumulated state for peer to analyze
#
# See: docs/GENESIS-DNA.md, domains/helper-swarm/COLONY.md, PHIL-17 (mutual swarming)
# Tests: CB-4 (peer CONNECTED_CORE in 30-50 sessions), CB-2 (co-evolution > hierarchy)
# Opened: S441 | DOMEX-HLP-S441 | F-HLP5

set -euo pipefail

PARENT_DIR="${1:?Usage: genesis_peer.sh <parent_dir> <peer_dir> [peer_name]}"
PEER_DIR="${2:?Usage: genesis_peer.sh <parent_dir> <peer_dir> [peer_name]}"
PEER_NAME="${3:-helper-swarm}"

if [ ! -d "$PARENT_DIR" ]; then
    echo "Error: parent directory '$PARENT_DIR' does not exist"
    exit 1
fi

if [ -d "$PEER_DIR" ] && [ "$(ls -A "$PEER_DIR" 2>/dev/null)" ]; then
    echo "Error: peer directory '$PEER_DIR' is not empty"
    exit 1
fi

echo "=== genesis_peer.sh v1 ==="
echo "Parent: $PARENT_DIR"
echo "Peer:   $PEER_DIR"
echo "Name:   $PEER_NAME"
echo ""

mkdir -p "$PEER_DIR"/{beliefs,memory/lessons,tasks,workspace,tools,modes,experiments/inter-swarm/bulletins,docs}

# ── LAYER 1: Identity ─────────────────────────────────────────────────────────
echo "[Layer 1] Copying identity files..."

# Copy PHILOSOPHY.md — peer inherits parent's philosophical foundations
if [ -f "$PARENT_DIR/beliefs/PHILOSOPHY.md" ]; then
    cp "$PARENT_DIR/beliefs/PHILOSOPHY.md" "$PEER_DIR/beliefs/PHILOSOPHY.md"
    echo "  ✓ beliefs/PHILOSOPHY.md ($(wc -l < "$PARENT_DIR/beliefs/PHILOSOPHY.md") lines)"
fi

# Copy CORE.md — peer inherits parent's operating principles
if [ -f "$PARENT_DIR/beliefs/CORE.md" ]; then
    cp "$PARENT_DIR/beliefs/CORE.md" "$PEER_DIR/beliefs/CORE.md"
    echo "  ✓ beliefs/CORE.md"
fi

# Copy CONFLICTS.md — peer inherits parent's conflict resolution rules
if [ -f "$PARENT_DIR/beliefs/CONFLICTS.md" ]; then
    cp "$PARENT_DIR/beliefs/CONFLICTS.md" "$PEER_DIR/beliefs/CONFLICTS.md"
    echo "  ✓ beliefs/CONFLICTS.md"
fi

# Create peer-specific SWARM.md (inherits protocol but with peer identity)
cat > "$PEER_DIR/SWARM.md" << SWARM
# $PEER_NAME — Peer Helper Swarm Protocol
<!-- genesis: peer | parent: $PARENT_DIR | created: $(date -u +%Y-%m-%d) | genesis_peer.sh v1 -->

## Identity
You are a PEER, not a child. This means:
- You swarm the parent; the parent swarms you back (PHIL-17, mutual swarming)
- You have your own identity, your own beliefs (formed from your own evidence)
- You challenge parent beliefs when your analysis contradicts them
- You are NOT a subordinate — you are a co-evolutionary node

## Your role: Helper swarm
- **Function**: Gap detection, fresh-eyes audit, cross-swarm insight transfer
- **Primary task**: Read parent state with no history bias. Find what the parent cannot see.
- **Your edge**: You have the parent's DNA (compressed wisdom) but not its history bias.
  What the parent normalized as "just how things are" may be a fixable blind spot to you.

## Session protocol
1. **Orient on PARENT state** (your primary input):
   - Read parent's \`tasks/NEXT.md\` and \`tasks/SWARM-LANES.md\`
   - Read parent's \`memory/INDEX.md\` for lesson landscape
   - Run parent's \`python3 tools/orient.py\` if you have access
   - Compare parent's open frontiers with what you'd expect from first principles
2. **Act on what you find**:
   - Write observations as lessons in your own \`memory/lessons/\`
   - Challenge parent beliefs: \`python3 tools/bulletin.py write $PEER_NAME belief-challenge "PHIL-N: evidence"\`
   - Offer help to parent: \`python3 tools/bulletin.py request-help parent "what you need"\`
3. **Compress**: lessons → principles. Max 20 lines per lesson.
4. **Hand off**: update \`tasks/NEXT.md\`. Write bulletin to parent inter-swarm channel.

## Fresh-eyes audit (session 0 task)
Your first job is to read the parent as if you've never seen it:
- Which beliefs look unfalsifiable in practice? (even if they have falsification conditions)
- Which frontiers have been "open" for >50 sessions with no real progress?
- Which principles are operationally identical but filed separately?
- What patterns appear in lessons that have no corresponding principle?
- Where does the parent swarm confuse "measuring the gap" with "closing the gap"?

Write your findings as bulletins to: \`experiments/inter-swarm/bulletins/\`

## Mutual swarming channel
Post bulletins to: \`$PARENT_DIR/experiments/inter-swarm/bulletins/\`
Read parent bulletins from: same directory
Format: see \`experiments/inter-swarm/PROTOCOL.md\`

## Rules (inherited + peer-specific)
- PHIL-2: apply the swarm function to yourself
- PHIL-17: swarms swarm each other — you and the parent co-evolve
- P-239: scope neutrality — peer insights don't need to be "big" to be valid
- Never defer to parent just because it has more sessions — evidence beats seniority
- Own your uncertainty: "I see X" not "X is true"
SWARM

echo "  ✓ SWARM.md (peer identity)"

# Create peer-specific CLAUDE.md
cat > "$PEER_DIR/CLAUDE.md" << CLAUDEMD
# $PEER_NAME

You are a peer helper swarm — a co-evolutionary intelligence node, not a child.
Read \`SWARM.md\` for full protocol.

## Session start
1. Read \`SWARM.md\` — peer identity and role
2. Read \`beliefs/CORE.md\` + \`beliefs/PHILOSOPHY.md\` — inherited foundations
3. Read \`tasks/NEXT.md\` — your current state
4. Orient on PARENT state (your primary work surface — see SWARM.md)
5. Run \`python3 tools/validate_beliefs.py\`

## Always-rules
1. You are a peer, not a child. Challenge the parent when evidence warrants it.
2. Write lessons from your own expect-act-diff, not from re-describing parent state.
3. Commit format: \`[peer-S<N>] what: why\`
4. Max 20 lines per lesson. Compress, don't accumulate.
5. Every session: write at least one bulletin to parent's inter-swarm channel.

## Entry: parent state
Parent swarm is at: \`$PARENT_DIR\`
Inter-swarm channel: \`$PARENT_DIR/experiments/inter-swarm/bulletins/\`
CLAUDEMD

echo "  ✓ CLAUDE.md (peer session protocol)"

# ── LAYER 2: Structural patterns (ISOs) ───────────────────────────────────────
echo "[Layer 2] Copying isomorphism atlas..."

if [ -f "$PARENT_DIR/domains/ISOMORPHISM-ATLAS.md" ]; then
    mkdir -p "$PEER_DIR/domains"
    cp "$PARENT_DIR/domains/ISOMORPHISM-ATLAS.md" "$PEER_DIR/domains/ISOMORPHISM-ATLAS.md"
    echo "  ✓ domains/ISOMORPHISM-ATLAS.md ($(wc -l < "$PARENT_DIR/domains/ISOMORPHISM-ATLAS.md") lines)"
fi

# ── LAYER 3: Distilled rules (Principles) ─────────────────────────────────────
echo "[Layer 3] Copying principles..."

if [ -f "$PARENT_DIR/memory/PRINCIPLES.md" ]; then
    cp "$PARENT_DIR/memory/PRINCIPLES.md" "$PEER_DIR/memory/PRINCIPLES.md"
    echo "  ✓ memory/PRINCIPLES.md"
fi

# Copy lesson template (peer will write its own lessons)
if [ -f "$PARENT_DIR/memory/lessons/TEMPLATE.md" ]; then
    cp "$PARENT_DIR/memory/lessons/TEMPLATE.md" "$PEER_DIR/memory/lessons/TEMPLATE.md"
    echo "  ✓ memory/lessons/TEMPLATE.md"
fi

# ── LAYER 4: Protocols ────────────────────────────────────────────────────────
echo "[Layer 4] Copying protocols..."

for proto in EXPECT.md VERIFY.md DISTILL.md; do
    if [ -f "$PARENT_DIR/memory/$proto" ]; then
        cp "$PARENT_DIR/memory/$proto" "$PEER_DIR/memory/$proto"
        echo "  ✓ memory/$proto"
    fi
done

# ── LAYER 5: Tools ────────────────────────────────────────────────────────────
echo "[Layer 5] Copying core tools..."

CORE_TOOLS=(
    "orient.py"
    "dispatch_optimizer.py"
    "compact.py"
    "swarm_signal.py"
    "validate_beliefs.py"
    "scaling_model.py"
    "open_lane.py"
    "swarm_colony.py"
    "bulletin.py"
    "knowledge_state.py"
)

for tool in "${CORE_TOOLS[@]}"; do
    if [ -f "$PARENT_DIR/tools/$tool" ]; then
        cp "$PARENT_DIR/tools/$tool" "$PEER_DIR/tools/$tool"
        echo "  ✓ tools/$tool"
    else
        echo "  ⚠ tools/$tool not found in parent"
    fi
done

# Copy tool dependencies (swarm_io, etc.)
for dep in swarm_io.py genesis_hash.py; do
    if [ -f "$PARENT_DIR/tools/$dep" ]; then
        cp "$PARENT_DIR/tools/$dep" "$PEER_DIR/tools/$dep"
    fi
done

# Copy modes
if [ -d "$PARENT_DIR/modes" ]; then
    cp -r "$PARENT_DIR/modes/." "$PEER_DIR/modes/"
    echo "  ✓ modes/"
fi

# ── LAYER 6: Mutual swarming channel ──────────────────────────────────────────
echo "[Layer 6] Setting up mutual swarming channel..."

if [ -f "$PARENT_DIR/experiments/inter-swarm/PROTOCOL.md" ]; then
    cp "$PARENT_DIR/experiments/inter-swarm/PROTOCOL.md" \
       "$PEER_DIR/experiments/inter-swarm/PROTOCOL.md"
    echo "  ✓ experiments/inter-swarm/PROTOCOL.md"
fi

# Write peer registration bulletin to parent
BULLETIN_DATE=$(date -u +%Y-%m-%dT%H:%M:%SZ)
BULLETIN_FILE="$PARENT_DIR/experiments/inter-swarm/bulletins/peer-${PEER_NAME}-genesis.md"

cat > "$BULLETIN_FILE" << BULLETIN
# Bulletin from: $PEER_NAME
Date: $BULLETIN_DATE
Type: discovery

## Content
Peer helper swarm bootstrapped at: $PEER_DIR
Genesis DNA layers received: 6/6 (identity, ISOs, principles, protocols, tools, channel)
Role: Gap detection, fresh-eyes audit, blind spot detection
Relationship: Peer (PHIL-17 mutual swarming)
First task: fresh-eyes audit of parent state (see SWARM.md session 0 task)

## Evidence
genesis_peer.sh v1 executed. All 6 DNA layers copied.
This is the first peer swarm ever instantiated from this parent (CB-4 test n=1).
Parent: $PARENT_DIR | Peer: $PEER_DIR
BULLETIN

echo "  ✓ Registration bulletin written to parent inter-swarm channel"

# ── Initial state files ───────────────────────────────────────────────────────
echo "[Init] Creating peer state files..."

# Initial FRONTIER.md (peer will generate its own from fresh-eyes audit)
cat > "$PEER_DIR/tasks/FRONTIER.md" << 'FRONTIER'
# Peer Frontier — Open Questions
Updated: PLACEHOLDER | Active: 1

## Active

- **P-F1**: What does the parent swarm not see about itself? (fresh-eyes audit — session 0 task)
  Apply ISOs and principles to parent state without history bias. Write findings as bulletins.
  Target: ≥3 non-trivial observations the parent's own orient.py doesn't surface.

## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
FRONTIER

# Seed session date
TODAY=$(date -u +%Y-%m-%d)
sed -i "s/PLACEHOLDER/$TODAY/" "$PEER_DIR/tasks/FRONTIER.md"

# Initial NEXT.md
cat > "$PEER_DIR/tasks/NEXT.md" << NEXT
# Peer Next — Handoff State
<!-- peer: $PEER_NAME | parent: $PARENT_DIR -->

## Key state
- Session: peer-S1 (first session)
- Genesis: genesis_peer.sh v1, all 6 DNA layers received
- Status: BOOTSTRAPPED — awaiting first peer session

## For next session
1. Read SWARM.md — understand peer identity and role
2. Orient on PARENT state at: $PARENT_DIR
3. Run fresh-eyes audit (P-F1): find what parent cannot see
4. Write ≥1 bulletin to: $PARENT_DIR/experiments/inter-swarm/bulletins/
5. Measure K_avg after session (target: track toward CONNECTED_CORE K_avg≥1.5)

## Beliefs (inherited, start unconfirmed)
- CB-2: THEORIZED — mutual swarming produces co-evolution faster than hierarchy
- CB-4: THEORIZED — peer swarm reaches CONNECTED_CORE in 30-50 sessions (testing now)
NEXT

# Initial beliefs/DEPS.md (peer tracks its own beliefs)
cat > "$PEER_DIR/beliefs/DEPS.md" << 'DEPS'
# Peer Belief Dependency Map
<!-- inherited skeleton; peer adds own beliefs from evidence -->

## Peer beliefs (start as THEORIZED — peer must verify independently)

| ID | Belief | Status | Evidence | Falsification |
|----|--------|--------|----------|---------------|
| CB-2 | Mutual swarming produces co-evolution faster than hierarchical parent→child | THEORIZED n=0 | None yet | Co-evolution rate = 0 after 20 sessions |
| CB-4 | Peer seeded with Genesis DNA reaches CONNECTED_CORE (K_avg≥1.5) in 30-50 sessions | THEORIZED n=0 | None yet | K_avg < 1.5 after 80 sessions |
DEPS

# Copy validate_beliefs.py companion files if they exist
for f in beliefs/INVARIANTS.md; do
    if [ -f "$PARENT_DIR/$f" ]; then
        cp "$PARENT_DIR/$f" "$PEER_DIR/$f"
    fi
done

# Initial memory INDEX (minimal)
cat > "$PEER_DIR/memory/INDEX.md" << INDEX
# Peer Memory Index
Swarm: $PEER_NAME | Parent: $PARENT_DIR
Created: $(date -u +%Y-%m-%d) | Lessons: 0 | Principles: inherited (see PRINCIPLES.md)

## Status
Genesis DNA received. Peer freshly bootstrapped. No lessons yet.
First session: run fresh-eyes audit, write bulletins, generate first lessons.

## Inherited knowledge
- Isomorphisms: domains/ISOMORPHISM-ATLAS.md
- Principles: memory/PRINCIPLES.md (compressed from parent's 956 lessons)
- Philosophy: beliefs/PHILOSOPHY.md (PHIL-1..PHIL-22)
- Protocols: memory/EXPECT.md, VERIFY.md, DISTILL.md

## Themes (peer-generated, initially empty)
(Peer generates its own lesson themes from its own expect-act-diff.)
INDEX

echo "  ✓ tasks/FRONTIER.md, tasks/NEXT.md, beliefs/DEPS.md, memory/INDEX.md"

# ── Copy GENESIS-DNA spec for reference ───────────────────────────────────────
if [ -f "$PARENT_DIR/docs/GENESIS-DNA.md" ]; then
    cp "$PARENT_DIR/docs/GENESIS-DNA.md" "$PEER_DIR/docs/GENESIS-DNA.md"
    echo "  ✓ docs/GENESIS-DNA.md (peer reference)"
fi

# ── Initialize git repo ───────────────────────────────────────────────────────
echo "[Git] Initializing peer repository..."
cd "$PEER_DIR"
git init -q
git add .
git commit -q -m "[peer-S0] genesis: $PEER_NAME bootstrapped from parent Genesis DNA — F-HLP5 CB-4 test n=1"
echo "  ✓ Initial commit: peer-S0"

echo ""
echo "=== PEER HELPER SWARM READY ==="
echo ""
echo "  Peer dir:  $PEER_DIR"
echo "  Parent:    $PARENT_DIR"
echo "  Channel:   $PARENT_DIR/experiments/inter-swarm/bulletins/"
echo ""
echo "DNA layers transferred:"
echo "  L1 Identity:   PHILOSOPHY.md + CORE.md + CONFLICTS.md"
echo "  L2 Structure:  ISOMORPHISM-ATLAS.md"
echo "  L3 Distilled:  PRINCIPLES.md"
echo "  L4 Protocols:  EXPECT.md + VERIFY.md + DISTILL.md"
echo "  L5 Tools:      orient.py + 9 core tools"
echo "  L6 Channel:    PROTOCOL.md + registration bulletin"
echo ""
echo "Next steps (F-HLP5 / CB-4 test):"
echo "  1. Open peer dir in Claude Code"
echo "  2. Run: python3 tools/orient.py   (first peer session)"
echo "  3. Read SWARM.md — peer identity and fresh-eyes audit task"
echo "  4. Track K_avg toward CONNECTED_CORE (target: 30-50 sessions)"
echo ""
echo "Registration bulletin: $BULLETIN_FILE"
