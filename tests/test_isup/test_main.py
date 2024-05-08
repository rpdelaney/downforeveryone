import pytest

from downforeveryone import isup


def test_args_parsed(mock_cli_args, mock_isitup, mock_sys_exit):
    isup.main()

    mock_cli_args.assert_called_once_with()


def test_exit_code(mock_cli_args, mock_isitup, mock_sys_exit):
    mock_isitup.return_value = "", 5

    isup.main()

    mock_sys_exit.assert_called_once_with(5)


def test_exception_exits_3(mock_cli_args, mock_isitup, mock_sys_exit):
    mock_isitup.side_effect = Exception

    isup.main()

    mock_sys_exit.assert_called_once_with(3)


def test_exception_prints_traceback(
    mock_cli_args, mock_isitup, mock_sys_exit, mocker
):
    mock_isitup.side_effect = Exception
    mock_traceback = mocker.patch("traceback.print_exc")

    isup.main()

    mock_traceback.assert_called_once_with()


@pytest.mark.parametrize(
    ("message", "exit_code", "stdout", "stderr"),
    [
        ("test message", 0, "test message\n", ""),
        ("test message", 1, "test message\n", ""),
        ("test message", 3, "", "test message\n"),
    ],
)
def test_output(
    capsys,
    exit_code,
    message,
    mock_cli_args,
    mock_isitup,
    mock_sys_exit,
    stderr,
    stdout,
):
    mock_isitup.return_value = (message, exit_code)

    isup.main()
    out, err = capsys.readouterr()

    assert out == stdout
    assert err == stderr
