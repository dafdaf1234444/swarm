#!/usr/bin/env python3
"""FMEA reconciliation tool — compute authoritative per-FM status from artifacts.

Reads all experiments/catastrophic-risks/f-cat1-*.json artifacts,
extracts per-FM status transitions in session order, and outputs
authoritative current state. Detects inconsistencies between
aggregate counts and individual FM statuses.

Prescription: L-1267 (FMEA aggregate counts have no single source of truth).
"""

import json
import glob
import re
import sys
from pathlib import Path

ARTIFACTS_DIR = Path("experiments/catastrophic-risks")
ARTIFACT_PATTERN = "f-cat1-*.json"

# Canonical status enum (ordered by mitigation level)
STATUS_ORDER = ["UNMITIGATED", "INADEQUATE", "MINIMAL", "PARTIAL", "ADEQUATE", "RESOLVED"]
# Legacy mapping — includes non-standard status strings from S426 candidates
STATUS_ALIASES = {
    "MITIGATED": "ADEQUATE",
    "FIXED FOR KNOWN INSTANCES; NOT YET FORMALLY REGISTERED": "MINIMAL",
    "IDENTIFIED; NO MITIGATION IMPLEMENTED": "UNMITIGATED",
}

# Manual name overrides for FMs registered only in prose text.
# Text-based extraction is lossy; these provide authoritative names
# sourced from domains/catastrophic-risks/tasks/FRONTIER.md entries.
FM_NAME_OVERRIDES = {
    "FM-29": "Module-extraction import chain fragility",
    "FM-30": "Cross-layer filter cascade blind spot",
    "FM-35": "Scanner attention bias",
    "FM-36": "Elif masking (tool false negatives)",
    "FM-37": "LLM self-tagging inflation",
    "FM-38": "False instrument rate (33% flagged)",
    "FM-39": "Discovery ratio contamination",
    "FM-40": "Diagnosis-without-repair gap",
    "FM-41": "FMEA aggregate tracking drift",
}


def extract_session_number(session_str):
    """Extract numeric session number from 'S420' format."""
    m = re.search(r'S(\d+)', str(session_str))
    return int(m.group(1)) if m else 0


def load_artifacts():
    """Load all FMEA artifacts sorted by session number."""
    artifacts = []
    for path in sorted(glob.glob(str(ARTIFACTS_DIR / ARTIFACT_PATTERN))):
        with open(path) as f:
            data = json.load(f)
        session = data.get("session", "")
        session_num = extract_session_number(session)
        # Fallback: extract session number from filename
        if session_num == 0:
            fname_match = re.search(r's(\d+)\.json$', Path(path).name)
            if fname_match:
                session_num = int(fname_match.group(1))
                if not session:
                    session = f"S{session_num}"
        artifacts.append({
            "path": path,
            "session": session,
            "session_num": session_num,
            "data": data,
        })
    artifacts.sort(key=lambda a: a["session_num"])
    return artifacts


def normalize_status(status):
    """Normalize status string to canonical form."""
    s = str(status).strip().upper()
    if s in STATUS_ALIASES:
        return STATUS_ALIASES[s]
    # Handle verbose status strings (e.g., "FIXED FOR KNOWN INSTANCES...")
    if s in STATUS_ORDER:
        return s
    # Map common verbose patterns to canonical status
    if "FIXED" in s or "RESOLVED" in s:
        return "MINIMAL"
    if "NO MITIGATION" in s or "IDENTIFIED" in s:
        return "UNMITIGATED"
    if "PARTIAL" in s:
        return "PARTIAL"
    # Check if any canonical status appears in the string
    for canonical in STATUS_ORDER:
        if canonical in s:
            return canonical
    return s


