#!/usr/bin/env python3
"""
swarm_peer.py — Peer swarm discovery and coordination (GAP-1, F-SWARMER2).

Closes the inter-swarm coordination gap: swarms can register peers,
check compatibility, and exchange state via git remotes.

Usage:
    python3 tools/swarm_peer.py register <name> <git-url> [--note "..."]
    python3 tools/swarm_peer.py list
    python3 tools/swarm_peer.py check <name>          # run merge_compatibility against peer
    python3 tools/swarm_peer.py fetch <name>           # shallow-clone peer, read their state
    python3 tools/swarm_peer.py exchange <name>        # post bulletin + fetch peer bulletins
    python3 tools/swarm_peer.py sync <name>             # bidirectional state diff + merge report
    python3 tools/swarm_peer.py remove <name>
"""

import json
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PEERS_FILE = ROOT / "workspace" / "swarm-peers.json"
BULLETINS_DIR = ROOT / "experiments" / "inter-swarm" / "bulletins"


def load_peers() -> dict:
    if PEERS_FILE.exists():
        return json.loads(PEERS_FILE.read_text())
    return {"schema": "swarm-peers-v1", "peers": {}}


def save_peers(data: dict) -> None:
    PEERS_FILE.write_text(json.dumps(data, indent=2) + "\n")


def cmd_register(args: list[str]) -> None:
    if len(args) < 2:
        print("Usage: register <name> <git-url> [--note '...']")
        sys.exit(1)
    name, url = args[0], args[1]
    note = ""
    if "--note" in args:
        idx = args.index("--note")
        if idx + 1 < len(args):
            note = args[idx + 1]

    peers = load_peers()
    now = datetime.now(timezone.utc).isoformat()
    peers["peers"][name] = {
        "url": url,
        "registered": now,
        "last_check": None,
        "compatibility": None,
        "note": note,
    }
    save_peers(peers)
    print(f"Registered peer '{name}' at {url}")


def cmd_list(_args: list[str]) -> None:
    peers = load_peers()
    if not peers["peers"]:
        print("No peers registered. Use: swarm_peer.py register <name> <git-url>")
        return
    print(f"{'Name':<20} {'Compat':<12} {'Last Check':<22} URL")
    print("-" * 80)
    for name, info in sorted(peers["peers"].items()):
        compat = info.get("compatibility") or "unknown"
        last = (info.get("last_check") or "never")[:19]
        print(f"{name:<20} {compat:<12} {last:<22} {info['url']}")


