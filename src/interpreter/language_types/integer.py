from typing import TYPE_CHECKING

from interpreter.exceptions import IncompatibleTypesError, LanguageValueError, LanguageZeroDivisionError
from interpreter.language_types.base_type import LanguageType
from interpreter.language_types.boolean import BooleanType
from interpreter.language_types.float import FloatType

if TYPE_CHECKING:
    from typing import Any


class IntegerType(FloatType):
    type_name = "integer"

    def _parse_value(self, value: "Any") -> int:
        if isinstance(value, int):
            return value
        if isinstance(value, str):
            return int(value)
        raise LanguageValueError(type_name=self.type_name, value=value)

    # unary operators
    def __neg__(self) -> "IntegerType":
        return IntegerType(-self.value)

    def __pos__(self) -> "IntegerType":
        return IntegerType(+self.value)

    # arithmetic operators
    def __add__(self, other: "Any") -> "IntegerType | FloatType":
        if isinstance(other, IntegerType):
            return IntegerType(self.value + other.value)
        if isinstance(other, FloatType):
            return FloatType(self.value + other.value)
        raise IncompatibleTypesError(
            operand="+",
            type_1=self.type_name,
            type_2=other.type_name,
        )

    def __sub__(self, other: "Any") -> "IntegerType | FloatType":
        if isinstance(other, IntegerType):
            return IntegerType(self.value - other.value)
        if isinstance(other, FloatType):
            return FloatType(self.value - other.value)
        raise IncompatibleTypesError(
            operand="-",
            type_1=self.type_name,
            type_2=other.type_name,
        )

    def __mul__(self, other: "Any") -> "IntegerType | FloatType":
        if isinstance(other, IntegerType):
            return IntegerType(self.value * other.value)
        if isinstance(other, FloatType):
            return FloatType(self.value * other.value)
        raise IncompatibleTypesError(
            operand="*",
            type_1=self.type_name,
            type_2=other.type_name,
        )

    def __truediv__(self, other: "Any") -> "IntegerType | FloatType":
        try:
            if isinstance(other, IntegerType):
                return IntegerType(self.value // other.value)
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
        if isinstance(other, (IntegerType, FloatType)):
            return BooleanType(self.value > other.value)
        raise IncompatibleTypesError(
            operand=">",
            type_1=self.type_name,
            type_2=other.type_name,
        )

    def __lt__(self, other: "Any") -> "BooleanType":
        if isinstance(other, (IntegerType, FloatType)):
            return BooleanType(self.value < other.value)
        raise IncompatibleTypesError(
            operand="<",
            type_1=self.type_name,
            type_2=other.type_name,
        )

    def is_greater_than(self, other: "Any") -> "LanguageType":
        if isinstance(other, LanguageType):
            return BooleanType(self.value > other.value)
        raise IncompatibleTypesError(
            operand=">",
            type_1=self.type_name,
            type_2=other.type_name,
        )

    def is_equal(self, other: "Any") -> "BooleanType":
        if isinstance(other, (IntegerType, FloatType)):
            return BooleanType(self.value == other.value)
        raise IncompatibleTypesError(
            operand="==",
            type_1=self.type_name,
            type_2=other.type_name,
        )
