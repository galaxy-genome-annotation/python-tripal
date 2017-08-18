import click
from tripaille.commands.organism.add_organism import cli as func0
from tripaille.commands.organism.get_organism_nodes import cli as func1
from tripaille.commands.organism.get_organisms import cli as func2
from tripaille.commands.organism.get_taxonomic_ranks import cli as func3
from tripaille.commands.organism.sync import cli as func4


@click.group()
def cli():
    pass


cli.add_command(func0)
cli.add_command(func1)
cli.add_command(func2)
cli.add_command(func3)
cli.add_command(func4)
