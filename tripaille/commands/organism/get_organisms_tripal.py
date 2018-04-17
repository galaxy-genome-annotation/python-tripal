import click
from tripaille.cli import pass_context
from tripaille.decorators import custom_exception, list_output


@click.command('get_organisms_tripal')
@click.option(
    "--organism_id",
    help="An organism entity ID",
    type=int
)
@pass_context
@custom_exception
@list_output
def cli(ctx, organism_id=""):
    """Get organism entities

Output:

    Organism entity information
    """
    return ctx.gi.organism.get_organisms_tripal(organism_id=organism_id)
