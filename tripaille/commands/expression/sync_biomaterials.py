import click
from tripaille.cli import pass_context
from tripaille.decorators import custom_exception, dict_output


@click.command('sync_biomaterials')

@click.option(
"--ids",
    help="List of ids of biomaterials to be synced (default: all)",
    type=str,
    multiple=True
)

@click.option(
"--max-sync",
    help="Maximum number of features to sync (default: all)",
    type=str
)

@click.option(
"--job_name",
    help="Name of the job. Default to 'Sync Biomaterials'",
    type=str
)

@click.option(
    "--no_wait",
    help="Do not wait for job to complete",
    type=bool
)

@pass_context
@custom_exception
@dict_output

def cli(ctx, ids=[], organism_id="", max_sync="", job_name="", no_wait=False):
    """Sync Biomaterials with Tripal\n
Output:

    status
    """
    return ctx.gi.expression.sync_biomaterials(ids=ids, max_sync=max_sync, job_name=job_name, no_wait=no_wait)
