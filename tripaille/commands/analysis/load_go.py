import click
from tripaille.cli import pass_context
from tripaille.decorators import custom_exception, str_output


@click.command('load_go')
@click.argument("name", type=str)
@click.argument("program", type=str)
@click.argument("programversion", type=str)
@click.argument("sourcename", type=str)
@click.argument("gaf_output", type=str)
@click.option(
    "--gaf_ext",
    help="If looking for files in a directory, extension of the GAF files",
    type=str
)
@click.option(
    "--query_type",
    help="The feature type (e.g. 'gene', 'mRNA', 'contig') of the query. It must be a valid Sequence Ontology term.",
    type=str
)
@click.option(
    "--query_uniquename",
    help="Use this if the --query-re regular expression matches unique names instead of names in the database.",
    is_flag=True
)
@click.option(
    "--method",
    help="Import method ('add' or 'remove')",
    default="add",
    show_default=True,
    type=str
)
@click.option(
    "--re_name",
    help="Regular expression to extract the feature name from GAF file.",
    type=str
)
@click.option(
    "--no_wait",
    help="Do not wait for job to complete",
    is_flag=True
)
@click.option(
    "--algorithm",
    help="analysis algorithm",
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
    "--description",
    help="analysis description",
    type=str
)
@click.option(
    "--date_executed",
    help="analysis date_executed (yyyy-mm-dd)",
    type=str
)
@pass_context
@custom_exception
@str_output
def cli(ctx, name, program, programversion, sourcename, gaf_output, gaf_ext="", query_type="", query_uniquename=False, method="add", re_name="", no_wait=False, algorithm="", sourceversion="", sourceuri="", description="", date_executed=""):
    """Create a GO analysis

Output:

    Loading information
    """
    return ctx.gi.analysis.load_go(name, program, programversion, sourcename, gaf_output, gaf_ext=gaf_ext, query_type=query_type, query_uniquename=query_uniquename, method=method, re_name=re_name, no_wait=no_wait, algorithm=algorithm, sourceversion=sourceversion, sourceuri=sourceuri, description=description, date_executed=date_executed)
