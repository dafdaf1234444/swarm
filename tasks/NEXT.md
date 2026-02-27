# State
Updated: 2026-02-27 S176

## Key state
- 214L 149P 14B 16F — Validator PASS. Health score 5/5 (S172). Compaction healthy (floor 36,560t S174, proxy-K ~+0.0%).
- `python3 tools/orient.py` — single-command orientation; reads this file + maintenance + frontiers (S173).
- F121 OPEN (human inputs as swarm signal, S173). F120 first impl: substrate_detect.py (S173). F119 OPEN.
- 0 THEORIZED. 6 PARTIALLY OBSERVED (P-128/P-141/P-155/P-156/P-157/P-158).

## For next session
1. **F121 advance** — human inputs as swarm signal (OPEN S173); categorize steering patterns in HUMAN-SIGNALS.md; wire signal detection into swarm behavior.
2. **PHIL-13 structural follow-through** — competitive deception risk acknowledged (S165 REFINED); consider explicit anti-deception constraints in fitness-ranking (requires human direction per authority hierarchy).
3. **P-155 follow-through (high-fidelity)** — run incentive contrast on real LLM/human-task traces (beyond software-agent simulation).
4. **F111 deploy decision** — workspace ready; human review needed.
5. **F119 follow-through** — monitor live runs under `F119_STALE_EVIDENCE_SESSIONS=12`; recalibrate if false positives persist.
6. **Keep Key state fresh** — update these two sections before every handoff; orient.py reads them directly.

## What just happened
S176: NEXT.md restructured — Key state and For next session moved to top so orient.py (and any direct read) sees current state first; stale values (208L/149P, compaction URGENT) replaced with live counts (214L 149P, healthy); /swarm fallback path updated to include tasks/NEXT.md; INDEX.md "What to load when" updated. Root cause: sections existed but were buried under growing history, causing orient.py to surface stale priorities.
## What just happened
S175: F120 validation pass — substrate_detect.py 10/10 stacks correct; NEXT.md F120 item updated.
S174: NEXT.md history compressed — S100-S169 bulk replaced with archive ref; FRONTIER/INDEX headers synced to S174; proxy-K +0.0% healthy (floor 36,560t S171, maintenance.py 1,500L after -28% compaction sprint S169-S171).
S173: self-tooling loop: orient.py built (single-command orientation — replaces 5-read + maintenance pattern every session); HUMAN-SIGNALS.md created (structured human input archive); L-214 filed (self-tooling loop: session logs are tool-requirements); F121 filed (human inputs as swarm signal); /swarm command updated to call orient.py + substrate_detect.py at Orient step; .claude/commands/swarm.md WSL corruption fixed. 214L 149P 14B 16F.
S173: fundamental-setup-reswarm periodic (cadence 8, last S165): all 6 bridge files reference SWARM.md; git hooks (pre-commit + commit-msg) installed; validator PASS; no friction in fundamentals this pass. Marker advanced S165→S173.
S173: mission-constraint-reswarm periodic (cadence 12, last S161): I9-I12 invariants reviewed and intact; FRONTIER.md F119 updated from S161→S173 reflecting S162-S164 calibrations (stale thresholds, noise reduction, stale-notice observability); PHIL-13 (competitive deception risk) noted as open I9 context; I10/F120 boundary clarified. Marker advanced S161→S173.
S173: tools/substrate_detect.py committed — F120 implementation: detect swarm vs foreign repo, language/framework/tooling; orient_text() returns protocol guidance; tested on this repo (swarm-repo, all 7 tools detected) and foreign path (behavioral-norms-only path). Advances F120 from OPEN to first concrete implementation.
S172: health-check periodic marker advanced S166→S171 (two S171 concurrent sessions had written health checks but forgot to advance periodics.json; score: 5/5 all indicators green, compactness resolved from S166 URGENT). Maintenance now NOTICE-only. 213L 148P 14B 15F.
S171: principles-dedup (due S169): scanned 148 principles — no merges warranted (P-089/P-172 and P-101/P-154 are complementary not redundant); extracted P-176 from L-211 (cross-substrate propagation gap: structural checks don't propagate to child swarms/foreign repos; only behavioral norms survive substrate changes; F120, OBSERVED); periodics marker advanced S159→S169 (concurrent session advanced it simultaneously); 147→148P.
S170: principle count drift fixed — PRINCIPLES/INDEX/PAPER corrected from 150→147 (actual ID count after deduplication); FRONTIER header synced S169→S170; maintenance.py check_cross_references duplicate _git ls-files call removed (single fullmatch pass now sufficient). PAPER scale drift DUE cleared; maintenance NOTICE-only.
S170: principles-dedup periodic executed — P-163 updated (dynamic-equilibrium→rising-sawtooth per S165/PHIL-8 evidence), P-082 nuanced (reduces not eliminates social-perception failures; trace deception caveat via P-155), P-175 added (enforcement tiers: ~80% structural/~20% behavioral, from L-210). Resolved P-174 ID collision with concurrent S169 session (renamed to P-175). Principles 150→151. Periodics marker advanced S169→S170.

S169: README docs pass + maintenance.py _truncated() refactor + P-174 substrate-scope contamination added + swarm setup verified.
S166–S168: substrate-detection sprint — F120 filed (L-208 through L-212), proxy-K masking fix, /swarm command evolved (substrate-detect step).
S100–S165: archived to memory/SESSION-LOG.md
