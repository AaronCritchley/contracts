from numpy import zeros, ones
import numpy as np
from pytest import raises

from contracts import ContractNotRespected
from contracts.main import check_contracts
from contracts.library.array import (
    np_int_dtypes, np_uint_dtypes, 
    np_float_dtypes)
from tests.utils import syntax_fail

a_u8 = np.zeros((3, 4), dtype='uint8')
a_i8 = np.zeros((3, 4), dtype='int8')
a_u16 = np.zeros((3, 4), dtype='uint16')
a_i16 = np.zeros((3, 4), dtype='int16')
a_u32 = np.zeros((3, 4), dtype='uint32')
a_i32 = np.zeros((3, 4), dtype='int32')
a_f32 = np.zeros((3, 4), dtype='float32')
a_f64 = np.zeros((3, 4), dtype='float64')
a_bool = np.zeros((3, 4), dtype='bool')

a0d = np.zeros((), dtype='float32')
a1d = np.zeros((2,))
a2d = np.zeros((2, 4,))
a3d = np.zeros((2, 4, 8))


def test_array_basic_sanity():
    # ## Strings
    assert check_contracts(['array'], [a_f32]) == {}
    assert check_contracts(['array'], [a_f64]) == {}

    # will be canonicalized to "array"
    assert check_contracts(['ndarray'], [a_f32]) == {}
    assert check_contracts(['ndarray'], [a_f64]) == {}
    with raises(AssertionError):
        check_contracts(['array'], [0, 1])

    # dtypes
    assert check_contracts(['array(uint8)'], [a_u8]) == {}
    assert check_contracts(['array(u1)'], [a_u8]) == {}
    assert check_contracts(['array(int8)'], [a_i8]) == {}
    assert check_contracts(['array(i1)'], [a_i8]) == {}
    assert check_contracts(['array(float32)'], [a_f32]) == {}
    assert check_contracts(['array(float64)'], [a_f64]) == {}
    assert check_contracts(['array(bool)'], [a_bool]) == {}

    with raises(ContractNotRespected):
        check_contracts(['array(float64)'], [a_f32])
    with raises(ContractNotRespected):
        check_contracts(['array(float32)'], [a_f64])
    with raises(ContractNotRespected):
        check_contracts(['array(uint8)'], [a_f32])
    with raises(ContractNotRespected):
        check_contracts(['array(float32)'], [a_u8])


def test_array_shapes():
    assert check_contracts(['shape[0]'], [a0d]) == {}
    assert check_contracts(['shape[1]'], [a1d]) == {}
    assert check_contracts(['shape[2]'], [a2d]) == {}
    assert check_contracts(['shape[3]'], [a3d]) == {}

    with raises(ContractNotRespected):
        check_contracts(['shape[>0]'], [a0d])
    with raises(ContractNotRespected):
        check_contracts(['shape[<1]'], [a1d])
    with raises(ContractNotRespected):
        check_contracts(['shape[>2]'], [a2d])
    with raises(ContractNotRespected):
        check_contracts(['shape[<3]'], [a3d])

    assert check_contracts(['shape[x]', 'shape[y],x=y'], [a3d, a3d])
    assert check_contracts(['shape[x]', 'shape[y],x=y'], [a2d, a2d])
    assert check_contracts(['shape[x]', 'shape[y],x=y'], [a1d, a1d])
    assert check_contracts(['shape[x]', 'shape[y],x=y'], [a0d, a0d])
    
    assert check_contracts(['array[2x4]'], [a2d]) == {}
    with raises(ContractNotRespected):
        check_contracts(['array[AxBxC]'], [a2d])
    with raises(ContractNotRespected):
        check_contracts(['array[2x4]'], [a3d])
    
    assert check_contracts(['array[HxW],H=2,W>3'], [a2d])
    assert check_contracts(['array[(=2)x(>3)]'], [a2d]) == {}
    
    # ellipsis to mean 0 or more dimensions 
    assert check_contracts(['array[2x4x...]'], [a2d]) == {}
    assert check_contracts(['array[2x4x...]'], [a3d]) == {}

    # if we really want more, use:
    assert check_contracts(['shape[>2],array[2x4x...]'], [a3d]) == {}
    with raises(ContractNotRespected):
        check_contracts(['shape[>2],array[2x4x...]'], [a2d])
    with raises(AssertionError):
        check_contracts(['shape[>2]'], [2, 2, 3])


