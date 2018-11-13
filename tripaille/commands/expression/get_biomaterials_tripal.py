import click
from tripaille.cli import pass_context
from tripaille.decorators import custom_exception, list_output


@click.command('get_biomaterials_tripal')
@click.option(
    "--biomaterial_id",
    help="A biomaterial entity ID",
    type=int
)
@pass_context
@custom_exception
@list_output
def cli(ctx, biomaterial_id=""):
    """Get Biomaterial entities

Output:

    Organism entity information
    """
    return ctx.gi.expression.get_biomaterials_tripal(biomaterial_id=biomaterial_id)
