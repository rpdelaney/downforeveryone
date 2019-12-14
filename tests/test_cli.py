import pytest as _pytest
from downforeveryone import cli


@_pytest.fixture
def argparse_mock(mocker):
    return mocker.patch("argparse.ArgumentParser", autospec=True)


def test_argparser_called(argparse_mock):
    cli.parse_args()
    argparse_mock.assert_called_once_with(
        prog="isup",
        description="checks if a site is down for everyone or just you",
    )


def test_only_url_arg_added(argparse_mock):
    cli.parse_args()

    argparse_mock.return_value.add_argument.assert_called_once_with(
        "url", help="url to test"
    )
