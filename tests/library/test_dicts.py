
from pytest import raises

from contracts import ContractNotRespected
from contracts.main import check_contracts
from tests.utils import syntax_fail


def test_dicts_basic_sanity():
    assert check_contracts(['dict'], [{}]) == {}

    with raises(ContractNotRespected):
        check_contracts(['dict'], [1])
    with raises(ContractNotRespected):
        check_contracts(['dict'], [[]])

    syntax_fail('dict[]')
    syntax_fail('dict[]()')
    syntax_fail('dict()')

    assert check_contracts(['dict[1]'], [{1: 2}]) == {}
    assert check_contracts(['dict[N],N<2'], [{1: 2}])

    with raises(ContractNotRespected):
        check_contracts(['dict[N],N<2'], [{1: 2, 3: 4}])

    assert check_contracts(['dict(int:int)'], [{1: 2}])

    with raises(ContractNotRespected):
        check_contracts(['dict(int:int)'], [{'a': 2}])

    assert check_contracts(['dict(*:int)'], [{1: 2}])
    assert check_contracts(['dict(*:int)'], [{'a': 2}])


def test_dicts_nested_constraints():
    # dictionary of string -> tuple, with tuple of two elements with different type
    assert check_contracts(['dict(str:tuple(type(x),type(y))),x!=y'], [{'a': (2, 1.1)}])

    with raises(ContractNotRespected):
        check_contracts(['dict(str:tuple(type(x),type(y))),x!=y'], [{'a': (2, 1)}])


if __name__ == '__main__':
    import pytest
    pytest.main([__file__])