def test_multi_binding():
    assert check_contracts(['array[XxYx...],X=2,Y=4'], [a3d])

    assert syntax_fail('array[2x...x3]')
    assert syntax_fail('array[2x...x3]')

    assert check_contracts(['array[XxYx...],X=2,Y=4'], [a2d])
    assert check_contracts(['array[XxYx...],X=2,Y=4'], [a3d])


def test_array_fixed_size():
    v1d = np.zeros(100)
    v2d = np.zeros((10, 10))
    assert check_contracts(['array[100]'], [v1d]) == {}
    with raises(ContractNotRespected):
        check_contracts(['array[100]'], [v2d])

    assert check_contracts(['array[10x10]'], [v2d]) == {}
    with raises(ContractNotRespected):
        check_contracts(['array[10x...]'], [v1d])

    assert check_contracts(['array[10x...]'], [v2d]) == {}


def test_array_shape_less_than_greater_than():
    with raises(ContractNotRespected):
        check_contracts(['shape[>0]'], [a0d])
    with raises(ContractNotRespected):
        check_contracts(['shape[<1]'], [a1d])
    with raises(ContractNotRespected):
        check_contracts(['shape[>2]'], [a2d])
    with raises(ContractNotRespected):
        check_contracts(['shape[<3]'], [a3d])

    assert check_contracts(['shape[0]'], [a0d]) == {}
    assert check_contracts(['shape[1]'], [a1d]) == {}
    assert check_contracts(['shape[2]'], [a2d]) == {}
    assert check_contracts(['shape[3]'], [a3d]) == {}

    # TODO: check this
    # assert check_contracts(['array[shape[3]]', a3d)


def test_array_fixed_size_different_cardinality():
    assert check_contracts(['array[1x2]'], [zeros((1, 2))]) == {}


def test_array_comparisons():
    # Now: special comparisons for arrays
    a = np.array([0, 1, 2])
    b = np.array([10, 20, 30])
    assert check_contracts(['array(>=0)'], [a]) == {}
    assert check_contracts(['array(<=2)'], [a]) == {}
    with raises(ContractNotRespected):
        check_contracts(['array(<=20)'], [b])

    assert check_contracts(['array(=0)'], [zeros(10)]) == {}
    with raises(ContractNotRespected):
        check_contracts(['array(=0)'], [np.array([0, 1, 0])])
    assert check_contracts(['array(=1)'], [ones(10)]) == {}

    assert check_contracts(['shape(x)', 'shape(x)'], [a2d, a2d])
    with raises(ContractNotRespected):
        check_contracts(['shape(x)', 'shape(x)'], [a2d, a3d])

    assert check_contracts(['array[NxN](<=1)'], [np.ones((10, 10))])
    assert check_contracts(['array[NxN](<=1,float32)'], [np.ones((10, 10), dtype='float32')])
    assert check_contracts(['array[NxN](<=1,float32|float64)'], [np.ones((10, 10), dtype='float64')])
    assert check_contracts(['array[NxN](<=1,(float32|float64))'],
         [np.ones((10, 10), dtype='float64')])
    assert check_contracts(['array[NxN](<=1,>=1)'], [np.ones((10, 10))])


