
from pytest import raises

from contracts import ContractNotRespected
from contracts.main import check_contracts


def test_wildcard_basic_sanity():
    assert check_contracts(['*'], [0]) == {}
    assert check_contracts(['*'], [[1]]) == {}
    assert check_contracts(['*'], [None]) == {}

    with raises(ContractNotRespected):
        check_contracts(['#'], [None])
    
    assert check_contracts(['*|#'], [None]) == {}

    with raises(ContractNotRespected):
        check_contracts(['*,#'], [None])


if __name__ == '__main__':
    import pytest
    pytest.main([__file__])
