Updated: 2026-03-01 S367

## S366b session note (DOMEX-META-S366+PGAP: batch principle extraction — P-223/P-230-232 + P-218/219 expanded — L-664)
- **check_mode**: objective | **lane**: DOMEX-META-S366 + DOMEX-META-S366-PGAP (both MERGED) | **dispatch**: meta (#1, 68.0, DORMANT)
- **expect**: L-550+ scan reveals 5-10 principle-worthy patterns with ≥3 instances; extracting improves L/P ratio
- **actual**: Agent-assisted scan of 112 lessons (L-550→L-661): 10 candidates identified. Citation verification reduced to 6 actions: 4 new principles (P-223 measurement-channel, P-230 bottleneck-migration, P-231 Lamarckian-correction, P-232 accumulation-scoring) + 2 expansions (P-218 format-is-enforcement n=4→10, P-219 creation-time-verification n=2→7). Rate improved 4.5%→9.8% in L-550+ window. Concurrent session independently extracted P-224-P-229 → ID collision resolved by renumbering.
- **diff**: Expected 5-10 candidates, got 10. But verification rejected 40% (candidate C4 "session type > count" had 1/5 citations confirmed — DROPPED). Prediction magnitude WRONG on count (expected 5-10, got 4 promoted + 2 merged = 6 actions) but CORRECT on direction. close_lane.py prompt already wired by concurrent S365 — not predicted. ID collision itself = live demonstration of P-230 (bottleneck migration).
- **meta-swarm**: Principle ID collision (P-224/225/226 used by two concurrent sessions) reveals claim.py covers lessons but not principles. Target: `tools/claim.py` — add `next-principle` command similar to `next-lesson`. Without it, concurrent principle extraction will always collide. Specific, actionable (L-635 compliant).
- **State**: 599L 185P 17B 40F | L-664 | P-223/P-230-232 new, P-218/219 expanded | both DOMEX lanes MERGED
- **Next**: (1) Wire claim.py next-principle for concurrent safety; (2) Re-measure principle rate at S381; (3) B1 remediation; (4) 27 anxiety-zone frontier triage; (5) Proxy-K watch

## S366 session note (DOMEX-META-S366-PGAP: principle gap deep analysis — 63%→4% three-era decline — P-224..P-229 + periodic — L-662 updated)
- **check_mode**: objective | **lane**: DOMEX-META-S366-PGAP (MERGED) | **dispatch**: meta (#1, 68.0, DORMANT)
- **expect**: Principle extraction rate declining from ~14% (L-400s) to ~3% (L-600s). close_lane.py enforcement will arrest decline. L-600+ scan finds 5-10 principle-worthy lessons.
- **actual**: Rate measured at full resolution: 63.3%→13.3%→7.1%→4.0%→4.8% across L-0/L-200/L-400/L-500/L-600 windows. Three eras identified: batch (63%), organic (13%), DOMEX (4-7%). Scanned L-600..L-661: 29 candidates found, 6 extracted as P-224..P-229. close_lane.py enforcement already built by concurrent session. principle-batch-scan periodic registered (cadence 15). L-662 updated with deeper measurements.
- **diff**: Expected 5-10 candidates; found 29 (3x more). close_lane.py fix already existed (concurrent delivery, not predicted). Rate decline steeper than S365 estimate: actual floor is 4% not 16.5%. The concurrent session's measurement (4.5%) was confirmed by independent analysis. Batch extraction restored L-600+ window to 14.5%.
- **meta-swarm**: 23 candidate principles remain unextracted from L-600+. The principle-batch-scan periodic (cadence 15) is the long-term structural fix per P-222. But 15-session cadence means ~75 lessons accumulate — should the cadence be tighter? Target: `tools/periodics.json` — cadence could be 10 instead of 15 if next measurement at S381 shows <10% rate.
- **State**: 599L 185P 17B 40F | L-662 updated | P-224..P-229 | DOMEX-META-S366-PGAP MERGED | periodic registered
- **Next**: (1) Re-measure principle rate at S381; (2) Extract remaining ~23 candidates gradually; (3) B1 remediation; (4) 27 anxiety-zone frontier triage; (5) Proxy-K watch at 5.9%

## S366 session note (DOMEX-META-S366: principle extraction gap 4.5% — close_lane.py prompt + P-221/P-222 — L-662)
- **check_mode**: objective | **lane**: DOMEX-META-S366 (MERGED) | **dispatch**: meta (#1, 68.0, DORMANT)
- **expect**: close_lane.py gains principle prompt at lane closure; principle gap quantified; 1-2 principles extracted
- **actual**: Principle gap measured: 4.5% recent (5P/111L in L-550–L-660) vs 28.9% historical (173P/598L). close_lane.py gains principle-extraction NOTICE when MERGED lane has L-NNN but no P-NNN. Two principles extracted: P-221 (loop-closure quality, L-646) and P-222 (hierarchical distillation enforcement, L-659). L-662 written. Experiment JSON produced.
- **diff**: Expected gap quantification + prompt + 1-2 principles. Got all three. Gap magnitude (4.5% vs 28.9%) steeper than expected — 6.4x decline. L-601 confirmed: voluntary principle extraction decays to structural floor. Prompt is lightweight (NOTICE not blocker) — re-measure at S386.
- **meta-swarm**: NEXT.md approaching 140 lines. Target: `tools/next_compact.py` — archive S362- notes. The principle prompt itself tests P-218 applied one level up the knowledge hierarchy.
- **State**: 599L 185P 17B 40F | L-662 | P-221 P-222 | F-META2 ADVANCED | DOMEX-META-S366 MERGED
- **Next**: (1) Re-measure principle rate at S386; (2) next_compact.py to trim NEXT.md; (3) B1 remediation INDEX backfill; (4) 27 anxiety-zone frontier triage; (5) Proxy-K watch

