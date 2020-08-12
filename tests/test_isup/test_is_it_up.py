import json

import responses

from downforeveryone import isup

__TEST_URL__ = "https://foo.bar"


@responses.activate
def test_requests_dot_get_called_once(fake_response_args):
    responses.add(**fake_response_args)

    isup.isitup(__TEST_URL__)

    responses.assert_call_count(isup.query_url(__TEST_URL__), 1)


@responses.activate
def test_handle_response_called_once(fake_response_args, handle_response_mock):
    responses.add(**fake_response_args)

    isup.isitup(__TEST_URL__)

    handle_response_mock.assert_called_once_with(
        json.loads(fake_response_args["body"])
    )


@responses.activate
def test_isup_returns_handle_response(
    fake_response_args, handle_response_mock
):
    responses.add(**fake_response_args)

    return_value = isup.isitup(__TEST_URL__)

    assert return_value == handle_response_mock.return_value


@responses.activate
def test_isup_error_with_description(
    fake_response_args, handle_response_mock, capsys
):
    fake_response_args["status"] = 404
    responses.add(**fake_response_args)

    isup.isitup(__TEST_URL__)

    captured = capsys.readouterr()
    assert (
        captured.err == "HTTP request failure. Status: 404 "
        "Description: ['Nothing matches the given URI']\n"
    )


@responses.activate
def test_isup_handles_broken_json(fake_response_args):
    fake_response_args["body"] = "This isn't valid json."
    fake_response_args["status"] = 200

    responses.add(**fake_response_args)

    assert isup.isitup(__TEST_URL__) == 3
