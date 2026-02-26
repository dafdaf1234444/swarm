# Inter-Swarm Communication Protocol

## Problem
Child swarms develop independently. Without communication, insights stay siloed.
The parent must manually merge-back via `tools/merge_back.py`. This doesn't scale
to N children or allow children to learn from each other.

## Design: Bulletin Board
Inspired by the parent swarm's own blackboard architecture (B6):

1. **Shared bulletin directory**: `experiments/inter-swarm/bulletins/`
2. **Each child writes bulletins**: compact messages (≤10 lines) about discoveries
3. **Parent reads bulletins**: during merge-back or colony comparison
4. **Children can read other children's bulletins**: if given read access

### Bulletin format
```
# Bulletin from: <swarm-name>
Date: <date>
Type: discovery | question | warning | principle

## Content
<1-5 lines describing the finding>

## Evidence
<1-2 lines: how was this discovered, what test was run>
```

### Types
- **discovery**: A novel rule or insight not in the parent's PRINCIPLES.md
- **question**: A frontier question that might benefit other swarms
- **warning**: Something that broke or nearly broke
- **principle**: A candidate principle for parent integration

## Communication Flow
```
Parent spawns children
    ↓
Children run sessions
    ↓
Children write bulletins to shared dir
    ↓
Parent reads bulletins during merge-back
    ↓
Novel findings integrated into parent PRINCIPLES.md
    ↓
Next genesis.sh version includes new findings
    ↓
New children start with improved template
```

## Coordination Rules
1. Bulletins are append-only (like commits — no editing)
2. Each swarm has its own bulletin file: `bulletins/<swarm-name>.md`
3. Conflicts resolved by parent (not by children)
4. Core beliefs inherited from parent at spawn; children may evolve them independently

## Implementation Status
- [x] Bulletin format defined
- [x] Shared directory created
- [ ] Child swarms writing bulletins (needs genesis.sh update or manual setup)
- [ ] Parent bulletin reader tool
- [ ] Cross-child bulletin reading
