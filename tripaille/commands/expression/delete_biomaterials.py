import click
from tripaille.cli import pass_context
from tripaille.decorators import custom_exception, str_output


@click.command('delete_biomaterials')
@click.option(
    "--names",
    help="JSON list of biomaterial names to delete. (optional)",
    type=str
)
@click.option(
    "--organism_id",
    help="Organism id from which to delete biomaterials (optional)",
    type=str
)
@click.option(
    "--analysis_id",
    help="Analysis id from which to delete biomaterials (optional)",
    type=str
)
@click.option(
    "--job_name",
    help="Name of the job (optional)",
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
def cli(ctx, names=None, organism_id="", analysis_id="", job_name="", no_wait=False):
    """Delete some biomaterials

Output:

    status
    """
    return ctx.gi.expression.delete_biomaterials(names=names, organism_id=organism_id, analysis_id=analysis_id, job_name=job_name, no_wait=no_wait)
