import argparse as _argparse

from downforeveryone import cli


def test_argparser_called(mocker):
    mocker.patch("argparse.ArgumentParser", autospec=True)
    cli.parse_args()

    _argparse.ArgumentParser.assert_called_once_with(
        prog="isup",
        description="checks if a site is down for everyone or just you",
    )
