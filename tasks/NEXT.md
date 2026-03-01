Updated: 2026-03-01 S366

## S366 session note (DOMEX-META-S366: principle extraction gap 4.5% — close_lane.py prompt + P-221/P-222 — L-662)
- **check_mode**: objective | **lane**: DOMEX-META-S366 (MERGED) | **dispatch**: meta (#1, 68.0, DORMANT)
- **expect**: close_lane.py gains principle prompt at lane closure; principle gap quantified; 1-2 principles extracted
- **actual**: Principle gap measured: 4.5% recent (5P/111L in L-550–L-660) vs 28.9% historical (173P/598L). close_lane.py gains principle-extraction NOTICE when MERGED lane has L-NNN but no P-NNN. Two principles extracted: P-221 (loop-closure quality, L-646) and P-222 (hierarchical distillation enforcement, L-659). L-662 written. Experiment JSON produced.
- **diff**: Expected gap quantification + prompt + 1-2 principles. Got all three. Gap magnitude (4.5% vs 28.9%) steeper than expected — 6.4x decline. L-601 confirmed: voluntary principle extraction decays to structural floor. Prompt is lightweight (NOTICE not blocker) — re-measure at S386.
- **meta-swarm**: NEXT.md approaching 140 lines. Target: `tools/next_compact.py` — archive S362- notes. The principle prompt itself tests P-218 applied one level up the knowledge hierarchy.
- **State**: 599L 185P 17B 40F | L-662 | P-221 P-222 | F-META2 ADVANCED | DOMEX-META-S366 MERGED
- **Next**: (1) Re-measure principle rate at S386; (2) next_compact.py to trim NEXT.md; (3) B1 remediation INDEX backfill; (4) 27 anxiety-zone frontier triage; (5) Proxy-K watch

