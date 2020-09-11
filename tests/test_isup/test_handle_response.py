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
    assert isup._handle_response(response)[1] == expected


@_pytest.mark.parametrize(
    ("fake_response", "expected_message", "expected_status"),
    [
        (
            {"statusCode": 200, "isDown": True},
            "down for everyone.",
            0,
        ),
        (
            {"statusCode": 200, "isDown": False},
            "just you.",
            1,
        ),
        (
            {"statusCode": 200, "isDown": None},
            (
                "There was a problem with the request. "
                "response was:\n{'statusCode': 200, 'isDown': None}"
            ),
            3,
        ),
        (
            {"statusCode": 429, "isDown": True},
            "down for everyone.",
            0,
        ),
        (
            {
                "statusCode": 530,
                "statusText": "",
                "isDown": True,
                "returnedUrl": "http://otuhaeiudapcid.com",
                "requestedDomain": "otuhaeiudapcid.com",
                "lastChecked": 1592789590165,
            },
            "down for everyone.",
            0,
        ),
    ],
)
def test_output(fake_response, expected_message, expected_status):
    result_message, result_status = isup._handle_response(fake_response)

    assert result_message == expected_message
    assert result_status == expected_status
