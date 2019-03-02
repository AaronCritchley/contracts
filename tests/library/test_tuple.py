
from pytest import raises

from contracts import ContractNotRespected
from contracts.main import check_contracts
from tests.utils import syntax_fail


def test_tuple_basic_sanity():
    assert check_contracts(['tuple'], [()]) == {}
    assert check_contracts(['tuple'], [(1,)]) == {}

    # tuples and lists are different
    with raises(ContractNotRespected):
        check_contracts(['tuple'], [[]])
    with raises(ContractNotRespected):
        check_contracts(['list'], [()])

    # tuples can have the length
    assert check_contracts(['tuple[*]'], [(2, 2)]) == {}
    assert check_contracts(['tuple[1]'], [(1,)]) == {}

    # you cannot specify every element
    assert check_contracts(['tuple(*,*)'], [(1, 2)]) == {}
    assert check_contracts(['tuple(*)'], [(1,)]) == {}

    with raises(ContractNotRespected):
        check_contracts(['tuple(*,*)'], [(1, 2, 3)])


def test_tuple_multiple_args():
    assert check_contracts(['tuple(int,int)'], [(1, 2)])
    assert check_contracts(['tuple(int,float)'], [(1, 2.0)])

    with raises(ContractNotRespected):
        check_contracts(['tuple(float,float)'], [(1, 2.0)])

    assert check_contracts(['tuple(type(x),type(x))'], [(1, 2)])


def test_nested_tuples():
    assert check_contracts(['tuple(x,tuple(*,*,x))'], [(1, (2, 3, 1))])

    with raises(ContractNotRespected):
        check_contracts(['tuple(x,tuple(*,*,x))'], [(1, (2, 3, 2))])

    assert check_contracts(['tuple(type(x),tuple(*,*,type(x)))'], [(1, (2.1, 3.0, 3))])

    with raises(ContractNotRespected):
        check_contracts(['tuple(type(x),tuple(*,*,type(x)))'], [(1, (2.1, 3.0, 3.1))])

    # cannot specify both, even if coherent
    syntax_fail('tuple[*](*,*)')


def test_tuple_const_values():
    assert check_contracts(['tuple(0,1|2)'], [(0, 2)]) == {}
    assert check_contracts(['tuple(0,1|2)'], [(0, 2)]) == {}
    assert check_contracts(['tuple(0,1|2|3)'], [(0, 3)]) == {}
    assert check_contracts(['tuple(0,1|2|3,4)'], [(0, 3, 4)]) == {}

    with raises(ContractNotRespected):
        check_contracts(['tuple(0,1|2)'], [(0, 3)])

    assert check_contracts(['tuple(0,1,2)'], [(0, 1, 2)]) == {}
    assert check_contracts(['tuple(1|2,3)'], [(1, 3)]) == {}
    assert check_contracts(['tuple(1,(>2,int))'],[(1, 3)])

    with raises(ContractNotRespected):
        check_contracts(['tuple(1,(>2,int))'], [(1, 3.0)])

    assert check_contracts(['tuple(1,(*,*),2)'], [(1, 3, 2)]) == {}
    assert check_contracts(['tuple(str,(str[1],str))'], [('a', 'b')]) == {}


if __name__ == '__main__':
    import pytest
    pytest.main([__file__])

