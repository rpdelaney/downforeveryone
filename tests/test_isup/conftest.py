import pytest as _pytest
import responses

from downforeveryone import cli, isup


@_pytest.fixture
def fake_response_args(url="https://foo.bar", status=200):
    return {
        "method": responses.GET,
        "url": isup._query_url(url),
        "body": "{}",
        "status": status,
        "content_type": "application/json",
    }


@_pytest.fixture
def fake_cli_args(mocker):
    return cli.parse_args("http://foo.bar")


@_pytest.fixture
def mock_cli_args(mocker):
    return mocker.patch("downforeveryone.cli.parse_args")


@_pytest.fixture
def handle_response_mock(mocker):
    return mocker.patch("downforeveryone.isup._handle_response", autospec=True)


@_pytest.fixture
def cli_args_mock(mocker):
    return mocker.patch("downforeveryone.cli.parse_args", autospec=True)


@_pytest.fixture
def isitup_mock(mocker):
    return mocker.patch("downforeveryone.isup.isitup")


@_pytest.fixture
def sys_exit_mock(mocker):
    return mocker.patch("sys.exit")
