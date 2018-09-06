import click
from tripaille.cli import pass_context
from tripaille.decorators import custom_exception, dict_output


@click.command('add_biomaterial')
@click.argument("organism_id", type=str)
@click.argument("file_path", type=str)
@click.argument("file_type", type=click.Choice(['xml', 'tsv', 'csv']))
@pass_context
@custom_exception
@dict_output
def cli(ctx, organism_id, file_path, file_type):
    """Add a new biomaterial to the database\n
   organism_id : Id of the associated organism\n
   file_path : Path to the biomaterial file\n
   file_type : Format of the biomaterial file : xml, tsv or csv\n
Output:

    Biomaterial information
    """
    return ctx.gi.biomaterial.add_biomaterial(organism_id, file_path, file_type)
