
from pytest import raises

from contracts import ContractNotRespected
from contracts.main import check_contracts


def test_isinstance_basic_sanity():
    class BaseClass():
        pass
    
    class SubClass(BaseClass):
        pass

    assert check_contracts(['isinstance(BaseClass)'], [BaseClass()]) == {}
    assert check_contracts(['isinstance(BaseClass)'], [SubClass()]) == {}
    assert check_contracts(['isinstance(SubClass)'], [SubClass()]) == {}

    with raises(ContractNotRespected):
        check_contracts(['isinstance(SubClass)'], [BaseClass()])


def test_isinstance_object_base():
    class BaseClass2(object):
        pass
    
    class SubClass2(BaseClass2):
        pass
    
    assert check_contracts(['isinstance(BaseClass2)'], [BaseClass2()]) == {}
    assert check_contracts(['isinstance(BaseClass2)'], [SubClass2()]) == {}
    assert check_contracts(['isinstance(SubClass2)'], [SubClass2()]) == {}

    with raises(ContractNotRespected):
        check_contracts(['isinstance(SubClass2)'], [BaseClass2()])


def test_isinstance_3_level():
    class BaseClass3():
        pass
    
    class MidClass3(BaseClass3):
        pass
    
    class SubClass3(MidClass3):
        pass
    
    assert check_contracts(['isinstance(BaseClass3)'], [BaseClass3()]) == {}
    assert check_contracts(['isinstance(BaseClass3)'], [SubClass3()]) == {}
    assert check_contracts(['isinstance(SubClass3)'], [SubClass3()]) == {}

    with raises(ContractNotRespected):
        check_contracts(['isinstance(SubClass3)'], [BaseClass3()])


def test_isinstance_3_level_object():
    class BaseClass4(object):
        pass
    
    class MidClass4(BaseClass4):
        pass
    
    class SubClass4(MidClass4):
        pass
    
    assert check_contracts(['isinstance(BaseClass4)'], [BaseClass4()]) == {}
    assert check_contracts(['isinstance(BaseClass4)'], [SubClass4()]) == {}
    assert check_contracts(['isinstance(SubClass4)'], [SubClass4()]) == {}

    with raises(ContractNotRespected):
        check_contracts(['isinstance(SubClass4)'], [BaseClass4()])


if __name__ == '__main__':
    import pytest
    pytest.main([__file__])
