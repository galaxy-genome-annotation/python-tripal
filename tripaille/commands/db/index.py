import click
from tripaille.cli import pass_context
from tripaille.decorators import custom_exception, str_output


@click.command('index')
@click.option(
    "--mode",
    help="Indexing mode: 'website' to index everything, 'table' to index a single table (default: website)",
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
    help="Number of indexing task queues",
    default="10",
    show_default=True,
    type=int
)
@click.option(
    "--fields",
    help="Fields to index (only in 'table' mode), syntax: <field_name>|<field_type>, field_type should be one of 'string', 'keyword', 'date', 'long', 'double', 'boolean', 'ip', 'object', 'nested', 'geo_point', 'geo_shape', or 'completion'",
    type=str,
    multiple=True
)
@click.option(
    "--links",
    help="List of links to show to users, syntax: <column-where-to-show-the-link>|</your/url/[any-column-name]>",
    type=str,
    multiple=True
)
@click.option(
    "--tokenizer",
    help="Tokenizer to use (one of 'standard', 'letter', 'lowercase', 'whitespace', 'uax_url_email', 'classic', 'ngram', 'edge_ngram', 'keyword', 'pattern', or 'path_hierarchy'; default='standard')",
    default="standard",
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
def cli(ctx, mode="website", table="", index_name="", queues=10, fields=None, links={}, tokenizer="standard", job_name="", no_wait=False):
    """Schedule database indexing using elasticsearch

Output:

    Indexing information
    """
    return ctx.gi.db.index(mode=mode, table=table, index_name=index_name, queues=queues, fields=fields, links=links, tokenizer=tokenizer, job_name=job_name, no_wait=no_wait)
