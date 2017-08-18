import click
from tripaille.cli import pass_context
from tripaille.decorators import custom_exception, dict_output


@click.command('run_jobs')
@click.option(
    "--wait",
    help="Wait for job completion",
    default="True",
    show_default=True,
    is_flag=True
)
@pass_context
@custom_exception
@dict_output
def cli(ctx, wait=True):
    """Run jobs in queue. There is no way to trigger a single job execution.

Output:

    Job information
    """
    return ctx.gi.job.run_jobs(wait=wait)
