import click
from tripaille.cli import pass_context
from tripaille.decorators import custom_exception, str_output


@click.command('delete_orphans')
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
def cli(ctx, job_name="", no_wait=""):
    """Delete orphans Drupal feature nodes

Output:

    status
    """
    return ctx.gi.feature.delete_orphans(job_name=job_name, no_wait=no_wait)
