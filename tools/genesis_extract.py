#!/usr/bin/env python3
"""
genesis_extract.py — Produce a compact genesis bundle for daughter swarm (L-1471).

Tiers: --lean --minimal ~470KB | --minimal ~730KB | default ~870KB

Usage:
    python3 tools/genesis_extract.py --out /tmp/daughter --minimal --lean
    python3 tools/genesis_extract.py --dry-run --json
"""

import argparse
import json
import os
import re
import shutil
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

IDENTITY_FILES = [
    ("beliefs/CORE.md", "beliefs/CORE.md"),
    ("beliefs/PHILOSOPHY.md", "beliefs/PHILOSOPHY.md"),
    ("SWARM.md", "SWARM.md"),
]
ORIENTATION_ESSENTIAL = [
    ("memory/PRINCIPLES.md", "memory/PRINCIPLES.md"),
    ("beliefs/DEPS.md", "beliefs/DEPS.md"),
    ("beliefs/INVARIANTS.md", "beliefs/INVARIANTS.md"),
    ("beliefs/CROSS.md", "beliefs/CROSS.md"),
    ("memory/INDEX.md", "memory/INDEX.md"),
    ("tasks/FRONTIER.md", "tasks/FRONTIER.md"),
]
ORIENTATION_REFERENCE = [
    ("beliefs/CHALLENGES.md", "beliefs/CHALLENGES.md"),
    ("memory/EXPECT.md", "memory/EXPECT.md"),
    ("memory/DISTILL.md", "memory/DISTILL.md"),
    ("memory/VERIFY.md", "memory/VERIFY.md"),
    ("domains/ISOMORPHISM-ATLAS.md", "domains/ISOMORPHISM-ATLAS.md"),
]
BOOT_TOOLS = [
    "tools/orient.py", "tools/orient_checks.py", "tools/orient_state.py",
    "tools/orient_sections.py", "tools/orient_analysis.py", "tools/orient_monitors.py",
    "tools/compact.py", "tools/validate_beliefs.py", "tools/sync_state.py",
    "tools/cell_blueprint.py",
]
GROWTH_TOOLS = [
    "tools/dispatch_optimizer.py", "tools/dispatch_data.py", "tools/dispatch_scoring.py",
    "tools/open_lane.py", "tools/close_lane.py", "tools/claim.py",
    "tools/genesis_seeds.py", "tools/genesis_extract.py", "tools/check.sh",
]
CORE_TOOLS = BOOT_TOOLS + GROWTH_TOOLS


def _citation_graph():
    in_degree = defaultdict(int)
    lessons_dir = ROOT / "memory" / "lessons"
    if not lessons_dir.exists():
        return in_degree
    lid_pattern = re.compile(r"L-(\d+)")
    for f in lessons_dir.glob("L-*.md"):
        text = f.read_text(errors="replace")
        refs = set()
        for m in lid_pattern.finditer(text):
            ref = f"L-{m.group(1)}"
            own_id_match = re.match(r"L-(\d+)", f.stem)
            if own_id_match and ref == f"L-{own_id_match.group(1)}":
                continue
            refs.add(ref)
        for ref in refs:
            in_degree[ref] += 1
    return in_degree


def _domain_reach(lessons_dir):
    reach = defaultdict(set)
    lid_pattern = re.compile(r"L-(\d+)")
    domain_pattern = re.compile(r"\*\*Domain\*\*:\s*(\S+)")
    for f in lessons_dir.glob("L-*.md"):
        text = f.read_text(errors="replace")
        dm = domain_pattern.search(text[:500])
        domain = dm.group(1) if dm else "unknown"
        for m in lid_pattern.finditer(text):
            reach[f"L-{m.group(1)}"].add(domain)
    return reach


def select_hub_lessons(top_n=100):
    lessons_dir = ROOT / "memory" / "lessons"
    if not lessons_dir.exists():
        return []
    in_degree = _citation_graph()
    reach = _domain_reach(lessons_dir)
    import math
    scores = {}
    for lid, deg in in_degree.items():
        dr = len(reach.get(lid, set()))
        scores[lid] = deg * math.log2(dr + 1) if dr > 0 else deg
    ranked = sorted(scores.items(), key=lambda x: -x[1])[:top_n]
    results = []
    for lid, score in ranked:
        if not re.match(r"L-(\d+)", lid):
            continue
        fpath = lessons_dir / f"{lid}.md"
        if not fpath.exists():
            continue
        results.append({"id": lid, "path": str(fpath.relative_to(ROOT)),
                        "in_degree": in_degree[lid],
                        "domain_reach": len(reach.get(lid, set())),
                        "score": round(score, 1)})
    return results