def extract_baseline(artifact):
    """Extract FM baseline from S420 registry artifact."""
    fms = {}
    data = artifact["data"]
    registry = data.get("registry", {})
    failure_modes = registry.get("failure_modes", [])
    if not failure_modes:
        return fms

    for fm in failure_modes:
        fm_id = fm.get("id", "")
        if not fm_id:
            continue
        fms[fm_id] = {
            "id": fm_id,
            "name": fm.get("name", ""),
            "severity": fm.get("severity", "UNKNOWN"),
            "status": normalize_status(fm.get("mitigation_status", "UNKNOWN")),
            "transitions": [{
                "session": artifact["session"],
                "status": normalize_status(fm.get("mitigation_status", "UNKNOWN")),
                "source": artifact["path"],
                "type": "baseline",
            }],
        }
    return fms


def extract_hardening_transitions(artifact):
    """Extract status transitions from individual hardening artifacts."""
    transitions = []
    data = artifact["data"]
    path = artifact["path"]
    session = artifact["session"]

    # Detect FM ID from filename (e.g., f-cat1-fm25-hardening-s475.json)
    fm_match = re.search(r'fm(\d+)', Path(path).name)
    if not fm_match:
        return transitions

    fm_ids = [f"FM-{int(fm_match.group(1)):02d}"]

    # Also check for dual-FM files (e.g., fm33-fm34)
    dual_match = re.search(r'fm(\d+)-fm(\d+)', Path(path).name)
    if dual_match:
        fm_ids = [
            f"FM-{int(dual_match.group(1)):02d}",
            f"FM-{int(dual_match.group(2)):02d}",
        ]

    # Infer new status from expect/actual/diff text OR status_change field
    actual = str(data.get("actual", ""))
    expect = str(data.get("expect", ""))
    diff = str(data.get("diff", ""))
    status_change = str(data.get("status_change", ""))
    combined = f"{expect} {actual} {diff} {status_change}"

    for fm_id in fm_ids:
        new_status = None
        # Check for explicit status mentions
        for status in reversed(STATUS_ORDER):
            pattern = rf'{fm_id}.*?(?:→|->|to)\s*{status}'
            if re.search(pattern, combined, re.IGNORECASE):
                new_status = status
                break
        # Check for status in actual field
        if not new_status:
            for status in reversed(STATUS_ORDER):
                pattern = rf'(?:→|->|to)\s*{status}'
                if re.search(pattern, combined, re.IGNORECASE):
                    new_status = status
                    break
        # Hardening artifacts generally upgrade; infer from common patterns
        if not new_status:
            for status in STATUS_ORDER:
                if status in actual.upper():
                    new_status = status

        if new_status:
            transitions.append({
                "fm_id": fm_id,
                "session": session,
                "status": normalize_status(new_status),
                "source": path,
                "type": "hardening",
            })

    return transitions


def extract_reclassifications(artifact):
    """Extract status transitions from reclassification artifacts."""
    transitions = []
    data = artifact["data"]
    path = artifact["path"]
    session = artifact["session"]

    # Check for reclassifications array
    reclassifications = data.get("reclassifications", [])
    for rec in reclassifications:
        fm_id = rec.get("fm", "")
        new_status = rec.get("new_status", "")
        if fm_id and new_status:
            transitions.append({
                "fm_id": fm_id,
                "session": session,
                "status": normalize_status(new_status),
                "source": path,
                "type": "reclassification",
            })

    # Check for survivors (maintained status)
    survivors = data.get("survivors", [])
    for surv in survivors:
        fm_id = surv.get("fm", "")
        if fm_id:
            transitions.append({
                "fm_id": fm_id,
                "session": session,
                "status": "ADEQUATE",
                "source": path,
                "type": "survived-audit",
            })

    return transitions


