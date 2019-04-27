
from pytest import raises

from contracts import ContractNotRespected
from contracts.main import check_contracts


def test_comparison_basic_sanity():
    assert check_contracts(['=0'], [0]) == {}
    assert check_contracts(['==0'], [0]) == {}

    with raises(ContractNotRespected):
        check_contracts(['=0'], [1])
    with raises(ContractNotRespected):
        check_contracts(['==0'], [1])

    assert check_contracts(['!=0'], [1]) == {}
    with raises(ContractNotRespected):
        check_contracts(['!=0'], [0])

    assert check_contracts(['>0'], [1]) == {}
    with raises(ContractNotRespected):
        check_contracts(['>0'], [0])
    with raises(ContractNotRespected):
        check_contracts(['>0'], [-1])

    assert check_contracts(['>=0'], [1]) == {}
    assert check_contracts(['>=0'], [0]) == {}
    with raises(ContractNotRespected):
        check_contracts(['>=0'], [-1])

    assert check_contracts(['<0'], [-1]) == {}
    with raises(ContractNotRespected):
        check_contracts(['<0'], [0])
    with raises(ContractNotRespected):
        check_contracts(['<0'], [+1])

    assert check_contracts(['<=0'], [-1]) == {}
    assert check_contracts(['<=0'], [0]) == {}
    with raises(ContractNotRespected):
        check_contracts(['<=0'], [+1])
    
    assert check_contracts(['<=1'], [1]) == {}
    assert check_contracts(['>=1'], [1]) == {}
    assert check_contracts(['=1'], [1]) == {}
    assert check_contracts(['<=1'], [0]) == {}


def test_comparison_incorrect_types():
    assert check_contracts(['=1'], [1]) == {}

    # with raises(ContractNotRespected):
    #     check_contracts(['=1'], [1])
    # with raises(ContractNotRespected):
    #     check_contracts(['=0'], [0])
    with raises(AssertionError):
        check_contracts(['>0'], [])


def test_comparison_binary_syntax():
    assert check_contracts(['1>0'], [None]) == {}
    with raises(ContractNotRespected):
        check_contracts(['1>1'], [None])

    assert check_contracts(['0<1'], [None]) == {}
    with raises(ContractNotRespected):
        check_contracts(['1<1'], [None])

    assert check_contracts(['1>=0'], [None]) == {}
    with raises(ContractNotRespected):
        check_contracts(['1>=2'], [None])

    assert check_contracts(['0<=1'], [None]) == {}
    with raises(ContractNotRespected):
        check_contracts(['2<=1'], [None])

    assert check_contracts(['1=1'], [None]) == {}
    with raises(ContractNotRespected):
        check_contracts(['1=0'], [None])

    assert check_contracts(['1==1'], [None]) == {}
    with raises(ContractNotRespected):
        check_contracts(['1==0'], [None])

    assert check_contracts(['0!=1'], [None]) == {}
    with raises(ContractNotRespected):
        check_contracts(['0!=0'], [None])
    
    assert check_contracts(['1+1>=0'], [None]) == {}
    with raises(ContractNotRespected):
        check_contracts(['0>=1+1'], [None])

    assert check_contracts(['1-1=0'], [None]) == {}
    with raises(ContractNotRespected):
        check_contracts(['1-1=1'], [None])

    assert check_contracts(['-1<=1-1'], [None]) == {}
    assert check_contracts(['3*2>=2*1'], [None]) == {}


if __name__ == '__main__':
    import pytest
    pytest.main([__file__])
