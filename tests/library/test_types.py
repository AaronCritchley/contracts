
from pytest import raises

from contracts import ContractNotRespected
from contracts.main import check_contracts
from tests.utils import syntax_fail


def test_types_basic_sanity():
    assert check_contracts(['int'], [1])

    with raises(ContractNotRespected):
        check_contracts(['int'], [None])
    with raises(ContractNotRespected):
        check_contracts(['int'], [2.0])
    
    assert check_contracts(['float'], [1.1])

    with raises(ContractNotRespected):
        check_contracts(['float'], [None])
    with raises(ContractNotRespected):
        check_contracts(['float'], [2])
    
    assert check_contracts(['number'], [1])
    assert check_contracts(['number'], [1.0])

    with raises(ContractNotRespected):
        check_contracts(['number'], [[1]])
    
    assert check_contracts(['bool'], [False]) == {}
    assert check_contracts(['bool'], [True]) == {}

    with raises(ContractNotRespected):
        check_contracts(['bool'], [1])
    with raises(ContractNotRespected):
        check_contracts(['bool'], [0])


def test_types_none():
    assert check_contracts(['None'], [None])
    assert check_contracts(['NoneType'], [None])

    with raises(ContractNotRespected):
        check_contracts(['None'], [1])
    with raises(ContractNotRespected):
        check_contracts(['NoneType'], [1])


def test_types_type_func():
    syntax_fail('type')
    syntax_fail('type()')
    
    assert check_contracts(['type(x)'], [1])

    with raises(ContractNotRespected):
        check_contracts(['type(X)'], [1])


if __name__ == '__main__':
    import pytest
    pytest.main([__file__])
