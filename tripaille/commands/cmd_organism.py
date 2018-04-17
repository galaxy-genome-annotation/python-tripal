import click
from tripaille.commands.organism.add_organism import cli as func0
from tripaille.commands.organism.delete_orphans import cli as func1
from tripaille.commands.organism.get_organisms import cli as func2
from tripaille.commands.organism.get_organisms_tripal import cli as func3
from tripaille.commands.organism.get_taxonomic_ranks import cli as func4
from tripaille.commands.organism.sync import cli as func5


@click.group()
def cli():
    """Manage Tripal organisms"""
    pass


cli.add_command(func0)
cli.add_command(func1)
cli.add_command(func2)
cli.add_command(func3)
cli.add_command(func4)
cli.add_command(func5)
