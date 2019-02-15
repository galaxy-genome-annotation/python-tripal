import click
from tripaille.cli import pass_context
from tripaille.decorators import custom_exception, str_output


@click.command('index')
@click.option(
    "--mode",
    help="Indexing mode: 'website' to index the website , 'nodes' for the website nodes, 'entities' for the website entities (Tripal 3), 'table' to index a single table, 'gene' to build a Gene search index (Tripal 3 only) (default: website) ('website' default to 'nodes' for Tripal 2, 'entities' for Tripal 3)",
    default="website",
    show_default=True,
    type=str
)
@click.option(
    "--table",
    help="Table to index (only in 'table' mode)",
    type=str
)
@click.option(
    "--index_name",
    help="Index name (only in 'table' mode)",
    type=str
)
@click.option(
    "--queues",
    help="Number of indexing task queues (Tripal 2 only)",
    default="10",
    show_default=True,
    type=int
)
@click.option(
    "--fields",
    help="Fields to index (only in 'table' mode), syntax: <field_name>|<field_type>, field_type should be one of 'string' (Tripal2), 'text' (Tripal3), 'keyword', 'date', 'long', 'double', 'boolean', 'ip', 'object', 'nested', 'geo_point', 'geo_shape', or 'completion'",
    type=str,
    multiple=True
)
@click.option(
    "--links",
    help="List of links to show to users, syntax: <column-where-to-show-the-link>|</your/url/[any-column-name]> (Tripal 2 only)",
    type=str,
    multiple=True
)
@click.option(
    "--tokenizer",
    help="Tokenizer to use (only in 'table' mode) (one of 'standard', 'letter', 'lowercase', 'whitespace', 'uax_url_email', 'classic', 'ngram', 'edge_ngram', 'keywordx', 'pattern', or 'path_hierarchy'; default='standard')",
    default="standard",
    show_default=True,
    type=str
)
@click.option(
    "--token_filters",
    help="Token filters (Tripal 3 only) (only in 'table' mode) (available filters are 'standard', 'asciifolding', 'length', 'lowercase', 'uppercase') (Default to ['standard', 'lowercase'])",
    type=str,
    multiple=True
)
@click.option(
    "--exposed",
    help="\"Expose the index (read-only) to other websites",
    is_flag=True
)
@click.option(
    "--index_url",
    help="In order for other sites to link back to your results page, you must specify a path where the form for this index can be reached",
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
def cli(ctx, mode=website, table="", index_name="", queues=10, fields=None, links={}, tokenizer=standard, token_filters=None, exposed=False, index_url="", job_name="", no_wait=False):
    """Schedule database indexing using elasticsearch

Output:

    Indexing information
    """
    return ctx.gi.db.index(mode=mode, table=table, index_name=index_name, queues=queues, fields=fields, links=links, tokenizer=tokenizer, token_filters=token_filters, exposed=exposed, index_url=index_url, job_name=job_name, no_wait=no_wait)
