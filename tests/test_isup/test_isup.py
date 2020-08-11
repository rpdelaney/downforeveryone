import urllib.parse

import pytest as _pytest

from downforeveryone import isup


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
            ({"statusCode": 429, "isDown": True}, 0),
            ({"statusCode": 200, "isDown": True}, 0),
            ({"statusCode": 200, "isDown": False}, 1),
            ({"statusCode": 200, "isDown": None}, 3),
            ({"statusCode": 200, "isDown": 0}, 3),
            ({"statusCode": 200, "isDown": 1}, 3),
            ({}, 3),
        ],
    )
    def test_return_values(self, response, expected):
        assert isup.handle_response(response) == expected

    @_pytest.mark.parametrize(
        ("response", "stdout", "stderr"),
        [
            ({"statusCode": 200, "isDown": True}, "down for everyone.\n", "",),
            ({"statusCode": 200, "isDown": False}, "just you.\n", ""),
            (
                {"statusCode": 200, "isDown": None},
                "",
                (
                    "There was a problem with the request. "
                    "response was:\n{'statusCode': 200, 'isDown': None}\n"
                ),
            ),
            ({"statusCode": 429, "isDown": True}, "down for everyone.\n", "",),
            (
                {
                    "statusCode": 530,
                    "statusText": "",
                    "isDown": True,
                    "returnedUrl": "http://otuhaeiudapcid.com",
                    "requestedDomain": "otuhaeiudapcid.com",
                    "lastChecked": 1592789590165,
                },
                "down for everyone.\n",
                "",
            ),
        ],
    )
    def test_output(self, response, stdout, stderr, capsys):
        isup.handle_response(response)
        out, err = capsys.readouterr()

        assert out == stdout
        assert err == stderr


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
