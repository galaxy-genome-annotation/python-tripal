import click
from tripaille.cli import pass_context
from tripaille.decorators import custom_exception, list_output


@click.command('get_entities')
@click.option(
    "--entity",
    help="Name of the entity type (e.g. Organism)",
    type=str
)
@click.option(
    "--entity_id",
    help="ID of an entity",
    type=int
)
@pass_context
@custom_exception
@list_output
def cli(ctx, entity="", entity_id=""):
    """Get entities

Output:

    Entity information
    """
    return ctx.gi.entity.get_entities(entity=entity, entity_id=entity_id)
