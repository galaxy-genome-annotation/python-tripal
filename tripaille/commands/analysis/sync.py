import click
from tripaille.cli import pass_context
from tripaille.decorators import custom_exception, str_output


@click.command('sync')
@click.option(
    "--analysis",
    help="Analysis name",
    type=str
)
@click.option(
    "--analysis_id",
    help="ID of the analysis to sync",
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
def cli(ctx, analysis="", analysis_id="", job_name="", no_wait=""):
    """Synchronize an analysis

Output:

    status
    """
    return ctx.gi.analysis.sync(analysis=analysis, analysis_id=analysis_id, job_name=job_name, no_wait=no_wait)
