import os

import click

from tripal import TripalInstance
from tripaille.cli import pass_context
from tripaille import config
from tripaille.io import warn, info

CONFIG_TEMPLATE = """## Tripal's tripaille: Global Configuration File.
# Each stanza should contain a single Tripal server to control.
#
# You can set the key __default to the name of a default instance
__default: local

local:
    tripal_url: "%(tripal_url)s"
    username: "%(username)s"
    password: "%(password)s"
    auth_login: "%(auth_login)s" # Optional, only if your tripal instance is running behind an authentication proxy
    auth_password: "%(auth_password)s" # Optional, only if your tripal instance is running behind an authentication proxy
"""

SUCCESS_MESSAGE = (
    "Ready to go! Type `tripaille` to get a list of commands you can execute."
)


@click.command("config_init")
@pass_context
def cli(ctx, url=None, api_key=None, admin=False, **kwds):
    """Help initialize global configuration (in home directory)
    """
    # TODO: prompt for values someday.
    click.echo("""Welcome to Tripal's Tripaille!""")
    if os.path.exists(config.global_config_path()):
        info("Your tripaille configuration already exists. Please edit it instead: %s" % config.global_config_path())
        return 0

    while True:
        # Check environment
        tripal_url = click.prompt("TRIPAL_URL")
        username = click.prompt("TRIPAL_USER")
        password = click.prompt("TRIPAL_PASS", hide_input=True)
        auth_login = ''
        auth_password = ''
        if click.confirm("""Is your tripal instance running behind an authentication proxy?"""):
            auth_login = click.prompt("TRIPAL_AUTH_USER")
            auth_password = click.prompt("TRIPAL_AUTH_PASS", hide_input=True)

        info("Testing config...")
        try:
            TripalInstance(tripal_url=tripal_url, username=username, password=password)
            # We do a connection test during startup.
            info("Ok! Everything looks good.")
            break
        except Exception as e:
            warn("Error, we could not access the configuration data for your instance: %s", e)
            should_break = click.prompt("Continue despite inability to contact this instance? [y/n]")
            if should_break in ('Y', 'y'):
                break

    config_path = config.global_config_path()
    if os.path.exists(config_path):
        warn("File %s already exists, refusing to overwrite." % config_path)
        return -1

    with open(config_path, "w") as f:
        f.write(CONFIG_TEMPLATE % {
            'tripal_url': tripal_url,
            'username': username,
            'password': password,
            'auth_login': auth_login,
            'auth_password': auth_password,
        })
        info(SUCCESS_MESSAGE)
