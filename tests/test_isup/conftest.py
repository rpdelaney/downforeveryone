import pytest
import responses

from downforeveryone import cli, constants


@pytest.fixture()
def fake_response_args(url="https://foo.bar", status=200):
    return {
        "method": responses.GET,
        "url": constants.API_URL.format(domain=url),
        "body": "{}",
        "status": status,
        "content_type": "application/json",
    }


@pytest.fixture()
def fake_cli_args():
    return cli.parse_args("http://foo.bar")


@pytest.fixture()
def mock_cli_args(mocker):
    return mocker.patch("downforeveryone.cli.parse_args", autospec=True)


@pytest.fixture()
def mock_handle_response(mocker):
    return mocker.patch("downforeveryone.isup._handle_response", autospec=True)


@pytest.fixture()
def mock_isitup(mocker):
    return mocker.patch("downforeveryone.isup.isitup")


@pytest.fixture()
def mock_sys_exit(mocker):
    return mocker.patch("sys.exit")
