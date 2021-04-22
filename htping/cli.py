"""Console script for htping."""
import sys
from time import sleep

import click

from htping.helpers import check_url, colorize


@click.command()
@click.argument("urls", nargs=-1, required=True)
@click.option("--daemon", "-d", default=False, is_flag=True)
def main(urls, daemon):
    """Check url and print their HTTP statuses (w/ colors)

    :param urls: URL (or a tuple with multiple URLs) to check
    :type urls: str or tuple(str)
    :param daemon: If set to True, after checking all URLs,
                   sleep for 5 seconds and check them again
    :type daemon: bool
    """
    while True:
        for url in urls:
            status_code = check_url(url)
            if status_code:
                colorize(url, status_code)
        if not daemon:
            break
        sleep(5)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
