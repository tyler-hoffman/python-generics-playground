from __future__ import annotations
from typing import Generic, Optional, TypeVar


_T = TypeVar("_T")

class Array(Generic[_T]):
    def __init__(self, data: Optional[list[_T]] = None) -> None:
        self.data = data or []

    def push(self, datum: _T) -> None:
        self.data.append(datum)

    def pop(self) -> _T:
        return self.data.pop()

    def __repr__(self) -> str:
        return f"Array({self.data})"


def _strings() -> None:
    # note the explicit type
    array = Array[str]() # equivalent to array: Array[str] = Array()
    array.push("hi")
    array.push("bye")

    print(array)


def _ints() -> None:
    # note the implicit type
    array = Array([1, 2, 3])

    print(array)

if __name__ == "__main__":
    _strings()
    _ints()