import click
from tripaille.cli import pass_context
from tripaille.decorators import custom_exception, list_output


@click.command('get_bundles')
@pass_context
@custom_exception
@list_output
def cli(ctx):
    """Get the list of tripal bundles

Output:

    Bundles information
    """
    return ctx.gi.entity.get_bundles()
