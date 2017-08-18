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
def cli(ctx, organism="", organism_id="", job_name="", no_wait=""):
    """Synchronize an organism

Output:

    status
    """
    return ctx.gi.organism.sync(organism=organism, organism_id=organism_id, job_name=job_name, no_wait=no_wait)
