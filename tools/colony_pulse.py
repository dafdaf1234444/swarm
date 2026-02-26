#!/usr/bin/env python3
"""colony_pulse.py -- Auto-generate memory/PULSE.md for fast human orientation."""
import json, re, subprocess, sys
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FRONTIER, EVO = ROOT/"tasks"/"FRONTIER.md", ROOT/"experiments"/"belief-variants"/"evolution-results.json"
PULSE = ROOT / "memory" / "PULSE.md"

def git(*a):
    return subprocess.run(["git","-C",str(ROOT)]+list(a),
                          capture_output=True, text=True, timeout=10).stdout.strip()

def recent_commits():
    since = (datetime.now() - timedelta(hours=24)).strftime("%Y-%m-%dT%H:%M:%S")
    h24 = [l for l in git("log",f"--since={since}","--format=%h %s (%ar)").splitlines() if l]
    h10 = [l for l in git("log","-10","--format=%h %s (%ar)").splitlines() if l]
    return "\n".join(f"  {l}" for l in (h24 if len(h24)<len(h10) else h10)) or "  (none)"

def hot_files():
    pairs = sorted([(( ROOT/f).stat().st_mtime, f) for f in git("ls-files").splitlines()
                     if (ROOT/f).is_file()], reverse=True)
    return "\n".join(f"  {f}" for _,f in pairs[:10])

def frontier_questions():
    if not FRONTIER.exists(): return "  (no frontier file)"
    text = FRONTIER.read_text(); cut = text.find("## Resolved")
    qs = re.findall(r"^\- \*\*F(\d+)\*\*:\s*(.+)$", text[:cut] if cut>0 else text, re.MULTILINE)
    qs.sort(key=lambda x: int(x[0]))
    return "\n".join(f"  F{i}: {d[:80]}" for i,d in qs) or "  (none open)"

def belief_variants():
    if not EVO.exists(): return "  (no evolution data)"
    data = json.loads(EVO.read_text())
    ranked = sorted(data.items(), key=lambda x: -x[1].get("fitness",0))
    return f"  {len(data)} variants\n"+"\n".join(f"  {n}: {v['fitness']}" for n,v in ranked)

def main():
    md = f"""# Colony Pulse
Generated: {datetime.now():%Y-%m-%d %H:%M}

## Recent Commits
{recent_commits()}

## Hot Files (by mtime)
{hot_files()}

## Open Frontier Questions
{frontier_questions()}

## Belief Variants (by fitness)
{belief_variants()}
"""
    PULSE.write_text(md)
    sys.stdout.write(md)
    print(f"\n--- Saved to {PULSE.relative_to(ROOT)} ---")

if __name__ == "__main__":
    main()
