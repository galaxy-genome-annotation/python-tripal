import click
from tripaille.commands.feature.delete_orphans import cli as func0
from tripaille.commands.feature.get_features import cli as func1
from tripaille.commands.feature.get_features_tripal import cli as func2
from tripaille.commands.feature.sync import cli as func3


@click.group()
def cli():
    """Manage Tripal features"""
    pass


cli.add_command(func0)
cli.add_command(func1)
cli.add_command(func2)
cli.add_command(func3)
