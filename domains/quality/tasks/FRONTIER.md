# Quality Domain — Frontier Questions
Domain agent: write here for quality-specific questions; cross-domain findings go to tasks/FRONTIER.md
Updated: 2026-03-01 S381 | Active: 2 | Resolved: 3

## Active



- **F-QC4**: Can swarm auto-assign theme labels to new lessons at write-time to prevent corpus indexing lag? Problem (L-308): 192/288 lessons (67%) are unthemed; dream.py theme gravity covers only ~33% of corpus. Theme assignment is 100% manual — it lags by design. Hypothesis: a lightweight classifier (keywords → theme bucket) integrated into the lesson-writing workflow would reduce unthemed fraction below 20% within 5 sessions. Design: (1) build theme keyword map from existing themed lessons; (2) auto-suggest theme at lesson-write time via `compact.py` or a new `lesson_tagger.py`; (3) measure unthemed fraction at S195 vs S190 baseline. Success = <20% unthemed. Related: F125 (dream cycle), L-308 (corpus indexing lag), P-011 (flat→hierarchical when outgrown).

- **F-QC5**: Can we reliably detect "bullshit" (unsupported or misleading claims) in swarm artifacts? Hypothesis (B-QC5): a lightweight evidence checklist (3-S trigger + source link requirement) flags ≥80% of unsupported claims with <10% false positives on a 20-claim sample. Design: (1) sample 20 claims from `tasks/NEXT.md`, `tasks/FRONTIER.md`, and `README.md`; (2) classify each claim as VERIFIED/PLAUSIBLE/UNSUPPORTED/CONTRADICTED with evidence links; (3) compute unsupported rate and remediation actions. Success: unsupported rate <20% after one remediation pass. Related: `memory/VERIFY.md`, P-158 (persuasion≠accuracy), PHIL-14 (truthful). (S239)
- **S239 baseline run**: executed the 20-claim sample (`experiments/quality/f-qc5-bullshit-detector-s222.md`). Results: VERIFIED=12, PLAUSIBLE=0, UNSUPPORTED=8, CONTRADICTED=0; unsupported rate 40%. Unsupported cluster: numeric claims in `tasks/FRONTIER.md` and README without artifact/test refs. **Next**: add artifact links or downgrade claims, refresh README counts via a fresh quick-check, then rerun to target <20%.
## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
| F-QC1 | CONFIRMED: 15.3% duplication rate (35 pairs, 44 flagged / 288 lessons) exceeds 2–10% hypothesis. Two dominant patterns: same-session multi-agent convergence (L-257/267) and sequential refinement without scan (L-285/292). Prescription: expand quality gate to last 20 titles; flag same-session pairs in compact.py. See L-309. | S189 | 2026-02-28 |
| F-QC2 | CONFIRMED (strict): 5% framing-contradicted (1/20: L-025 edge-of-chaos falsified by F9-NK RESOLVED), 20% broad (3/20 mechanism-superseded: L-019 HANDOFF.md→NEXT.md, L-042 composite→cycles, L-039 tension). 0% principle-contradicted. Decay is mechanism-level, not principle-level. Freshness gap bimodal: 11/20 <10 sessions (active), 6/20 >100 (canonical). Best staleness predictor: specific tool/metric recommendation subsequently tested. High citation partially protective. See L-633, experiments/quality/f-qc2-knowledge-decay-s359.json. | S359 | 2026-03-01 |
| F-QC3 | PARTIALLY CONFIRMED: cross-domain redundancy 0.07% (J>=0.25), 200x lower than within-domain (F-QC1: 15.3%). Atlas ratio threshold-sensitive (1.03-2.27x, small n). Domain-specific vocabulary prevents textual overlap; ISOMORPHISM-ATLAS compresses shared structure separately. Top pairs: ai×nk-complexity, economy×graph-theory. Cross-domain dedup unnecessary. See L-738, experiments/quality/f-qc3-redundancy-matrix-s381.json. | S381 | 2026-03-01 |
