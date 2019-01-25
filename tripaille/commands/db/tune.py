import click
from tripaille.cli import pass_context
from tripaille.decorators import custom_exception, dict_output


@click.command('tune')
@pass_context
@custom_exception
@dict_output
def cli(ctx):
    """Tune indices for website indexation

Output:

    "Status"
    """
    return ctx.gi.db.tune()
