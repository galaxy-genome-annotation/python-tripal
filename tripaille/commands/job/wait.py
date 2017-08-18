import click
from tripaille.cli import pass_context
from tripaille.decorators import custom_exception, dict_output


@click.command('wait')
@click.argument("job_id", type=int)
@pass_context
@custom_exception
@dict_output
def cli(ctx, job_id):
    """Wait for a job completion

Output:

    Job information
    """
    return ctx.gi.job.wait(job_id)
