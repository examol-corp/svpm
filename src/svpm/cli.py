import click

@click.group()
def cli():
    """Command line application

    See sub-command's --help for more specific information.

    """

    pass

@cli.command()
def stencil():
    """Subcommand for working with stencils."""
    pass
