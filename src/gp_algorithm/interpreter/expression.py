from __future__ import annotations

from gp_algorithm.interpreter.exceptions import LanguageZeroDivisionError


class Expression:
    def __init__(
        self,
        bool_value: bool | None = None,
        int_value: int | None = None,
    ) -> None:
        self._bool_value = bool_value
        self._int_value = int_value

    @property
    def boolean(self) -> bool:
        if self._bool_value is not None:
            return self._bool_value

        if self._int_value is None:
            raise NotImplementedError("Unknown expression type")

        return self._int_value > 0

    @property
    def integer(self) -> int:
        if self._int_value is None:
            return bool(self._bool_value)
        return self._int_value

    def __str__(self) -> str:
        if self._bool_value is True:
            return "true"
        if self._bool_value is False:
            return "false"
        if self._int_value is not None:
            return str(self._int_value)
        raise NotImplementedError("Unknown expression type")

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Expression):
            raise NotImplementedError(f"Cannot compare {self} and {other}")
        return all(
            (
                self._int_value == other._int_value,
                self._bool_value == other._bool_value,
            ),
        )

    # unary operators
    def __neg__(self) -> Expression:
        return Expression(int_value=-self.integer)

    def __invert__(self) -> Expression:
        return Expression(bool_value=not self.boolean)

    # arithmetic operators
    def __add__(self, other: object) -> Expression:
        if not isinstance(other, Expression):
            raise NotImplementedError(f"Cannot add {self} and {other}")
        return Expression(int_value=self.integer + other.integer)

    def __sub__(self, other: object) -> Expression:
        if not isinstance(other, Expression):
            raise NotImplementedError(f"Cannot subtract {self} and {other}")
        return Expression(int_value=self.integer - other.integer)

    def __mul__(self, other: object) -> Expression:
        if not isinstance(other, Expression):
            raise NotImplementedError(f"Cannot multiply {self} and {other}")
        return Expression(int_value=self.integer * other.integer)

    def __truediv__(self, other: object) -> Expression:
        if not isinstance(other, Expression):
            raise NotImplementedError(f"Cannot divide {self} and {other}")
        try:
            return Expression(int_value=self.integer // other.integer)
        except ZeroDivisionError:
            raise LanguageZeroDivisionError()

    # comparison operators
    def is_greater_than(self, other: object) -> Expression:
        if not isinstance(other, Expression):
            raise NotImplementedError(f"Cannot compare {self} and {other}")
        return Expression(bool_value=self.integer > other.integer)

    def is_equal(self, other: object) -> Expression:
        if not isinstance(other, Expression):
            raise NotImplementedError(f"Cannot compare {self} and {other}")
        return Expression(bool_value=self.integer == other.integer)

    # logical operators
    def and_(self, other: object) -> Expression:
        if not isinstance(other, Expression):
            raise NotImplementedError(f"Cannot compare {self} and {other}")
        return Expression(bool_value=self.boolean and other.boolean)

    def or_(self, other: object) -> Expression:
        if not isinstance(other, Expression):
            raise NotImplementedError(f"Cannot compare {self} and {other}")
        return Expression(bool_value=self.boolean or other.boolean)


CONST_TRUE = Expression(bool_value=True)
CONST_FALSE = Expression(bool_value=False)
