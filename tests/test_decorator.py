
from pytest import raises

from contracts import (
    decorate, contract,
    ContractException, ContractNotRespected
)
from contracts.interface import MissingContract


def test_malformed():
    def f():
        """
            Wrong syntax

            :rtype okok
        """
        pass

    with raises(ContractException):
        decorate(f)


def test_malformed2():
    def f():
        """
            Wrong syntax

            :rtype: okok
        """
        pass

    with raises(ContractException):
        decorate(f)


def test_not_specified1():
    """ No docstring specified """
    def f():
        pass

    with raises(ContractException):
        decorate(f)


def test_not_specified2():
    def f():
        """ No types specified in the docstring """
        pass

    with raises(ContractException):
        decorate(f)


def test_too_many():
    def f():
        """
            Too many rtype clauses.
            :rtype: int
            :rtype: int
        """
        pass

    with raises(ContractException):
        decorate(f)


def test_invalid1():
    def f(a):
        """ Unknown b.
            :type a: int
            :type b: int
        """
        pass

    with raises(ContractException):
        decorate(f)


def test_parse_error1():
    def f(a, b):
        """ Same with optional
            :type a: in
            :type b: int
        """
        pass

    with raises(ContractException):
        decorate(f)


def test_parse_error2():
    def f(a, b):
        """ Same with optional
            :type a: int
            :type b: int
            :rtype: in
        """
        pass

    with raises(ContractException):
        decorate(f)


def not_supported1():
    """ Support of *args """

    def f(a, *b):  # @UnusedVariable
        """
            :type a: int
            :type b: tuple(int)
            :rtype: int
        """
        pass

        decorate(f)


def not_supported2():
    """ Support of **args """
    def f(a, **b):
        """
            :type a: int
            :type b: dict(int:int)
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


def test_ok3():
    """ Trying the quoting thing. """
    @contract
    def f(a, b):
        """ This is good
            :type a: ``int``
            :type b: ``int``
            :rtype: ``int``
        """
        pass


def test_bad_quoting():
    def f(a, b):
        """
            :type a: ``int``
            :type b: ``int``
            :rtype: ``int`
        """
        pass

    with raises(ContractException):
        decorate(f)


def test_bad_quoting2():
    def f(a, b):
        """
            :type a: ``int``
            :type b: `int``
            :rtype: ``int``
        """
        pass

    with raises(ContractException):
        decorate(f)


def test_ok2():
    @contract(a='int', returns='int')
    def f(a, b):
        pass


def test_invalid_args():
    def f():
        @contract(1)
        def g(a, b):
            return int(a + b)
    with raises(ContractException):
        f()


def test_invalid_args2():
    """ unknown parameter """
    def f():
        @contract(c=2)
        def g(a, b):
            return int(a + b)
    with raises(ContractException):
        f()


def test_check_it_works1():
    @contract(a='int', b='int', returns='int')
    def f(a, b):  # @UnusedVariable
        return 2.0

    with raises(ContractNotRespected):
        f(1, 2)


def test_check_it_works2():
    @contract(a='int', b='int', returns='int')
    def f(a, b):  # @UnusedVariable
        return a + b
    f(1, 2)
    with raises(ContractNotRespected):
        f(1.0, 2)

    with raises(ContractNotRespected):
        f(1, 2.0)


def test_check_it_works2b():
    """ Nothing for b """
    @contract(a='int', returns='int')
    def f(a, b):  # @UnusedVariable
        return int(a + b)
    f(1, 2)
    f(1, 2.0)


def test_check_it_works2c():
    """ Nothing for b """
    def f1(a, b):  # @UnusedVariable
        return int(a + b)

    f = decorate(f1, a='int', returns='int')

    f(1, 2)
    f(1, 2.0)
    with raises(ContractNotRespected):
        f(1.0, 2)

# def test_module_as_decorator():
#     import contracts as contract_module
#
#     @contract_module
#     def f(a, b): #@UnusedVariable
#         return a + b
#     f(1, 2)
#     with raises(ContractNotRespected, f, 1.0, 2)


def test_check_it_works3():
    @contract
    def f(a, b):
        """ This is good
            :type a: int
            :type b: int
            :rtype: int
        """
        return a + b
    f(1, 2)
    with raises(ContractNotRespected):
        f(1.0, 2)

    with raises(ContractNotRespected):
        f(1, 2.0)


def test_inline_docstring_format_works():
    @contract
    def f(a, b):
        """ This is good
            :param int,>0 a: Description
            :param int,>0 b: Description
            :returns int,>0: Description
        """
        return a + b
    f(1, 2)
    with raises(ContractNotRespected):
        f(1.0, 2)
    with raises(ContractNotRespected):
        f(-1, 2)


def test_check_docstring_maintained():
    def f1(a, b):
        """ This is good
            :type a: int
            :type b: int
            :rtype: int
        """
        return a + b

    def f2(string):
        pass

    f1_dec = decorate(f1)
    assert f1.__doc__ != f1_dec.__doc__
    assert f1.__name__ == f1_dec.__name__
    assert f1.__module__ == f1_dec.__module__

    f2_dec = decorate(f2, string='str')
    assert f2.__doc__ != f2_dec.__doc__
    assert f2.__name__ == f2_dec.__name__
    assert f2.__module__ == f2_dec.__module__

    f1_dec_p = decorate(f1, modify_docstring=False)
    assert f1_dec_p.__doc__ == f1.__doc__

    f2_dec_p = decorate(f2, modify_docstring=False, string='str')
    assert f2.__doc__ == f2_dec_p.__doc__

    @contract
    def f1b(a, b):
        """ This is good
            :type a: int
            :type b: int
            :rtype: int
        """
        return a + b

    @contract(string='str')
    def f2b(string):
        pass

    @contract(modify_docstring=False)
    def f1b_p(a, b):
        """ This is good
            :type a: int
            :type b: int
            :rtype: int
        """
        return a + b

    @contract(modify_docstring=False, string='str')
    def f2b_p(string):
        pass

    assert f1.__doc__ != f1b.__doc__
    assert f1.__doc__ == f1b_p.__doc__
    assert f2.__doc__ != f2b.__doc__
    assert f2.__doc__ == f2b_p.__doc__


def test_kwargs():
    def f(a, b, c=7):  # @UnusedVariable
        """ Same with optional
            :type a: int
            :type b: int
            :type c: int
        """
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
    def f(a, b, *c):
        """ Same with optional
            :type a: int
            :type b: int
            :type c: tuple
        """
        assert c == (a, b)

    f2 = decorate(f)
    f2(0, 7, 0, 7)


def test_keywords():
    def f(A, B, **c):
        """ Same with optional
            :type A: int
            :type B: int
            :type c: dict
        """
        assert c['a'] == A
        assert c['b'] == B

    f2 = decorate(f)
    f(0, 7, a=0, b=7)
    f2(0, 7, a=0, b=7)

    with raises(Exception):
        f2(0, 5, 0, 6)


def test_same_signature():
    from inspect import getargspec

    def f(a):
        return a

    @contract(a='int')
    def f2(a):
        return a

    assert getargspec(f2) == getargspec(f)


def test_empty_types():

    def x():
        @contract
        def f(myparam):
            """
            :param myparam: something
            """

    with raises(MissingContract):
        x()


def test_empty_types2():

    @contract
    def f(x):
        """
        :param x: something
        :type x: *
        """

    f(1)


if __name__ == '__main__':
    import pytest
    pytest.main([__file__])
