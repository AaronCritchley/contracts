
from pytest import raises

from contracts import ContractNotRespected
from contracts.main import check_contracts


def test_separate_context_basic_sanity():
    # dictionary of string -> tuple, with tuple of two elements with different type
    # In this case, each value should have the same two types
    assert check_contracts(['dict(str:tuple(type(x),type(y))),x!=y'], [{'a': (2, 1.1)}])
    
    with raises(ContractNotRespected):
        check_contracts(
            ['dict(str:tuple(type(x),type(y))),x!=y'], 
            [{'a': (2, 1)}]
        )


def test_separate_context_order_of_types():
    # This fails because we have x=int,y=float followed by float,int
    with raises(ContractNotRespected):
        check_contracts(
            ['dict(str:tuple(type(x),type(y))),x!=y'], 
            [{'a': (2, 1.1), 'b': (1.1, 2)}]
        )


def test_separate_context_no_match():
    # Here we force the context to not match using $(...) 
    assert check_contracts(['dict(str:$(tuple(type(x),type(y)),x!=y))'],
                           [{'a': (2, 1.1), 'b': (1.1, 2)}]) == {}
    
    with raises(ContractNotRespected):
        check_contracts(
            ['dict(str:$(tuple(type(x),type(y)),x!=y))'], 
            [{'a': (2, 1)}]
        )


if __name__ == '__main__':
    import pytest
    pytest.main([__file__])
