import json

import responses
from requests.exceptions import RequestException

from downforeveryone import isup

__TEST_URL__ = "https://foo.bar"


@responses.activate
def test_requests_dot_get_called_once(fake_response_args):
    responses.add(**fake_response_args)

    isup.isitup(__TEST_URL__)

    responses.assert_call_count(isup._query_url(__TEST_URL__), 1)


@responses.activate
def test_handle_response_called_once(fake_response_args, mock_handle_response):
    responses.add(**fake_response_args)

    isup.isitup(__TEST_URL__)

    mock_handle_response.assert_called_once_with(
        json.loads(fake_response_args["body"])
    )


@responses.activate
def test_isup_returns_handle_response(
    fake_response_args, mock_handle_response
):
    responses.add(**fake_response_args)

    return_value = isup.isitup(__TEST_URL__)

    assert return_value == mock_handle_response.return_value


@responses.activate
def test_isup_error_with_description(fake_response_args, mock_handle_response):
    fake_response_args["status"] = 404
    responses.add(**fake_response_args)

    result_message, result_status = isup.isitup(__TEST_URL__)

    assert result_message == "404 Nothing matches the given URI"
    assert result_status == 3


@responses.activate
def test_isup_handles_broken_json(fake_response_args):
    fake_response_args["body"] = "This isn't valid json."
    fake_response_args["status"] = 200
    responses.add(**fake_response_args)

    result_message, result_status = isup.isitup(__TEST_URL__)

    assert (
        result_message == "JSONDecodeError: [Errno Expecting value] "
        "This isn't valid json.: 0"
    )
    assert result_status == 3


@responses.activate
def test_isup_handles_request_exception(fake_response_args):
    exc = RequestException("Exception message.")
    fake_response_args["body"] = exc

    responses.add(**fake_response_args)

    result_message, result_status = isup.isitup(__TEST_URL__)

    assert result_message == "RequestException: Exception message."
    assert result_status == 3
