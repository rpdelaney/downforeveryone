from json.decoder import JSONDecodeError

import pytest as _pytest
import responses

from downforeveryone import isup


@_pytest.fixture
def fake_response_args(url="https://foo.bar", status=200):
    return {
        "method": responses.GET,
        "url": isup.query_url(url),
        "body": "{}",
        "status": status,
        "content_type": "application/json",
    }


@_pytest.fixture
def mock_request_success(mocker):
    fake = mocker.patch("requests.models.Response", autospec=True)
    fake.ok = True
    fake.status_code = 200
    return fake


@_pytest.fixture
def mock_request_failure(mocker):
    # This test does not mock the response object as intended, which
    # is causing test coverage to fall below the minimum as the JSONDecodeError
    # is not actually being raised.
    # TODO: Look into https://github.com/getsentry/responses for mocking
    # requests response objects
    fake = mocker.patch("requests.models.Response", autospec=False)
    fake.ok = False
    fake.status_code = 404
    fake.json.return_value = mocker.Mock(side_effect=JSONDecodeError)
    return fake


@_pytest.fixture
def requests_get_mock(mocker, mock_request_success):
    mock_response = mocker.patch("requests.get", autospec=True)
    mock_response.return_value = mock_request_success
    return mock_response


@_pytest.fixture
def handle_response_mock(mocker):
    return mocker.patch("downforeveryone.isup.handle_response", autospec=True)


@_pytest.fixture
def cli_args_mock(mocker):
    return mocker.patch("downforeveryone.cli.parse_args", autospec=True)


@_pytest.fixture
def isitup_mock(mocker):
    return mocker.patch("downforeveryone.isup.isitup")


@_pytest.fixture
def sys_exit_mock(mocker):
    return mocker.patch("sys.exit")