def extract_genesis(out_dir, top_n=100, include_tools=True, minimal=False,
                    lean=False, dry_run=False):
    out = Path(out_dir)
    manifest = {"layers": {}, "total_files": 0, "total_bytes": 0}

    def _copy(src_rel, dst_rel, layer_name):
        src = ROOT / src_rel
        if not src.exists():
            return None
        size = src.stat().st_size
        entry = {"src": src_rel, "dst": dst_rel, "bytes": size}
        if not dry_run:
            dst = out / dst_rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(str(src), str(dst))
        if layer_name not in manifest["layers"]:
            manifest["layers"][layer_name] = {"files": [], "bytes": 0}
        manifest["layers"][layer_name]["files"].append(entry)
        manifest["layers"][layer_name]["bytes"] += size
        manifest["total_files"] += 1
        manifest["total_bytes"] += size
        return entry

    for src, dst in IDENTITY_FILES:
        _copy(src, dst, "identity")
    for src, dst in ORIENTATION_ESSENTIAL:
        _copy(src, dst, "orientation")
    if not minimal:
        for src, dst in ORIENTATION_REFERENCE:
            _copy(src, dst, "orientation_ref")
    hubs = select_hub_lessons(top_n)
    manifest["hub_lesson_count"] = len(hubs)
    manifest["hub_lessons_top5"] = [h["id"] for h in hubs[:5]]
    for hub in hubs:
        _copy(hub["path"], hub["path"], "hub_lessons")
    if include_tools:
        for tool_path in (BOOT_TOOLS if lean else CORE_TOOLS):
            _copy(tool_path, tool_path, "core_tools")
    if not dry_run:
        _rewrite_daughter_index(out, hubs)
        _write_daughter_stubs(out)
        _write_daughter_bridge(out, hubs)
        _init_daughter_git(out)
    manifest["compression_ratio"] = f"{manifest['total_bytes'] / 1024:.0f}KB"
    return manifest


def _rewrite_daughter_index(out_dir, hubs):
    index_path = out_dir / "memory" / "INDEX.md"
    if not index_path.exists():
        return
    text = index_path.read_text(encoding="utf-8")
    lesson_count = len(list((out_dir / "memory" / "lessons").glob("L-*.md"))) \
        if (out_dir / "memory" / "lessons").exists() else 0
    principles_path = out_dir / "memory" / "PRINCIPLES.md"
    principle_count = 0
    if principles_path.exists():
        p_text = principles_path.read_text(errors="replace")
        pm = re.search(r"(\d+)\s+live\s+principles", p_text[:500])
        if pm:
            principle_count = int(pm.group(1))
        else:
            principle_count = len(set(re.findall(r"P-(\d+)", p_text)))
    text = re.sub(r"Updated:.*?\n", "Updated: genesis | Sessions: 0\n", text, count=1)
    text = re.sub(r"\*\*\d+ lessons\*\*", f"**{lesson_count} lessons**", text, count=1)
    theme_pattern = re.compile(r"^## Themes.*?\n(?:\|.*\n)*", re.MULTILINE)
    text = theme_pattern.sub(
        f"## Themes ({lesson_count} hub lessons — build your own theme index)\n"
        "| Theme | Count | Key insight |\n|-------|-------|-------------|\n"
        f"| (unthemed hub lessons) | {lesson_count}"
        " | Inherited from parent — categorize as you grow |\n", text)
    provenance = ("<!-- DAUGHTER SWARM: genesis bundle. "
        f"{lesson_count} hub lessons inherited from parent's {len(hubs)} ranked. -->\n")
    if "<!-- DAUGHTER SWARM" not in text:
        text = provenance + text
    index_path.write_text(text, encoding="utf-8")


def _write_daughter_stubs(out_dir):
    stubs = {
        "tasks/NEXT.md": "Updated: genesis S0\n\n## Key state\n- Genesis daughter.\n\n"
            "## For next session\n1. **Orient** — `python3 tools/orient.py`\n"
            "2. **Pick a frontier** — `tasks/FRONTIER.md`\n3. **Act and learn**\n",
        "tasks/SWARM-LANES.md": "# Swarm Lanes\n\n## Active\n"
            "| Lane | Domain | Mode | Session | Scope |\n"
            "|------|--------|------|---------|-------|\n\n## Merged\n"
            "| Lane | Domain | Session | Outcome |\n|------|--------|---------|--------|\n",
        "tasks/SIGNALS.md": "# Signals\n\nNo signals yet.\n",
        "tasks/SESSION-LOG.md": "# Session Log\n\n"
            "| Session | Date | Lessons | Principles | Summary |\n"
            "|---------|------|---------|------------|---------|\n",
    }
    for rel_path, content in stubs.items():
        fpath = out_dir / rel_path
        fpath.parent.mkdir(parents=True, exist_ok=True)
        if not fpath.exists():
            fpath.write_text(content, encoding="utf-8")


