import click
from tripaille.cli import pass_context
from tripaille.decorators import custom_exception, list_output


@click.command('get_analyses_tripal')
@click.option(
    "--analysis_id",
    help="An analysis entity/node ID",
    type=int
)
@pass_context
@custom_exception
@list_output
def cli(ctx, analysis_id=""):
    """Get analysis entities

Output:

    Analysis entity/node information
    """
    return ctx.gi.analysis.get_analyses_tripal(analysis_id=analysis_id)
