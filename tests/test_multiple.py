
from pytest import raises

from contracts import ContractNotRespected
from contracts.main import check_contracts


def test_multiple_basic_sanity():
    assert check_contracts(['*'], [0]) == {}
    assert check_contracts(['*', '*'], [0, 1]) == {}
    assert check_contracts(['=0', '=1'], [0, 1]) == {}

    with raises(ContractNotRespected):
        check_contracts(['=0', '=1'], [0, 2])


def test_lists_of_equal_length():
    assert check_contracts(['list[N]', 'list[N]'], [[4], [3]])
    assert check_contracts(['list[N]', 'list[N]'], [[], []])
    with raises(ContractNotRespected):
        check_contracts(['list[N]', 'list[N]'], [[], [1]])

    assert check_contracts(['list[N]', 'list[N],N>0'], [[1], [3]])

    # we can also refer to the other context
    assert check_contracts(['list[N]', 'list,N>0'], [[1], [3]])
    with raises(ContractNotRespected):
        check_contracts(['list[N]', 'list,N>0'], [[], [3]])


def tests_lists_of_different_length():
    assert check_contracts(['list[N]', 'list[M],M!=N'], [[4], [3, 2]])
    assert check_contracts(['list[N]', 'list[M],M!=N'], [[4, 3], [3]])
    with raises(ContractNotRespected):
        check_contracts(['list[N]', 'list[M],M!=N'], [[3], [3]])


def test_one_list_shorter_than_the_other():
    assert check_contracts(['list[N]', 'list[M],M<N'], [[4, 3], [3]])
    assert check_contracts(['list[N]', 'list[M],N>M'], [[4, 3], [3]])
    with raises(ContractNotRespected):
        check_contracts(['list[N]', 'list[M],N>M'], [[3], [3]])


def test_values_of_the_same_type():
    assert check_contracts(['type(x)', 'type(x)'], [0, 1])
    assert check_contracts(['type(x)', 'type(x)'], [0.1, 1.1])
    with raises(ContractNotRespected):
        check_contracts(['type(x)', 'type(x)'], [0.1, 1])

    assert check_contracts(['type(x)', 'type(y)', 'type(x)|type(y)'], [0, 1.1, 1.2])
    assert check_contracts(['type(x)', 'type(y)', 'type(x)|type(y)'], [0, 1.1, 3])
    with raises(ContractNotRespected):
        check_contracts(['type(x)', 'type(y)', 'type(x)|type(y)'], [0, 1.1, 'ciao'])


def test_list_with_all_elements_of_the_same_type():
    assert check_contracts(['list(type(x))'], [[0, 1, 2]])
    with raises(ContractNotRespected):
        check_contracts(['list(type(x))'], [[0, 1.2, 2]])
    with raises(ContractNotRespected):
        check_contracts(['list(type(x))'], [[0, None, 2]])

    assert check_contracts(['list(type(x))', 'list(type(x))'], [[1, 2], [3, 4]])
    with raises(ContractNotRespected):
        check_contracts(['list(type(x))', 'list(type(x))'], [[1, 2], [3.0, 4]])

    assert check_contracts(['list(type(x))', 'list(type(y)),x=y'], [[1, 2], [3, 4]])
    with raises(ContractNotRespected):
        check_contracts(['list(type(x))', 'list(type(y)),x=y'], [[1, 2], [3.0, 4]])


def test_list_with_at_most_two_types():
    assert check_contracts(['list(type(x|y))'], [[1, 2, 3, 4.0]])
    with raises(ContractNotRespected):
        check_contracts(['list(type(x|y))'], [[1, 2, 'ciao', 4.0]])


if __name__ == '__main__':
    import pytest
    pytest.main([__file__])
