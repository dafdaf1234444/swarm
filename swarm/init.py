from pathlib import Path
SEED_DIRS = ["lessons", "principles", "questions", "sessions"]
def run(root: Path):
    root.mkdir(parents=True, exist_ok=True)
    for d in SEED_DIRS:
        (root / d).mkdir(exist_ok=True)
        (root / d / ".gitkeep").touch()
    r = root / "SWARM.md"
    if not r.exists():
        r.write_text("# Swarm workspace\n\nInitialized by `swarm init`.\n")
    print(f"Initialized swarm workspace at {root}")
