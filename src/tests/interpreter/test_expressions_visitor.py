from typing import Callable

import pytest

from antlr.LanguageParser import LanguageParser
from interpreter.exceptions import IncompatibleTypesError, LanguageZeroDivisionError
from interpreter.types.base_type import LanguageType
from interpreter.types.boolean import CONST_FALSE, CONST_TRUE
from interpreter.types.float import FloatType
from interpreter.types.integer import IntegerType
from interpreter.visitors.main import Visitor


@pytest.mark.parametrize(
    ("input_string", "expected_result"),
    [
        ("2", IntegerType(2)),
        ("2 + 5 * 7", IntegerType(37)),
        ("2 * 5 - 7", IntegerType(3)),
        ("0 * 190", IntegerType(0)),
        ("100 / 30", IntegerType(3)),
        ("2. * 2.", FloatType(4.0)),
        ("2. * 2", FloatType(4.0)),
        ("0. * 190", FloatType(0.0)),
        ("100. / 30", FloatType(100 / 30)),
        ("100. - 7 / (5 + 2)", FloatType(99.0)),
        ("100 > 10 and true", CONST_TRUE),
        ("1 > 2", CONST_FALSE),
        ("1 < 2", CONST_TRUE),
        ("2. > 2", CONST_FALSE),
        ("2 < 2.", CONST_FALSE),
        ("2 > 1.", CONST_TRUE),
        ("2. < 1.", CONST_FALSE),
        ("2 == 2", CONST_TRUE),
        ("2. == 2", CONST_TRUE),
        ("2 == 2.", CONST_TRUE),
        ("2. == 2.", CONST_TRUE),
        ("2 == 1", CONST_FALSE),
        ("2. == 1", CONST_FALSE),
        ("2 == 1.", CONST_FALSE),
        ("2. == 1.", CONST_FALSE),
        ("2 != 2.1", CONST_TRUE),
        ("2. != 2.1", CONST_TRUE),
        ("2 != 2.0", CONST_FALSE),
        ("2. != 2.0", CONST_FALSE),
        ("2 != 2", CONST_FALSE),
        ("true == true", CONST_TRUE),
        ("true == false", CONST_FALSE),
        ("false == true", CONST_FALSE),
        ("false == false", CONST_TRUE),
        ("true != true", CONST_FALSE),
        ("true != false", CONST_TRUE),
        ("false != true", CONST_TRUE),
        ("false != false", CONST_FALSE),
        ("true", CONST_TRUE),
        ("false", CONST_FALSE),
        ("true and false or true", CONST_FALSE),
        ("true or false and false", CONST_TRUE),
        ("(true or false) and true", CONST_TRUE),
    ],
)
def test_visit_expression(
    input_string: str,
    expected_result: LanguageType,
    get_parser_from_input: Callable[[str], LanguageParser],
    visitor: Visitor,
) -> None:
    parser = get_parser_from_input(input_string)
    expression_ctx = parser.expression()

    result = visitor.visit(expression_ctx)
    assert result == expected_result


@pytest.mark.parametrize(
    "input_string",
    [
        "1 / 0",
        "1/0",
        "4 / 0",
        "1 / 0.",
        "1. / 0",
        "1. / 0.",
    ],
)
def test_visit_expression_divide_by_zero(
    input_string: str,
    get_parser_from_input: Callable[[str], LanguageParser],
    visitor: Visitor,
) -> None:
    parser = get_parser_from_input(input_string)
    expression_ctx = parser.expression()

    with pytest.raises(LanguageZeroDivisionError):
        visitor.visit(expression_ctx)


@pytest.mark.parametrize(
    "input_string",
    [
        "true < 1",
        "1 == true",
        "(1 > 1) + 1",
    ],
)
def test_visit_expression_incompatible_types(
    input_string: str,
    get_parser_from_input: Callable[[str], LanguageParser],
    visitor: Visitor,
) -> None:
    parser = get_parser_from_input(input_string)
    expression_ctx = parser.expression()

    with pytest.raises(IncompatibleTypesError):
        visitor.visit(expression_ctx)
