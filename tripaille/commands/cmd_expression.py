import click
from tripaille.commands.expression.add_expression import cli as func0


@click.group()
def cli():
    """Manage Tripal Expression"""
    pass


cli.add_command(func0)
