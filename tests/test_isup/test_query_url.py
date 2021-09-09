import urllib.parse

import pytest as _pytest

from downforeveryone import isup


def test_raises_typerror():
    with _pytest.raises(TypeError):
        isup._query_url(0)


def test_urljoin_called_once(mocker):
    mock_urllib_parse = mocker.patch.object(
        urllib.parse, "urljoin", autospec=True
    )
    isup._query_url("foo")
    mock_urllib_parse.assert_called_once_with(
        isup.__API_URL__["netloc"], isup.__API_URL__["path"] + "foo"
    )
