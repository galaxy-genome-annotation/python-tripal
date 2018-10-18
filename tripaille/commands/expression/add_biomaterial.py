import click
from tripaille.cli import pass_context
from tripaille.decorators import custom_exception, dict_output


@click.command('add_biomaterial')
@click.argument("organism_id", type=str)
@click.argument("file_path", type=str)
@click.argument("file_type", type=str)
@click.option(
    "--analysis_id",
    help="The id of the associated analysis. Required for TripalV3",
    type=str
)
@click.option(
    "--no_wait",
    help="Do not wait for job to complete",
    is_flag=True
)
@pass_context
@custom_exception
@dict_output
def cli(ctx, organism_id, file_path, file_type, analysis_id="", no_wait=False):
    """Add a new biomaterial to the database

Output:

    Job information
    """
    return ctx.gi.expression.add_biomaterial(organism_id, file_path, file_type, analysis_id=analysis_id, no_wait=no_wait)