def test_array_boolean_comparisons():
    assert check_contracts(['array[(2|3)xN]'], [np.ones((2, 10))])
    assert check_contracts(['array[(2|3)xN]'], [np.ones((3, 10))])
    with raises(ContractNotRespected):
        check_contracts(['array[(2|3)xN]'], [np.ones((4, 10))])

    assert check_contracts(['array[(2|3)x...]'], [np.ones((2, 10))]) == {}
    assert check_contracts(['array[(2|3)x...]'], [np.ones((3, 10))]) == {}
    with raises(ContractNotRespected):
        check_contracts(['array[(2|3)x...]'], [np.ones((4, 10))])

    assert check_contracts(['array[(2,*)xN]'], [np.ones((2, 10))])
    with raises(ContractNotRespected):
        check_contracts(['array[(2,3)xN]'], [np.ones((4, 10))])
    assert check_contracts(['array[(2,*)x...]'], [np.ones((2, 10))]) == {}
    with raises(ContractNotRespected):
        check_contracts(['array[(2,3)x...]'], [np.ones((4, 10))])

    assert check_contracts(['seq'], [np.ones(3)]) == {}
    assert check_contracts(['seq[3]'], [np.ones(3)]) == {}
    with raises(ContractNotRespected):
        check_contracts(['seq[3]'], [np.ones(2)])
    assert check_contracts(['seq[6]'], [np.ones((2, 3))]) == {}
    with raises(ContractNotRespected):
        check_contracts(['seq[6]'], [np.ones((2, 4))])


def test_array_finite():
    assert check_contracts(['finite'], [1])
    assert check_contracts(['finite'], [0])
    assert check_contracts(['finite'], [-1])
    assert check_contracts(['finite'], [np.float(1)])
    with raises(ContractNotRespected):
        check_contracts(['finite'], [np.inf])
    with raises(ContractNotRespected):
        check_contracts(['finite'], [np.nan])


def test_array_multiple_constraints():
    assert check_contracts(['array[N](>=-pi,<pi)'], [np.array([0], 'float32')])
    assert check_contracts(['array[N](>=0)'], [np.array([0], 'float32')])
    assert check_contracts(['array(float)'], [np.array(1.32, 'float32')]) == {}


def test_array_int_dtypes():
    for dt in np_int_dtypes:
        x = np.array(1).astype(dt)
        assert check_contracts(['number'], [x])
        with raises(ContractNotRespected):
            check_contracts(['Number'], [x])

        assert check_contracts(['array(int)'], [x]) == {}
        assert check_contracts(['int'], [x])

        with raises(ContractNotRespected):
            check_contracts(['Int'], [x])
        with raises(ContractNotRespected):
            check_contracts(['array(float)'], [x])
        with raises(ContractNotRespected):
            check_contracts(['float'], [x])
        with raises(ContractNotRespected):
            check_contracts(['Float'], [x])
    

def test_array_float_dtypes_all():
    for dt in np_float_dtypes:
        x = np.array(1).astype(dt)
        assert check_contracts(['number'], [x])

        with raises(ContractNotRespected):
            check_contracts(['Number'], [x])
        with raises(ContractNotRespected):
            check_contracts(['array(int)'], [x])
        with raises(ContractNotRespected):
            check_contracts(['int'], [x])
        with raises(ContractNotRespected):
            check_contracts(['Int'], [x])

        assert check_contracts(['array(float)'], [x]) == {}
        assert check_contracts(['float'], [x])

        with raises(ContractNotRespected):
            check_contracts(['Float'], [x])


def test_array_uint_dtypes():
    for dt in np_uint_dtypes:
        x = np.array(1).astype(dt)
        assert check_contracts(['number'], [x])

        with raises(ContractNotRespected):
            check_contracts(['Number'], [x])
        with raises(ContractNotRespected):
            check_contracts(['array(int)'], [x])
        with raises(ContractNotRespected):
            check_contracts(['int'], [x])
        with raises(ContractNotRespected):
            check_contracts(['Int'], [x])

        assert check_contracts(['array(uint)'], [x]) == {}

        with raises(ContractNotRespected):
            check_contracts(['Int'], [x])
        with raises(ContractNotRespected):
            check_contracts(['array(float)'], [x])
        with raises(ContractNotRespected):
            check_contracts(['float'], [x])
        with raises(ContractNotRespected):
            check_contracts(['Float'], [x])


if __name__ == '__main__':
    import pytest
    pytest.main([__file__])
