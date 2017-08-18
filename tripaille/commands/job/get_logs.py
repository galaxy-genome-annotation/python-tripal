import click
from tripaille.cli import pass_context
from tripaille.decorators import custom_exception, dict_output


@click.command('get_logs')
@click.argument("stdout", type=str)
@click.argument("stderr", type=str)
@pass_context
@custom_exception
@dict_output
def cli(ctx, stdout, stderr):
    """Get job output

Output:

    Output information
    """
    return ctx.gi.job.get_logs(stdout, stderr)
