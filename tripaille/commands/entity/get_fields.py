import click
from tripaille.cli import pass_context
from tripaille.decorators import custom_exception, dict_output


@click.command('get_fields')
@click.argument("entity", type=str)
@pass_context
@custom_exception
@dict_output
def cli(ctx, entity):
    """Get the list of available fields for an entity

Output:

    Fields information
    """
    return ctx.gi.entity.get_fields(entity)
