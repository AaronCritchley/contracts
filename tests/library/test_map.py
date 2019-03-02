
from pytest import raises

from contracts import ContractNotRespected
from contracts.main import check_contracts
from tests.utils import syntax_fail


def test_map_basic_sanity():
    assert check_contracts(['map'], [{}]) == {}

    with raises(ContractNotRespected):
        check_contracts(['map'], [1])
    with raises(ContractNotRespected):
        check_contracts(['map'], [[]])

    assert syntax_fail('map[]')
    assert syntax_fail('map[]()')
    assert syntax_fail('map()')

    assert check_contracts(['map[1]'], [{1: 2}]) == {}
    assert check_contracts(['map[N],N<2'], [{1: 2}])

    with raises(ContractNotRespected):
        check_contracts(['map[N],N<2'], [{1: 2, 3: 4}])

    assert check_contracts(['map(int:int)'], [{1: 2}])

    with raises(ContractNotRespected):
        check_contracts(['map(int:int)'], [{'a': 2}])

    assert check_contracts(['map(*:int)'], [{1: 2}])
    assert check_contracts(['map(*:int)'], [{'a': 2}])
    
    # mapionary of string -> tuple, with tuple of two elements with different type
    assert check_contracts(['map(str:tuple(type(x),type(y))),x!=y'], [{'a': (2, 1.1)}])

    with raises(ContractNotRespected):
        check_contracts(['map(str:tuple(type(x),type(y))),x!=y'], [{'a': (2, 1)}])


if __name__ == '__main__':
    import pytest
    pytest.main([__file__])
