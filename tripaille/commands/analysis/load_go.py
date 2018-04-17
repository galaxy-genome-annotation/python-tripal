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
    "--organism",
    help="Organism common name or abbreviation",
    type=str
)
@click.option(
    "--organism_id",
    help="Organism ID",
    type=int
)
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
    "--query_matching",
    help="Method to match identifiers to features in the database. ('name', 'uniquename' or 'dbxref')",
    default="uniquename",
    show_default=True,
    type=str
)
@click.option(
    "--method",
    help="Import method ('add' or 'remove')",
    default="add",
    show_default=True,
    type=str
)
@click.option(
    "--name_column",
    help="Column containing the feature identifiers (2, 3, 10 or 11; default=2).",
    default="2",
    show_default=True,
    type=int
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
def cli(ctx, name, program, programversion, sourcename, gaf_output, organism="", organism_id="", gaf_ext="", query_type="", query_matching="uniquename", method="add", name_column=2, re_name="", no_wait=False, algorithm="", sourceversion="", sourceuri="", description="", date_executed=""):
    """Create a GO analysis

Output:

    Loading information
    """
    return ctx.gi.analysis.load_go(name, program, programversion, sourcename, gaf_output, organism=organism, organism_id=organism_id, gaf_ext=gaf_ext, query_type=query_type, query_matching=query_matching, method=method, name_column=name_column, re_name=re_name, no_wait=no_wait, algorithm=algorithm, sourceversion=sourceversion, sourceuri=sourceuri, description=description, date_executed=date_executed)
