import urllib.parse

import pytest as _pytest

from downforeveryone import __version__
from downforeveryone import isup


def test_version():
    assert __version__ == "0.1.0"


class TestUrlJoin:
    @_pytest.mark.parametrize(
        ("url", "expected"),
        [
            ("google.com", "https://api.downfor.cloud/httpcheck/google.com"),
            ("8.8.8.8", "https://api.downfor.cloud/httpcheck/8.8.8.8"),
        ],
    )
    def test_urljoin(self, url, expected):
        assert isup.query_url(url) == expected


class TestQueryUrl:
    def test_raises_typerror(self):
        with _pytest.raises(TypeError):
            isup.query_url(0)  # type: ignore

    def test_urljoin_called_once(self, mocker):
        urllib_parse_mock = mocker.patch.object(
            urllib.parse, "urljoin", autospec=True
        )
        isup.query_url("foo")
        urllib_parse_mock.assert_called_once_with(
            isup.__API_URL__["netloc"], isup.__API_URL__["path"] + "foo"
        )


class TestResponseHandler:
    @_pytest.mark.parametrize(
        ("response", "expected"),
        [
            ({"isDown": True}, 0),
            ({"isDown": False}, 1),
            ({"isDown": None}, 3),
            ({"isDown": 0}, 3),
            ({"isDown": 1}, 3),
            ({}, 3),
        ],
    )
    def test_return_values(self, response, expected):
        assert isup.handle_response(response) == expected

    @_pytest.mark.parametrize(
        ("response", "stdout", "stderr"),
        [
            ({"isDown": True}, "down for everyone.\n", ""),
            ({"isDown": False}, "just you.\n", ""),
            (
                {"isDown": None},
                (
                    "There was a problem with the request. "
                    "response was:\n{'isDown': None}\n"
                ),
                "",
            ),
        ],
    )
    def test_output(self, response, stdout, stderr, capsys):
        isup.handle_response(response)
        out, err = capsys.readouterr()

        assert out == stdout
        assert err == stderr


class TestIsUp:
    def test_requests_dot_get_called_once(self, mocker):
        requests_get_mock = mocker.patch("requests.get", autospec=True)
        test_url = "https://foo.bar"

        isup.isitup(test_url)

        requests_get_mock.assert_called_once_with(
            isup.query_url(test_url), headers=isup.__QUERY_HEADERS__,
        )

    def test_handle_response_called_once(self, mocker):
        requests_get_mock = mocker.patch("requests.get")
        handle_response_mock = mocker.patch(
            "downforeveryone.isup.handle_response", autospec=True
        )
        test_url = "https://foo.bar"

        isup.isitup(test_url)

        handle_response_mock.assert_called_once_with(
            requests_get_mock.return_value.json()
        )

    def test_isup_returns_handle_response(self, mocker):
        mocker.patch("requests.get")
        handle_response_mock = mocker.patch(
            "downforeveryone.isup.handle_response", autospec=True
        )
        test_url = "https://foo.bar"

        return_value = isup.isitup(test_url)

        assert return_value == handle_response_mock.return_value
