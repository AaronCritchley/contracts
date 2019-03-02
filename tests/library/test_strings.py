
from pytest import raises

from contracts import ContractNotRespected
from contracts.main import check_contracts
from tests.utils import syntax_fail


def test_strings_basic_sanity():
    assert check_contracts(['str'], ['ciao']) == {}
    assert check_contracts(['string'], ['ciao']) == {}

    # Check sequences of chars are not str
    with raises(ContractNotRespected):
        check_contracts(['str'], [list('ciao')])

    # Can specify the length
    assert check_contracts(['str[N]'], [''])
    assert check_contracts(['str[1]'], ['a']) == {}
    assert check_contracts(['str[2]'], ['ab']) == {}
    assert check_contracts(['str[>0]'], ['ab']) == {}

    with raises(ContractNotRespected):
        check_contracts(['str[>0]'], [''])

    assert check_contracts(['str[N],N>3'], ['ciao'])

    with raises(ContractNotRespected):
        check_contracts(['str[N],N>3'], ['cia'])

    assert syntax_fail('str(*)')


if __name__ == '__main__':
    import pytest
    pytest.main([__file__])
