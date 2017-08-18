import click
from tripaille.cli import pass_context
from tripaille.decorators import custom_exception, str_output


@click.command('populate_mviews')
@click.option(
    "--name",
    help="filter on mview name",
    type=str
)
@click.option(
    "--no_wait",
    help="Do not wait for job to complete",
    is_flag=True
)
@pass_context
@custom_exception
@str_output
def cli(ctx, name="", no_wait=""):
    """Populate materialized views

Output:

    Loading information
    """
    return ctx.gi.db.populate_mviews(name=name, no_wait=no_wait)
