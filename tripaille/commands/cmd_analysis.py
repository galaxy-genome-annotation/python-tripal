import click
from tripaille.commands.analysis.add_analysis import cli as func0
from tripaille.commands.analysis.get_analyses import cli as func1
from tripaille.commands.analysis.get_analysis_nodes import cli as func2
from tripaille.commands.analysis.load_blast import cli as func3
from tripaille.commands.analysis.load_fasta import cli as func4
from tripaille.commands.analysis.load_gff3 import cli as func5
from tripaille.commands.analysis.load_go import cli as func6
from tripaille.commands.analysis.load_interpro import cli as func7
from tripaille.commands.analysis.sync import cli as func8


@click.group()
def cli():
    pass


cli.add_command(func0)
cli.add_command(func1)
cli.add_command(func2)
cli.add_command(func3)
cli.add_command(func4)
cli.add_command(func5)
cli.add_command(func6)
cli.add_command(func7)
cli.add_command(func8)
