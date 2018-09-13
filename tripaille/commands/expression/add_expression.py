import click
from tripaille.cli import pass_context
from tripaille.decorators import custom_exception, str_output


@click.command('add_expression')
@click.argument("organism_id", type=str)
@click.argument("analysis_id", type=str)
@click.argument("matching_type", type=click.Choice(['name', 'uniquename']))
@click.argument("file_path", type=str)

@click.option(
"--use_column",
    help="If the expression file is a column",
    is_flag=True
)

@click.option(
    "--biomaterial_provider",
    help="Biomaterial provider",
    type=str
)

@click.option(
    "--array_design",
    help="Array design id (not required for next-gen seq)",
    type=str
)

@click.option(
    "--assay_id",
    help="The id of the assay associated with the experiment",
    type=str
)

@click.option(
    "--acquisition_id",
    help="The id of the acquisition associated with the experiment",
    type=str
)

@click.option(
    "--quantification_id",
    help="The id of the quantification associated with the experiment",
    type=str
)

@click.option(
    "--file_extension",
    help="File extension (required for column file). Please exlude the '.'",
    type=str
)

@click.option(
    "--start_regex",
    help="Regular expression to describe the line that occurs before the start of the expression data. Can be blank if there are no header",
    type=str
)
@click.option(
    "--stop_regex",
    help="Regular expression to describe the line that occurs after the end of the expression data. Can be blank if there are no footer",
    type=str
)

@click.option(
    "--no_wait",
    help="Do not wait for job to complete",
    is_flag=True
)

@pass_context
@custom_exception
@str_output
def cli(ctx, organism_id, analysis_id, matching_type, file_path, use_column=False, biomaterial_provider="", array_design ="", assay_id="", acquisition_id="", quantification_id="", file_extension="", start_regex ="", stop_regex ="", no_wait=False):
    """Add one or multiple expression file\n
       Matching type is either name or unique_name\n
       Default type is matrix, set the --use_column flag if otherwise
    """
    return ctx.gi.expression.add_expression(organism_id, analysis_id, matching_type, file_path, use_column=use_column, biomaterial_provider=biomaterial_provider, array_design=array_design, assay_id=assay_id, acquisition_id=acquisition_id, quantification_id=quantification_id, file_extension=file_extension, start_regex=start_regex, stop_regex=stop_regex, no_wait=no_wait)
