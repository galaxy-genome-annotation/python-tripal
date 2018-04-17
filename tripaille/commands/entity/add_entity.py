import click
from tripaille.cli import pass_context
from tripaille.decorators import custom_exception, dict_output


@click.command('add_entity')
@click.argument("entity", type=str)
@click.option(
    "--params",
    help="Values to populate the entity fields",
    type=str
)
@pass_context
@custom_exception
@dict_output
def cli(ctx, entity, params={}):
    """Add a new entity to the database

Output:

    Entity information
    """
    return ctx.gi.entity.add_entity(entity, params=params)
