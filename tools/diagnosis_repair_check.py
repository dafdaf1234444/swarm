#!/usr/bin/env python3
"""FM-40: Diagnosis-without-repair gap detector.

Scans lessons for targeted prescriptions ('Message: tool:X → ...') and checks
whether the target file was modified after the lesson was created. Reports
unfulfilled prescriptions as NOTICE-level maintenance items.

L-1211/L-1263: 61% of prescriptions are unenforced. This tool catches the
specific subset that names a concrete target file but was never acted on.
"""

import os
import re
import subprocess
import sys
import json

LESSON_DIR = "memory/lessons"


def get_prescriptions():
    """Extract targeted prescriptions from lessons."""
    prescriptions = []
    for f in sorted(os.listdir(LESSON_DIR)):
        if not f.startswith("L-") or not f.endswith(".md"):
            continue
        path = os.path.join(LESSON_DIR, f)
        with open(path) as fh:
            text = fh.read()
        # Extract session number
        sm = re.search(r"Session[:\s]*S(\d+)", text)
        session = int(sm.group(1)) if sm else 0
        for line in text.split("\n"):
            # Pattern 1: Message: tool:X → action
            m = re.search(r"Message:\s*tool:(\S+)\s*[→\-—]+\s*(.+)", line)
            if m:
                target = m.group(1)
                action = m.group(2).strip()[:80]
                target_path = target if "/" in target else f"tools/{target}"
                prescriptions.append(
                    {
                        "lesson": f,
                        "session": session,
                        "target": target_path,
                        "action": action,
                        "type": "Message",
                    }
                )
    return prescriptions


def check_fulfillment(prescriptions):
    """Check if prescribed targets were modified after lesson creation."""
    results = []
    for p in prescriptions:
        target = p["target"]
        # Check if target exists
        if not os.path.exists(target):
            p["status"] = "TARGET_MISSING"
            p["detail"] = "File does not exist (archived or never created)"
            results.append(p)
            continue
        # Get lesson creation session
        lesson_session = p["session"]
        # Check if target was modified in commits after the lesson's session
        try:
            result = subprocess.run(
                ["git", "log", "--oneline", "--format=%s", "-20", "--", target],
                capture_output=True,
                text=True,
                timeout=5,
            )
            commits = result.stdout.strip().split("\n") if result.stdout.strip() else []
            # Check if any commit after lesson session mentions related work
            modified_after = False
            for c in commits:
                cm = re.search(r"\[S(\d+)\]", c)
                if cm and int(cm.group(1)) > lesson_session:
                    modified_after = True
                    break
            if modified_after:
                p["status"] = "POSSIBLY_FULFILLED"
                p["detail"] = f"Target modified after S{lesson_session}"
            else:
                p["status"] = "UNFULFILLED"
                p["detail"] = f"No modification to {target} after S{lesson_session}"
        except Exception:
            p["status"] = "CHECK_FAILED"
            p["detail"] = "Could not check git history"
        results.append(p)
    return results


def main():
    prescriptions = get_prescriptions()
    if not prescriptions:
        print("No targeted prescriptions found.")
        return
    results = check_fulfillment(prescriptions)
    unfulfilled = [r for r in results if r["status"] in ("UNFULFILLED", "TARGET_MISSING")]
    fulfilled = [r for r in results if r["status"] == "POSSIBLY_FULFILLED"]

    if "--json" not in sys.argv:
        print(f"=== FM-40 DIAGNOSIS-REPAIR CHECK ({len(prescriptions)} prescriptions) ===")
        print(f"  Fulfilled/modified: {len(fulfilled)}")
        print(f"  Unfulfilled: {len(unfulfilled)}")
        print()
        if unfulfilled:
            print("--- Unfulfilled prescriptions ---")
            for r in unfulfilled:
                print(f"  {r['lesson']} (S{r['session']}) → {r['target']}: {r['status']}")
                print(f"    Action: {r['action']}")
                print(f"    Detail: {r['detail']}")
            print()

    json_mode = "--json" in sys.argv
    if json_mode:
        artifact = {
            "tool": "diagnosis_repair_check.py",
            "session": "S501",
            "total_prescriptions": len(prescriptions),
            "fulfilled": len(fulfilled),
            "unfulfilled": len(unfulfilled),
            "unfulfilled_items": [
                {
                    "lesson": r["lesson"],
                    "session": r["session"],
                    "target": r["target"],
                    "action": r["action"],
                    "status": r["status"],
                }
                for r in unfulfilled
            ],
        }
        json.dump(artifact, sys.stdout, indent=2)
        print()


if __name__ == "__main__":
    main()
