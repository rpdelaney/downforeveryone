import pytest as _pytest

from downforeveryone import isup


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
def test_return_values(response, expected):
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
def test_output(response, stdout, stderr, capsys):
    isup.handle_response(response)
    out, err = capsys.readouterr()

    assert out == stdout
    assert err == stderr
