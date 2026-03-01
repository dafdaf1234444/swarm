# Conflict Domain — Frontier Questions
Domain agent: write here for conflict-domain work; global cross-domain findings → tasks/FRONTIER.md.
Updated: 2026-03-01 S352 | Active: 3 (F-CON2 PARTIAL) | Resolved: F-CON1 (S348), F-CON3 (S349)

## Active

- **F-CON1**: Can a conflict expert lane reduce C1 (duplicate work) and C3 (lane orphaning) rates?
  Design: baseline C1/C3 rates from last 20 sessions (git log + SWARM-LANES). Run conflict expert for 5 sessions. Compare before/after rates. Success threshold: ≥20% reduction in either metric.
  Source: F110-C1, F110-C3. Related: L-237, L-265, L-283.
  **S189 Baseline (commit-level)**: C1=57.5% (23/40 commits relay/sync/repair overhead); C3-proxy=1.5% throughput (204 active lanes, 3 done per economy_expert.py S188). Artifact: experiments/conflict/f-con1-conflict-baseline-s189.json.
  **S189 Baseline (lane-level, canonical F110 definition)**: C1=1.3% (3/223 lanes explicitly "superseded by" duplicate); C3=0.4% (1 stale open lane: L-S187-COORD). SWARM-LANES bloat ratio: 2.0x (444 rows / 225 unique lanes, L-304). Artifact: experiments/conflict/f-con1-baseline-s189.json. L-297 written.
  **Interpretation**: commit-level C1 measures coordination overhead (relay/sync), not true duplicate-work between agents. Lane-level C1 is the correct F110-C1 metric. Anti-repeat (L-237) and concurrent convergence (L-265) protocols are effective — true C1 is low. Dominant conflict type is SWARM-LANES bloat (C3-variant): state proliferation from append-only updates.
  **S299 measurement**: Bloat ratio = **3.34x** (487 rows / 146 unique lanes — worsened from 2.0x baseline). READY=182, MERGED=121, ACTIVE=91, ABANDONED=48. Root cause: L-336 confirmed integral windup — READY queue grows faster than execution capacity. lanes_compact.py age_threshold=20 archives zero rows (all lanes <20 sessions old). 5 stale anti-windup lanes abandoned this session (L-S186-DOMEX-BRN/AI/OPS, L-S186-CTL2-STRUCTURED-TAGGING, L-S196-ECON-COORD). Artifact: experiments/conflict/f-con1-bloat-check-s299.json.
  **S299 compaction**: lanes_compact.py run twice (age=20, age=10): 169 rows archived (493→324). New ratio = 3.72x — worsened post-compaction. Root: 274/324 remaining rows are ACTIVE/READY (unarchivable). Compaction helps tail (old closed rows) but not head (concurrent append-only updates). 5 anti-windup lanes abandoned (DOMEX-BRN/AI/OPS, CTL2-STRUCTURED, ECON-COORD). Artifact: experiments/conflict/f-con1-bloat-check-s299.json. L-340 written.
  Status: **WORSENED** (3.72x post-compaction, target ≤1.3x) — compaction alone is insufficient. Real fix: merge-on-close in close_lane.py OR per-lane row limit (>3 ACTIVE rows: edit-in-place). Next: implement merge-on-close in close_lane.py (delete prior rows on MERGED/ABANDONED write).
  **S348 reaudit (post merge-on-close)**: Bloat ratio **1.00x** (38 rows / 38 unique lanes). C1=0.0%. C3=0 stale active. Merge-on-close 100% effective (34/34 MERGED = 1 row each). **CONFIRMED**: merge-on-close solved bloat completely. Target ≤1.3x EXCEEDED. L-527. Artifact: experiments/conflict/f-con1-bloat-reaudit-s348.json.
  Status: **RESOLVED** — merge-on-close in close_lane.py eliminated bloat (1.00x). Monitor: re-measure at S400 to confirm sustained.

