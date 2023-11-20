from typing import TYPE_CHECKING

from interpreter.exceptions import IncompatibleTypesError, LanguageValueError, LanguageZeroDivisionError
from interpreter.types.base_type import LanguageType
from interpreter.types.boolean import BooleanType

if TYPE_CHECKING:
    from typing import Any


class FloatType(LanguageType):
    type_name = "float"

    def _parse_value(self, value: "Any") -> float:
        if isinstance(value, float):
            return value
        if isinstance(value, str):
            return float(value)
        raise LanguageValueError(type_name=self.type_name, value=value)

    # unary operators
    def __neg__(self) -> "FloatType":
        return FloatType(-self.value)

    def __pos__(self) -> "FloatType":
        return FloatType(+self.value)

    # arithmetic operators
    def __add__(self, other: "Any") -> "FloatType":
        if isinstance(other, FloatType):
            return FloatType(self.value + other.value)
        raise IncompatibleTypesError(
            operand="+",
            type_1=self.type_name,
            type_2=other.type_name,
        )

    def __sub__(self, other: "Any") -> "FloatType":
        if isinstance(other, FloatType):
            return FloatType(self.value - other.value)
        raise IncompatibleTypesError(
            operand="-",
            type_1=self.type_name,
            type_2=other.type_name,
        )

    def __mul__(self, other: "Any") -> "FloatType":
        if isinstance(other, FloatType):
            return FloatType(self.value * other.value)
        raise IncompatibleTypesError(
            operand="*",
            type_1=self.type_name,
            type_2=other.type_name,
        )

    def __truediv__(self, other: "Any") -> "FloatType":
        try:
            if isinstance(other, FloatType):
                return FloatType(self.value / other.value)
        except ZeroDivisionError:
            raise LanguageZeroDivisionError()
        raise IncompatibleTypesError(
            operand="/",
            type_1=self.type_name,
            type_2=other.type_name,
        )

    # comparison operators
    def __gt__(self, other: "Any") -> "BooleanType":
        if isinstance(other, FloatType):
            return BooleanType(self.value > other.value)
        raise IncompatibleTypesError(
            operand=">",
            type_1=self.type_name,
            type_2=other.type_name,
        )

    def __lt__(self, other: "Any") -> "BooleanType":
        if isinstance(other, FloatType):
            return BooleanType(self.value < other.value)
        raise IncompatibleTypesError(
            operand="<",
            type_1=self.type_name,
            type_2=other.type_name,
        )

    def is_equal(self, other: "Any") -> "BooleanType":
        if isinstance(other, FloatType):
            return BooleanType(self.value == other.value)
        raise IncompatibleTypesError(
            operand="==",
            type_1=self.type_name,
            type_2=other.type_name,
        )

    def is_not_equal(self, other: "Any") -> "BooleanType":
        if isinstance(other, FloatType):
            return BooleanType(self.value != other.value)
        raise IncompatibleTypesError(
            operand="!=",
            type_1=self.type_name,
            type_2=other.type_name,
        )
