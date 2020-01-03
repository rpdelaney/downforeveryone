import urllib.parse

import pytest as _pytest

from downforeveryone import __version__, isup

__TEST_URL__ = "https://foo.bar"


@_pytest.fixture
def requests_get_mock(mocker):
    return mocker.patch("requests.get", autospec=True)


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


def test_version():
    assert __version__ == "0.1.2"


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
    def test_requests_dot_get_called_once(self, requests_get_mock):
        isup.isitup(__TEST_URL__)

        requests_get_mock.assert_called_once_with(
            isup.query_url(__TEST_URL__), headers=isup.__QUERY_HEADERS__,
        )

    def test_handle_response_called_once(
        self, requests_get_mock, handle_response_mock
    ):
        isup.isitup(__TEST_URL__)

        handle_response_mock.assert_called_once_with(
            requests_get_mock.return_value.json()
        )

    def test_isup_returns_handle_response(
        self, requests_get_mock, handle_response_mock
    ):
        return_value = isup.isitup(__TEST_URL__)

        assert return_value == handle_response_mock.return_value


class TestMain:
    def test_args_parsed(self, cli_args_mock, isitup_mock, sys_exit_mock):
        isup.main()

        cli_args_mock.assert_called_once_with()

    def test_exit_code(self, cli_args_mock, isitup_mock, sys_exit_mock):
        isup.main()

        sys_exit_mock.assert_called_once_with(isitup_mock.return_value)

    def test_exception_exits_3(
        self, cli_args_mock, isitup_mock, sys_exit_mock
    ):
        isitup_mock.side_effect = Exception

        isup.main()

        sys_exit_mock.assert_called_once_with(3)

    def test_exception_prints_traceback(
        self, cli_args_mock, isitup_mock, sys_exit_mock, mocker
    ):
        isitup_mock.side_effect = Exception
        traceback_mock = mocker.patch("traceback.print_exc")

        isup.main()

        traceback_mock.assert_called_once_with()
