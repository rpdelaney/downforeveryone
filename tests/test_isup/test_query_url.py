import urllib.parse

import pytest as _pytest

from downforeveryone import isup


def test_raises_typerror():
    with _pytest.raises(TypeError):
        isup._query_url(0)  # type: ignore


def test_urljoin_called_once(mocker):
    urllib_parse_mock = mocker.patch.object(
        urllib.parse, "urljoin", autospec=True
    )
    isup._query_url("foo")
    urllib_parse_mock.assert_called_once_with(
        isup.__API_URL__["netloc"], isup.__API_URL__["path"] + "foo"
    )
