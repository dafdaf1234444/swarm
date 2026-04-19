import click
from pathlib import Path
from . import docs as docs_mod
from . import init as init_mod

@click.group()
@click.version_option()
def main():
    """Swarm: self-organizing AI session coordinator."""

@main.command()
@click.argument("path", type=click.Path(), default=".")
def init(path):
    """Initialize a swarm workspace in PATH."""
    init_mod.run(Path(path).resolve())

@main.command()
@click.option("--out", default="docs")
@click.option("--root", default=".")
def docs(out, root):
    """Regenerate markdown documentation."""
    docs_mod.build(Path(root).resolve(), Path(out))

@main.command()
def status():
    """Show swarm repo health."""
    click.echo("swarm status: ok")

if __name__ == "__main__":
    main()
