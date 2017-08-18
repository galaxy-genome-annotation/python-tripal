import click
from tripaille.cli import pass_context
from tripaille.decorators import custom_exception, dict_output


@click.command('add_organism')
@click.argument("genus", type=str)
@click.argument("common", type=str)
@click.argument("abbr", type=str)
@click.option(
    "--species",
    help="The species of the organism",
    type=str
)
@click.option(
    "--comment",
    help="A comment / description",
    type=str
)
@click.option(
    "--infraspecific_rank",
    help="The type name of infraspecific name for any taxon below the rank of species. Must be one of ['subspecies', 'varietas', 'subvariety', 'forma', 'subforma']",
    type=str
)
@click.option(
    "--infraspecific_name",
    help="The infraspecific name for this organism.",
    type=str
)
@pass_context
@custom_exception
@dict_output
def cli(ctx, genus, common, abbr, species="", comment="", infraspecific_rank="", infraspecific_name=""):
    """Add a new organism to the database

Output:

    Organism information
    """
    return ctx.gi.organism.add_organism(genus, common, abbr, species=species, comment=comment, infraspecific_rank=infraspecific_rank, infraspecific_name=infraspecific_name)
