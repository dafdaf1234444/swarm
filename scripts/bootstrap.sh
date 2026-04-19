#!/usr/bin/env bash
set -euo pipefail
SWARM_REPO="${SWARM_REPO:-git+https://github.com/dafdaf1234444/swarm.git}"
command -v python3 >/dev/null || { echo "python3 required"; exit 1; }
if ! command -v pipx >/dev/null; then
  python3 -m pip install --user pipx
  python3 -m pipx ensurepath
  export PATH="$HOME/.local/bin:$PATH"
fi
command -v swarm >/dev/null || pipx install "$SWARM_REPO"
swarm init "$(pwd)"
