import click
from tripaille.cli import pass_context
from tripaille.decorators import custom_exception, str_output


@click.command('add_expression')
@click.argument("organism_id", type=str)
@click.argument("analysis_id", type=str)
@click.argument("match_type", type=str)
@click.argument("file_path", type=str)
@click.option(
    "--biomaterial_provider",
    help="The contact who provided the biomaterial. (optional, non functional in Tripal2)",
    type=str
)
@click.option(
    "--array_design",
    help="The array design associated with this analysis. This is not required if the experimental data was gathered from next generation sequencing methods. (optional, non functional in Tripal2)",
    type=str
)
@click.option(
    "--assay_id",
    help="The id of the assay associated with the experiment. (optional, non functional in Tripal2)",
    type=str
)
@click.option(
    "--acquisition_id",
    help="The id of the acquisition associated with the experiment (optional, non functional in Tripal2)",
    type=str
)
@click.option(
    "--quantification_id",
    help="The id of the quantification associated with the experiment (optional, non functional in Tripal2)",
    type=str
)
@click.option(
    "--file_extension",
    help="File extension for the file(s) to be loaded into Chado. Do not include the \".\". Not required for matrix files. (optional)",
    type=str
)
@click.option(
    "--start_regex",
    help="A regular expression to describe the line that occurs before the start of the expression data. If the file has no header, this is not needed. (optional)",
    type=str
)
@click.option(
    "--stop_regex",
    help="A regular expression to describe the line that occurs after the end of the expression data. If the file has no footer text, this is not needed. (optional)",
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
def cli(ctx, organism_id, analysis_id, match_type, file_path, biomaterial_provider="", array_design="", assay_id="", acquisition_id="", quantification_id="", file_extension="", start_regex="", stop_regex="", use_column=False, no_wait=False):
    """:type organism_id: str :param organism_id: Organism Id

Output:

    Loading information
    """
    return ctx.gi.expression.add_expression(organism_id, analysis_id, match_type, file_path, biomaterial_provider=biomaterial_provider, array_design=array_design, assay_id=assay_id, acquisition_id=acquisition_id, quantification_id=quantification_id, file_extension=file_extension, start_regex=start_regex, stop_regex=stop_regex, use_column=use_column, no_wait=no_wait)
