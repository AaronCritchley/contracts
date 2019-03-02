
import math

from pytest import raises

from contracts import ContractNotRespected
from contracts.main import check_contracts


def test_constants_basic_sanity():
    assert check_contracts(['0'], [0]) == {}
    assert check_contracts(['1'], [1]) == {}

    with raises(ContractNotRespected):
        check_contracts(['1'], [2])
    
    assert check_contracts(['pi'], [math.pi]) == {}

    with raises(ContractNotRespected):
        check_contracts(['pi'], [math.pi * 2])


if __name__ == '__main__':
    import pytest
    pytest.main([__file__])
