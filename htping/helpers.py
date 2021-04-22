import click
import requests

CLI_COLORS = {2: "green", 3: "yellow", 4: "bright_red", 5: "bright_red"}


def check_url(url):
    """Send HEAD request to the url and return the status code

    :param url: URL to check
    :type url: str
    :return: HTTP status code
    :rtype: int
    """
    try:
        response = requests.head(url)
    except requests.exceptions.ConnectionError:
        click.echo(f"ConnectionError: Can't reach {url}")
        return
    return response.status_code


def colorize(url, status):
    """Print the URL and status in color to the terminal

    :param url: URL to check
    :type url: str
    :param status: status code to display
    :type status: int
    :return: HTTP status code
    :rtype: int
    """
    click.secho(f"{url} -> {status}", fg=CLI_COLORS.get(status // 100, "magenta"))
