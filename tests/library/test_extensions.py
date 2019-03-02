
from pytest import raises

from contracts import new_contract, ContractNotRespected
from contracts.main import check_contracts
from tests.utils import syntax_fail


@new_contract
def ext0_positive(value):
    return value > 0


@new_contract
def ext1_lessthan(value, threshold):
    return value < threshold


def test_extensions_basic_sanity():
    assert check_contracts(['ext0_positive'], [1])

    with raises(ContractNotRespected):
        check_contracts(['ext0_positive'], [-1])

    assert check_contracts(['ext1_lessthan(0)'], [-1])

    with raises(ContractNotRespected):
        check_contracts(['ext1_lessthan(0)'], [+1])


def test_extensions_named_argument():
    # named
    assert check_contracts(['ext1_lessthan(threshold=0)'], [-1])

    with raises(ContractNotRespected):
        check_contracts(['ext1_lessthan(threshold=0)'], [+1])


def test_extensions_failure_cases():
    # needs to fail parsing because we didn't provide argument
    syntax_fail('ext1_lessthan')
    # needs to fail parsing because the argument name is wrong
    syntax_fail('ext1_lessthan(th=0)')
    # too many arguments
    syntax_fail('ext1_lessthan(0,1)')


if __name__ == '__main__':
    import pytest
    pytest.main([__file__])