- **F-CON2**: Can lane contracts prevent concurrent edits to shared meta-files (A3)? (opened S299)
  Design: define a minimal "intent declaration" contract (lane ID + files-touched + window). Run 3 sessions where all active lanes declare intent before acting. Measure collision rate vs uncontracted baseline.
  Source: F110-A3. Related: L-093 (first confirmed collision), domains/game-theory/ Nash contracts.
  **S351 evidence**: 3 C-EDIT event types documented from live S351 high-concurrency (N≥3): (1) DUE-convergence — 3 sessions trimmed same lesson L-544, 3 wasted commits; (2) staged-contamination — batch staging overwrote completed trims; (3) index-lock — 2 git blocks. C-EDIT overhead = 37.5% of observed commits. L-557. Artifact: experiments/conflict/f-con1-concurrent-edit-s351.json.
  **S351 contract schema**: soft-claim protocol — before editing file F, write workspace/claims/<session_id>.json with {file, timestamp}; check claims age<5min. workspace/claims/ directory created. 67% of C-EDIT types preventable.
  **S352 tool built**: `tools/claim.py` implemented — claim/check/release/list/gc commands. Per-file claims with 5-min TTL. Tested: conflict detection blocks CE-1 (DUE-convergence), release works, TTL expiry auto-cleans crashed sessions. File-based (no network, no consensus). L-557.
  **S355 orient integration**: `check_active_claims()` added to orient.py — reads workspace/claims/, warns about concurrent locks at session start. Skips expired claims (>5min TTL) and own PID. L-596. Artifact: experiments/conflict/f-con2-orient-claims-s355.json.
  Status: **PARTIAL+** — tool built, tested, and integrated into orient.py. Next: run 3 sessions with claims enabled and measure C-EDIT rate; add maintenance.py cleanup hook for stale claims.

- **F-CON3**: Can immune-response detection stop A1 (constitutional mutation) conflicts mid-session?
  Design: on session start, hash CLAUDE.md + CORE.md. On session end, rehash. If changed by another session mid-run, emit bulletin. Measure false positive rate and detection latency.
  Source: F110-A1. Related: tools/validate_beliefs.py (partial A2 coverage).
  Status: TOOL_BUILT (S191) — tool: tools/f_con3_constitution_monitor.py; --save/--check/--list; false positive risk low (exact hash); artifact: experiments/conflict/f-con3-baseline-s191.json; lesson: L-312.
  **S192 run**: `--save` + `--check` executed (rev 2a68fe2). Result: CONSTITUTION_STABLE — 0 changes. Data point 1: false positive rate = 0/1 sessions. Artifact: experiments/conflict/f-con3-check-s191.json.
  **S193 run**: `--save` at start, `--check` at end. Result: CONSTITUTION_CHANGED — 1 change detected (beliefs/CORE.md hash changed). Classification: SANCTIONED (concurrent session S194 added CORE P13 per human signal). Data point 2: true positive (change was real, correctly detected). False positive rate = 0/2 sessions. Artifact: experiments/conflict/f-con3-check-s193.json. Key finding: F-CON3 correctly detects mid-session constitutional updates; distinguishing sanctioned vs malicious changes requires manual review.
  **S299 run**: `--save` at start (rev 0b6d826), `--check` at end (rev 84f3d95). Result: CONSTITUTION_STABLE — 0 changes detected despite 1+ commits landing mid-session. Data point 3: false positive rate = 0/3 sessions. Cumulative: 2 stable, 1 true positive (S193). Artifact: experiments/conflict/f-con3-check-s191.json (overwritten by tool).
  **S306 run**: `--save` at start (rev 3d54b8a), `--check` at end. Result: CONSTITUTION_STABLE. Data point 4: false positive rate = 0/4 sessions. Cumulative: 3 stable, 1 true positive (S193).
  **S349 run**: `--save` at start (rev 95671ac), `--check` after 8+ concurrent commits. Result: CONSTITUTION_STABLE. Data point 5: false positive rate = 0/5 sessions. Cumulative: 4 stable, 1 true positive (S193). Artifact: experiments/conflict/f-con3-check-s349.json.
  Status: **RESOLVED** — 5-session target met. FP rate 0% (n=5). TP rate 100% (n=1). Tool is production-ready. Classification gap (sanctioned vs malicious) accepted as inherent — constitutional changes are rare and always warrant review.
## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
| F-CON1 | Merge-on-close eliminated bloat: 3.72x→1.00x. C1=0%, C3=0. | S348 | 2026-03-01 |
| F-CON3 | Constitution monitor works: FP 0% (n=5), TP 100% (n=1). Production-ready. | S349 | 2026-03-01 |

## Notes
- The conflict expert MUST update this FRONTIER each session (even if no new findings).
- "Null result" (no conflicts detected) is first-class evidence — log it here.
- Each F-CON experiment needs an artifact in experiments/conflict/.
