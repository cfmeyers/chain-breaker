# -*- coding: utf-8 -*-

"""Console script for chain_breaker."""
import sys
import click


@click.command()
@click.argument('chain_path')
def main(chain_path):
    """Console script for chain_breaker."""
    click.echo(chain_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
