from typing import TYPE_CHECKING

from interpreter.exceptions import IncompatibleTypesError, LanguageValueError
from interpreter.language_types.base_type import LanguageType

if TYPE_CHECKING:
    from typing import Any


class BooleanType(LanguageType):
    type_name = "boolean"
    true_values = {"true"}
    false_values = {"false"}

    def _parse_value(self, value: "Any") -> bool:
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            if value in self.true_values:
                return True
            if value in self.false_values:
                return False
        raise LanguageValueError(type_name=self.type_name, value=value)

    # unary operators
    def __invert__(self) -> "BooleanType":
        return BooleanType(not self.value)

    # comparison operators
    def is_greater_than(self, other: "Any") -> "LanguageType":
        if isinstance(other, LanguageType):
            return BooleanType(self.value > other.value)
        raise IncompatibleTypesError(
            operand=">",
            type_1=self.type_name,
            type_2=other.type_name,
        )

    def is_equal(self, other: "Any") -> "BooleanType":
        if isinstance(other, BooleanType):
            return BooleanType(self.value is other.value)
        raise IncompatibleTypesError(
            operand="==",
            type_1=self.type_name,
            type_2=other.type_name,
        )

    # logical operators
    def __and__(self, other: "Any") -> "BooleanType":
        if isinstance(other, BooleanType):
            return BooleanType(self.value and other.value)
        raise IncompatibleTypesError(
            operand="and",
            type_1=self.type_name,
            type_2=other.type_name,
        )

    def __or__(self, other: "Any") -> "BooleanType":
        if isinstance(other, BooleanType):
            return BooleanType(self.value or other.value)
        raise IncompatibleTypesError(
            operand="or",
            type_1=self.type_name,
            type_2=other.type_name,
        )


CONST_TRUE = BooleanType(True)
CONST_FALSE = BooleanType(False)
