import click
from tripaille.cli import pass_context
from tripaille.decorators import custom_exception, str_output


@click.command('sync')
@click.option(
    "--organism",
    help="Common name of the organism to sync",
    type=str
)
@click.option(
    "--organism_id",
    help="ID of the organism to sync",
    type=str
)
@click.option(
    "--max_sync",
    help="Maximum number of features to sync (default: all)",
    type=str
)
@click.option(
    "--types",
    help="List of types of records to be synced (e.g. gene mRNA, default: all)",
    type=str,
    multiple=True
)
@click.option(
    "--ids",
    help="List of names of records to be synced (e.g. gene0001, default: all)",
    type=str,
    multiple=True
)
@click.option(
    "--job_name",
    help="Name of the job",
    type=str
)
@click.option(
    "--no_wait",
    help="Return immediately without waiting for job completion",
    is_flag=True
)
@pass_context
@custom_exception
@str_output
def cli(ctx, organism="", organism_id="", max_sync="", types=None, ids=None, job_name="", no_wait=""):
    """Synchronize some features

Output:

    status
    """
    return ctx.gi.feature.sync(organism=organism, organism_id=organism_id, max_sync=max_sync, types=types, ids=ids, job_name=job_name, no_wait=no_wait)
