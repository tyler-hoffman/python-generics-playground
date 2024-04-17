from typing import TypeVar


_T_Multipliable = TypeVar("_T_Multipliable", int, str)

def double(x: _T_Multipliable) -> _T_Multipliable:
    return x * 2

if __name__ == "__main__":
    output_1 = double(2) # 4
    output_2 = double("hi") # "hihi

    print(output_1)
    print(output_2)