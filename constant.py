import inspect
import math
import typing

class Constant:
    _instance: typing.Optional['Constant'] = None

    def __new__(cls: type) -> 'Constant':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            globals()[ cls.__name__.upper()] = cls._instance
        else:
            print("Constant already exists.")
        return cls._instance

    def __str__(self: typing.Self) -> str:
        return f"{self.value:.10}"

    def __repr__(self: typing.Self) -> str:
        return f"{self.symbol} = {self.__str__()}"

    def _warn_and_return_self(self: typing.Self) -> 'Constant':
        print(f" This method '{inspect.stack()[1][3]}' is not allowed with a Constant.")
        return self

    def __mul__(self: typing.Self, other: float) -> float:
        return self.value * other

    def __rmul__(self: typing.Self, other: float) -> float:
        return other * self.value

    def __imul__(self: typing.Self, _: float) -> typing.Self:
        return self._warn_and_return_self()

@lambda _:_()
class Euler(Constant):
    def __init__(self: typing.Self) -> None:
        self.value: float = math.e
        self.symbol: str = "e"

@lambda _: _()
class Pi(Constant):
    def __init__(self: typing.Self) -> None:
        self.value: float = math.pi
        self.symbol: str = "π"

@lambda _: _()
class Ipsum(Constant):
    def __init__(self: typing.Self) -> None:
        self.value: str = "ipsum lodis"
        self.symbol: str = "latin"


print(EULER)
print(repr(EULER))
print(EULER * 5)
print(5 * EULER)
EULER *= 5
print(EULER)
EULER = 10
print(EULER)
print(PI)
print(repr(PI))
print(2 * IPSUM)

