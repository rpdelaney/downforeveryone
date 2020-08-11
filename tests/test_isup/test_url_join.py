import pytest as _pytest

from downforeveryone import isup


@_pytest.mark.parametrize(
    ("url", "expected"),
    [
        ("google.com", "https://api.downfor.cloud/httpcheck/google.com"),
        ("8.8.8.8", "https://api.downfor.cloud/httpcheck/8.8.8.8"),
    ],
)
def test_urljoin(url, expected):
    assert isup.query_url(url) == expected
