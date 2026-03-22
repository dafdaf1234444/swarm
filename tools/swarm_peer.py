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
    python3 tools/swarm_peer.py remove <name>
"""

import json
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

        # Check for bulletins from them
        peer_bulletins = peer / "experiments" / "inter-swarm" / "bulletins"
        if peer_bulletins.exists():
            bfiles = list(peer_bulletins.glob("*.md"))
            print(f"  Bulletins: {len(bfiles)} files")
        else:
            print("  Bulletins: none (no inter-swarm dir)")


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
