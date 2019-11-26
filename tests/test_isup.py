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
