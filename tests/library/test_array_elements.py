import numpy
from pytest import raises

from contracts import ContractNotRespected
from contracts.main import check_contracts


def test_array_elements_basic_sanity():
    arr01 = numpy.array([0, 1, 0, 1])
    arr012 = numpy.array([0, 1, 0, 2])

    assert check_contracts(['array(=0|=1|=2)'], [arr01]) == {}
    assert check_contracts(['array(=0|=1|=2)'], [arr012]) == {}
    assert check_contracts(['array(=0|=1)'], [arr01]) == {}
    with raises(ContractNotRespected):
        check_contracts(['array(=0|=1)'], [arr012])


def test_array_elements_boolean_or():
    arr124 = numpy.array([1, 2, 4])
    arr125 = numpy.array([1, 2, 5])

    assert check_contracts(['array(=4|>=0,<=2)'], [arr124]) == {}
    assert check_contracts(['array(=5|>=0,<=2)'], [arr125]) == {}
    with raises(ContractNotRespected):
        check_contracts(['array(=4|>=2,<=0)'], [arr124])


def test_array_elements_zeros():
    arr01int16 = numpy.zeros((3,), 'int16')

    assert check_contracts(['array(int16,(=0|=1))'], [arr01int16]) == {}


if __name__ == '__main__':
    import pytest
    pytest.main([__file__])
