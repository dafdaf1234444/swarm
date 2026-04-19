import subprocess
from pathlib import Path
from datetime import datetime

def _git(root, *args):
    try:
        return subprocess.check_output(["git", "-C", str(root), *args], text=True).strip()
    except Exception:
        return ""

def _index(root, sub):
    d = root / sub
    if not d.exists():
        return f"_No {sub}/ directory._\n"
    lines = [f"# {sub.capitalize()} Index\n"]
    for f in sorted(d.glob("*.md")):
        first = ""
        try:
            for ln in f.read_text().splitlines():
                if ln.strip():
                    first = ln.strip().lstrip("#").strip(); break
        except Exception: pass
        lines.append(f"- [{f.stem}]({sub}/{f.name}) — {first}")
    return "\n".join(lines) + "\n"

def build(root, out):
    out = root / out if not out.is_absolute() else out
    out.mkdir(parents=True, exist_ok=True)
    for sub in ["lessons", "principles", "questions", "sessions"]:
        (out / f"{sub}-index.md").write_text(_index(root, sub))
    log = _git(root, "log", "--oneline", "-n", "200")
    (out / "CHANGELOG.md").write_text(f"# Changelog\n\n```\n{log}\n```\n")
    toc = ["# Documentation", "", f"_Auto-generated {datetime.utcnow().isoformat()}Z_", "",
           "- [Lessons](lessons-index.md)", "- [Principles](principles-index.md)",
           "- [Questions](questions-index.md)", "- [Sessions](sessions-index.md)",
           "- [Changelog](CHANGELOG.md)", ""]
    (out / "README.md").write_text("\n".join(toc))
    print(f"Docs written to {out}")