def extract_new_fms(artifact):
    """Extract newly registered FMs from FMEA snapshot artifacts."""
    new_fms = {}
    data = artifact["data"]
    session = artifact["session"]
    path = artifact["path"]

    # Check data.new_fms (S452 format)
    for fm in data.get("data", {}).get("new_fms", []):
        fm_id = str(fm.get("id", ""))
        if not fm_id:
            continue
        status = normalize_status(fm.get("status", fm.get("mitigation_status", "UNMITIGATED")))
        new_fms[fm_id] = {
            "id": fm_id,
            "name": fm.get("name", ""),
            "severity": fm.get("severity", "UNKNOWN"),
            "status": status,
            "transitions": [{
                "session": session,
                "status": status,
                "source": path,
                "type": "registered",
            }],
        }

    # Check registry.new_fms or registry.failure_modes for new entries
    registry = data.get("registry", {})
    if isinstance(registry, dict):
        for fm in registry.get("new_failure_modes", []):
            fm_id = str(fm.get("id", ""))
            if fm_id and fm_id not in new_fms:
                status = normalize_status(fm.get("status", fm.get("mitigation_status", "UNMITIGATED")))
                new_fms[fm_id] = {
                    "id": fm_id,
                    "name": fm.get("name", ""),
                    "severity": fm.get("severity", "UNKNOWN"),
                    "status": status,
                    "transitions": [{
                        "session": session,
                        "status": status,
                        "source": path,
                        "type": "registered",
                    }],
                }

    return new_fms


def extract_s426_transitions(artifact):
    """Extract transitions and new FM registrations from registry update format."""
    transitions = []
    new_fms = {}
    data = artifact["data"]
    path = artifact["path"]
    session = artifact["session"]

    results = data.get("results", {})
    hardenings = results.get("hardenings_since_s414", results.get("hardenings", {}))
    if isinstance(hardenings, dict):
        for fm_id, info in hardenings.items():
            change = info.get("change", "")
            m = re.match(r'(\w+)\s*(?:→|->)\s*(\w+)', change)
            if m:
                new_status = normalize_status(m.group(2))
                transitions.append({
                    "fm_id": fm_id,
                    "session": info.get("session", session),
                    "status": new_status,
                    "source": path,
                    "type": "registry-update",
                })

    # Extract candidate/new FMs registered in this artifact
    candidates = results.get("candidate_uncatalogued_fms", [])
    for c in candidates:
        fm_id = c.get("candidate", c.get("id", ""))
        if fm_id:
            status = normalize_status(c.get("status", "UNMITIGATED"))
            new_fms[fm_id] = {
                "id": fm_id,
                "name": c.get("name", ""),
                "severity": c.get("severity_estimate", c.get("severity", "UNKNOWN")),
                "status": status,
                "transitions": [{
                    "session": session,
                    "status": status,
                    "source": path,
                    "type": "candidate-registered",
                }],
            }

    return transitions, new_fms


def extract_text_fms_and_transitions(artifact):
    """Extract FM registrations and transitions from actual/diff text fields.

    Catches FMs registered in prose (e.g., 'FM-29 module-extraction import chain fragility')
    and transitions described in text (e.g., 'FM-30 UNMITIGATED→MINIMAL').
    """
    data = artifact["data"]
    session = artifact["session"]
    path = artifact["path"]
    results = {"new_fms": {}, "transitions": []}

    actual = str(data.get("actual", ""))
    diff = str(data.get("diff", ""))
    combined = f"{actual} {diff}"

    # Find FM registrations: "FM-NN name-text" patterns
    for m in re.finditer(r'(FM-(\d+))\s+([A-Za-z][A-Za-z0-9\s\-/()]+?)(?:\.|,|;|\)|\]|$)', combined):
        fm_id = m.group(1)
        fm_num = int(m.group(2))
        name_candidate = m.group(3).strip()
        # Filter out status words that aren't names
        if name_candidate.upper() in STATUS_ORDER or len(name_candidate) < 3:
            continue
        # Only register if it looks like a real name (has lowercase)
        if any(c.islower() for c in name_candidate):
            if fm_id not in results["new_fms"]:
                results["new_fms"][fm_id] = {
                    "id": fm_id,
                    "name": name_candidate[:60],
                    "severity": "UNKNOWN",
                    "status": "UNMITIGATED",
                    "transitions": [{
                        "session": session,
                        "status": "UNMITIGATED",
                        "source": path,
                        "type": "text-registered",
                    }],
                }

    # Find status transitions: "FM-NN STATUS→STATUS" or "FM-NN transitions STATUS→STATUS"
    for m in re.finditer(r'(FM-\d+)\s+(?:\w+\s+)*?(\w+)\s*[→\->]+\s*(\w+)', combined):
        fm_id = m.group(1)
        old_s = m.group(2).upper()
        new_s = m.group(3).upper()
        if old_s in STATUS_ORDER and new_s in STATUS_ORDER:
            results["transitions"].append({
                "fm_id": fm_id,
                "session": session,
                "status": normalize_status(new_s),
                "source": path,
                "type": "text-transition",
            })

    return results


