import click
from tripaille.cli import pass_context
from tripaille.decorators import custom_exception, list_output


@click.command('get_mviews')
@click.option(
    "--name",
    help="filter on mview name",
    type=str
)
@pass_context
@custom_exception
@list_output
def cli(ctx, name=""):
    """Get all materialized views

Output:

    materialized views information
    """
    return ctx.gi.db.get_mviews(name=name)
