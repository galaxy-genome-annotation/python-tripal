import click
from tripaille.cli import pass_context
from tripaille.decorators import custom_exception, str_output


@click.command('publish')
@click.option(
    "--types",
    help="List of entity types to be published (e.g. Gene mRNA, default: all)",
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
def cli(ctx, types=None, job_name="", no_wait=""):
    """Publish entities (Tripal 3 only)

Output:

    status
    """
    return ctx.gi.entity.publish(types=types, job_name=job_name, no_wait=no_wait)
