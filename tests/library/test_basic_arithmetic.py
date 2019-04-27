
from pytest import raises

from contracts import ContractNotRespected
from contracts.main import parse_contract_string

from tests.utils import syntax_fail


def test_syntax_equals_plus():
    assert syntax_fail('=1+')


def test_syntax_equals_minus():
    assert syntax_fail('=1-')


def test_syntax_equals_mul():
    assert syntax_fail('=1*')


def test_syntax_ints():
    assert parse_contract_string('=%r' % 1)
    assert parse_contract_string('%r' % 1)
    assert parse_contract_string('=%r' % -1)
    assert parse_contract_string('%r' % -1)


def test_syntax_floats():
    assert parse_contract_string('=%r' % 1.0)
    assert parse_contract_string('%r' % 1.0)
    assert parse_contract_string('=%r' % 1e10)
    assert parse_contract_string('%r' % 1e10)


def test_syntax_integer_arithmetic():
    # TODO : these `.check()` calls should return
    #        a boolean for testing purposes
    value = parse_contract_string('=2')
    value.check(2)

    with raises(ContractNotRespected):
        value.check(3)

    eq_one_plus_one = parse_contract_string('=1+1')
    eq_one_plus_one.check(2)

    with raises(ContractNotRespected):
        value.check(5)

    one_plus_one = parse_contract_string('1+1')
    one_plus_one.check(2)

    with raises(ContractNotRespected):
        value.check(10)

    eq_one_minus_one = parse_contract_string('=1-1')
    eq_one_minus_one.check(0)

    with raises(ContractNotRespected):
        value.check(0)

    one_minus_one = parse_contract_string('1-1')
    one_minus_one.check(0)

    with raises(ContractNotRespected):
        value.check(-1)

# unary operators
#
# good('N,-N=-1', 1)
#
# good(['N', 'N-1'], [1, 0])
# good(['N', 'N+1'], [1, 2])
#
# good(['N', 'N-1'], [1, 0])
# good(['N', 'N*4'], [1, 4])
# good(['N', 'Y,N==Y+1'], [5, 4])
#
# # Checking precedence
# good('1+2*3', 7)
# good('2*3+1', 7)
# # Now with parentheses
# good('=1+1*3', 4)
# good('=(1+1)*3', 6)
#
# good('1+1+1', 3)
# good('2*2*2', 8)
# good('2-1-1', 0)
#
# # Wrong math
# fail('x,x+1=0', 'ciao')
# fail('x,-x=0', 'ciao')
#
# # Binding to non-existing variable
# fail('N+1=0', 1)


if __name__ == '__main__':
    import pytest
    pytest.main([__file__])