def reconcile():
    """Build authoritative FM state from all artifacts."""
    artifacts = load_artifacts()
    if not artifacts:
        print("ERROR: No artifacts found", file=sys.stderr)
        return None

    fm_state = {}  # fm_id -> {id, name, severity, status, transitions}
    inconsistencies = []

    for art in artifacts:
        path = art["path"]
        fname = Path(path).name

        # 1. Baseline registry
        if "failure-registry" in fname:
            baseline = extract_baseline(art)
            fm_state.update(baseline)

        # 2. Registry updates (S426 format)
        elif "fm-registry-update" in fname:
            transitions, new_fms = extract_s426_transitions(art)
            for t in transitions:
                fm_id = t["fm_id"]
                if fm_id in fm_state:
                    fm_state[fm_id]["status"] = t["status"]
                    fm_state[fm_id]["transitions"].append(t)
            for fm_id, fm_data in new_fms.items():
                if fm_id not in fm_state:
                    fm_state[fm_id] = fm_data

        # 3. Individual FM-specific artifacts (hardening, replication, etc.)
        elif re.search(r'fm\d+', fname) and "fmea" not in fname:
            for t in extract_hardening_transitions(art):
                fm_id = t["fm_id"]
                if fm_id in fm_state:
                    fm_state[fm_id]["status"] = t["status"]
                    fm_state[fm_id]["transitions"].append(t)
                else:
                    fm_state[fm_id] = {
                        "id": fm_id,
                        "name": "",
                        "severity": "UNKNOWN",
                        "status": t["status"],
                        "transitions": [t],
                    }

        # 4. Reclassification artifacts
        elif "reclassification" in fname:
            for t in extract_reclassifications(art):
                fm_id = t["fm_id"]
                if fm_id in fm_state:
                    fm_state[fm_id]["status"] = t["status"]
                    fm_state[fm_id]["transitions"].append(t)

        # 5. FMEA snapshot artifacts — extract new FMs AND text transitions
        elif "fmea-s" in fname:
            new_fms = extract_new_fms(art)
            for fm_id, fm_data in new_fms.items():
                if fm_id not in fm_state:
                    fm_state[fm_id] = fm_data
                else:
                    # Update name/severity if missing
                    if not fm_state[fm_id]["name"] and fm_data["name"]:
                        fm_state[fm_id]["name"] = fm_data["name"]

        # 6. Swiss Cheese / falsification / other special artifacts
        # (handled via text extraction below)

        # Apply text-based extraction to ALL artifacts as fallback
        text_results = extract_text_fms_and_transitions(art)
        for fm_id, fm_data in text_results["new_fms"].items():
            if fm_id not in fm_state:
                fm_state[fm_id] = fm_data
            elif not fm_state[fm_id]["name"] and fm_data["name"]:
                fm_state[fm_id]["name"] = fm_data["name"]
        for t in text_results["transitions"]:
            fm_id = t["fm_id"]
            if fm_id in fm_state:
                fm_state[fm_id]["status"] = t["status"]
                fm_state[fm_id]["transitions"].append(t)

    # Apply name overrides — authoritative names for FMs registered via prose
    for fm_id, name in FM_NAME_OVERRIDES.items():
        if fm_id in fm_state:
            fm_state[fm_id]["name"] = name
        elif fm_id not in fm_state:
            # FM mentioned in FRONTIER.md but no artifact found
            fm_state[fm_id] = {
                "id": fm_id,
                "name": name,
                "severity": "UNKNOWN",
                "status": "UNMITIGATED",
                "transitions": [{"session": "?", "status": "UNMITIGATED", "source": "FM_NAME_OVERRIDES", "type": "manual"}],
            }

    # Build distribution
    distribution = {}
    for fm in fm_state.values():
        s = fm["status"]
        distribution[s] = distribution.get(s, 0) + 1

    # Detect inconsistencies: check S489/S492 aggregate claims
    for art in artifacts:
        fname = Path(art["path"]).name
        data = art["data"]
        if "reclassification" in fname:
            new_dist = data.get("new_distribution", {})
            if new_dist:
                claimed_adequate = new_dist.get("ADEQUATE", 0)
                actual_adequate = distribution.get("ADEQUATE", 0)
                if claimed_adequate != actual_adequate:
                    inconsistencies.append({
                        "source": art["path"],
                        "field": "ADEQUATE count",
                        "claimed": claimed_adequate,
                        "reconciled": actual_adequate,
                    })

    return {
        "fm_state": fm_state,
        "distribution": distribution,
        "total": len(fm_state),
        "inconsistencies": inconsistencies,
        "artifact_count": len(artifacts),
    }


