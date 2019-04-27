
from pytest import raises

from contracts import (
    decorate, ContractException,
    contract, ContractNotRespected
)


def test_malformed():
    def f() -> "":
        pass

    with raises(ContractException):
        decorate(f)


def test_malformed2():
    def f() -> "okok":
        pass

    with raises(ContractException):
        decorate(f)


def test_malformed3():
    def f() -> 3:
        pass

    with raises(ContractException):
        decorate(f)


def test_not_specified1():
    """ No docstring specified, but annotation is. """
    def f() -> "int":
        pass

    decorate(f)


def test_parse_error1():
    def f(a: "int", b: "in"):
        pass

    with raises(ContractException):
        decorate(f)


def test_parse_error2():
    def f(a, b) -> "in":
        pass

    with raises(ContractException):
        decorate(f)


def not_supported2():
    """ Cannot do with **args """
    def f(a, **b):
        """
            :type a: int
            :rtype: int
        """
        pass

    with raises(ContractException):
        decorate(f)


def test_ok1():
    @contract
    def f(a, b):
        """ This is good
            :type a: int
            :type b: int
            :rtype: int
        """
        pass


def test_types1():
    @contract
    def f(a: int, b: int) -> int:
        return a + b

    assert f(1, 2) == 3

    with raises(ContractNotRespected):
        f(1.0, 2)

    with raises(ContractNotRespected):
        f(1, 2.0)


def test_types2():
    """ Testing return value contract """
    @contract
    def f(a: int, b: int) -> int:
        return (a + b) * 2.1

    with raises(ContractNotRespected):
        f(1, 2)


def test_kwargs():
    def f(a:int, b:int, c:int=7): #@UnusedVariable
        if c != b:
            raise Exception()


    f2 = decorate(f)
    f2(0, 7)
    f2(0, 5, 5)
    with raises(Exception):
        f2(0, 5, 4)

    with raises(Exception):
        f2(0, 5)


def test_varargs():
    def f(a, b, *c: tuple):
        assert c == (a, b)

    f2 = decorate(f)
    f2(0, 7, 0, 7)


def test_varargs2():
    def f(a, b, *c: """tuple"""

    ):
        assert c == (a, b)

    f2 = decorate(f)
    f2(0, 7, 0, 7)


def test_keywords():
    def f(A:int, B:int, **c: dict):
        assert c['a'] == A
        assert c['b'] == B

    f2 = decorate(f)
    f(0, 7, a=0, b=7)
    f2(0, 7, a=0, b=7)

    with raises(Exception):
        f2(0, 5, 0, 6)


if __name__ == '__main__':
    import pytest
    pytest.main([__file__])
