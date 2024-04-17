from __future__ import annotations
from typing import Callable, Generic, Optional, TypeVar

from func import double


_T = TypeVar("_T")
_U = TypeVar("_U")

class Array(Generic[_T]):
    def __init__(self, data: Optional[list[_T]] = None) -> None:
        self.data = data or []

    def push(self, datum: _T) -> None:
        self.data.append(datum)

    def pop(self) -> _T:
        return self.data.pop()

    def map(self, func: Callable[[_T], _U]) -> Array[_U]:
        return Array([func(d) for d in self.data])

    def filter(self, func: Callable[[_T], bool]) -> Array[_T]:
        return Array([d for d in self.data if func(d)])

    def reduce(self, func: Callable[[_U, _T], _U], initial: _U) -> _U:
        result = initial
        for d in self.data:
            result = func(result, d)
        return result

    def __repr__(self) -> str:
        return f"Array({self.data})"


def _strings() -> None:
    # note the explicit type
    array = Array[str]() # equivalent to array: Array[str] = Array()
    array.push("hi")
    array.push("bye")

    output = array \
        .map(lambda x: x.upper()) \
        .reduce(_delimit(", "), "") 

    print(output)


def _ints() -> None:
    # note the implicit type
    array = Array([1, 2, 3])

    # get the odds, double them, and sum them
    output = array \
        .filter(lambda x: x % 2 == 1) \
        .map(double) \
        .reduce(lambda acc, x: acc + x, 0) 

    print(output)

def _more() -> None:
    array = Array([1, 2, 3])

    # get the odds, double them, and sum them
    output = array \
        .map(lambda x: f"{x}") \
        .map(double) \
        .reduce(_delimit("-"), "") 

    print(output)

def _delimit(delimiter: str):
    def func(a: str, b: str) -> str:
        if a and b:
            return f"{a}{delimiter}{b}"
        else:
            return f"{a}{b}"
    return func


if __name__ == "__main__":
    _strings()
    _ints()
    _more()