def main():
    result = reconcile()
    if not result:
        sys.exit(1)

    fm_state = result["fm_state"]
    distribution = result["distribution"]
    inconsistencies = result["inconsistencies"]

    if "--json" in sys.argv:
        output = {
            "total_fms": result["total"],
            "distribution": distribution,
            "inconsistencies": inconsistencies,
            "fms": {
                fm_id: {
                    "id": fm["id"],
                    "name": fm["name"],
                    "severity": fm["severity"],
                    "current_status": fm["status"],
                    "transition_count": len(fm["transitions"]),
                    "last_transition": fm["transitions"][-1] if fm["transitions"] else None,
                }
                for fm_id, fm in sorted(fm_state.items(), key=lambda x: extract_session_number(x[0]) if x[0].startswith("FM-") else 0)
            },
        }
        print(json.dumps(output, indent=2))
        return

    # Human-readable output
    print(f"=== FMEA RECONCILIATION ({result['artifact_count']} artifacts) ===")
    print(f"Total FMs: {result['total']}")
    print()

    # Distribution
    print("Distribution:")
    for status in STATUS_ORDER:
        count = distribution.get(status, 0)
        if count:
            print(f"  {status:15s}: {count}")
    print()

    # Per-FM status
    print(f"{'FM':8s} {'Status':15s} {'Sev':10s} {'Trans':6s} {'Last':8s} Name")
    print("-" * 90)
    for fm_id in sorted(fm_state.keys(), key=lambda x: int(re.search(r'\d+', x).group()) if re.search(r'\d+', x) else 0):
        fm = fm_state[fm_id]
        last = fm["transitions"][-1]["session"] if fm["transitions"] else "?"
        print(f"{fm_id:8s} {fm['status']:15s} {str(fm['severity']):10s} {len(fm['transitions']):6d} {last:8s} {fm['name'][:40]}")

    # Inconsistencies
    if inconsistencies:
        print(f"\n--- Inconsistencies ({len(inconsistencies)}) ---")
        for inc in inconsistencies:
            print(f"  {Path(inc['source']).name}: {inc['field']} claimed={inc['claimed']} reconciled={inc['reconciled']}")

    # Transitions detail
    if "--verbose" in sys.argv:
        print("\n--- Transition History ---")
        for fm_id in sorted(fm_state.keys(), key=lambda x: int(re.search(r'\d+', x).group()) if re.search(r'\d+', x) else 0):
            fm = fm_state[fm_id]
            if len(fm["transitions"]) > 1:
                print(f"\n{fm_id} ({fm['name'][:40]}):")
                for t in fm["transitions"]:
                    print(f"  {t['session']:6s} → {t['status']:15s} ({t['type']}) [{Path(t['source']).name}]")


if __name__ == "__main__":
    main()
