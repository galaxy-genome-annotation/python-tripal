import click
from tripaille.commands.expression.add_biomaterial import cli as func0
from tripaille.commands.expression.add_expression import cli as func1
from tripaille.commands.expression.delete_biomaterials import cli as func2
from tripaille.commands.expression.get_biomaterials import cli as func3
from tripaille.commands.expression.get_biomaterials_tripal import cli as func4
from tripaille.commands.expression.sync_biomaterials import cli as func5


@click.group()
def cli():
    """Manage Tripal expressions"""
    pass


cli.add_command(func0)
cli.add_command(func1)
cli.add_command(func2)
cli.add_command(func3)
cli.add_command(func4)
cli.add_command(func5)
