import click
from tripaille.cli import pass_context
from tripaille.decorators import custom_exception, list_output


@click.command('get_dbs')
@click.option(
    "--db_id",
    help="A db ID",
    type=str
)
@click.option(
    "--name",
    help="filter on db name",
    type=str
)
@pass_context
@custom_exception
@list_output
def cli(ctx, db_id="", name=""):
    """Get all dbs

Output:

    Dbs information
    """
    return ctx.gi.db.get_dbs(db_id=db_id, name=name)
