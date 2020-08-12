import responses

from downforeveryone import isup

__TEST_URL__ = "https://foo.bar"


@responses.activate
def test_requests_dot_get_called_once(fake_response_args):
    responses.add(**fake_response_args)

    isup.isitup(__TEST_URL__)

    responses.assert_call_count(isup.query_url(__TEST_URL__), 1)


def test_handle_response_called_once(requests_get_mock, handle_response_mock):
    isup.isitup(__TEST_URL__)

    handle_response_mock.assert_called_once_with(
        requests_get_mock.return_value.json()
    )


def test_isup_returns_handle_response(requests_get_mock, handle_response_mock):
    return_value = isup.isitup(__TEST_URL__)

    assert return_value == handle_response_mock.return_value


def test_isup_error_with_description(
    requests_get_mock, handle_response_mock, mock_request_failure, capsys,
):
    requests_get_mock.return_value = mock_request_failure

    isup.isitup(__TEST_URL__)

    captured = capsys.readouterr()
    assert (
        captured.err == "HTTP request failure. Status: 404 "
        "Description: ['Nothing matches the given URI']\n"
    )


def test_isup_handles_broken_json(
    requests_get_mock, handle_response_mock, mock_request_failure
):
    requests_get_mock.return_value = mock_request_failure

    assert isup.isitup(__TEST_URL__) == 3
