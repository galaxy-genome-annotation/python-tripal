import click
from tripaille.commands.biomaterial.add_biomaterial import cli as func0


@click.group()
def cli():
    """Manage Tripal Biomaterials"""
    pass


cli.add_command(func0)
