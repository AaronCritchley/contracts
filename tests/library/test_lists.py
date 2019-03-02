from pytest import raises

from contracts import ContractNotRespected
from contracts.main import check_contracts


def test_list_basic_sanity():
    assert check_contracts(['list'], [[]]) == {}

    with raises(ContractNotRespected):
        check_contracts(['list'], ['ciao'])

    assert check_contracts(['list[*]'], [[]]) == {}
    assert check_contracts(['list[*]'], [[1]]) == {}
    assert check_contracts(['list[*](*)'], [[1]]) == {}
    assert check_contracts(['list[*](float)'], [[1.0]])

    with raises(ContractNotRespected):
        check_contracts(['list[*](float)'], [[1]])
    assert check_contracts(['list[=1]'], [[0]]) == {}
    assert check_contracts(['list[=2]'], [[0, 1]]) == {}

    with raises(ContractNotRespected):
        check_contracts(['list[=2]'], [[0]])
    assert check_contracts(['list[1]'], [[0]]) == {}
    assert check_contracts(['list[2]'], [[0, 1]]) == {}

    with raises(ContractNotRespected):
        check_contracts(['list[2]'], [[0]])
    assert check_contracts(['list(int)'], [[]]) == {}
    assert check_contracts(['list(int)'], [[0, 1]])

    with raises(ContractNotRespected):
        check_contracts(['list(int)'], [[0, 'a']])
    with raises(ContractNotRespected):
        check_contracts(['list(int)'], [[0, 'a']])


def test_list_value_constraints():
    assert check_contracts(['list(int,>0)'], [[2, 1]])

    with raises(ContractNotRespected):
        check_contracts(['list(int,>0)'], [[0, 1]])

    assert check_contracts(['list(int,=0)'], [[0, 0]])


def test_list_parameterised_constraints():
    assert check_contracts(['list[N]'], [[]])
    assert check_contracts(['list[N],N>0'], [[1]])
    assert check_contracts(['list[N],N=1'], [[1]])
    assert check_contracts(['list[N],N>0,N<2'], [[1]])

    with raises(ContractNotRespected):
        check_contracts(['list[N],N>0'], [[]])


if __name__ == '__main__':
    import pytest
    pytest.main([__file__])
