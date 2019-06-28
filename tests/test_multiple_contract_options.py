import pytest
from pytest import raises

from contracts import contract, ContractNotRespected


def test_can_only_run_docstring():
    # Type annotations intentionally bad
    @contract(_evaluate_annotations=False)
    def add_float_and_int(a: str, b: dict) -> set:
        """
        :type a: int
        :type b: float
        :rtype: float
        """
        return a + b

    assert add_float_and_int(1, 2.5) == 3.5

    bad_inputs = [
        (10, 20),
        (3.3, 6.6),
        ('junk', 'junk')
    ]

    for arg_a, arg_b in bad_inputs:
        with raises(ContractNotRespected):
            add_float_and_int(arg_a, arg_b)


def test_can_only_run_annotations():
    # Docstring intentionally bad
    @contract(_evaluate_docstring=False)
    def add_float_and_int(a: int, b: float) -> float:
        """
        :type a: dict
        :type b: str
        :rtype: set
        """
        return a + b

    assert add_float_and_int(1, 2.5) == 3.5

    bad_inputs = [
        (10, 20),
        (3.3, 6.6),
        ('junk', 'junk')
    ]

    for arg_a, arg_b in bad_inputs:
        with raises(ContractNotRespected):
            add_float_and_int(arg_a, arg_b)


def test_default_runs_both():
    @contract
    def add_two_ints(a: int, b: int) -> int:
        """
        :type a: int,<5
        :type b: int,<10
        :rtype: int
        """
        return a + b

    assert add_two_ints(4, 8) == 12

    bad_inputs = [
        (10, 20),
        (3.3, 6.6),
        ('junk', 'junk'),
        (7, 2),
        (1, 12),
    ]

    for arg_a, arg_b in bad_inputs:
        with raises(ContractNotRespected):
            add_two_ints(arg_a, arg_b)


def test_no_evaluation_of_skipped_contract():
    '''Invalid contracts shouldn't be an issue if we're skipping evaluation'''
    @contract(_evaluate_annotations=False)
    def invalid_annotations(a: 'not_a_valid_contract'):
        '''
        :type a: int
        '''
        return a ** 2

    @contract(_evaluate_docstring=False)
    def invalid_docs(a: int):
        '''
        :type a: not_a_valid_contract
        '''
        return a ** 2

    # And just to make sure, they should obviously be callable as normal as well.
    assert invalid_annotations(10) == 100
    assert invalid_docs(20) == 400


if __name__ == '__main__':
    pytest.main([__file__, '-s'])
