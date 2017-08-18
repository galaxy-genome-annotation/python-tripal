import click
from tripaille.cli import pass_context
from tripaille.decorators import custom_exception, list_output


@click.command('get_analyses')
@click.option(
    "--analysis_id",
    help="An analysis ID",
    type=str
)
@click.option(
    "--name",
    help="analysis name",
    type=str
)
@click.option(
    "--program",
    help="analysis program",
    type=str
)
@click.option(
    "--programversion",
    help="analysis programversion",
    type=str
)
@click.option(
    "--algorithm",
    help="analysis algorithm",
    type=str
)
@click.option(
    "--sourcename",
    help="analysis sourcename",
    type=str
)
@click.option(
    "--sourceversion",
    help="analysis sourceversion",
    type=str
)
@click.option(
    "--sourceuri",
    help="analysis sourceuri",
    type=str
)
@click.option(
    "--date_executed",
    help="analysis date_executed (yyyy-mm-dd)",
    type=str
)
@pass_context
@custom_exception
@list_output
def cli(ctx, analysis_id="", name="", program="", programversion="", algorithm="", sourcename="", sourceversion="", sourceuri="", date_executed=""):
    """Get analyses

Output:

    Analysis information
    """
    return ctx.gi.analysis.get_analyses(analysis_id=analysis_id, name=name, program=program, programversion=programversion, algorithm=algorithm, sourcename=sourcename, sourceversion=sourceversion, sourceuri=sourceuri, date_executed=date_executed)
