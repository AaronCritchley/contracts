
from pytest import raises

from contracts import (check, ContractNotRespected, Contract, parse,
                       check_multiple, ContractSyntaxError, fail)


def test_check_1():
    res = check('tuple(int,int)', (2, 2))

    assert isinstance(res, dict)


def test_check_1a():
    with raises(ValueError):
        check(1, 2)


def test_parse_1():
    contract = parse('>0')
    assert isinstance(contract, Contract)
    contract.check(2)
    with raises(ContractNotRespected):
        contract.check('ciao')


def test_parse_2():
    with raises(ContractSyntaxError):
        parse('>>')


def test_check_2():
    with raises(ContractNotRespected):
        check('tuple(int,int)', (None, 2))


def test_check_3():
    with raises(ContractSyntaxError):
        check('tuple(>>int,int)', (None, 2))


def test_check_4():
    score = (2, None)
    msg = 'Player score must be a tuple of 2 int.'
    try:
        check('tuple(int,int)', score, msg)
    except ContractNotRespected as e:
        s = str(e)
        assert msg in s
    else:
        assert False


def test_repr_1():
    contract = parse(' list[N](int), N > 0')

    ("%s" % contract)   # => 'list[N](int),N>0'
    ("%r" % contract)   # => And([List(BindVariable('N',int),...


def test_binding():
    context = check('list[N](str), N>0', ['a', 'b', 'c'])

    assert 'N' in context
    assert context['N'] == 3


def test_check_multiple_1():

    data = [[1, 2, 3],
            [4, 5, 6]]
    row_labels = ['first season', 'second season']
    col_labels = ['Team1', 'Team2', 'Team3']

    spec = [('list[C](str),C>0', col_labels),
            ('list[R](str),R>0', row_labels),
            ('list[R](list[C])', data)]
    check_multiple(spec)

    # now with description 
    check_multiple(spec,
                    'I expect col_labels, row_labels, data to '
                    'have coherent dimensions.')

    data = [[1, 2, 3], [1, 2]]
    spec = [('list[C](str),C>0', col_labels),
            ('list[R](str),R>0', row_labels),
            ('list[R](list[C])', data)]

    with raises(ContractNotRespected):
        check_multiple(spec)

    with raises(ContractNotRespected):
        check_multiple(spec, 'my message')


def test_equality_contract():
    c1 = parse('list[C](str),C>0')
    c2 = parse('list[C](str),C>0')
    c3 = parse('list[R](str),R>0')
    assert c1 == c2
    assert c1 != c3


def test_equality_rvalue():
    c1 = parse('N+1')
    c2 = parse('N+2')
    c3 = parse('P+1')
    assert c1 == c1
    assert c2 == c2
    assert c3 == c3
    assert c1 != c2
    assert c1 != c3
    assert c2 != c3


def test_check_context():
    check('N', 1, N=1)
    fail('N', 1, N=2)

    with raises(ContractNotRespected):
        check('N', 1, N=2)

    with raises(ValueError):
        fail('N', 1, N=1)


def test_check_context2():
    """ Variable names must have only one letter. """
    with raises(ValueError):
        check('N', 1, NN=2)

    with raises(ValueError):
        check('N', 1, nn=2)


if __name__ == '__main__':
    import pytest
    pytest.main([__file__])
