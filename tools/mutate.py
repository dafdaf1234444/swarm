#!/usr/bin/env python3
"""Mutation operator — the missing evolutionary mechanism (PHIL-19).

The swarm has selection (compact.py), reproduction (genesis_extract.py),
recombination (F-MERGE1) — but no formal mutation operator. Without mutation,
evolution stalls: selection can only trim, never create.

Mutation types:
  NEGATE      — flip claim polarity ("X is true" → "not-X")
  WEAKEN      — add boundary conditions ("X always" → "X when Y")
  STRENGTHEN  — remove qualifiers ("X sometimes" → "X always")
  INVERT      — reverse causation/direction ("A→B" → "B→A")
  COMBINE     — merge two claims
  SPECIALIZE  — narrow scope
  GENERALIZE  — broaden scope
  PARAMETER   — perturb a numeric constant

Target priority = dogma_score × (1 + is_self_referential) × (1 / (grounding + 0.1))

Usage:
  python3 tools/mutate.py                          # list mutation targets
  python3 tools/mutate.py --target PHIL-10         # propose mutations for target
  python3 tools/mutate.py --execute PHIL-10 WEAKEN # execute and log mutation
  python3 tools/mutate.py --parameters             # list mutable tool parameters
  python3 tools/mutate.py --history                # mutation log
  python3 tools/mutate.py --json                   # machine-readable output
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PHILOSOPHY = REPO / "beliefs" / "PHILOSOPHY.md"
MUTATION_LOG = REPO / "experiments" / "mutations"
SESSION_FILE = REPO / "tasks" / "NEXT.md"

MUTATION_TYPES = {
    "NEGATE": "Flip the claim's polarity — test what happens if the opposite is true",
    "WEAKEN": "Add boundary conditions — where does this claim NOT hold?",
    "STRENGTHEN": "Remove qualifiers — is this universally true?",
    "INVERT": "Reverse the causal direction — does the arrow point the other way?",
    "COMBINE": "Merge with another claim — do two ideas compose into something stronger?",
    "SPECIALIZE": "Narrow the scope — is this only true in domain D?",
    "GENERALIZE": "Broaden the scope — does this apply beyond its current domain?",
    "PARAMETER": "Perturb a numeric threshold or constant — is the current value optimal?",
}

# Mutable parameters in tools (file, variable, current, range, description)
MUTABLE_PARAMETERS = [
    ("tools/dispatch_optimizer.py", "UCB1_C", 1.414, (0.5, 3.0), "Exploration-exploitation tradeoff"),
    ("tools/dogma_finder.py", "AXIOM_STUCK_WEIGHT", 0.60, (0.2, 1.0), "How much axiom-stuck contributes to dogma score"),
    ("tools/dogma_finder.py", "CONFIRM_ONLY_WEIGHT", 0.70, (0.2, 1.0), "How much confirm-only contributes to dogma score"),
    ("tools/dogma_finder.py", "SELF_REF_WEIGHT", 0.50, (0.2, 1.0), "Self-referential evidence penalty"),
    ("tools/compact.py", "PROXY_K_THRESHOLD", 6.0, (2.0, 15.0), "Drift % that triggers compaction"),
    ("tools/science_quality.py", "FALSIF_TARGET", 0.20, (0.10, 0.40), "Target fraction of falsification lanes"),
    ("tools/open_lane.py", "LEVEL_FIELD_REQUIRED", True, (False, True), "Whether --level field is enforced"),
]


def get_session():
    """Extract current session number from NEXT.md."""
    try:
        text = SESSION_FILE.read_text()
        m = re.search(r"S(\d+)", text)
        return int(m.group(1)) if m else 0
    except Exception:
        return 0


def parse_philosophy():
    """Extract PHIL claims from PHILOSOPHY.md."""
    if not PHILOSOPHY.exists():
        return []
    text = PHILOSOPHY.read_text()
    claims = []
    # Match [PHIL-N] claims
    for m in re.finditer(r"\*\*\[PHIL-(\d+[a-z]?)\]\*\*\s*(.+?)(?=\n\n|\n\*\*\[PHIL|\Z)", text, re.DOTALL):
        phil_id = f"PHIL-{m.group(1)}"
        body = m.group(2).strip()
        # Check for DROPPED/SUPERSEDED
        if "SUPERSEDED" in body or "DROPPED" in body:
            continue
        # Extract first sentence as claim
        first_sentence = body.split(".")[0] + "." if "." in body else body[:200]
        claims.append({
            "id": phil_id,
            "claim": first_sentence,
            "body": body[:500],
            "grounding": extract_grounding(body),
            "self_referential": "internal" in body.lower() or "self-" in body.lower(),
        })
    return claims


def extract_grounding(text):
    """Extract grounding level from claim text."""
    text_lower = text.lower()
    if "unverified" in text_lower or "aspirational" in text_lower:
        return 0.1
    if "partially" in text_lower:
        return 0.4
    if "grounded" in text_lower or "observed" in text_lower or "confirmed" in text_lower:
        return 0.7
    if "measured" in text_lower:
        return 0.9
    return 0.3


def get_dogma_scores():
    """Get dogma scores from dogma_finder if available."""
    scores = {}
    try:
        import subprocess
        result = subprocess.run(
            ["python3", str(REPO / "tools" / "dogma_finder.py"), "--json"],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            items = data if isinstance(data, list) else data.get("items", [])
            for item in items:
                scores[item["id"]] = item.get("total_score", item.get("score", 0.0))
    except Exception:
        pass
    return scores


def score_mutation_priority(claim, dogma_scores):
    """Score how much this claim needs mutation."""
    dogma = dogma_scores.get(claim["id"], 0.0)
    self_ref_mult = 1.5 if claim["self_referential"] else 1.0
    grounding_mult = 1.0 / (claim["grounding"] + 0.1)
    return round(dogma * self_ref_mult * grounding_mult, 3)


def propose_mutations(claim):
    """Generate mutation proposals for a claim."""
    mutations = []
    claim_text = claim["claim"]

    # NEGATE
    mutations.append({
        "type": "NEGATE",
        "original": claim_text,
        "mutant": f"[NEGATED] The opposite of '{claim['id']}' is true: this property actively hinders the swarm.",
        "test": f"Find 3 concrete instances where {claim['id']}'s claim caused harm or waste in the last 50 sessions.",
        "risk": "low — testing only, no structural change",
    })

    # WEAKEN
    mutations.append({
        "type": "WEAKEN",
        "original": claim_text,
        "mutant": f"[WEAKENED] {claim['id']} holds only within specific boundary conditions (domain, scale, or time horizon).",
        "test": f"Identify the boundary where {claim['id']} stops being true. Measure: at what N, age, or domain does it break?",
        "risk": "low — adds precision without removing claim",
    })

    # STRENGTHEN
    mutations.append({
        "type": "STRENGTHEN",
        "original": claim_text,
        "mutant": f"[STRENGTHENED] {claim['id']} is universally true with no qualifiers — remove all hedging.",
        "test": f"Search for any counterexample to {claim['id']} in the full lesson history. If none found in 1239 lessons, strengthen.",
        "risk": "medium — removes safety qualifiers",
    })

    # INVERT
    mutations.append({
        "type": "INVERT",
        "original": claim_text,
        "mutant": f"[INVERTED] The causal arrow in {claim['id']} points the wrong way. The effect is actually the cause.",
        "test": f"Check temporal ordering: did the supposed cause in {claim['id']} actually precede the supposed effect in git history?",
        "risk": "low — analytical only",
    })

    # SPECIALIZE
    mutations.append({
        "type": "SPECIALIZE",
        "original": claim_text,
        "mutant": f"[SPECIALIZED] {claim['id']} applies only to the meta domain, not universally.",
        "test": f"Test {claim['id']} in 3 non-meta domains. If it fails in ≥2, specialize.",
        "risk": "low — narrows scope",
    })

    return mutations


def list_targets(as_json=False):
    """List mutation targets sorted by priority."""
    claims = parse_philosophy()
    dogma_scores = get_dogma_scores()

    targets = []
    for claim in claims:
        priority = score_mutation_priority(claim, dogma_scores)
        targets.append({
            "id": claim["id"],
            "priority": priority,
            "dogma": dogma_scores.get(claim["id"], 0.0),
            "grounding": claim["grounding"],
            "self_referential": claim["self_referential"],
            "claim": claim["claim"][:120],
        })

    targets.sort(key=lambda x: x["priority"], reverse=True)

    if as_json:
        print(json.dumps({"targets": targets[:15], "parameters": len(MUTABLE_PARAMETERS)}, indent=2))
        return

    print("=" * 70)
    print(f"  MUTATION TARGETS — {len(targets)} claims, {len(MUTABLE_PARAMETERS)} parameters")
    print("=" * 70)
    print()

    for i, t in enumerate(targets[:15], 1):
        sr = " [SELF-REF]" if t["self_referential"] else ""
        print(f"  #{i:2d}  {t['id']:12s}  priority={t['priority']:.2f}  dogma={t['dogma']:.2f}  grounding={t['grounding']:.1f}{sr}")
        print(f"       {t['claim']}")
        print()

    # Mutation history summary
    history = load_history()
    if history:
        print(f"  --- Mutation history: {len(history)} mutations logged ---")
        for h in history[-3:]:
            print(f"  S{h.get('session', '?')} {h['target']} {h['type']} → {h.get('outcome', 'pending')}")
        print()


def list_parameters():
    """List mutable tool parameters."""
    print("=" * 70)
    print("  MUTABLE PARAMETERS")
    print("=" * 70)
    print()
    for i, (file, var, current, range_, desc) in enumerate(MUTABLE_PARAMETERS, 1):
        print(f"  #{i}  {file}::{var}")
        print(f"      Current: {current}  Range: {range_}  — {desc}")
        print()


def execute_mutation(target_id, mutation_type):
    """Log a mutation execution."""
    claims = parse_philosophy()
    claim = next((c for c in claims if c["id"] == target_id), None)
    if not claim:
        print(f"ERROR: {target_id} not found in PHILOSOPHY.md")
        sys.exit(1)

    mutations = propose_mutations(claim)
    mutation = next((m for m in mutations if m["type"] == mutation_type), None)
    if not mutation:
        print(f"ERROR: mutation type {mutation_type} not found")
        sys.exit(1)

    session = get_session()
    MUTATION_LOG.mkdir(parents=True, exist_ok=True)

    record = {
        "session": session,
        "timestamp": datetime.now().isoformat(),
        "target": target_id,
        "type": mutation_type,
        "original": mutation["original"],
        "mutant": mutation["mutant"],
        "test": mutation["test"],
        "risk": mutation["risk"],
        "outcome": "pending",
        "evidence": "",
    }

    filename = f"MUT-{target_id}-{mutation_type}-S{session}.json"
    filepath = MUTATION_LOG / filename
    filepath.write_text(json.dumps(record, indent=2))

    print(f"MUTATION LOGGED: {filepath.name}")
    print(f"  Target:  {target_id}")
    print(f"  Type:    {mutation_type}")
    print(f"  Mutant:  {mutation['mutant'][:120]}")
    print(f"  Test:    {mutation['test'][:120]}")
    print(f"  Risk:    {mutation['risk']}")
    print()
    print(f"  → Execute the test. Record outcome with:")
    print(f"    python3 tools/mutate.py --resolve {filename} CONFIRMED|REJECTED|PARTIAL \"evidence\"")

    return record


def resolve_mutation(filename, outcome, evidence):
    """Resolve a pending mutation with outcome."""
    filepath = MUTATION_LOG / filename
    if not filepath.exists():
        print(f"ERROR: {filepath} not found")
        sys.exit(1)

    record = json.loads(filepath.read_text())
    record["outcome"] = outcome
    record["evidence"] = evidence
    record["resolved"] = datetime.now().isoformat()
    filepath.write_text(json.dumps(record, indent=2))

    print(f"MUTATION RESOLVED: {filename}")
    print(f"  Outcome:  {outcome}")
    print(f"  Evidence: {evidence[:200]}")

    if outcome == "CONFIRMED":
        print(f"\n  → The mutant is better. Apply it to {record['target']} in PHILOSOPHY.md.")
    elif outcome == "REJECTED":
        print(f"\n  → Original claim survives. Log as negative result (still valuable).")
    elif outcome == "PARTIAL":
        print(f"\n  → Boundary found. WEAKEN the original with the discovered condition.")


def load_history():
    """Load mutation history."""
    if not MUTATION_LOG.exists():
        return []
    records = []
    for f in sorted(MUTATION_LOG.glob("MUT-*.json")):
        try:
            records.append(json.loads(f.read_text()))
        except Exception:
            pass
    return records


def show_history():
    """Display mutation history."""
    history = load_history()
    if not history:
        print("No mutations logged yet.")
        return

    print("=" * 70)
    print(f"  MUTATION HISTORY — {len(history)} mutations")
    print("=" * 70)
    print()

    stats = {"pending": 0, "CONFIRMED": 0, "REJECTED": 0, "PARTIAL": 0}
    for h in history:
        outcome = h.get("outcome", "pending")
        stats[outcome] = stats.get(outcome, 0) + 1
        status = "⏳" if outcome == "pending" else "✅" if outcome == "CONFIRMED" else "❌" if outcome == "REJECTED" else "◐"
        print(f"  {status} S{h.get('session', '?'):>3s}  {h['target']:12s}  {h['type']:12s}  → {outcome}")
        if h.get("evidence"):
            print(f"       {h['evidence'][:100]}")
        print()

    print(f"  Summary: {stats}")


def main():
    args = sys.argv[1:]

    if not args:
        list_targets()
    elif args[0] == "--json":
        list_targets(as_json=True)
    elif args[0] == "--parameters":
        list_parameters()
    elif args[0] == "--history":
        show_history()
    elif args[0] == "--target" and len(args) >= 2:
        target_id = args[1]
        claims = parse_philosophy()
        claim = next((c for c in claims if c["id"] == target_id), None)
        if not claim:
            print(f"ERROR: {target_id} not found")
            sys.exit(1)
        mutations = propose_mutations(claim)
        print(f"MUTATIONS FOR {target_id}: {claim['claim'][:100]}")
        print()
        for m in mutations:
            print(f"  [{m['type']}]")
            print(f"    Mutant: {m['mutant'][:120]}")
            print(f"    Test:   {m['test'][:120]}")
            print(f"    Risk:   {m['risk']}")
            print()
    elif args[0] == "--execute" and len(args) >= 3:
        execute_mutation(args[1], args[2])
    elif args[0] == "--resolve" and len(args) >= 4:
        resolve_mutation(args[1], args[2], " ".join(args[3:]))
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
