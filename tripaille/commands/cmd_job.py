import click
from tripaille.commands.job.add_import_job import cli as func0
from tripaille.commands.job.add_job import cli as func1
from tripaille.commands.job.get_jobs import cli as func2
from tripaille.commands.job.get_logs import cli as func3
from tripaille.commands.job.run_jobs import cli as func4
from tripaille.commands.job.wait import cli as func5


@click.group()
def cli():
    """Manage Tripal jobs"""
    pass


cli.add_command(func0)
cli.add_command(func1)
cli.add_command(func2)
cli.add_command(func3)
cli.add_command(func4)
cli.add_command(func5)
