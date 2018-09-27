import click
from tripaille.cli import pass_context
from tripaille.decorators import custom_exception, dict_output


@click.command('delete_biomaterials')

@click.option(
"--name",
    help="Biomaterial name to delete. Setting this parameter will ignore the others",
    type=str,
    multiple=True
)

@click.option(
"--organism_id",
    help="Delete biomaterials from an organism",
    type=str
)

@click.option(
"--analysis_id",
    help="Delete biomaterials from an analysis",
    type=str
)

@click.option(
"--no_wait",
    help="Do not wait for job to complete",
    is_flag=True
)

@click.option(
"--job_name",
    help="Job name",
    type=str
)


@pass_context
@custom_exception
@dict_output

def cli(ctx, name=[], organism_id="", analysis_id="", no_wait=False, job_name=""):
    """Delete biomaterials\n
Output:

    status
    """
    return ctx.gi.expression.delete_biomaterials(names=name, organism_id=organism_id, analysis_id=analysis_id, no_wait=no_wait, job_name=job_name)
