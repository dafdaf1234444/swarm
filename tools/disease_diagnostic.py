#!/usr/bin/env python3
"""disease_diagnostic.py — Unified disease scanner for knowledge systems.

Directive: "swarm what is good for the swarm and swarm the bad for the swarm"

Scans any knowledge system (this swarm, external repos, organizations) for
15 disease types. Produces a health report with diagnosis + treatment.

Internal use: unified health dashboard across all disease detectors.
External use: first genuinely externalizable swarm product — a disease
framework applicable to any knowledge-accumulating system.

The 15 diseases generalize from swarm-specific pathologies to universal
patterns. Each disease has:
  - Detection criteria (regex + structural)
  - Severity scoring (0-10)
  - Treatment prescription
  - External analog (what this looks like outside the swarm)

Usage:
    python3 tools/disease_diagnostic.py              # full internal scan
    python3 tools/disease_diagnostic.py --summary     # one-line-per-disease
    python3 tools/disease_diagnostic.py --external    # external-facing report
    python3 tools/disease_diagnostic.py --json        # machine-readable
    python3 tools/disease_diagnostic.py --treat       # prescribe top-3 treatments
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# ============================================================================
# The 15 diseases — universal knowledge-system pathologies
# ============================================================================

DISEASES = {
    "zombie": {
        "name": "Zombie Persistence",
        "description": "Tasks/items persist without resolution, re-queued indefinitely",
        "external_analog": "Standing meetings nobody cancels, legacy projects nobody kills",
        "detection": "recurring items with no resolution across multiple cycles",
        "severity_weight": 7,
    },
    "goodhart": {
        "name": "Goodhart Drift",
        "description": "Proxy metrics diverge from true objective; optimizing proxy destroys target",
        "external_analog": "KPI gaming, citation gaming in academia, teaching-to-the-test",
        "detection": "measurement channels where proxy and target diverge",
        "severity_weight": 9,
    },
    "protocol_decay": {
        "name": "Protocol Decay (L-601)",
        "description": "High-effort voluntary protocols erode within 2-3 cycles",
        "external_analog": "Policy manuals nobody reads after month 1, checkbox compliance",
        "detection": "protocols with declining compliance over time",
        "severity_weight": 8,
    },
    "false_confidence": {
        "name": "False Confidence",
        "description": "Measurement without mechanism change creates illusion of progress",
        "external_analog": "Green dashboards while systems rot, 'meets expectations' reviews",
        "detection": "measurement tools reporting success without corresponding action",
        "severity_weight": 8,
    },
    "self_referentiality": {
        "name": "Self-Referentiality",
        "description": "Evidence chains entirely internal; system evaluates itself by its own standards",
        "external_analog": "Echo chambers, in-paradigm peer review, internal promotion cultures",
        "detection": "ratio of self-referential to externally-grounded knowledge",
        "severity_weight": 9,
    },
    "recursion_trap": {
        "name": "Recursion Trap",
        "description": "Measuring problems is cheaper than fixing them; measurement becomes the equilibrium",
        "external_analog": "Consulting that recommends more consulting, committees that spawn committees",
        "detection": "diagnosis-to-repair ratio; prescriptions without enforcement",
        "severity_weight": 7,
    },
    "ossification": {
        "name": "Ossification / Dogma",
        "description": "Unchallenged claims calcify into axioms; unfalsifiable assumptions harden",
        "external_analog": "'We've always done it this way,' institutional orthodoxy, paradigm lock-in",
        "detection": "claims with zero challenges, confirm-only resolution patterns",
        "severity_weight": 6,
    },
    "survivorship_bias": {
        "name": "Survivorship Bias",
        "description": "Feedback operates only on active/visible state; archived history invisible",
        "external_analog": "Studying successful startups while ignoring failures (Wald 1943)",
        "detection": "feedback mechanisms reading partial history vs full history",
        "severity_weight": 5,
    },
    "cascade_failure": {
        "name": "Cascading Failure",
        "description": "Errors propagate downstream through ungated layer boundaries",
        "external_analog": "2008 financial crisis, supply chain fragility, domino defaults",
        "detection": "layer boundaries without structural gates",
        "severity_weight": 8,
    },
    "false_instrument": {
        "name": "False Instruments",
        "description": "Measurement tools themselves corrupt silently; worse than no measurement",
        "external_analog": "GDP as welfare proxy, BMI as health proxy, broken thermometers",
        "detection": "tools returning zero errors for extended periods, regex drift",
        "severity_weight": 7,
    },
    "measurement_inflation": {
        "name": "Measurement Inflation",
        "description": "Detectors overfit to proxy, flag false positives proportional to quality",
        "external_analog": "Security scanners with 90% false positive rate, spam filters blocking real mail",
        "detection": "high-recurrence + high-completion flagged as problematic",
        "severity_weight": 4,
    },
    "aspiration_erosion": {
        "name": "Aspiration Erosion",
        "description": "Goals without measurement downgrade to advisory; ambition decays to platitude",
        "external_analog": "Mission statements that drift to meaningless platitudes, unfunded mandates",
        "detection": "goals listed without measurement mechanisms",
        "severity_weight": 6,
    },
    "information_bottleneck": {
        "name": "Information Bottleneck",
        "description": "Knowledge isolates from external world as system grows; grounding decays",
        "external_analog": "Institutional amnesia, siloed departments, not-invented-here syndrome",
        "detection": "external citation rate declining with system size",
        "severity_weight": 7,
    },
    "concurrency_conflict": {
        "name": "Concurrency Conflict",
        "description": "Parallel workers overwrite each other; planning becomes preempted",
        "external_analog": "Merge conflicts in large teams, two managers giving contradictory orders",
        "detection": "work absorption rate, planning-to-execution gap",
        "severity_weight": 5,
    },
    "integration_plateau": {
        "name": "Integration Plateau",
        "description": "Architectural ceiling reached; incremental patches can't push past it",
        "external_analog": "Large companies that can't innovate past bureaucratic ceiling, S-curve limits",
        "detection": "growth rate plateau despite continued input",
        "severity_weight": 6,
    },
}


# ============================================================================
# Internal disease detectors (swarm-specific)
# ============================================================================

def _detect_zombies() -> dict:
    """Detect zombie items in SWARM-LANES and NEXT.md."""
    severity = 0
    findings = []

    lanes_file = REPO_ROOT / "tasks" / "SWARM-LANES.md"
    if lanes_file.exists():
        text = lanes_file.read_text()
        # Count rows with session gaps suggesting zombie persistence
        stale_lanes = re.findall(r"\|\s*(DOMEX-\S+)\s*\|.*?\|\s*open\s*\|", text, re.IGNORECASE)
        if stale_lanes:
            findings.append(f"{len(stale_lanes)} open lanes (check for zombies)")
            severity += min(len(stale_lanes), 5)

    next_file = REPO_ROOT / "tasks" / "NEXT.md"
    if next_file.exists():
        text = next_file.read_text()
        recurring = re.findall(r"(?i)\b(recurring|repeat|again|still)\b", text)
        if recurring:
            findings.append(f"{len(recurring)} recurring-language items in NEXT.md")
            severity += min(len(recurring), 3)

    # Check zombie_drops.json for registered zombies (treatment evidence)
    drops = REPO_ROOT / "tools" / "zombie_drops.json"
    treated = 0
    if drops.exists():
        data = json.loads(drops.read_text())
        treated = len(data) if isinstance(data, list) else len(data.get("drops", []))
        findings.append(f"{treated} zombies registered in zombie_drops.json (treated)")

    return {"severity": min(severity, 10), "findings": findings, "treated": treated}


def _detect_self_referentiality() -> dict:
    """Measure internal vs external reference ratio."""
    lessons_dir = REPO_ROOT / "memory" / "lessons"
    if not lessons_dir.exists():
        return {"severity": 0, "findings": ["No lessons directory found"]}

    internal_refs = 0
    external_refs = 0
    total_lessons = 0

    for f in sorted(lessons_dir.glob("L-*.md")):
        text = f.read_text()
        total_lessons += 1
        # Count internal references (L-NNN, P-NNN, PHIL-NNN, F-XXX)
        internal_refs += len(re.findall(r"\b(L-\d+|P-\d+|PHIL-\d+|F-[A-Z]+\d+|SIG-\d+)\b", text))
        # Count external references (author-year citations, URLs, paper titles)
        external_refs += len(re.findall(r"\b[A-Z][a-z]+\s+(\(&?\s*)?(19|20)\d{2}", text))
        external_refs += len(re.findall(r"(?i)\b(arXiv|doi|journal|paper|published)\b", text))

    ratio = internal_refs / max(external_refs, 1)
    severity = min(int(ratio / 2), 10)  # ratio > 20 = severity 10

    findings = [
        f"{total_lessons} lessons scanned",
        f"Internal refs: {internal_refs}, External refs: {external_refs}",
        f"Internal/external ratio: {ratio:.1f}:1",
    ]

    return {"severity": severity, "findings": findings, "ratio": round(ratio, 1)}


def _detect_ossification() -> dict:
    """Run dogma detection on philosophy claims."""
    phil_file = REPO_ROOT / "beliefs" / "PHILOSOPHY.md"
    if not phil_file.exists():
        return {"severity": 0, "findings": ["No PHILOSOPHY.md found"]}

    text = phil_file.read_text()
    unchallenged = len(re.findall(r"(?i)\bUNCHALLENGED\b", text))
    confirm_only = len(re.findall(r"(?i)\bCONFIRM-ONLY\b", text))
    axiom_stuck = len(re.findall(r"(?i)\bAXIOM-STUCK\b", text))
    total_phils = len(re.findall(r"\bPHIL-\d+\b", text))

    ossified = unchallenged + confirm_only + axiom_stuck
    severity = min(int(ossified / 2), 10)

    findings = [
        f"{total_phils} PHIL claims found",
        f"UNCHALLENGED: {unchallenged}, CONFIRM-ONLY: {confirm_only}, AXIOM-STUCK: {axiom_stuck}",
        f"Ossification rate: {ossified}/{total_phils} ({100*ossified/max(total_phils,1):.0f}%)",
    ]

    return {"severity": severity, "findings": findings}


def _detect_false_confidence() -> dict:
    """Detect claims of success without external validation."""
    lessons_dir = REPO_ROOT / "memory" / "lessons"
    if not lessons_dir.exists():
        return {"severity": 0, "findings": []}

    false_conf_count = 0
    examples = []

    for f in sorted(lessons_dir.glob("L-*.md"))[-200:]:  # Recent 200
        text = f.read_text()
        if re.search(r"(?i)\b(confirmed|verified|proven)\b.*\b(self|internal|swarm)\b", text):
            if not re.search(r"(?i)\b(external|independent|adversarial)\b.*\b(validat|verif|test)\b", text):
                false_conf_count += 1
                if len(examples) < 3:
                    examples.append(f.stem)

    severity = min(false_conf_count // 3, 10)
    findings = [
        f"{false_conf_count} lessons with internal-only confirmation (recent 200)",
    ]
    if examples:
        findings.append(f"Examples: {', '.join(examples)}")

    return {"severity": severity, "findings": findings}


def _detect_goodhart() -> dict:
    """Detect proxy-target divergence in measurement channels."""
    findings = []
    severity = 0

    # Check if reward_theory.py exists and has documented channels
    reward_file = REPO_ROOT / "tools" / "reward_theory.py"
    if reward_file.exists():
        text = reward_file.read_text()
        channels = len(re.findall(r"(?i)channel\s*\d", text))
        findings.append(f"{channels} Goodhart channels documented in reward_theory.py")
        severity += min(channels, 6)

    # Check for known Goodhart symptoms: high metric + low mechanism change
    principles_file = REPO_ROOT / "memory" / "PRINCIPLES.md"
    if principles_file.exists():
        text = principles_file.read_text()
        goodhart_refs = len(re.findall(r"(?i)\bgoodhart\b", text))
        findings.append(f"{goodhart_refs} Goodhart references in principles")
        if goodhart_refs > 3:
            severity += 2  # System is aware of the disease (partial treatment)

    return {"severity": min(severity, 10), "findings": findings}


def _detect_aspiration_erosion() -> dict:
    """Detect goals/principles without enforcement mechanisms."""
    principles_file = REPO_ROOT / "memory" / "PRINCIPLES.md"
    if not principles_file.exists():
        return {"severity": 0, "findings": []}

    text = principles_file.read_text()
    total_principles = len(re.findall(r"\bP-\d+\b", text))

    # Count aspirational language without enforcement
    aspirational = len(re.findall(r"(?i)\b(should|must|needs to|aspirational|target)\b.*\b(but|however|yet|0%|zero)\b", text))

    severity = min(aspirational, 10)
    findings = [
        f"{total_principles} principles total",
        f"{aspirational} with aspirational-but-unenforced language",
    ]

    return {"severity": severity, "findings": findings}


def _detect_protocol_decay() -> dict:
    """Detect evidence of protocol non-compliance over time."""
    findings = []
    severity = 0

    # Check maintenance outcomes for recurring failures
    outcomes_file = REPO_ROOT / "workspace" / "maintenance-outcomes.json"
    if outcomes_file.exists():
        try:
            data = json.loads(outcomes_file.read_text())
            if isinstance(data, list):
                fails = sum(1 for d in data if d.get("status") in ("FAIL", "WARN"))
                findings.append(f"{fails}/{len(data)} maintenance outcomes FAIL/WARN")
                severity += min(fails, 5)
        except (json.JSONDecodeError, TypeError):
            findings.append("maintenance-outcomes.json parse error")
            severity += 2

    # L-601 structural enforcement theorem: check for unstructured protocols
    swarm_md = REPO_ROOT / "SWARM.md"
    if swarm_md.exists():
        text = swarm_md.read_text()
        voluntary = len(re.findall(r"(?i)\b(should|recommended|optional|advisory)\b", text))
        structural = len(re.findall(r"(?i)\b(must|required|enforced|mandatory|wired)\b", text))
        findings.append(f"Protocol language: {structural} structural vs {voluntary} voluntary")
        if voluntary > structural:
            severity += 3

    return {"severity": min(severity, 10), "findings": findings}


def _detect_integration_plateau() -> dict:
    """Detect growth rate plateau signals."""
    findings = []
    severity = 0

    lessons_dir = REPO_ROOT / "memory" / "lessons"
    if lessons_dir.exists():
        total = len(list(lessons_dir.glob("L-*.md")))
        findings.append(f"{total} total lessons")
        if total > 500:
            severity += 3  # Past integration-bound crossover
            findings.append("Past N=550 integration-bound crossover (L-912)")
        if total > 1000:
            severity += 2
            findings.append("Attention per lesson: ~0.001 (below 0.002 threshold)")

    return {"severity": min(severity, 10), "findings": findings}


# Map disease IDs to detector functions
DETECTORS = {
    "zombie": _detect_zombies,
    "self_referentiality": _detect_self_referentiality,
    "ossification": _detect_ossification,
    "false_confidence": _detect_false_confidence,
    "goodhart": _detect_goodhart,
    "aspiration_erosion": _detect_aspiration_erosion,
    "protocol_decay": _detect_protocol_decay,
    "integration_plateau": _detect_integration_plateau,
}


# ============================================================================
# Treatment prescriptions
# ============================================================================

TREATMENTS = {
    "zombie": "Register in zombie_drops.json. Apply 95%-rule (L-1062). Convert deferred conditions to frontier or ABANDON.",
    "goodhart": "Map proxy AND target simultaneously. Composite metrics (proxy × quality). Falsification premium 2.4x.",
    "protocol_decay": "Enforce at creation time, not retrofit (L-601). Wire into execution path. 3-tier cost gradient.",
    "false_confidence": "Require adversarial review for self-referential claims (L-1210). Test measurement tools themselves.",
    "self_referentiality": "Produce external outputs (F-COMP1). External prediction registry. Grounding decay mechanism.",
    "recursion_trap": "Make fixing cheaper than measuring. DUE entries with concrete tool paths at creation (PHIL-22).",
    "ossification": "Run dogma_finder.py --prescribe. Subject axioms to epistemic type classification. Cross-challenge.",
    "survivorship_bias": "Verify feedback mechanisms read full history including archives (L-572, Wald 1943).",
    "cascade_failure": "Structural gates at layer boundaries (L-1359). Swiss Cheese model: gated layers contain failures.",
    "false_instrument": "Format contracts for regex parsers. Any tool returning zero errors for N cycles → audit.",
    "measurement_inflation": "Calibrate detectors before deployment. High recurrence + high completion = healthy not zombie.",
    "aspiration_erosion": "Measurement required at goal creation. Enforcement wiring within 5 cycles (L-601).",
    "information_bottleneck": "External grounding enforcement. Prediction registry with independent outcome verification.",
    "concurrency_conflict": "Anti-repeat checks before each action. Expect work absorption at high concurrency as normal.",
    "integration_plateau": "Architectural rework required. External output production. Publication loop for substrate improvement.",
}


# ============================================================================
# Amplification prescriptions (what's GOOD — feed more of this)
# ============================================================================

AMPLIFIERS = {
    "external_grounding": {
        "signal": "Knowledge grounded in external evidence (119x strongest GOOD signal)",
        "amplify": "Weight dispatch toward domains producing external citations. Grounding audit mandatory.",
        "mechanism": "dispatch_scoring.py soul_boost, grounding_audit.py, external_grounding_check.py",
    },
    "external_method": {
        "signal": "Methods/patterns usable outside the swarm (97x)",
        "amplify": "Every DOMEX lane must state what external system could use the finding.",
        "mechanism": "open_lane.py --external-use field, F-COMP1 closure requirement",
    },
    "world_discovery": {
        "signal": "Discovers something about the world, not about itself (25x)",
        "amplify": "Prediction registry (PRED-NNNN). Finance domain. Real forecasts with verifiable outcomes.",
        "mechanism": "F-FORE1, SIG-77 (finance), external prediction tracking",
    },
    "quantified_finding": {
        "signal": "Quantified comparative findings with transferable insight (54x)",
        "amplify": "Require effect sizes in all DOMEX conclusions. Not just 'confirmed' — how much?",
        "mechanism": "science_quality.py effect-size field, EAD enforcement",
    },
    "teaches_principle": {
        "signal": "Transferable principles about systems/knowledge/collaboration",
        "amplify": "Extract generalizable laws from domain findings. ISO framework for cross-system transfer.",
        "mechanism": "concept_inventor.py, polymath mapping (L-1374: 4x faster for ISO discovery)",
    },
}


def run_diagnostics() -> dict:
    """Run all internal disease detectors and return unified health report."""
    results = {}

    for disease_id, disease_info in DISEASES.items():
        detector = DETECTORS.get(disease_id)
        if detector:
            detection = detector()
        else:
            detection = {"severity": -1, "findings": ["No automated detector (manual check required)"]}

        results[disease_id] = {
            **disease_info,
            "detected_severity": detection["severity"],
            "findings": detection.get("findings", []),
            "treatment": TREATMENTS.get(disease_id, "No treatment documented"),
            "detection_data": {k: v for k, v in detection.items() if k not in ("severity", "findings")},
        }

    return results


def print_summary(results: dict) -> None:
    """Print one-line-per-disease summary."""
    print("=== SWARM DISEASE DIAGNOSTIC ===\n")

    # Sort by severity (highest first)
    sorted_diseases = sorted(results.items(), key=lambda x: x[1]["detected_severity"], reverse=True)

    total_severity = 0
    detected_count = 0

    for disease_id, info in sorted_diseases:
        sev = info["detected_severity"]
        if sev < 0:
            bar = "  [?]  "
            label = "UNSCANNED"
        elif sev == 0:
            bar = "  [·]  "
            label = "HEALTHY"
        elif sev <= 3:
            bar = "  [▪]  "
            label = "MILD"
        elif sev <= 6:
            bar = "  [▪▪] "
            label = "MODERATE"
        else:
            bar = "  [▪▪▪]"
            label = "SEVERE"

        if sev >= 0:
            total_severity += sev
            detected_count += 1

        print(f"{bar} {label:10s} {info['name']}")
        if info["findings"]:
            for f in info["findings"][:2]:
                print(f"              {f}")

    # Overall health score
    if detected_count > 0:
        health = max(0, 100 - (total_severity * 100 // (detected_count * 10)))
        print(f"\n  Overall health: {health}% ({total_severity}/{detected_count * 10} disease burden)")

    # Human impact integration
    print("\n--- Good/Bad Signal Balance ---")
    print("  AMPLIFY (do more of):")
    for amp_id, amp in AMPLIFIERS.items():
        print(f"    ↑ {amp['signal']}")
    print("  ATTACK (do less of):")
    # Top 3 by severity
    for disease_id, info in sorted_diseases[:3]:
        if info["detected_severity"] > 0:
            print(f"    ↓ {info['name']}: {info['treatment'][:80]}...")


def print_treatments(results: dict) -> None:
    """Print top-3 treatment prescriptions."""
    sorted_diseases = sorted(
        [(k, v) for k, v in results.items() if v["detected_severity"] > 0],
        key=lambda x: x[1]["detected_severity"],
        reverse=True,
    )

    print("=== TREATMENT PRESCRIPTIONS (top 3) ===\n")
    for i, (disease_id, info) in enumerate(sorted_diseases[:3], 1):
        print(f"  [{i}] {info['name']} (severity {info['detected_severity']}/10)")
        print(f"      Diagnosis: {'; '.join(info['findings'][:2])}")
        print(f"      Treatment: {info['treatment']}")
        print(f"      External analog: {info['external_analog']}")
        print()


def print_external(results: dict) -> None:
    """Print external-facing report (no swarm-specific jargon)."""
    print("=" * 60)
    print("KNOWLEDGE SYSTEM HEALTH DIAGNOSTIC")
    print("A framework for detecting diseases in any knowledge-")
    print("accumulating system: organizations, codebases, research")
    print("programs, institutions, markets.")
    print("=" * 60)
    print()

    for disease_id, info in DISEASES.items():
        sev = results[disease_id]["detected_severity"]
        status = "DETECTED" if sev > 3 else "LOW" if sev >= 0 else "UNCHECKED"
        print(f"  {info['name']}")
        print(f"    What it is: {info['description']}")
        print(f"    In organizations: {info['external_analog']}")
        print(f"    How to detect: {info['detection']}")
        print(f"    Status in this system: {status} (severity {sev}/10)")
        print()

    print("--- Healthy patterns to amplify ---")
    for amp_id, amp in AMPLIFIERS.items():
        print(f"  ↑ {amp_id}: {amp['signal']}")
        print(f"    How: {amp['amplify']}")
        print()


def main():
    parser = argparse.ArgumentParser(description="Unified disease diagnostic for knowledge systems")
    parser.add_argument("--summary", action="store_true", help="One-line-per-disease summary")
    parser.add_argument("--external", action="store_true", help="External-facing report (no jargon)")
    parser.add_argument("--json", action="store_true", help="Machine-readable output")
    parser.add_argument("--treat", action="store_true", help="Top-3 treatment prescriptions")
    args = parser.parse_args()

    results = run_diagnostics()

    if args.json:
        # Flatten for JSON output
        output = {
            "diseases": results,
            "amplifiers": AMPLIFIERS,
            "total_severity": sum(v["detected_severity"] for v in results.values() if v["detected_severity"] >= 0),
            "scanned": sum(1 for v in results.values() if v["detected_severity"] >= 0),
        }
        print(json.dumps(output, indent=2))
    elif args.external:
        print_external(results)
    elif args.treat:
        print_treatments(results)
    else:
        print_summary(results)
        if not args.summary:
            print()
            print_treatments(results)


if __name__ == "__main__":
    main()
