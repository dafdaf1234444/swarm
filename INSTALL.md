## Install (user-level, no admin)

```bash
# One-liner:
curl -sSL https://raw.githubusercontent.com/dafdaf1234444/swarm/master/scripts/bootstrap.sh | bash
```

Or manually:
```bash
python3 -m pip install --user pipx
pipx install git+https://github.com/dafdaf1234444/swarm.git
swarm --help
```

Upgrade: `pipx upgrade swarm`
Uninstall: `pipx uninstall swarm`
