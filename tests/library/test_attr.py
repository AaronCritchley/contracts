
from pytest import raises

from contracts import ContractNotRespected
from contracts.main import check_contracts
from tests.utils import syntax_fail


class A(object):
    a = 1
    b = 2


class B(object):
    a = 2


def test_attr_basic_sanity():
    tc_a = A()
    tc_b = B()
    
    assert syntax_fail('attr')  # need at least some attribute
    
    assert check_contracts(['attr(a:*)'], [tc_a]) == {}
    assert check_contracts(['attr(a:int)'], [tc_a])
    assert check_contracts(['attr(b:int)'], [tc_a])
    assert check_contracts(['attr(b:>1)'], [tc_a]) == {}
    assert check_contracts(['attr(b:int,>1)'], [tc_a])
    with raises(ContractNotRespected):
        check_contracts(['attr(b:int,<=1)'], [tc_a])
    
    assert check_contracts(['attr(a:*)'], [tc_b]) == {}
    with raises(ContractNotRespected):
        check_contracts(['attr(b:*)'], [tc_b])


def test_attr_multiple_constraints():
    tc_a = A()

    assert check_contracts(['attr(a:int;b:int)'], [tc_a])
    assert check_contracts(['attr(a:int;b:int)'], [tc_a])
    assert check_contracts(['attr(a:int;b:int,>1)'], [tc_a])
    with raises(ContractNotRespected):
        check_contracts(['attr(a:int;b:int,<=1)'], [tc_a])


if __name__ == '__main__':
    import pytest
    pytest.main([__file__])
