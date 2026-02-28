# Quality Domain Index
Updated: 2026-02-28 | Sessions: 190

## What this domain knows
- **Core purpose**: audit the swarm's own knowledge corpus for redundancy, staleness, and cross-domain overlap
- **Active frontiers**: 3 in `domains/quality/tasks/FRONTIER.md` (F-QC2, F-QC3, F-QC4)
- **F-QC1 RESOLVED S189**: 15.3% duplication rate confirmed (35 pairs / 288 lessons). Quality gate added to Work phase. See `experiments/quality/f-qc1-repeated-knowledge-s189.json`.
- **F-QC4 OPEN**: Auto-assign theme labels to new lessons at write-time to prevent corpus indexing lag (L-308: 192/288 lessons = 67% unthemed). Hypothesis: `lesson_tagger.py` reduces unthemed fraction below 20% in 5 sessions.

## Lesson themes

| Theme | Example lessons | Core insight |
|-------|-----------------|--------------|
| Near-duplicate detection | (pending F-QC1) | Jaccard similarity on word sets detects structurally redundant lessons |
| Knowledge freshness | (pending F-QC2) | Citation gap is a proxy for lesson staleness |
| Cross-domain redundancy | (pending F-QC3) | High-isomorphism domain pairs produce lesson duplicates in different vocabulary |

## Structural isomorphisms with swarm design

| Quality finding | Swarm implication | Status |
|----------------|-------------------|--------|
| Near-duplicate rate baseline | Informs compaction aggressiveness and MDL threshold | THEORIZED (B-QC1) |
| Citation decay proxy | Staleness-weighted compaction: prioritize zero-cited AND old lessons | THEORIZED (B-QC2) |
| Cross-domain overlap | ISOMORPHISM-ATLAS entries should absorb cross-domain duplicates | THEORIZED (B-QC3) |

## What's open
- **F-QC2**: Do frequently-cited lessons exhibit lower accuracy over time as swarm belief evolves?
- **F-QC3**: Which domain pairs have the highest cross-domain lesson redundancy?
- **F-QC4**: Can auto-theme-labeling at write-time reduce the unthemed fraction (currently 67%) below 20%?

## Resolved
- **F-QC1** (S189): 15.3% near-duplicate rate (35 pairs / 288 lessons, Jaccard>0.4). Quality gate placed in Work phase. L-309.

## Quality domain links to current principles
P-163 (proxy-K sawtooth — quality degrades when lesson count inflates without compression) | P-181 (expect-act-diff — quality domain applies the same calibration loop to lesson claims) | P-197 (high-yield session cluster — quality domain identifies what makes a lesson high-yield)
