import click
from tripaille.cli import pass_context
from tripaille.decorators import custom_exception, list_output


@click.command('get_analysis_nodes')
@click.option(
    "--node",
    help="filter on node id",
    type=int
)
@pass_context
@custom_exception
@list_output
def cli(ctx, node=""):
    """Get analysis nodes

Output:

    Analysis node information
    """
    return ctx.gi.analysis.get_analysis_nodes(node=node)
