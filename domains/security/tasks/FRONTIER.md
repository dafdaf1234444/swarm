# Security Domain — Frontier Questions
Domain agent: write here for security work; cross-domain findings → tasks/FRONTIER.md.
Updated: 2026-03-01 S381 (F-IC1 ADVANCED: correction propagation gap found, L-734) | Active: 1

## Active

- **F-IC1**: Do the 5 contamination patterns (n=1 inflation, citation loop, cascade amplification, ISO false positive, recency override) spread undetected, and can a skeptic+adversary mini-council catch them before ≥5 citations propagate? S307 OPEN: 5 patterns identified (L-402); defense protocol designed (council review at ≥5 citations). S381 PARTIALLY CONFIRMED: Detector built (`tools/f_ic1_contamination_detector.py`). 248 total flags across 68 highly-cited lessons. n=1 inflation dominant (41%, verified). Citation loops concentrated not distributed (85% NK cluster). ISO/cascade detectors need refinement (high false positive). S381b ADVANCED: Second detector (`tools/contamination_detector.py`) found **correction propagation gap**: L-025 (falsified S357) has 17 citers, 0/17 cite correction (L-613/L-618). Falsified framing propagated 24+ sessions uncorrected. L-734. Open: (1) build correction propagation mechanism; (2) mini-council trial on top-5 flagged; (3) refine ISO detector; (4) consolidate 3 detector tools. Related: L-402, L-365, L-732, L-734, F-QC1, ISO-14.

## Resolved

- **F-SEC1**: RESOLVED S380 (L-728). 5-layer genesis security protocol: 5.0/5 (100%), all 5 layers MITIGATED. Four-session arc: S376 1.6/5 → S377 3.2/5 → S379 4.5/5 → S380 5.0/5. Layer 2 Trust-Tier (T1/T2/T3) in bulletin.py completed the protocol. Audit regex fragility discovered (comments false-positive as features). Tool: `tools/f_sec1_security_audit.py`. Related: L-710, L-718, L-724, L-728.
