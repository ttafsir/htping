import click
import pytest
import requests
from click.testing import CliRunner

from htping import __version__
from htping.cli import main
from htping.helpers import check_url, colorize


def test_version():
    assert __version__ == "0.1.0"


def mock_response_object(code):
    resp = requests.Response()
    resp.status_code = code
    return resp


def test_check_url(mocker):
    mocker.patch("requests.head", return_value=mock_response_object(200))
    assert check_url("dummy_url") == 200

    mocker.patch("requests.head", return_value=mock_response_object(404))
    assert check_url("dummy_url") == 404


def test_check_url_wo_args_raises():
    with pytest.raises(TypeError):
        check_url()  # noqa


# def test_colorize_status_called(mocker):
#     mocker.patch("click.secho")
#     colorize("dummyurl", 200)
#     click.secho.assert_called


def test_colorize_status_called_w_args(mocker):
    mocker.patch("click.secho")
    url = "dummyurl"
    status = 200
    colorize(url, status)
    click.secho.assert_called_with(f"{url} -> {status}", fg="green")


@pytest.mark.parametrize(
    "code, color",
    [
        (200, "green"),
        (304, "yellow"),
        (404, "bright_red"),
        (500, "bright_red"),
        (1, "magenta"),
    ],
)
def test_check_one_url(mocker, code, color):
    mocker.patch("requests.head", return_value=mock_response_object(code))

    runner = CliRunner()
    result = runner.invoke(main, ["dummyurl"], color=True)

    expected_message = click.style(f"dummyurl -> {code}", fg=color)
    assert result.output == f"{expected_message}\n"


def test_check_multiple_urls(mocker):
    mocker.patch(
        "requests.head",
        side_effect=[mock_response_object(200), mock_response_object(500)],
    )

    runner = CliRunner()
    result = runner.invoke(main, ["dummy_url1", "dummy_url2"], color=True)

    expected_msg1 = click.style("dummy_url1 -> 200", fg="green")
    expected_msg2 = click.style("dummy_url2 -> 500", fg="bright_red")
    assert result.output == f"{expected_msg1}\n{expected_msg2}\n"
