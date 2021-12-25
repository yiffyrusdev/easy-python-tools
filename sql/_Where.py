from typing import Union

from ._Table import *


class Where:
    _operator = "????"

    def __init__(self, field1: 'TableField', field2: 'TableField'):
        self._left = field1
        self._right = field2

    def __str__(self) -> str:
        return f'({self._left.full_name} {self.__class__._operator} {self._right})'


class WhereEq(Where):
    _operator = "="


class WhereGt(Where):
    _operator = ">"


class WhereLt(Where):
    _operator = "<"


class WhereComposition(Where):
    _operator = "????"

    def __init__(self, *wheres: Union['Where', 'WhereComposition']):
        self._wheres = wheres

    def __str__(self) -> str:
        return f'({f" {self.__class__._operator} ".join(str(w) for w in self._wheres)})'


class WhereAND(WhereComposition):
    _operator = "AND"


class WhereOR(WhereComposition):
    _operator = "OR"