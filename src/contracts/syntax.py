from numbers import Number
# All the imports from pyparsing go here
from pyparsing import (delimitedList, Forward, Literal, stringEnd, nums, Word, #@UnusedImport
    CaselessLiteral, Combine, Optional, Suppress, OneOrMore, ZeroOrMore, opAssoc, #@UnusedImport
    operatorPrecedence, oneOf, ParseException, ParserElement, alphas, alphanums) #@UnusedImport

ParserElement.enablePackrat()

from .interface import SimpleRValue, Where


class ParsingTmp:
    current_filename = None 
    contract_types = []
    rvalues_types = []

def add_contract(x):
    ParsingTmp.contract_types.append(x)
    
def add_rvalue(x):  
    ParsingTmp.rvalues_types.append(x)

def W(string, location):
    return Where(ParsingTmp.current_filename, string, location)

def get_xor(l):
    tmp = l[0]
    for i in range(1, len(l)):
        tmp = tmp.__xor__(l[i])
    return tmp

def get_or(l):
    tmp = l[0]
    for i in range(1, len(l)):
        tmp = tmp.__or__(l[i])
    return tmp

O = Optional
S = Suppress

number = Word(nums) 
point = Literal('.')
e = CaselessLiteral('E')
plusorminus = Literal('+') | Literal('-')
integer = Combine(O(plusorminus) + number)
floatnumber = Combine(integer + O(point + O(number)) + O(e + integer))
integer.setParseAction(lambda tokens: SimpleRValue(int(tokens[0])))
floatnumber.setParseAction(lambda tokens: SimpleRValue(float(tokens[0])))

isnumber = lambda x: isinstance(x, Number)

rvalue = Forward()
contract = Forward()
simple_contract = Forward()


# Import all expressions -- they will call add_contract() and add_rvalue()
from .library import EqualTo, Unary, Binary, composite_contract, identifier_contract


operand = integer | floatnumber | get_or(ParsingTmp.rvalues_types)

rvalue << operatorPrecedence(operand, [
             ('-', 1, opAssoc.RIGHT, Unary.parse_action),
             ('*', 2, opAssoc.LEFT, Binary.parse_action),
             ('-', 2, opAssoc.LEFT, Binary.parse_action),
             ('+', 2, opAssoc.LEFT, Binary.parse_action),
          ])

add_contract(rvalue.copy().setParseAction(EqualTo.parse_action))

# Try to parse the string normally; then try identifiers
#add_contract(identifier_contract)
#simple_contract << get_xor(ParsingTmp.contract_types)

simple_contract << (get_xor(ParsingTmp.contract_types) | identifier_contract)

par = S('(') + contract + S(')') 
contract << ((par ^ composite_contract ^ simple_contract)) # Parentheses before << !!

