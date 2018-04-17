import click
from tripaille.cli import pass_context
from tripaille.decorators import custom_exception, str_output


@click.command('sync')
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
def cli(ctx, max_sync="", job_name="", no_wait=""):
    """Synchronize some phylotree

Output:

    status
    """
    return ctx.gi.phylogeny.sync(max_sync=max_sync, job_name=job_name, no_wait=no_wait)
