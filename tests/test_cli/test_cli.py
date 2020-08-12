import pytest as _pytest

from downforeveryone import __version__, cli


@_pytest.fixture
def argparse_mock(mocker):
    return mocker.patch("argparse.ArgumentParser", autospec=True)


def test_argparser_called(argparse_mock):
    cli.parse_args()
    argparse_mock.assert_called_once_with(
        prog="isup",
        description="checks if a site is down for everyone or just you",
    )


def test_args_added(argparse_mock):
    cli.parse_args()
    mock_add_argument = argparse_mock.return_value.add_argument

    mock_add_argument.assert_any_call("url", help="url to test")
    mock_add_argument.assert_any_call(
        "--version", action="version", version=f"{__version__}"
    )

    assert mock_add_argument.call_count == 2
