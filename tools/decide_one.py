#!/usr/bin/env python3
import re
import sys
import subprocess

ID = sys.argv[1] if len(sys.argv) > 1 else ""

def run(cmd):
    try:
        return subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)
    except Exception:
        return ""

orient = run(["python3", "tools/orient.py"])
next_md = ""
for path in ["tasks/NEXT.md", "memory/SESSION-LOG.md", "tasks/SWARM-LANES.md"]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            next_md += "\n" + f.read()
    except Exception:
        pass

text = (orient + "\n" + next_md).lower()

id_hits = []
for line in text.splitlines():
    if ID.lower() in line:
        id_hits.append(line)

scope = "\n".join(id_hits) if id_hits else text

delete_words = [
    "duplicate", "near-duplicate", "overfit", "stale", "obsolete",
    "abandon", "remove", "delete", "bad", "failed", "wrong",
    "regression", "redundant", "not needed"
]
keep_words = [
    "achieved", "working", "resolved", "good", "merged", "accepted",
    "done", "keep", "useful", "important", "success", "shipped"
]
skip_words = [
    "unclear", "unknown", "todo", "follow-up", "investigate", "maybe",
    "consider", "question", "needs review", "open"
]

d = sum(scope.count(w) for w in delete_words)
k = sum(scope.count(w) for w in keep_words)
s = sum(scope.count(w) for w in skip_words)

if d > k and d >= s:
    print("d")
elif k > d and k >= s:
    print("k")
else:
    print("s")
