import click
from tripaille.cli import pass_context
from tripaille.decorators import custom_exception, str_output


@click.command('load_interpro')
@click.argument("name", type=str)
@click.argument("program", type=str)
@click.argument("programversion", type=str)
@click.argument("sourcename", type=str)
@click.argument("interpro_output", type=str)
@click.option(
    "--interpro_parameters",
    help="InterProScan parameters used to produce these results",
    type=str
)
@click.option(
    "--query_re",
    help="The regular expression that can uniquely identify the query name. This parameters is required if the feature name is not the first word in the blast query name.",
    type=str
)
@click.option(
    "--query_type",
    help="The feature type (e.g. 'gene', 'mRNA', 'contig') of the query. It must be a valid Sequence Ontology term.",
    type=str
)
@click.option(
    "--query_uniquename",
    help="Use this if the query_re regular expression matches unique names instead of names in the database.",
    is_flag=True
)
@click.option(
    "--parse_go",
    help="Load GO annotation to the database",
    is_flag=True
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
def cli(ctx, name, program, programversion, sourcename, interpro_output, interpro_parameters="", query_re="", query_type="", query_uniquename=False, parse_go=False, no_wait=False, algorithm="", sourceversion="", sourceuri="", description="", date_executed=""):
    """Create an Interpro analysis

Output:

    Loading information
    """
    return ctx.gi.analysis.load_interpro(name, program, programversion, sourcename, interpro_output, interpro_parameters=interpro_parameters, query_re=query_re, query_type=query_type, query_uniquename=query_uniquename, parse_go=parse_go, no_wait=no_wait, algorithm=algorithm, sourceversion=sourceversion, sourceuri=sourceuri, description=description, date_executed=date_executed)
