from numpy.testing import assert_array_equal

from contracts import contract
from contracts.interface import ContractNotRespected
from contracts.useful_contracts.numpy_specific import not_null
import numpy as np
import pandas as pd
from pytest import raises


#
# This should raise
#
# @contract
# def no_annotations(a, b):
#     return a + b


def test_annotations_only():
    @contract
    def annotations_only(a: pd.Series, b: int) -> pd.Series:
        return a + b

    # Confirm the contract rejects the wrong type.
    with raises(ContractNotRespected):
        arr = np.array([1, 2, 3])
        annotations_only(arr, 6)


def test_docstring_only():
    @contract
    def docstring_only(a, b):
        """
        :param a: first arg
        :type a: array[N]

        :param b: second arg
        :type b: int

        :rtype: array[N]
        """
        return a + b

    # Confirm the contract rejects the wrong type
    with raises(ContractNotRespected):
        s = pd.Series(range(5))
        docstring_only(s, 5)


def test_annotations_with_docstring():
    @contract
    def annotations_with_docstring(a, b: int):
        """
        :param a: first arg
        :type a: array[N], N>5

        :rtype: array[N], N>5
        """
        return a + b

    # Confirm the contract rejects non-integer values for `b`,
    # which confirms the type annotations are being checked
    with raises(ContractNotRespected):
        arr = np.array([1, 2, 3, 4, 5, 6])
        annotations_with_docstring(arr, 'blah')

    # Confirm the contract rejects arrays shorter than 5,
    # which confirms that the docstring contracts are being checked.
    with raises(ContractNotRespected):
        arr = np.array([1, 2, 3])
        annotations_with_docstring(arr, 10)

    # Confirm a valid array len > 5, values > 0
    # with an integer addition works as expected
    arr = np.array([1, 2, 3, 4, 5, 6])
    result = annotations_with_docstring(arr, 10)
    expected = np.array([11, 12, 13, 14, 15, 16])
    assert_array_equal(result, expected)


def test_both_annotations_and_docstring():
    @contract
    def both_annotations_and_docstring(a: pd.DataFrame, b: pd.DataFrame) -> pd.DataFrame:
        """
        :param a: first arg
        :type a: not_null

        :param b: second arg
        :type b: not_null
        """
        return a

    first = pd.DataFrame([[1, 2], [3, 4]], columns=['a', 'b'])
    second = pd.DataFrame([[5, 6], [7, 8]])

    result = both_annotations_and_docstring(first, second)
    assert result.sum().sum() == 10

    # Confirm that a null value in either of the dataframes results
    # in a `not respected` error that mentions the null check
    with raises(ContractNotRespected) as exc:
        bad = pd.DataFrame([[1, 2], [3, np.nan]], columns=['a', 'b'])
        both_annotations_and_docstring(bad, second)

    assert 'not_null' in str(exc.value)

    with raises(ContractNotRespected) as exc2:
        both_annotations_and_docstring(first, bad)

    assert 'not_null' in str(exc2.value)

    result = both_annotations_and_docstring(first, second)
    assert result.sum().sum() == 10

    # Confirm that non-dataframe inputs results in failures
    s_first = pd.Series(range(10))
    s_second = s_first.copy()
    with raises(ContractNotRespected) as exc3:
        _ = both_annotations_and_docstring(s_first, s_second)

    assert "Expected type 'DataFrame'" in str(exc3.value)


def test_return_values_basic_sanity():
    @contract
    def annotations_return_values(a: pd.Series, b: pd.Series) -> pd.Series:
        if a.sum() == 10:
            return "bad value"
        return a * b

    first = pd.Series([0, 1, 2, 3])
    second = pd.Series([1, 2, 3, 4])  # This one sums to 10

    # Confirm it works fine for valid inputs
    result = annotations_return_values(first, second)
    assert isinstance(result, pd.Series)
    assert result.iloc[1] == 2
    assert result.iloc[2] == 6

    # Confirm the type annotations are working
    with raises(ContractNotRespected) as exc1:
        annotations_return_values(5, 6)

    assert "Expected type 'Series'" in str(exc1.value)

    # Confirm invalid return values throw the correct error
    with raises(ContractNotRespected) as exc2:
        _ = annotations_return_values(second, first)

    assert "Breach for return value" in str(exc2.value)
    assert "Expected type 'Series', got <class 'str'>" in str(exc2.value)
    assert "'bad value'" in str(exc2.value)


def test_return_values_anns_and_docstrings():
    @contract
    def anns_and_docstring_return_values(a: int, b: float, c: str) -> list:
        """
        :param a: first param
        :type a: int,>5

        :param b: second param
        :type b: float,>10.0

        :param c: third param
        :type c: str[N],N>3

        :rtype: list[N]
        """
        if c == 'cccc':
            return 'bad value'
        if c == 'dddd':
            return ['d']
        return [c] * len(c)

    # Confirm valid properties don't raise
    result = anns_and_docstring_return_values(6, 20.0, 'blah')
    assert result == ['blah', 'blah', 'blah', 'blah']

    # Confirm value of `a` below 5 raises
    with raises(ContractNotRespected) as exc:
        anns_and_docstring_return_values(3, 20.0, 'blah')

    exc_value = str(exc.value)
    assert "Breach for argument 'a'" in exc_value
    assert "Condition 3 > 5 not respected" in exc_value

    # Confirm value of `b` below 10.0 raises
    with raises(ContractNotRespected) as exc2:
        anns_and_docstring_return_values(6, 5.0, 'blah')

    exc2_value = str(exc2.value)
    assert "Breach for argument 'b'" in exc2_value
    assert "Condition 5.0 > 10.0 not respected" in exc2_value

    # Confirm value of `c` smaller than 4 chars raises
    with raises(ContractNotRespected) as exc3:
        anns_and_docstring_return_values(10, 20.0, 'x')

    exc3_value = str(exc3.value)
    assert "Breach for argument 'c'" in exc3_value
    assert "Condition 1 > 3 not respected" in exc3_value

    # Confirm 'cccc' as the third param gives a bad return type
    # which breaks the annotation
    with raises(ContractNotRespected) as exc4:
        anns_and_docstring_return_values(20, 20.0, 'cccc')

    exc4_value = str(exc4.value)
    assert "Breach for return value" in exc4_value

    # Confirm `dddd` as third param gives a bad return value
    # which breaks the docstring contract
    with raises(ContractNotRespected) as exc5:
        anns_and_docstring_return_values(20, 20.0, 'dddd')

    exc5_value = str(exc5.value)
    assert "Breach for return value" in exc5_value
    assert "Expected value for 'N' was" in exc5_value


def test_not_null():
    arr = np.array([1, 2, 3, 4])
    assert not_null(arr)

    arr2 = np.array([1, 2, 3, 4, np.nan])
    assert not not_null(arr2)


if __name__ == '__main__':
    import pytest
    pytest.main([__file__])
