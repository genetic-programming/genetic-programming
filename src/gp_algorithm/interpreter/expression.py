from __future__ import annotations


class Expression:
    def __init__(
        self,
        literal_value: bool | int,
    ) -> None:
        self._value = literal_value

    def __bool__(self) -> bool:
        if isinstance(self._value, bool):
            return self._value
        if isinstance(self._value, int):
            return bool(self._value)
        raise NotImplementedError("Unknown expression type")

    def __int__(self) -> int:
        if isinstance(self._value, int):
            return self._value
        if isinstance(self._value, bool):
            return int(self._value)
        raise NotImplementedError("Unknown expression type")

    def __str__(self) -> str:
        if isinstance(self._value, bool):
            return str(self._value).lower()
        if isinstance(self._value, int):
            return str(self._value)
        raise NotImplementedError("Unknown expression type")

    def __repr__(self) -> str:
        if isinstance(self._value, bool):
            return f"bool: {str(self._value).lower()}"
        if isinstance(self._value, int):
            return f"int: {str(self._value)}"
        raise NotImplementedError("Unknown expression type")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Expression):
            raise NotImplementedError(f"Cannot compare {self} and {other}")
        return self._value == other._value

    # unary operators
    def __neg__(self) -> Expression:
        return Expression(-int(self))

    def __invert__(self) -> Expression:
        return Expression(not bool(self))

    # arithmetic operators
    def __add__(self, other: object) -> Expression:
        if not isinstance(other, Expression):
            raise NotImplementedError(f"Cannot add {self} and {other}")
        return Expression(int(self) + int(other))

    def __sub__(self, other: object) -> Expression:
        if not isinstance(other, Expression):
            raise NotImplementedError(f"Cannot subtract {self} and {other}")
        return Expression(int(self) - int(other))

    def __mul__(self, other: object) -> Expression:
        if not isinstance(other, Expression):
            raise NotImplementedError(f"Cannot multiply {self} and {other}")
        return Expression(int(self) * int(other))

    def __truediv__(self, other: object) -> Expression:
        if not isinstance(other, Expression):
            raise NotImplementedError(f"Cannot divide {self} and {other}")
        try:
            return Expression(int(self) // int(other))
        except ZeroDivisionError:
            return Expression(int(self))

    # comparison operators
    def is_greater_than(self, other: object) -> Expression:
        if not isinstance(other, Expression):
            raise NotImplementedError(f"Cannot compare {self} and {other}")
        return Expression(int(self) > int(other))

    def is_equal(self, other: object) -> Expression:
        if not isinstance(other, Expression):
            raise NotImplementedError(f"Cannot compare {self} and {other}")
        return Expression(int(self) == int(other))

    # logical operators
    def and_(self, other: object) -> Expression:
        if not isinstance(other, Expression):
            raise NotImplementedError(f"Cannot compare {self} and {other}")
        return Expression(bool(self) and bool(other))

    def or_(self, other: object) -> Expression:
        if not isinstance(other, Expression):
            raise NotImplementedError(f"Cannot compare {self} and {other}")
        return Expression(bool(self) or bool(other))


CONST_TRUE = Expression(True)
CONST_FALSE = Expression(False)
