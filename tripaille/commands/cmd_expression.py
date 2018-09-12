import click
from tripaille.commands.expression.add_expression import cli as func0
from tripaille.commands.expression.add_biomaterial import cli as func1

@click.group()
def cli():
    """Manage Tripal Expression"""
    pass


cli.add_command(func0)
cli.add_command(func1)
