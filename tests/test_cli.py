from downforeveryone import cli


def test_argparser_called(mocker):
    argparse_mock = mocker.patch("argparse.ArgumentParser", autospec=True)
    cli.parse_args()

    argparse_mock.assert_called_once_with(
        prog="isup",
        description="checks if a site is down for everyone or just you",
    )
