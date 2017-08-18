import click
from tripaille.cli import pass_context
from tripaille.decorators import custom_exception, list_output


@click.command('get_organisms')
@click.option(
    "--organism_id",
    help="An organism ID",
    type=str
)
@click.option(
    "--genus",
    help="The genus of the organism",
    type=str
)
@click.option(
    "--species",
    help="The species of the organism",
    type=str
)
@click.option(
    "--common",
    help="The common name of the organism",
    type=str
)
@click.option(
    "--abbr",
    help="The abbreviation of the organism",
    type=str
)
@click.option(
    "--comment",
    help="A comment / description",
    type=str
)
@pass_context
@custom_exception
@list_output
def cli(ctx, organism_id="", genus="", species="", common="", abbr="", comment=""):
    """Get organisms

Output:

    Organism information
    """
    return ctx.gi.organism.get_organisms(organism_id=organism_id, genus=genus, species=species, common=common, abbr=abbr, comment=comment)
