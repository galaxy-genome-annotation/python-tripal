import click
from tripaille.cli import pass_context
from tripaille.decorators import custom_exception, dict_output


@click.command('get_biomaterials')

@click.option(
"--provider_id",
    help="Limit query to a provider id",
    type=str
)

@click.option(
"--biomaterial_id",
    help="Limit query to a biomaterial id",
    type=str
)

@click.option(
"--taxon_id",
    help="Limit query to a taxon id",
    type=str
)

@click.option(
"--dbxref_id",
    help="Limit query to a dbxref id",
    type=str
)



@pass_context
@custom_exception
@dict_output

def cli(ctx, provider_id="", biomaterial_id="", taxon_id="", dbxref_id=""):
    """List Biomaterials in DB\n
Output:

    status
    """
    return ctx.gi.expression.get_biomaterials(biomaterial_id=biomaterial_id, provider_id=provider_id, taxon_id=taxon_id, dbxref_id=dbxref_id)
