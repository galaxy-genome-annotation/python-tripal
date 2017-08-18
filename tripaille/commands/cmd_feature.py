import click
from tripaille.commands.feature.sync import cli as func0


@click.group()
def cli():
    pass


cli.add_command(func0)
