import click
from tripaille.commands.phylogeny.sync import cli as func0


@click.group()
def cli():
    """Manage Tripal phylogeny"""
    pass


cli.add_command(func0)
