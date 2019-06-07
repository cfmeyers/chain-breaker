# -*- coding: utf-8 -*-

"""Console script for chain_breaker."""
import sys
import click

from chain_breaker.chain_breaker import render_chain


@click.command()
@click.argument('path_to_chain')
@click.argument('title')
def main(path_to_chain, title):
    """Console script for chain_breaker."""
    render_chain(path_to_chain, title)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
