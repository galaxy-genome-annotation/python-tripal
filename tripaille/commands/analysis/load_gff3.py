import click
from tripaille.cli import pass_context
from tripaille.decorators import custom_exception, str_output


@click.command('load_gff3')
@click.argument("gff", type=str)
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
    "--analysis",
    help="Analysis name",
    type=str
)
@click.option(
    "--analysis_id",
    help="Analysis ID",
    type=int
)
@click.option(
    "--import_mode",
    help="Import mode (add_only=existing features won't be touched, update=existing features will be updated and obsolete attributes kept)')",
    default="update",
    show_default=True,
    type=str
)
@click.option(
    "--target_organism",
    help="In case of Target attribute in the GFF3, choose the organism abbreviation or common name to which target sequences belong. Select this only if target sequences belong to a different organism than the one specified with --organism-id. And only choose an organism here if all of the target sequences belong to the same species. If the targets in the GFF file belong to multiple different species then the organism must be specified using the 'target_organism=genus:species' attribute in the GFF file.')",
    type=str
)
@click.option(
    "--target_organism_id",
    help="In case of Target attribute in the GFF3, choose the organism ID to which target sequences belong. Select this only if target sequences belong to a different organism than the one specified with --organism-id. And only choose an organism here if all of the target sequences belong to the same species. If the targets in the GFF file belong to multiple different species then the organism must be specified using the 'target_organism=genus:species' attribute in the GFF file.')",
    type=int
)
@click.option(
    "--target_type",
    help="In case of Target attribute in the GFF3, if the unique name for a target sequence is not unique (e.g. a protein and an mRNA have the same name) then you must specify the type for all targets in the GFF file. If the targets are of different types then the type must be specified using the 'target_type=type' attribute in the GFF file. This must be a valid Sequence Ontology (SO) term.')",
    type=str
)
@click.option(
    "--target_create",
    help="In case of Target attribute in the GFF3, if the target feature cannot be found, create one using the organism and type specified above, or using the 'target_organism' and 'target_type' fields specified in the GFF file. Values specified in the GFF file take precedence over those specified above.')",
    is_flag=True
)
@click.option(
    "--start_line",
    help="The line in the GFF file where importing should start",
    type=int
)
@click.option(
    "--landmark_type",
    help="A Sequence Ontology type for the landmark sequences in the GFF fie (e.g. 'chromosome').",
    type=str
)
@click.option(
    "--alt_id_attr",
    help="When ID attribute is absent, specify which other attribute can uniquely identify the feature.",
    type=str
)
@click.option(
    "--create_organism",
    help="Create organisms when encountering organism attribute (these lines will be skip otherwise)",
    is_flag=True
)
@click.option(
    "--re_mrna",
    help="Regular expression for the mRNA name",
    type=str
)
@click.option(
    "--re_protein",
    help="Replacement string for the protein name",
    type=str
)
@click.option(
    "--job_name",
    help="Name of the job",
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
def cli(ctx, gff, organism="", organism_id="", analysis="", analysis_id="", import_mode="update", target_organism="", target_organism_id="", target_type="", target_create=False, start_line="", landmark_type="", alt_id_attr="", create_organism=False, re_mrna="", re_protein="", job_name="", no_wait=False):
    """Load GFF3 file

Output:

    Loading information
    """
    return ctx.gi.analysis.load_gff3(gff, organism=organism, organism_id=organism_id, analysis=analysis, analysis_id=analysis_id, import_mode=import_mode, target_organism=target_organism, target_organism_id=target_organism_id, target_type=target_type, target_create=target_create, start_line=start_line, landmark_type=landmark_type, alt_id_attr=alt_id_attr, create_organism=create_organism, re_mrna=re_mrna, re_protein=re_protein, job_name=job_name, no_wait=no_wait)
