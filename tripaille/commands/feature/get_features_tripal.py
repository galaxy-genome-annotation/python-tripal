import click
from tripaille.cli import pass_context
from tripaille.decorators import custom_exception, list_output


@click.command('get_features_tripal')
@click.option(
    "--feature_id",
    help="A feature entity/node ID",
    type=int
)
@pass_context
@custom_exception
@list_output
def cli(ctx, feature_id=""):
    """Get features entities

Output:

    Feature entity/node information
    """
    return ctx.gi.feature.get_features_tripal(feature_id=feature_id)
