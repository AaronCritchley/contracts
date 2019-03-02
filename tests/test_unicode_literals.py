# encoding: utf-8

from contracts import contract
from contracts.library import Extension
from contracts.main import parse_contract_string

name = 'helló wörld from one'


def test_unicode_literal():
    result = parse_contract_string(u'int')
    assert result == Extension('int')


def test_unicode_literal2():
    @contract(x='string')
    def f(x):
        pass

    f('')


if __name__ == '__main__':
    import pytest
    pytest.main([__file__])
