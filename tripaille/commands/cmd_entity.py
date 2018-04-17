import click
from tripaille.commands.entity.add_entity import cli as func0
from tripaille.commands.entity.get_entities import cli as func1
from tripaille.commands.entity.get_fields import cli as func2


@click.group()
def cli():
    """Manage any type of Tripal entities"""
    pass


cli.add_command(func0)
cli.add_command(func1)
cli.add_command(func2)
