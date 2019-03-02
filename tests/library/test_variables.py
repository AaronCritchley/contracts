from pytest import raises

from contracts import ContractNotRespected
from contracts.main import check_contracts
from tests.utils import syntax_fail


def test_variables_only_single_letters():
    assert syntax_fail('NN')
    assert syntax_fail('xx')


def test_upper_case_can_only_bind_to_numbers():
    assert check_contracts(['N,N>0'], [1])
    with raises(ContractNotRespected):
        check_contracts(['N,N>0'], [0])

    with raises(ContractNotRespected):
        check_contracts(['N'], [[]])


def test_lower_case_can_bind_to_anything():
    assert check_contracts(['x'], [1])
    assert check_contracts(['x'], [[]])


if __name__ == '__main__':
    import pytest
    pytest.main([__file__])
