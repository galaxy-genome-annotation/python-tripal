import click
from tripaille.cli import pass_context
from tripaille.decorators import custom_exception, list_output


@click.command('get_organism_nodes')
@click.option(
    "--node",
    help="filter on node id",
    type=int
)
@pass_context
@custom_exception
@list_output
def cli(ctx, node=""):
    """Get organism nodes

Output:

    Organism node information
    """
    return ctx.gi.organism.get_organism_nodes(node=node)
