import click
from tripaille.cli import pass_context
from tripaille.decorators import custom_exception, dict_output


@click.command('tune')
@pass_context
@custom_exception
@dict_output
def cli(ctx):
    """Setup default entity index priority for whole website indexing

Output:

    "Status"
    """
    return ctx.gi.db.tune()
