import pickle

from .utils import check_contracts_fail
from contracts import ContractNotRespected, parse, Contract


def test_exceptions_are_pickable():
    for contract, value, exact in semantic_fail_examples:  # @UnusedVariable
        yield check_contracts_fail, contract, value, ContractNotRespected
    for contract, value, exact in contract_fail_examples:  # @UnusedVariable
        yield check_contracts_fail, contract, value, ContractNotRespected


def check_contract_pickable(contract):
    c = parse(contract)
    assert isinstance(c, Contract)
    try:
        s = pickle.dumps(c)
        c2 = pickle.loads(s)
    except TypeError as e:
        msg = 'Could not pickle contract.\n'
        msg += '- string: %s\n' % c
        msg += '-   repr: %r\n' % c
        msg += 'Exception: %s' % e
        raise Exception(msg)

    assert c == c2


def test_contracts_are_pickable():
    allc = (good_examples + semantic_fail_examples + contract_fail_examples)
    for contract, _, _ in allc:
        if isinstance(contract, list):
            for c in contract:
                yield check_contract_pickable, c
        else:
            yield check_contract_pickable, contract


if __name__ == '__main__':
    import pytest
    pytest.main([__file__])
