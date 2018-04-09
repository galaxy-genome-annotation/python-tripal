import click
from tripaille.cli import pass_context
from tripaille.decorators import custom_exception, dict_output


@click.command('add_import_job')
@click.argument("name", type=str)
@click.argument("importer", type=str)
@click.argument("input_file", type=str)
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
def cli(ctx, name, importer, input_file, arguments, priority=10):
    """Schedule a new import job

Output:

    Job information
    """
    return ctx.gi.job.add_import_job(name, importer, input_file, arguments, priority=priority)
