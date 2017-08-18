import click
from tripaille.cli import pass_context
from tripaille.decorators import custom_exception, list_output


@click.command('get_taxonomic_ranks')
@pass_context
@custom_exception
@list_output
def cli(ctx):
    """Get taxonomic ranks

Output:

    Taxonomic ranks
    """
    return ctx.gi.organism.get_taxonomic_ranks()
