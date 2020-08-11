from downforeveryone import isup


def test_args_parsed(cli_args_mock, isitup_mock, sys_exit_mock):
    isup.main()

    cli_args_mock.assert_called_once_with()


def test_exit_code(cli_args_mock, isitup_mock, sys_exit_mock):
    isup.main()

    sys_exit_mock.assert_called_once_with(isitup_mock.return_value)


def test_exception_exits_3(cli_args_mock, isitup_mock, sys_exit_mock):
    isitup_mock.side_effect = Exception

    isup.main()

    sys_exit_mock.assert_called_once_with(3)


def test_exception_prints_traceback(
    cli_args_mock, isitup_mock, sys_exit_mock, mocker
):
    isitup_mock.side_effect = Exception
    traceback_mock = mocker.patch("traceback.print_exc")

    isup.main()

    traceback_mock.assert_called_once_with()
