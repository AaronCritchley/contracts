import io

from pytest import raises

from contracts import ContractNotRespected
from contracts.main import check_contracts

from tests.utils import syntax_fail


def test_file_basic_sanity():
    assert check_contracts(['file'], [io.IOBase()]) == {}
    
    with raises(ContractNotRespected):
        check_contracts(['file'], [1])
    with raises(ContractNotRespected):
        check_contracts(['file'], [[]])
        
    syntax_fail('file[]')
    syntax_fail('file[]()')
    syntax_fail('file()')


if __name__ == '__main__':
    import pytest
    pytest.main([__file__])