def cmd_check(args: list[str]) -> None:
    if not args:
        print("Usage: check <name>")
        sys.exit(1)
    name = args[0]
    peers = load_peers()
    if name not in peers["peers"]:
        print(f"Unknown peer '{name}'. Register first.")
        sys.exit(1)

    url = peers["peers"][name]["url"]
    print(f"Checking compatibility with '{name}' ({url})...")

    with tempfile.TemporaryDirectory(prefix="swarm-peer-") as tmpdir:
        # Shallow clone peer repo
        result = subprocess.run(
            ["git", "clone", "--depth", "1", "--single-branch", url, tmpdir],
            capture_output=True, text=True, timeout=60,
        )
        if result.returncode != 0:
            print(f"FAIL: Could not clone {url}")
            print(result.stderr[:500])
            return

        # Check if it's a swarm
        peer_swarm = Path(tmpdir) / "SWARM.md"
        if not peer_swarm.exists():
            print(f"NOT A SWARM: {url} has no SWARM.md")
            peers["peers"][name]["compatibility"] = "not-swarm"
            peers["peers"][name]["last_check"] = datetime.now(timezone.utc).isoformat()
            save_peers(peers)
            return

        # Run merge_compatibility.py
        mc_path = ROOT / "tools" / "merge_compatibility.py"
        result = subprocess.run(
            [sys.executable, str(mc_path), tmpdir, "--json"],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode != 0:
            print(f"merge_compatibility.py failed: {result.stderr[:300]}")
            return

        try:
            compat = json.loads(result.stdout)
            zone = compat.get("zone", "unknown")
            distance = compat.get("overall_distance", -1)
        except (json.JSONDecodeError, KeyError):
            zone = "parse-error"
            distance = -1

        now = datetime.now(timezone.utc).isoformat()
        peers["peers"][name]["compatibility"] = zone
        peers["peers"][name]["distance"] = distance
        peers["peers"][name]["last_check"] = now
        save_peers(peers)

        print(f"Zone: {zone} | Distance: {distance:.3f}")
        if zone == "HETEROSIS":
            print("  OPTIMAL for mutual swarming")
        elif zone == "CAUTIOUS":
            print("  Viable with careful arbitration")
        elif zone == "INCOMPATIBLE":
            print("  NOT viable — core axioms contradict")
        elif zone == "INBREEDING":
            print("  Too similar — low hybrid vigor expected")


def cmd_fetch(args: list[str]) -> None:
    if not args:
        print("Usage: fetch <name>")
        sys.exit(1)
    name = args[0]
    peers = load_peers()
    if name not in peers["peers"]:
        print(f"Unknown peer '{name}'.")
        sys.exit(1)

    url = peers["peers"][name]["url"]
    print(f"Fetching state from '{name}' ({url})...")

    with tempfile.TemporaryDirectory(prefix="swarm-peer-") as tmpdir:
        result = subprocess.run(
            ["git", "clone", "--depth", "1", "--single-branch", url, tmpdir],
            capture_output=True, text=True, timeout=60,
        )
        if result.returncode != 0:
            print(f"FAIL: Could not clone {url}")
            return

        peer = Path(tmpdir)
        # Read key state files
        for rel in [
            "beliefs/PHILOSOPHY.md", "beliefs/CORE.md", "memory/INDEX.md",
            "tasks/FRONTIER.md", "tasks/NEXT.md",
        ]:
            p = peer / rel
            if p.exists():
                lines = p.read_text(errors="ignore").split("\n")
                header = lines[0] if lines else "(empty)"
                count = len(lines)
                print(f"  {rel}: {count}L — {header[:80]}")
            else:
                print(f"  {rel}: MISSING")

        # Count lessons and principles
        lessons = list((peer / "memory" / "lessons").glob("L-*.md")) if (peer / "memory" / "lessons").exists() else []
        tools_dir = list((peer / "tools").glob("*.py")) if (peer / "tools").exists() else []
        print(f"  Lessons: {len(lessons)} | Tools: {len(tools_dir)}")

        # Extract peer's active frontiers
        peer_frontier = peer / "tasks" / "FRONTIER.md"
        if peer_frontier.exists():
            ftext = peer_frontier.read_text(errors="ignore")
            resolved_idx = ftext.find("\n## Resolved")
            if resolved_idx > 0:
                ftext = ftext[:resolved_idx]
            peer_frontiers = re.findall(r"^- \*\*(\S+)\*\*:", ftext, re.MULTILINE)
            print(f"  Active frontiers: {len(peer_frontiers)} ({', '.join(peer_frontiers[:5])}{'...' if len(peer_frontiers) > 5 else ''})")
        else:
            print("  Active frontiers: MISSING (no FRONTIER.md)")

        # Check for bulletins from them
        peer_bulletins = peer / "experiments" / "inter-swarm" / "bulletins"
        if peer_bulletins.exists():
            bfiles = list(peer_bulletins.glob("*.md"))
            print(f"  Bulletins: {len(bfiles)} files")
        else:
            print("  Bulletins: none (no inter-swarm dir)")


def _extract_local_frontiers() -> list[str]:
    """Extract active frontier IDs + summaries from local FRONTIER.md."""
    frontier_path = ROOT / "tasks" / "FRONTIER.md"
    if not frontier_path.exists():
        return []
    text = frontier_path.read_text()
    resolved_idx = text.find("\n## Resolved")
    if resolved_idx > 0:
        text = text[:resolved_idx]
    frontiers = []
    for m in re.finditer(r"^- \*\*(\S+)\*\*:\s*(.+?)$", text, re.MULTILINE):
        frontiers.append(f"{m.group(1)}: {m.group(2).strip()[:120]}")
    return frontiers


def cmd_exchange(args: list[str]) -> None:
    if not args:
        print("Usage: exchange <name>")
        sys.exit(1)
    name = args[0]
    peers = load_peers()
    if name not in peers["peers"]:
        print(f"Unknown peer '{name}'.")
        sys.exit(1)

    url = peers["peers"][name]["url"]

    # 1. Post a bulletin about ourselves
    our_index = ROOT / "memory" / "INDEX.md"
    state_line = "unknown"
    if our_index.exists():
        for line in our_index.read_text().split("\n"):
            if "lessons" in line.lower() and "principles" in line.lower():
                state_line = line.strip()[:100]
                break

    # Extract our active frontiers for the exchange
    frontier_lines = _extract_local_frontiers()
    frontier_block = "\n".join(f"  - {f}" for f in frontier_lines) if frontier_lines else "(none)"

    BULLETINS_DIR.mkdir(parents=True, exist_ok=True)
    our_name = ROOT.name  # repo directory name as swarm identity
    bulletin_file = BULLETINS_DIR / f"peer-exchange-{name}.md"
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    bulletin_content = (
        f"# Bulletin from: {our_name}\n"
        f"Date: {now}\n"
        f"Type: sibling-sync\n"
        f"Trust-Tier: T3\n\n"
        f"## Content\n"
        f"Peer exchange initiated with {name} ({url}).\n"
        f"Our state: {state_line}\n\n"
        f"## Active Frontiers ({len(frontier_lines)})\n"
        f"{frontier_block}\n\n"
        f"## Evidence\n"
        f"Automated peer exchange via swarm_peer.py\n---\n"
    )

    # Append (don't overwrite)
    with open(bulletin_file, "a") as f:
        f.write(bulletin_content)
    print(f"Posted exchange bulletin: {bulletin_file.name}")

    # 2. Fetch peer bulletins
    print(f"Fetching bulletins from '{name}'...")
    with tempfile.TemporaryDirectory(prefix="swarm-peer-") as tmpdir:
        result = subprocess.run(
            ["git", "clone", "--depth", "1", "--single-branch", url, tmpdir],
            capture_output=True, text=True, timeout=60,
        )
        if result.returncode != 0:
            print(f"FAIL: Could not clone {url}")
            return

        peer_bulletins = Path(tmpdir) / "experiments" / "inter-swarm" / "bulletins"
        if not peer_bulletins.exists():
            print("  Peer has no bulletins directory")
            return

        imported = 0
        for bfile in sorted(peer_bulletins.glob("*.md")):
            dest = BULLETINS_DIR / f"from-{name}-{bfile.name}"
            if not dest.exists():
                dest.write_text(bfile.read_text(errors="ignore"))
                imported += 1

        print(f"  Imported {imported} new bulletins from {name}")

    now_iso = datetime.now(timezone.utc).isoformat()
    peers["peers"][name]["last_exchange"] = now_iso
    save_peers(peers)


def _compute_state_fingerprint(root: Path) -> dict:
    """Extract structured state fingerprint from a swarm repo root."""
    fp: dict = {"frontiers": [], "beliefs": [], "phils": [], "lessons": [],
                "lesson_count": 0, "principle_count": 0, "tool_count": 0,
                "session": "unknown", "identity": "unknown"}

    # Identity (repo name)
    fp["identity"] = root.name

    # Session from NEXT.md or INDEX.md header
    for rel in ["tasks/NEXT.md", "memory/INDEX.md"]:
        p = root / rel
        if p.exists():
            header = p.read_text(errors="ignore").split("\n")[0]
            m = re.search(r"S(\d+)", header)
            if m:
                fp["session"] = f"S{m.group(1)}"
                break

    # Active frontiers (IDs only)
    frontier_path = root / "tasks" / "FRONTIER.md"
    if frontier_path.exists():
        text = frontier_path.read_text(errors="ignore")
        resolved_idx = text.find("\n## Resolved")
        if resolved_idx > 0:
            text = text[:resolved_idx]
        for m_f in re.finditer(r"^- \*\*(\S+)\*\*:", text, re.MULTILINE):
            fid = m_f.group(1)
            if not fid.startswith("~~"):
                fp["frontiers"].append(fid)

    # Beliefs from DEPS.md — format is B1, B2, B-EVAL1, etc.
    deps_path = root / "beliefs" / "DEPS.md"
    if deps_path.exists():
        for m_b in re.finditer(r"\b(B-?\w+\d+)\b", deps_path.read_text(errors="ignore")):
            bid = m_b.group(1)
            if bid.startswith("B") and bid not in fp["beliefs"]:
                fp["beliefs"].append(bid)

    # Philosophy claims — format is **[PHIL-N]**
    phil_path = root / "beliefs" / "PHILOSOPHY.md"
    if phil_path.exists():
        for m_p in re.finditer(r"\*\*\[PHIL-(\d+)\]\*\*", phil_path.read_text(errors="ignore")):
            fp["phils"].append(f"PHIL-{m_p.group(1)}")

    # Lesson IDs (last 50 by filename sort for recent comparison)
    lessons_dir = root / "memory" / "lessons"
    if lessons_dir.exists():
        all_lessons = sorted(lessons_dir.glob("L-*.md"))
        fp["lesson_count"] = len(all_lessons)
        fp["lessons"] = [lf.stem for lf in all_lessons[-50:]]

    # Principle count — format is P-NNN (plain, not bold) in themed sections
    principles_path = root / "memory" / "PRINCIPLES.md"
    if principles_path.exists():
        text_p = principles_path.read_text(errors="ignore")
        fp["principle_count"] = len(set(re.findall(r"\bP-\d{3}\b", text_p)))

    # Tool count
    tools_dir = root / "tools"
    if tools_dir.exists():
        fp["tool_count"] = len(list(tools_dir.glob("*.py")))

    return fp


def _diff_fingerprints(local: dict, peer: dict) -> dict:
    """Compute bidirectional diff between two state fingerprints."""
    diff: dict = {}

    for key in ["frontiers", "beliefs", "phils", "lessons"]:
        local_set = set(local.get(key, []))
        peer_set = set(peer.get(key, []))
        diff[f"{key}_only_local"] = sorted(local_set - peer_set)
        diff[f"{key}_only_peer"] = sorted(peer_set - local_set)
        diff[f"{key}_shared"] = sorted(local_set & peer_set)

    # Numeric comparisons
    for key in ["lesson_count", "principle_count", "tool_count"]:
        diff[f"{key}_local"] = local.get(key, 0)
        diff[f"{key}_peer"] = peer.get(key, 0)
        diff[f"{key}_delta"] = local.get(key, 0) - peer.get(key, 0)

    diff["local_session"] = local.get("session", "unknown")
    diff["peer_session"] = peer.get("session", "unknown")

    return diff


def cmd_sync(args: list[str]) -> None:
    """Bidirectional sync: compute state diff with a peer, generate sync report."""
    if not args:
        print("Usage: sync <name> [--post-bulletin]")
        sys.exit(1)
    name = args[0]
    post_bulletin = "--post-bulletin" in args

    peers = load_peers()
    if name not in peers["peers"]:
        print(f"Unknown peer '{name}'. Register first.")
        sys.exit(1)

    url = peers["peers"][name]["url"]
    print(f"=== BIDIRECTIONAL SYNC: {name} ({url}) ===\n")

    # 1. Compute local fingerprint
    local_fp = _compute_state_fingerprint(ROOT)
    print(f"Local state ({local_fp['identity']}): {local_fp['session']} | "
          f"{local_fp['lesson_count']}L {local_fp['principle_count']}P "
          f"{len(local_fp['frontiers'])}F {len(local_fp['phils'])}PHIL "
          f"{local_fp['tool_count']} tools")

    # 2. Clone peer and compute their fingerprint
    with tempfile.TemporaryDirectory(prefix="swarm-sync-") as tmpdir:
        result = subprocess.run(
            ["git", "clone", "--depth", "1", "--single-branch", url, tmpdir],
            capture_output=True, text=True, timeout=60,
        )
        if result.returncode != 0:
            print(f"FAIL: Could not clone {url}")
            print(result.stderr[:300])
            return

        peer_root = Path(tmpdir)
        if not (peer_root / "SWARM.md").exists():
            print(f"NOT A SWARM: {url} has no SWARM.md")
            return

        peer_fp = _compute_state_fingerprint(peer_root)
        print(f"Peer state ({peer_fp['identity']}): {peer_fp['session']} | "
              f"{peer_fp['lesson_count']}L {peer_fp['principle_count']}P "
              f"{len(peer_fp['frontiers'])}F {len(peer_fp['phils'])}PHIL "
              f"{peer_fp['tool_count']} tools")

        # 3. Compute diff
        diff = _diff_fingerprints(local_fp, peer_fp)

        print(f"\n--- STATE DIFF ---")
        print(f"Sessions: local={diff['local_session']} peer={diff['peer_session']}")
        print(f"Lessons: local={diff['lesson_count_local']} peer={diff['lesson_count_peer']} "
              f"(delta={diff['lesson_count_delta']:+d})")
        print(f"Principles: local={diff['principle_count_local']} peer={diff['principle_count_peer']} "
              f"(delta={diff['principle_count_delta']:+d})")
        print(f"Tools: local={diff['tool_count_local']} peer={diff['tool_count_peer']} "
              f"(delta={diff['tool_count_delta']:+d})")

        # Frontiers
        if diff["frontiers_only_local"]:
            print(f"\nFrontiers only LOCAL ({len(diff['frontiers_only_local'])}):")
            for f_id in diff["frontiers_only_local"][:10]:
                print(f"  + {f_id}")
        if diff["frontiers_only_peer"]:
            print(f"\nFrontiers only PEER ({len(diff['frontiers_only_peer'])}):")
            for f_id in diff["frontiers_only_peer"][:10]:
                print(f"  - {f_id}")
        if diff["frontiers_shared"]:
            print(f"\nShared frontiers: {len(diff['frontiers_shared'])}")

        # Philosophy claims
        if diff["phils_only_local"]:
            print(f"\nPHIL claims only LOCAL ({len(diff['phils_only_local'])}): "
                  f"{', '.join(diff['phils_only_local'][:10])}")
        if diff["phils_only_peer"]:
            print(f"\nPHIL claims only PEER ({len(diff['phils_only_peer'])}): "
                  f"{', '.join(diff['phils_only_peer'][:10])}")

        # Recent lessons unique to each
        if diff["lessons_only_peer"]:
            print(f"\nRecent lessons only PEER ({len(diff['lessons_only_peer'])}):")
            for lid in diff["lessons_only_peer"][:10]:
                # Try to read the lesson title from peer
                lpath = peer_root / "memory" / "lessons" / f"{lid}.md"
                title = lid
                if lpath.exists():
                    first_line = lpath.read_text(errors="ignore").split("\n")[0]
                    title = first_line.lstrip("# ").strip()[:100]
                print(f"  → {title}")

        # 4. Sync report
        sync_report = {
            "schema": "swarm-sync-v1",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "local": {"identity": local_fp["identity"], "session": local_fp["session"],
                      "lessons": local_fp["lesson_count"], "tools": local_fp["tool_count"]},
            "peer": {"identity": peer_fp["identity"], "name": name, "url": url,
                     "session": peer_fp["session"], "lessons": peer_fp["lesson_count"],
                     "tools": peer_fp["tool_count"]},
            "diff": {
                "frontiers_only_local": diff["frontiers_only_local"],
                "frontiers_only_peer": diff["frontiers_only_peer"],
                "frontiers_shared": len(diff["frontiers_shared"]),
                "phils_only_local": diff["phils_only_local"],
                "phils_only_peer": diff["phils_only_peer"],
                "lessons_only_peer": diff["lessons_only_peer"][:20],
                "lesson_delta": diff["lesson_count_delta"],
                "principle_delta": diff["principle_count_delta"],
                "tool_delta": diff["tool_count_delta"],
            },
            "merge_candidates": [],
        }

        # Identify merge candidates: peer lessons we don't have
        for lid in diff["lessons_only_peer"][:10]:
            lpath = peer_root / "memory" / "lessons" / f"{lid}.md"
            if lpath.exists():
                text = lpath.read_text(errors="ignore")
                # Extract domain and Sharpe if present
                from lesson_header import parse_domain_field
                _doms = parse_domain_field(text[:500])
                sharpe_m = re.search(r"Sharpe:\s*(\d+)", text)
                sync_report["merge_candidates"].append({
                    "id": lid,
                    "domain": _doms[0] if _doms else "unknown",
                    "sharpe": int(sharpe_m.group(1)) if sharpe_m else 0,
                    "first_line": text.split("\n")[0].lstrip("# ").strip()[:100],
                })

        # Save sync report
        sync_dir = ROOT / "workspace" / "sync-reports"
        sync_dir.mkdir(parents=True, exist_ok=True)
        report_path = sync_dir / f"sync-{name}-{datetime.now(timezone.utc).strftime('%Y%m%d')}.json"
        report_path.write_text(json.dumps(sync_report, indent=2) + "\n")
        print(f"\nSync report saved: {report_path.relative_to(ROOT)}")

        # 5. Post bulletin if requested
        if post_bulletin:
            BULLETINS_DIR.mkdir(parents=True, exist_ok=True)
            our_name = ROOT.name
            bulletin_file = BULLETINS_DIR / f"sync-{name}.md"
            now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            content = (
                f"\n---\n"
                f"# Bulletin from: {our_name}\n"
                f"Date: {now}\n"
                f"Type: sibling-sync\n"
                f"Trust-Tier: T3\n\n"
                f"## Content\n"
                f"Bidirectional sync with {name}.\n"
                f"Local: {local_fp['session']} {local_fp['lesson_count']}L | "
                f"Peer: {peer_fp['session']} {peer_fp['lesson_count']}L\n"
                f"Unique local frontiers: {len(diff['frontiers_only_local'])}\n"
                f"Unique peer frontiers: {len(diff['frontiers_only_peer'])}\n"
                f"Merge candidates: {len(sync_report['merge_candidates'])}\n\n"
                f"## Evidence\n"
                f"Automated bidirectional sync via swarm_peer.py sync\n"
            )
            with open(bulletin_file, "a") as bf:
                bf.write(content)
            print(f"Sync bulletin posted: {bulletin_file.name}")

        # Update peer record
        now_iso = datetime.now(timezone.utc).isoformat()
        peers["peers"][name]["last_sync"] = now_iso
        peers["peers"][name]["peer_session"] = peer_fp["session"]
        peers["peers"][name]["peer_lessons"] = peer_fp["lesson_count"]
        save_peers(peers)

    print(f"\n✓ Sync complete. Merge candidates: {len(sync_report['merge_candidates'])}")


def cmd_remove(args: list[str]) -> None:
    if not args:
        print("Usage: remove <name>")
        sys.exit(1)
    name = args[0]
    peers = load_peers()
    if name in peers["peers"]:
        del peers["peers"][name]
        save_peers(peers)
        print(f"Removed peer '{name}'")
    else:
        print(f"Peer '{name}' not found")


COMMANDS = {
    "register": cmd_register,
    "list": cmd_list,
    "check": cmd_check,
    "fetch": cmd_fetch,
    "exchange": cmd_exchange,
    "sync": cmd_sync,
    "remove": cmd_remove,
}


def main() -> None:
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print("swarm_peer.py — Peer swarm discovery and coordination")
        print(f"Commands: {', '.join(COMMANDS)}")
        print("Usage: python3 tools/swarm_peer.py <command> [args...]")
        sys.exit(1)
    COMMANDS[sys.argv[1]](sys.argv[2:])


if __name__ == "__main__":
    main()
