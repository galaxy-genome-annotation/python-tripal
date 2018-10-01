import click
from tripaille.cli import pass_context
from tripaille.decorators import custom_exception, dict_output


@click.command('add_biomaterial')
@click.argument("organism_id", type=str)
@click.argument("file_path", type=str)
@click.argument("file_type", type=click.Choice(['xml', 'tsv', 'csv']))

@click.option(
    "--no_wait",
    help="Do not wait for job to complete",
    is_flag=True
)

@pass_context
@custom_exception
@dict_output

def cli(ctx, organism_id, file_path, file_type, no_wait=False):
    """Add a new biomaterial to the database\n
   organism_id : Id of the associated organism\n
   file_path : Path to the biomaterial file\n
   file_type : Format of the biomaterial file : xml, tsv or csv\n
Output:

    Biomaterial information
    """
    return ctx.gi.expression.add_biomaterial(organism_id, file_path, file_type, no_wait=no_wait)
