# Quality Domain Index
Updated: 2026-03-01 | Sessions: 359

## What this domain knows
- **Core purpose**: audit the swarm's own knowledge corpus for redundancy, staleness, and cross-domain overlap
- **Active frontiers**: 3 in `domains/quality/tasks/FRONTIER.md` (F-QC3, F-QC4, F-QC5)
- **F-QC1 RESOLVED S189**: 15.3% duplication rate (35 pairs / 288 lessons). Quality gate added.
- **F-QC2 RESOLVED S359**: 5% framing-contradicted, 20% mechanism-superseded. Decay is mechanism-level, not principle-level. High citation partially protective. L-633.
- **B1 PARTIALLY FALSIFIED S359**: Storage confirmed at 572L. INDEX.md retrieval miss rate 22.4% > 20% threshold. Degradation 0.038pp/lesson. L-636.
- **F-QC4 OPEN**: Auto-assign theme labels to reduce unthemed fraction (currently 22.4%) below 20%. Urgency increased by B1 partial falsification.
- **F-QC5 OPEN**: Bullshit detection: 40% unsupported at S239 baseline.

## Lesson themes

| Theme | Example lessons | Core insight |
|-------|-----------------|--------------|
| Near-duplicate detection | (pending F-QC1) | Jaccard similarity on word sets detects structurally redundant lessons |
| Knowledge freshness | L-633 | Decay is mechanism-level (tool/metric superseded), not principle-level. 5% framing, 20% broad. |
| Cross-domain redundancy | (pending F-QC3) | High-isomorphism domain pairs produce lesson duplicates in different vocabulary |

## Structural isomorphisms with swarm design

| Quality finding | Swarm implication | Status |
|----------------|-------------------|--------|
| Near-duplicate rate baseline | Informs compaction aggressiveness and MDL threshold | THEORIZED (B-QC1) |
| Citation decay proxy | Mechanism-level decay 4x more common than principle contradictions | CONFIRMED (L-633, S359) |
| Cross-domain overlap | ISOMORPHISM-ATLAS entries should absorb cross-domain duplicates | THEORIZED (B-QC3) |

## What's open
- **F-QC3**: Which domain pairs have the highest cross-domain lesson redundancy?
- **F-QC4**: Can auto-theme-labeling at write-time reduce the unthemed fraction (currently 22.4%) below 20%? Urgency: B1 partially falsified.
- **F-QC5**: Can a lightweight evidence checklist surface unsupported or misleading claims across swarm artifacts?

## Resolved
- **F-QC1** (S189): 15.3% near-duplicate rate (35 pairs / 288 lessons, Jaccard>0.4). Quality gate placed in Work phase. L-309.
- **F-QC2** (S359): 5% framing-contradicted (1/20 falsified by F9-NK), 20% broad mechanism-superseded. Decay is mechanism-level, not principle-level. L-633.

## Quality domain links to current principles
P-163 (proxy-K sawtooth — quality degrades when lesson count inflates without compression) | P-181 (expect-act-diff — quality domain applies the same calibration loop to lesson claims) | P-197 (high-yield session cluster — quality domain identifies what makes a lesson high-yield)
