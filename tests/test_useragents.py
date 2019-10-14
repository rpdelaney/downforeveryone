import pytest as _pytest

from isup import useragents


@_pytest.mark.parametrize("execution_number", range(20))
def test_string_returned(execution_number):
    result = useragents.random_agent()
    assert isinstance(result, str)


def test_random_called_once(mocker):
    random_choice = mocker.patch("random.choice", autospec=True)
    useragents.random_agent()

    random_choice.assert_called_once_with(useragents.USER_AGENTS)
