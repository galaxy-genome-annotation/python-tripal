import click
from tripaille.cli import pass_context
from tripaille.decorators import custom_exception, str_output


@click.command('sync_biomaterials')
@click.option(
    "--ids",
    help="JSON list of ids of biomaterials to be synced (default: all)",
    type=str
)
@click.option(
    "--max_sync",
    help="Maximum number of features to sync (default: all)",
    type=str
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
def cli(ctx, ids=None, max_sync="", job_name="", no_wait=False):
    """Synchronize some biomaterials

Output:

    status
    """
    return ctx.gi.expression.sync_biomaterials(ids=ids, max_sync=max_sync, job_name=job_name, no_wait=no_wait)
