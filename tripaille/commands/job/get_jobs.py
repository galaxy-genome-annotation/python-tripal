import click
from tripaille.cli import pass_context
from tripaille.decorators import custom_exception, list_output


@click.command('get_jobs')
@click.option(
    "--job_id",
    help="job id",
    type=int
)
@pass_context
@custom_exception
@list_output
def cli(ctx, job_id=""):
    """Get all jobs

Output:

    Jobs information
    """
    return ctx.gi.job.get_jobs(job_id=job_id)
