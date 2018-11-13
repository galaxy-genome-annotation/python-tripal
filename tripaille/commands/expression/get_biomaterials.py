import click
from tripaille.cli import pass_context
from tripaille.decorators import custom_exception, dict_output


@click.command('get_biomaterials')
@click.option(
    "--biomaterial_name",
    help="Limit query to the selected biomaterial",
    type=str
)
@click.option(
    "--provider_id",
    help="Limit query to the selected provider",
    type=str
)
@click.option(
    "--biomaterial_id",
    help="Limit query to the selected biomaterial",
    type=str
)
@click.option(
    "--organism_id",
    help="Limit query to the selected organism",
    type=str
)
@click.option(
    "--dbxref_id",
    help="Limit query to the selected ref",
    type=str
)
@pass_context
@custom_exception
@dict_output
def cli(ctx, biomaterial_name="", provider_id="", biomaterial_id="", organism_id="", dbxref_id=""):
    """List biomaterials in the database

Output:

    Biomaterial list
    """
    return ctx.gi.expression.get_biomaterials(biomaterial_name=biomaterial_name, provider_id=provider_id, biomaterial_id=biomaterial_id, organism_id=organism_id, dbxref_id=dbxref_id)
