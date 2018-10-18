import click
from tripaille.cli import pass_context
from tripaille.decorators import custom_exception, str_output


@click.command('add_expression')
@click.argument("organism_id", type=str)
@click.argument("analysis_id", type=str)
@click.argument("file_path", type=str)
@click.option(
    "--match_type",
    help="Match to features using either name or uniquename. Default to uniquename",
    default="uniquename",
    show_default=True,
    type=str
)
@click.option(
    "--array_design_id",
    help="The array design ID associated with this analysis. (Non functional in Tripal2)",
    type=str
)
@click.option(
    "--quantification_units",
    help="The units associated with the loaded values (ie, FPKM, RPKM, raw counts).",
    type=str
)
@click.option(
    "--file_extension",
    help="File extension for the file(s) to be loaded into Chado. Do not include the \".\". Not required for matrix files.",
    type=str
)
@click.option(
    "--start_regex",
    help="A regular expression to describe the line that occurs before the start of the expression data. If the file has no header, this is not needed.",
    type=str
)
@click.option(
    "--stop_regex",
    help="A regular expression to describe the line that occurs after the end of the expression data. If the file has no footer text, this is not needed.",
    type=str
)
@click.option(
    "--seq_type",
    help="Specify the feature type to associate the data with. (Tripal3 only)",
    type=str
)
@click.option(
    "--use_column",
    help="Set if the expression file is a column file",
    is_flag=True
)
@click.option(
    "--no_wait",
    help="Do not wait for job to complete",
    is_flag=True
)
@pass_context
@custom_exception
@str_output
def cli(ctx, organism_id, analysis_id, file_path, match_type="uniquename", array_design_id="", quantification_units="", file_extension="", start_regex="", stop_regex="", seq_type="", use_column=False, no_wait=False):
    """:type organism_id: str :param organism_id: Organism Id

Output:

    Loading information
    """
    return ctx.gi.expression.add_expression(organism_id, analysis_id, file_path, match_type=match_type, array_design_id=array_design_id, quantification_units=quantification_units, file_extension=file_extension, start_regex=start_regex, stop_regex=stop_regex, seq_type=seq_type, use_column=use_column, no_wait=no_wait)
