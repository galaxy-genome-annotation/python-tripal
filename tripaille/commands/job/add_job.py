import click
from tripaille.cli import pass_context
from tripaille.decorators import custom_exception, dict_output


@click.command('add_job')
@click.argument("name", type=str)
@click.argument("module", type=str)
@click.argument("callback", type=str)
@click.argument("arguments", type=str)
@click.option(
    "--priority",
    help="An integer score to prioritize the job",
    default="10",
    show_default=True,
    type=int
)
@pass_context
@custom_exception
@dict_output
def cli(ctx, name, module, callback, arguments, priority=10):
    """Schedule a new job

Output:

    Job information
    """
    return ctx.gi.job.add_job(name, module, callback, arguments, priority=priority)
