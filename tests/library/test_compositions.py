
from pytest import raises

from contracts import ContractNotRespected
from contracts.main import check_contracts


def test_compositions_logical_and():
    with raises(ContractNotRespected):
        check_contracts(['=0,=1'], [0])
    assert check_contracts(['=0,>=0'], [0]) == {}


def test_compositions_logical_or():
    assert check_contracts(['=0|=1'], [0]) == {}
    assert check_contracts(['=0|=1'], [1]) == {}

    with raises(ContractNotRespected):
        check_contracts(['=0|=1'], [2])


def test_compositions_logical_not():
    with raises(ContractNotRespected):
        check_contracts(['!1'], [1])
    assert check_contracts(['!None'], [1])

    with raises(ContractNotRespected):
        check_contracts(['!(1|2)'], [1])
    assert check_contracts(['!(0|None)'], [3]) == {}


def test_compositions_multiple_consts_logical_or():
    assert check_contracts(['0|1|2'], [2]) == {}
    assert check_contracts(['0|1|2'], [1]) == {}

    assert check_contracts(['0|2'], [2]) == {}
    assert check_contracts(['0|1|2'], [2]) == {}
    assert check_contracts(['0|1|2|3'], [2]) == {}
    assert check_contracts(['0|1|2|3|4'], [2]) == {}
    assert check_contracts(['0|1|2|3|4|5'], [2]) == {}


def test_compositions_list_const_values():
    assert check_contracts(['list(0|1)'], [[0, 1, 0]]) == {}

    with raises(ContractNotRespected):
        check_contracts(['list(0|1)'], [[0, 1, 2]])


def test_compositions_precedence():
    assert check_contracts(['*|#'], [None]) == {}
    assert check_contracts(['*|(#,*)'], [None]) == {}
    assert check_contracts(['*|(*,#)'], [None]) == {}
    assert check_contracts(['*|*,#'], [None]) == {}

    with raises(ContractNotRespected):
        check_contracts(['(*|*),#'], [None])

    assert check_contracts(['*,*|#'], [None]) == {}
    assert check_contracts(['*,#|*'], [None]) == {}
    assert check_contracts(['*|#|*'], [None]) == {}

    with raises(ContractNotRespected):
        check_contracts(['*,#,*'], [None])
    with raises(ContractNotRespected):
        check_contracts(['*,#|#'], [None])

    assert check_contracts(['#|*,(#|*)'], [None]) == {}

    # ! has lower precedence than | or &
    assert check_contracts(['!#|*'], [None]) == {}

    with raises(ContractNotRespected):
        check_contracts(['!(#|*)'], [None])
    with raises(ContractNotRespected):
        check_contracts(['!*,#'], [None])

    assert check_contracts(['!(*,#)'], [None]) == {}


if __name__ == '__main__':
    import pytest
    pytest.main([__file__])
