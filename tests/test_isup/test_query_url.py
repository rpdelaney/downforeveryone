import urllib.parse

from downforeveryone import isup


def test_urljoin_called_once(mocker):
    mock_urllib_parse = mocker.patch.object(
        urllib.parse, "urljoin", autospec=True
    )
    isup._query_url("foo")
    mock_urllib_parse.assert_called_once_with(
        isup.API_URL["netloc"], isup.API_URL["path"] + "foo"
    )
