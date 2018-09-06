import click
from tripaille.cli import pass_context
from tripaille.decorators import custom_exception, dict_output


@click.command('add_biomaterial')
@click.argument("organism_id", type=str, help="Id of the associated organism")
@click.argument("file_path", type=str, help="Path to the biomaterial file")
@click.argument("file_type", type=click.Choice(['xml', 'tsv', 'csv']), help="Format of the biomaterial file : xml, tsv or csv")
@pass_context
@custom_exception
@dict_output
def cli(ctx, organism_id, file_path, file_type):
    """Add a new biomaterial to the database

Output:

    Biomatarial information
    """
    return ctx.gi.biomaterial.add_biomaterial(organism_id, file_path, file_type)
