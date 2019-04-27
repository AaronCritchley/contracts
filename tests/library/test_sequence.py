from pytest import raises

from contracts import ContractNotRespected
from contracts.main import check_contracts


def test_sequences_basic_sanity():
    assert check_contracts(['seq'], [[]]) == {}
    assert check_contracts(['seq'], [()]) == {}
    assert check_contracts(['seq'], ['ciao']) == {}
    with raises(ContractNotRespected):
        check_contracts(['seq'], [{}])

    # assert check_contracts(['seq[*]'], [[]]) # Should this be an AssertionError?
    assert check_contracts(['seq[*]'], [[1]]) == {}
    assert check_contracts(['seq[*](*)'], [[1]]) == {}
    assert check_contracts(['seq[*](float)'], [[1.0]])
    with raises(ContractNotRespected):
        check_contracts(['seq[*](float)'], [[1]])

    assert check_contracts(['seq[*]'], [()]) == {}
    assert check_contracts(['seq[*]'], [(1,)]) == {}
    assert check_contracts(['seq[*](*)'], [(1,)]) == {}
    assert check_contracts(['seq[*](float)'], [(1.0,)])
    with raises(ContractNotRespected):
        check_contracts(['seq[*](float)'], [(1,)])


def test_sequences_equality():
    assert check_contracts(['seq[=1]'], [[0]]) == {}
    assert check_contracts(['seq[=2]'], [[0, 1]]) == {}

    with raises(ContractNotRespected):
        check_contracts(['seq[=2]'], [[0]])

    assert check_contracts(['seq[1]'], [[0]]) == {}
    assert check_contracts(['seq[2]'], [(0, 1)]) == {}

    with raises(ContractNotRespected):
        check_contracts(['seq[2]'], [(0,)])


def test_sequences_length_variable():
    assert check_contracts(['seq[N]'], [[]])
    assert check_contracts(['seq[N],N>0'], [[1]])
    assert check_contracts(['seq[N],N=1'], [[1]])
    assert check_contracts(['seq[N],N>0,N<2'], [[1]])

    with raises(ContractNotRespected):
        check_contracts(['seq[N],N>0'], [[]])

    assert check_contracts(['seq[N]'], [()])
    assert check_contracts(['seq[N],N>0'], [(1,)])
    assert check_contracts(['seq[N],N=1'], [(1,)])
    assert check_contracts(['seq[N],N>0,N<2'], [(1,)])

    with raises(ContractNotRespected):
        check_contracts(['seq[N],N>0'], [()])


if __name__ == '__main__':
    import pytest
    pytest.main([__file__])
