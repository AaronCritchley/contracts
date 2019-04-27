
from pytest import raises

from contracts import ContractNotRespected
from contracts.main import check_contracts


def test_aliases_basic_sanity():
    assert check_contracts(['Container'], [[]]) 
    
    with raises(ContractNotRespected):
        check_contracts(['Container'], [1])
    assert check_contracts(['Hashable'], [1])
    assert check_contracts(['Iterable'], [[]]) 
    
    with raises(ContractNotRespected):
        check_contracts(['Iterable'], [1])
    assert check_contracts(['Iterable'], [{}])
    assert check_contracts(['Iterator'], [[].__iter__()])

    with raises(ContractNotRespected):
        check_contracts(['Iterator'], [[]])

    assert check_contracts(['Sized'], [[]])
    assert check_contracts(['Sized'], [{}])
    
    with raises(ContractNotRespected):
        check_contracts(['Sized'], [lambda: None])

    assert check_contracts(['Sized'], [''])
    assert check_contracts(['Callable'], [lambda: None])
    
    with raises(ContractNotRespected):
        check_contracts(['Callable'], [[]])
        
    assert check_contracts(['Sequence'], [[]])
    assert check_contracts(['Sequence'], [(1,)])
    assert check_contracts(['Sequence'], [''])
    
    with raises(ContractNotRespected):
        check_contracts(['Sequence'], [{}])
    
    assert check_contracts(['Set'], [set([])])
    
    with raises(ContractNotRespected):
        check_contracts(['Set'], [[]])
        
    assert check_contracts(['MutableSequence'], [[]])
    
    with raises(ContractNotRespected):
        check_contracts(['MutableSequence'], [(1,)])
        
    assert check_contracts(['MutableSet'], [set([])])
    
    with raises(ContractNotRespected):
        check_contracts(['MutableSet'], [frozenset([])])
        
    assert check_contracts(['Mapping'], [{}])
    
    with raises(ContractNotRespected):
        check_contracts(['Mapping'], [[]])
    
    assert check_contracts(['MutableMapping'], [{}])
    #assert check_contracts(['MappingView', {}.keys())
    #assert check_contracts(['ItemsView', {}.items())
    #assert check_contracts(['ValuesView', {}.values())


if __name__ == '__main__':
    import pytest
    pytest.main([__file__])
