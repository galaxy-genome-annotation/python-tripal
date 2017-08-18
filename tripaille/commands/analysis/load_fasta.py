import click
from tripaille.cli import pass_context
from tripaille.decorators import custom_exception, str_output


@click.command('load_fasta')
@click.argument("fasta", type=str)
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
    "--sequence_type",
    help="Sequence type",
    default="contig",
    show_default=True,
    type=str
)
@click.option(
    "--re_name",
    help="Regular expression for the name",
    type=str
)
@click.option(
    "--re_uniquename",
    help="Regular expression for the unique name",
    type=str
)
@click.option(
    "--db_ext_id",
    help="External DB ID",
    type=str
)
@click.option(
    "--re_accession",
    help="Regular expression for the accession from external DB",
    type=str
)
@click.option(
    "--rel_type",
    help="Relation type (part_of or derives_from)",
    type=str
)
@click.option(
    "--rel_subject_re",
    help="Relation subject regular expression (used to extract id of related entity)",
    type=str
)
@click.option(
    "--rel_subject_type",
    help="Relation subject type (must match already loaded data, e.g. mRNA)",
    type=str
)
@click.option(
    "--method",
    help="Insertion method (insert, update or insup, default=insup (Insert and Update))",
    default="insup",
    show_default=True,
    type=str
)
@click.option(
    "--match_type",
    help="Match type for already loaded features (name or uniquename; default=uniquename; used for \"Update only\" or \"Insert and update\" methods)'",
    default="uniquename",
    show_default=True,
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
def cli(ctx, fasta, organism="", organism_id="", analysis="", analysis_id="", sequence_type="contig", re_name="", re_uniquename="", db_ext_id="", re_accession="", rel_type="", rel_subject_re="", rel_subject_type="", method="insup", match_type="uniquename", job_name="", no_wait=False):
    """Load fasta sequences

Output:

    Loading information
    """
    return ctx.gi.analysis.load_fasta(fasta, organism=organism, organism_id=organism_id, analysis=analysis, analysis_id=analysis_id, sequence_type=sequence_type, re_name=re_name, re_uniquename=re_uniquename, db_ext_id=db_ext_id, re_accession=re_accession, rel_type=rel_type, rel_subject_re=rel_subject_re, rel_subject_type=rel_subject_type, method=method, match_type=match_type, job_name=job_name, no_wait=no_wait)