def _init_daughter_git(out_dir):
    import subprocess
    try:
        subprocess.run(["git", "init"], cwd=str(out_dir), capture_output=True, timeout=10)
        subprocess.run(["git", "add", "."], cwd=str(out_dir), capture_output=True, timeout=10)
        subprocess.run(["git", "commit", "-m", "Genesis: daughter swarm born"],
                       cwd=str(out_dir), capture_output=True, timeout=10)
    except Exception:
        pass


def _write_daughter_bridge(out_dir, hubs):
    lesson_count = len(list((out_dir / "memory" / "lessons").glob("L-*.md"))) \
        if (out_dir / "memory" / "lessons").exists() else 0
    (out_dir / "CLAUDE.md").write_text(
        "# Daughter Swarm (Genesis Bundle)\n\n"
        "Read `SWARM.md` for the full protocol.\n\n"
        "## Quick start\n- `python3 tools/orient.py` — orient\n"
        "- `beliefs/CORE.md` for identity\n- `memory/PRINCIPLES.md` for rules\n"
        f"- {lesson_count} hub lessons in `memory/lessons/`\n\n"
        "## What you are\nYou are a daughter cell. You inherit:\n"
        "- **Genome**: CORE.md, PHILOSOPHY.md, SWARM.md\n"
        "- **Epigenetics**: PRINCIPLES.md, INDEX.md, FRONTIER.md\n"
        f"- **Hub knowledge**: {lesson_count} lessons — lossy scaffold\n\n"
        "Parent's full phenotype (1200+ lessons, 127 tools) was NOT transferred.\n"
        "Grow your own lessons and experiments.\n\n"
        "## First session\n1. `python3 tools/orient.py`\n2. Read `beliefs/CORE.md`\n"
        "3. Pick a frontier or create your own\n4. Act, learn, write lessons\n"
        "5. `python3 tools/sync_state.py` before session end\n")


def _find_tool_deps():
    deps = set()
    import_pattern = re.compile(r"(?:from|import)\s+([\w.]+)")
    tools_dir = ROOT / "tools"
    for tool_path in CORE_TOOLS:
        src = ROOT / tool_path
        if not src.exists() or not src.suffix == ".py":
            continue
        text = src.read_text(errors="replace")
        for m in import_pattern.finditer(text):
            mod = m.group(1).split(".")[0]
            candidate = tools_dir / f"{mod}.py"
            if candidate.exists() and str(candidate.relative_to(ROOT)) not in CORE_TOOLS:
                deps.add(str(candidate.relative_to(ROOT)))
    return sorted(deps)


def main():
    parser = argparse.ArgumentParser(description="Extract compact genesis bundle")
    parser.add_argument("--out", default=str(ROOT / "workspace" / "genesis-bundle"))
    parser.add_argument("--top", type=int, default=100)
    parser.add_argument("--no-tools", action="store_true")
    parser.add_argument("--minimal", action="store_true", help="Skip reference + ISO atlas")
    parser.add_argument("--lean", action="store_true", help="Boot-only tools")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if not args.dry_run and os.path.exists(args.out):
        shutil.rmtree(args.out)
    manifest = extract_genesis(args.out, top_n=args.top, include_tools=not args.no_tools,
                               minimal=args.minimal, lean=args.lean, dry_run=args.dry_run)
    if args.json:
        print(json.dumps(manifest, indent=2))
    else:
        print(f"{'[DRY RUN] ' if args.dry_run else ''}Genesis bundle → {args.out}")
        print()
        for layer, info in manifest["layers"].items():
            kb = info["bytes"] / 1024
            print(f"  {layer:15s}  {len(info['files']):3d} files  {kb:7.1f} KB")
        print(f"  {'─' * 40}")
        print(f"  {'TOTAL':15s}  {manifest['total_files']:3d} files  "
              f"{manifest['total_bytes'] / 1024:7.1f} KB")
        print()
        if manifest.get("hub_lessons_top5"):
            print(f"  Hub lessons (top 5): {', '.join(manifest['hub_lessons_top5'])}")
        print(f"  Compression: {manifest['compression_ratio']} "
              f"(target <500KB for functional daughter)")

if __name__ == "__main__":
    main()
